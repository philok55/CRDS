# REORDERINGS EXECUTED: 0

"""
Lab 3 - Chat Room (Client)
NAME: Philo Decroos
STUDENT ID: 11752262
DESCRIPTION:
This file is a client for a chatroom. It can connect to a chatroom server
and send and recieve messages to and from other users. To do so it uses a
user interface provided by gui.py. Every command put into the gui is sent
to the server and every message recieved by the socket is printed to the
users screen.
"""
fromguiimportMainWindow
importsocket
importtime
importselect
defloop(port,cert,ip):
    """
    GUI loop.
    port: port to connect to.
    cert: public certificate (task 3)
    ip: IP to bind to (task 3)

    A socket is created for communication with the server. We can recieve
    and send messages through this socket.
    """
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
try:
        client_socket.connect((ip,port))
 exceptsocket.errorasmsg:
        print('Connection failed. Error Code: '+str(msg[0])+' Message '+msg[1])
sys.exit()
 client_socket.setblocking(0)
list=[client_socket]
w=MainWindow()
whilew.update():
        read_list,write_list,except_list=select.select(list,list,list)
ifread_list:
            recv_line=client_socket.recv(1024)
ifrecv_line:
                w.writeln(recv_line.decode())
  ifwrite_list:
            line=w.getline()
ifline:
                client_socket.send(str.encode(line))
  ifexcept_list:
            w.quit()
  client_socket.close()

if__name__=='__main__':
    importsys
importargparse
p=argparse.ArgumentParser()
p.add_argument('--port',help='port to connect to',default=12345,type=int)
p.add_argument('--cert',help='server public cert',default='',type=str)
p.add_argument('--ip',help='IP to bind to',default='127.0.0.1',type=str)
args=p.parse_args(sys.argv[1:])
loop(args.port,args.cert,args.ip)

<EOF>