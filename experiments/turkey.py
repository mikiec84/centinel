import dns.resolver
import urllib
import httplib

SEARCH_STRING = "home network testbed will appear at"

class TurkeyExperiment:
    name = "turkey"

    def __init__(self, input_file):
        self.input_file = input_file
        self.results = []

    def get_dns(self, nameserver=None):
        resolver = dns.resolver.Resolver()

        if nameserver:
            resolver.nameservers = [nameserver]

        #XXX: ipv6?
        answers = resolver.query("twitter.com", "A")

        ips = [rdata.address for rdata in answers]

        return ips

    def is_blocked(self, ip):
        response = {}
        headers = {
            "Host" : "twitter.com"
        }

        conn = httplib.HTTPSConnection(ip)
        conn.request("GET", "/feamster/status/452889624541921280", headers=headers)

        resp = conn.getresponse()
        response["status"] = resp.status
        response["reason"] = resp.reason

        headers = dict(resp.getheaders())
        response["headers"] = headers

        body = resp.read()

        response["body"] = body

        conn.close()

        return body.find(SEARCH_STRING) == -1

    def run(self):
        ips = self.get_dns()
        blocked_ips = filter(self.is_blocked, ips)

        print blocked_ips
        
        ips = self.get_dns(nameserver="8.8.8.8")
        blocked_ips = filter(self.is_blocked, ips)

        print blocked_ips
