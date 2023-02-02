import csv
#Pricing codes
#Monthly - LICNCCPRO1MO
#Annual - LICNCCPRO1YR

licensing_costs = {'lic_1mo_pro': 4.24, 'lic_1yo_pro': 32.99}
total_dollars = 0
total_monthly_lics = 0

def days_to_licenses(days_to_buy):
    #print(days_to_buy % 30)
    months = days_to_buy / 30
    days = days_to_buy % 30
    # Calculating years
    years = days_to_buy // 365
    # Calculating months
    months = (days_to_buy - years * 365) // 30
    # Calculating days
    days = (days_to_buy - years * 365 - months * 30)
    # Displaying results
    #print("Years = ", years)
    #print("Months = ", months)
    #print("Days = ", days)

    buy_string = "Please buy " + str(months) + "monthly licences"
    #return int(months)
    #return months

    return months

#Please pass these in later! Argparse is yur friend!
devices_list_csv = '/Users/vlad.bekker/code/sophos_ssh/2022-03-15_license-inventory-device-list.csv'
licenses_list_csv = '/Users/vlad.bekker/code/sophos_ssh/2022-03-15_license-inventory-license-list.csv'
devices_dict = {}
licenses_dict = {}

#First create the devices dictionary
with open(devices_list_csv) as devices_csv_file:
    devices_csv = csv.reader(devices_csv_file, delimiter=',')
    for device_row in devices_csv:
        if 'Device' not in device_row[0]:
            #print(device_row[0])
            devices_dict[device_row[0]] = {'type':device_row[1], 'site':device_row[2], 'model':device_row[3], 'SN':device_row[4], 'mac':device_row[5], 'in_use':device_row[8], 'exp_date':device_row[10], 'lic_info':device_row[11]}

#Then create the Non-Expired licences dictionary
#Please note: The "Show expired licensing" option should be turned off for more accurate data
#We are not checking for state just yet in the code


with open(licenses_list_csv) as lic_csv_file:
    licenses_csv = csv.reader(lic_csv_file, delimiter=',')
    for license_row in licenses_csv:
        if 'License Key' not in license_row[0]:
            if 'Inactive' not in license_row[2]:
                if devices_dict[license_row[7]]:
                    #print("Found a match      -    " + license_row[7])
                    licenses_dict[license_row[7]] = {'key': license_row[0], 'service': license_row[1], 'state': license_row[2], 'exp_date': license_row[3], 'rem_days': license_row[4], 'site': license_row[5]}

#We have both devices_dict and licenses_dict with the key of the device name, which we will rename accordingly

# for item in licenses_dict.items():
#     print(item)
# exit()
days_list = []
count=0
#num_days = 0
for row in devices_dict.items():
    mac = row[0]
    try:
        #print(mac, row[1])
        num_days = int(licenses_dict[mac]['rem_days'].split(' ')[0])
        #print(mac, licenses_dict[mac]['key'], licenses_dict[mac]['state'], licenses_dict[mac]['rem_days'] + " left")
        days_list.append(num_days)
    except:
        count += 1
        num_lics = days_to_licenses(max(days_list))
        #print('--------------------------------' + mac + " License for device not found. Let's purchase ASAP!")
        print(mac + " Requires a NEW license! Please buy " + str(days_to_licenses(max(days_list))) + " monthly licenses. Cost: $"+ str(num_lics*licensing_costs['lic_1mo_pro']))
        total_dollars += num_lics*licensing_costs['lic_1mo_pro']
        total_monthly_lics += num_lics
        #print(total_dollars)

print("We have " + str(count) + " device(s) without an active license")

#print(days_list)
#print('\n')
print("We have active devices with " + str(max(days_list)) + " days of licensing left. It would make sense to get the expirations dates as close as possible... Here is the breakdown:" )

#Let's iterate over the dict again and do math of how many licences we should buy:

for mac in licenses_dict:
    #print(mac)
    rem_days = int(licenses_dict[mac]['rem_days'].split()[0])
    days_we_need_to_buy = max(days_list) - rem_days
    num_lics = days_to_licenses(days_we_need_to_buy)
    #print(days_we_need_to_buy)
    try:
        #print(mac, licenses_dict[mac]['key'], licenses_dict[mac]['state'], day_to_licenses(days_we_need_to_buy))
        #WORKS(below)
        #print(mac, licenses_dict[mac]['key'], licenses_dict[mac]['state'], days_we_need_to_buy, days_to_licenses(days_we_need_to_buy))
        saving_this = (mac, licenses_dict[mac]['key'], licenses_dict[mac]['state'], days_we_need_to_buy, num_lics)
        if num_lics != 0:
            print(mac + " License is active, Please buy " + str(num_lics) + " monthly licenses. Cost: $" + str(num_lics*licensing_costs['lic_1mo_pro']))
        #print(day_to_licenses(days_we_need_to_buy))
        total_monthly_lics += num_lics
        total_dollars += num_lics*licensing_costs['lic_1mo_pro']
        #print(total_monthly_lics)
        #print(total_dollars)
    except:
        #print('--------------------------------' + mac + " License for device not found. Let's purchase ASAP!")
        #This cannot happen, these are all active licenses
        print(" This text will probably never be reached ")

total_dollars = "{:.2f}".format(total_dollars)
print("Total Monthly licenses: " + str(total_monthly_lics))
print("Total Cost: $" + str(total_dollars))