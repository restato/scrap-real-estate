import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='play',
                             database='realestate',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM transaction LIMIT 10"
        # sql = "SELECT COUNT(*) FROM transaction"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)