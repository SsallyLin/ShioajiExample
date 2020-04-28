import typing
from functools import partial
from collections import deque, defaultdict
import shioaji as sj
from shioaji.data import Snapshot


class ExampleCompose:
    def __init__(self, api: sj.Shioaji, store_tick_num: int):
        self.api: sj.Shioaji = api
        self.tick_last_n_collector: typing.DefaultDict[str, typing.Deque] = defaultdict(
            partial(deque, maxlen=store_tick_num)
        )
        self.api.quote.set_quote_callback(self.quote_callback)

    def quote_callback(self, topic: str, quote: typing.Dict):
        self.tick_last_n_collector[topic].append(quote)


class TouchPriceCompose:
    def __init__(self, api: sj.Shioaji):
        self.api: sj.Shioaji = api
        self.infos: typing.Dict[str, Snapshot] = {}
        self.api.quote.set_quote_callback(self.quote_callback)

    def subscribe_tick(self, stock: str):
        contract = self.api.Contracts.Stocks[stock]
        self.api.quote.subscribe(contract, quote_type="tick")
        self.api.quote.subscribe(contract, quote_type="bidask")
        self.infos = {stock: self.api.snapshots([contract]).snapshot[0]}

    def quote_callback(self, topic: str, quote: typing.Dict):
        if topic.startswith("MKT/"):
            code = topic.split("/")[-1]
            snapshot = self.infos.get(code, None)
            if snapshot:
                snapshot.close = quote["Close"][0]
                snapshot.high = (
                    snapshot.close if snapshot.high < snapshot.close else snapshot.high
                )
                snapshot.low = (
                    snapshot.close if snapshot.low > snapshot.close else snapshot.low
                )
                snapshot.total_volume = quote["VolSum"][0]
                snapshot.volume = quote["Volume"][0]
                print(self.infos)
        elif topic.startswith("QUT/"):
            code = topic.split("/")[-1]
            snapshot = self.infos.get(code, False)
            if snapshot:
                snapshot.buy_price = quote["BidPrice"][0]
                snapshot.sell_price = quote["AskPrice"][0]
                print(self.infos)
