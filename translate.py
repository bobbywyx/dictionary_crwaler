import urllib.request
import json
import urllib.parse
import time
import requests
import re

class translate:
    def __init__(self,word = ''):
        self.word = word

    def getword(self,word):
        self.word = word

    def fetch(self,query_str):
        query = {'q': "".join(query_str)}   # list --> str: "".join(list)
        url = 'https://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&' + urllib.parse.urlencode(query)
        response = urllib.request.urlopen(url, timeout=3)
        html = response.read().decode('utf-8')
        return html
    
    def parse(self,html):
        d = json.loads(html)
        try:
            if d.get('errorCode') == 0:
                explains = d.get('basic').get('explains')
                result = str(explains).replace('\'', "").replace('[', "").replace(']', "")  #.replace真好用~
                return result
            else:
                print('无法翻译!****')
                return ""       #若无法翻译，则空出来
        except:
            return ""      #若无法翻译，则空出来
    def translation(self):
        chinese = self.parse(self.fetch(self.word))
        return chinese
    def translateSep(self):
        string = self.translation().split(",")
        return string

class dictionary:
    def __init__(self,word = ''):
        self.word = word
        word=word.replace(" ","_")
        proxies = {'http': 'http://127.0.0.1:11000', 'https': 'http://127.0.0.1:11000'}
        #url的格式有规律
        request=requests.get(url="https://www.lexico.com/definition/"+word , proxies = proxies)
        #print(request)
        self.html=request.text
        print(self.html)

    def getItem(self, regularExpression):
        matchItem=re.search(regularExpression,self.html)
        if matchItem:
            if matchItem.group(1):
                Item = matchItem.group(1)
                print("\nphoneticSpelling: ",word,"--->", Item)
                return Item
            else:
                print("\nword \""+word+"\" has no phonetic spelling in the dictionary")
        else:
            print("\nword \""+word+"\" has no phonetic spelling in the dictionary")
            return "NONE"

    def meaning(self):
        meaningExpression=r'<span\s+class="ind">/([^\/]*)/</span>'
        matchMeaning = self.getItem(meaningExpression)
        return matchMeaning
    def spelling(self):
        spellingExpression=r'<span\s+class="phoneticspelling">/([^\/]*)/</span>'
        matchSpelling = self.getItem(spellingExpression)
        return matchSpelling
    def examples(self):
        exampleExpression=r'<span\s+class="ind">/([^\/]*)/</span>'
        matchExample = self.getItem(exampleExpression)
        return matchExample
    def getAll(self):
        return [self.meaning(),self.spelling(),self.examples()]


if __name__ == '__main__':
    word = input("test mode , input a word to find traslation and meaning")
    tran = translate(word)
    print(tran.translation())
    print(tran.translateSep())
   # translation returns a word while translateSep returns a list
    dict = dictionary(word)
    print(dict.getAll())