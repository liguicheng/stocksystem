import datetime
import pandas as pd

from data.scrapy_day_data import get_lastday_close, get_day_k_history
from data.scrapy_min_data import get_min_k_history
from pathlib import Path
import akshare as ak





def get_data(code):
    dict_return = {} # 存放需要的数据
    data = ts.get_hist_data(code) # 通过股票代码获取股票最近的数据
    data_30 = data[:30].iloc[::-1] # 按照日期正序排列数据
    data_30['rise'] = data_30['price_change'] > 0 # 涨
    data_30['fall'] = data_30['price_change'] < 0 # 跌
    close = data_30['close'] #最近30个交易日的收盘价
    close_index = list(close.index) # 收盘价x轴数据
    close_value = close.values.tolist() # 收盘价y轴数据
    df_diff = data_30[['rise','fall']].sum() # 统计近30交易日的涨跌次数
    df_diff_index = list(df_diff.index) # 将数据转为列表格式
    df_diff_value = df_diff.values.tolist() # 将数据转为列表格式
    dict_return['diff'] = [{"name":item[0],"value":item[1]} for item in list(zip(df_diff_index,df_diff_value))] # 将数据制作成饼图需要的数据格式
    price_change = data_30['price_change'].values.tolist() # 统计近30交易日的价格变化
    volume = data_30['volume'].values.tolist() # 统计近30交易日的成交量
    # 以下为将处理好的数据加入字典
    dict_return['close_index'] = close_index
    dict_return['close_value'] = close_value
    dict_return['price_change'] = price_change
    dict_return['volume'] = volume
    dict_return['df_diff_index'] = df_diff_index
    return dict_return

def get_day_data(code):
    #打开csv文件
    # df = pd.read_csv('../../文件/data/600519_day.csv')
    # my_file = Path('../../文件/data/' + code +'_day.csv')
    # if my_file.exists():
    #     df = pd.read_csv('../../文件/data/' + code +'_day.csv')
    # else:

    today = datetime.date.today()
    lastyear_today = str(int(str(today).split('-')[0]) - 1) + (str(today).split('-')[1]) + (str(today).split('-')[2])
    today = str(today).split('-')[0] + (str(today).split('-')[1]) + (str(today).split('-')[2])

    df = pd.DataFrame
    try:
        df = get_day_k_history(code, beg=lastyear_today, end=today)
    except Exception as e:
        return "该股票不存在"

    result = []
    for date in df['时间']:
        result.append([date])

    for i, time in enumerate(result):
        time.append(str(df['开盘价'][i]))
        time.append(str(df['收盘价'][i]))
        time.append(str(df['最低价'][i]))
        time.append(str(df['最高价'][i]))
        time.append(str(df['成交量'][i]))
    # print(result)
    return result

def get_min_data(code):

    dict_return = {}  # 存放需要的数据

    # 打开csv文件
    # df = pd.read_csv('../../文件/data/600519_min.csv')

    df = get_min_k_history(code)

    dict_return['data'] = []
    date_time = [x for x in df['时间'].str.split(' ')]
    for date, time in date_time:
        dict_return['data'].append([time.split(':')[0] + time.split(':')[1]])

    for i, time in enumerate(dict_return['data']):
        time.append(df['开盘价'][i])
        time.append(str(round((float(df['开盘价'][i]) +  float(df['收盘价'][i])) / 2, 2)))
        time.append(str(df['成交量'][i]))

    # 要替换为昨天的收盘价
    dict_return['yestclose'] = get_lastday_close(code)

    return dict_return


def get_name(code):
    '''通过股票代码导出公司名称'''
    a_code_name_df = ak.stock_info_a_code_name()
    # print(a_code_name_df)
    name = "未识别代码"
    for row in a_code_name_df.iterrows():
        if row[1]['code'] == code:
            name = row[1]['name']
            break
    return name


if __name__ == '__main__':
    # get_min_data('600519')
    # print(get_day_data('600519'))
    print(get_name('600520'))