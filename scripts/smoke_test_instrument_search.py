"""Verify the index futures master search against LS Open API (read-only)."""

from __future__ import annotations

import os

from ls_openapi import LSFutureClient


def main() -> None:
    query = os.getenv("LS_INSTRUMENT_QUERY", "코스피200 선물")
    client = LSFutureClient()
    result = client.market.search_instruments(query, instrument_type="futures", limit=20)
    matches = result["results"]

    print(
        f"Instrument master: {result['master_tr']}; "
        f"query={query!r}; matches={result['match_count']}; "
        f"shown={result['returned_count']}"
    )
    for item in matches:
        print(
            f"- {item['name']} | code={item['code']} "
            f"| extended_code={item['extended_code']}"
        )

    if not matches:
        raise RuntimeError(f"No futures instruments matched {query!r}")


if __name__ == "__main__":
    main()
