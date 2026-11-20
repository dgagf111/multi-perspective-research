# STORM 提问机制的执行细节 —— 一次完整运行的逐步追踪

> 目标：把"多个独立先验、受外部证据约束、带预算与负反馈的探索过程"拆成**可执行的动作序列**，每一步都对应真实代码。
> 代码基线：`stanford-oval/storm` @ `fb951af`。本页记录参考实现。当前执行规则和预算见 [主文](../SKILL.md)。

---

## 0. 总控：谁在驱动这个循环

`STORMWikiRunner.run()` 串起四个阶段（`_research/storm/knowledge_storm/storm_wiki/engine.py:341-441`）：

```
run()
 ├─ run_knowledge_curation_module()   ← 提问引擎在这里
 │    └─ StormKnowledgeCurationModule.research()
 │         ├─ _get_considered_personas()      [先验生成]
 │         └─ _run_conversation()             [并行探索]
 │              └─ ConvSimulator.forward()    [单条对话线]
 │                   ├─ WikiWriter.forward()          [提问]
 │                   └─ TopicExpert.forward()         [检索+回答]
 ├─ run_outline_generation_module()   ← 收敛一：结构
 ├─ run_article_generation_module()   ← 收敛二：正文
 └─ run_article_polishing_module()    ← 收敛三：摘要+去重
```

关键参数（默认值，`engine.py:127-168`）：

| 参数 | 默认 | 含义 |
|---|---|---|
| `max_perspective` | 3 | 额外 perspective 数（+1 基本事实 = 4 条线） |
| `max_conv_turn` | 3 | 每条线的最大提问轮数 |
| `max_search_queries_per_turn` | 3 | 每次提问拆成的查询数 |
| `search_top_k` | 3 | 每个查询取几条结果 |
| `retrieve_top_k` | 3 | 写每节时从信息表捞几条 |
| `max_thread_num` | 10 | 并行线程 |

**总检索预算** = 4 条线 × 3 轮 × 3 查询 × 3 结果 = **108 条候选**（去重前）。

---

## 1. 阶段 A：先验生成（`_get_considered_personas`）

### 执行步骤（`persona_generator.py:77-111`）

**A1. 让 LLM 提名同类条目**（`FindRelatedTopic`，`:48-53`）
```
输入: topic = "2022 Winter Olympics opening ceremony"
输出: related_topics = "1. https://en.wikipedia.org/wiki/2008_Summer_Olympics_opening_ceremony
                        2. https://en.wikipedia.org/wiki/2012_Summer_Olympics_opening_ceremony
                        ..."
```

**A2. 真实抓取这些页面的结构**（`get_wiki_page_title_and_toc`，`:10-45`）
- 用 `requests` + `BeautifulSoup` 真实拉取
- 提取 H1 作标题
- 遍历 h2–h6，**用 `levels` 栈计算层级缩进**（`:38-43`），生成缩进 TOC
- 排除 `Contents / See also / Notes / References / External links`

> ⚠️ **这一步是全部价值的来源**。`examples` 不是 LLM 编的，是从真实世界读出来的结构。若抓取失败，`examples = ["N/A"]`（`:93-94`）—— 此时先验退化为纯参数化知识，正交性立刻崩塌。

**A3. 用 TOC 语料生成 persona**（`GenPersona`，`:56-65`）
```
输入: topic + "\n----------\n".join(examples)   # 多个真实 TOC
输出: "1. Event planner: focuses on preparation, logistics and budget
       2. Cultural commentator: focuses on symbolic and artistic elements"
```

**A4. 解析 + 补兜底**（`:99-103`，`:152-153`）
```python
personas = [re.search(r"\d+\.\s*(.*)", s).group(1) for s in output.split("\n") if match]
personas = ["Basic fact writer: ..."] + personas[:max_num_persona]
```

### 这一步的可复刻要点

| 要点 | 原因 |
|---|---|
| 先验必须锚定外部结构 | 否则所有 persona 是同一先验的措辞变体 |
| 至少抓 2 个同类结构 | 单个 TOC 会把所有 persona 拉向同一模板 |
| 必须有第 0 号兜底先验 | 保证覆盖度下限，防止全员专业化导致基本事实缺失 |
| **不要求**先验数量多 | 3+1 就够；质量（正交性）远比数量重要 |

---

## 2. 阶段 B：并行探索（`_run_conversation`）

### B0. 线程池扇出（`knowledge_curation.py:315-345`）

```python
max_workers = min(self.max_thread_num, len(considered_personas))
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_persona = {executor.submit(run_conv, p): p for p in considered_personas}
    for future in as_completed(future_to_persona):
        conv = future.result()
        conversations.append((persona, clean_up_citation(conv).dlg_history))
```

