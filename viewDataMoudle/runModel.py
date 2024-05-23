# runModel.py

def run():
    from Design.visualTkinter.importModule import model,df
    from sklearn.preprocessing import MinMaxScaler
    if model:
        # 创建 MinMaxScaler 对象
        scaler = MinMaxScaler()
        # Test the model with data
        predictions = model.predict(scaler.fit_transform(df)) # 返回二维数组，如[[9.9999774e-01 2.2898796e-06]]
        if predictions[0][0] > 0.5: 
            print("","Normal traffic")
        else:
            print("","Illegal traffic")
    else:
        print("Warning","No model loaded yet.")

if __name__ == "__main__":
    run()