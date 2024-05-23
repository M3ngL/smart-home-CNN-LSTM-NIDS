import pandas as pd
from sklearn.preprocessing import StandardScaler
from func import getFlow
import threading
from tkinter import messagebox


def judgeFlow(defaultmodel):
    global df, data_dicts
    global illegal_count, normal_count
    # 从csv文件导入data
    file_path = 'output.csv'
    df = pd.read_csv(file_path)
    df.fillna(0, inplace=True)
    data_dicts = df.to_dict(orient='records')
    scaler = StandardScaler()
    # Test the model with data
    scaler.fit(df)
    df = scaler.transform(df)
    predictions = defaultmodel.predict(scaler.fit_transform(df)) # 返回二维数组，如[[9.9999774e-01 2.2898796e-06]]
    illegal_count = 0
    normal_count = 0
    for sample in predictions:
        if sample[0] < 0.4: 
            illegal_count += 1
        else:
            normal_count += 1

    messagebox.showinfo("警告！","检测到有恶意流量！请查看网络和设备状况！")

