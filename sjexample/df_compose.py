import typing
import numpy as np
import pandas as pd
import shioaji as sj



class DataFrameCompose:
    def __init__(self, api: sj.Shioaji):
        self.api: sj.Shioaji = api
        self.tick_count = 0
        self.bidask_count = 0
        # init df_ticks and fixed it's dtype
        self.df_ticks = pd.DataFrame(
            index=np.arange(0, 100000),
            columns=["ts", "seq", "code", "close", "volume"],
        )
        self.df_ticks["ts"] = self.df_ticks["ts"].astype("datetime64[ns]")
        self.df_ticks["seq"] = 0
        self.df_ticks["seq"] = self.df_ticks["seq"].astype("int")
        self.df_ticks["code"] = self.df_ticks["code"].astype("str")
        self.df_ticks["close"] = self.df_ticks["close"].astype("float")
        self.df_ticks["volume"] = 0
        self.df_ticks["volume"] = self.df_ticks["volume"].astype("int")
        # init df_bidask
        self.bidask_col = ("AskPrice", "AskVolume", "BidPrice", "BidVolume")
        self.df_bidask = pd.DataFrame(
            index=np.arange(0, 100000),
            columns=(
                ["ts", "code"]
                + [
                    col
                    for cols in [[f"{c}{i}" for c in self.bidask_col] for i in range(5)]
                    for col in cols
                ]
            ),
        )
        self.df_bidask["ts"] = self.df_bidask["ts"].astype("datetime64[ns]")
        self.df_bidask["code"] = self.df_bidask["code"].astype("str")
        for i in range(5):
            for col in ["AskPrice", "BidPrice"]:
                self.df_bidask[f"{col}{i}"] = self.df_bidask[f"{col}{i}"].astype(
                    "float"
                )
            for col in ["AskVolume", "BidVolume"]:
                self.df_bidask[f"{col}{i}"] = 0
                self.df_bidask[f"{col}{i}"] = self.df_bidask[f"{col}{i}"].astype("int")

        self.api.quote.set_quote_callback(self.quote_callback)

    @staticmethod
    def flatten_tick(ticks: dict, seq: int):
        tick = {
            k: v[seq] if isinstance(v, (list, tuple)) else v for k, v in ticks.items()
        }
        tick["seq"] = seq
        return tick

    def get_df_ticks(self):
        return self.df_ticks[: self.tick_count]

    def get_df_bidask(self):
        return self.df_bidask[: self.bidask_count]

    def quote_callback(self, topic: str, quote: typing.Dict):
        if topic.startswith("MKT"):
            for seq, _ in enumerate(quote["Close"]):
                tick = DataFrameCompose.flatten_tick(quote, seq)
                self.df_ticks.loc[self.tick_count, "ts"] = pd.to_datetime(
                    f"{tick['Date']} {tick['Time']}", format="%Y%m%d %H:%M:%S.%f"
                )
                self.df_ticks.loc[self.tick_count, "seq"] = seq
                self.df_ticks.loc[self.tick_count, "code"] = topic.split("/")[-1]
                self.df_ticks.loc[self.tick_count, "close"] = tick["Close"]
                self.df_ticks.loc[self.tick_count, "volume"] = tick["Volume"]
                self.tick_count += 1
        if topic.startswith("QUT"):
            self.df_bidask.loc[self.bidask_count, "ts"] = pd.to_datetime(
                f"{quote['Date']} {quote['Time']}", format="%Y%m%d %H:%M:%S.%f"
            )
            self.df_bidask.loc[self.bidask_count, "code"] = topic.split("/")[-1]
            for i in range(5):
                for col in self.bidask_col:
                    self.df_bidask.loc[self.bidask_count, f"{col}{i}"] = quote[col][i]
            self.bidask_count += 1
