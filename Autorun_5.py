import schedule
import time
from Write_in_DB_4 import *


def job():
    write_db()
    print("\n БАЗА ГОТОВА \n")
    return


print("Ожидание 14:00 для запуска программы")
schedule.every().day.at("14:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
