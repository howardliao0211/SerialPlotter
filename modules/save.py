from datetime import datetime
import os

def save_log(log: str, dir: str, filename: str):
    w_type = 'w'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    if os.path.exists(os.path.join(dir, filename)):
        w_type = 'a'
    
    with open(os.path.join(dir, filename), w_type) as f:
        f.write(log)

if __name__ == '__main__':
    save_log('test_string', 'logs', 'test1')