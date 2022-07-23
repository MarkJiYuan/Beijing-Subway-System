# -*- coding: utf-8 -*-
# @Author: MarkJiYuan
# @Date:   2019-05-28 11:08:03
# @Last Modified by:   MarkJiYuan
# @email: zhengjiy16@163.com
# @Last Modified time: 2019-05-28 18:54:55
# @Abstract: 通过高德api，获取地铁站经纬度，然后很不准，最后方案手动一个个查的mmp

import requests
import math
import time
import random


def geocode(address):
    parameters = {'address': address, 'key': '7dac2f3552085b200731ef80e83df2d2', 'city': '北京'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['geocodes'][0]['location']


def get_distance(x1, y1, x2, y2) -> int:
    print(x1, y1, x2, y2)
    NF_pi = 0.017453292519943295
    x1 *= NF_pi
    y1 *= NF_pi
    x2 *= NF_pi
    y2 *= NF_pi
    sinx1 = math.sin(x1)
    siny1 = math.sin(y1)
    cosx1 = math.cos(x1)
    cosy1 = math.cos(y1)
    sinx2 = math.sin(x2)
    siny2 = math.sin(y2)
    cosx2 = math.cos(x2)
    cosy2 = math.cos(y2)
    v0 = cosy1 * cosx1 - cosy2 * cosx2
    v1 = cosy1 * sinx1 - cosy2 * sinx2
    v2 = siny1 - siny2
    distance = math.sqrt(v0 ** 2 + v1 ** 2 + v2 ** 2)
    print(distance)
    return int(math.asin(distance / 2) * 12742001.5798544)


def getLasted(subway_map_file, output_file, encoding='utf-8'):
    station_list = []
    with open(subway_map_file, 'r', encoding=encoding) as f:
        for line in f.readlines():
            if line.strip() != '':
                if line[0] != '&':
                    station_list.append(line.strip())

    with open(output_file, 'w', encoding=encoding) as f:
        for station in station_list:
            try:
                address = station + '地铁站'
                geo = geocode(address)
                f.write(station + ' ' + geo + '\n')
                print(station + ' ' + geo + '写入成功！')
                time.sleep(random.random())
            except Exception as e:
                print(f'FAILED: {station} with {e}')
    print('All done!')


if __name__ == '__main__':
    getLasted('../output_file/2019-6-4/subway_map.txt', 'output_file/2019-6-4/station_geo.txt')
