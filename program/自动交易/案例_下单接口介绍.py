"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

## 注意：原版本已经无法正常运行，可以直接参考论坛：
以及使用文件：
案例_下单接口介绍_新版.py

演示各个下单操作
"""
# import easytrader_xingbuxing  # 导入自动交易的库
from program.自动交易.Xbx_auto_trade import *

pd.set_option('expand_frame_repr', False)


# =====创建自动下单对象
# 使用同花顺客户端进行下单
ths = easytrader_xingbuxing.use('ths')
# 填入交易客户端的路径。即安装目录下的xiadan.exe的地址
ths.connect(r'C:\同花顺软件\同花顺\xiadan.exe')

# =====获取账户资金状况
# balance_info = xbx_get_balance(ths, max_try_count=3)
# print(balance_info)
# print(type(balance_info), balance_info['资金余额'])  # 返回结果是一个dict

# =====获取持仓
# position_info = xbx_get_position(ths, max_try_count=3)
# if position_info.empty:
#     print('没有持仓')
# else:
#     print(position_info)  # 返回结果是一个DataFrame

# =====下单交易
# ===限价买单
# order_info = xbx_buy(ths, code='600823', price=5, amount=100, max_try_count=3)  # 600823
# print(order_info)  # 返回order_id，即为合同编号：{'entrust_no': '74671'}
# order_num = order_info['entrust_no']
# print('订单编号：', order_num)

# ===下单特殊情况
# 未上市、停牌、退市的股票无法操作，尝试600001，提交失败：-990221020[-990221020]无此证券代码!
# 委托股数不对：easytrader.exceptions.TradeError: 提交失败：-150904070[-150904070] 委托数量必须是每手股(张)数的倍数。
# 委托价格最多小数点后两位，精度太高，会四舍五入。例如 5.423会取整为5.42
# 不能提交低于跌停价，高于涨停价的价格: 提交失败：-990265060[-990265060]委托价格超过涨停价格。
# 资金余额不够，尝试600519：提交失败：-150906130[-150906130]资金可用数不足,尚需322944.07。
# 不在交易时间，提交失败：-990297020[-990297020]当前时间不允许做该项业务。
# 断网会直接报错

# ===限价卖单，同买单一样
# order_info = xbx_sell(ths, code='000005', price=0.55, amount=100)

# ===市价单，不需要填价格
# order_info = xbx_market_buy(ths, code='600823', amount=100)
# order_info = xbx_market_sell(ths, code='600823', amount=100)

# =====撤单
# order_num = '150576'
# cancel_info = xbx_cancel_entrust(ths, order_num, max_try_count=3)
# print(cancel_info)  # {'message': '您的撤单委托已成功提交，合同编号：104332。'}

# =====查询订单
# 查看今日所有的委托
# entrust_info = xbx_get_today_entrusts(ths)
# if entrust_info.empty:
#     print('今日没有委托')
# else:
#     print(entrust_info)

# 查看今日所有订单
# trade_info = xbx_get_today_trades(ths)
# if trade_info.empty:
#     print('今日没有订单')
# else:
#     print(trade_info)
