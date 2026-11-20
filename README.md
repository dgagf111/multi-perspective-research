# multi-perspective-research

> 多视角交叉验证深度调研，按每条结论追溯原始证据。

技能目录包含主指令 `SKILL.md`、按需读取的参考资料和一个 Python 引用校验脚本。

## 核对证据

每条结论都追溯到原始依据。同一公告的多篇转载合计一份。独立实测可为其覆盖的事实提供另一份依据。权威原文可直接确认其职责范围内的事实，例如法规生效日期。

| 判定 | 含义 |
| --- | --- |
| 多源印证 | 相互独立的原始依据支持同一口径的结论。 |
| 单一来源 | 仅确认一份原始依据，说明适用范围与限制。 |
| 有分歧 | 对齐时间、版本、单位等口径后，证据仍互不相容。 |
| 证据不足 | 已执行相关检索，所得材料不足以回答。 |
| 获取受阻 | 相关查询或关键原文无法访问。 |
| 未覆盖 | 关键问题尚未进入检索或读取。 |

## 六步流程

1. 确定问题和报告路径，分别设置搜索、读页和合并核查额度。
2. 从官方文档、监管分类等真实资料提出不同的检索问题，保留基本事实视角。
3. 独立查询并读取原文，记录具体证据和访问缺口。
4. 按结论追溯原始依据，核查可比的分歧和可能推翻判断的反例。
5. 写底稿与读者稿，校验编号与网址，再逐条对照事实和限定语。
6. 留存 `working-report.md`，将 `reader-report.md` 全文作为最终回复。

完整流程见 [SKILL.md](SKILL.md)。

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

检索使用宿主提供的搜索和页面读取工具。引用校验脚本只依赖 Python 标准库。操作方法见 [读者稿与验收](references/reader-report.md)。

---

## 仓库结构

```
multi-perspective-research/
├── README.md              本文件（中文）
├── README.en.md           English version
├── LICENSE                MIT
├── SKILL.md               主指令（可直接放进 skills 根目录）
├── references/
│   ├── execution-trace.md STORM 源码级执行追踪
│   └── reader-report.md   读者稿格式与验收说明
└── scripts/
    └── check_report.py    引用校验
```

## License

[MIT](LICENSE) © dgagf111

提问机制参考 [Stanford STORM](https://github.com/stanford-oval/storm)。源码与参数见 [执行追踪](references/execution-trace.md)。
