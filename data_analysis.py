from loguru import logger
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_data(df):
    try:
        # Проверяем наличие необходимых колонок
        required_columns = ['age', 'salary', 'experience', 'projects']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            logger.warning(f"Отсутствуют необходимые колонки: {missing_columns}")
            return {}

        # Основной анализ
        analysis = {
            'basic_stats': df.describe(),
            'correlations': df.corr(),
            'missing_values': df.isnull().sum()
        }

        # Дополнительные метрики
        if 'salary' in df.columns:
            analysis['salary_stats'] = {
                'mean_salary': df['salary'].mean(),
                'median_salary': df['salary'].median(),
                'max_salary': df['salary'].max(),
                'min_salary': df['salary'].min()
            }

        return analysis

    except Exception as e:
        logger.error(f"Ошибка при анализе данных: {str(e)}")
        return {}

def visualize_data(df):
    try:
        # Проверяем наличие необходимых данных
        if df.empty:
            logger.warning("Данные для визуализации отсутствуют")
            return

        # Создаем директорию для отчетов, если её нет
        if not os.path.exists('reports/visualizations'):
            os.makedirs('reports/visualizations')

        # Визуализация только существующих колонок
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

        for col in numeric_cols:
            try:
                # Создаем визуализации
                plt.figure(figsize=(10, 6))
                sns.histplot(df[col], kde=True)
                plt.title(f'Распределение {col}')
                plt.savefig(f'reports/visualizations/{col}_distribution.png')
                plt.close()

            except Exception as e:
                logger.warning(f"Ошибка при визуализации {col}: {str(e)}")

        return True

    except Exception as e:
        logger.error(f"Общая ошибка при визуализации: {str(e)}")
        return False

def generate_report(df, analysis_results):
    try:
        # Проверяем наличие данных
        if df.empty or not analysis_results:
            logger.warning("Нет данных для генерации отчета")
            return

        # Создаем директорию для отчетов, если её нет
        if not os.path.exists('reports'):
            os.makedirs('reports')

        # Создаем Excel отчет
        with pd.ExcelWriter('reports/final_report.xlsx') as writer:
            df.to_excel(writer, sheet_name='Данные', index=False)

            if 'basic_stats' in analysis_results:
                analysis_results['basic_stats'].to_excel(writer, sheet_name='Статистика')

            if 'correlations' in analysis_results:
                analysis_results['correlations'].to_excel(writer, sheet_name='Корреляции')

            if 'salary_stats' in analysis_results:
                pd.DataFrame(analysis_results['salary_stats'], index=[0]).T.to_excel(writer, sheet_name='Зарплаты')

        logger.info("Отчет успешно сгенерирован")
        return True

    except Exception as e:
        logger.error(f"Ошибка при генерации отчета: {str(e)}")
        return False
