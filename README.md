# smart-home-CNN-LSTM-NIDS
dataProcessMoudle 部分对初始的数据集进行预处理，其中包括随机抽样、平衡恶意/良性流量样本量的个数等。  <br />
detectMoudle 部分是使用CNN-LSTM神经网络对预处理后的数据集进行训练调优。  <br />
viewDataMoudle 部分是系统的展示模块，使用Tkinter框架构建Windows下的智能家居软件管理系统。
