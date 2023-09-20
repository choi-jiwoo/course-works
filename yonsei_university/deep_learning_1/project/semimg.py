import pandas as pd
import numpy as np
import json
import os
import cv2
import matplotlib.pyplot as plt
from typing import Optional


IMAGE_DIR = 'RCore(MH).CSV'
IMG_PATH = f'dataset/image/{IMAGE_DIR}/Main/'
CROPPED_PATH = 'cropped'
AREA_UPPERBOUND = 500_000

class SemImage:
    
    with open('dataset/data_container.json') as f:
        sem_img_name_list = json.load(f)
        
    posi_mh_main = pd.read_csv('dataset/posi_mh_main.csv')
    
    def __init__(self, type_: str='hole', sem_no: Optional[int]=None,
                 extension: str='jpg') -> None:
        self.type_ = type_.upper()
        self.sem_no = sem_no if sem_no is not None else self._get_random_sem_no()
        self.extension = extension.upper()
        self.img = self._get_sem_img()
        self.bbox = self.img.copy()
    
    def info(self, verbose=True) -> pd.Series:
        watchlist = [
            'group',
            'design',
            'duty',
            'pitch',
            'TARGET',
            'CD',
            'Error',
        ]
        sem_data = SemImage.posi_mh_main.query(f'SEM_No == {self.sem_no}')
        watchlist_metadata = sem_data[watchlist].squeeze(axis=0)
        if verbose:
            print(f'SEM_No: {self.sem_no:05d}')
            for k, v in watchlist_metadata.items():
                print(f'  |__{k}: {v}')
        return watchlist_metadata
        
    def _get_random_sem_no(self) -> int:
        sem_type_list = SemImage.sem_img_name_list[self.type_]
        ran_sem_filename = np.random.choice(sem_type_list)
        ran_sem_no = int(ran_sem_filename.split('.')[0])
        return ran_sem_no
    
    def _get_sem_img(self) -> np.ndarray:
        img_full_path = f'{IMG_PATH}/{self.sem_no:05d}.{self.extension}'
        img = cv2.imread(img_full_path)
        return img
    
    def plot(self, bbox: bool=False, figsize: tuple=(8, 5)) -> None:
        try:
            print(f'SEM No: {self.sem_no}')
            output_img = self.bbox if bbox else self.img
            plt.figure(figsize=figsize)
            plt.imshow(output_img)
        except Exception as e:
            print(e)
    
    def transform(self, thresh: int=127, kernel_size=(3, 3),
                  morph_type='open') -> np.ndarray:
        morph = cv2.MORPH_OPEN if morph_type == 'open' else cv2.MORPH_CLOSE
        blur = cv2.GaussianBlur(self.img, (9, 9), 0)
        bw = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        transformed = cv2.morphologyEx(bw, morph, kernel, iterations=1)
        return transformed
        
    def get_contour(self, bw_img: np.ndarray) -> tuple:
        transformed = bw_img[:, :, 0] if bw_img.shape[2] == 3 else bw_img
        contours, _ = cv2.findContours(
            transformed,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return contours
    
    def crop(self, contours: tuple,
             design_threshold: float=0.06, save: bool=False) -> None:
        sem_no_dir = f'{CROPPED_PATH}/{self.sem_no:05d}'
        try: os.mkdir(sem_no_dir)
        except FileExistsError as e: print(e)
        
        sem_metadata = self.info(verbose=False)
        sem_design = sem_metadata['design']

        area_list = [cv2.contourArea(c) for c in contours]
        max_area = np.max(area_list)
        ratio_list = [area/max_area for area in area_list]
        ratio_std = np.std(ratio_list)
        
        if sem_design > design_threshold:
            n, bins = np.histogram(ratio_list, bins=2)
            threshold = sorted(ratio_list)[-int(n[1])]
        else:
            threshold = 0
        roi_num = 0
        
        for i, c in enumerate(contours):
            area = area_list[i]
            area_ratio = ratio_list[i]
            if area < AREA_UPPERBOUND:
                if ratio_std <= 0.1:
                    conditional = True
                else:
                    conditional = area_ratio >= threshold

                if conditional:
                    x, y, w, h = cv2.boundingRect(c)
                    roi = self.img[y:y + h, x:x + w]
                    if save: cv2.imwrite(f'{sem_no_dir}/roi_{roi_num}.png', roi)
                    roi_num += 1

    def __repr__(self) -> str:
        return f"SemImage(sem_no={self.sem_no}, extension='{self.extension}')"