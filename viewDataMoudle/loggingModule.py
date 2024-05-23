
import subprocess
import os
import time


def catLog():
    filePath = 'logging.txt'
    if os.path.exists(filePath):
        subprocess.Popen(['notepad.exe', filePath])
    else:
        with open(filePath, 'w') as file:
            pass
        subprocess.Popen(['notepad.exe', filePath])


def cleanLog():
    T = time.time()
    local_time = time.localtime(T)
    formatted_date = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    with open('logging.txt', 'w') as file:
        file.write(f'Rewrite log file at {formatted_date}')
        file.write("\n")  # 在一行结束时添加换行符
        line_length = 150  # 设定线的长度
        for _ in range(line_length):
            file.write("-")
        file.write("\n")  # 在一行结束时添加换行符


def enterLog(log):
    filePath = 'logging.txt'
    if os.path.exists(filePath):
        pass
    else:
        with open(filePath, 'w') as file:
            pass        
    with open(filePath, 'a') as file:
        file.write(log)
        file.write("\n")  # 在一行结束时添加换行符
        line_length = 150  # 设定线的长度
        for _ in range(line_length):
            file.write("-")
        file.write("\n")  # 在一行结束时添加换行符


def ProduceLog():
    log = None
    

    return log


if __name__ == "__main__":
    catLog()
    # cleanLog()