import pymysql.cursors
import pandas as pd

from src.logger import init_logger

logger = init_logger('csv_to_mysql')

from sqlalchemy import create_engine


# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

engine = create_engine("mysql+pymysql://root:play@localhost/realestate?charset=utf8", encoding="utf-8")
# # Connect to the database
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='play',
#                              database='realestate',
#                              cursorclass=pymysql.cursors.DictCursor)



df = pd.read_csv('./data/preprocessed/apt-trade/11110/202106.csv')
logger.info(df.head(10))
df.to_sql(con=engine, name='transaction', if_exists='replace')

# with connection:
#     with connection.cursor() as cursor:
#         # Create a new record
#         columns = f"`{f'`,`'.join(df.columns)}`"
#         values = (','.join(['%s'] * len(df.columns)))
#         logger.info(columns)
#         sql = f"INSERT INTO `transaction` ({columns}) VALUES ({values})"
#         logger.info(sql)
#         for row in df.iterrows():
#             values = row[1].values

           
#         df.to_sql(con=con, name='table_name_for_df', if_exists='replace', flavor='mysql') 
#         # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

# #     # connection is not autocommit by default. So you must commit to save
# #     # your changes.
# #     connection.commit()

# #     with connection.cursor() as cursor:
# #         # Read a single record
# #         sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
# #         cursor.execute(sql, ('webmaster@python.org',))
# #         result = cursor.fetchone()
# #         print(result)