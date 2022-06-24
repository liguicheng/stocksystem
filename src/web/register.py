import hashlib
import pymysql

def register_into_db(name, email, password, database='stock_system'):
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
    if len(result) != 0:
        return "False"

    sql_user = "INSERT INTO user (name, email) VALUES (%s, %s)"
    val_user = [(name, email)]
    cur.executemany(sql_user, val_user)

    user_id_sql = "SELECT id FROM user WHERE email=\"" + email + "\""
    cur.execute(user_id_sql)
    user_id = [x[0] for x in cur.fetchall()][0]

    # 需要对密码进行加密，插入密码表
    password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
    sql_password = "INSERT INTO user_password (password, user_id) VALUES (%s, %s)"
    val_password = [(password, user_id)]
    cur.executemany(sql_password, val_password)

    conn.commit()
    # 关闭连接
    conn.close()
    cur.close()
    return "True"