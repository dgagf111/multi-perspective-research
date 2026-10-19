# multi-perspective-research

> 多视角交叉验证深度调研 —— 给每条结论标注「多来源印证 / 单一来源 / 存在冲突 / 检索未找到」。

一个**自包含的 Markdown 指令包**：带 frontmatter 的 `SKILL.md`，加上按需加载的 `references/`。任何支持 SKILL.md 约定的 agent（DeepSeek Harness、Claude Code、ZCode 等）把目录丢进 skills 根目录即可生效，不依赖任何二进制、密钥或网络服务。

---

## 它解决什么问题

普通搜索回答的是「**网上关于 X 怎么说**」。这个 Skill 回答的是「**X 里哪一部分有多个独立来源互相印证，哪一部分只有一个人说过**」。

可靠性不是来源的属性，是**独立路径在同一处相遇**的属性。派几个背景完全不同的调研线分头去查、**互不通气**，最后看哪几条各自独立地落到了同一个结论上 —— 那才算数。一条线把同一个页面找了十遍，那是一条线，不是十个来源。

### 证据收敛等级

| 等级 | 含义 |
|---|---|
| A 收敛 | 多条互不通信的独立路径落到同一结论 |
| B 确证 | 至少两个独立域名印证 |
| C 单源 | 只有一个来源说过，标注为单源 |
| D 争议 | 不同来源互相矛盾，把冲突摊开写 |
| E 未找到 | 检索预算用完仍无来源能回答，直说「没有来源能回答」 |

---

## 六步流程

1. **不查内容，先查结构** —— 去读维基百科章节、同行文档目录、监管文件分类等 2~4 个真实东西，从它们的**结构**里读出正交视角。自己想出来的「三个角度」往往只是同一个角度戴三顶帽子。
2. **先写死预算** —— 3 视角 + 1 常识底线视角，每视角 3 轮，每问 2~3 个查询 ≈ 36 次检索。预算用完是设计好的事件，不是意外。
3. **并行取证，线间不通信** —— 摘要只是线索必须真抓页面；搜不到就写「没有来源能回答」，禁止用模型记忆补坑。
4. **碰头打分** —— 按域名而非 URL 聚类；每条断言标 A/B/C/D/E 五个证据等级。
5. **写两份文件** —— `working-report.md`（机制可见，可审计）+ `reader-report.md`（机制不可见，给人看）。
6. **独立 pass 改写 + 机械终检** —— 查机制泄漏、引用对齐、等级保真、无新增事实。

最终回复 = `reader-report.md` 全文原样，不额外加料。

细节见 [SKILL.md](SKILL.md)。

---

## 安装

### Claude Code / 通用 SKILL.md 宿主

```bash
git clone https://github.com/dgagf111/multi-perspective-research.git
cp -r multi-perspective-research <你的 skills 根目录>/
```

`skills 根目录`按宿主而定，常见位置：

| 宿主 | 默认位置 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| ZCode | `~/.zcode/skills/`（或 `ZCODE_SKILLS_ROOT`） |
| agents 标准 | `~/.agents/skills/` |
| DeepSeek Harness | `~/.dsh/skills/` |

### DeepSeek Harness

在 Settings → Skills 中添加本仓库路径，或直接把本目录复制到工作区的 skills 目录。

### 不想装，只想读

直接读 [`SKILL.md`](SKILL.md) —— 它是自解释的。

---

## 依赖说明

本 Skill 本身不含代码，检索能力由宿主的搜索工具提供。文中以 `anysearch` / `agent-reach` 作为检索后端举例，换成宿主的 `web_search` / `web_fetch` 同样成立。

---

## 仓库结构

```
multi-perspective-research/
├── README.md              本文件（中文）
├── README.en.md           English version
├── LICENSE                MIT
├── SKILL.md               主指令（可直接放进 skills 根目录）
└── references/
    ├── execution-trace.md STORM 源码级执行追踪（本流程的来源）
    └── reader-report.md   Step 6 完整规格 + 五项终检
```

## License

[MIT](LICENSE) © dgagf111

本仓库借鉴并明确标注了 [Stanford STORM](https://github.com/stanford-oval/storm) 的提问机制，`references/execution-trace.md` 记录了其源码级参数与本 Skill 相对 STORM 补齐的两处缺口。
