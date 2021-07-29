# ParserHTML by NiKO
Парсер создавался для скрабинка карточек товаров с веб-сайтов.

## Например нужно спарсить карточку товара
Есть HTML веб-страница:
```html
<html>
    <head>
        <title>Title page</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1 class="name" data-name="Header">Header H1</h1>
        <h2>Header H2.1</h2>
        <h2>Header H2.2</h2>
        <span data-type="type1">Product description text</span>
        <span class="price" elem="USD">$99</span>
        <div id="product-gallery" value="1">
            <a href="img1.jpg"><img src="img1.jpg" alt="Image 1" /></a>
            <a href="img2.jpg"><img src="img2.jpg" alt="Image 2" /></a>
            <a href="img3.jpg"><img src="img3.jpg" alt="Image 3" /></a>
        </div>
    </body>
</html>
```
Задаем шаблон для парсинга:
```html
<template>
	<h1 class="name" data-name="$data-name">$Head1</h1>
	<h2>$Head2</h2>
	<span elem="$Сurrency">$Price</span>
	<span data-type="$Type">$Description</span>
	<div id="product-gallery" value="$product_gallery">
		<a href="$Img"></a>
	</div>
</template>
```
${var} -- название переменной, в которую будет занесен результат.

### Пример кода
```python
result = ParserHTML(template, html_contents)
print(result.get())
```
### Результат
---
Массив данных

```json
{'Head1': ['Header H1'], 'Head2': [['Header H2.1'], ['Header H2.2']], 'Price': ['$99'], 'Сurrency': 'USD', 'Description': ['Product description text'], 'Type': 'type1', 'product_gallery': '1', 'Img': ['img1.jpg', 'img2.jpg', 'img3.jpg']}
```