import logging, os, urllib, csv

DEFAULT_NODE_CSV_URL = "https://docs.google.com/spreadsheets/u/0/d/1LP97xLDsvo8ZIbmMJP5gYHbXMTjrj5NB-zfdhTRnXdo/export?format=csv"
CONF_TEMPLATE = """dev tun
remote {ip}
ifconfig 10.7.0.2 10.7.0.1
redirect-gateway def1

# This might reduce CPU usage and make things faster.
fast-io

# OpenVPN allows us to setup pinging to keep the connection open.
# Some of these are from the Nord default configs.
ping 15
ping-restart 45
ping-timer-rem

# A failed ping sends a SIGUSR1 signal which OpenVPN uses to restart.
# These allow for cleaner restarts.
persist-key
persist-tun

# Compress data passing over the connection to save on bandwidth costs
compress lz4

cipher AES-256-CBC
<secret>
{secret}
</secret>
"""

def create_config_file(ip, secret):
    return CONF_TEMPLATE.format(ip=ip, secret=secret)

def create_config_files(directory, secret_file, node_csv_url=DEFAULT_NODE_CSV_URL):
    if not os.path.exists(directory):
        os.makedirs(directory)

    logging.info("Downloading list of Anexia nodes")
    url_opener = urllib.URLopener()
    csv_path = os.path.join(directory, '../anexia_vpss.csv')
    url_opener.retrieve(node_csv_url, csv_path)

    with open(secret_file) as f:
        secret = f.read().strip()

    server_country = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ip = row['IP'].strip()
            config_content = create_config_file(ip, secret)
            server_country[ip] = row['Country']
            with open(os.path.join(directory, ip + '.ovpn'), 'w') as out:
                out.write(config_content)

    with open(os.path.join(directory, 'servers.txt'), 'a') as f:
        for ip in server_country:
            f.write('|'.join([ip, server_country[ip]]) + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage {0} <directory to create VPNs in> <file containing secret>".format(sys.argv[0])
        sys.exit(1)
    create_config_files(sys.argv[1], sys.argv[2])
