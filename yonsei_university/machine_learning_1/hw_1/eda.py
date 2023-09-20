# 시각화 함수를 모아둔 파일
import pandas as pd
import numpy as np
from collections import Counter
from typing import (
    Tuple,
    Iterable,
    Optional,
)
import seaborn as sns
import matplotlib.pyplot as plt


def plot_dist(df: pd.DataFrame, cols: Iterable[str]) -> None:
    for col in cols:
        plt.figure(figsize=(6, 4))
        sns.distplot(df[col], kde=False);

def get_categorical_info(df: pd.DataFrame, cols: Iterable[str],
                         figsize: Tuple[int, int]=(5, 3),
                         rotation: Optional[str]=None) -> None:
    """명목변수의 변수별 카테고리 시각화"""
    cat_col_num = df[cols].nunique()

    for i, v in cat_col_num.items():
        print(f'{i}: {v}')

    for i, v in cat_col_num.items():
        info = Counter(df[i])
        cat_sorted = {str(e[0]): e[1] for e in info.most_common()}
        label, label_cnt = cat_sorted.keys(), cat_sorted.values()

        plt.figure(figsize=figsize)
        plt.bar(x=label, height=label_cnt, width=0.3)
        plt.xticks(list(label), rotation=rotation)
        plt.title(i);

def plot_churn_rate(df: pd.DataFrame, col: str,
                    title: str='', figsize: Tuple[int, int]=(3, 3)) -> None:
    total_exited = df['Exited'].sum()
    pivot_tbl = pd.pivot_table(
        df,
        values='Exited',
        columns=[col],
        aggfunc=lambda x: np.sum(x)/total_exited,
    )
    plt.figure(figsize=figsize)
    sns.barplot(pivot_tbl, width=0.3)
    plt.title(title)
    plt.yticks(np.arange(0, 1.1, 0.2));
    
def get_target_percentage(df: pd.DataFrame, col: str,
                          label: Iterable[str]=['0', '1'],
                          figsize: Tuple[int, int]=(8, 3)) -> pd.Series:
    """클래스 비율 시각화. 이진 클래스만 가능"""
    percentage = df[col].value_counts(normalize=True)
    name = percentage.index.name
    
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.barh([1], percentage[0], label=label[0])
    ax.barh([1], percentage[1], left=percentage[0], label=label[1])
    for c in ax.containers:
        labels = [f'{v.get_width():.2%}' for v in c]
        ax.bar_label(
            c,
            label_type='center',
            labels=labels,
            size=10,
        )
    plt.legend()
    plt.yticks([1], [f'{name} percentage'])
    plt.margins(y=2, x=0);
    return percentage

def plot_cont_boxplot(df: pd.DataFrame, figsize: Tuple[int, int]=(5, 3)) -> None:
    """개별 연속변수의 박스플롯 그리기"""
    plt.figure(figsize=figsize)
    sns.boxplot(df, orient='h');
    
def corr_plot(df: pd.DataFrame, cmap: str='Blues') -> pd.DataFrame:
    """상관계수 히트맵 그리기"""
    corr_matrix = df.corr()
    sns.heatmap(np.abs(corr_matrix), cmap=cmap);
    return corr_matrix