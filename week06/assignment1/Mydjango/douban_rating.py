import requests
import pymysql
from lxml.etree import HTML
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    cookie = '__utmv=30149280.4682; douban-fav-remind=1; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=D4F57DF55C2630E99034E2D26B6917E3A|5ae60036656b543c11d0b744f9b0db02; __utmz=30149280.1601173737.32.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1601173737.6.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1601276735%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1988463621.1478701486.1601173737.1601276735.33; __utmb=30149280.0.10.1601276735; __utma=223695111.331160516.1597759350.1601173737.1601276736.7; __utmb=223695111.0.10.1601276736; _pk_id.100001.4cf6=dec6603cc090059e.1597759350.7.1601276856.1601173838.; ll="118348"; bid=N2gM7WhTyh4'
    headers = {'user-agent': user_agent, 'cookie': cookie}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res
        print("status code:", res.status_code)
    except requests.RequestException as e:
        raise e


def parse_detail(url):
    response = fetch(url)
    selector = HTML(response.text)
    ratings = selector.xpath('//span[@class="comment-info"]/span[2]/@class')
    stars = [int(rating.split()[0][-2]) for rating in ratings]
    comments = selector.xpath('//span[@class="short"]/text()')
    comment_date = selector.xpath('//span[@class="comment-time "]/text()')
    comment_date = [time.strip() for time in comment_date]
    return stars, comments, comment_date


def save(connection, stars, comments, comment_date):
    for star, comment, date in zip(stars, comments, comment_date):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO movies (star, comment, comment_date) VALUES (%s, %s, %s);"
                cursor.execute(sql, (star, comment, date))
            connection.commit()
        except:
            connection.rollback()


def main():
    dbInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'xxxxxxxx',
        'db': 'douban'
    }
    connection = pymysql.connect(
        host = dbInfo['host'],
        port = dbInfo['port'],
        user = dbInfo['user'],
        password = dbInfo['password'],
        db = dbInfo['db']
    )
    with ThreadPoolExecutor(max_workers=4) as executor:
        BASE_URL = f"https://movie.douban.com/subject/1851857/comments?limit=%s&status=P&sort=new_score"
        all_tasks = []
        for i in range(10):
            url = BASE_URL % (i * 20)
            all_tasks.append(executor.submit(parse_detail, url))
        for future in as_completed(all_tasks):
            try:
                stars, comments, comment_date = future.result()
                save(connection, stars, comments, comment_date)
            except Exception as e:
                print(e)
    
    connection.close()


if __name__ == "__main__":
    main()

