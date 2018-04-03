#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@auth: alcorzheng<alcor.zheng@gmail.com>
@file: spider.py
@time: 2018/4/216:54
@desc: 通用爬虫工具
"""

import requests
from bs4 import BeautifulSoup
from das_by_python.common import utils


def spider_cn_dlt():
    url = 'http://www.lottery.gov.cn/historykj/history.jspx?_ltype=dlt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    features = 'lxml'
    rules_tr = 'body > div.yyl > div.yylMain > div.result > table > tbody > tr'
    rules_td_list = [
        # 列名，规则，数据类型，字符处理，列表处理方式(0,不处理；1,)，列表拼接分隔符
        ['id_', 'td:nth-of-type(1)', 'I', ',，- ', 0, None],
        ['date_', 'td:nth-of-type(20)', 'S', None, 0, None],
        ['win_nums_red', 'td.red', 'S', None, 1, ','],
        ['win_nums_blue', 'td.blue', 'S', None, 1, ','],
        ['amount_', 'td:nth-of-type(18)', 'I', ',，- ', 0, None],
        ['prize_first', 'td:nth-of-type(9)', 'I', ',，- ', 0, None],
        ['prize_second', 'td:nth-of-type(13)', 'I', ',，- ', 0, None]
    ]
    print(SpiderTable(url, headers, features, rules_tr, rules_td_list).tbl_datas)


class SpiderTable:
    """爬取页面表格数据"""
    def __init__(self, url, headers, features, rules_tr, rules_td_list, proxy=None, num_retries=2, timeout=5):
        self.url = url
        self.headers = headers
        self.features = features
        self.rules_tr = rules_tr
        # 列名，规则，数据类型，字符处理，是否列表，列表拼接分隔符
        self.rules_td_list = rules_td_list
        self.proxy = proxy
        self.num_retries = num_retries
        self.timeout = timeout
        self.tbl_datas = self.spiderpage()

    def _getpage(self):
        try:
            req = requests.get(self.url, headers=self.headers, proxies=self.proxy)
            req.raise_for_status()
            req.encoding = req.apparent_encoding
            return req
        except requests.HTTPError as e:
            print(e)

    def spiderpage(self):
        soup = BeautifulSoup(self._getpage().content, self.features)
        html_tr_list = soup.select(self.rules_tr)
        if self.rules_td_list is None or len(self.rules_td_list) == 0:
            return html_tr_list
        tr_datas = []
        for html_tr in html_tr_list:
            tr_data = {}
            for rules_td in self.rules_td_list:
                if rules_td[4] == 1:
                    tr_data[rules_td[0]] = rules_td[5].join([
                        utils.obj2oth(
                            data.get_text().strip(),
                            rules_td[2],
                            'replaces',
                            0,
                            oldchars=rules_td[3],
                            newchars=''
                        ) for data in html_tr.select(rules_td[1])
                    ])
                else:
                    tr_data[rules_td[0]] = utils.obj2oth(
                        html_tr.select(rules_td[1])[0].get_text().strip(),
                        rules_td[2],
                        'replaces',
                        None,
                        oldchars=rules_td[3],
                        newchars=''
                    )
            tr_datas.append(tr_data)
        return tr_datas
