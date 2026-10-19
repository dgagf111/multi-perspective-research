---
name: multi-perspective-research
description: 多视角交叉验证深度调研——从外部真实结构读出多个正交视角，各视角独立并行检索取证，按显式预算收敛，产出带"证据收敛等级"（收敛/确证/单源/争议/未找到）的内部底稿，再由一个独立 pass 润色成机制不可见、附完整来源与交叉验证的读者稿 reader-report.md；该文件全文原样作为对用户的最终回复。触发条件（命中即用，无需点名本 skill）：用户说"深度调研 / 深度研究 / 深度分析 / 深入研究 / deep-research / deep research"，或提出同义要求——仔细调研、认真调研、调研得仔细一点、多查几个来源、确定性调研、要确定性结论、别只给一个来源、多维度调研、多视角、全景分析、正反双方梳理、交叉验证、多方观点对比、彻底搞清楚 X、把 X 查透、X 到底怎么样，或要求标注"哪些结论有多来源印证、哪些只有单一来源"。与 anysearch / agent-reach 的通用"调研/搜索"触发重叠时，凡带"深/仔细/确定性/交叉验证"限定词者以本 skill 为准。不适用于一次性快速查证（那用 anysearch 或 agent-reach 即可）。
---

# Multi-perspective research

A flat search answers "what does the web say about X". This skill answers "**which parts of X are independently corroborated, and which rest on a single source**".

The mechanism, abstracted from Stanford's STORM (verified against source at `stanford-oval/storm`):

```
(perspectives × budget) → retrieve → (evidence | refusal) → write back → ask again
     repeat M rounds, N+1 independent lanes, converge once at the end
                                  ↓
                 working-report.md (mechanism visible, audit trail)
                                  ↓
                 reader-report.md  (mechanism invisible, the product)
                                  ↓
        reply to user = reader-report.md verbatim, nothing added
```

The whole value sits in four places most research attempts skip: **perspectives must come from outside the model**, **every question must cash out as a real search**, **convergence must be scored, not assumed**, and **the scored result must then survive being read by someone who was not there**.

---

## When to trigger

Fire this skill on **any** of these, from the user's own words — the user never needs to name the skill:

- **Explicit tokens**: 深度调研 / 深度研究 / 深度分析 / 深入研究 / deep-research / deep research / deep dive / 深入调研。
- **Quality-adverb requests**: 仔细调研 / 认真调研 / 调研得仔细一点 / 多查几个来源 / 别只给一个来源 / 要确定性结论 / 确定性调研 / 查得踏实一点 / 帮我彻底搞清楚 X / 把 X 查透 / X 到底怎么样 / 不要泛泛而谈。
- **Method requests**: 多维度调研 / 多视角 / 全景分析 / 正反双方梳理 / 交叉验证 / 多方观点对比 / 交叉比对来源 / 标注"哪些结论有多来源印证、哪些只有单一来源"。
- **Implicit form**: any research request where the user signals that a one-shot answer is not enough.

Overlap rule: `anysearch` and `agent-reach` own generic 调研/搜索/查一下 (they are the retrieval backends and this skill uses them as tools). The moment the request carries a depth / care / certainty / cross-validation qualifier, **this skill owns the request** and drives those backends inside its lanes. When in doubt, prefer this skill: the cost of over-researching is time, the cost of under-researching is a confident wrong answer.

Not for: single quick fact checks, "查一下这个 API 是什么", or one-page lookups.

---

## The two artifacts

Steps 1–5 produce a **working report**: a mechanism-visible artifact where `lane`, `A–E`, `query`, `round` and orthogonality sentences are the whole point. It is correct, and it is unreadable to anyone who did not run it.

Step 6 produces the **reader report**: the thing you actually hand over. Same evidence, same honesty, same sources — but the machinery is gone, and the structure is rebuilt around what a reader needs to decide something.

**Keep both artifacts, and never let Step 6 replace Step 5.**

- The working report is the audit trail: it is what lets you (or a later pass) verify that no claim drifted, no level was upgraded, and no empty row was filled from memory. It is written to a file (e.g. `working-report.md`) and is **never** pasted into the reply.
- The reader report is the deliverable, saved as **`reader-report.md`**: it is what a person can actually use, in one sitting, without a glossary.

**Delivery rule (hard): the final reply to the user is the verbatim, complete content of `reader-report.md` — nothing added, nothing changed, nothing wrapped around it.** See §Delivery below. No preamble ("我做完了，下面是报告"), no sign-off, no summary, no verification line, no commentary describing what you did or which files exist. Read the file and emit exactly its bytes as your message body. Anything you feel like adding belongs in the working report, not in the reply.

