# 데이터 준비 및 전처리를 위한 함수를 모아둔 파일
import pandas as pd
import numpy as np
from typing import (
    Iterable,
    Union,
    Tuple,
    Optional,
)
import sys
import seaborn as sns
import matplotlib.pyplot as plt


class Dataset:
    
    def __init__(self, path: Optional[str]=None, filename: Optional[str]=None,
                 df: Optional[pd.DataFrame]=None, print_info: bool=True, **kwargs):
        """Constructor."""
        self.path = path
        self.filename = filename
        self.df = df
        self.print_info = print_info
        
        try:
            self.extension = self._get_extension(filename)
            self.data = self._load_data(**kwargs)
        except AttributeError:
            self.filename = filename
            self.data = df
        finally:
            self._print_dataset_info()

    def _get_extension(self, filename: str) -> str:
        """파일명과 확장자명 분리"""
        filename_component = filename.split('.')
        extension = filename_component[1]
        return extension
        
    def _load_data(self, **kwargs) -> pd.DataFrame:
        """CSV 파일 pandas dataframe으로 불러오기"""
        if self.extension == 'csv':
            df = pd.read_csv(f'{self.path}/{self.filename}', **kwargs)
        elif self.extension == 'pkl':
            df = pd.read_pickle(f'{self.path}/{self.filename}', **kwargs)
        else:
            raise Exception(f'Currently does not support reading .{self.extension} file.')
        return df

    def _print_dataset_info(self) -> None:
        """데이터에 대한 간단한 정보 표기"""
        if not self.print_info:
            return
        total_mem_usage = self.data.memory_usage(deep=True, index=True)

        if isinstance(total_mem_usage, pd.Series):
            total_mem_usage = total_mem_usage.sum()
            num_features = self.data.shape[1]
            dtype_list = self.data.dtypes.unique()
        else:
            num_features = 1
            dtype_list = [self.data.dtypes]
            
        try:
            info = f'[{self.path}/{self.filename}.{self.extension}]'
        except AttributeError:
            info = type(self.data)
            
        print(f'{info}\n'
              f'Size: {total_mem_usage/1024**2:.2f} MiB\n'
              f'Number of Features: {num_features}')

        for dtype in dtype_list:
            try:
                num_dtype = self.data.select_dtypes(dtype).shape[1]
            except AttributeError:
                num_dtype = 1
            finally:
                print(f' |_{dtype} => {num_dtype}')
            
    def remove_punct(self, cols: Iterable[str],
                      pattern: str, regex: bool=False) -> pd.DataFrame:
        """변수에 특수문자 치환"""
        self.data = self.data.replace(pattern, None, regex=regex)
        self.data[cols] = (self.data[cols]
                           .astype('float32')
                           .applymap(lambda x: round(x, 2)))
    
    def check_nans(self, by_pct: bool=False, plot: bool=False) -> pd.Series:
        """결측치 조사"""
        na_info = self.data.isna()
        nans = na_info.sum()
        nans = nans[nans > 0]
        nan_pct = round(nans / len(self.data) * 100, 2)
        if plot:
            sns.heatmap(na_info, cmap='Reds', cbar=False);
            
        if by_pct:
            print(nan_pct)
            return nan_pct
        else:
            print(nans)
            return nans
    
    def plot_nan_ratio(self, nan_pct: pd.Series, figsize: Tuple[int, int]=(7, 5)) -> None:
        """결측치 비율 그리기"""
        nan_pct_ranking = nan_pct.sort_values(ascending=False).to_frame().T
        plt.figure(figsize=figsize)
        sns.barplot(nan_pct_ranking, orient='h');
        
    def drop_data(self, to_drop: Iterable[str], axis: int) -> None:
        """변수/관측치 제거"""
        try:
            self.data.drop(to_drop, axis=axis, inplace=True)
            self.data.reset_index(drop=True, inplace=True)
            print('Successfully dropped!')
        except Exception as e:
            print(e)
            
    def __repr__(self) -> str:
        return (f"Dataset(path='{self.path}', "
                f"filename='{self.filename},' "
                f"df={None if self.df is None else type(self.df)}, "
                f"print_info={str(self.print_info)})")