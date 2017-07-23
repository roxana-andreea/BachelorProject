from dnsimple import DNSimple
import ipgetter

# Use email/api_token credentials
dns = DNSimple(email='cristianlupu@gmail.com', api_token='LMpfhsnUYhZQcWdGqG0x2B6LI4yidd5q')
domains = dns.domains()

# print(domains)

records = dns.records('lupu.online')
# print(records)

IP_ADDRESS = ipgetter.myip()
# print(IP_ADDRESS)
DOMAIN_ID=247223
RECORD_ID=5940312
DATA = {
    'name':'rpi',
    'content': IP_ADDRESS,
    'ttl': '3600',
    'prio': None,
}

dns.update_record(DOMAIN_ID, RECORD_ID, DATA)
