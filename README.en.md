# multi-perspective-research

> Multi-perspective research that traces each claim to its original evidence.

The skill includes `SKILL.md`, reference documents, and a Python citation checker.

## Evidence status

Trace every claim to its original evidence. Several reports repeating one announcement share a single basis for the reported fact. An independent measurement can support the facts it covers. A single authoritative record can establish facts within its remit, such as a regulation's effective date.

| Status | Meaning |
| --- | --- |
| Independently corroborated | Independent original evidence supports the same scoped claim. |
| Single source | One original source has been verified. State its scope and limits. |
| Disputed | Evidence conflicts after aligning the scope, period, version, and units. |
| Insufficient evidence | The search ran and yielded too little evidence to answer. |
| Access blocked | A relevant search or source could not be accessed. |
| Outside coverage | A relevant question could not be investigated within the run. |

## Six steps

1. Define the question and report paths. Budget searches and page reads for the initial batch, added perspectives, and synthesis checks.
2. Start with four perspectives. One covers basic facts. Derive the other three from specific passages in the original material. [How to select and read sources](references/perspective-discovery.md)
3. Search independently and read the original material. After each batch, review unused findings. Add a perspective when the material reveals a question that can affect the decision, remains uncovered, and can be investigated.
4. Trace the evidence behind each claim. Recheck important disagreements and search for counterexamples.
5. Draft both reports. Validate citation numbers and URLs, then check claims and qualifications against their sources.
6. Archive `working-report.md` and use the full text of `reader-report.md` as the final reply.

See the full procedure in [SKILL.md](SKILL.md).

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

Research uses the host's search and page-reading tools. The citation checker uses the Python standard library. See the [reader report and validation guide](references/reader-report.md).

---

## Layout

```
multi-perspective-research/
├── README.md              this file (Chinese)
├── README.en.md           English version
├── LICENSE                MIT
├── SKILL.md               main instruction (drop straight into a skills root)
├── references/
│   ├── execution-trace.md       trace of the STORM implementation
│   ├── perspective-discovery.md source selection and discovery of new perspectives
│   └── reader-report.md         reader report format and validation
└── scripts/
    └── check_report.py    citation checker
```

## License

[MIT](LICENSE) © dgagf111

The questioning workflow draws on [Stanford STORM](https://github.com/stanford-oval/storm). The [execution trace](references/execution-trace.md) covers the implementation and its parameters.
