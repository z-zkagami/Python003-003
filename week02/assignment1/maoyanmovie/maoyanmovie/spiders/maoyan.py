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
        movie_list = Selector(response=response).xpath('//div[@class="movie-hover-info"]')[:10]
        for movie in movie_list:
            # 修改为新方法get和getall
            movie_name = movie.xpath('./div[1]/span[@class="name "]/text()').get()
            print(movie_name)
            catagories = movie.xpath(f'./div/span[contains(text(), "类型")]/parent::*/text()').getall()[-1].strip()
            print(catagories)
            release_date = movie.xpath('./div/span[contains(text(), "上映时间")]/parent::*/text()').getall()[-1].strip()
            print(release_date)

            item = MaoyanmovieItem()
            item['movie_name'] = movie_name
            item['catagories'] = catagories
            item['release_date'] = release_date
            yield item