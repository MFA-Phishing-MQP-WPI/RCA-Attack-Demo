from scapy.all import *
import netfilterqueue

def process_request(packet):
    """Process outgoing DNS requests."""
    scapy_packet = IP(packet.get_payload())
    
    if scapy_packet.haslayer(DNS) and scapy_packet[DNS].qr == 0:  # DNS request
        query_name = scapy_packet[DNSQR].qname.decode()
        print(f"[DNS REQUEST] {query_name}")
    
    packet.accept()

def main():
    """Main function for processing DNS requests."""
    print("[*] Starting DNS request handler...")
    queue = netfilterqueue.NetfilterQueue()

    try:
        queue.bind(0, process_request)  # Bind to queue 0
        queue.run()
    except KeyboardInterrupt:
        print("\n[!] Stopping DNS request handler.")
    finally:
        queue.unbind()

if __name__ == "__main__":
    main()
