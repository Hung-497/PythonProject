from game import run_cli

def main():
    db_conf = dict(
        host='127.0.0.1',
        port=3306,
        database='demogame',
        user='root',
        password='Toikobiet123',
        autocommit=True,
    )
    run_cli(db_conf)

if __name__ == "__main__":
    main()
