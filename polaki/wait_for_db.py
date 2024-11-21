import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="polaki_new",
                user="mafi2",
                password="1234",
                host="db",
                port="5432"
            )
            conn.close()
            break
        except OperationalError:
            print("Database not ready, waiting...")
            time.sleep(2)

if __name__ == "__main__":
    wait_for_db()
