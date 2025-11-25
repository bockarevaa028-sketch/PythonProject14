# ml_models.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from loguru import logger


def train_regression_model(df, target_column):
    try:
        if target_column not in df.columns:
            raise ValueError(f"Целевая колонка {target_column} не найдена")

        features = df.columns.difference([target_column])
        if len(features) == 0:
            raise ValueError("Нет признаков для обучения модели")

        non_numeric_features = df.select_dtypes(exclude=['float64', 'int64']).columns
        if not non_numeric_features.empty:
            raise ValueError(f"Нечисловые признаки: {list(non_numeric_features)}")

        X = df.drop(columns=[target_column])
        y = df[target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
        numeric_transformer = StandardScaler()

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features)
            ]
        )

        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())
        ])

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }

        logger.info(f"Метрики модели: {metrics}")

        return model, metrics

    except Exception as e:
        logger.error(f"Ошибка при обучении модели: {str(e)}")
        raise  


def evaluate_model(model, X_test, y_test):
    try:
        y_pred = model.predict(X_test)
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }
        return metrics
    except Exception as e:
        logger.error(f"Ошибка при оценке модели: {str(e)}")
        return {}


def save_model(model, model_path):
    try:
        import joblib
        joblib.dump(model, model_path)
        logger.info(f"Модель сохранена в {model_path}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении модели: {str(e)}")
