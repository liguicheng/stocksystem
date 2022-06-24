import datetime
from urllib.parse import urlencode
import pandas as pd
import requests
import time

from data.data_todb import load_csv


def gen_eastmoney_code(rawcode: str) -> str:
    '''
    生成东方财富专用的secid
    Parameters
    ----------
    rawcode ： 6 位股票代码
    Parameters
    ----------
    str : 按东方财富格式生成的字符串
    '''
    if rawcode[0] != '6':
        return f'0.{rawcode}'
    return f'1.{rawcode}'

def get_day_k_history(code: str, beg: str = '16000101', end: str = '20500101', klt: int = 101, fqt: int = 1) -> pd.DataFrame:
    '''
    功能获取k线数据
    Parameters
    ----------
    code : 6 位股票代码
    beg: 开始日期 例如 20200101
    end: 结束日期 例如 20200201
    klt: k线间距 默认为 101 即日k
        klt:1 1 分钟
        klt:5 5 分钟
        klt:101 日
        klt:102 周
    fqt: 复权方式
        不复权 : 0
        前复权 : 1
            后复权 : 2
    Return
    ------
    DateFrame : 包含股票k线数据
    '''
    EastmoneyKlines = {
        'f51': '时间',
        'f52': '开盘价',
        'f53': '收盘价',
        'f54': '最高价',
        'f55': '最低价',
        'f56': '成交量',
        'f57': '成交额',
        'f58': '振幅',
        'f59': '涨跌幅',
        'f60': '涨跌额',
        'f61': '换手率'
    }
    EastmoneyHeaders = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    fields = list(EastmoneyKlines.keys())
    columns = list(EastmoneyKlines.values())
    fields2 = ",".join(fields)
    secid = gen_eastmoney_code(code)
    params = (
        ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'),
        ('fields2', fields2),
        ('beg', beg),
        ('end', end),
        ('rtntype', '6'),
        ('secid', secid),
        ('klt', f'{klt}'),
        ('fqt', f'{fqt}'),
    )
    base_url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
    url = base_url + '?' + urlencode(params)
    json_response = requests.get(
        url, headers=EastmoneyHeaders).json()
    data = json_response['data']
    # code = data['code']
    # 股票名称
    # name = data['name']
    klines = data['klines']
    rows = []
    for _kline in klines:
        kline = _kline.split(',')
        rows.append(kline)
    df = pd.DataFrame(rows, columns=columns)

    file_name = "../../文件/data/" + code + '_day.csv'
    df.to_csv(file_name, encoding='utf-8-sig', index=None)
    # print(f'股票代码：{code} 的 k线数据已保存到代码目录下的 {code}.csv 文件中')

    # 写入数据库
    load_csv(file_name, 'stock' + code + '_day')


    return df

def get_lastday_close(code):
    lastday = datetime.date.today() + datetime.timedelta(-1)
    lastday_str = str(lastday).split('-')[0] + (str(lastday).split('-')[1]) + (str(lastday).split('-')[2])
    lastday_close = get_day_k_history(code, beg=lastday_str, end=lastday_str)
    while lastday_close.empty:
        lastday = lastday + datetime.timedelta(-1)
        lastday_str = str(lastday).split('-')[0] + (str(lastday).split('-')[1]) + (str(lastday).split('-')[2])
        lastday_close = get_day_k_history(code, beg=lastday_str, end=lastday_str)
    return lastday_close['收盘价'][0]


if __name__ == "__main__":

    # 股票代码
    code = '600521'
    # 根据股票代码、开始日期、结束日期获取指定股票代码指定日期区间的k线数据
    df = get_day_k_history(code, beg="20210401", end="20220401")
    # 保存k线数据到表格里面
    # file_name = "../../文件/data/" + code + '_day.csv'
    # df.to_csv(file_name, encoding='utf-8-sig', index=None)
    # print(f'股票代码：{code} 的 k线数据已保存到代码目录下的 {code}.csv 文件中')

    # print(get_lastday_close('600523'))
