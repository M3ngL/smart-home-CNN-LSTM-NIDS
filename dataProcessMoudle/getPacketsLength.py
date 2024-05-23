def getPacketsLength(flow_key, flows, packets_length):
    for i in range(len(flows[flow_key])):
        data_packet = flows[flow_key][i][1]
        packets_length.append(len(data_packet))

    return packets_length

