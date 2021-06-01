"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

## 注意：原版本已经无法正常运行，可以直接参考论坛：
以及使用文件：
案例_下单完整流程_新版.py

完整实验整个交易流程，进行多次循环尝试：
1. 账户余额查询
2. 持仓查询
3. 限价买入股票
4. 撤单
5. 查询当日委托
6. 查询今日成交
"""
import warnings

# import easytrader_xingbuxing as et
from program.自动交易.Xbx_auto_trade import *

pd.set_option('expand_frame_repr', False)
warnings.filterwarnings("ignore")

# 使用同花顺客户端进行下单
ths = et.use('ths')
# 填入交易客户端的路径。即安装目录下的 xiadan.exe 的地址
ths.connect(r'C:\同花顺软件\同花顺\xiadan.exe')

stock_code = '600823'
buy_price = 5.0

# 循环整个流程n次
for _ in range(3):
    print('*' * 10, '开始本次下单测试循环', '*' * 10)
    ths.clear()  # 清理不必要的弹窗

    # =====获取账户资金状况
    print('\n账户资金状况：')
    balance_info = xbx_get_balance(ths)
    print(balance_info)
    time.sleep(2)

    # =====获取持仓
    print('\n账户持仓状况：')
    ths.clear()  # 清理不必要的弹窗
    position_info = xbx_get_position(ths)
    if position_info.empty:
        print('没有持仓')
    else:
        print(position_info)
    time.sleep(1)

    # =====下单交易：限价买单
    print('\n准备下单买入股票：')
    order_info = xbx_buy(ths, code=stock_code, price=buy_price, amount=100)
    print('买入股票成功：', order_info)
    time.sleep(1)

    # =====撤单
    print('\n准备撤单买入的股票：')
    order_num = order_info.get('entrust_no') if order_info else None
    cancel_info = xbx_cancel_entrust(ths, order_num)
    print('撤单成功：', cancel_info)
    time.sleep(1)

    # =====撤单后查询当日委托
    print('\n准备查询当日所有的委托：')
    ths.clear()  # 清理不必要的弹窗
    entrust_info = xbx_get_today_entrusts(ths)
    if entrust_info.empty:
        print('没有委托')
    else:
        print(entrust_info)
    time.sleep(1)

    # =====查看今日成交
    print('\n准备查询当日所有的成交：')
    ths.clear()  # 清理不必要的弹窗
    trade_info = xbx_get_today_trades(ths)
    if trade_info.empty:
        print('没有成交记录')
    else:
        print(trade_info)

    print('本次下单测试循环结束', '\n' * 3)
    time.sleep(10)

"""
>>>> 重要注意事项 <<<<
1. xiadan.exe程序可能会崩溃，重新启动即可。建议每天开盘前重启xiadan.exe
2. 运行过程中不要把交易窗口最小化或者关闭,不要使用鼠标干预。
3. 关闭其他不用软件，例如360杀毒等。保持环境整洁。
4. 运行前切换为英文输入法。
5. 因为每个人的电脑环境问题，不是所有人都能正常运行，有任何问题请联系助教。
"""