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
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'test_db')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWD', '00000000')

        self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['movie_name'], 
            item['catagories'], 
            item['release_date'],
        )

        sql_1 = """
                    drop table if exists `movies`;
                    create table if not exists `movies` (
                        `name` varchar(50) not null, 
                        `catagory` varchar(100) not null, 
                        `release` date) 
                        default charset=utf8;
                """
        self.db_cur.execute(sql_1)

        sql_2 = """
                    INSERT INTO `movies`(`name`, `catagory`, `release`) 
                    VALUES (%s, %s, %s)
                """

        self.db_cur.execute(sql_2, values)