import pytest
import typing
from shioaji.contracts import Stock
from sjexample.deal_callback import DealCallback


@pytest.fixture()
def contracts():
    return {
        "2330": Stock(
            exchange="TSE",
            code="2330",
            symbol="TSE2330",
            name="台積電",
            category="24",
            limit_up=323.0,
            limit_down=265.0,
            reference=294.0,
            update_date="2020/04/23",
            day_trade="Yes",
        ),
        "2890": Stock(
            exchange="TSE",
            code="2890",
            symbol="TSE2890",
            name="永豐金",
            category="17",
            limit_up=12.45,
            limit_down=10.25,
            reference=11.35,
            update_date="2020/04/23",
            day_trade="Yes",
        ),
    }


@pytest.fixture()
def api(mocker):
    api = mocker.MagicMock()
    return api


@pytest.fixture()
def deal_callback(api):
    return DealCallback(api)


testcase_deal_callback = [
    [
        "QUT/idcdmzpcr01/TSE/2330",
        {
            "AskPrice": [296.5, 297.0, 297.5, 298.0, 298.5],
            "AskVolume": [205, 284, 204, 500, 352],
            "BidPrice": [296.0, 295.5, 295.0, 294.5, 294.0],
            "BidVolume": [77, 199, 770, 939, 1483],
            "Date": "2020/04/23",
            "Time": "13:24:55.230350",
        },
        "台積電委賣價:296.5",
    ],
    [
        "MKT/idcdmzpcr01/TSE/2330",
        {
            "AmountSum": [6185660000.0],
            "Close": [284.0],
            "Date": "2020/04/14",
            "TickType": [2],
            "Time": "11:19:48.493616",
            "VolSum": [21832],
            "Volume": [1],
        },
        "台積電成交價:284.0",
    ],
]


@pytest.mark.parametrize("topic, quote, expected", testcase_deal_callback)
def test_deal_callback(
    topic: str,
    quote: typing.Dict,
    expected: str,
    deal_callback: DealCallback,
    contracts: Stock,
):
    deal_callback.contracts = contracts
    res = deal_callback.deal_callback(topic, quote)
    assert res == expected

