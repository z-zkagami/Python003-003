import pandas as pd
import pymysql

conn = pymysql.connect(host='localhost', 
                       user='test', 
                       password='00000000', 
                       port=3306, 
                       db='testdb', 
                       charset='utf8mb4')


# 1. SELECT * FROM data;
sql = 'SELECT * FROM data'
df = pd.read_sql(sql, conn)

# 2. SELECT * FROM data LIMIT 10;
df.loc[:10]


# 3. SELECT id FROM data;  //id 是 data 表的特定一列
df['id']

# 4. SELECT COUNT(id) FROM data;
df['id'].count()

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
df.loc([(df['id'] < 1000) & (df['age'] > 30)])

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
df.groupby(['id']).agg({'order_id': 'nunique'})

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
sql1 = 'SELECT * FROM table1'
sql2 = 'SELECT * FROM table2'

t1 = pd.read_sql(sql1, conn)
t2 = pd.read_sql(sql2, conn)
pd.merge(t1, t2, how='inner', on=['id', 'id'])

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([t1, t2])

# 9. DELETE FROM table1 WHERE id=10;
t9 = t1[ t1['id'] != 10 ]

# 10. ALTER TABLE table1 DROP COLUMN column_name;
df.drop(columns=['column_name'])

conn.close()