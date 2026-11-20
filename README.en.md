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

1. Define the question and report paths. Set separate limits for searches, page reads, and follow-up checks.
2. Develop distinct questions from real material, including a baseline check of the facts.
3. Search independently, read the original material, and log findings and gaps.
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
│   ├── execution-trace.md trace of the STORM implementation
│   └── reader-report.md   reader report format and validation
└── scripts/
    └── check_report.py    citation checker
```

## License

[MIT](LICENSE) © dgagf111

The questioning workflow draws on [Stanford STORM](https://github.com/stanford-oval/storm). The [execution trace](references/execution-trace.md) covers the implementation and its parameters.
