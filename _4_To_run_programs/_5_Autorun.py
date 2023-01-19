import schedule
import time
from _2_Data_generation._4_Write_in_DB import write_db


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
