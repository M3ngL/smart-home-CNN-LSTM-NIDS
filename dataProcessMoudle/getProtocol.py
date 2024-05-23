import dpkt
import pcapy
def getProtocol(eth, protocols):
    ip = eth.data
    # 判断传输层协议
    if isinstance(ip.data, dpkt.tcp.TCP):
        protocols['TCP'] += 1
        # 进一步判断应用层协议
        tcp = ip.data
        if tcp.dport == 80:
            protocols['HTTP'] += 1
        elif tcp.dport == 443:
            protocols['HTTPS'] += 1
        elif tcp.dport == 25:
            protocols['SMTP'] += 1
        elif tcp.dport == 23:
            protocols['Telnet'] += 1
        elif tcp.dport == 22:
            protocols['SSH'] += 1
        elif tcp.dport == 6667:
            protocols['IRC'] += 1
        elif tcp.dport == 67 or tcp.dport == 68:
            protocols['DHCP'] += 1

    elif isinstance(ip.data, dpkt.udp.UDP):
        protocols['UDP'] += 1
        # 进一步判断应用层协议
        udp = ip.data
        if udp.dport == 53:
            protocols['DNS'] += 1
    elif isinstance(eth.data, dpkt.icmp.ICMP):
        protocols['ICMP'] += 1
    elif eth.type == dpkt.ethernet.ETH_TYPE_ARP:
        protocols['ARP'] += 1

    return protocols
if __name__ =="__main__":
        import pcapy
        import dpkt
        # 初始化协议计数器
        protocols = {
            'TCP': 0,
            'UDP': 0,
            'HTTP': 0,
            'HTTPS': 0,
            'DNS': 0,
            'Telnet': 0,
            'SMTP': 0,
            'SSH': 0,
            'IRC': 0,
            'ICMP': 0,
            'IP': 0,
            'ARP': 0,
            'LLC': 0
            }
        eths = pcapy.findalldevs()
        # 打开网络接口，准备捕获数据包
        cap = pcapy.open_live(eths[2], 65536, 1, 0)
        # 读取数据包
        for _ in range(5):
            header, packet = cap.next()
            # 解析数据包
            eth = dpkt.ethernet.Ethernet(packet)

            protocols = getProtocol(eth, protocols)
            print(protocols)