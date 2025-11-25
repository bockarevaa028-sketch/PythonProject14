import pandas as pd
import numpy as np
import sqlalchemy
import requests
import os
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from loguru import logger

def detect_outliers_iqr(df, columns=None):
    if columns is None:
        columns = df.select_dtypes(include=['float64', 'int64']).columns

    outliers = {}
    for col in columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers[col] = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

    return outliers

def detect_outliers_zscore(df, columns=None, threshold=3):
    if columns is None:
        columns = df.select_dtypes(include=['float64', 'int64']).columns

    outliers = {}
    for col in columns:
        if df[col].std() == 0:
            logger.warning(f"Колонка {col} имеет нулевое стандартное отклонение")
            outliers[col] = pd.DataFrame()
            continue

        z_scores = (df[col] - df[col].mean()) / df[col].std()

        outliers[col] = df[abs(z_scores) > threshold]

        outliers[col]['z_score'] = z_scores[abs(z_scores) > threshold]

    return outliers




def validate_data(df):
    try:
        logger.info("Начинаем валидацию данных")

        type_info = {}
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                type_info[col] = 'числовой'
            elif df[col].dtype == 'object':
                type_info[col] = 'строковый'
            else:
                type_info[col] = 'другой'

            logger.info(f"Колонка {col} имеет тип {type_info[col]}")

        duplicates = df.duplicated().sum()
        if duplicates > 0:
            logger.warning(f"Обнаружено {duplicates} дубликатов")
            df = df.drop_duplicates()

        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            logger.warning("Обнаружены пропуски:")
            for col, count in missing_values.items():
                if count > 0:
                    logger.warning(f"Колонка {col}: {count} пропусков")

        logger.info("Начинаем поиск выбросов")
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

        iqr_outliers = detect_outliers_iqr(df, numeric_cols)
        zscore_outliers = detect_outliers_zscore(df, numeric_cols)

        for col in numeric_cols:
            iqr_count = len(iqr_outliers[col])
            zscore_count = len(zscore_outliers[col])

            if iqr_count > 0:
                logger.warning(f"Колонка {col}: {iqr_count} выбросов по IQR")

            if zscore_count > 0:
                logger.warning(f"Колонка {col}: {zscore_count} выбросов по Z-score")

        return df

    except Exception as e:
        logger.error(f"Ошибка при валидации данных: {str(e)}")
        return None

def handle_missing_values(df):
    try:
        missing_values = df.isnull().sum()
        logger.info(f"Пропущенные значения:\n{missing_values}")

        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns

        if not numeric_cols.empty:
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

        if not categorical_cols.empty:
            df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])

        if not numeric_cols.empty:
            imputer = KNNImputer(n_neighbors=5)
            df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

        return df
    except Exception as e:
        logger.error(f"Ошибка при обработке пропусков: {str(e)}")
        return df

def encode_categorical_features(df):
    try:
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns

        if not categorical_cols.empty:
            df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

        return df
    except Exception as e:
        logger.error(f"Ошибка при кодировании категориальных признаков: {str(e)}")
        return df

# Функция нормализации данных
def normalize_data(df):
    try:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

        if not numeric_cols.empty:
            scaler = MinMaxScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        return df
    except Exception as e:
        logger.error(f"Ошибка при нормализации данных: {str(e)}")
        return df


def clean_data(df):
    try:
        logger.info("Начинаем очистку данных")

        if df.empty:
            logger.error("Данные пустые, очистка невозможна")
            return df

        df = handle_missing_values(df)

        df = encode_categorical_features(df)

        df = normalize_data(df)

        logger.info("Данные успешно очищены")
        return df
    except Exception as e:
        logger.error(f"Общая ошибка очистки данных: {str(e)}")
        return df


def create_database_connection():
    try:
        db_url = DB_CONFIG['url']

        engine = sqlalchemy.create_engine(
            db_url,
            connect_args={
                'client_encoding': 'utf8',
                'options': '-c search_path=your_schema',
                'application_name': 'data_loader'
            }
        )
        logger.info("Подключение к БД успешно установлено")
        return engine
    except Exception as e:
        logger.error(f"Ошибка подключения к БД: {e}")
        return None


def load_sql(query):
    try:
        engine = create_database_connection()
        if engine is None:
            raise Exception("Не удалось создать подключение к БД")

        logger.info("Выполняется SQL-запрос")
        df = pd.read_sql(query, engine)
        logger.info("Данные успешно загружены из БД")
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных из БД: {str(e)}")
        return None


def load_excel(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")

        dtype = {
            'id': int,
            'age': int,
            'salary': float,
            'experience': int,
            'projects': int
        }

        df = pd.read_excel(file_path)
        return df

    except FileNotFoundError as e:
        logger.error(f"Ошибка при загрузке Excel-файла: {str(e)}")
        raise 
    except Exception as e:
        logger.error(f"Ошибка при загрузке Excel-файла: {str(e)}")
        return None


def load_api(url, params=None, headers=None):
    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        df = pd.json_normalize(data)
        logger.info("Данные из API успешно загружены")
        return df

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при загрузке из API: {str(e)}")
        return None

def load_data(source_type, file_path=None, query=None, url=None):
    try:
        if source_type == 'csv':
            return pd.read_csv(file_path, encoding='utf-8')
        elif source_type == 'excel':
            return load_excel(file_path)
        elif source_type == 'sql':
            if query is None:
                raise ValueError("Для SQL необходим SQL-запрос")
            return load_sql(query)
        elif source_type == 'api':
            if url is None:
                raise ValueError("Для API необходим URL")
            return load_api(url)
        else:
            logger.error("Неподдерживаемый тип источника данных")
            return None
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {str(e)}")
        return None

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        logger.info(f"CSV файл {file_path} успешно загружен")
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке CSV файла: {str(e)}")
        return None

import numpy as np
from loguru import logger


def validate_data(df):
    try:
        report = {
            'missing_values': df.isnull().sum().sum(),
            'duplicates': df.duplicated().sum(),
            'outliers': 0
        }

        if report['duplicates'] > 0:
            logger.warning("Обнаружены дубликаты!")
            df = df.drop_duplicates()
            report['duplicates'] = df.duplicated().sum()

        if report['missing_values'] > 0:
            logger.warning("Обнаружены пропуски!")

        for col in df.columns:
            if df[col].dtype == 'object':
                logger.info(f"Колонка {col} содержит строковые данные")
            elif df[col].dtype in ['int64', 'float64']:
                logger.info(f"Колонка {col} содержит числовые данные")

        for col in df.select_dtypes(include=[np.number]).columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            report['outliers'] += outliers_count

        return df, report

    except Exception as e:
        logger.error(f"Ошибка при валидации данных: {str(e)}")
        return None, None

