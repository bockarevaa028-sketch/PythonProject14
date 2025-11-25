# tests/test_ml_models.py
import pytest
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from ml_models import train_regression_model


def test_train_regression_model():
    # Создаем тестовые данные
    data = pd.DataFrame({
        'feature': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'target': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]  # Идеальная линейная зависимость
    })

    model, metrics = train_regression_model(data, 'target')

    # Проверяем метрики
    assert metrics['mse'] < 1e-6  # Ожидаем почти идеальное предсказание
    assert metrics['r2'] > 0.99  # R2 должен быть близок к 1.0

    # Проверяем предсказания модели
    predictions = model.predict(data.drop(columns=['target']))
    assert np.allclose(predictions, data['target'])  # Предсказания должны совпадать с истинными значениями


def test_train_regression_model_invalid_target():
    data = pd.DataFrame({'feature': [1, 2, 3]})
    with pytest.raises(ValueError, match="Целевая колонка non_existent_target не найдена"):
        train_regression_model(data, 'non_existent_target')

def test_train_regression_model_empty_data():
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="Целевая колонка target не найдена"):
        train_regression_model(empty_df, 'target')

def test_train_regression_model_non_numeric():
    data = pd.DataFrame({
        'feature': ['a', 'b', 'c'],
        'target': [1, 2, 3]
    })
    with pytest.raises(ValueError, match="Нечисловые признаки"):
        train_regression_model(data, 'target')

def test_train_regression_model_no_features():
    data = pd.DataFrame({'target': [1, 2, 3]})
    with pytest.raises(ValueError, match="Нет признаков для обучения модели"):
        train_regression_model(data, 'target')

def test_train_regression_model_mixed_types():
    data = pd.DataFrame({
        'feature1': [1, 2, 3],
        'feature2': ['a', 'b', 'c'],
        'target': [1, 2, 3]
    })
    with pytest.raises(ValueError, match="Нечисловые признаки"):
        train_regression_model(data, 'target')
