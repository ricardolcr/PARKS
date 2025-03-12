from credentials import user_parks, password_parks
from scrapli.driver import GenericDriver
from telnetlib import Telnet

class OLT_PARKS():
    
    def __init__(self, ip_address):

        self.ip_address = ip_address
        
    def connect_via_ssh(self):
        try:
            ssh = GenericDriver(**{
                "host": self.ip_address,
                "auth_username": user_parks,
                "auth_password": password_parks,
                "auth_strict_key": False,
                })

            ssh.open()
            self.ssh_client = ssh

            print(f"Connected to {self.ip_address} via SSH")
        except Exception as e:
            print(f"Failed to connect to {self.ip_address} via SSH: {e}")

    def connect_via_telnet(self):
        try:
            tn = Telnet(self.ip_address, timeout=5)
            tn.write(b"\n")
            tn.read_until(b"Username:")
            tn.write(bytes(user_parks, 'UTF-8'))
            tn.write(b"\n")
            tn.read_until(b"Password:")
            tn.write(bytes(password_parks, 'UTF-8'))
            tn.write(b"\n")
            self.telnet_client = tn
            print(f"Connected to {self.ip_address} via Telnet")
        except Exception as e:
            print(f"Failed to connect to {self.ip_address} via Telnet: {e}")

    def find_prks(self, prks):
        try:
            self.telnet_client.write(bytes(f"show gpon onu {prks} su\n", 'UTF-8'))
            response = self.telnet_client.read_until(b'Unknown command', timeout=0.5).decode("UTF-8")
            print(response)
        except Exception as e:
            print(f"Failed to find PRKS {prks} in {self.ip_address}: {e}")