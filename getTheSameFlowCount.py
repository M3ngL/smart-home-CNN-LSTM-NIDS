import dpkt

def getTheSameFlowCount(now_flow_key, flows, packet, the_same_flow_count):
    for _ in range(len(flows[now_flow_key])):
        eth = dpkt.ethernet.Ethernet(packet)
        tcp = eth.data.data
        try:
            the_same_flow_count['ack_count'] += tcp.flags & dpkt.tcp.TH_ACK == dpkt.tcp.TH_ACK
            the_same_flow_count['syn_count'] += tcp.flags & dpkt.tcp.TH_SYN == dpkt.tcp.TH_SYN
            the_same_flow_count['fin_count'] += tcp.flags & dpkt.tcp.TH_FIN == dpkt.tcp.TH_FIN
            the_same_flow_count['urg_count'] += tcp.flags & dpkt.tcp.TH_URG == dpkt.tcp.TH_URG
            the_same_flow_count['rst_count'] += tcp.flags & dpkt.tcp.TH_RST == dpkt.tcp.TH_RST
        except AttributeError:
            continue
    return the_same_flow_count

if __name__== "__main__":
    import dpkt
    getTheSameFlowCount((0,0),0,0,0)