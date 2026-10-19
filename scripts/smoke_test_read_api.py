"""One-shot read-only verification for GitHub Actions secrets."""
from __future__ import annotations
import sys
from ls_openapi import LSOpenAPI


def main() -> int:
    try:
        client = LSOpenAPI()
        # Public futures product master lookup; no account or order operation.
        result = client.call("t8426", {"dummy": ""})
        response_fields = set(result) - {"_continuation"}
        if not response_fields:
            print("Read-only API returned an empty response.")
            return 1
    except Exception as exc:
        # Do not print exception text or response payloads to public Actions logs.
        print(f"Read-only API verification failed ({type(exc).__name__}).")
        return 1
    print(f"Read-only API verification succeeded: t8426, response fields={len(response_fields)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
