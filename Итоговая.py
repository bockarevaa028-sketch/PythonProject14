# main.py

import os
import sys

sys.path.append(os.path.abspath('.'))  # Добавляем текущую директорию в путь поиска

from loguru import logger
import pandas as pd
import os

try:
    import data_loader  # Пытаемся импортировать модуль
    from data_loader import load_csv, validate_data
except ModuleNotFoundError:
    print("Ошибка: файл data_loader.py не найден в текущей директории")
    sys.exit(1)


def create_directories():
    directories = ['data/input', 'data/output', 'data/temp', 'reports']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Создана папка {directory}")


def create_sample_csv():
    try:
        data = {
            'id': [1, 2, 3, 4, 5],
            'name': ['Иван', 'Мария', 'Петр', 'Анна', 'Сергей'],
            'age': [25, 30, 28, 22, 35],
            'salary': [50000, 60000, 55000, 45000, 70000]
        }

        df = pd.DataFrame(data)
        df.to_csv('data/input/sample_data.csv', index=False)
        logger.info("Файл sample_data.csv успешно создан")
        return df
    except Exception as e:
        logger.error(f"Ошибка при создании CSV файла: {str(e)}")
        return None


def main():
    logger.info("Запуск процесса обработки данных")

    # Создаем необходимые директории
    create_directories()

    # Создаем тестовый файл
    create_sample_csv()

    try:
        # Загружаем данные из созданного файла
        df = load_csv('data/input/sample_data.csv')

        if df is not None:
            # Валидируем данные
            df = validate_data(df)
            logger.info("Данные загружены и проверены")

            # Дальнейшая обработка
            logger.info("Проверка данных")
            logger.info("Очистка данных")
            logger.info("Анализ данных")
            logger.info("Создание отчетов")

    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()

from data_loader import (
    load_csv,
    load_excel,
    load_sql,
    load_api,
    validate_data
)


def main():
    logger.info("Запуск процесса обработки данных")

    # Обновленный URL для подключения
    db_url = "postgresql://username:password@localhost:5432/your_db?client_encoding=utf8"

    # Загрузка из SQL
    sql_query = "SELECT * FROM employees"
    df_sql = load_data('sql', sql_query, db_url)



from loguru import logger
import pandas as pd
import os

try:
    import data_loader  # Пытаемся импортировать модуль
    from data_loader import load_csv, validate_data
except ModuleNotFoundError:
    print("Ошибка: файл data_loader.py не найден в текущей директории")
    sys.exit(1)


def create_directories():
    directories = ['data/input', 'data/output', 'data/temp', 'reports']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Создана папка {directory}")


def create_sample_csv():
    try:
        data = {
            'id': [1, 2, 3, 4, 5],
            'name': ['Иван', 'Мария', 'Петр', 'Анна', 'Сергей'],
            'age': [25, 30, 28, 22, 35],
            'salary': [50000, 60000, 55000, 45000, 70000]
        }

        df = pd.DataFrame(data)
        df.to_csv('data/input/sample_data.csv', index=False)
        logger.info("Файл sample_data.csv успешно создан")
        return df
    except Exception as e:
        logger.error(f"Ошибка при создании CSV файла: {str(e)}")
        return None


def main():
    logger.info("Запуск процесса обработки данных")

    # Создаем необходимые директории
    create_directories()

    # Создаем тестовый файл
    create_sample_csv()

    try:
        # Загружаем данные из созданного файла
        df = load_csv('data/input/sample_data.csv')

        if df is not None:
            # Валидируем данные
            df = validate_data(df)
            logger.info("Данные загружены и проверены")

            # Дальнейшая обработка
            logger.info("Проверка данных")
            logger.info("Очистка данных")
            logger.info("Анализ данных")
            logger.info("Создание отчетов")

    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()


# 2 часть