> **注意：4 条线之间零通信**。这正是"独立先验"的工程保证 —— 它们只能在**事后**（信息表合并时）相遇。任何中途共享都会破坏独立性。

### B1. 单条对话线的循环（`ConvSimulator.forward`，`knowledge_curation.py:47-81`）

```python
dlg_history = []
for _ in range(self.max_turn):                       # ← 预算：M 轮
    user_utterance = self.wiki_writer(
        topic, persona, dlg_history).question        # ← 提问
    if user_utterance == "":
        break                                        # ← 异常退出
    if user_utterance.startswith("Thank you so much for your help!"):
        break                                        # ← 模型自判终止
    expert_output = self.topic_expert(topic, user_utterance, ground_truth_url)
    dlg_turn = DialogueTurn(
        agent_utterance = expert_output.answer,
        user_utterance  = user_utterance,
        search_queries  = expert_output.queries,     # ← 保留查询，供追溯
        search_results  = expert_output.searched_results,
    )
    dlg_history.append(dlg_turn)                     # ← 答案进入下一轮上下文
    callback_handler.on_dialogue_turn_end(dlg_turn)
```

**三层终止条件**：轮数耗尽 / 模型自判 / 空输出。这是"预算"的完整实现。

### B2. 提问（`WikiWriter.forward`，`knowledge_curation.py:95-125`）

上下文装配是这里最关键的技术细节：

```python
conv = []
for turn in dialogue_turns[:-4]:                     # 远期：只留问句
    conv.append(f"You: {turn.user_utterance}\nExpert: Omit the answer here due to space limit.")
for turn in dialogue_turns[-4:]:                     # 近期：保留答案
    conv.append(f"You: {turn.user_utterance}\nExpert: {remove_citations(turn.agent_utterance)}")
conv = limit_word_count_preserve_newline(conv, 2500)  # 硬预算
```

Prompt（`AskQuestionWithPersona`，`:139-151`）：
```
You are an experienced Wikipedia writer and want to edit a specific page. Besides your
identity as a Wikipedia writer, you have specific focus when researching the topic.     ← 先验注入点
Now, you are chatting with an expert to get information. Ask good questions to get more
useful information.
When you have no more question to ask, say "Thank you so much for your help!" to end
the conversation.                                                                        ← 显式退出令牌
Please only ask a question at a time and don't ask what you have asked before.           ← 反重复
Your questions should be related to the topic you want to write.                         ← 反漂移
```

四条约束缺一不可：**先验接线 / 退出令牌 / 反重复 / 反漂移**。

### B3. 检索与作答（`TopicExpert.forward`，`knowledge_curation.py:204-244`）

```python
# ① 问题 → 查询（QuestionToQuery）
queries = self.generate_queries(topic=topic, question=question).queries
queries = [q.replace("-","").strip().strip('"') for q in queries.split("\n")][:max_search_queries]
# ② 检索（去重 + 排除 ground truth）
searched_results = self.retriever.retrieve(list(set(queries)), exclude_urls=[ground_truth_url])
# ③ 分支：有结果 / 无结果
if len(searched_results) > 0:
    info = ""                                        # 每个来源只取 top-1 snippet
    for n, r in enumerate(searched_results):
        info += "\n".join(f"[{n+1}]: {s}" for s in r.snippets[:1]) + "\n\n"
    info = limit_word_count_preserve_newline(info, 1000)   # ← 预算：1000 词
    answer = self.answer_question(topic=topic, conv=question, info=info).answer
    answer = remove_uncompleted_sentences_with_citations(answer)
else:
    answer = "Sorry, I cannot find information for this question. Please ask another question."
```

**负反馈回路就在这里**（`:238-240`）：检索为零 → 返回一句显式拒答 → 这句话被 B1 写进 `dlg_history` → 下一轮提问的 prompt 里就带着"你上次问的东西查不到"。

> 没有 reward model、没有打分、没有重试。**检索器本身就是 critic**，拒答文本就是梯度信号。

### B4. 来源过滤（`Retriever.retrieve` → `rm.forward`）

`YouRM.forward`（`_research/storm/knowledge_storm/rm.py:67`）：
```python
if self.is_valid_source(r["url"]) and r["url"] not in exclude_urls:
```
默认 `is_valid_source = is_valid_wikipedia_source`（`storm_wiki/modules/retriever.py:225-233`），命中三张黑名单即丢弃。

**语义**：这是**先验可信度**（硬编码、静态），不是收敛得出的可信度。两者必须区分——黑名单负责"不要垃圾"，收敛负责"什么是真的"。

---

## 3. 阶段 C：结构化沉淀（`StormInformationTable`）

### C1. 以 URL 为主键合并（`storm_dataclass.py:65-80`）

