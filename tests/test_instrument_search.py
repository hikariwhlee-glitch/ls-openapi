import unittest

from ls_openapi.sdk import MarketData


OUTPUTS = {
    "t9943": "t9943OutBlock",
    "t9944": "t9944OutBlock",
    "t8433": "t8433OutBlock",
    "t8435": "t8435OutBlock",
    "t8401": "t8401OutBlock",
    "t8426": "t8426OutBlock",
    "t8467": "t8467OutBlock",
}


class FakeClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def call(self, tr_code, params):
        self.calls.append((tr_code, params))
        key = (tr_code, tuple(sorted(params.items())))
        return self.responses.get(key, self.responses.get(tr_code, {OUTPUTS[tr_code]: []}))


class InstrumentSearchTests(unittest.TestCase):
    def test_natural_korean_query_matches_standard_and_mini_kospi200_futures(self):
        client = FakeClient(
            {
                ("t9943", (("gubun", ""),)): {
                    "t9943OutBlock": [
                        {"hname": "KOSPI200 202612", "shcode": "A016C000", "expcode": "KR4101VC6000"}
                    ]
                },
                ("t8435", (("gubun", "MF"),)): {
                    "t8435OutBlock": [
                        {"hname": "Mini KOSPI200 202612", "shcode": "A196C000", "expcode": "KR4106VC6000"}
                    ]
                },
            }
        )

        result = MarketData(client).search_instruments(
            "코스피 200 지수선물 찾아줘",
            asset_class="index",
        )

        self.assertEqual(result["match_count"], 2)
        self.assertEqual(
            [item["code"] for item in result["results"]],
            ["A016C000", "A196C000"],
        )
        self.assertEqual(result["results"][0]["extended_code"], "KR4101VC6000")
        self.assertIn(("t9943", {"gubun": ""}), client.calls)
        self.assertIn(("t8435", {"gubun": "MF"}), client.calls)

    def test_mini_qualifier_filters_out_standard_futures(self):
        client = FakeClient(
            {
                ("t9943", (("gubun", ""),)): {
                    "t9943OutBlock": [
                        {"hname": "KOSPI200 202612", "shcode": "A016C000", "expcode": ""}
                    ]
                },
                ("t8435", (("gubun", "MF"),)): {
                    "t8435OutBlock": [
                        {"hname": "Mini KOSPI200 202612", "shcode": "A196C000", "expcode": ""}
                    ]
                },
            }
        )

        result = MarketData(client).search_instruments(
            "코스피200 미니 선물",
            asset_class="index",
        )

        self.assertEqual([item["code"] for item in result["results"]], ["A196C000"])

    def test_stock_futures_master_matches_underlying_stock_name(self):
        client = FakeClient(
            {
                "t8401": {
                    "t8401OutBlock": [
                        {"hname": "삼성전자 202612", "shcode": "S005930", "expcode": "KR700593VC60"}
                    ]
                }
            }
        )

        result = MarketData(client).search_instruments(
            "삼성전자 주식선물 찾아줘",
            asset_class="stock",
        )

        self.assertEqual(client.calls, [("t8401", {})])
        self.assertEqual(result["results"][0]["asset_class"], "stock")
        self.assertEqual(result["results"][0]["code"], "S005930")

    def test_commodity_futures_master_matches_product_query(self):
        client = FakeClient(
            {
                "t8426": {
                    "t8426OutBlock": [
                        {"hname": "금 202612", "shcode": "GCZ26", "expcode": "KRA000000001"}
                    ]
                }
            }
        )

        result = MarketData(client).search_instruments(
            "금 상품선물",
            asset_class="commodity",
        )

        self.assertEqual(client.calls, [("t8426", {"dummy": ""})])
        self.assertEqual(result["results"][0]["asset_class"], "commodity")

    def test_weekly_option_and_call_strike_qualifiers_are_preserved(self):
        client = FakeClient(
            {
                ("t8435", (("gubun", "WK"),)): {
                    "t8435OutBlock": [
                        {"hname": "KOSPI200 202612 C 400", "shcode": "201W6400", "expcode": "KR4201W64000"}
                    ]
                }
            }
        )

        result = MarketData(client).search_instruments(
            "코스피200 위클리 400 콜옵션 검색해줘",
            instrument_type="options",
            asset_class="index",
        )

        self.assertEqual(result["match_count"], 1)
        self.assertEqual(result["results"][0]["code"], "201W6400")
        self.assertEqual(result["results"][0]["product_family"], "코스피200 위클리 옵션")

    def test_duplicate_codes_from_overlapping_option_masters_are_removed(self):
        row = {"hname": "KOSPI200 202612 C 400", "shcode": "201T6000", "expcode": "KR4201T64000"}
        client = FakeClient(
            {
                "t9944": {"t9944OutBlock": [row]},
                "t8433": {"t8433OutBlock": [row]},
            }
        )

        result = MarketData(client).search_instruments(
            "KOSPI200",
            instrument_type="options",
            asset_class="index",
        )

        self.assertEqual(result["match_count"], 1)
        self.assertEqual(result["results"][0]["code"], "201T6000")
        self.assertEqual(result["master_tr"], None)
        self.assertEqual(result["master_trs"], ["t9944", "t8433", "t8435"])

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

        result = MarketData(client).search_instruments("A016C000", asset_class="index")

        self.assertEqual(result["match_count"], 1)
        self.assertEqual(result["results"][0]["name"], "KOSPI200 202612")

    def test_limit_caps_candidates_but_preserves_match_count(self):
        rows = [
            {"hname": f"KOSPI200 {month}", "shcode": f"A016{month}", "expcode": ""}
            for month in ("202612", "202703", "202706")
        ]
        client = FakeClient({"t9943": {"t9943OutBlock": rows}})

        result = MarketData(client).search_instruments(
            "KOSPI200 futures",
            asset_class="index",
            limit=2,
        )

        self.assertEqual(result["match_count"], 3)
        self.assertEqual(result["returned_count"], 2)
        self.assertEqual(len(result["results"]), 2)

    def test_invalid_search_parameters_fail_before_api_call(self):
        client = FakeClient({})

        with self.assertRaises(ValueError):
            MarketData(client).search_instruments("조회해줘")
        with self.assertRaises(ValueError):
            MarketData(client).search_instruments("코스피200", instrument_type="stocks")
        with self.assertRaises(ValueError):
            MarketData(client).search_instruments("코스피200", asset_class="currency")
        with self.assertRaises(ValueError):
            MarketData(client).search_instruments("코스피200", limit=0)
        self.assertEqual(client.calls, [])

    def test_unexpected_master_response_shape_is_an_error(self):
        client = FakeClient(
            {
                ("t9943", (("gubun", ""),)): {
                    "t9943OutBlock": {"hname": "KOSPI200"}
                }
            }
        )

        with self.assertRaises(RuntimeError):
            MarketData(client).search_instruments("KOSPI200", asset_class="index")


if __name__ == "__main__":
    unittest.main()
