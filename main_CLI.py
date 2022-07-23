# -*- coding: utf-8 -*-
# @Author: MarkJiYuan
# @Date:   2019-05-23 10:39:42
# @Last Modified by:   MarkJiYuan
# @email: zhengjiy16@163.com
# @Last Modified time: 2019-05-31 23:56:47
# @Abstract: 生成station对象

# Update: 2022-7-23 10:42:06 孟骏清 GWillS@163.com (github)

from utils.subwayClass import Station, Path
import sys
import math
import time

# km/min
SUBWAY_SPEED = 0.58


class Node:
    def __init__(self, station, subway_map):
        self.station = station
        self.subway_map = subway_map
        self.parent = None
        self.basecost = 0

    def Parent(self, parent_node):
        self.parent = parent_node
        time = parent_node.station.next_station[self.station.name]
        self.basecost = self.parent.basecost + time

    def IsRoot(self):
        return self.parent == None

    def GetParent(self):
        return self.parent

    def IsStation(self, station):
        return self.station == station

    def Info(self):
        print('大家好！我目前在' + self.station.name)
        print('我来自' + self.parent.station.name)
        print('我已经经过了' + str(self.basecost) + '分钟')
        print('***********************************')

    def __str__(self):
        return self.station.name + ' ' + str(self.basecost)


class AStar:
    # km/min
    SUBWAY_SPEED = 0.58

    def __init__(self, subway_map, start_station_name, end_station_name):
        self.subway_map = subway_map
        self.start_station = self.subway_map[start_station_name]
        self.end_station = self.subway_map[end_station_name]
        start_node = Node(self.start_station, self.subway_map)
        self.open_set = [start_node]
        self.close_set = []
        self.stations_have_been = {start_node.station.name: start_node.basecost}

    def GetDistance(self, station1, station2) -> int:
        location1 = station1.location
        location2 = station2.location
        # print(x1, y1, x2, y2)
        x1, y1 = location1
        x2, y2 = location2
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
        # print(distance)
        return int(math.asin(distance / 2) * 12742001.5798544)

    def HeuristicCost(self, node) -> float:
        station_now = node.station
        distance = self.GetDistance(station_now, self.end_station)
        return distance / self.SUBWAY_SPEED / 1000

    def TotalCost(self, node) -> float:
        return node.basecost + self.HeuristicCost(node)

    def OnSameLine(self, node1, node2) -> bool:
        station1 = node2.station
        station2 = node2.parent.station
        line_name2 = list(set(station1.line) & set(station2.line))[0]

        if node1.parent != None:
            station1 = node1.station
            station2 = node1.parent.station
            line_name1 = list(set(station1.line) & set(station2.line))[0]
        else:
            line_name1 = line_name2

        return line_name1 == line_name2

    def ExpandNode(self, node) -> list:
        child_node_list = []
        for next_station_name in node.station.next_station:
            next_station = self.subway_map[next_station_name]
            child_node = Node(next_station, self.subway_map)
            child_node.Parent(node)
            if not self.OnSameLine(node, child_node):
                child_node.basecost += 8
            child_node_list.append(child_node)
        return child_node_list

    def SelectNodeInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for node in self.open_set:
            cost = self.TotalCost(node)
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index

    def TraceRoute(self, node):
        node_path = []
        while not node.IsRoot():
            node_path.insert(0, node)
            node = node.parent
        node_path.insert(0, node)

        station_name_path = []
        for node in node_path:
            station_name_path.append(node.station.name)

        return station_name_path

    def InsertNodeInOpenSet(self, node):
        this_node_cost = self.TotalCost(node)
        i = 0
        while i < len(self.open_set):
            node_in_set = self.open_set[i]
            node_in_set_cost = self.TotalCost(node_in_set)
            if this_node_cost < node_in_set_cost:
                self.open_set.insert(i, node)
                return
            i += 1
        self.open_set.append(node)

    def Run(self):
        while self.open_set != []:
            node = self.open_set[0]
            if node.IsStation(self.end_station):
                return self.TraceRoute(node)
            else:
                self.open_set.pop(0)
                self.close_set.append(node)
                new_node_list = self.ExpandNode(node)

                for new_node in new_node_list:
                    if new_node.station.name in self.stations_have_been:
                        if new_node.basecost < self.stations_have_been[new_node.station.name]:
                            self.stations_have_been[new_node.station.name] = new_node.basecost
                            self.InsertNodeInOpenSet(new_node)
                    else:
                        self.stations_have_been[new_node.station.name] = new_node.basecost
                        self.InsertNodeInOpenSet(new_node)
            # for node in self.open_set:
            # 	print(node.station.name, self.TotalCost(node))
            # print(self.stations_have_been)
            # print('*********%s个节点********' % len(self.open_set))


