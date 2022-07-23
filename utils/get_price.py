# -*- coding: utf-8 -*-
# @Author: MarkJiYuan
# @Date:   2019-05-28 18:27:03
# @Last Modified by:   MarkJiYuan
# @email: zhengjiy16@163.com
# @Last Modified time: 2019-05-28 19:51:52
# @Abstract: 用selenium模拟查询操作，通过百度地铁获取地铁票价328 * 328三角矩阵 实在太忙而且蠢，我决定用距离算票价，不确定的边缘距离用这个来查

from selenium import webdriver
import time
import sys


def openChrome():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')

    driver = webdriver.Chrome(chrome_options=option)
    return driver


def operation_get_price(driver, start: str, end: str) -> int:
    elem1 = driver.find_element_by_id("sub_start_input")
    elem1.clear()
    elem1.send_keys(start)

    elem2 = driver.find_element_by_id("sub_end_input")
    elem2.clear()
    elem2.send_keys(end)

    driver.find_element_by_id("search-button").click()

    print('休息一下')
    time.sleep(3)

    price = driver.find_element_by_xpath("//*[@id='rinfo']/span[5]").text
    price = int(price[:-1])

    return price


def getLastedByMap(subway_map_file: str, subway_price_file: str, subway_log_file: str) -> None:
    global start_station, end_station

    driver = openChrome()
    url = "https://map.baidu.com/?subway=index.html"
    driver.get(url)

    station_name_list = []
    with open(subway_map_file, 'r') as f:
        for line in f.readlines():
            if line.strip() != '':
                if line[0] != '&':
                    station_name = line.strip()
                    if station_name not in station_name_list:
                        station_name_list.append(station_name)

    station_name_list = station_name_list[:10]
    length = len(station_name_list)
    print(station_name_list)
    i = 0
    while i < length:
        j = i + 1
        while j < length:
            try:
                start_station = station_name_list[i]
                end_station = station_name_list[j]
                price = operation_get_price(driver, start_station, end_station)
                print(start_station, end_station, price)
                with open(subway_price_file, 'a') as f:
                    f.write(start_station + ' ' + end_station + ' ' + str(price) + '\n')
            except Exception as e:
                with open(subway_log_file, 'a') as log:
                    datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    log.write(start_station + ' ' + end_station + ' ' + '发生不明错误,请重新查询' + i + ' ' + j + ' ' + datetime)
                    print(start_station, end_station, f'发生不明错误{e},请重新查询')
                    sys.exit()
            j += 1
        i += 1

    command = input()
    if command == 'quit':
        driver.quit()


if __name__ == '__main__':
    # get current time format like "2019-05-03"
    time_str = time.strftime("%Y-%m-%d", time.localtime())
    getLastedByMap('../output_file/2019-6-4/subway_map.txt',
                   f'../output_file/{time_str}/price.txt',
                   f'../output_file/{time_str}/log.txt')