```python
for persona, conv in conversations:
    for turn in conv:
        for storm_info in turn.search_results:
            if storm_info.url in url_to_info:
                url_to_info[storm_info.url].snippets.extend(storm_info.snippets)
            else:
                url_to_info[storm_info.url] = storm_info
for url in url_to_info:
    url_to_info[url].snippets = list(set(url_to_info[url].snippets))
```

**这里是"多维度收敛"的第一个物理落点**，但也是最大的信息损失点：

- ✅ 同一 URL 被多条线命中 → snippet 并集
- ❌ **丢掉了"是哪些 persona / 哪些 query 命中了它"**
- ❌ `list(set(...))` 无序 → 后续 1000 词截断时"先到先得"，优先级随机

**后果**：被 4 条独立路径命中的来源，和被 1 条路径命中的来源，在下游权重完全相同。

### C2. 信息表 → 大纲（`outline_generation.py:75-125`）

两阶段，这是"内部先验 × 外部证据"的乘积：

```python
# 阶段 1：纯参数化知识
old_outline = clean_up_outline(self.draft_page_outline(topic=topic).outline)
# 阶段 2：用全部对话修正
outline = clean_up_outline(
    self.write_page_outline(topic=topic, old_outline=old_outline, conv=conv).outline
)
```

其中 `conv` = 所有对话线拼接，`remove_citations` 后截断到 **5000 词**（`:105-106`）。

### C3. 大纲 → 正文（`article_generation.py:53-133`）

```python
for section_title in sections_to_write:
    section_query    = article.get_outline_as_list(root_section_name=section_title, add_hashtags=False)
    section_outline  = "\n".join(article.get_outline_as_list(section_title, add_hashtags=True))
    # ↓ 用 section 标题当 query，从信息表里语义检索素材
    collected_info = information_table.retrieve_information(queries=section_query, search_top_k=3)
```

`prepare_table_for_retrieval()` 用 `paraphrase-MiniLM-L6-v2` 编码全部 snippet，`retrieve_information` 做余弦相似度 top-k（`storm_dataclass.py:109-145`）。

### C4. 引用裁剪（`storm_dataclass.py:267-288`）

```python
references = {int(x) for x in re.findall(r"\[(\d+)\]", current_section_content)}
# 越界的引用编号直接删除
if max_ref_num > len(current_section_info_list):
    for i in range(len(current_section_info_list), max_ref_num + 1):
        current_section_content = current_section_content.replace(f"[{i}]", "")
# 未被引用的来源，从列表里剔除
index_to_keep = [i - 1 for i in references]
```

**收敛的最后一刀**：只有正文真正用到的来源，才进入最终参考列表。

---

## 4. 完整执行时序图（一次真实运行）

```
t=0   topic = "2022 Winter Olympics opening ceremony"
      │
t=1   ├─ [A1] LLM 提名 5 个同类条目
t=2   ├─ [A2] requests 抓取 5 个页面的 H1+TOC  ← 网络 IO，可能失败
t=3   ├─ [A3] LLM 基于 TOC 生成 persona 列表
t=4   ├─ [A4] 拼接 → P = [Basic fact writer, Event planner, Cultural commentator, ...]
      │
t=5   ├─ [B0] ThreadPoolExecutor 启动 4 条并行线
      │        ╔═════════╦═════════╦═════════╦═════════╗
      │        ║ P0      ║ P1      ║ P2      ║ P3      ║   ← 零通信
      │        ╚════╤════╩════╤════╩════╤════╩════╤════╝
      │             │         │         │         │
t=6   ├─ [B2] 提问 q1  (每条线各问一个)
t=7   ├─ [B3] q1 → 3 个查询 → 检索 9 结果 → 1000 词截断 → 带引用作答 a1
t=8   ├─ [B1] dlg_history.append({q1, a1, queries, results})
      │             │
t=9   ├─ [B2] 提问 q2  (上下文 = 裁剪后的 dlg_history)  ← 追问在此发生
t=10  ├─ [B3] q2 → ...      ┌─ 若检索为 0：注入 "Sorry, I cannot find..."  ← 负反馈
      │                     └─ 若模型判断问够了：注入 "Thank you so much for your help!"
t=11  ├─ [B1] ... 直到 3 轮耗尽 / 自判终止 / 空输出
      │        ╔═════════╩═════════╩═════════╩═════════╗
      │        ╚═════════════════╤═════════════════════╝
t=12  ├─ [C1] 合并：url → snippets (并集，去重)     ← 此处发生收敛，但来源归属被丢弃
t=13  ├─ [C2] draft outline (纯先验) → final outline (先验 × 对话)
t=14  ├─ [C3] 逐节：section 标题当 query → 语义检索素材 → 生成带引用正文
t=15  └─ [C4] 引用裁剪 → 最终参考列表

输出: conversation_log.json / raw_search_results.json /
      direct_gen_outline.txt / storm_gen_outline.txt /
      storm_gen_article.txt / url_to_info.json
```

