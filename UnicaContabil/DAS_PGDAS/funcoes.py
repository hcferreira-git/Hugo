def ConectaBD():
    return pymysql.connect(
    host='localhost',
    user='master',
    password='123456',
    database='unicacontabil',
    cursorclass = pymysql.cursors.DictCursor
)