#!/usr/bin/env python

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) # иначе from classParserHTML import * не загрузится 
from classParserHTML import *

currDirname = os.path.dirname(os.path.realpath(__file__))

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

if __name__ == '__main__':
    contents = open(currDirname + '/index.html').read()
    result = ParserHTML(template, contents)
    print(result.get())


    