from scapy.all import *
import netfilterqueue

def process_packet(packet):
    """Process packets and print them without modification."""
    scapy_packet = IP(packet.get_payload())  # Convert raw packet to Scapy packet
    print(f"[PACKET] {scapy_packet.summary()}")  # Print the packet summary

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
