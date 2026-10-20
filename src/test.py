"""Report which date formats are used in a list of filenames.

    >>> date_pattern_report(["2024-01-15_a.csv", "15Jan2024.pdf", "notes.txt"])
    {'unknown date': 1, '%Y-%m-%d': 1, '%d%b%Y': 1}
"""
import os
import re
from collections import Counter, defaultdict
from datetime import datetime

UNKNOWN = "unknown date"

# ---------------------------------------------------------------------------
# Formats to look for (strptime syntax).
# ORDER MATTERS: most specific first. A filename gets the first format that
# matches, so "2024-01-15" counts as "%Y-%m-%d" and not as the partial "%m-%d".
# Add your own formats here (or pass `formats=` to the functions below).
# ---------------------------------------------------------------------------
_SEPS = ("-", "_", ".", "")
_NAME_SEPS = ("", "-", "_", " ", ".")      # around month names: 15Jan2024, 15 Jan 2024
_TIMES = ("%H%M%S", "%H-%M-%S", "%H.%M.%S")
_JOINERS = ("_", "-", " ", "T", "")

DEFAULT_FORMATS = (
    # full numeric dates (4-digit year)
    + [f"%Y{s}%m{s}%d" for s in _SEPS]
    + [f"%d{s}%m{s}%Y" for s in _SEPS]
    + [f"%m{s}%d{s}%Y" for s in _SEPS]
    # month names
    + [f"%d{s}%b{s}%Y" for s in _NAME_SEPS]
    + [f"%d{s}%B{s}%Y" for s in _NAME_SEPS]
    + [f"%b{s}%d{s}%Y" for s in _NAME_SEPS]
    + [f"%B{s}%d{s}%Y" for s in _NAME_SEPS]
    + [f"%Y{s}%b{s}%d" for s in _NAME_SEPS]
    # 2-digit year (only with - or _ to avoid matching version numbers like 1.2.34)
    + [f"%y{s}%m{s}%d" for s in ("-", "_")]
    + [f"%d{s}%m{s}%y" for s in ("-", "_")]
    + [f"%m{s}%d{s}%y" for s in ("-", "_")]
    # year + month
    + ["%Y-%m", "%Y_%m"]
    # no year
    + [f"%m{s}%d" for s in ("-", "_")]
    + [f"%d{s}%m" for s in ("-", "_")]
    + [f"%d{s}%b" for s in _NAME_SEPS]
    + [f"%b{s}%d" for s in _NAME_SEPS]
)

# ---------------------------------------------------------------------------
# strptime format  ->  compiled regex
# ---------------------------------------------------------------------------
_TOKEN = re.compile(r"%[A-Za-z]|[^%]+")
_NUMERIC = {"%Y", "%y", "%m", "%d", "%H", "%M", "%S"}
_MONTH_NAME = {"%b", "%B"}


def _to_regex(fmt):
    tokens = _TOKEN.findall(fmt)
    parts = []
    for i, tok in enumerate(tokens):
        if tok == "%Y":
            parts.append(r"(?:19|20)\d{2}")
        elif tok in ("%y", "%H", "%M", "%S"):
            parts.append(r"\d{2}")
        elif tok in ("%m", "%d"):
            # 1-2 digits, unless glued to another number (e.g. %Y%m%d)
            glued = any(n in _NUMERIC for n in tokens[max(i - 1, 0):i] + tokens[i + 1:i + 2])
            parts.append(r"\d{2}" if glued else r"\d{1,2}")
        elif tok == "%b":
            parts.append(r"[A-Za-z]{3}")
        elif tok == "%B":
            parts.append(r"[A-Za-z]{4,9}")      # 4+ so "May" is only ever %b
        else:
            parts.append(re.escape(tok))
    # don't start/end in the middle of a longer number (or word, for month names)
    pre = r"(?<![A-Za-z])" if tokens[0] in _MONTH_NAME else r"(?<!\d)"
    post = r"(?![A-Za-z])" if tokens[-1] in _MONTH_NAME else r"(?!\d)"
    return re.compile(pre + "".join(parts) + post)


def _is_real_date(fmt, text):
    """Reject things like 2024-13-45 that merely *look* like a date."""
    try:
        if "%Y" in fmt or "%y" in fmt:
            datetime.strptime(text, fmt)
        else:
            # no year in the format: borrow a leap year so Feb 29 is accepted
            datetime.strptime("2000 " + text, "%Y " + fmt)
        return True
    except ValueError:
        return False


def _candidate_formats(name, compiled):
    """Formats that fit the most specific date found in `name` (0, 1 or several)."""
    hits = []
    for fmt, rx in compiled:
        for m in rx.finditer(name):
            if _is_real_date(fmt, m.group()):
                hits.append((fmt, m.span()))
                break
    if not hits:
        return []
    best_span = hits[0][1]                  # hits are in priority order
    return [fmt for fmt, span in hits if span == best_span]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def group_by_date_format(filenames, formats=DEFAULT_FORMATS):
    """Return {format: [filenames]}; files with no date go under "unknown date".

    Some strings fit several formats ("05-06-2024" is %d-%m-%Y or %m-%d-%Y).
    Those are settled by looking at the unambiguous files in the same list
    (e.g. one "13-05-2024" proves the folder is day-first). If there is no
    evidence either way, the key lists the possibilities: "%d-%m-%Y | %m-%d-%Y".
    """
    compiled = [(f, _to_regex(f)) for f in formats]
    found = {n: _candidate_formats(os.path.basename(n), compiled) for n in filenames}

    votes = Counter(c[0] for c in found.values() if len(c) == 1)

    groups = defaultdict(list)
    for name, cands in found.items():
        if not cands:
            key = UNKNOWN
        elif len(cands) == 1:
            key = cands[0]
        else:
            top = max(votes[c] for c in cands)
            winners = [c for c in cands if votes[c] == top]
            key = winners[0] if len(winners) == 1 else " | ".join(winners)
        groups[key].append(name)
    return dict(groups)


def date_pattern_report(filenames, formats=DEFAULT_FORMATS):
    """Return {format: count}: "unknown date" first, then most common first."""
    groups = group_by_date_format(filenames, formats)
    counts = {fmt: len(files) for fmt, files in groups.items()}
    return dict(sorted(counts.items(), key=lambda kv: (kv[0] != UNKNOWN, -kv[1])))


if __name__ == "__main__":
    import sys

    # usage: python date_patterns.py /path/to/folder
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    names = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for fmt, n in date_pattern_report(names).items():
        print(f"{fmt}: {n}")