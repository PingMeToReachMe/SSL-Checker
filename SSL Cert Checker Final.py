# Libraries/Tools
import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse

# User input functions
def get_log_preference():
    while True:
        save_log = input("\nAre you backing up the information in a log file? (yes/no): ").strip().lower()
        if save_log == 'yes':
            log_path = input("Enter path for the log file (e.g., ssllog.txt) or type 'cancel' to skip: ").strip()
            if log_path.lower() == 'cancel':
                print("Okay, log file will not be used.")
                return None
            return log_path
        elif save_log == 'no':
            return None
        else:
            print("Please enter 'yes' or 'no'.")

def get_user_input():
    return input("\nEnter website, or type 'file' to load from .txt, or 'exit' to quit: ").strip()

def get_file_path():
    return input("Enter path to your .txt file (e.g., domains.txt): ").strip()

# Retrieving certificate information
def get_certificate_info(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            return ssock.getpeercert()


def check_ssl_expiry(hostname, log_file=None, stats=None):
    print(f"\nChecking SSL certificate for: {hostname}")
    try:
        cert = get_certificate_info(hostname)
        issuer = dict(x[0] for x in cert['issuer'])
        subject = dict(x[0] for x in cert['subject'])
        not_after = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
        days_left = (not_after - datetime.utcnow()).days

# Certificate results and output
        result = [
            f"Website: {hostname}",
            f" Subject: {subject.get('commonName', 'N/A')}",
            f" Issuer: {issuer.get('commonName', 'N/A')}",
            f" Expiration Date: {not_after}",
            f" Days Until Expiration: {days_left} days"
        ]

        if days_left < 0:
            result.append(" Status: Expired")
            if stats is not None:
                stats['failed'] += 1
        elif days_left < 30:
            result.append(" Status: Expires Soon")
            if stats is not None:
                stats['failed'] += 1
        else:
            result.append(" Status: Valid")
            if stats is not None:
                stats['successful'] += 1

        output = "\n".join(result)
        print(output)

        if log_file:
            with open(log_file, 'a') as f:
                f.write(f"\n--- {datetime.now()} ---\n")
                f.write(output + "\n")

    except Exception as e:
        error_message = f"Error retrieving certificate for {hostname}: {e}"
        print(error_message)
        if stats is not None:
            stats['failed'] += 1
        if log_file:
            with open(log_file, 'a') as f:
                f.write(f"\n--- {datetime.now()} ---\n{error_message}\n")

if __name__ == "__main__":
    log_file = get_log_preference()

#Stat summary
    stats = {
        'total': 0,
        'successful': 0,
        'failed': 0
    }

    while True:
        user_input = get_user_input()

        if user_input.lower() == 'exit':
            print("\nIf a log was used, a summary will be added. Exiting.")

#Stat summary added to log once user exits
            if log_file:
                with open(log_file, 'a') as f:
                    f.write(f"\n--- {datetime.now()} ---\n")
                    f.write("--- Summary ---\n")
                    f.write(f"Total domains checked: {stats['total']}\n")
                    f.write(f"Successful checks: {stats['successful']}\n")
                    f.write(f"Failed checks: {stats['failed']}\n")

            break

        elif user_input.lower() == 'file':
            file_path = get_file_path()
            try:
                with open(file_path, 'r') as file:
                    domains = [line.strip() for line in file if line.strip()]
                    for domain in domains:
                        if domain.startswith("http"):
                            domain = urlparse(domain).netloc
                        stats['total'] += 1
                        check_ssl_expiry(domain, log_file, stats)
            except FileNotFoundError:
                print("File not found.")

        else:
            domain = urlparse(user_input).netloc if user_input.startswith("http") else user_input
            stats['total'] += 1
            check_ssl_expiry(domain, log_file, stats)