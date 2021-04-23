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
        WordList = []

        for sections in response.xpath("//span[@class='dictentry']"):
            #part of speech setion
            try:
                part_of_speech = (sections.xpath(".//span[@class='POS']/text()").extract()[0]).strip()
            except:
                part_of_speech = ""

            #grammar section
            try:
                gram_header = (sections.xpath(".//span[@class='GRAM']/text()").extract()[0]).strip()
            except:
                gram_header = ""
            
            try:
                gram_header += " " + (sections.xpath(".//span[@class='POS']/text()").extract()[0]).strip()
            except:
                pass

            print(part_of_speech,gram_header)
            #print(len(def_list))
            #if len(def_list) is 1:
            #    def_list.append(def_header)

            for sections in response.xpath(".//span[@class='Sense']"):
                senseSUM = []
                try:
                    gram_list = sections.xpath(".//span[@class='GRAM']").extract()
                except:
                    gram_list = []
                
                gram_list1 = []

                for i in gram_list:
                    try:
                        gram_item = re.search(r'</span>([^\/]*)<span\s+class="neutral span">',i).group(0)
                        gram_item = gram_item.replace("</span>","")
                        gram_item = gram_item.replace("<span class=\"neutral span\">","")
                        gram_list1.append(gram_item)
                    except:
                        pass

                def_list = sections.xpath(".//span[@class='DEF']").extract()
                def_list = [re.sub(r'<.*?>', "", i[18:-7]).strip() for i in def_list]
                def_list = [i for i in def_list if i]

                def_list = sections.xpath(".//span[@class='DEF']").extract()
                def_list = [re.sub(r'<.*?>', "", i[18:-7]).strip() for i in def_list]
                def_list = [i for i in def_list if i]

                collo_list = sections.xpath(".//span[@class='ColloExa']/span[@class='COLLO']").extract()
                collo_list = [re.sub(r'<.*?>', "", i[20:-7]).strip() for i in collo_list]
                collo_list = [ i  for i in collo_list if i]

                gramexa_list1 = sections.xpath(".//span[@class='GramExa']/span[@class='PROPFORMPREP']").extract()
                gramexa_list1 = [re.sub(r'<.*?>', "", i[26:-7]).strip() for i in gramexa_list1]
                gramexa_list1 = [i for i in gramexa_list1 if i]

                gramexa_list2 = sections.xpath(".//span[@class='GramExa']/span[@class='PROPFORM']").extract()
                gramexa_list2 = [re.sub(r'<.*?>', "", i[22:-7]).strip() for i in gramexa_list2]
                gramexa_list2 = [i for i in gramexa_list2 if i]

                #processing after filtering
                gramexa_list = gramexa_list1 + gramexa_list2
                if len(gram_list1) >= 1:
                    gram_list1 = [i + " " + part_of_speech for i in gram_list1]
                elif len(gram_header) >= 1:
                    gram_list1 = [gram_header]
                #print(gram_list1,part_of_speech,def_list,collo_list,gramexa_list,gramexa_list2)
                if len(def_list) >= 1:
                    senseSUM = [gram_list1,def_list,collo_list,gramexa_list]
                    #print(senseSUM)
                    WordList.append(senseSUM)
            
            for sections in response.xpath(".//span[@class='Sense']/span[@class='Subsense']"):
                senseSUM = []
                try:
                    gram_list = sections.xpath(".//span[@class='GRAM']").extract()
                except:
                    gram_list = []
                
                gram_list1 = []

                for i in gram_list:
                    try:
                        gram_item = re.search(r'</span>([^\/]*)<span\s+class="neutral span">',i).group(0)
                        gram_item = gram_item.replace("</span>","")
                        gram_item = gram_item.replace("<span class=\"neutral span\">","")
                        gram_list1.append(gram_item)
                    except:
                        pass

                def_list = sections.xpath(".//span[@class='DEF']").extract()
                def_list = [re.sub(r'<.*?>', "", i[18:-7]).strip() for i in def_list]
                def_list = [i for i in def_list if i]

                def_list = sections.xpath(".//span[@class='DEF']").extract()
                def_list = [re.sub(r'<.*?>', "", i[18:-7]).strip() for i in def_list]
                def_list = [i for i in def_list if i]

                collo_list = sections.xpath(".//span[@class='ColloExa']/span[@class='COLLO']").extract()
                collo_list = [re.sub(r'<.*?>', "", i[20:-7]).strip() for i in collo_list]
                collo_list = [ i  for i in collo_list if i]

                gramexa_list1 = sections.xpath(".//span[@class='GramExa']/span[@class='PROPFORMPREP']").extract()
                gramexa_list1 = [re.sub(r'<.*?>', "", i[26:-7]).strip() for i in gramexa_list1]
                gramexa_list1 = [i for i in gramexa_list1 if i]

                gramexa_list2 = sections.xpath(".//span[@class='GramExa']/span[@class='PROPFORM']").extract()
                gramexa_list2 = [re.sub(r'<.*?>', "", i[22:-7]).strip() for i in gramexa_list2]
                gramexa_list2 = [i for i in gramexa_list2 if i]

                #processing after filtering
                gramexa_list = gramexa_list1 + gramexa_list2
                if len(gram_list1) >= 1:
                    gram_list1 = [i + " " + part_of_speech for i in gram_list1]
                elif len(gram_header) >= 1:
                    gram_list1 = [gram_header]
                #print(gram_list1,part_of_speech,def_list,collo_list,gramexa_list,gramexa_list2)
                if len(def_list) >= 1:
                    senseSUM = [gram_list1,def_list,collo_list,gramexa_list]
                    #print(senseSUM)
                    WordList.append(senseSUM)
        print(WordList)
        yield {word : WordList}