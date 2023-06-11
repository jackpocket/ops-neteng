import os
import fileinput
import subprocess

os.system('sudo systemctl stop datadog-agent')

#TODO this does not work - using source is the only option
#os.system('source /etc/environment')
#TODO moving this to a manual step for now

# Get DD environment variables
dd_api_key = os.getenv('DD_API_KEY')
dd_agent_major_version = os.getenv('DD_AGENT_MAJOR_VERSION')
dd_install_only = os.getenv('DD_INSTALL_ONLY')
dd_weburl = os.getenv('DD_WEBURL')

# Get JP environment variables
site = os.getenv('BACKUP_SITE')

# disable ipv6
os.system('sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1')
os.system('sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1')
os.system('sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1')

# Install some packages
try:
    os.system('sudo apt install -y ssh')
    os.system('sudo apt install -y curl')
    os.system('sudo apt install -y net-tools')

except:
    exit("Failed to install the packages")

# Install Datadog Agent - hope this does not change
#Old installer
#os.system('curl -s https://s3.amazonaws.com/dd-agent/scripts/install_script.sh | bash /dev/stdin')

#New Installer
os.system('curl -s https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh | bash /dev/stdin')

# Install relevant integrations
os.system('sudo -u dd-agent datadog-agent integration install -t datadog-speedtest==1.0.0 -r')

# Install speedtest utility
os.system('sudo wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-x86_64.tgz')
os.system('sudo tar -zxf ookla-speedtest-1.2.0-linux-x86_64.tgz')
os.system('sudo cp speedtest* /usr/local/bin/')

# Copy templated files
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/backup_speedtest/conf.yaml /etc/datadog-agent/conf.d/speedtest.d/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/tcp_check/conf.yaml /etc/datadog-agent/conf.d/tcp_check.d/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/snmp/conf.yaml /etc/datadog-agent/conf.d/snmp.d/')
os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/conf/agent/datadog.yaml /etc/datadog-agent/')

os.system('sudo cp /home/datadog/ops-neteng-public/snmp_poller/github_pull_backuptest.py /opt/')
os.system('sudo chmod +x /opt/github_pull_backuptest.py')

# Give each file a variable
dd_agent_conf = '/etc/datadog-agent/datadog.yaml'
dd_snmp_conf = '/etc/datadog-agent/conf.d/snmp.d/conf.yaml'
dd_ping_conf = '/etc/datadog-agent/conf.d/ping.d/conf.yaml'
dd_speedtest_conf = '/etc/datadog-agent/conf.d/speedtest.d/conf.yaml'
dd_tcp_check_conf = '/etc/datadog-agent/conf.d/tcp_check.d/conf.yaml'

#WORKS - callcheck but we do run below
#subprocess.check_output(f'sudo sed -i s/BACKUP_SITE/{site}/g /etc/datadog-agent/conf.d/ping.d/conf.yaml', shell=True)

subprocess.run(f'sudo sed -i s/BACKUP_SITE/{site}/g /etc/datadog-agent/conf.d/speedtest.d/conf.yaml', shell=True)

#subprocess.run(f'sudo sed -i s/BACKUP_SITE/{site}/g /etc/datadog-agent/conf.d/snmp.d/conf.yaml', shell=True)

subprocess.run(f'sudo sed -i s/BACKUP_SITE/{site}/g /etc/datadog-agent/datadog.yaml', shell=True)

subprocess.run(f'sudo sed -i s/DD_WEBURL/{dd_weburl}/g /etc/datadog-agent/datadog.yaml', shell=True)

subprocess.run(f'sudo sed -i s/DD_API_KEY/{dd_api_key}/g /etc/datadog-agent/datadog.yaml', shell=True)

os.system('sudo systemctl enable datadog-agent')
os.system('sudo systemctl restart datadog-agent')

# #Cleanup
os.system('sudo rm speedtest*')
os.system('sudo rm ookla*')

# #Press YES to accept agreement and run the test at least once
# #This must run in order for the check to succeed
os.system('sudo -u dd-agent speedtest --accept-license')