def ExceptionAirportLine(subway_map: dict):
    station = subway_map['2号航站楼']
    del station.next_station['3号航站楼']
    station.add_next_station('三元桥')
    subway_map['2号航站楼'] = station
    station = subway_map['3号航站楼']
    del station.next_station['三元桥']
    subway_map['3号航站楼'] = station


def CaculatePrice(distance: int):
    # 不要用！是错的。实际上的价格应该是轨道距离，而不是直线距离
    distance = math.ceil(distance / 1000)
    if distance <= 6:
        price = 3
    elif distance <= 12:
        price = 4
    elif distance <= 22:
        price = 5
    elif distance <= 32:
        price = 6
    else:
        price = 6 + math.ceil((distance - 32) / 20)
    return price


def GetPrice(start_station_name, end_station_name, price_map):
    try:
        combine = start_station_name + '-' + end_station_name
        price = price_map[combine]
        return price
    except:
        combine = end_station_name + '-' + start_station_name
        price = price_map[combine]
        return price


if __name__ == '__main__':
    # '生成Station对象'
    subway_map = {}
    with open('output_file/2019-6-4/subway_map.txt', 'r', encoding='UTF-8') as f:
        texts = f.read()
        texts = texts.split()
    line_name = ''
    length = len(texts)
    for i in range(length):
        station_name = texts[i]
        if station_name[0] == '&':
            line_name = station_name[1:]
        else:
            if station_name not in subway_map:
                station = Station(station_name)
                station.add_line(line_name)
                if i != length - 1:
                    next_station_name = texts[i + 1]
                    if next_station_name[0] != '&':
                        station.add_next_station(next_station_name)
                if i != 0:
                    next_station_name = texts[i - 1]
                    if next_station_name[0] != '&':
                        station.add_next_station(next_station_name)
                subway_map[station_name] = station
            else:
                station = subway_map[station_name]
                station.add_line(line_name)
                if i != length - 1:
                    next_station_name = texts[i + 1]
                    if next_station_name[0] != '&':
                        station.add_next_station(next_station_name)
                if i != 0:
                    next_station_name = texts[i - 1]
                    if next_station_name[0] != '&':
                        station.add_next_station(next_station_name)
                subway_map[station_name] = station

    # '机场线特殊处理'
    ExceptionAirportLine(subway_map)

    # '制作线路到站的字典'
    line_map = {}
    with open('output_file/2019-6-4/subway_map.txt', 'r') as f:
        for line in f.readlines():
            if line.strip() != '':
                if line[0] == '&':
                    line_name = line.strip()[1:]
                    line_map[line_name] = []
                else:
                    station_name = line.strip()
                    line_map[line_name].append(station_name)

    #'为station增加地理位置'
    with open('output_file/2019-6-4/station_geo.txt', 'r') as f:
        for line in f.readlines():
            s = line.split()
            station_name = s[0]
            location = s[1].split(',')
            location = (float(location[0]), float(location[1]))
            subway_map[station_name].location = location

    # '为station的nextstation增加timecost值'
    with open('output_file/2019-6-4/timecost_list.txt', 'r') as f:
        for line in f.readlines():
            message = line.strip().split()
            start = message[0]
            end = message[1]
            timeused = message[2]
            subway_map[start].next_station[end] = int(timeused)

    # '加载票价'
    price_map = {}
    with open('output_file/2019-6-4/price.txt', 'r') as f:
        for line in f.readlines():
            s = line.split()
            start_station_name = s[0]
            end_station_name = s[1]
            combine = start_station_name + '-' + end_station_name
            price = s[2]
            price_map[combine] = price

    # '测试'
    # while True:
    # 	command = input('您在哪一站？')
    # 	if command == 'quit':
    # 		sys.exit()
    # 	station = subway_map[command]
    # 	station.can_go()

    start = time.time()
    start_station_name = input("请输入出发站：")
    end_station_name = input("请输入目的地站：")
    a = AStar(subway_map, start_station_name, end_station_name)
    path = a.Run()
    p = Path(path, line_map, subway_map)
    p.go()
    end = time.time()
    price = GetPrice(start_station_name, end_station_name, price_map)
    print('票价为：' + str(price))
# print('程序用时：', (end - start), '秒')
