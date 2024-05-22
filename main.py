import pcapy
import dpkt
import socket
import struct
import numpy as np
import requests
import netifaces as ni
import csv
from tqdm import tqdm
import sys
import time


from getProtocol import getProtocol
from getTheSameFlowCount import getTheSameFlowCount
from getPacketsLength import getPacketsLength
from getInOutTraffic import getInOutTraffic


'''
准备阶段
'''
eths = pcapy.findalldevs()
# 打开网络接口，准备捕获数据包
cap = pcapy.open_live(eths[1], 65536, 1, 0)

# 初始化变量
flows = {}
headers, packets  = [], []

# 获取本机所有网络接口
interfaces = ni.interfaces()
eth_name = eths[1].split('_')[1]

for interface in interfaces:
    if eth_name == interface:
        address_info = ni.ifaddresses(interface)  # 选择网络接口的信息
        host_ip = None
        try:
            host_ip = address_info[ni.AF_INET][0]['addr']
        except:
            print('WLAN not connect')
            sys.exit(1)
# host_ip = host_ip.split('.')

'''
抓取阶段
'''

# 循环捕获数据包
for _ in tqdm(range(1000)):
    # 读取数据包
    header, packet = cap.next()
    
    # 如果没有数据包了则退出循环
    if not packet:
        continue
    
    headers.append(header)
    packets.append(packet)

# 关闭网络接口
cap.close()



'''
分类阶段, 根据数据流向分类flow并进一步分类出站/进站流量
'''
# 依据源IP到目的IP进行flow分类
for i in range(len(packets)):
    packet = packets[i]
    header = headers[i]

    # 解析数据包
    eth = dpkt.ethernet.Ethernet(packet)
    ip = eth.data

    # 提取源IP地址和目标IP地址作为流的标识符key
    try:
        src_ip = socket.inet_ntoa(ip.src)
        dst_ip = socket.inet_ntoa(ip.dst)
        flow_key = (src_ip, dst_ip)
    except AttributeError:
        continue
    except OSError:
        continue
    # 去掉源IP和目的IP在同一IP分段的流量（局域网内的流量不纳入检测范围）
    if host_ip.split('.')[:-1] == flow_key[0].split('.')[:-1] and host_ip.split('.')[:-1] == flow_key[1].split('.')[:-1]:
        continue
    
    # 判断是否是新的数据流
    if flow_key not in flows and flow_key[::-1] not in flows:
        if host_ip.split('.')[:-1] == src_ip.split('.')[:-1]: # 出站流量
            flows[flow_key] = [] # 时间顺序导入
            flows[flow_key].append((header, packet, 0)) # 0代表出站，1代表进站流量
        else:
            flows[flow_key[::-1]] = [] # 时间顺序导入
            flows[flow_key[::-1]].append((header, packet, 1))
    elif flow_key in flows and flow_key[::-1] not in flows:
        # 将数据包添加到流中
        flows[flow_key].append((header, packet, 0)) # header, packet = flows[flow_key][i][0], flows[flow_key][i][1]
    elif flow_key not in flows and flow_key[::-1] in flows:
        flows[flow_key[::-1]].append((header, packet, 1)) # header, packet = flows[flow_key][i][0], flows[flow_key][i][1]


'''
提取特征阶段
'''

