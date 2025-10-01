from game import run_cli

def main():
    db_conf = dict(
        host='127.0.0.1',
        port=3306,
        database='demogame',
        user='root',
        password='Giahung@!497',
        autocommit=True,
        auth_plugin="mysql_native_password",
        use_pure=True
    )
    run_cli(db_conf)

if __name__ == "__main__":
    main()
