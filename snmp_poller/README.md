#### Step 1. Locate a suitable hypervisor desktop and enable Hyper-V
#### Step 2. Build an Ubuntu server VM, as light weight as possible
#### Step 3. Login to VM, set environment variables and check out repo
#### Step 4. Run the installer
#### Step 5. A few manual steps to make sure we have "automation"
#### Step 6. Improve upon this process

REQUIRED - Place all required environment variables into /etc/environment:

sudo git clone https://github.com/jackpocket/ops-neteng-public.git

cd ops-neteng-public

python3 snmp_poller/snmp_poller

add cronjob
add line to /etc/sudoers

CHECKS:
sudo -u dd-agent datadog-agent check snmp
sudo -u dd-agent datadog-agent check agent
sudo -u dd-agent datadog-agent check speedtest
sudo -u dd-agent datadog-agent check ping
sudo -u dd-agent datadog-agent check tcp_check
