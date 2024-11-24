from threading import Thread
import subprocess
import signal
import sys

# Define flags to signal threads to stop
running = True

def run_requests_handler():
    """Run DNS requests handler."""
    global running
    try:
        subprocess.run(["sudo", "python3", "dns_req.py"])
    except Exception as e:
        print(f"[ERROR] DNS requests handler stopped: {e}")

def run_responses_handler():
    """Run DNS responses handler."""
    global running
    try:
        subprocess.run(["sudo", "python3", "dns_resp.py"])
    except Exception as e:
        print(f"[ERROR] DNS responses handler stopped: {e}")

def signal_handler(sig, frame):
    """Handle keyboard interrupt signal to stop threads gracefully."""
    global running
    print("\n[!] Keyboard interrupt detected. Shutting down...")
    running = False
    sys.exit(0)

def main():
    """Run both DNS handlers concurrently."""
    global running

    print("[*] Starting multithreaded DNS handlers...")

    # Set up signal handler for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Create threads
    request_thread = Thread(target=run_requests_handler)
    response_thread = Thread(target=run_responses_handler)

    # Start threads
    request_thread.start()
    response_thread.start()

    # Wait for both threads to finish
    try:
        request_thread.join()
        response_thread.join()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
