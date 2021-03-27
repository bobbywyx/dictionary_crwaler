import re

import scrapy

# by Peyman (mohsenikiasari@ce.sharif.edu) in 2019.

import os
os.environ["http_proxy"] = "http://127.0.0.1:11000"
os.environ["https_proxy"] = "http://127.0.0.1:11000"
#set proxy

working_dir = os.getcwd()
words = []

#读取dump.txt

def read(file_path):
    lines = 0
    string = ''
    output = []
    with open(file_path,encoding='UTF-8') as file:
        contents=file.read()
    # print(contents)
    if not contents == '':
        for i in contents:
            print(i,end='')
            if i == '\n':
                lines+=1
                output.append(string)
                string = ''
            else:
                string += i
    else:
        lines=0

    return output


# words = ['I', 'hope', 'you', 'like', 'this', 'dictionary', 'web', 'crawler']
words = read(working_dir+'/dump.txt')
#print(words)

#  scrapy crawl oxford -o oxford.jl
class OxfordCrawler(scrapy.Spider):
    name = "oxford"
    allowed_domains = ["www.lexico.com"]
    start_urls = ["https://www.lexico.com/en/definition/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = {}

        for sections in response.xpath("//section[@class='gramb']"):
            try:
                part_of_speech = sections.xpath(".//span[@class='pos']/text()").extract()[0]
            except:
                part_of_speech = False
            def_list = sections.xpath("./ul/li/div[@class='trg']//span[@class='ind']").extract()
            if not def_list:
                def_list = sections.xpath(".//div[@class='empty_sense']//div[@class='crossReference']").extract()

            def_list = [re.sub(r'<.*?>', "", i).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            if def_list and part_of_speech:
                if part_of_speech in definition_dict:
                    definition_dict[part_of_speech] += def_list
                else:
                    definition_dict[part_of_speech] = def_list

        if definition_dict:
            yield {word: definition_dict}
        
        return definition_dict


#  scrapy crawl longman -o longman.jl
class LongmanCrawler(scrapy.Spider):
    name = "longman"
    allowed_domains = ["https://www.ldoceonline.com"]
    start_urls = ["https://www.ldoceonline.com/dictionary/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = {}

        for sections in response.xpath("//span[@class='dictentry']"):
            try:
                part_of_speech = (sections.xpath(".//span[@class='POS']/text()").extract()[0]).strip()
            except:
                part_of_speech = False

            try:
                gram_list1 = sections.xpath(".//span[@class='Sense']/span[@class='GRAM']").extract()
            except:
                gram_list1 = []
            gram_list = []
            for i in gram_list1:
                try:
                    gram_item = re.search(r'</span>([^\/]*)<span\s+class="neutral span">',i).group(0)
                    gram_item = gram_item.replace("</span>","")
                    gram_item = gram_item.replace("<span class=\"neutral span\">","")
                    gram_list.append(gram_item)
                except:
                    pass
            gram_list = [i for i in gram_list if i]

            try:
                gram_header = (sections.xpath(".//span[@class='GRAM']/text()").extract()[0]).strip()
            except:
                gram_header = ""
            
            try:
                gram_header += " " + (sections.xpath(".//span[@class='POS']/text()").extract()[0]).strip()
            except:
                pass
        
            def_list = sections.xpath(".//span[@class='Sense']/span[@class='DEF']").extract()
            def_list = [re.sub(r'<.*?>', "", i[18:-7]).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            try:
                def_header = (sections.xpath(".//span[@class='GRAM']/text()").extract()[0]).strip()
            except:
                def_header = ""

            print(len(def_list))
            if len(def_list) is 1:
                def_list.append(def_header)

            defgram_list = []
            for i in range(0,len(def_list) - 1):
                try:
                    gram_item2 = gram_list[i]
                except:
                    gram_item2 = gram_header
                defgram_list.append("**" + gram_item2 + "**   " + def_list[i])
            try:
                if defgram_list and part_of_speech:
                    if part_of_speech in definition_dict:
                        definition_dict[part_of_speech] += defgram_list
                    else:
                        definition_dict[part_of_speech] = defgram_list
            except:
                if def_list and part_of_speech:
                    if part_of_speech in definition_dict:
                        definition_dict[part_of_speech] += def_list
                    else:
                        definition_dict[part_of_speech] = def_list
        
            collo_list = sections.xpath(".//span[@class='Sense']/span[@class='ColloExa']/span[@class='COLLO']").extract()
            collo_list = [re.sub(r'<.*?>', "", i[20:-7]).strip() for i in collo_list]
            collo_list = [ i  for i in collo_list if i]

            if collo_list and "Usage-" + part_of_speech:
                if "Usage-" + part_of_speech in definition_dict:
                    definition_dict["Usage-" + part_of_speech] += collo_list
                else:
                    definition_dict["Usage-" + part_of_speech] = collo_list

            gramexa_list = sections.xpath(".//span[@class='Sense']/span[@class='GramExa']/span[@class='PROPFORMPREP']").extract()
            gramexa_list = [re.sub(r'<.*?>', "", i[26:-7]).strip() for i in gramexa_list]
            gramexa_list = [i  for i in gramexa_list if i]

            if gramexa_list and "Usage-" + part_of_speech:
                if "Usage-" + part_of_speech in definition_dict:
                    definition_dict["Usage-" + part_of_speech] += gramexa_list
                else:
                    definition_dict["Usage-" + part_of_speech] = gramexa_list

        if definition_dict:
            yield {word: definition_dict}


#  scrapy crawl cambridge -o cambridge.jl
class CambridgeCrawler(scrapy.Spider):
    name = "cambridge"
    allowed_domains = ["https://dictionary.cambridge.org"]
    start_urls = ["https://dictionary.cambridge.org/dictionary/english/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = {}

        for enrty in response.xpath("//div[@class='entry-body__el clrd js-share-holder']"):
            part_of_speeches = enrty.xpath("./div[@class='pos-header']//span[@class='pos']/text()").extract()
            def_list = enrty.xpath(
                ".//div[@class='sense-body']/div[@class='def-block pad-indent']//b[@class='def']").extract()
            def_list = [re.sub(r'<.*?>|:', "", i[15:-4]).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            if def_list and part_of_speech:
                for part_of_speech in part_of_speeches:
                    if part_of_speech in definition_dict:
                        definition_dict[part_of_speech] += def_list
                    else:
                        definition_dict[part_of_speech] = def_list

        if definition_dict:
            yield {word: definition_dict}


#  scrapy crawl webster -o webster.jl
class WebsterCrawler(scrapy.Spider):
    name = "webster"
    allowed_domains = ["https://www.merriam-webster.com"]
    start_urls = ["https://www.merriam-webster.com/dictionary/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = {}

        part_of_speeches = [re.sub(r'\(.*\)', "", i).strip() for i in
                            response.xpath("//span[@class='fl']/a/text()|//span[@class='fl']/text()").extract()]

        for sections in response.xpath("//div[contains(@id, 'dictionary-entry')]/div[@class='vg']"):
            part_of_speech = part_of_speeches.pop(0)
            def_list = sections.xpath(
                ".//span[@class='dtText' or @class='unText'][not(ancestor::span[@class='dtText'])]").extract()
            def_list = [re.sub(r'<span.*>.+</span>', "", i[21:-7]) for i in def_list]
            def_list = [re.sub(r'<.*?>|:', "", i).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            if def_list and part_of_speech:
                if part_of_speech in definition_dict:
                    definition_dict[part_of_speech] += def_list
                else:
                    definition_dict[part_of_speech] = def_list

        if definition_dict:
            yield {word: definition_dict}


#  scrapy crawl collins -o collins.jl
class CollinsCrawler(scrapy.Spider):
    name = "collins"
    allowed_domains = ["https://www.collinsdictionary.com"]
    start_urls = ["https://www.collinsdictionary.com/dictionary/english/" + word for word in words]

    def parse(self, response):
        word = response.request.url.split("/")[-1]
        definition_dict = {}

        for sections in response.xpath("//div[@class='dictionary Cob_Adv_Brit']"
                                       "//div[@class='content definitions cobuild br']/div[@class='hom']"):
            try:
                part_of_speech = (sections.xpath(".//span[@class='pos']/text()").extract()[0]).strip()
            except:
                part_of_speech = False
            def_list = sections.xpath("./div[@class='sense']/div[@class='def']").extract()
            def_list = [re.sub(r'<.*?>', "", i[17:-6]).strip() for i in def_list]
            def_list = [i for i in def_list if i]

            if def_list and part_of_speech:
                if part_of_speech in definition_dict:
                    definition_dict[part_of_speech] += def_list
                else:
                    definition_dict[part_of_speech] = def_list

        if definition_dict:
            yield {word: definition_dict}
