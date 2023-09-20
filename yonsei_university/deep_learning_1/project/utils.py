import torch
import subprocess
import re
from typing import Iterable
from pprint import pprint


COMMAND = 'nvidia-smi pmon -c 1'
REGEX_PATTERN = r'\d{1,}|(?![A-Z])\w+'

def get_free_gpu(encoding: str='utf-8', verbose: bool=True) -> Iterable[str]:
    input_ = COMMAND.split(' ')
    output = subprocess.run(input_, capture_output=True)
    stdout = output.stdout.decode(encoding)
    process_stat = stdout.split('\n')

    allocated_process = []
    free_gpu_id = set()
    
    for i in process_stat:
        res = re.findall(REGEX_PATTERN, i)
        try:
            gpu_id = int(res[0])
            pid = res[1]
            process = res[2]
        except ValueError:
            continue
        except IndexError:
            free_gpu_id.add(gpu_id)
        else:
            process_info = {
                'pid': pid,
                'gpu_id': gpu_id,
                'process': process,
            }
            allocated_process.append(process_info)
    
    free_gpu_id = list(free_gpu_id)
    
    if verbose:
        print('Allocated process:')
        pprint(allocated_process)
        print('List of free GPU:')
        gpu_list = [f'/device:GPU:{gpu}' for gpu in free_gpu_id]
        pprint(gpu_list)
        
    return free_gpu_id

def assign_gpu(gpu_id: int=0) -> torch.device:
    device = torch.device(f'cuda:{gpu_id}')
    torch.cuda.set_device(device)
    curr_gpu = torch.cuda.current_device()
    print(f'Assigned [/device:GPU:{curr_gpu}]')
    return device