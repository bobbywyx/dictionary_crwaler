import os
import json
from openpyxl import load_workbook
from docx import Document
from docx.shared import Inches
from docx.shared import Pt

working_dir = os.getcwd()
output_txt = ''

# 读取数据  从words2.xlsx读取并且输出一个txt文件直接喂给crawler

forms = load_workbook("words2.xlsx")

sheetlist = []
t = 0
for sheets in forms:
    t += 1
    sheetlist.append(sheets)
    print(t, ">", sheets)

'''
def newwordtranslater(sheet,word,row,meaningcolume):
    trans.getword(word)
    meaning_list = trans.translateSep()
    times = 0
    if meaning_list == None:
        print(word,"没有")
    for i in meaning_list:
        if not "人名" in i:
            print(word,i)
            sheet[meaningcolume+str(row)].value = i
            row+=1
            times+=1
            if times == len(meaning_list):
                row-=1
            else:
                sheet.insert_rows(row)
        else:
            sheet.delete_rows(row)
            row-=1
    return row
'''


def indexer(she):
    global output_txt
    rowdelete = 1
    sheet = sheetlist[she - 1]
    row = 2
    word_colume = 'A'
    meanings_colume = 'B'

    newstate = False
    while True:
        value_word = sheet[word_colume + str(row)].value  # 获取单词/词组本身 以获得翻译
        if newstate == True and value_word:
            output_txt += value_word + '\n'
            # row = newwordtranslater(sheet,value_word,row,meanings_colume)  #本来这里用来自动换行  现在不需要了，直接导出txt
        elif newstate and not value_word:
            break
        if value_word == None and newstate == False:
            pass
        elif value_word[0] == '#':
            if value_word == "#new":
                rowdelete = row
                newstate = True
        elif newstate == False:
            pass
        row += 1

    output_txt += '\n'  # 最后来一个回车以防bug
    sheet.delete_rows(rowdelete)


i = input("请输入要翻译的表格序号:")
indexer(int(i))


# 读取并选择表格内第几个

def txtwriter(f_path, txt, aorw='w'):
    # f_path = r'E:\haha\readme.txt'
    if aorw == 'w':  # 创建新文件并覆盖之前的
        with open(f_path, 'w', encoding='UTF-8') as f:
            f.write(txt)
    if aorw == 'a':
        with open(f_path, 'a', encoding='UTF-8') as f:
            f.write('\n' + txt)


txtwriter(working_dir + '/dictionary_crawler/dictionary_crawler/spiders/dump.txt', output_txt)
# 写入文件

#cmd = '/dictionary_crawler/dictionary_crawler/spiders/run.bat'

# print(os.system(working_dir+cmd))
# 执行scrapy
print('爬虫执行完毕 可以导入')
# forms.save("words2.xlsx")