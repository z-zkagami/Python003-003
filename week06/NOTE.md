# 学习笔记

**Django ORM API常见问题**

> 找不到MySQLdb

    django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'

解决方法：在`__init__.py`文件中添加如下内容

    import pymysql
    pymysql.install_as_MySQLdb()

> MySQL版本问题

    version = Database.version_info

解决方法：注释对应的判断代码

    # if version < (1, 3, 13):
    # raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)

> Python版本的问题

    AttributeError: 'str' object has no attribute 'decode'

解决方法：在`PATH/TO/DJANGO/DB/BACKENDS/MYSQL/SITE_PACKAGES/operations.py`中注释相应代码

    def last_executed_query(self, cursor, sql, params):
    query = getattr(cursor, '_executed', None)
    # if query is not None:
    #     query = query.decode(errors='replace')
    return query

