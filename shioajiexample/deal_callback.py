import typing
import shioaji as sj


def get_contracts(api: sj.Shioaji):
    contracts = {
        code: contract
        for name, iter_contract in api.Contracts
        for code, contract in iter_contract._code2contract.items()
    }
    return contracts


class DealCallback:
    def __init__(self, api: sj.Shioaji):
        self.api: sj.shioaji = api
        self.contracts: dict = get_contracts(self.api)

    def deal_callback(self, topic: str, quote: typing.Dict):
        if topic.startswith("MKT"):
            code = topic.split("/")[-1]
            return "{}成交價:{}".format(self.contracts[code].name, quote["Close"][0])
        elif topic.startswith("QUT"):
            code = topic.split("/")[-1]
            return "{}委賣價:{}".format(self.contracts[code].name, quote["AskPrice"][0])
