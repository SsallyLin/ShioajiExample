import pytest
import typing

from sjexample.compose import TouchPriceCompose
from shioaji.data import Snapshots, Snapshot


@pytest.fixture()
def api(mocker):
    api = mocker.MagicMock()
    return api


@pytest.fixture()
def touchprice_compose(api):
    return TouchPriceCompose(api)


@pytest.fixture()
def snapshot():
    return Snapshot(
        ts=1588070727273000000,
        code="2890",
        exchange="TSE",
        open=11.6,
        high=11.65,
        low=11.45,
        close=11.5,
        tick_type="Sell",
        change_price=0.0,
        change_rate=0.0,
        change_type="Unchanged",
        average_price=11.53,
        volume=1,
        total_volume=4278,
        amount=11500,
        total_amount=49311750,
        yesterday_volume=12048.0,
        buy_price=11.5,
        buy_volume=160.0,
        sell_price=11.55,
        sell_volume=286,
        volume_ratio=0.36,
    )


def test_touchprice_compose(api):
    composer = TouchPriceCompose(api)
    assert composer.api.quote.set_quote_callback.called
    composer.api.quote.set_quote_callback.assert_called_once_with(
        composer.quote_callback
    )


def test_subscribe_tick(api):
    composer = TouchPriceCompose(api)
    composer.subscribe_tick(stock="2890")
    assert composer.api.quote.subscribe.call_count == 2


testcase_quote_callback = [
    [
        "QUT/idcdmzpcr01/TSE/2890",
        {
            "AskPrice": [11.6, 11.65, 11.7, 11.75, 11.8],
            "AskVolume": [284, 720, 573, 536, 74],
            "BidPrice": [11.55, 11.5, 11.45, 11.4, 11.35, 11.3],
            "BidVolume": [157, 602, 726, 249, 485],
            "Date": "2020/04/28",
            "Time": "10:47:08.956636",
        },
        Snapshot(
            ts=1588070727273000000,
            code="2890",
            exchange="TSE",
            open=11.6,
            high=11.65,
            low=11.45,
            close=11.5,
            tick_type="Sell",
            change_price=0.0,
            change_rate=0.0,
            change_type="Unchanged",
            average_price=11.53,
            volume=1,
            total_volume=4278,
            amount=11500,
            total_amount=49311750,
            yesterday_volume=12048.0,
            buy_price=11.55,
            buy_volume=160.0,
            sell_price=11.6,
            sell_volume=286,
            volume_ratio=0.36,
        ),
    ],
    [
        "MKT/idcdmzpcr01/TSE/2890",
        {
            "AmountSum": [49484400.0],
            "Close": [11.8],
            "Date": "2020/04/28",
            "TickType": [2],
            "Time": "10:47:04.674598",
            "VolSum": [4293],
            "Volume": [1],
        },
        Snapshot(
            ts=1588070727273000000,
            code="2890",
            exchange="TSE",
            open=11.6,
            high=11.8,
            low=11.45,
            close=11.8,
            tick_type="Sell",
            change_price=0.0,
            change_rate=0.0,
            change_type="Unchanged",
            average_price=11.53,
            volume=1,
            total_volume=4293,
            amount=11500,
            total_amount=49311750,
            yesterday_volume=12048.0,
            buy_price=11.5,
            buy_volume=160.0,
            sell_price=11.55,
            sell_volume=286,
            volume_ratio=0.36,
        ),
    ],
]


@pytest.mark.parametrize("topic, quote, update_snapshot", testcase_quote_callback)
def test_quote_callback(
    topic: str,
    quote: typing.Dict,
    update_snapshot: Snapshot,
    snapshot: Snapshot,
    touchprice_compose: TouchPriceCompose,
):
    touchprice_compose.infos = {"2890": snapshot}
    touchprice_compose.quote_callback(topic, quote)
    assert touchprice_compose.infos["2890"] == update_snapshot
