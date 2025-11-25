# tests/test_data_cleaning.py
import pytest
import pandas as pd
from data_loader import clean_data


def test_clean_data():
    df = pd.DataFrame({
        'col1': [1, 2, None, 4],
        'col2': ['a', 'b', None, 'd'],
        'date': ['2023-01-01', '2023-01-02', None, '2023-01-04']
    })

    cleaned_df = clean_data(df)

    assert cleaned_df.isnull().sum().sum() == 0

    expected_columns = ['col1', 'col2_b', 'col2_d']

    date_columns = [col for col in cleaned_df.columns if col.startswith('date_')]

    for col in expected_columns:
        assert col in cleaned_df.columns

    assert pd.api.types.is_numeric_dtype(cleaned_df['col1'])
    assert pd.api.types.is_bool_dtype(cleaned_df['col2_b'])
    assert pd.api.types.is_bool_dtype(cleaned_df['col2_d'])

    for date_col in date_columns:
        assert pd.api.types.is_bool_dtype(cleaned_df[date_col])

    assert len(cleaned_df) == 4


def test_clean_data_empty():
    df_empty = pd.DataFrame()
    cleaned_df = clean_data(df_empty)
    assert cleaned_df.empty


def test_clean_data_single_row():
    df_single = pd.DataFrame({
        'col1': [1],
        'col2': ['a'],
        'date': ['2023-01-01']
    })
    cleaned_df = clean_data(df_single)
    assert len(cleaned_df) == 1
    assert cleaned_df.isnull().sum().sum() == 0


if __name__ == "__main__":
    pytest.main()
