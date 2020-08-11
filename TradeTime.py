# coding=utf-8
import easyutils as eu


def if_trade_time():
    """
    判断是否为交易时间，返回值为1或者0
    :return:
    """
    if not eu.is_holiday_today():
        if eu.is_tradetime_now():
            return True
        else:
            return False
    else:
        return False
