# 분석에 사용할 함수들을 주피터 파일에서 분리
import pandas as pd
import numpy as np
from typing import (
    Optional,
    Iterable,
    Tuple,
)
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import (
    KNNImputer,
    SimpleImputer,
)
from utils.heomdistance import HeomDistance

from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    OrdinalEncoder,
    FunctionTransformer,
)
from sklearn.metrics import f1_score
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def imputation(data: pd.DataFrame, cat_ix: Iterable[int],
               n_neighbors: int=1, nan_eqv: int=-9999,
               normalised: str='normal') -> pd.DataFrame:
    """결측치 보간"""
    columns = data.columns
    data = data.to_numpy()
    heom_dist = HeomDistance(data, cat_ix, normalised=normalised)
    imputer = KNNImputer(
        missing_values=nan_eqv,
        n_neighbors=n_neighbors,
        metric=heom_dist.heom,
    )
    imputed = imputer.fit_transform(data)
    imputed_data = pd.DataFrame(imputed, columns=columns)
    if n_neighbors > 1:
        round_cat = imputed_data.iloc[:, list(cat_ix)].apply(round, 0)
        imputed_data.iloc[:, list(cat_ix)] = round_cat
    return imputed_data

def oversample(X: pd.DataFrame, y: pd.Series, method,
               **kwargs) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """연속형 변수 오버샘플링"""
    oversampling_method = method(**kwargs)
    X_resample, y_resample = oversampling_method.fit_resample(
        X.to_numpy(),
        y.to_numpy().reshape(-1, 1),
    )
    synthesized = pd.merge(
        X,
        pd.DataFrame(X_resample, columns=X.columns),
        how='outer',
        indicator=True,
    ).query('_merge == "right_only"').drop('_merge', axis=1)
    oversampled_dataset = pd.DataFrame(np.concatenate(
        (X_resample, y_resample.reshape(-1, 1)),
        axis=1),
    )
    oversampled_dataset.columns = list(X.columns) + [y.name]
    return oversampled_dataset, synthesized

def knn_oversampling(X: pd.DataFrame, oversampled_dataset: pd.DataFrame,
                     synthesized: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """명목형 변수 오버샘플링. 연속형 변수 오버샘플링 이후 진행."""
    knn_dataset = pd.DataFrame(
        [],
        index=synthesized.index,
        columns=X.columns,
    )    
    knn_nan_data = pd.concat([
        pd.concat([X, knn_dataset]),
        oversampled_dataset,
    ], axis=1)
    knn_nan_data = (knn_nan_data.astype(float)
                    .fillna(kwargs['nan_eqv']))
    kwargs['cat_ix'] = np.arange(0, len(X.columns), 1)
    knn_dataset = imputation(knn_nan_data, **kwargs)
    return knn_dataset

def scale_and_encode(train_X: pd.DataFrame, val_X: pd.DataFrame,
                     numeric_scaler: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """변수 스케일링"""
    scaler = {
        'standard': StandardScaler,
        'minmax': MinMaxScaler,
        'robust': RobustScaler,
    }
    
    cont_col = train_X.select_dtypes(['int', 'float']).columns
    ordinal_col = [
        'PerformanceStatus',
        'Encefalopathydegree',
        'Ascitesdegree',
    ]
    non_binary_col = list(cont_col) + ordinal_col
    binary_col = [i for i in train_X.columns if i not in non_binary_col]
    
    numeric_transformer = Pipeline(
        [
            ('scaler', scaler[numeric_scaler]()),
        ]
    )
    ordinal_transformer = Pipeline(
        [
            ('ordinal', OrdinalEncoder()),
        ]
    )
    identity_transformer = Pipeline(
        [
            ('identity', FunctionTransformer(func=None,
                                             feature_names_out='one-to-one')),
        ]
    )
    column_transformer = ColumnTransformer(
        transformers=[
            ('id', identity_transformer, binary_col),
            ('ord', ordinal_transformer, ordinal_col),
            ('num', numeric_transformer, cont_col),
        ],
    )
    train_X = column_transformer.fit_transform(train_X)
    val_X = column_transformer.transform(val_X)

    new_col_name = column_transformer.get_feature_names_out()
    train_X = pd.DataFrame(train_X, columns=new_col_name)
    val_X = pd.DataFrame(val_X, columns=new_col_name)

    return train_X, val_X

def cross_validation(X: pd.DataFrame, y: pd.Series, model,
                     numeric_scaler: str, oversampling: Optional[dict]=None,
                     scale: bool=True, verbose: bool=True, **kwargs) -> float:
    """5-폴드 교차검증"""
    kf = KFold(n_splits=5, shuffle=False)
    score_list = {}

    for i, (train_index, val_index) in enumerate(kf.split(X)):
        split_res = []

        for j in [train_index, val_index]:
            split_res.append(y.loc[j].value_counts().to_dict())
        
        train_X = X.loc[train_index, :].reset_index(drop=True)
        train_y = y.loc[train_index].reset_index(drop=True)
        val_X = X.loc[val_index, :].reset_index(drop=True)
        val_y = y.loc[val_index].reset_index(drop=True)

        if scale:
            train_X, val_X = scale_and_encode(train_X, val_X, numeric_scaler)

        if oversampling:
            if scale:
                cont_train_X = train_X.filter(like='num__')
                cat_train_X = train_X.filter(regex='(id__)|(ord__)')
            else:
                cont_train_X = train_X.select_dtypes(['int', 'float'])
                cat_train_X = train_X.select_dtypes('category')
            
            oversampled_dataset, synthesized = oversample(
                cont_train_X,
                train_y,
                oversampling['model'],
                **oversampling['param'],
            )
            oversampled = knn_oversampling(
                cat_train_X,
                oversampled_dataset,
                synthesized,
                **kwargs,
            )
            train_X = oversampled.drop('Class', axis=1)
            train_y = oversampled['Class']
            
        train_X = train_X.to_numpy()
        val_X = val_X.to_numpy()
        train_y = train_y.to_numpy().reshape(-1, 1)

        model.fit(train_X, train_y)
        pred = model.predict(val_X)
        f1 = f1_score(val_y, pred)
        
        if verbose: print(f1)

        score_list[i] = f1

    avg_score = np.mean(list(score_list.values()))
    if verbose: print(f'|_ Average F1 Score: {avg_score}')
    return avg_score
