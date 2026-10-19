"""Fetch the Vebtan ``failedFiles`` table and print/write a report grouped by failure reason.

Implements steps 1-3 of ``debug_vebtan/concept``:

1. request every page of ``http://130.149.179.21/database/failedFiles?rows=1000&page=N``
   and read the failed-file table directly from there,
2. group the entries by their individual failure reason,
3. print and write a plain-text report listing each reason, how often it occurs and the
   first file (with its id) that failed with it.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from collections.abc import Hashable
from pathlib import Path
from typing import Any
from urllib.request import urlopen

BASE_URL = "http://130.149.179.21/database/failedFiles?rows=1000&page={page}"
REPORT_PATH = Path(__file__).resolve().parent / "failed_files.txt"

# Failure reasons that are considered an acceptable, expected outcome, tagged as such in the report.
FAILED_SUCCESSFULLY = [
    "File type must be TXT or CSV.",
]


def fetch_html(url: str) -> str:
    """Fetch ``url`` and return the decoded response body."""
    with urlopen(url) as response:  # noqa: S310 - fixed, trusted internal host
        return response.read().decode(response.headers.get_content_charset() or "utf-8")


def rsc_payload(html: str) -> str:
    """Reassemble the React Server Component payload from the Next.js HTML."""
    return "".join(
        json.loads(match) for match in re.compile(r'self\.__next_f\.push\(\[1,("(?:\\.|[^"\\])*")\]\)').findall(html)
    )


def _records(payload: str) -> list[dict[str, Any]]:
    """Return the failed-file records from a single page's RSC payload."""
    table_index = payload.find('"table":"failedFiles"')
    if table_index == -1:
        return []
    data_index = payload.find('"data":', table_index)
    if data_index == -1:
        return []
    try:
        array_start = payload.index("[", data_index)
        records, _ = json.JSONDecoder().raw_decode(payload, array_start)
    except ValueError:
        return []
    return records


def download_records() -> list[dict[str, Any]]:
    """Download every page and return the de-duplicated failed-file records."""
    entries: list[dict[str, Any]] = []
    seen: set[Any] = set()
    total: int | None = None
    page = 1
    while True:
        html = fetch_html(BASE_URL.format(page=page))
        payload = rsc_payload(html)
        page_records = _records(payload)
        if not page_records:
            break

        new_records = 0
        for entry in page_records:
            entry_id = entry.get("id")
            if isinstance(entry_id, Hashable) and entry_id in seen:
                continue
            if isinstance(entry_id, Hashable):
                seen.add(entry_id)
            entries.append(entry)
            new_records += 1

        if total is None:
            match = re.search(r'"pageFilter":\{"total":(\d+)', payload)
            total = int(match.group(1)) if match else None
        print(f"Downloaded page {page}: {new_records} new records ({len(entries)}/{total or '?'}).")

        if new_records == 0 or (total is not None and len(entries) >= total):
            break
        page += 1
    return entries


def write_report(entries: list[dict[str, Any]], path: Path = REPORT_PATH) -> Path:
    """Print and store the failures grouped by reason in a plain-text report."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        error = entry.get("error")
        reason = str(error.get("error", error)) if isinstance(error, dict) else str(error)
        groups[reason].append(entry)

    blocks = []
    for reason, records in sorted(groups.items(), key=lambda item: len(item[1]), reverse=True):
        first = records[0]
        raw_files = first.get("rawFiles") or []
        first_file = str(raw_files[0]) if raw_files else ""
        tag = "Tag: failed successfully\n" if reason in FAILED_SUCCESSFULLY else ""
        blocks.append(
            f"Error: {reason}\n"
            f"{tag}"
            f"Number of occurrences: {len(records)}\n"
            f"First file with said Error: {first_file} , {first.get('id')}"
        )
    text = "\n\n".join(blocks) + "\n"
    print(text, end="")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


if __name__ == "__main__":
    entries = download_records()
    report = write_report(entries)
    print(f"\n{len(entries)} failed files -> {report}")