Collapsing the two into one document fails in both directions. Keep the machinery and readers bounce off it; drop the machinery without Step 6's rules and the cross-validation silently disappears — the reader can no longer tell "four independent paths met here" from "one lucky hit got repeated", which was the entire point of the skill.

---

## Non-negotiables

1. **Perspectives are read, not invented.** You must derive them from real artifacts you fetched (existing reports, competitor docs, TOCs, forum categories, regulatory headings). Never just ask yourself "what are three angles on this".
2. **Every question must produce a search.** A question that cannot be decomposed into queries that hit real sources is not research, it is speculation. Say so and drop it.
3. **Lanes do not talk to each other while running.** Independence is the only thing that makes agreement informative. Convergence happens once, at the end.
4. **Refusal is a signal, not a failure.** When a lane's searches come back empty, record that and let it steer the next question. Do not fill the gap from parametric memory.
5. **Report corroboration level per claim.** "Three independent sources agree" and "one blog says so" must never look the same in the reader report.
6. **The mechanism is invisible in the reader report, but the evidence is not.** A reader must never need to know what a lane is; a reader must always be able to ask "who says so, and did anyone else say it".
7. **The reply is the reader report, unaltered.** The final message to the user is `reader-report.md` copied out in full — no preamble, no sign-off, no summary, no gate line, no commentary. If you want the user to see something different, change the file and re-emit it; never edit on the way out.

---

## Step 1 — Anchor the perspectives

**Do not start from the topic. Start from how this topic is already structured in the world.**

Fetch 2–4 real artifacts whose *structure* you can borrow:

| Topic kind | Where to read structure from |
|---|---|
| An entity, product, event | Its Wikipedia page sections + 2 neighbouring/competitor pages' sections |
| A market, industry | Two analyst report TOCs, a regulator's filing index, a conference agenda |
| A technical approach | The upstream docs' sidebar, two rival projects' README headings |
| A controversial issue | The strongest pro piece's headings, the strongest con piece's headings |
| A person, org | Their own site structure vs. critical coverage's structure |

Then derive **3 lanes** (plus lane 0, below). Each lane is a *different reason to care about the topic*, not a different subtopic:

- ✅ "Someone who has to operate this in production, caring about failure modes and cost"
- ✅ "Someone financially exposed to this decision, caring about who pays"
- ❌ "Technical aspects" / "Economic aspects" / "Social aspects" — these are the same prior wearing three hats

**Check orthogonality before spending budget.** For each pair of lanes, write one sentence: *"Lane A would ask X; would Lane B ever ask X?"* If yes for any pair, merge them and re-derive. If two lanes would generate the same first three questions, they are one lane. This check is the single highest-leverage minute in the whole procedure — skip it and you get four paraphrases of one search.

**Lane 0 is mandatory**: a plain "someone who needs the basic uncontroversial facts, dates, definitions, numbers" lane. It is the coverage floor that stops every other lane from being specialized into irrelevance.

Record the anchor artifacts and the orthogonality sentences; they go in the **working report** (Step 5) as the provenance of the perspective set. They do **not** appear in the reader report (Step 6).

## Step 2 — Set the budget before you spend it

Write the budget down explicitly, then obey it:

| Item | Default | Rationale |
|---|---|---|
| Lanes | 3 + lane 0 = **4** | More lanes dilute rather than diversify; 4 is the empirical sweet spot |
| Rounds per lane | **3** | Enough for one follow-up; beyond that a lane is usually lost |
| Queries per question | **2–3** | One query is a lottery ticket, five is a shotgun |
| Results per query | **3–5** | Read the top few, do not hoard |
| Words of evidence per round | **~1000** | Force yourself to keep the load-bearing sentences only |
| Words of lane context | **~2500** | Keeps recent detail, drops stale detail |
| Parallel lanes | **≤4** | Concurrency is the point; rate limits are the constraint |

Total retrieval budget ≈ `4 × 3 × 3 = 36` queries. When it is spent, stop searching and start converging. **Running out of budget is a designed event, not an accident.**

## Step 3 — Run the lanes in parallel, independently

Launch all lanes **in the same turn** — use parallel subagents when available (`subagent` / `workflow`), one per lane. Each lane gets: the topic, its lane description, the budget, and the rules below. **Give each lane no visibility into the other lanes.**

Inside a lane, for each round:

