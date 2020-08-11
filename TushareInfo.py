# coding=utf-8

import tushare as ts
import easyquotation as eq
import time
import easyutils as et


def code_convert(code):
    if len(code) == 6:
        stock_type = et.get_stock_type(code)
        stock_code = code + "." + stock_type
        return stock_code
    if "." in code and len(code) == 9:
        stock_code = code[0:6]
        return stock_code


def get_price_now(ts_code):
    """
    获取现在etf的价格
    :param ts_code:
    :return: 返回当前的价格 float
    """
    quo = eq.use("sina").stocks(ts_code)
    print(quo[ts_code]["now"])
    print(type(quo))
    return quo


def get_ma_n(ts_code, min_n, ma_n):
    """
    得到某只信息 多少分钟、几个周期内的信息
    :param ts_code: etf代码
    :param min_n: 60min数据或30min数据
    :param ma_n: 几个周期
    :return: 返回一个dataframe的值
    """
    df = "某只股票，的30min或者60min ，maN及ma2N的信息"
    return df


def tushare_set_token():
    ts.set_token("8245313cabb6239a4dce3591e2c64fa199611ee7ade564cf9e437b61")
    return ts


def get_all_etf():
    pro = ts.pro_api("8245313cabb6239a4dce3591e2c64fa199611ee7ade564cf9e437b61")
    df = pro.fund_basic(market="E")
    df_etf = df[df['name'].str.contains('ETF')]
    return df_etf


def get_high_wave_stcok(wave_rate):
    pass


