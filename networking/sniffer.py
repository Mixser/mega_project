import socket

from struct import unpack

import pcapy


def loop():
    cap = pcapy.open_live('en0', 65565, 1, 0)

    while True:
        header, packet = cap.next()
        eth_header_length = 14

        eth_header_raw = packet[:eth_header_length]
        eth_header = unpack('!6s6sH', eth_header_raw)
        eth_protocol = socket.ntohs(eth_header[2])

        if eth_protocol != 8:
            print "Bad protocol"

        raw_data = packet[eth_header_length:]

        ip_header_raw = raw_data[:20]

        ip_header = unpack('!BBHHHBBHII', ip_header_raw)

        version_ihl = ip_header[0]
        version = version_ihl >> 4
        ip_header_length = (version_ihl & 0xF) * 4
        print '=' * 80
        print 'IP Header'
        print 'Version: ', version, 'IP Header length: ', str(ip_header_length)
        print '=' * 80
        protocol = ip_header[6]

        if protocol == 6:
            tcp_header_raw = raw_data[ip_header_length:ip_header_length + 20]

            tcp_header = unpack('!HHIIBBHHH', tcp_header_raw)

            source = tcp_header[0]
            destination = tcp_header[1]
            sequence = tcp_header[2]

            offset = (tcp_header[5] >> 4)

            h_size = ip_header_length + offset * 4
            print 'TCP Header'
            print 'Source: ', source, 'Destination: ', destination
            print 'Sequence: ', sequence, 'TCP header length: ', offset

            print 'Data:'
            print str(raw_data[h_size:])


        elif protocol == 17:
            print 'UDP'
            # pass
            
            # udp_header_length = 8
            # udp_header_raw = raw_data[ip_header_length:ip_header_length + udp_header_length]

            # udp_header = unpack('!HHHH', udp_header_raw)

            # data = packet[ip_header_length + udp_header_length:]
            # print data
        print '=' * 80
loop()
