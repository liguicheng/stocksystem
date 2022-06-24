import hashlib
import pymysql

def login_into_db(email, password, database='stock_system'):
    # 连接数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', charset='utf8', local_infile=1)
    cur = conn.cursor()
    # 使用数据库
    cur.execute('use %s' % database)
    # 设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')

    cur.execute("SELECT * FROM user WHERE email=\"" + email + "\"")
    result = cur.fetchall()  # fetchall() 获取所有记录
    if len(result) == 0:
        return "NOT_EXIST"

    # 需要把密码加密了，然后看与数据库中加密后的密码一样不
    user_id_sql = "SELECT id FROM user WHERE email=\"" + email + "\""
    cur.execute(user_id_sql)
    # 获取从数据库中选出的数据
    user_id = [x[0] for x in cur.fetchall()][0]

    password_encode = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
    sql_password = "SELECT password FROM user_password WHERE user_id=\"" + str(user_id) + "\""
    cur.execute(sql_password)
    user_password = [x[0] for x in cur.fetchall()][0]
    if password_encode != user_password:
        return "False"

    conn.commit()
    # 关闭连接
    conn.close()
    cur.close()
    return "True"

def get_user_name(email, database='stock_system'):
    # 连接数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', charset='utf8', local_infile=1)
    cur = conn.cursor()
    # 使用数据库
    cur.execute('use %s' % database)
    # 设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')

    cur.execute("SELECT name FROM user WHERE email=\"" + email + "\"")
    result = cur.fetchall()  # fetchall() 获取所有记录
    name = [x[0] for x in result][0]

    return name