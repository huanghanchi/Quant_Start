"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

一键买入十个股票，每个股票买入100股
"""
import easytrader
import pandas as pd
import time
import warnings
from urllib.request import urlopen  # python自带爬虫库

def get_content_from_internet(url, max_try_num=10, sleep_time=5):
    """
    使用python自带的urlopen函数，从网页上抓取数据
    :param url: 要抓取数据的网址
    :param max_try_num: 最多尝试抓取次数
    :param sleep_time: 抓取失败后停顿的时间
    :return: 返回抓取到的网页内容
    """
    get_success = False  # 是否成功抓取到内容
    # 抓取内容
    for i in range(max_try_num):
        try:
            content = urlopen(url=url, timeout=10).read()  # 使用python自带的库，从网络上获取信息
            get_success = True  # 成功抓取到内容
            break
        except Exception as e:
            print('抓取数据报错，次数：', i+1, '报错内容：', e)
            time.sleep(sleep_time)

    # 判断是否成功抓取内容
    if get_success:
        return content
    else:
        raise ValueError('使用urlopen抓取网页数据不断报错，达到尝试上限，停止程序，请尽快检查问题所在')

def get_today_data_from_sinajs(code_list):
    """
    返回一串股票最近一个交易日的相关数据
    从这个网址获取股票数据：http://hq.sinajs.cn/list=sh600000,sz000002,sz300001
    正常网址：https://finance.sina.com.cn/realstock/company/sh600000/nc.shtml,
    :param code_list: 一串股票代码的list，可以多个，例如[sh600000, sz000002, sz300001],
    :return: 返回一个存储股票数据的DataFrame
    """

    # 构建url
    url = "http://hq.sinajs.cn/list=" + ",".join(code_list)

    # 抓取数据
    content = get_content_from_internet(url)
    content = content.decode('gbk')

    # 将数据转换成DataFrame
    content = content.strip()  # 去掉文本前后的空格、回车等
    data_line = content.split('\n')  # 每行是一个股票的数据
    data_line = [i.replace('var hq_str_', '').split(',') for i in data_line]
    df = pd.DataFrame(data_line, dtype='float')  #

    # 对DataFrame进行整理
    df[0] = df[0].str.split('="')
    df['stock_code'] = df[0].str[0].str.strip()
    df['stock_name'] = df[0].str[-1].str.strip()
    df['candle_end_time'] = df[30] + ' ' + df[31]  # 股票市场的K线，是普遍以当跟K线结束时间来命名的
    df['candle_end_time'] = pd.to_datetime(df['candle_end_time'])
    # print(df)
    rename_dict = {1: 'open', 2: 'pre_close', 3: 'close', 4: 'high', 5: 'low', 6: 'buy1', 7: 'sell1',
                   8: 'amount', 9: 'volume', 32: 'status'}  # 自己去对比数据，会有新的返现
    # 其中amount单位是股，volume单位是元
    df.rename(columns=rename_dict, inplace=True)
    # print(df)
    # print(df['status'])
    df['status'] = df['status']#.str.strip('";')
    df = df[['stock_code', 'stock_name', 'candle_end_time', 'open', 'high', 'low', 'close', 'pre_close', 'amount',
             'volume', 'buy1', 'sell1', 'status']]

    return df

pd.set_option('expand_frame_repr', False)
warnings.filterwarnings("ignore")

# =====客户端初始化
user = easytrader.use('yh_client')  # 选择银河客户端

# 输入用户名和密码，以及程序的路径
user.prepare(
    user='410170012049', password='430911',
    exe_path=r'C:\apps\双子星金融终端-中国银河证券\Binarystar.exe'
)

# =====获取账户资金状况
balance = pd.DataFrame(user.balance)
print('\n账户资金状况：')
print(balance)
exit()
# =====获取持仓
position_info = pd.DataFrame(user.position)
if position_info.empty:
    print('没有持仓')
else:
    print(position_info)
time.sleep(1)

# =====下单交易
stock_code_list = [
    'sh600010', 'sh600022', 'sh600157', 'sh600255', 'sh601258',
    'sh603077', 'sz002131', 'sz002509', 'sz002610', 'sz300116'
]
slippery_rate = 2 / 1000  # 设置下单运行的滑点
# 获取最新股价
price_df = get_today_data_from_sinajs(stock_code_list)

for stock_code in stock_code_list:
    security_code = stock_code[2:]  # 生成下单需要的证券代码
    print()
    print('>' * 5, '准备下单买入股票', security_code, '<' * 5)
    # 买入限价
    sell1_price = price_df[price_df['stock_code'] == stock_code].iloc[-1]['sell1']
    sell1_price = sell1_price * (1 + slippery_rate)  # 加入滑点价格

    try:
        result = user.buy(
            security_code, '%s' % (round(sell1_price, 2)), '100'
        )  # 这边可以优化买入数量
    except easytrader.exceptions.TradeError as e:
        print(security_code, '交易失败', str(e))
        continue

    print(security_code, '买入股票成功：', result)

# =====获取今日委托
today_entrusts = pd.DataFrame(user.today_entrusts)
print('\n今日委托：')
print(today_entrusts)

# =====查看今日成交
today_trades = pd.DataFrame(user.today_trades)
print('\n今日成交：')
print(today_trades)
