# multi-perspective-research

> Cross-validated deep research — label every claim as independently corroborated, single-source, contested, or unfound.

A **self-contained Markdown instruction pack**: a `SKILL.md` with YAML frontmatter, plus on-demand `references/`. Any agent that honours the SKILL.md convention (DeepSeek Harness, Claude Code, ZCode, …) can use it by dropping the directory into its skills root — no binaries, no keys, no network service required.

---

## What problem it solves

A flat search answers *"what does the web say about X"*. This skill answers *"**which parts of X are independently corroborated, and which rest on a single source**"*.

Reliability is not a property of a source. It is the property of **independent paths meeting on the same evidence**. Send several lanes with genuinely different reasons to care after the topic, forbid them from talking to each other, and see which conclusions they reach independently. A lane that finds one page ten times is one lane, not ten.

### Evidence convergence grades

| Grade | Meaning |
|---|---|
| A converged | Several non-communicating independent lanes landed on the same conclusion |
| B corroborated | At least two independent domains agree |
| C single-source | Only one source says it; labelled as such |
| D contested | Sources contradict each other; the conflict is laid out openly |
| E unfound | Budget exhausted with no source able to answer; say so plainly |

---

## Six steps

1. **Read the world's structure, not the topic** — fetch 2–4 real artifacts (Wikipedia sections, rival docs' TOCs, regulator headings) and derive the orthogonality lanes from *their* structure. Angles you invent yourself are usually one angle in three hats.
2. **Write the budget down first** — 3 lanes + 1 baseline-facts lane × 3 rounds × 2–3 queries ≈ 36 retrievals. Running out of budget is a designed event, not an accident.
3. **Run lanes in parallel, independently** — snippets are leads, not evidence; fetch the page. If nothing can answer, write "no source answers this" — never fill the hole from model memory.
4. **Converge and score** — cluster by *domain*, not URL, then grade every claim A/B/C/D/E.
5. **Write two artifacts** — `working-report.md` (mechanism visible, auditable) and `reader-report.md` (mechanism invisible, the product).
6. **Polish in a fresh pass, then a mechanical gate** — grep for mechanism leakage, assert citation parity, verify grade fidelity, forbid new facts.

The reply to the user is `reader-report.md` verbatim, nothing added.

Full procedure: [SKILL.md](SKILL.md).

---

## Install

### Claude Code / any SKILL.md host

```bash
git clone https://github.com/dgagf111/multi-perspective-research.git
cp -r multi-perspective-research <your skills root>/
```

Typical skills roots:

| Host | Default location |
|---|---|
| Claude Code | `~/.claude/skills/` |
| ZCode | `~/.zcode/skills/` (or `ZCODE_SKILLS_ROOT`) |
| agents standard | `~/.agents/skills/` |
| DeepSeek Harness | `~/.dsh/skills/` |

### DeepSeek Harness

Add the repository path in Settings → Skills, or copy this directory into your workspace skills directory.

### Just want to read it

Open [`SKILL.md`](SKILL.md) — it explains itself.

---

## Dependencies

This skill contains no code; retrieval is delegated to the host's search tools. It cites `anysearch` / `agent-reach` as example backends — a host's `web_search` / `web_fetch` works just as well.

---

## Layout

```
multi-perspective-research/
├── README.md              this file (Chinese)
├── README.en.md           English version
├── LICENSE                MIT
├── SKILL.md               main instruction (drop straight into a skills root)
└── references/
    ├── execution-trace.md source-level trace of the STORM mechanism this abstracts
    └── reader-report.md   full Step 6 spec + the five-check verification gate
```

## License

[MIT](LICENSE) © dgagf111

The questioning mechanism is derived from [Stanford STORM](https://github.com/stanford-oval/storm); `references/execution-trace.md` records its source-level parameters and the two gaps this skill closes.
