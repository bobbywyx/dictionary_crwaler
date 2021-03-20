# dictionary_crwaler
集数据读取，网站爬虫，数据写入于一体的学习工具

本工具集成了 https://github.com/Tony-YYC/WordRecitation

本工具主要使用dumper.py

依赖库：openpyxl  python-docx  scrapy

大致思路：

从根目录里面读取 words2.xlsx 寻找一个表格，从有#new的一行开始读取单词，读取完毕后导出一个txt给scrapy使用，爬下json格式的数据之后再通过本程序读取并在根目录输出一个demo.docx

温馨提示：爬虫部分可能需要科学上网

具体内容可以到  文档.docx  中查询