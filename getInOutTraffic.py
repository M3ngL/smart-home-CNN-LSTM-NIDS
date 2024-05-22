
def getInOutTraffic(flow_key, flows, outgoing, incoming):
    for i in range(len(flows[flow_key])):
        data_header = flows[flow_key][i][0]
        data_packet = flows[flow_key][i][1]
        if flows[flow_key][i][2] == 0:
            incoming.append((data_header, data_packet))
        else:
            outgoing.append((data_header, data_packet))

    return outgoing, incoming