1. **Ask one question at a time**, in the lane's voice. Constraints that are not optional:
   - ask about the topic, not about adjacent topics (anti-drift)
   - do not re-ask something already asked (anti-repeat)
   - if there is nothing left worth asking, stop the lane — do not manufacture a question to fill the round
2. **Decompose the question into 2–3 search queries.** A question that will not decompose is a bad question; rewrite it.
3. **Search, then actually fetch.** Snippets are a lead, not evidence. Fetch the page for anything load-bearing.
4. **Answer only from what you fetched.** Every sentence traceable to a URL. If the sources do not answer it, write the refusal verbatim: *"no source found for this question"*.
5. **Write the turn back into lane context** — the question skeleton always, the answer detail for the last few turns only. This is what makes the next question a *follow-up* instead of a restart.

Maintain a per-lane log with, for every retrieved source: `url`, `title`, `query that found it`, `round`, and the exact claim it supports. **The `query` and `round` fields are the ones everyone forgets and the ones Step 4 needs.**

**The refusal loop**: when a round's searches come back empty or useless, that goes into the lane context and the next question must move away from it. Never patch a hole with what you already believe.

## Step 4 — Converge, and score the convergence

Now, and only now, bring the lanes together.

**4a. Merge by source, not by summary.** Key every piece of evidence by URL (normalized: strip tracking params, fragments, trailing slash). Same URL from two lanes → one source, union of the claims it supports. This is the first and cheapest convergence and it is where you find out that two lanes independently landed on the same page.

**4b. Build the claim × lane matrix.** Cluster the extracted claims into atomic assertions (one fact per row). For each claim, record **which lanes** and **how many distinct sources** support it:

```
claim | supporting URLs | distinct sources | lanes that found it | conflicts
```

**4c. Score corroboration.** This is the deliverable's spine:

| Level | Condition | How to state it |
|---|---|---|
| **A — Converged** | found by ≥2 *independent lanes*, ≥2 distinct domains | state plainly |
| **B — Corroborated** | ≥2 distinct sources, same lane | state with sources attached |
| **C — Single-source** | 1 source only | state + flag `single-source` |
| **D — Contested** | credible sources disagree | present **both**, do not average |
| **E — Unfound** | searched, nothing found | say so explicitly; do not fill from memory |

A claim is only A if the lanes were genuinely independent — if two lanes both just searched the topic name and both got the Wikipedia page, that is one lane twice, not convergence.

**4d. Weigh, do not count.** Cluster by domain, not by URL. Ten pages quoting the same press release is one source. Two pages from the same organisation are one source. Note upstream dependencies (`relates to`, `according to`) — corroboration from an echo is not corroboration.

**4e. Hunt the conflicts explicitly.** STORM's measured failure mode is not hallucination, it is *linking facts that merely co-occurred*. Before writing, scan the matrix for claims whose supporting sources do not actually connect the two things being connected. Mark any such link `inferred-by-me`, never as sourced. Look for level-D rows and make sure each one is visible in the report rather than quietly resolved.

## Step 5 — Report (working report, mechanism visible)

Write a Markdown **file**. Default name: `working-report.md` (if the user or the caller specified another output directory or filename for the report, obey that — set `WORKING = <that path>` and `READER = <report path>` at the start and use those two variables for the rest of the run, so the reply emits the right file).

Required structure:

```markdown
# <Topic>

## Corroboration summary
<counts: N claims converged / corroborated / single-source / contested / unfound>

## How the perspectives were chosen
<the anchor artifacts actually fetched + the orthogonality sentences + the lane list>

## Findings
### <Theme>
<prose; each claim marked A/B/C/D/E inline; citations as [n]>

## Contested points
<every level-D row, both sides, sources attached>

## Single-source claims
<every level-C row — read these as leads to verify, not as facts>

## What was searched and not found
<level-E rows, with the queries used>

## Sources
[n] <url> — found by <lane>, round <k>, via query "<q>"
```

Keep the `found by lane / round / query` provenance in the source list. It costs almost nothing to record and it is the only thing that lets a reader tell "four independent lanes converged here" from "one lucky hit got repeated".

**This is the artifact you audit against, not the artifact you hand over.** Proceed to Step 6.

## Step 6 — Polish into the reader report (mechanism invisible)

Write the result to **`reader-report.md`** (or `<READER>` as fixed in Step 5). Run this as **a separate pass with a fresh context** — a subagent that receives only the working report, not the lane prompts, not the lane logs, not your reasoning. A pass that has seen the machinery will leak the machinery.

