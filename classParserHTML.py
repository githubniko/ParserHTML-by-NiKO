#!/usr/bin/env python
import requests, json, re
from bs4 import BeautifulSoup

class ParserHTML(object):
	def __init__(self, template, html):
		self.template = template
		self.html = html

		dom = BeautifulSoup(html,'html.parser') # то, что нужно спарсить
		template =  BeautifulSoup(self.template, 'html.parser')
		self.result = self.parsing(template.template, dom)

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
	def parsing(self, template, dom) :
		result = dict()

		for value in template.children: # !!!! тут нужен перебор на одном уровнне

			if(value.name != None) :
				# print(value)
				# Парсим шаблон <tag>$var</tag>

				# Смотрим есть ли дочерние объекты
				child = value.find()
				if(child) : 
					# находим объект в дереве и передаем его в рексию
					group = None
					nogroup = None
					if(value.attrs.get('group')): # если указан атрибут для группировки
						group = value.attrs.get('group')
						del value.attrs['group']

					if(value.attrs.get('nogroup')==''): # посик флага "не группировать"
						nogroup = True

					attrTemplate = self.AttrVarToTrue(value.attrs) # заменяем в значении $var на True
					tag = dom.find_all(value.name, attrTemplate)
					if tag :
						if(len(tag) > 1) : # если несколько объектов, то нужно их разместить в массив
							arr = []	
							if not group: # если атрибут для группировки не указан, то берем тег группы
								group = value.name					
							for elemTag in tag:
								res = self.parsing(value, elemTag) # рекурсия
								#_result = {**result, **res} # объединяем два списка
								arr.append(res)
							if(len(arr) > 1): # если найдено несколько блоков
								if nogroup : # если установлен флаг "не группировать", то записываем только первый результат
									result = {**result, **arr[0]}
								else:
									result[group] = arr # сохраняем первый найденый блок 
							else:  
								result = {**result, **arr}
						else : # иначе просто записываем в переменную
							res = self.parsing(value, tag[0]) # рекурсия
							result = {**result, **res} if len(result) else res # объединяем два списка
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
									arr.append(re.sub(r'^\s+|\n|\r|\s+$', '', r''.join(map(str,parent.next))))
								result[regxRes[0][1]] = arr
							else : # иначе просто записываем в переменную
								result[regxRes[0][1]] = re.sub(r'^\s+|\n|\r|\s+$', '', r''.join(map(str,tag[0].next)))
						
				# Парсим шаблон <tag attr="$var">text</tag>
				clearValue = re.sub(r'>.*<.*>', r'/>', str(value)) # убераем внутннее содержимое
				regxRes = re.findall(r'<.*(\$([\w\d]+)).*/>', clearValue) # ищим переменную
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
	template = '<template>\
		<h1>$head</h1>\
		<p><a href="$link"></a></p>\
		</template>\
' 
	# 
	# <p>$text</p>\

	url = 'https://example.com/'
	HTML = requests.get(url).text

	result = ParserHTML(template, HTML)
	print(result.get())

