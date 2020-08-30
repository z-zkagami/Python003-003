# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import csv
# import os

import pymysql

# class MaoyanmoviePipeline:
#     def __init__(self):
#         # csv文件的位置
#         store_file = os.path.dirname(__file__) + '/maoyan_movies.csv'

#         self.file = open(store_file, 'a+', encoding="utf-8", newline='')

#         self.writer = csv.writer(self.file, dialect="excel")

#     def process_item(self, item, spider):
#         if item['movie_name']:
#             self.writer.writerow([item['movie_name'], item['catagories'], item['release_date']])
#         return item

#     def close_spider(self, spider):
#         # 关闭爬虫时顺便将文件保存退出
#         self.file.close()

class MaoyanmoviePipeline:
    def conn_db(self, spider):
        self.conn = pymysql.connect(host = 'localhost', 
                                    user = 'test', 
                                    db = 'test', 
                                    charset = 'utf8-mb4', 
                                    password = '000000')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        movie_name = item['movie_name']
        catagories = item['catagories']
        release_data = item['release_data']
        value = (movie_name, catagories, release_data)
        self.values.append(value)
        sql = "INSERT INTO `test`(`movie_name`, `catagories`, `release_data`) VALUES(%s, %s, %s)"
        try:
            self.cursor.execute(sql, (movie_name, catagories, release_data))
            self.conn.commit()
        except Exception as e:
            self.rollback()
            print(e)

        return item

    def close_db(self, spider):
        self.conn.close()

            