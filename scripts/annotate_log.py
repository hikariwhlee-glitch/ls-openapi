"""로그 파일을 GitHub Actions 주석(::notice::)으로 출력합니다.

사용: python scripts/annotate_log.py <로그파일>

주석은 Actions 화면 상단에 표시되고 `gh api repos/<owner>/<repo>/check-runs/<job id>/annotations`
로 읽을 수 있습니다. 한 단계에 주석 개수 제한(10개)이 있어 긴 로그는 큰 덩어리로 묶고,
넘치면 마지막 덩어리에 생략 표시를 붙입니다. 로그에 이미 있는 내용만 옮깁니다.
"""

import sys
from pathlib import Path

CHUNK_CHARS = 3000
MAX_NOTICES = 10


def escape(text):
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def chunks(text):
    parts, current = [], ""
    for line in text.splitlines():
        if current and len(current) + len(line) + 1 > CHUNK_CHARS:
            parts.append(current)
            current = ""
        current += line[:500] + "\n"
    if current:
        parts.append(current)
    return parts


def main(argv):
    if len(argv) != 2:
        print("사용법: python scripts/annotate_log.py <로그파일>")
        return 2
    path = Path(argv[1])
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    if not text.strip():
        print("::notice title=live-check 로그::(출력 없음)")
        return 0
    parts = chunks(text)
    omitted = max(0, len(parts) - MAX_NOTICES)
    if omitted:
        parts = parts[: MAX_NOTICES - 1] + parts[-1:]
    total = len(parts)
    for index, part in enumerate(parts, 1):
        title = "live-check 로그 {}/{}".format(index, total)
        if omitted and index == total - 1:
            part += "... (중간 {}덩어리 생략) ...\n".format(omitted)
        print("::notice title={}::{}".format(title, escape(part)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
