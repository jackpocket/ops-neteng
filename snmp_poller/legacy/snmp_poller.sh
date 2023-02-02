#!/bin/sh

#MANUAL STEPS#
#sudo apt install git -y
#sudo git clone https://github.com/jackpocket/ops-neteng-public.git

#AUTOMATION
#Set env
export DD_SITE="datadoghq.com"
export DD_AGENT_MAJOR_VERSION=7
export DD_INSTALL_ONLY=true

#Remove anything old or remaining
sudo rm ookla*
sudo apt remove datadog-agent -y

#Run this install script
#sudo apt-get update
sudo apt install ssh -y
sudo apt install curl -y
sudo apt install snmp -y
sudo apt install iputils-ping -y

#Install Datadog Agent - hope this does not change
curl -s https://s3.amazonaws.com/dd-agent/scripts/install_script.sh | bash /dev/stdin

#Install relevant integrations
sudo -u dd-agent datadog-agent integration install -t datadog-ping==1.0.2 -r
sudo -u dd-agent datadog-agent integration install -t datadog-speedtest==1.0.0 -r

#Install speedtest utility
sudo wget https://install.speedtest.net/app/cli/ookla-speedtest-1.1.1-linux-x86_64.tgz
sudo tar -zxvf ookla-speedtest-1.1.1-linux-x86_64.tgz
sudo cp speedtest* /usr/local/bin/

#Must copy files now
sudo cp ./snmp_poller/profiles/sophos-xg.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/
sudo cp ./snmp_poller/profiles/brother.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/
sudo cp ./snmp_poller/profiles/zyxel.yaml /etc/datadog-agent/conf.d/snmp.d/profiles/
sudo cp ./snmp_poller/conf/ping/conf.yaml /etc/datadog-agent/conf.d/ping.d/
sudo cp ./snmp_poller/conf/speedtest/conf.yaml /etc/datadog-agent/conf.d/speedtest.d/
sudo cp ./snmp_poller/conf/tcp_check/conf.yaml /etc/datadog-agent/conf.d/tcp_check.d/
sudo cp ./snmp_poller/conf/snmp/conf.yaml /etc/datadog-agent/conf.d/snmp.d/

#Ask user for variables:

echo Site:
read site
echo Community String:
read community_string_v2
echo Auth Key:
read authkey_v3
echo Priv Key:
read privkey_v3
echo Firewall IP:
read firewall_ip
#echo Printer VLAN:
#read printer_vlan
echo Network Management VLAN:
read network_management_vlan

sudo sed -i "s/<SITE>/$site/g" /etc/datadog-agent/conf.d/ping.d/conf.yaml
sudo sed -i "s/<SITE>/$site/g" /etc/datadog-agent/conf.d/speedtest.d/conf.yaml
sudo sed -i "s/<SITE>/$site/g" /etc/datadog-agent/conf.d/tcp_check.d/conf.yaml
sudo sed -i "s/<SITE>/$site/g" /etc/datadog-agent/conf.d/snmp.d/conf.yaml
#
sudo sed -i "s/<FIREWALL_IP>/$firewall_ip/g" /etc/datadog-agent/conf.d/snmp.d/conf.yaml
sudo sed -i "s/<authKey>/$authkey_v3/g" /etc/datadog-agent/conf.d/snmp.d/conf.yaml
sudo sed -i "s/<privKey>/$privkey_v3/g" /etc/datadog-agent/conf.d/snmp.d/conf.yaml
sudo sed -i "s/<COMMUNITY_STRING>/$community_string_v2/g" /etc/datadog-agent/conf.d/snmp.d/conf.yaml
#sudo sed -i "s/<PRINTER_VLAN>/$printer_vlan/g" /etc/datadog-agent/conf.d/snmp.d/conf.yaml
sudo sed -i "s/<NETWORK_MANAGEMENT_VLAN>/$network_management_vlan/g" /etc/datadog-agent/conf.d/snmp.d/conf.yaml

#disable ipv6
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1

#Replace tags with those variables for certain files
#Site
#community_string_v2
#authkey_v3
#privkey_v3
#firewall_ip
#printer_vlan
#network_management_vlan
#Second octet - future
#Enable and restart the agent

sudo systemctl enable datadog-agent
sudo systemctl restart datadog-agent

#Cleanup
sudo rm speedtest*
sudo rm ookla*

#Press YES to accept agreement and run the test at least once
#This must run in order for the check to succeed
sudo -u dd-agent speedtest


#set secrets as env variables
#I would set environment variables locally first and manually and pull them from somewhere (cloud vault/GCP/etc)
#Add a script that will check for any updates to git branch repo currently checked out
# - specify the repo and the folder
#check for SHA if it changed or string output and perform and re-run the poller script again
#use python import git
#use environment variables on the agent machines and leave them there locally.
#How can they survive a reboot? - Linux ENV vars

#Write the python script

#import git
#repo = git.Repo('Path/to/repo')
#repo.remotes.origin.pull()

#Check if something changed:
#
#current = repo.head.commit
#repo.remotes.origin.pull()
#if current != repo.head.commit:
#    print("It changed")
##

#If changes are located, run the installer
