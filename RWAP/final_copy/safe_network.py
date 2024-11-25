from scapy.all import *
import netfilterqueue

SHOW_ALL = False

def process_packet(packet):
    """
    Process all packets. Decide how to handle DNS and non-DNS traffic.
    """
    scapy_packet = IP(packet.get_payload())  # Convert raw packet to Scapy packet

    if scapy_packet.haslayer(DNS):  # Handle DNS packets
        if scapy_packet[DNS].qr == 0:  # DNS Request
            print(f"[DNS-REQUEST] {scapy_packet.summary()}")
        elif scapy_packet[DNS].qr == 1:  # DNS Response
            print(f"[DNS-RESPONSE] {scapy_packet.summary()}")
            # Modify DNS response as needed (e.g., spoof IP)
    else:  # Handle non-DNS packets
        if SHOW_ALL: print(f"    [NON-DNS PACKET] {scapy_packet.summary()}")
    packet.accept()

def main():
    """Main function to intercept packets."""
    print("[*] Starting packet inspection...")
    queue = netfilterqueue.NetfilterQueue()
    try:
        queue.bind(0, process_packet)
        queue.run()
    except KeyboardInterrupt:
        print("\n[!] Stopping script.")
    finally:
        queue.unbind()

if __name__ == "__main__":
    main()
