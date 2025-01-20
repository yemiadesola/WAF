import socket
import subprocess
from waf_utils import log_action, log_error

HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"
BLOCK_MARKER = "# WAF BLOCK"

def resolve_domain_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        raise ValueError(f"Unable to resolve domain: {domain}")

def add_to_hosts(domain):
    try:
        with open(HOSTS_FILE, "r+") as file:
            lines = file.readlines()
            if any(domain in line for line in lines if BLOCK_MARKER in line):
                return
            file.write(f"127.0.0.1 {domain} {BLOCK_MARKER}\n")
    except Exception as e:
        log_error(f"Error updating hosts file for {domain}: {e}")

def add_to_firewall(domain):
    try:
        ip = resolve_domain_to_ip(domain)
        subprocess.run(
            ["powershell", "-Command",
             f"New-NetFirewallRule -DisplayName 'WAF Block {domain}' -Direction Outbound -Action Block -RemoteAddress {ip}"],
            check=True
        )
    except Exception as e:
        log_error(f"Failed to add firewall rule for {domain}: {e}")

def block_domain(domain):
    add_to_hosts(domain)
    add_to_firewall(domain)
    log_action("Blocked", domain)
