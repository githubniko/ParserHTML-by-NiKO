#!/usr/bin/python3
import requests
import json
import re
from bs4 import BeautifulSoup


html = '<html>\
	<h1 class="name" data-name="Заголовок c name">Заголовок c name</h1>\
	<h1>Заголовок</h1>\
	<h2>Заголовок 2</h2>\
	<h2>Заголовок 2_2</h2>\
	<span data-type-3="ИД3"></span>\
	<span class="price" elem="ИД">990</span>\
	<div id="product-gallery" value="1">\
		<a href="img1.jpg"></a>\
		<a href="img2.jpg"></a>\
		<a href="img3.jpg"></a>\
	</div>\
</html>'

# шаблон для парсинга
template = '\
<template>\
	<h1 class="name" data-name="$head">$name</h1>\
	<h2>$name2</h2>\
	<span elem="$id">$price</span>\
	<span data-type-3="$data"></span>\
	<div id="product-gallery" value="$value">\
		<a href="$img"></a>\
	</div>\
</template>' 

### Функция заменяет в значении $var на True
def AttrVarToTrue (list) :
	listCopy = list.copy()
	for attr in listCopy :
		if re.findall(r'\$[\w\d]+', str(listCopy[attr])) :
			listCopy[attr] = True
	return listCopy
###
### функция парсит html по шаблону template
###
def parsing(template, html) :
	dom = BeautifulSoup(html,'html.parser') # то, что нужно спарсить
	template =  BeautifulSoup(template, 'html.parser')
	result = dict()
	for value in template.find():
		if(value.name != None) :
			print(value)
			# Парсим шаблон <tag>$var</tag>
			regxRes = re.findall(r'<(.*)>.*\$([\w\d]+).*<\/.*>', str(value)) # ищим переменную
			if regxRes :
				attrTemplate = AttrVarToTrue(value.attrs) # заменяем в значении $var на True
				# Производим поиск шаблона в HTML документе
				tag = dom.find_all(value.name, attrTemplate)
				if tag :
					if(len(tag) > 1) : # если несколько объектов, то нужно их разместить в массив
						arr = []
						for parent in tag :
							arr.append(parent.text)
						result[regxRes[0][1]] = arr									
					else : # иначе просто записываем в переменную
						result[regxRes[0][1]] = tag[0].text.strip()
				
			# Парсим шаблон <tag attr="$var">text</tag>
			regxRes = re.findall(r'<.*(\$([\w\d]+)).*>.*<\/.*>', str(value)) # ищим переменную
			test = template.find(value.name, attr=re.compile(r'class'))
			print(test)
			if regxRes :
				#print(regxRes)
				# находим название нужной переменной
				for attr in value.attrs : 
					if(value.attrs.get(attr) == regxRes[0][0]) : # если найднеа
						attrTemplate = AttrVarToTrue(value.attrs) # заменяем в значении $var на True
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
				
				# смотрим есть ли дочерние объекты
				if(value.find()) : 
					res = parsing(str(value), html) # рекурсия
					result = {**result, **res} # объединяем два списка
	return result

result = parsing(template, html)
print(result)
'''
url = 'https://gremir.ru/zadvizhki/stalnye-flancevye/30s41nzh/mzta/zkl2-125/'
response = requests.get(url)
dom = BeautifulSoup(response.text, 'html.parser')

result = dict();
name = dom.find('h1')
if name != None : 
	result['name'] = name.text.strip()
	
price = dom.find('span', {'class': 'price'})
if price != None : 
	result['price'] = price.attrs.get('data-price')
	
div_img = dom.find('div', {'id': 'product-gallery'})
if div_img != None : 
	result['images'] = [];
	for value in div_img.findAll('a'):
		result['images'].append(value.attrs.get('href'))

strRes = json.dumps(result)
print(strRes)
'''
