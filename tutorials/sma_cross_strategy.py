#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName     :sma_cross_strategy.py
# @Time         :2022/11/13 15:56
# @Author       :Henry Feng
# @Description  :该策略根据日k线确定某一股票的买卖实际：当收盘价上穿5日均线时，若无仓位，则市价买入；当收盘价下穿5日均线时，则市价卖出。

from datetime import datetime
import backtrader as bt
import os.path
import sys


class SmaClass(bt.Strategy):
    params = dict(period=5)

    def __init__(self):
        # 初始化移动平均线指标
        self.move_average = bt.ind.MovingAverageSimple(
            self.datas[0].close, period=self.params.period
        )

    def next(self):
        if not self.position.size:  # 没有持仓
            # 当日收盘价上穿5日均线，创建买单
            if self.datas[0].close[-1] < self.move_average.sma[0] < self.datas[0].close[0]:
                self.buy(size=100)
                # print("buy", self.datas[0])
        # 持仓，并且当日收盘价下破5日均线，创建卖单
        elif self.datas[0].close[0] < self.move_average.sma[0] < self.datas[0].close[-1]:
            self.sell(size=100)
            # print("sell", self.datas[0])


############
# 主程序
############

# 创建大脑引擎对象
cerebro = bt.Cerebro()

# 获取本脚本文件所在路径
modepath = os.path.dirname(os.path.abspath(sys.argv[0]))

# 拼接得到数据文件全路径
datapath = os.path.join(modepath, './sma_cross_data.csv')

# 创建行情数据对象，加载数据
data = bt.feeds.GenericCSVData(
    dataname=datapath,
    datetime=0,  # 日期行所在列
    open=1,  # 开盘价所在列
    close=2,  # 收盘价所在列
    high=3,  # 最高价所在列
    low=4,  # 最低价所在列
    volume=5,  # 成交量所在列
    openinterest=-1,  # 无未平仓量列（openinterest是期货交易使用）
    dtformat='%Y-%m-%d',  # 日期格式
    fromdate=datetime(2019, 1, 1),  # 起始日
    todate=datetime(2020, 7, 8)  # 结束日
)

cerebro.adddata(data)  # 将行情数据对象注入引擎
cerebro.addstrategy(SmaClass)  # 将策略注入引擎
cerebro.broker.setcash(10000.0)  # 设置初始资金
cerebro.run()  # 运行
print('最终市值: %.2f' % cerebro.broker.getvalue())

cerebro.plot(style='bar')
