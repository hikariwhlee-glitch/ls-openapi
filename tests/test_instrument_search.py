import unittest

from ls_openapi.sdk import MarketData


class FakeClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def call(self, tr_code, params):
        self.calls.append((tr_code, params))
        return self.responses[tr_code]


class InstrumentSearchTests(unittest.TestCase):
    def test_futures_search_normalizes_korean_name_and_returns_contract_candidates(self):
        client = FakeClient(
            {
                "t9943": {
                    "t9943OutBlock": [
                        {
                            "hname": "KOSPI200 202612",
                            "shcode": "A016C000",
                            "expcode": "KR4101VC6000",
                        },
                        {
                            "hname": "Mini KOSPI200 202612",
                            "shcode": "A196C000",
                            "expcode": "KR4106VC6000",
                        },
                        {
                            "hname": "KOSDAQ150 202612",
                            "shcode": "A301C000",
                            "expcode": "KR4301VC6000",
                        },
                    ]
                }
            }
        )

        result = MarketData(client).search_instruments("코스피200 선물")

        self.assertEqual(client.calls, [("t9943", {"gubun": "V"})])
        self.assertEqual(result["match_count"], 2)
        self.assertEqual(
            [item["code"] for item in result["results"]],
            ["A016C000", "A196C000"],
        )
        self.assertEqual(result["results"][0]["extended_code"], "KR4101VC6000")

    def test_search_matches_short_and_extended_codes(self):
        client = FakeClient(
            {
                "t9943": {
                    "t9943OutBlock": [
                        {"hname": "KOSPI200 202612", "shcode": "A016C000", "expcode": "KR4101VC6000"}
                    ]
                }
            }
        )

        result = MarketData(client).search_instruments("A016C000")

        self.assertEqual(result["match_count"], 1)
        self.assertEqual(result["results"][0]["name"], "KOSPI200 202612")

    def test_options_search_uses_option_master(self):
        client = FakeClient(
            {
                "t9944": {
                    "t9944OutBlock": [
                        {"hname": "KOSPI200 202612 C 400", "shcode": "201T6000", "expcode": "KR4201T64000"}
                    ]
                }
            }
        )

        result = MarketData(client).search_instruments("코스피200 옵션", instrument_type="options")

        self.assertEqual(client.calls, [("t9944", {"dummy": ""})])
        self.assertEqual(result["master_tr"], "t9944")
        self.assertEqual(result["results"][0]["code"], "201T6000")

    def test_limit_caps_returned_candidates_but_preserves_match_count(self):
        client = FakeClient(
            {
                "t9943": {
                    "t9943OutBlock": [
                        {"hname": f"KOSPI200 {month}", "shcode": f"A016{month}", "expcode": ""}
                        for month in ("202612", "202703", "202706")
                    ]
                }
            }
        )

        result = MarketData(client).search_instruments("KOSPI200 futures", limit=2)

        self.assertEqual(result["match_count"], 3)
        self.assertEqual(result["returned_count"], 2)
        self.assertEqual(len(result["results"]), 2)

    def test_invalid_search_parameters_fail_before_api_call(self):
        client = FakeClient({})

        with self.assertRaises(ValueError):
            MarketData(client).search_instruments("선물")
        with self.assertRaises(ValueError):
            MarketData(client).search_instruments("코스피200", instrument_type="stocks")
        with self.assertRaises(ValueError):
            MarketData(client).search_instruments("코스피200", limit=0)
        self.assertEqual(client.calls, [])

    def test_unexpected_master_response_shape_is_an_error(self):
        client = FakeClient({"t9943": {"t9943OutBlock": {"hname": "KOSPI200"}}})

        with self.assertRaises(RuntimeError):
            MarketData(client).search_instruments("KOSPI200")


if __name__ == "__main__":
    unittest.main()
