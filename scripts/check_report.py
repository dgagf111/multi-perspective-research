"""Check the citation structure shared by a working report and its reader report."""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


HEADING = re.compile(r" {0,3}(#{1,6})[ \t]+(.+?)[ \t]*")
FENCE = re.compile(r" {0,3}(`{3,}|~{3,})(.*)")
SOURCE = re.compile(r"- \[([1-9][0-9]*)\] <(https?://[^<>\s]+)> — \S.*")
NO_SOURCES = "本次没有可引用的来源。"
INLINE_LITERAL = re.compile(r"(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)|https?://[^\s<>()]+")
CITATION = re.compile(r"(?<![!\\])\[([0-9]+)\](?!\()")


def prose_lines(text):
    fence = ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        marker = FENCE.fullmatch(line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = ""
        elif marker:
            fence = marker[1]
        else:
            yield line_number, line


def parse_sources(path, lines):
    entries = [(number, line.strip()) for number, line in lines if line.strip()]
    if len(entries) == 1 and entries[0][1] == NO_SOURCES:
        return {}
    if not entries:
        raise ValueError(f"{path} 的来源节为空。无可引用来源时填写『{NO_SOURCES}』")

    sources = {}
    urls = set()
    for line_number, line in entries:
        location = f"{path} 第 {line_number} 行"
        entry = SOURCE.fullmatch(line)
        if not entry:
            raise ValueError(f"{location}的来源格式有误。应为 - [n] <https://网址> — 标题")
        number, url = entry.groups()
        try:
            hostname = urlsplit(url).hostname
        except ValueError:
            hostname = None
        if not hostname:
            raise ValueError(f"{location}的来源网址无效。")
        if number in sources:
            raise ValueError(f"{location}重复使用了来源编号 [{number}]。")
        if url in urls:
            raise ValueError(f"{location}重复列出了同一来源网址。")
        sources[number] = url
        urls.add(url)
    return sources


def read_report(path):
    lines = list(prose_lines(path.read_text(encoding="utf-8-sig")))
    headings = []
    for index, (_, line) in enumerate(lines):
        heading = HEADING.fullmatch(line)
        if heading and len(heading[1]) <= 2:
            headings.append((index, heading[1], heading[2]))

    source_headings = [index for index, level, title in headings if level == "##" and title == "来源"]
    if len(source_headings) != 1:
        raise ValueError(f"{path} 应恰好有一处二级标题『来源』。")
    start = source_headings[0]
    end = next((index for index, _, _ in headings if index > start), len(lines))
    sources = parse_sources(path, lines[start + 1:end])
    return sources, lines[:start] + lines[end:]


def main():
    parser = argparse.ArgumentParser(description="核对两份调研报告的来源编号与读者稿引用。")
    parser.add_argument("working", type=Path, help="工作底稿的路径")
    parser.add_argument("reader", type=Path, help="读者稿的路径")
    args = parser.parse_args()
    if args.working.resolve() == args.reader.resolve():
        parser.error("请分别提交底稿和读者稿的路径。")
    try:
        working_sources, _ = read_report(args.working)
        reader_sources, body = read_report(args.reader)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    citations = set()
    for _, line in body:
        citations.update(CITATION.findall(INLINE_LITERAL.sub(" ", line)))

    errors = []
    for number in sorted(citations - reader_sources.keys()):
        errors.append(f"读者稿引用了来源表中缺少的编号 [{number}]。")
    for number in sorted(reader_sources.keys() - citations):
        errors.append(f"读者稿来源 [{number}] 未在正文引用。")
    for number in sorted(working_sources.keys() | reader_sources.keys()):
        if working_sources.get(number) != reader_sources.get(number):
            errors.append(f"底稿与读者稿的来源 [{number}] 缺失或网址不一致。")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"引用校验通过，核对了 {len(reader_sources)} 条来源。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
