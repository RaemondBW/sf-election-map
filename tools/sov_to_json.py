"""Convert an SF Elections Statement of the Vote (sov.xlsx) into the map's data files.

usage: python3 tools/sov_to_json.py sov.xlsx PREFIX [SOURCE_URL]

Writes public/PREFIX-meta.json and public/PREFIX-precinct-vote.json in the same
shape as the 11-2024 files (contests, candidates, per-precinct vote counts), so
index.html can load either election the same way.

Every contest sheet is checked: the precinct "Total" rows must add up to the
sheet's "Countywide - Total" row for every candidate, or nothing is written.
Contests with no votes in San Francisco (districts that only clip one empty
precinct) are left out.

Needs openpyxl (pip install openpyxl).
"""
import json
import os
import re
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "..", "public")


def clean(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def pct_id(label):
    # "PCT 1101" or "PCT 1101 MB" (all-mail precinct) -> 1101
    return int(label[4:].replace(" MB", "").strip())


def main(path, prefix, source_url=""):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheets = [list(wb[n].iter_rows(values_only=True)) for n in wb.sheetnames]

    title = clean(sheets[0][2][2])  # "... Preliminary Statement of the Vote - 6"
    generated = sheets[0][0][-1]
    report = title.split("\n")[-1]
    m = re.search(r"(Preliminary|Final|Certified)?\s*Statement of the Vote(?:\s*-\s*(\d+))?", title)
    if m:
        kind = m.group(1) or "Final"
        report = f"{kind} Report {m.group(2)}" if m.group(2) else f"{kind} Report"

    contests = [{"Description": "Turnout", "Id": 99}]
    candidates = [{"Description": "Voted", "Id": 998, "Type": "Turnout", "ContestId": 99}]
    precincts = {}  # pct -> {contestId: {candId: votes, total: n}}

    # Turnout sheet: Precinct, Registered, -, Voters Cast, -, % Turnout
    cur = None
    for r in sheets[0]:
        if not r:
            continue
        if isinstance(r[0], str) and r[0].startswith("PCT "):
            cur = pct_id(r[0])
        elif r[0] == "Total" and cur is not None:
            precincts.setdefault(cur, {})["99"] = {"998": r[3], "total": r[1]}
            cur = None

    next_contest, next_cand = 1, 1
    for rows in sheets[1:]:
        name = clean(rows[1][0])
        header = rows[3]
        cols = [(i, clean(c)) for i, c in enumerate(header) if i >= 6 and c and clean(c) != "Total Votes"]
        total_col = next(i for i, c in enumerate(header) if c and clean(c) == "Total Votes")

        per_pct, county = {}, None
        cur = None
        for r in rows:
            if not r:
                continue
            if isinstance(r[0], str) and r[0].startswith("PCT "):
                cur = pct_id(r[0])
            elif r[0] == "Total" and cur is not None:
                per_pct[cur] = ([r[i] or 0 for i, _ in cols], r[total_col] or 0)
                cur = None
            elif r[0] == "Countywide - Total":
                county = [r[i] or 0 for i, _ in cols]

        if not county or sum(county) == 0:
            print(f"skip (no SF votes): {name}")
            continue
        sums = [sum(v[0][k] for v in per_pct.values()) for k in range(len(cols))]
        if sums != county:
            sys.exit(f"{name}: precinct sums {sums} != countywide {county}")

        cid = next_contest
        next_contest += 1
        contests.append({"Description": name, "Id": cid})
        ids = []
        for _, cname in cols:
            ctype = "WriteIn" if cname.lower() == "write-in" else "Regular"
            candidates.append({"Description": cname, "Id": next_cand, "ContestId": cid, "Type": ctype})
            ids.append(next_cand)
            next_cand += 1
        for pct, (votes, total) in per_pct.items():
            d = {str(i): v for i, v in zip(ids, votes) if v}
            d["total"] = total
            precincts.setdefault(pct, {})[str(cid)] = d

    vote = [
        {"Id": n, "prec_2012": pct, "Description": f"PCT {pct}", "Contests": precincts[pct]}
        for n, pct in enumerate(sorted(precincts), 1)
    ]
    meta = {
        "contests": contests,
        "candidates": candidates,
        "report_name": report,
        "last_updated": generated.strftime("%B %-d, %Y %-I:%M %p") if hasattr(generated, "strftime") else "",
        "source": source_url,
    }
    with open(os.path.join(PUBLIC, f"{prefix}-meta.json"), "w") as f:
        json.dump(meta, f, separators=(",", ":"))
    with open(os.path.join(PUBLIC, f"{prefix}-precinct-vote.json"), "w") as f:
        json.dump(vote, f, separators=(",", ":"))
    print(f"{report} ({meta['last_updated']}): {len(contests)} contests, {len(vote)} precincts -> public/{prefix}-*.json")


if __name__ == "__main__":
    main(*sys.argv[1:])
