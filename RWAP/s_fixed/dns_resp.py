from scapy.all import *
import netfilterqueue

def process_response(packet):
    """Process incoming DNS responses."""
    scapy_packet = IP(packet.get_payload())
    
    if scapy_packet.haslayer(DNS) and scapy_packet[DNS].qr == 1:  # DNS response
        rrname = scapy_packet[DNSRR].rrname.decode()
        rdata = scapy_packet[DNSRR].rdata
        print(f"[DNS RESPONSE] {rrname} -> {rdata}")
    
    packet.accept()

def main():
    """Main function for processing DNS responses."""
    print("[*] Starting DNS response handler...")
    queue = netfilterqueue.NetfilterQueue()

    try:
        queue.bind(1, process_response)  # Bind to queue 1
        queue.run()
    except KeyboardInterrupt:
        print("\n[!] Stopping DNS response handler.")
    finally:
        queue.unbind()

if __name__ == "__main__":
    main()
