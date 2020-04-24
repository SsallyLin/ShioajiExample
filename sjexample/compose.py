import typing
from functools import partial
from collections import deque, defaultdict
import shioaji as sj


class ExampleCompose:
    def __init__(self, api: sj.Shioaji, store_tick_num: int):
        self.api: sj.Shioaji = api
        self.tick_last_n_collector: typing.DefaultDict[str, typing.Deque] = defaultdict(
            partial(deque, maxlen=store_tick_num)
        )
        self.api.quote.set_quote_callback(self.quote_callback)

    def quote_callback(self, topic: str, quote: typing.Dict):
        self.tick_last_n_collector[topic].append(quote)
