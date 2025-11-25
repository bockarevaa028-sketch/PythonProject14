
# tests/test_data_analysis.py
import pytest
import pandas as pd
import numpy as np
from data_loader import detect_outliers_iqr, detect_outliers_zscore
from loguru import logger

def calculate_statistics(df):
    stats = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        stats[col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max()
        }
    return stats


def test_calculate_statistics():
    df = pd.DataFrame({
        'values': [1, 2, 3, 4, 5]
    })

    stats = calculate_statistics(df)
    assert stats['values']['mean'] == 3
    assert stats['values']['median'] == 3
    assert stats['values']['std'] > 0
    assert stats['values']['min'] == 1
    assert stats['values']['max'] == 5


def test_detect_outliers_iqr():
    df = pd.DataFrame({
        'values': [1, 2, 3, 4, 100] 
    })

    outliers = detect_outliers_iqr(df)
    assert len(outliers['values']) == 1 
    assert outliers['values']['values'].iloc[0] == 100


def test_detect_outliers_zscore():
    df = pd.DataFrame({
        'values': [1, 2, 3, 4, 5] * 10 + [10000] 
    })

    mean = df['values'].mean()
    std = df['values'].std()
    print(f"Среднее: {mean}, Стандартное отклонение: {std}")

    for threshold in [1, 1.5, 2, 2.5, 3]:
        outliers = detect_outliers_zscore(df, threshold=threshold)
        assert len(outliers['values']) >= 1 

        if threshold <= 3:
            assert outliers['values']['values'].iloc[0] == 10000
            z_score_value = outliers['values']['z_score'].iloc[0]
            assert z_score_value > threshold
            print(f"При пороге {threshold} Z-score = {z_score_value}")

    df_zero_std = pd.DataFrame({
        'values': [5, 5, 5, 5, 5]
    })
    outliers = detect_outliers_zscore(df_zero_std)
    assert outliers['values'].empty

    df_small = pd.DataFrame({
        'values': [1, 2, 3, 4, 10] 
    })
    outliers_small = detect_outliers_zscore(df_small, threshold=1)
    assert len(outliers_small['values']) >= 1

    df_negative = pd.DataFrame({
        'values': [-1000] + list(range(1, 101))  
    })
    outliers_negative = detect_outliers_zscore(df_negative, threshold=2)
    assert len(outliers_negative['values']) >= 1
    assert outliers_negative['values']['values'].iloc[0] == -1000


def test_calculate_statistics_empty():
    df = pd.DataFrame()
    stats = calculate_statistics(df)
    assert stats == {}


def test_calculate_statistics_multiple_columns():
    df = pd.DataFrame({
        'values1': [1, 2, 3, 4, 5],
        'values2': [10, 20, 30, 40, 50]
    })

    stats = calculate_statistics(df)
    assert stats['values1']['mean'] == 3
    assert stats['values2']['mean'] == 30


if __name__ == "__main__":
    pytest.main()
