from schedule import repeat, every, run_pending
import time
from _2_Data_generation._4_Write_in_DB import write_db
from subprocess import Popen
from os import getcwd


def main_app():
    file_path_current = fr"{getcwd()}\_3_Data_Visualisation\_7_Streamlit.py"
    file_path_current = file_path_current.replace('\\_4_To_run_programs', '')

    main = Popen(["streamlit", "run", file_path_current], shell=False)
    return main


print("Запуск приложения...")
a = main_app()
print("\n Запущено \n")


@repeat(every().day.at('23:00'))
def table_write():
    global a
    a.terminate()
    print("Создание новой таблицы ..")
    write_db()
    print("\n БАЗА ГОТОВА \n")
    print("Запуск приложения...")
    a = main_app()
    print("\n Запущено \n")


print("Ожидание запуска (23:00)..")

while True:
    run_pending()
    time.sleep(60)
