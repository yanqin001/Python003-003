import scrapy
from task2.items  import Task2Item
from scrapy.selector import  Selector

class MydySpider(scrapy.Spider):
    name = 'mydy'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        i = 1
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        for movie in movies:
            if i > 1:
                break
            i += 1
            title = movie.xpath('./a/text()')
            print(title.extract())
            myid = movie.xpath('./a/@href')
            url2 = 'https://maoyan.com/'+myid
            yield scrapy.Request(url=url2, callback=self.parse2, dont_filter=False)

    def parse2(self, response):
        movie_brief = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        mytype = movie_brief.xpath('./a/text()')
        onlinedate = movie_brief.xpath('./li/text()')
        print(mytype.extract())
        print(onlinedate.extract())
