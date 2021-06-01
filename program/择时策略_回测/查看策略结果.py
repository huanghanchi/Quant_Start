from Functions import cal_fuquan_price, cal_zhangting_price
from Signals import simple_moving_average_signal
from Position import position_at_close
from Evaluate import equity_curve_with_long_at_close
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读入股票数据
stock_code = 'sh600000'
df = pd.read_csv(r'C:\Users\SpiceeYJ\Desktop\量化投资\stock\%s.csv' % stock_code, encoding='gbk', skiprows=1, parse_dates=['交易日期'])
df.sort_values(by=['交易日期'], inplace=True)
df.drop_duplicates(subset=['交易日期'], inplace=True)
df.reset_index(inplace=True, drop=True)

# 计算复权价格、涨停价格
df = cal_fuquan_price(df, fuquan_type='后复权')
df = cal_zhangting_price(df)

# 参数
para = [10, 30]

# 计算交易信号
df = simple_moving_average_signal(df, para=para)
# print(df)
# exit()
# 计算实际持仓
df = position_at_close(df)

# 选择时间段
# 截取上市一年之后的数据
df = df.iloc[250 - 1:]  # 股市一年交易日大约250天
# 截图2007年之后的数据
df = df[df['交易日期'] >= pd.to_datetime('20070101')]  # 一般可以从2006年开始

# 计算资金曲线
df = equity_curve_with_long_at_close(df, c_rate=2.5/10000, t_rate=1.0/1000, slippage=0.01)

#print(df)

equity_curve = df.iloc[-1]['equity_curve']
equity_curve_base = df.iloc[-1]['equity_curve_base']
print(para, '策略最终收益：', equity_curve)

df.set_index('交易日期', inplace=True)
plt.plot(df['equity_curve'])
plt.plot(df['收盘价_复权'] / df.loc['2007-01-04', '收盘价_复权'])
plt.legend(loc='best')
plt.show()
print(df)