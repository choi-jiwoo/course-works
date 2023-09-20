from datetime import datetime
from typing import Iterable
import pandas as pd
from IPython.display import display, HTML


class ScoreTable:
    
    def __init__(self, columns: Iterable[str]) -> None:
        self.columns = columns
        self.table = pd.DataFrame([], columns=columns)

    def _print_record_table(self) -> None:
        display(HTML(self.table.to_html()))
    
    def record(self, record: dict, print_output: bool=False) -> None:
        timestamp = datetime.now().strftime('%Y%m%d %H:%M:%S')
        try:
            new_record = pd.DataFrame.from_dict(
                record,
                orient='index',
                columns=[timestamp],
            ).T
            self.table = pd.concat([self.table, new_record])
            print('>>> Successfully recorded!')
            if print_output:
                self._print_record_table()
        except Exception as e:
            print(e)
            
    def delete(self, idx: str, print_output: bool=False) -> None:
        try:
            self.table = self.table.drop(idx, axis=0)
            print(f">>> Successfully dropped '{idx}'!")
            if print_output:
                self._print_record_table()
        except Exception as e:
            print(e)
    
    def export_record(self, filename: str) -> None:
        print(f">>> Successfully exported!")
        self.table.to_csv(filename)
    
    def __repr__(self) -> str:
        return f"ScoreTable(columns={self.columns})"