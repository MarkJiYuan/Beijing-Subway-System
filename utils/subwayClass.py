# -*- coding: utf-8 -*-
# @Author: MarkJiYuan
# @Date:   2019-05-23 10:41:45
# @Last Modified by:   MarkJiYuan
# @email: zhengjiy16@163.com
# @Last Modified time: 2019-05-31 23:56:59
# @Abstract: 地铁查询系统所需要用到的类

class Station:
    name = None
    line = None
    # platform = None
    next_station = None
    location = None

    def __init__(self, name):
        self.name = name

    def get_line(self):
        return self.line

    def add_line(self, line_name):
        if self.line == None:
            self.line = [line_name]
        else:
            self.line.append(line_name)

    def add_next_station(self, station_name, timecost=2):
        if self.next_station == None:
            self.next_station = {station_name: timecost}
        else:
            self.next_station[station_name] = timecost

    def can_go(self):
        if self.next_station != None:
            for station_name in self.next_station:
                print('可前往：' + station_name, '用时：' + str(self.next_station[station_name]))
        else:
            print('无可去车站！')

    def info(self):
        print('尊敬的旅客朋友您好！您目前位于 %s %s 站' % (self.line[0], self.name))

    def __str__(self):
        return self.name


class Path:
    line_name = ''
    location = ''

    def __init__(self, path, line_map, subway_map):
        station1 = subway_map[path[0]]
        self.location = station1
        station2 = subway_map[path[1]]
        self.path = path
        self.line_name = list(set(station1.line) & set(station2.line))[0]
        self.line_map = line_map
        self.subway_map = subway_map

    def in_line(self, station_name):
        if station_name in self.line_map[self.line_name]:
            return True
        return False

    def restart(self):
        station1 = self.subway_map[self.path[0]]
        station2 = self.subway_map[self.path[1]]
        self.line_name = list(set(station1.line) & set(station2.line))[0]
        self.location = station1

    def transfer_time(self):
        self.restart()
        count = 0
        for i in range(1, len(self.path)):
            next_station = self.subway_map[self.path[i]]
            if not self.in_line(next_station.name):
                new_line_name = list(set(self.location.line) & set(next_station.line))[0]
                self.line_name = new_line_name
                count += 1
            self.location = next_station
        return count

    def go(self):
        self.restart()
        print('您的出发地为%s的%s站' % (self.line_name, self.location.name))
        for i in range(1, len(self.path)):
            next_station = self.subway_map[self.path[i]]
            if not self.in_line(next_station.name):
                new_line_name = list(set(self.location.line) & set(next_station.line))[0]
                print('从%s换乘到%s！' % (self.line_name, new_line_name))
                self.line_name = new_line_name
            print('    %s 站 -----> %s 站' % (self.location.name, next_station.name))
            self.location = next_station
        print('您已到达位于%s的%s站！全长%s站！感谢您乘坐北京地铁，期待您的下次出行！' % (self.line_name, self.location.name, len(self.path) - 1))
