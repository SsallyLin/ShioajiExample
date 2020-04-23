import pytest
import typing

from sjexample.compose import ExampleCompose
from collections import deque


@pytest.fixture()
def api(mocker):
    api = mocker.MagicMock()
    return api


@pytest.fixture()
def example_compose(api):
    return ExampleCompose(api, store_tick_num=5)


def test_example_compose(api):
    n = 5
    composer = ExampleCompose(api, store_tick_num=n)

    assert composer.api.quote.set_quote_callback.called

    composer.api.quote.set_quote_callback.assert_called_once_with(
        composer.quote_callback
    )

    assert composer.tick_last_n_collector.default_factory.keywords == dict(maxlen=n)


testcase_quote_callback = [
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
        10,
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
        3,
    ],
]


@pytest.mark.parametrize("topic, quote, run_n_time", testcase_quote_callback)
def test_quote_callback(
    topic: str, quote: typing.Dict, run_n_time: str, example_compose: ExampleCompose,
):

    for i in range(run_n_time):
        example_compose.quote_callback(topic, quote)

    assert (
        len(example_compose.tick_last_n_collector[topic]) == 5
        if run_n_time > 5
        else run_n_time
    )

    assert example_compose.tick_last_n_collector[topic] == deque(
        [quote] * (5 if run_n_time > 5 else run_n_time)
    )
