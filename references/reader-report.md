# Step 6 — The reader report

Full specification for turning the Step 5 working report into the artifact you actually hand to someone.

**Core rule:** the working report is the *proof*; the reader report is the *product*. Both ship. Step 6 never replaces Step 5.

**Delivery rule:** the reader report is written to `reader-report.md`, and the user's final reply **is that file's content, verbatim and complete** — see §5.5 and §7.

---

## 1. Run it as a separate pass

Give the polishing pass **only the working report file**. Do not give it:

- the lane prompts or lane descriptions,
- the lane logs,
- your own reasoning or the conversation that produced them,
- any sibling draft.

A pass that has seen the machinery will leak the machinery — it will reach for "the capital lane found…" because that is the most compressed way to say it. A fresh context has no such shortcut, and is forced into reader language.

If the polishing pass is run by you in the same context, expect leakage; treat 6d.1 as a hard gate rather than a formality.

---

## 2. Term mapping (fixed — not a judgment call)

| Working report | Reader report |
|---|---|
| lane / perspective / lane 0 | delete. Readers get findings, not org charts. |
| orthogonality check | delete entirely |
| anchor artifact | delete entirely (the *structure* it lent survives as ordinary section order) |
| budget, round | delete entirely |
| **A — Converged** | **由多个相互独立的来源印证的结论**，并要求列出**两条独立路径** |
| **B — Corroborated** | **由两个独立来源印证**（同一来源渠道内，强度低于 A） |
| **C — Single-source** | **目前只有单一来源的结论（请当线索，不要当事实）** |
| **D — Contested** | **来源之间存在冲突或口径不一致的数据** → 拆成具名「冲突一…N」，两侧并列 |
| **E — Unfound** | **检索未能回答的问题**（标题用读者视角，不用 "level E") |
| source provenance `lane/round/query` | delete from the source list; keep plain `[n] <url> — <what it supports>` |
| `query "<q>"` used as evidence trail | delete from prose; **preserve verbatim in the E-section's search-direction column** — this is the one place it earns its keep, because it lets the reader re-run and confirm the gap |
| `inferred-by-me` | **本文推论（来源并未连接这两件事）** |
| fetch failure / bot_blocked / paywall | **未能获取全文的来源（不作为证据）** — a list at the end |

**Renumbering:** merge duplicate URLs before numbering. The reader report's citation set must **equal** the working report's source set — same sources, possibly renumbered. If a source disappears, that is a defect, not a tidy-up.

---

## 3. Reader-report skeleton

```markdown
# <Title that states the question, not the method>

**调研截止日：<date>**

> **一分钟版本。** <the whole conclusion in one paragraph, including the caveat that makes it valid>

## 一、结论
<layered verdict as a table: 问题 | 答案 | 依据强度>

## 二、前提：<why the naive framing is invalid>
<the caliber/definition problem, early. This section prevents most downstream misuse.>

## 三…N、<主体章节>
<findings grouped by theme; prose carrying the load, numbers inline, [n] citations>

## 交叉验证情况
### 由多个相互独立的来源印证的结论   <table: 结论 | 两条独立路径>
### 目前只有单一来源的结论          <table: 结论 | 唯一来源>  ← flag self-interested sources
### 来源之间存在冲突或口径不一致     <#### 冲突一…N, both sides, never averaged>
### 检索未能回答的问题               <table: 没能找到什么 | 检索方向>

## 使用这些结论时必须同时交付的判断
<the few meta-judgements that must travel with any conclusion>

## 数据截止与版本提醒
## 来源
### 未能获取全文的来源（不作为证据）
```

### Why the cross-validation section is structured this way

It is the reader-facing form of Step 4c. Four subsections, in this order, each answering a different reader question:

1. **独立印证** — *What can I treat as settled?* Naming **both paths** is the whole value; "multiple sources agree" without saying which is a level collapse, not a level A.
2. **单一来源** — *What needs a second look before I rely on it?* Also the only place to flag that a source is **self-interested** (a vendor, a recruiter, an integrator, a founder) — a qualification a reader cannot recover once it is dropped.
3. **冲突** — *Where will I get burned if I quote only the convenient half?* Every D row, both sides, named, never averaged. Say explicitly which pairs are "both true, different quantities" (e.g. unit cost falling while total cost rises) versus genuinely irreconcilable.
4. **未能回答** — *What do we not know?* Unfound is a finding. Give the search direction so the reader can check for themselves.

---

## 4. Defect classes to expect on rewrite

Reading an audit-shaped document in order to rewrite it surfaces contradictions the original buried. These recur; fix them and report what you fixed.

| Class | What it looks like | Fix |
|---|---|---|
| **Grade conflict** | Same figure is A in one table and C in another | Unify. Prefer the **lower** grade; then check whether the surrounding table header still claims level A. |
| **Mis-attributed number** | A figure gets re-paired with the wrong source during compression | Re-derive each figure → source pair from the working report, row by row |
| **Naming drift** | One source group called two different things in two sections | Pick one name, apply everywhere |
| **Internal contradiction** | Two mutually exclusive framings of the same datapoint in different sections | Resolve explicitly; if unresolved, it belongs in 冲突 |
| **Bilingual splice** | A stray English word inside Chinese prose | Proofread; grep for stray Latin runs |
| **Mechanism residue** | "lane", "A 级", "轮次" surviving the rewrite | Gate 6d.1 |
| **Caveat stripping** | The number survives; the clause bounding it does not | Gate 6d.3 — this is the most dangerous defect, because the reader cannot detect it |