---

## 5. 四个机制的可执行定义

把上面全部细节抽象出来，这四个机制就是复刻清单：

### ① 多个独立先验

| 必须做的 | 反例 |
|---|---|
| 从**外部结构**读出维度 | 让模型"想三个角度" |
| 每条线**独立**跑完，中途不通信 | 共享一个 growing context |
| 有**兜底维度**保底 | 全部专业化 |
| 主动**检查正交性** | 假设 prompt 说的"different"真的生效 |

> STORM 只做了前三条，第四条没做 —— 这是它的第一个缺口。

### ② 受外部证据约束

| 约束 | STORM 的实现 |
|---|---|
| 提问必须落成可检索查询 | `QuestionToQuery` 拆解 |
| 答案必须基于检索结果 | `AnswerQuestion` 的 "every sentence is supported" |
| 无证据时明确拒答 | "I cannot find information for this question" |
| 来源域有前置过滤 | 三张 Wikipedia 黑名单 |
| **矛盾检测** | ❌ STORM 完全没有 |

### ③ 预算

| 预算项 | STORM 默认值 | 代码 |
|---|---|---|
| 先验数 | 3 (+1) | `max_perspective` |
| 每条线轮数 | 3 | `max_conv_turn` |
| 每轮查询数 | 3 | `max_search_queries_per_turn` |
| 每查询结果数 | 3 | `search_top_k` |
| 每轮证据词数 | 1000 | `limit_word_count_preserve_newline(info, 1000)` |
| 对话上下文词数 | 2500 | `limit_word_count_preserve_newline(conv, 2500)` |
| 大纲上下文词数 | 5000 | `limit_word_count_preserve_newline(conv, 5000)` |
| 写每节素材词数 | 1500 | `limit_word_count_preserve_newline(info, 1500)` |
| 并行度 | 10 | `max_thread_num` |

**预算不是优化，是机制**：它把"无限追问"变成"必须在有限轮次内问到点子上"，这本身就是对提问质量的隐性压力。

### ④ 负反馈

| 信号 | 产生方式 | 消费方式 |
|---|---|---|
| 检索为零 | 检索器返回空 | 拒答文本写回对话历史 |
| 提问重复 | prompt 约束 | 只是 prompt，**无检测** |
| 话题漂移 | prompt 约束 | 只是 prompt，**无检测** |
| 方向停滞（Co-STORM） | 连续 3 轮无提问 | 强制 Moderator 接管 |

> STORM 有"点状负反馈"（单次检索失败），**没有"线状负反馈"**（整条线跑偏了没人管）。这是第二个缺口。

---

## 6. 上游实现与本技能关注的问题

| 机制 | STORM 做了什么 | 缺什么 | 后果 |
|---|---|---|---|
| 独立性 | 4 条线程零通信 | 无正交性检查 | 维度重叠时静默塌缩 |
| 收敛 | URL 主键并集 | 不记录来源归属 | 无法计算"独立确证数" |
| 矛盾 | 无 | 无跨源矛盾检测 | 冲突证据被并集平铺 |
| 反馈 | 单次检索拒答 | 无整线级信号 | 跑偏的线会烧完全部预算 |
| 交付 | `run_article_polishing_module()`：摘要 + 去重 | **没有"面向读者的重写"这一步** | 产物是流程的副产品，读者读的是机制 |

当前技能把检索路径作为覆盖记录，按每条结论追溯原始依据，对齐口径后再核查分歧。

### 关于"交付"这一条，需要区分 STORM 的 polishing 与 Step 6

STORM 的 `run_article_polishing_module()` 做的是**机械收敛**：抽摘要、去重、合并重复引用。它优化的是**文档内部的一致性**，不是**文档与读者之间的距离**。它不会：

- 删除机制词汇（因为它的读者被假定为流程参与者，或至少不介意）；
- 写清每条结论的独立来源、单源限制和查证缺口；
- 为每一级证据重建"哪些可当事实、哪些只是线索"的章节结构；
- 检查压缩过程中是否丢了限定语。

本技能用底稿保留可追溯的取证过程，用读者稿说明结论和适用范围。成稿验收包含引用结构校验和逐条证据复核，见 [读者稿与验收](reader-report.md)。

---

## 7. 一句话

> STORM 的提问循环 = `(先验 × 预算) → 检索 → (证据 | 拒答) → 写回上下文 → 再提问`，
> 重复 `M` 轮、并行 `N+1` 条线，
> 最后所有线在 **URL 主键**处相遇一次 —— 收敛只发生这一次，而且是副产品。
