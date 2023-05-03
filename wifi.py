import subprocess

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('UTF-8').split('\n')
profiles = [i.split(":")[1][1:-1]

for i in data if "All user profiles" in i]

for i in profiles:
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', i, 'key=clear']).decode('UTF-8').split('\n')

    result = [b.split(":")[1][1:-1] for b in result if "Key Content" in b]

    try:
        print("{:<30}| {:<}".format(i,result[0]))
    except IndexError:
        print("{:<30}| {:<}".format(i,""))