**Caveat stripping deserves emphasis.** A summary that keeps `+15–25%` but drops `估算，非审计` produces a document that is *shorter and more confident and wrong to act on*. Detect it by checking, for every number carried over, that its bounding clause survived too.

---

## 5. Verification gate — run before delivering

Do not ship on impression. Run these mechanically and **record the results in the working report** (never in the reader report or the reply — §5.5, §7).

### 5.1 Mechanism leakage = 0

```powershell
$f = "<reader-report.md>"
$t = Get-Content $f -Raw
foreach ($p in @('lane','Lane','（A）','（B）','（C）','（D）','（E）',
                 'A 级','B 级','C 级','D 级','E 级',
                 '锚定','正交','收敛','round','视角独立')) {
  $c = ([regex]::Matches($t, [regex]::Escape($p))).Count
  if ($c -gt 0) { "LEAK: '$p' x$c" }
}
```

Permitted survivors: the verbatim queries inside the E-section's search-direction column, and the fetch-failure list.

### 5.2 Citation integrity — body set == source list

```powershell
$all = Get-Content $f -Raw
$body = ($all -split '## 来源')[0]
$src  = ($all -split '## 来源')[1]
$in = @([regex]::Matches($body,'\[(\d{1,2})\]') | ForEach-Object { [int]$_.Groups[1].Value } | Sort-Object -Unique)
$li = @([regex]::Matches($src,'(?m)^(\d{1,2})\. https') | ForEach-Object { [int]$_.Groups[1].Value } | Sort-Object -Unique)
"orphans (cited, unlisted): " + (@($in | Where-Object { $li -notcontains $_ }) -join ',')
"strays  (listed, uncited): " + (@($li | Where-Object { $in -notcontains $_ }) -join ',')
```

Both must be empty. If auto-assigning numbers left gaps, renumber the list so the set is contiguous.

### 5.3 Level fidelity

- Every **A** row from the working report appears under 独立印证 **with both paths named**.
- Every **B** row appears, marked as same-channel.
- Every **C** row appears under 单一来源, with self-interest flagged where applicable.
- Every **D** row appears as a named 冲突, **both sides intact, nothing averaged away**.
- Every **E** row appears under 未能回答 with a search direction.
- The counts in the reader report match the working report's summary counts, or you state why not.

### 5.4 No new facts

Every number and named entity in the reader report traces to the working report. Anything newly introduced is either marked 本文推论 or it does not ship.

### 5.5 Record the gate results (in the working report, not to the user)

Append the gate line to the **working report** — the end of `working-report.md` or a sibling log file:

```
leakage 0 · citations 80/80 (orphans 0, strays 0) · A 9/B 3/C 28/D 8/E 10 all present · no new facts
```

A recorded gate line is worth materially more than a silent ship — but it is evidence *about* the machinery, so it stays with the machinery. Putting it in `reader-report.md`, or in the reply, is a delivery-rule violation (§7).

---

## 6. What Step 6 is not allowed to do

- **Not allowed to drop a contradiction to make the prose cleaner.** Clean structure may reveal a conflict more sharply; it may never dissolve one.
- **Not allowed to promote a level.** Rewriting is not new evidence. If a claim reads weak, the fix is wording, not a better grade.
- **Not allowed to fill an unfound row.** A short list is honest; an invented entry is the failure this whole skill exists to prevent.
- **Not allowed to become the only artifact.** Keep the working report. If someone later asks "how do you know", the answer must be a file, not a memory.

---

## 7. Delivery — the reply is `reader-report.md`, verbatim

The last step is mechanical; do not reinterpret it.

1. Read `reader-report.md` back from disk — the file, not your memory of writing it.
2. Your entire message body **is that content, complete and unchanged**: same headings, same order, same numbers, same links, same wording.
3. Emit nothing around it.

**Forbidden in the reply** (each has been an observed failure):

| Forbidden | Example |
|---|---|
| preamble / framing | "已完成深度调研，以下是报告：" |
| sign-off / offer | "如果需要进一步分析请告诉我" |
| summary or highlights | a TL;DR that duplicates the report |
| gate line / check counts | "leakage 0 · citations 80/80 · 检查通过" |
| mechanism mentions | lanes, perspectives, rounds, levels, budgets, working report, subagents |
| file logistics | "报告已保存到 …" |
| content edits | retyping, trimming, reordering, merging, translating, reformatting |
| silent corrections | fixing a typo, softening a claim, adding a citation |

If the report already contains a date line, a summary section, or a sentence that reads like a caveat to the reader, it ships as written. **Editing the report to improve the reply and editing the reply to improve the report are both violations.** The only way to change what the user sees is to change `reader-report.md` (through §2–§5) and re-emit it in full.

Do not attach extra artifacts to the reply: no `present` cards, no file list, no "报告已保存" note. Emitting the file's content directly, via a harness mode that sends file content as the message, is the only acceptable substitute — and it must send the content unchanged.
