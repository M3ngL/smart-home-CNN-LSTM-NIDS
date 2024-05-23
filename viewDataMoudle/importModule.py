# importModel.py

from tkinter import filedialog
from tensorflow.keras.models import load_model as tf_keras_models_load_model
from pandas import read_csv as pd_read_csv
from tkinter import messagebox



model = None
df = None
def importModel():
    global model
    folder_path = filedialog.askdirectory()
    if folder_path:
        # 加载 SavedModel
        messagebox.showinfo("","The model is being loaded...")
        try:
            model = tf_keras_models_load_model(folder_path)
        except:
            messagebox.showinfo("Warning","Please choose a model folder!")
    else:
        messagebox.showinfo("Warning","The path dose not exit!")


def importData():
    global df
    file_path = filedialog.askopenfilename()
    try:
        # 导入CSV文件并转换为DataFrame
        df = pd_read_csv(file_path)
    except FileNotFoundError:
        messagebox.showinfo("Warning","File not found!")
    except Exception as e:
        messagebox.showinfo("Warning","Error:", e)


def importdefaultModel():
    # 导入默认模型
    defaultmodel = None
    folder_path = 'saved_model'
    try:
        defaultmodel = tf_keras_models_load_model(folder_path)
    except:
        messagebox.showinfo("Warning","Default model folder is gone!")
    return defaultmodel
