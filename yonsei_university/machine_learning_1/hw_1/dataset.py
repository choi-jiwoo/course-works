# 데이터 준비 및 전처리를 위한 함수를 모아둔 파일
import pandas as pd
import numpy as np
from typing import Iterable, Union
import seaborn as sns


class Dataset:
    
    def __init__(self, path: str, filename: str, extension: str='csv', print_info: bool=True):
        """생성자"""
        self.path = path
        self.filename = filename
        self.extension = extension
        self.print_info = print_info
        self.data = self._load_data()
        self._print_dataset_info()
        
    def _load_data(self) -> pd.DataFrame:
        """CSV파일 불러오기"""
        df = pd.read_csv(f'{self.path}/{self.filename}.{self.extension}')
        return df

    def _print_dataset_info(self) -> None:
        """데이터에 대한 간단한 정보 표기"""
        if not self.print_info:
            return
        total_mem_usage = self.data.memory_usage(deep=True, index=True).sum()
        print(f'[{self.filename}]\n'
              f'Size: {total_mem_usage/1024**2:.2f} MiB\n'
              f'Number of Features: {self.data.shape[1]}')

        for dtype in self.data.dtypes.unique():
            print(f' |_{dtype} => {self.data.select_dtypes(dtype).shape[1]}')
            
    def remove_puct(self, cols: Iterable[str],
                      pattern: str, regex: bool=False) -> pd.DataFrame:
        """변수에 특수문자 치환"""
        self.data = self.data.replace(pattern, None, regex=regex)
        self.data[cols] = (self.data[cols]
                           .astype('float32')
                           .applymap(lambda x: round(x, 2)))

    def get_dtype_col_name(self, dtype: Union[str, Iterable[str]]) -> pd.DataFrame:
        """명목변수 추출"""
        subset = self.data.select_dtypes(dtype).columns
        return subset
        
    def get_one_hot_encode(self, cols: Iterable[str]) -> pd.DataFrame:
        """원핫인코딩"""
        one_hot_encoded = pd.get_dummies(
            self.data,
            columns=cols,
            drop_first=True,
            dtype=np.int8,
        )
        return one_hot_encoded
    
    def check_nans(self, by_pct: bool=False) -> None:
        """결측치 조사"""
        na_info = self.data.isna()
        sns.heatmap(na_info, cmap='Reds', cbar=False);
        nans = na_info.sum()
        nans = nans[nans > 0]
        print(round(nans / len(self.data) * 100, 2) if by_pct else nans)
        
    def drop_data(self, to_drop: Iterable[str], axis: int) -> None:
        """변수/관측치 제거"""
        try:
            self.data.drop(to_drop, axis=axis, inplace=True)
            self.data.reset_index(drop=True, inplace=True)
            print('Successfully dropped!')
        except Exception as e:
            print(e)
            
    def __repr__(self) -> str:
        return f"Dataset(path='{self.path}', filename='{self.filename}', extension='{self.extension}')"
        
        