import os
import pandas as pd
import pytest
from data_loader import load_excel, load_api, validate_data, clean_data

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def test_load_excel():
    excel_path = os.path.join(PROJECT_ROOT, 'data', 'input', 'sample_data.xlsx')
    assert os.path.exists(excel_path), f"Файл {excel_path} не найден"

    df = load_excel(excel_path)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) > 0
    assert len(df) > 0


def test_validate_data():
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Иван', 'Мария', 'Петр'],
        'age': [25, 30, 35]
    })
    validate_data(df)
    assert df['id'].dtype == 'int64'
    assert df['name'].dtype == 'object'
    assert df['age'].dtype == 'int64'


def test_clean_data():
    df = pd.DataFrame({
        'id': [1, 2, None],
        'age': [25, None, 35]
    })
    cleaned_df = clean_data(df)
    assert cleaned_df.isnull().sum().sum() == 0
    assert len(cleaned_df) == len(df)


@pytest.mark.skip(reason="Требуется настройка API")
def test_load_api():
    df = load_api('https://api.example.com/data')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_excel_invalid_path():
    with pytest.raises(FileNotFoundError):
        load_excel('non_existent_file.xlsx')
