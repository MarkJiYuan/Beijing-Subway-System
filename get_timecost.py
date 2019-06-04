# -*- coding: utf-8 -*-
# @Author: MarkJiYuan
# @Date:   2019-05-28 21:13:47
# @Last Modified by:   MarkJiYuan
# @email: zhengjiy16@163.com
# @Last Modified time: 2019-05-29 14:06:30
# @Abstract: 
import json

def get_time_cost(f):
	for id in range(0, 20):
		line_name = response.xpath('//div[@id="sub' + str(id) + '"]/div/table/thead/tr[1]/td/text()').extract()[0]
		f.write('&' + line_name + '\n')
		for i in range(0, 5):
			xpath_route = '//div[@id="sub' + str(id) + '"]/div/table/tbody/tr/td[' + str(i) + ']/text()'
			l = response.xpath(xpath_route).extract()
			strip = lambda i:i.strip()
			l = list(map(strip, l))
			f.write(json.dumps(l))
			f.write('\n')

def time_minus(time1:str, time2:str) -> int:
	time1 = time1.split(':')
	time2 = time2.split(':')

	hour1 = int(time1[0])
	hour2 = int(time2[0])
	minute1 = int(time1[1])
	minute2 = int(time2[1])

	dif = (hour1 * 60 + minute1) - (hour2 * 60 + minute2)
	dif = abs(dif)

	return dif

def calculate_time_cost(l:list) -> list:
	timecost = []
	for i in range(len(l)-1):
		dif = time_minus(l[i], l[i+1])
		timecost.append(dif)
	return timecost

def timecost_exception(dic):
	dic['2号线'][0] = 2
	dic['2号线'][9] = 2
	dic['4号线/大兴线'][10] = 2
	dic['4号线/大兴线'][9] = 3
	dic['4号线/大兴线'].reverse()
	dic['6号线'][5] = 3
	dic['6号线'][24] = 2
	dic['8号线（北段）'][2] = 3
	dic['10号线'][25] = 2
	dic['10号线'][41] = 3
	dic['13号线'][8] = 4
	dic['15号线'][7] = 3
	dic['昌平线'][9] = 2

if __name__=='__main__':
	line_map = {}
	timecost = {}
	'读入线站表，顺序与首末班对应'
	with open('subway_map.txt', 'r') as f:
		for line in f.readlines():
			if line.strip() != '':
				if line[0] == '&':
					line_name = line.strip()[1:]
					line_map[line_name] = []
				else:
					station_name = line.strip()
					line_map[line_name].append(station_name)

	'读入首班车时间表'
	with open('timecost.txt', 'r') as f:
		for line in f.readlines():
			if line[0] == '&':
				line_name = line.strip()[1:]
			else:
				timecost[line_name] = json.loads(line.strip())

	'根据首班车时间表计算站间时长'
	for line_name in timecost:
		time_list = timecost[line_name]
		a = calculate_time_cost(time_list)
		timecost[line_name] = a

	'处理异常'
	timecost_exception(timecost)
	
	'将时间表与线站表相结合，生成乘车用时文件，机场线特殊情况直接手动处理了'
	with open('timecost_list.txt', 'w') as f:
		for line_name in line_map:
			stations = line_map[line_name]
			for i in range(len(stations)-1):
				start = stations[i]
				end = stations[i+1]
				time = timecost[line_name][i]
				f.write(start + ' ' + end + ' ' + str(time) + '\n')
				f.write(end + ' ' + start + ' ' + str(time) + '\n')

	print('done!')















