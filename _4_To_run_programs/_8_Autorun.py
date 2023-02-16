from schedule import repeat, every, run_pending
import time
from subprocess import Popen, call
from os import getcwd


def main_app():
    file_path_current = fr"{getcwd()}\_3_Data_Visualisation\_7_Streamlit.py"
    file_path_current = file_path_current.replace('\\_4_To_run_programs', '')

    main = Popen(["streamlit", "run", file_path_current], shell=False)
    return main


def main_db():
    file_path_current = fr"{getcwd()}\_2_Data_generation\_4_Write_in_DB.py"
    file_path_current = file_path_current.replace('\\_4_To_run_programs', '')

    main = call(["python", file_path_current], shell=True)
    return main


print("Запуск приложения...")
app_ = main_app()


@repeat(every().day.at('23:00'))
def table_write():
    global app_
    app_.terminate()
    print("Создание новой таблицы ..")
    main_db()
    print("Запуск приложения...")
    app_ = main_app()


print("Ожидание запуска (23:00)..")

while True:
    run_pending()
    time.sleep(60)
