# -*- coding: utf-8 -*-

"""
BitMEX 注文関連ライブラリ(仮)
"""
import ccxt
import json

__author__ = "Lepus <lepuspy@gmail.com>"
__version__ = "1.0"
__date__    = "2018/08/10"

# BITMEXのAPIキーとSECRETキー
API = {
    "api": {
        "apiKey": "**************", 
        "secret": "**************"},
    "test": {
        "apiKey": "**************", 
        "secret": "**************"}}

# 通貨ペアの選択
PAIR = "XBTUSD"
# テストネットの選択
TEST = True

class Bitmex:
    def __init__(self):
        access = "api"
        if TEST:
            access = "test"
        self.client = ccxt.bitmex(API[access])
        self.client.urls["api"] = self.client.urls[access]
        self.pair = PAIR

    def _order(self, data, method_name):
        """ccxt関数呼び出し"""
        try:
            res = eval(f"self.client.{method_name}(data)")
        except Exception as e:
            print(e)
        else:
            return res

    def market(self, size, **data):
        """成行注文"""
        data.update({"symbol": self.pair, "orderQty": size, "ordType": "Market"})
        return self._order(data ,"privatePostOrder")

    def limit(self, size, price, **data):
        """指値注文"""
        data.update({"symbol": self.pair, "orderQty": size, "price": price})
        return self._order(data ,"privatePostOrder")
    
    def stop(self, size, trigger_price, **data):
        """STOP注文"""
        data.update({"symbol": self.pair, "orderQty": size, "stopPx": trigger_price, "ordType": "Stop"})
        return self._order(data ,"privatePostOrder")

    def stop_limit(self, size, trigger_price, **data):
        """STOP LIMIT注文"""
        data.update({"symbol": self.pair, "orderQty": size, "stopPx": trigger_price, "price": price, "ordType": "StopLimit"})
        return self._order(data ,"privatePostOrder")

    def trailing_stop(self, size, price_offset, **data):
        """トレーリング注文"""
        data.update({"symbol": self.pair, "orderQty": size, "pegOffsetValue": price_offset, "pegPriceType": "TrailingStopPeg", "ordType": "Stop"})
        return self._order(data ,"privatePostOrder")

    def bulk(self, *params):
        """一括注文"""
        data = {"orders": json.dumps(list(params))}
        return self._order(data ,"privatePostOrderBulk")

    def edit(self, **data):
        """注文内容変更"""
        return self._order(data ,"privatePutOrder")

    def cancel(self, **data):
        """注文個別キャンセル"""
        return self._order(data ,"privateDeleteOrder")

    def cancel_all(self, **data):
        """注文一括キャンセル"""
        return self._order(data ,"privateDeleteOrderAll")

    def active_orders(self, reverse=True, **data):
        """注文情報確認"""
        data.update({"symbol": self.pair, "filter": json.dumps({"open": True}), "reverse": reverse})
        return self._order(data ,"privateGetOrder")
        

    def history_orders(self, reverse=True, **data):
        """注文履歴"""
        data.update({"symbol": self.pair, "reverse":reverse})
        return self._order(data ,"privateGetOrder")