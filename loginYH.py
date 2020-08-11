# coding=utf-8

import os
from config import CommonConfig
from pywinauto.application import Application
from time import sleep
import pandas as pd
import easyquotation as eq


class ClientTrade:
    def __init__(self,ts_code):
        self.code = ts_code
        self._app = None
        self._main = None

        self.all_etf_position = None
        self.use_position = None
        self.all_position = None
        self.balance = None

        self.price = None
        self.message = None

    def app(self):
        return self._app

    def main(self):
        return self._main

    @staticmethod
    def _xls2csv(path_type):
        if path_type == "balance":
            try:
                os.renames(CommonConfig.DEFAULT_OLD_BALANCE_PATH, CommonConfig.DEFAULT_BALANCE_PATH)
                return True
            except WindowsError:
                os.remove(CommonConfig.DEFAULT_BALANCE_PATH)
                os.renames(CommonConfig.DEFAULT_OLD_BALANCE_PATH, CommonConfig.DEFAULT_BALANCE_PATH)
                return True
        if path_type == "position":
            try:
                os.renames(CommonConfig.DEFAULT_OLD_POSITION_PATH, CommonConfig.DEFAULT_POSIION_PATH)
                return True
            except WindowsError:
                os.remove(CommonConfig.DEFAULT_POSIION_PATH)
                os.renames(CommonConfig.DEFAULT_OLD_POSITION_PATH, CommonConfig.DEFAULT_POSIION_PATH)
                return True

    def connect(self, exe_path=None, **kwargs):
        """
        直接连接登陆后的客户端
        :param exe_path:
        :param kwargs:
        :return:
        """
        connect_path = exe_path or CommonConfig.DEFAULT_EXE_PATH
        if connect_path is None:
            raise ValueError(
                "参数 exe_path 未设置，请设置客户端对应的 exe 地址,类似 C:\\客户端安装目录\\xiadan.exe"
            )

        self._app = Application().connect(path=connect_path)
        self._main = self._app.top_window()

    def print_control_identifiers(self):
        self._app.window(title="网上股票交易系统5.0", class_name="AfxFrameOrView42s").print_control_identifiers()

    def is_exist_pop_dialog(self):
        sleep(1)  # wait dialog display
        if self._main.wrapper_object() != self._app.top_window().wrapper_object():
            return True
        else:
            return False

    def get_balance(self):
        """
        获取可用资金
        :return: 今天的可以用的资金 float
        """
        self._main.child_window(
            control_id=129, class_name="SysTreeView32").get_item(["查询[F4]", "资金股份"]).click()
        self._main.child_window(
            control_id=1308,class_name="CVirtualGridCtrl").type_keys("^S")
        while self.is_exist_pop_dialog():
            try:
                self._app.top_window()["保存（S）"].click() or self._app.top_window()["是(Y)"].click()
            except Exception as e:
                pass
        if self._xls2csv("balance"):
            df = pd.read_csv(CommonConfig.DEFAULT_BALANCE_PATH,encoding='gbk',sep='\t')
            self.balance = float(df.loc[0, ['可用金额']])
        return self.balance

    def get_all_etf_position(self):
        """
        获取这个ts_code可以用的持仓数量
        :param
        :return: 今天可以用的持仓 int
        """
        self._main.child_window(
            control_id=129, class_name="SysTreeView32").get_item(["查询[F4]", "资金股份"]).click()
        self._main.child_window(
            control_id=1047, class_name="CVirtualGridCtrl").type_keys("^S")
        while self.is_exist_pop_dialog():
            try:
                self._app.top_window()["保存(S)"].click() or self._app.top_window()["是(Y)"].click()
            except Exception as e:
                pass
        if self._xls2csv("position"):
            self.all_etf_position = pd.read_csv(CommonConfig.DEFAULT_POSIION_PATH,encoding='gbk',sep='\t')
        return self.all_etf_position

    def get_position(self):
        df = self.all_etf_position
        df1 = df[df['证券代码'] == int(self.code)]
        self.all_position = int(df1["当前持仓"])
        self.use_position = int(df1["可用余额"])

    def get_price_now(self):
        quotation = eq.use('sina').stocks(self.code)
        self.price = quotation[self.code]['now']

    def trade_buy(self):
        """
        买入
        :return:
        """
        self._main.child_window(
            control_id=129, class_name="SysTreeView32").get_item(["买入[F1]"]).click()
        self._main.child_window(
            control_id=1032,class_name="Edit").type_keys(self.code)
        self._main.child_window(
            control_id=1033, class_name="Edit").type_keys(self.price)
        self._main.child_window(
            control_id=1034, class_name="Edit").type_keys(CommonConfig.DEFAULT_TRADE_AMOUNT)

        self._main.child_window(
            control_id=1006, class_name="Button").click()
        for i in range(2):
            if i == 0 and self.is_exist_pop_dialog():
                self._app.top_window()["是"].click()
            if i == 1 and self.is_exist_pop_dialog():
                self.message = self._app.top_window().child_window(
                    control_id=1004,class_name="Static").window_text()
                self._app.top_window()["确定"].click()

    def trade_sell(self):
        self._main.child_window(
            control_id=129, class_name="SysTreeView32").get_item(["卖出[F2]"]).click()
        self._main.child_window(
            control_id=1032, class_name="Edit").type_keys(self.code)
        self._main.child_window(
            control_id=1033, class_name="Edit").type_keys(self.price)
        self._main.child_window(
            control_id=1034, class_name="Edit").type_keys(CommonConfig.DEFAULT_TRADE_AMOUNT)

        self._main.child_window(
            control_id=1006, class_name="Button").click()
        for i in range(2):
            if i == 0 and self.is_exist_pop_dialog():
                self._app.top_window()["是"].click()
            if i == 1 and self.is_exist_pop_dialog():
                self.message = self._app.top_window().child_window(
                    control_id=1004, class_name="Static").window_text()
                self._app.top_window()["确定"].click()

    def trade_ensure(self, message):
        pass

    def trade_not_buy(self):
        self._main.child_window(
            control_id=129, class_name="SysTreeView32").get_item(["买入[F1]"]).click()
        self._main.type_keys('R')
        self._main.child_window(
            control_id=30001, class_name="Button").click()
        while self.is_exist_pop_dialog():
            try:
                self._app.top_window().child_window(
                    control_id=6, class_name="Button").click()
            except Exception as e:
                self._app.top_window()["确定"].click()

    def trade_not_sell(self):
        self._main.child_window(
            control_id=129, class_name="SysTreeView32").get_item(["卖出[F2]"]).click()
        self._main.type_keys('R')
        self._main.child_window(
            control_id=30001, class_name="Button").click()
        while self.is_exist_pop_dialog():
            try:
                self._app.top_window().child_window(
                    control_id=6, class_name="Button").click()
            except Exception as e:
                self._app.top_window()["确定"].click()


