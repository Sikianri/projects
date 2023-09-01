"""使用标准库 做一个终端里的液晶时钟 
使用CTRL + C 退出 
ps: 这是我人生中独立写的第一个小项目
"""
import sys
import datetime
import time
import os

LCD_NUMBERS = {  # 数字的上中下三段液晶样式
    0 : [' __ ', '|  |', '|__|'],
    1 : ['    ', '   |', '   |'],
    2 : [' __ ', ' __|', '|__ '],
    3 : [' __ ', ' __|', ' __|'],
    4 : ['    ', '|__|', '   |'],
    5 : [' __ ', '|__ ', ' __|'],
    6 : [' __ ', '|__ ', '|__|'],
    7 : [' __ ', '   |', '   |'],
    8 : [' __ ', '|__|', '|__|'],
    9 : [' __ ', '|__|', ' __|'],
    }
DUCK = [  # 小黄鸭
    '    _   ',
    ' __(.)< ',
    ' \___)  '
    ]


def number_to_lcd(num):  # 把数字改为液晶样式
    return LCD_NUMBERS.get(num, LCD_NUMBERS[0])  # 提供相应的液晶样式，如果错误则默认提供0的样式


def display_lcd_time(hour, minute, second):  # 打印液晶时间
        left_hour, right_hour = number_to_lcd(hour // 10), number_to_lcd(hour % 10)  # 更新为当前小时的液晶样式
        left_minute, right_minute = number_to_lcd(minute // 10), number_to_lcd(minute % 10)  # 更新为当前分钟的液晶样式
        left_second, right_second = number_to_lcd(second // 10),number_to_lcd(second % 10)  # 更新为当前秒的液晶样式

        os.system('cls' if os.name == 'nt' else 'clear')  # 清空屏幕
        for i in range(3):  # 在终端打印出液晶时间
            print(left_hour[i] + right_hour[i] + '    ' + left_minute[i] + right_minute[i] + '    ' + left_second[i] + right_second[i] + '    ' + DUCK[i])
        print()


def get_time(hours=24): 
    while True:
        current_time = datetime.datetime.now()  # 获取当前时间
        next_tick = current_time + datetime.timedelta(seconds=1)  # 计算到下一秒的剩余时间
        hour, minute, second = current_time.hour % hours, current_time.minute, current_time.second  # 分别获取当前的小时、分钟和秒
        display_lcd_time(hour,minute, second)  # 打印时间

        sleep_time = get_sleep_time(next_tick)  # 获取需要休眠的时间
        if sleep_time > 0:
            time.sleep(sleep_time)
            

def get_sleep_time(next_tick):  # 计算休眠时间
    return (next_tick - datetime.datetime.now()).total_seconds()


def main():
    print("\n 液晶时钟，按 CTRL+C 退出")
    time.sleep(1)  # 显示提示1秒
    try:
        get_time()
    except KeyboardInterrupt:
        print("\n 液晶时钟已停止。")
        sys.exit()


if __name__ == "__main__":
    main()