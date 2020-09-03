import os,subprocess
import re
homedir = os.path.expanduser("~")
name = homedir.split("\\")
username = name[len(name)-1]
os.chdir("C:\\Users\\"+username+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu")
os.remove("Programs\\Startup\\svCHost.lnk")
proc = subprocess.Popen("tasklist | findstr svCHost.exe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
taskl = proc.stdout.read() + proc.stderr.read()
PIDs = taskl.decode("UTF-8").split("\n")
for PID in PIDs:
    try:
        kill = re.findall(r"\d+",PID)[0]
        os.system("taskkill /F /PID "+kill)
    except Exception as e:
         pass
try:
    os.remove("C:\\Users\\"+username+"\\Appdata\\local\\Microsoft\\svCHost.exe")
except:
	os.remove("C:\\Users\\"+username+"\\Appdata\\local\\Microsoft\\Office\\svCHost.exe")