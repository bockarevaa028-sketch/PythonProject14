# tests/test_data_validation.py
import pytest
import pandas as pd
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_loader import validate_data


def test_validate_data():
    df = pd.DataFrame({
        'col1': [1, 2, None, 4],
        'col2': ['a', 'b', 'a', 'd']
    })

    # Теперь функция возвращает кортеж (df, report)
    cleaned_df, report = validate_data(df)

    # Проверяем, что отчет содержит корректные значения
    assert report['missing_values'] > 0
    assert report['duplicates'] == 0
    assert report['outliers'] == 0

    # Проверяем, что DataFrame не пустой
    assert not cleaned_df.empty

    # Проверяем, что количество строк не увеличилось
    assert len(cleaned_df) <= len(df)


if __name__ == "__main__":
    pytest.main()
