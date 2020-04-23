import pytest
import typing
from shioaji.contracts import Stock
from sjexample.compose import ExampleCompose


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
def example_compose(api):
    return ExampleCompose(api, store_tick_num=10)


def test_example_compose(api):
    composer = ExampleCompose(api, store_tick_num=5)
    assert composer.api.quote.set_quote_callback.called
