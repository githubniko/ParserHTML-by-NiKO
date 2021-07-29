#!/usr/bin/env python

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) # иначе from classParserHTML import * не загрузится 
from classParserHTML import *

currDirname = os.path.dirname(os.path.realpath(__file__))

# шаблон для парсинга
template = '\
<template>\
	<h1 class="name" data-name="$data-name">$Head1</h1>\
	<h2>$Head2</h2>\
	<span elem="$Сurrency">$Price</span>\
	<span data-type="$Type">$Description</span>\
	<div id="product-gallery" value="$product_gallery">\
		<a href="$Img"></a>\
	</div>\
</template>' 

if __name__ == '__main__':
    contents = open(currDirname + '/index.html').read()
    result = ParserHTML(template, contents)
    print(result.get())


    