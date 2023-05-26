import os
import subprocess

#	git config --global --add safe.directory /home/datadog/ops-neteng-public

os.chdir("/home/datadog/ops-neteng-public")

result = subprocess.check_output(["sudo", "git", "pull"])

coolresult = (str(result))

if "Already up to date." in coolresult:
    pass
else:
    #print("Need to execute the installer")
    os.system('/usr/bin/python3 /home/datadog/ops-neteng-public/backup_speedtest/backup_speedtest_installer.py')
