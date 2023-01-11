import schedule
import time
from Data_generation_2.Write_in_DB_4 import write_db


def job():
    write_db()
    print("\n БАЗА ГОТОВА \n")
    print("Ожидание следующего запуска программы в 14:00")
    return


print("Ожидание 14:00 для запуска программы")
schedule.every().day.at("14:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
