# NTLM HTTP Authentication Bruteforce
Original Code and Writeup from: https://dhimasln.medium.com/ntlm-brute-force-attacks-a-practical-lab-simulation-detection-guide-365f5005dfea

Added proxy for better visibility/logging.

## Setup
1. `pip install requests-ntlm`

2. `python ntlm_bruteforce.py -url http://target.tld -u users.txt -p passwords.txt -d 0.5 -t 10`

    - `--proxy` or `-x`
    - `-d`: A delay between attempts to evade rate-limit-based detection.
    - `-t`: The number of concurrent threads to speed up the process.
    - `--user-agent`: Spoof user agent (optional)

## Other tools
- https://github.com/PortSwigger/ntlm-challenge-decoder
