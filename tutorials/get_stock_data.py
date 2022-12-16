#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName     :get_stock_data.py
# @Time         :2022/11/13 19:49
# @Author       :Henry Feng
# @Description  :获取A股历史交易数据

import akshare as ak

# 个股信息
# print(ak.stock_individual_info_em(symbol="600000"))

ak.stock_zh_a_hist('600000', start_date='20190101', end_date='20201231', adjust='qfq').to_csv('sma_cross_data.csv', index=False)
