import os
import sys
import pandas as pd
import numpy as np
from loguru import logger
import schedule
import time
from config import DB_CONFIG, PATHS, API_CONFIG
from ml_models import train_regression_model, save_model

try:
    from data_loader import (
        load_excel,
        load_sql,
        load_api,
        load_csv,
        validate_data,
        clean_data
    )
    from data_analysis import (
        analyze_data,
        visualize_data,
        generate_report
    )
    from utils import send_notification
except ModuleNotFoundError as e:
    logger.error(f"Ошибка импорта: {str(e)}")
    sys.exit(1)


def create_directories():
    directories = [
        PATHS['data_input'],
        PATHS['data_output'],
        PATHS['reports_documents'],
        PATHS['reports_visualizations'],
        PATHS['models']
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Создана папка {directory}")


def main():
    try:
        create_directories()

        # Создаем пустой датафрейм
        df = pd.DataFrame()

        # Загрузка из Excel
        excel_path = os.path.join(PATHS['data_input'], 'sample_data.xlsx')
        if os.path.exists(excel_path):
            logger.info("Начинаем загрузку из Excel")
            excel_df = load_excel(excel_path)
            if excel_df is not None:
                df = pd.concat([df, excel_df], ignore_index=True)

        # Загрузка из API
        logger.info("Начинаем загрузку из API")
        api_df = load_api(
            API_CONFIG['base_url'] + API_CONFIG['endpoints']['data'],
            headers=API_CONFIG['headers'],
            params=API_CONFIG['params']
        )
        if api_df is not None:
            df = pd.concat([df, api_df], ignore_index=True)

        if df.empty:
            logger.error("Данные не были загружены ни из одного источника")
            return

        # Обработка данных
        validate_data(df)
        df = clean_data(df)  # Важно сохранить результат очистки

        # Инициализация результатов анализа
        analysis_results = {}

        # Обучаем ML-модель
        model, metrics = None, {}
        if 'salary' in df.columns:
            logger.info("Начинаем обучение модели")
            model, metrics = train_regression_model(df, 'salary')

            if model:
                # Сохраняем модель
                save_model(
                    model,
                    os.path.join(PATHS['models'], 'salary_model.pkl')
                )

                # Добавляем метрики в анализ
                metrics_dict = {
                    'MSE': metrics['mse'],
                    'R2': metrics['r2']
                }
                analysis_results['model_metrics'] = metrics_dict

        # Анализ и отчетность с обработкой ошибок
        try:
            analysis_results = analyze_data(df)

            if not analysis_results:
                logger.warning("Результаты анализа отсутствуют")

            visualize_success = visualize_data(df)
            report_success = generate_report(df, analysis_results)

            if not visualize_success or not report_success:
                logger.warning("Не все процессы отчетности выполнены успешно")

        except Exception as e:
            logger.error(f"Ошибка при выполнении анализа и отчетности: {str(e)}")

        logger.info("Все процессы успешно завершены")

    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")
        send_notification(
            "Критическая ошибка в системе",
            f"Произошла ошибка: {str(e)}",
            "your-email@domain.com"
        )


def job():
    try:
        main()
        logger.info("Задача выполнена успешно")
    except Exception as e:
        logger.error


def job():
    try:
        main()
        logger.info("Задача выполнена успешно")
    except Exception as e:
        logger.error(f"Ошибка при выполнении задачи: {str(e)}")
        send_notification(
            "Ошибка в расписании",
            f"Произошла ошибка при выполнении задачи: {str(e)}",
            "your-email@domain.com"
        )

if __name__ == "__main__":
    try:
        # Настройка расписания
        schedule.every().day.at("08:00").do(job)

        # Запуск основного процесса сразу при старте
        main()

        # Бесконечный цикл для проверки расписания
        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Программа остановлена пользователем")
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске: {str(e)}")
        send_notification(
            "Критическая ошибка",
            f"Произошла ошибка при запуске программы: {str(e)}",
            "your-email@domain.com"
        )