### 6a. Translate every mechanism term into reader language

This is a **fixed mapping, not a judgment call**. Do not invent alternatives.

| Working report | Reader report |
|---|---|
| lane, perspective, lane 0 | *(delete — readers get findings, not org charts)* |
| orthogonality check, anchor artifact, budget, round | *(delete entirely)* |
| **A** | 由多个相互独立的来源印证 — say *which two*, in a column |
| **B** | 由两个独立来源印证（同一来源渠道内） |
| **C** | 目前只有单一来源（请当线索，不要当事实） |
| **D** | 来源之间存在冲突或口径不一致 |
| **E** | 检索未能回答的问题 |
| `query "<q>"` in prose | *(delete)*; the E-section keeps a **search-direction column** — the stored query verbatim is acceptable here because it lets the reader re-run and verify the gap themselves |
| `inferred-by-me` | 本文推论（来源并未连接这两件事） |
| fetch failure, bot_blocked, paywall | 未能获取全文的来源（不作为证据） |

**Never delete a citation number to make the prose flow.** Merge duplicates, renumber if you must, but the reader report's citation set must reconstruct the working report's source set.

### 6b. Rebuild the structure around reader questions, not around your procedure

The working report is ordered by *how you found out*. The reader report is ordered by *what the reader needs*:

```
一分钟版本            → the whole conclusion in one paragraph
结论                  → the layered verdict, as a table
前提 / 口径           → why the naive comparison is invalid (keep this early; it prevents most misuse)
主体章节              → the findings, grouped by theme, prose + numbers
交叉验证情况          → the load-bearing section: 独立印证 / 单一来源 / 冲突 / 检索未能回答
使用守则              → what must be delivered alongside any conclusion
数据截止与版本提醒     → date, version-sensitive figures
来源                  → full numbered list + 未能获取全文的来源
```

**The cross-validation section is not optional and must not be compressed into a footnote.** In the reader report it carries four subsections, in this order: independently corroborated (with the two paths named) → single-source (with the self-interested ones flagged) → conflicts (named, both sides, never averaged) → unfound (with search direction). If a reader cannot tell from the reader report alone which claims are hard and which are leads, Step 6 failed.

### 6c. Fix the defects that only become visible on rewrite

Re-reading an audit-shaped document to rewrite it surfaces contradictions the original buried. Expect to find real ones; fix them, and note what you fixed. Recurring classes:

- **grade conflicts** — the same figure marked A in one table and C in another (unify, and prefer the *lower* grade);
- **mis-attributed numbers** — a figure re-paired with the wrong source during compression;
- **naming drift** — one source group called two different things in two places;
- **internal contradictions** — two mutually exclusive framings of the same datapoint living in different sections;
- **bilingual splices and stray mechanism words** — grep for the deleted terms before shipping.

### 6d. Verification gate (run before delivering)

Do not ship on impression. Run these checks mechanically:

1. **Mechanism leakage = 0.** Grep the reader report for: `lane`, the A–E level tokens used as labels, `query`/`round`, `anchor`, `orthogonal`, `budget`, and the internal ROUND/GRADE vocabulary. The only permitted survivors are inside the E-section's search-direction column and the fetch-failure list.
2. **Citation integrity.** Parse the numbered citations in the body and in the source list; assert the two sets are **equal**. Zero orphans (cited but unlisted), zero strays (listed but never cited).
3. **Level fidelity.** Every working-report **A** must appear in the reader report's corroborated section *with both paths named*; every **D** must appear as a conflict with both sides intact; every **E** must survive as an unfound row with its search direction.
4. **No new facts.** Every number in the reader report must trace to the working report. Anything you were tempted to add is either `本文推论` or it does not ship.
5. **Count check.** If the working report says "N claims at level B", the reader report's corroborated section must contain N entries — or you state why not.

**Record the gate result, never speak it.** Append the one line (e.g. `leakage 0 · citations 80/80 (orphans 0, strays 0) · A 9/B 3/C 28/D 8/E 10 all present · no new facts`) to the **working report** — a log file, or the end of `working-report.md`. It is evidence about the reader report, and evidence about the machinery is machinery: it must not appear in `reader-report.md`, in the reply, or anywhere the reader can see. A gate line pasted into the reply breaks the delivery rule (§Delivery).

---

## Delivery — the reply is the reader report, byte for byte

This is the last step and it is mechanical. Do not reinterpret it.

1. `reader-report.md` has been written and has passed 6d.
2. Read the file back from disk — the actual file, not your memory of writing it.
3. Your entire message to the user **is that file's content, verbatim and complete**: same text, same headings, same order, same numbers, same links. Copy it; do not retype it from memory.

