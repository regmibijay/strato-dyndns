from strato_dyndns.clients import StratoClient

strato = StratoClient()

strato.set_authentication(username="bijayregmi", password="mypassword")

strato.set_domain(domain="cdn.regdelivery.de")

strato.set_ip_addresses(ip_addresses=["192.168.0.1", "2a01:1493:14g4:116"])

print(strato.is_initialized())

print(strato.update_url())
