import mysql.connector
from Intro import show_intro
def flight_game():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='demogame',
        user='root',
        password='Giahung@!497',
        autocommit=True,
        auth_plugin="mysql_native_password",
        use_pure=True
    )
    sql = "select id, name, code from goals"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for id, name, code in rows:
        print(f'{id} name: {name} code:\n{code}')
    cursor.close()
    connection.close()
show_intro()
flight_game()
