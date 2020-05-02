import pytest
import typing

from sjexample.compose import DataFrameCompose


@pytest.fixture()
def api(mocker):
    api = mocker.MagicMock()
    return api


@pytest.fixture()
def compose(api):
    return DataFrameCompose(api)


def test_compose(api):
    composer = DataFrameCompose(api)

    assert composer.api.quote.set_quote_callback.called

    composer.api.quote.set_quote_callback.assert_called_once_with(
        composer.quote_callback
    )

    assert composer.df_ticks.columns.tolist() == [
        "ts",
        "seq",
        "code",
        "close",
        "volume",
    ]

    assert composer.df_bidask.columns.tolist() == [
        "ts",
        "code",
        "AskPrice0",
        "AskVolume0",
        "BidPrice0",
        "BidVolume0",
        "AskPrice1",
        "AskVolume1",
        "BidPrice1",
        "BidVolume1",
        "AskPrice2",
        "AskVolume2",
        "BidPrice2",
        "BidVolume2",
        "AskPrice3",
        "AskVolume3",
        "BidPrice3",
        "BidVolume3",
        "AskPrice4",
        "AskVolume4",
        "BidPrice4",
        "BidVolume4",
    ]


def test_compose_get_df_ticks(compose: DataFrameCompose):
    df = compose.get_df_ticks()
    assert df.empty == True


def test_compose_get_df_bidask(compose: DataFrameCompose):
    df = compose.get_df_bidask()
    assert df.empty == True


def test_flatten_tick():
    quote = {
        "AmountSum": [6185660000.0],
        "Close": [284.0],
        "Date": "2020/04/14",
        "TickType": [2],
        "Time": "11:19:48.493616",
        "VolSum": [21832],
        "Volume": [1],
    }
    seq = 0
    expected = {
        "AmountSum": 6185660000.0,
        "Close": 284.0,
        "Date": "2020/04/14",
        "TickType": 2,
        "Time": "11:19:48.493616",
        "VolSum": 21832,
        "Volume": 1,
        "seq": 0,
    }
    tick = DataFrameCompose.flatten_tick(quote, seq)

    assert tick == expected


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
    topic: str, quote: typing.Dict, run_n_time: str, compose: DataFrameCompose,
):

    for i in range(run_n_time):
        compose.quote_callback(topic, quote)
    if topic.startswith("QUT"):
        assert len(compose.get_df_bidask()) == run_n_time
    if topic.startswith("MKT"):
        assert len(compose.get_df_ticks()) == run_n_time
