# This script removes any existing VPN configuration files that might exist. It
# then downloads information about VPN nodes from NordVPN and creates new VPN
# configuration files. This script should be run regularly to ensure VPN nodes
# are kept up-to-date.
rm -rf ./vpn_config
python vpn.py --create-nordvpn-configs --create-config ./vpn_config
