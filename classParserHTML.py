#!/usr/bin/env python
import requests, json, re
from bs4 import BeautifulSoup

class ParserHTML(object):
	def __init__(self, template, html):
		self.template = template
		self.html = html
		self.result = self.parsing(self.template, self.html)

	### Получить массив с результатом
	def get(self):
		return self.result

	### Функция заменяет в значении $var на True
	def AttrVarToTrue(self, list) :
		listCopy = list.copy()
		for attr in listCopy :
			if re.findall(r'\$[\w\d]+', str(listCopy[attr])) :
				listCopy[attr] = True
		return listCopy

	### Функция парсит html по шаблону template
	def parsing(self, template, html) :
		dom = BeautifulSoup(html,'html.parser') # то, что нужно спарсить
		template =  BeautifulSoup(template, 'html.parser')
		result = dict()
		for value in template.find(): 
			if(value.name != None) :
				# print(value)
				# Парсим шаблон <tag>$var</tag>

				# Смотрим есть ли дочерние объекты
				child = value.find()
				if(child) : 
					# находим объект в дереве и передаем его в рексию
					attrTemplate = self.AttrVarToTrue(value.attrs) # заменяем в значении $var на True
					tag = dom.find_all(value.name, attrTemplate)
					if tag :
						if(len(tag) > 1) : # если несколько объектов, то нужно их разместить в массив
							arr = []
							for elemTag in tag:
								res = self.parsing(str(value), r''.join(map(str,elemTag.contents))) # рекурсия
								_result = {**result, **res} # объединяем два списка
								arr.append(_result)
							result = arr
						else : # иначе просто записываем в переменную
							res = self.parsing(str(value), r''.join(map(str,tag[0].contents))) # рекурсия
							result = {**result, **res} # объединяем два списка
							# return _result

					# return _result
				else :
					regxRes = re.findall(r'<(.*)>\$([\w\d]+)<\/.*>$', str(value)) # ищим переменную
					if regxRes :
						#print(regxRes)
						attrTemplate = self.AttrVarToTrue(value.attrs) # заменяем в значении $var на True
						# Производим поиск шаблона в HTML документе
						tag = dom.find_all(value.name, attrTemplate)
						if tag :
							if(len(tag) > 1) : # если несколько объектов, то нужно их разместить в массив
								arr = []
								for parent in tag :
									arr.append(re.sub(r'^\s+|\n|\r|\s+$', '', r''.join(map(str,parent.contents))))
								result[regxRes[0][1]] = arr
							else : # иначе просто записываем в переменную
								result[regxRes[0][1]] = re.sub(r'^\s+|\n|\r|\s+$', '', r''.join(map(str,tag[0].contents)))
						
				# Парсим шаблон <tag attr="$var">text</tag>
				clearValue = re.sub(r'>.*<', r'><', str(value)) # убераем внутннее содержимое
				regxRes = re.findall(r'<.*(\$([\w\d]+)).*><\/.*>', clearValue) # ищим переменную
				# print(regxRes)
				if regxRes :
					#print(regxRes)
					# находим название нужной переменной
					for attr in value.attrs : 
						if(value.attrs.get(attr) == regxRes[0][0]) : # если найднеа
							attrTemplate = self.AttrVarToTrue(value.attrs) # заменяем в значении $var на True
							tag = dom.find_all(value.name, attrTemplate) # ищим атрибут в html, где value.name тег в котором ищится атрибут
							if (tag) :
								if(len(tag) > 1) : # если несколько объектов, то нужно их разместить в массив
									arr = []
									for parent in tag :
										_attr = parent.attrs.get(attr)
										arr.append(_attr)
									result[regxRes[0][1]] = arr									
								else : # иначе просто записываем в переменную
									result[regxRes[0][1]] = tag[0].attrs.get(attr)
							else :
								result[regxRes[0][1]] = None # если значение или тэг не найдены, то выводим None
				

		return result

### Example
#########################################

if __name__ == '__main__':
	# шаблон для парсинга
	template = '\
	<template>\
		<h1>$head</h1>\
		<p>$text</p>\
		<p><a href="$link"></a></p>\
	</template>' 
	

	url = 'https://example.com/'
	HTML = requests.get(url).text

	result = ParserHTML(template, HTML)
	print(result.get())

