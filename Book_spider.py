import os
import requests
from bs4 import BeautifulSoup
class Spider:
    #属性
    prefix_url='https://www.xbiquge.so/book/6281/'
    suffix_url='.html'
    first_page=4072981
    current_page=4072981
    last_page=4076212
    book_name="吞噬星空"
    chapter_id=1

    #构造函数
    def __init__(self,first_page,last_page,book_name):
        self.first_page=first_page
        self.last_page=last_page
        self.book_name=book_name
        self.current_page=first_page
        self.chapter_id=1
    #主函数
    def main(self):
        self.__make_dir()
        while self.current_page<=self.last_page:
            #拼接url
            url=self.prefix_url+str(self.current_page)+self.suffix_url
            self.current_page+=1
            html=self.__request_website(url)
            chapter=self.__parse_result(html)
            if chapter==None:
                continue
            else:
                self.__write_chapter_to_file(chapter)
                self.chapter_id+=1

    #创建图书文件夹
    def __make_dir(self):
        os.mkdir(self.book_name)

    #请求网页源码
    def __request_website(self,url):
        try:
            response =requests.get(url)
            if response.status_code==200:
                return response.text
        except requests.RequestException:
            return None

    #解析网页源码
    def __parse_result(self,html):
        soup=BeautifulSoup(html,'lxml')
        chapter_title=soup.title.string
        if soup.find(id="content")==None:
            return None
        else:
            chapter_content=soup.find(id="content").get_text()
        return {
            'title':chapter_title,
            'content':chapter_content
        }
    #将文本写入文件
    def __write_chapter_to_file(self,chapter):
        print('writing chapter {}...'.format(self.chapter_id))
        with open(self.book_name+'/'+str(self.chapter_id),'a',encoding='UTF-8') as file:
            file.write(chapter['title']+'\n')
            file.write(chapter['content'])
            file.close()

if __name__ == '__main__':
    TuShiXingKong_spider=Spider(4072981,4076212,'吞噬星空')
    TuShiXingKong_spider.main()
