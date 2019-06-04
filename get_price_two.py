# -*- coding: utf-8 -*-
# @Author: MarkJiYuan
# @Date:   2019-05-29 15:24:26
# @Last Modified by:   MarkJiYuan
# @email: zhengjiy16@163.com
# @Last Modified time: 2019-05-30 13:04:52
# @Abstract: 北京地铁官方的api有些操作，直接用requests访问不了，所以还是用selenium一点点模拟吧, 发现也会限流，我很烦

from urllib import parse
from selenium import webdriver
import requests
import time
import json
import random

def openChrome():
	option = webdriver.ChromeOptions()
	option.add_argument('disable-infobars')

	driver = webdriver.Chrome(chrome_options=option)
	return driver

if __name__ == '__main__':
	driver = openChrome()

	station_name_list = []
	with open('subway_map.txt', 'r') as f:
		for line in f.readlines():
			if line.strip() != '':
				if line[0] != '&':
					station_name = line.strip()
					if station_name not in station_name_list:
						station_name_list.append(station_name)

	length = len(station_name_list)
	failed_list = []
	i = 0
	while i < length:
		j = i + 1
		while j < length:
			try:
				start_station = station_name_list[i]
				end_station = station_name_list[j]
				start_station_url = parse.quote(start_station)
				end_station_url = parse.quote(end_station)

				url = 'https://map.bjsubway.com/api/searchstartend?start=' + start_station_url + '&end=' + end_station_url
				driver.get(url)
				body = driver.find_element_by_xpath('//pre').text
				dic = json.loads(body)
				price = dic['price']
				with open('price.txt', 'a') as f:
					f.write(start_station + ' ' + end_station + ' ' + str(price) + ' ' + str(i) + ' ' + str(j) + '\n' )
				print(start_station + ' ' + end_station + ' ' + str(price) + ' ' + str(i) + ' ' + str(j))
				
				time.sleep(1 + random.random())
			except:
				print('失败！', start_station, end_station)
				failed_list.append(start_station + ':' + end_station)
			j += 1
		i += 1

	while failed_list != []:
		new_failed_list = []
		for i in range(len(failed_list)):
			search_record = failed_list[i].split(':')
			start_station = search_record[0]
			end_station = search_record[1]
			start_station_url = parse.quote(start_station)
			end_station_url = parse.quote(end_station)
			url = 'https://map.bjsubway.com/api/searchstartend?start=' + start_station_url + '&end=' + end_station_url
			try:
				driver.get(url)
				body = driver.find_element_by_xpath('//pre').text
				dic = json.loads(body)
				price = dic['price']
				with open('price.txt', 'a') as f:
					f.write(start_station + ' ' + end_station + ' ' + str(price) + '\n' )
				time.sleep(1 + random.random())
			except:
				new_failed_list.append(start_station + ':' + end_station)
		failed_list = new_failed_list

	command = input('已全部完成！')
	if command == 'quit':
		driver.quit()







