import os
import sys
import ctypes
from waf_blocker import apply_blocklist, cleanup_rules
from waf_monitor import start_monitoring
from waf_gui import start_gui
from waf_utils import load_blocklist

BLOCKLIST_FILE = "blocked_urls.txt"

def is_admin():
    """Check if the program is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def initialize_waf():
    """Initialize the WAF application."""
    print("Initializing WAF...")
    if not is_admin():
        print("This program must be run as administrator. Exiting...")
        sys.exit()

    if not os.path.exists(BLOCKLIST_FILE):
        with open(BLOCKLIST_FILE, "w") as file:
            pass

    blocklist = load_blocklist(BLOCKLIST_FILE)
    if blocklist:
        apply_blocklist(blocklist)
    print("WAF initialized successfully.")

def main():
    """Main function to start the WAF application."""
    try:
        initialize_waf()
        start_monitoring(BLOCKLIST_FILE)
        start_gui()
    except KeyboardInterrupt:
        print("\nWAF interrupted. Cleaning up...")
    finally:
        if is_admin():
            cleanup_rules()

if __name__ == "__main__":
    main()
