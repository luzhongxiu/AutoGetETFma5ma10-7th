import ConnSQL
from config import CommonConfig
import TradeTime
import loginYH


def loop_process(trade):
    while TradeTime.if_trade_time():
        pass


def main():
    trade = loginYH.ClientTrade(CommonConfig.DEFAULT_EXE_PATH)
    loop_process(trade)


if __name__ == '__main__':
    main()