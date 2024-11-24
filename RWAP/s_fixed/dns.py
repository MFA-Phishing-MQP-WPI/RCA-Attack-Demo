from threading import Thread
import subprocess

# Define functions to run the two handlers
def run_requests_handler():
    subprocess.run(["sudo", "python3", "dns_req.py"])

def run_responses_handler():
    subprocess.run(["sudo", "python3", "dns_resp.py"])

def main():
    """Run both handlers concurrently."""
    print("[*] Starting multithreaded DNS handlers...")
    
    # Create threads
    request_thread = Thread(target=run_requests_handler)
    response_thread = Thread(target=run_responses_handler)

    # Start threads
    request_thread.start()
    response_thread.start()

    # Wait for both threads to finish
    request_thread.join()
    response_thread.join()

if __name__ == "__main__":
    main()