Forbidden in the reply — every one of these has been a real failure:

- a preamble or framing sentence ("已完成深度调研", "以下是报告", "按你的要求…");
- a sign-off, offer, or follow-up question ("需要我进一步…", "如需调整请告诉我");
- a summary, TL;DR, or highlight list that duplicates or foreshadows the report;
- the verification line, gate output, check counts, or any statement that checks passed;
- any mention of the mechanism: lanes, perspectives, rounds, levels, budgets, working report, files written, steps taken, subagents used;
- a file listing, `present` card description, or "报告已保存到 …" note;
- reordering, trimming, merging, "cleaning up", translating, or reformatting the content;
- fixing a typo, softening a claim, or adding a citation you think belongs.

If the report's own text already contains a date line, a summary section, or a verification-adjacent sentence, it ships as written. **Editing the report to improve the reply is a violation; changing the reply to improve the report is a violation.** The only legitimate way to change what the user sees is to change `reader-report.md` (through Step 6 and 6d) and then re-emit it in full.

Do not attach anything to the reply: no `present` cards, no file lists, no "报告已保存到 …", no second artifact. The reader report text is the whole delivery. (If the harness's own file-attachment metadata appears outside your message, that is the harness's business — your message body stays exactly the report.)

If the harness offers a way to emit the file's content directly (reading the file and passing it through, or a presentation mode that sends file content as the message), use it — it removes the retyping risk entirely. That mode is the only acceptable substitute, and it must emit the file's content unchanged.

---

## Failure modes to actively avoid

| Failure | Tell | Fix |
|---|---|---|
| **Perspective collapse** | Lanes' first questions are near-paraphrases | Re-derive lanes from a different anchor artifact |
| **Pseudo-convergence** | Levels look high but all sources are one domain/one press release | Cluster by domain; mark upstream dependencies |
| **Speculative linking** | A claim connects two facts your sources never connected | Mark `inferred-by-me` or drop it |
| **Parametric backfill** | A level-E row got written up anyway | Delete it and say unfound |
| **Budget drift** | Searching past the budget because "one more angle" | Stop; converge with what you have |
| **Single-lane report** | Output reads as one voice | Verify each lane produced a log; a silent lane is a failed lane |
| **Mechanism leak** | Reader report says "lane", "A 级", "轮次", or ships the orthogonality check | Step 6a mapping is fixed; grep before shipping |
| **Compression amnesia** | Reader report is short and confident, but its URL count collapsed toward zero and its E-section shrank | The citation set must equal the working report's; missing ≠ tidied |
| **Caveat stripping** | A number keeps its headline value but loses the clause that bounded it ("估算，非审计" / "自利来源" / "单一来源") | Grade fidelity check (6d.3): a figure may be compressed, a qualification may not |
| **Contract drift** | A "retention" rule gets satisfied while the pass invents its own extra claims to satisfy it | Verification gate is a separate pass with a fresh context |
| **Reply wrapper** | The reply opens with "已完成 / 以下是报告 / 报告已保存到…" or closes with an offer or a "检查通过" line | The reply is `reader-report.md` verbatim; read the file and copy it |
| **Reply paraphrase** | The reply reads like the report but is not byte-identical — retyped, trimmed, reordered, or "tidied up" | Re-read the file and re-emit the whole thing; never compose the reply from memory |
| **Gate line in the reply** | "leakage 0 · citations 80/80" appears to the user | The gate line belongs in the working report; it is machinery |

## Why this works

Reliability is not a property of a source. It is the property of **independent paths meeting on the same evidence**. A single perspective cannot distinguish "everyone agrees" from "I only looked one way" — both look like a clean, confident report. Running the lanes separately and scoring where they land is what makes agreement mean something, and what makes the disagreements visible instead of averaged away.

Step 6 exists because scored evidence that nobody can read has not been delivered. The two-artifact split is what keeps the scoring honest *and* the result usable: the working report is the proof, the reader report is the product, and the verification gate is what stops the product from quietly outrunning the proof.

## Reference

`references/execution-trace.md` — the STORM source-level execution trace this procedure abstracts, with the concrete defaults, budget sites, and the two known gaps (no orthogonality check, no per-source convergence scoring) that this skill closes.

`references/reader-report.md` — the Step 6 specification in full: the term mapping table, the reader-report skeleton, the defect classes found on rewrite, and the five-check verification gate with ready-to-run commands.
