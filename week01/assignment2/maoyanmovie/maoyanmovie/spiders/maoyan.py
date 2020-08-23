import scrapy
from scrapy.selector import Selector
from maoyanmovie.items import MaoyanmovieItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    # def parse(self, response):
    #     pass
    def start_requests(self):
        url = "https://maoyan.com/films?showType=3"
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        items = []
        selector = Selector(response=response)
        movie_list = selector.xpath('//div[@class="movie-hover-info"]')[:10]
        for movie in movie_list:
            item = MaoyanSpidersItem()
            # 这里不优雅，如果遇到取的前面10个对象中存在没有评分的电影，则拿不到name //捂脸
            movie_name = movie.xpath('./div[1]/span[@class="name "]/text()').extract_first()
            catagories = movie.xpath('./div[2]/span/following-sibling::text()').extract_first().strip()
            release_date = movie.xpath('./div[4]/span/following-sibling::text()').extract_first().strip()
            yield item