# 定义data_dicts
data_dicts = []
# 提取各个特征规范化单个数据data
for flow_key in flows:
    the_same_flow_count = { # 用于针对一对IP间单向通信的所有数据包特征提取
        'ack_count' : 0,
        'syn_count' : 0,
        'fin_count' : 0,
        'urg_count' : 0,
        'rst_count' : 0
    }

    # 提前获取同一个流中的所有数据包长度
    packets_length = []
    packets_length = getPacketsLength(flow_key, flows, packets_length)

    # 分离进站出站流量，统计数据包
    incoming = []
    outgoing = []
    outgoing, incoming = getInOutTraffic(flow_key, flows, outgoing, incoming)

    in_packets_length = [len(in_packet[1]) for in_packet in incoming]
    out_packets_length = [len(out_packet[1]) for out_packet in outgoing]
    # 如果使用numpy数组
    if np.isnan(in_packets_length).any() or np.isnan(out_packets_length).any():
        # 处理缺失值
        in_packets_length = in_packets_length[~np.isnan(in_packets_length)]
        out_packets_length = out_packets_length[~np.isnan(out_packets_length)]

    for i in range(len(flows[flow_key])):
        data = {}
        data_header = flows[flow_key][i][0]
        data_packet = flows[flow_key][i][1]
        tmp_eth = dpkt.ethernet.Ethernet(data_packet)

        # 初始化Protocols
        protocols = {
            'HTTP': 0,
            'HTTPS': 0,
            'DNS': 0,
            'Telnet': 0,
            'SMTP': 0,
            'SSH': 0,
            'IRC': 0,
            'TCP': 0,
            'UDP': 0,
            'DHCP': 0,
            'ARP': 0,
            'ICMP': 0,
            }
        
        # 流传递时间，计算两个流量包之间的时差
        if i < len(flows[flow_key]) - 1:
            data["flow duration"] = flows[flow_key][i+1][0].getts()[0] - flows[flow_key][i][0].getts()[0] + (flows[flow_key][i+1][0].getts()[1] - flows[flow_key][i][0].getts()[1]) / 10**6
        else: # 最后一组流量采用前一组流量的duration
            data["flow duration"] = flows[flow_key][i][0].getts()[0] - flows[flow_key][i-1][0].getts()[0] + (flows[flow_key][i][0].getts()[1] - flows[flow_key][i-1][0].getts()[1]) / 10**6

        # header 长度
        data['Header_Length'] = (struct.unpack('B', data_packet[0:1])[0] & 0x0F) * 4

        # TTL
        if isinstance(tmp_eth.data, dpkt.ip.IP):
            data['Duration'] = tmp_eth.data.ttl
        else:
            data['Duration'] = None

        # Rate of packet transmission in a flow
        data['Rate'] = len(data_packet) / data['Duration']

        # FIN/SYN/RST/PUSH/ACK/ECE/CWR flag value
        if isinstance(tmp_eth.data, dpkt.ip.IP) and isinstance(tmp_eth.data.data, dpkt.tcp.TCP):
            tcp = eth.data.data
            try:
                flag = tcp.flags
            except AttributeError:
                break
            data['fin_flag_number'] = flag & dpkt.tcp.TH_FIN
            data['syn_flag_number'] = flag & dpkt.tcp.TH_SYN
            data['rst_flag_number'] = flag & dpkt.tcp.TH_RST
            data['push_flag_number'] = flag & dpkt.tcp.TH_PUSH
            data['ack_flag_number'] = int(flag & dpkt.tcp.TH_ACK == 16)
            data['ece_flag_number'] = flag & dpkt.tcp.TH_ECE
            data['cwr_flag_number'] = flag & dpkt.tcp.TH_CWR

        # Number of packets with ack/syn/fin/urg/rst flag set in the same flow
        res = getTheSameFlowCount(flow_key, flows, data_packet, the_same_flow_count)
        data.update(res)

        # 使用的协议
        res = getProtocol(tmp_eth, protocols)
        data.update(res)

        # Summation of packets lengths in flow
        data['Tot sum'] = sum(packets_length)

        # Minimum/Maximum/Average/Standard deviation of packet length in the flow
        data['Min'] = max(packets_length)
        data['Max'] = min(packets_length)
        data['AVG'] = sum(packets_length) / len(packets_length)
        data['Std'] = np.std(packets_length)

        # Packet's length
        data['Tot size'] = len(data_packet)


        # The number of packets in the flow
        data['Number'] = len(flows[flow_key])


        # (Average of the lengths of incoming packets in the flow + Average of the lengths of outgoing packets in the flow) ** 0.5
        try:
            if len(in_packets_length) or len(out_packets_length):
                data['Magnitue'] = (sum(in_packets_length) / len(in_packets_length) + sum(out_packets_length) / len(out_packets_length)) ** 0.5
            else:
                data['Magnitue'] = 0 
        except ZeroDivisionError:
            data['Magnitue'] = 0 
        # (Variance of the lengths of incoming packets in the flow + Variance of the lengths of outgoing packets in the flow) ** 0.5
        try:
            if len(in_packets_length) or len(out_packets_length):
                data['Radius'] = (np.var(in_packets_length) + np.var(out_packets_length)) ** 0.5
            else:
                data['Radius'] = 0 
        except:
                data['Radius'] = 0 
    
        # (Covariance of the lengths of incoming packets in the flow + Covariance of the lengths of outgoing packets in the flow) ** 0.5
        try:
            if np.count_nonzero(in_packets_length)>=2 or np.count_nonzero(out_packets_length) >= 2:
                data['Covariance'] = (np.cov(in_packets_length) + np.cov(out_packets_length)) ** 0.5
            else:
                data['Covariance'] = 0
        except:
            data['Covariance'] = 0 
        
        # (Variance of the lengths of incoming packets in the flow + Variance of the lengths of outgoing packets in the flow) ** 0.5
        try:
            var_out = np.var(out_packets_length, skipna=True)
            if np.any(np.isclose(var_out, 0)):  # 检查是否有接近零的值
                data['Variance'] = 0
            else:
                data['Variance'] = np.var(in_packets_length, ddof=1) / var_out
        except:
            data['Variance'] = 0 

        # Number of incoming packets * Number of outgoing packets
        try:
            data['Weight'] = len(in_packets_length) * len(out_packets_length)
        except:
            data['Weight'] = 0 
        
        # print(data)
        data_dicts.append(data)

'''
导出为CSV文件阶段
'''

# 获取所有字典的键（即特征值），并去重，确保作为表头不重复
headers = list(data)

# 指定输出CSV文件的路径
csv_file_path = "output.csv"

# 使用csv.writer写入数据
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    
    # 写入表头
    writer.writeheader()
    # 写入每个字典的数据行
    for data_dict in data_dicts:
        writer.writerow(data_dict)

