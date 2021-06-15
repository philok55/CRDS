
"""
Networks and Network Security
Lab 6 - Distributed Sensor Network
NAME: Philo Decroos, Mitchell van den Bulk
STUDENT ID: 11752262, 11333650

DESCRIPTION:
This file contains code to simulate a sensor in a network of communicating
sensors. We use UDP socket programming to let different sensors communicate
with each other. Sensors can send multicast pings to find out where other
sensors are in the network, and unicast messages to neighbors (sensors in
their reach). These unicast messages are used to send echo waves through the
network (for example to calculate the size) and attack (jam) the central node.

Sensors can be operated through a GUI that takes certain commands and prints
output to the user.
"""
importsys
importstruct
fromsocketimport*
fromrandomimportrandint
fromguiimportMainWindow
fromsensorimport*
importselect
importmath
importtime
importqueue
ROUTE_STRENGTH=0
ROUTE_DECAY=1
defrandom_position(n):
    """Get a random position in nxn grid."""
x=randint(0,n)
y=randint(0,n)
return(x,y)

classSensor():
    """The Sensor class represents the actual sensor. It contains all the data
    that the sensor needs to operate: its own position in the grid, variables
    used to calculate its range, and a GUI object to print
    messages to the user. It also keeps a lot of data about other sensors
    in the grid in different datastructures. With this it can work in a
    network of sensors, using pings, pongs, and echos that traverse the entire
    network.
    """
def__init__(self,mcast_addr,pos,strength,decay,window,grid_size):
        """This method sets up all class variables: a lot of empty
        datastructures and a few variables recieved from the main function
        that set up the sensor.
        """
self.pos=pos
self.strength=strength
self.decay=decay
self.msg_queue=queue.Queue()
self.neighbors=[]
self.repinged_neighbors=[]
self.mcast_addr=mcast_addr
self.seq_num=0
self.fathers={}
self.seen_echos=[]
self.echo_replies={}
self.echos_sent={}
self.window=window
self.neighbors_sums={}
self.grid_size=grid_size
self.known_sensors={}
 defnew_mcast(self,pos,strength,decay):
        """Every time we recieved a multicast message we add the sender
        to our known sensors in the network.
        """
self.known_sensors[pos]=(strength,decay)
self.known_sensors[self.pos]=(self.strength,self.decay)
 defcalc_distance(self,pos1,pos2=None):
        """This method calculates the distance between to sensors in the grid.
        If only one position is given it uses its own coordinates as the
        second position.
        """
ifpos2isNone:
            returnmath.sqrt(abs(self.pos[0]-pos1[0])**2+abs(self.pos[1]-pos1[1])**2)
 returnmath.sqrt(abs(pos1[0]-pos2[0])**2+abs(pos1[1]-pos2[1])**2)
 defcalc_range(self,pos1,pos2=None):
        """Calculates whether the sensor at pos1 can reach the sensor at
        pos2. If no pos2 is given we calculate whether we can reach pos1 from
        our own sensor. To calculate the range we use the strength and decay
        values of a sensors signal.
        """
distance=self.calc_distance(pos1,pos2)
ifpos2isNone:
            ifdistance==0.0:
                returnFalse
 returnmath.floor(self.strength-(distance**self.decay))>0
 strength,decay=self.known_sensors[pos1]
returnmath.floor(strength-(distance**decay))>0
 defprocess_message(self,data,address):
        """When the main function recieves a message from another sensor
        through the peer UDP socket, this method analyses it and calls the
        appropriate methods.
        """
type,seq_num,init,neighbor,operation,_,_,payload=message_decode(data)
iftype==MSG_PONG:
            ifself.calc_range(neighbor):
                if(neighbor,address)notinself.neighbors:
                    self.neighbors.append((neighbor,address))
 self.repinged_neighbors.append((neighbor,address))
  eliftype==MSG_ECHO:
            self.handle_echo(seq_num,init,neighbor,operation,payload)
 eliftype==MSG_ECHO_REPLY:
            self.handle_echo_reply(seq_num,init,neighbor,operation,payload)
 eliftype==MSG_JAM:
            self.window.quit()
  defhandle_echo(self,seq_num,init,neighbor,operation,payload):
        """This method is part of the echo algorithm. When we recieve an echo
        we determine what to do with it depending on who sent it and whether we
        have seen it before. We keep track of seen echos and fathers for our
        echos in the class variables."""
key=str((init,seq_num))
if(init,seq_num)notinself.seen_echos:
            self.window.writeln("Echo recieved from initiator "+str(init))
self.echo_replies[key]=[]
self.fathers[key]=neighbor
iflen(self.neighbors)==1:
                ifoperation==OP_SIZE:
                    payload=1
 self.echo_reply(neighbor,seq_num,init,operation,payload)
return
 self.echo(init,seq_num,operation)
self.seen_echos.append((init,seq_num))
 else:
            self.echo_reply(neighbor,seq_num,init,operation,0)
  defhandle_echo_reply(self,seq_num,init,neighbor,operation,payload):
        """This method determines what to do when we have recieved a reply
        to our echo sent to our neighbors.
        """
key=str((init,seq_num))
ifneighbornotinself.echo_replies[key]:
            ifoperation==OP_SIZE:
                self.neighbors_sums[key]+=payload
 self.echo_replies[key].append(neighbor)
 ifself.pos==init:
            if(len(self.echo_replies[key])==self.echos_sent[key]):
                self.window.writeln("DECIDE EVENT")
ifoperation==OP_SIZE:
                    msg=("Size of Network: "+str(int(self.neighbors_sums[key]+1))+" sensors.")
self.window.writeln(msg)
  return
 if(len(self.echo_replies[key])==self.echos_sent[key]):
            ifoperation==OP_SIZE:
                payload=self.neighbors_sums[key]+1
 self.echo_reply(self.fathers[key],seq_num,init,operation,payload)
  defget_msg(self):
        """This method retrieves a message from the message queue of this
        sensor. This method can then be sent through the socket by the main
        function.
        """
ifself.msg_queue.empty():
            returnNone
 returnself.msg_queue.get()
 defping(self):
        """This method is used to send a multicast ping. It determines which
        sensors are our neighbors by checking which neighbors replied to our
        last ping.
        """
forneighborinself.neighbors:
            ifneighbornotinself.repinged_neighbors:
                self.neighbors.remove(neighbor)
  self.repinged_neighbors=[]
msg=message_encode(MSG_PING,0,self.pos,self.pos,strength=self.strength,decay=self.decay)
self.msg_queue.put((msg,self.mcast_addr))
 defpong(self,pos_init,address):
        """This method sends a pong message in reply to a ping."""
msg=message_encode(MSG_PONG,0,pos_init,self.pos,strength=self.strength,decay=self.decay)
self.msg_queue.put((msg,address))
 defecho(self,init,seq_num,operation):
        """This method sens an echo message to all its neighbors except the
        one it got the echo from. It sets up the datastructures used to
        keep track of how many of its neighbors have replied to the echo.
        """
ifinitisNone:
            init=self.pos
 ifseq_numisNone:
            seq_num=self.seq_num
 key=str((init,seq_num))
msg=message_encode(MSG_ECHO,seq_num,init,self.pos,operation,strength=self.strength,decay=self.decay)
self.seen_echos.append((init,seq_num))
ifoperation==OP_SIZE:
            self.neighbors_sums[key]=0
 ifkeynotinself.echo_replies:
            self.echo_replies[key]=[]
 self.echos_sent[key]=0
forneighborinself.neighbors:
            ifneighborinself.fathers:
                continue
 self.msg_queue.put((msg,neighbor[1]))
self.echos_sent[key]+=1
  defecho_reply(self,dest,seq_num,init,operation,payload):
        """This method sends an echo reply to a specified sensor."""
msg=message_encode(MSG_ECHO_REPLY,seq_num,init,self.pos,operation,strength=self.strength,decay=self.decay,payload=payload)
addr=None
forneighborinself.neighbors:
            ifneighbor[0]==dest:
                addr=neighbor[1]
  ifaddrisnotNone:
            self.msg_queue.put((msg,addr))
  defmove(self):
        """This method changes the position of the sensor in the grid to a
        random other position.
        """
self.pos=random_position(self.grid_size)
self.window.writeln('new position is (%s, %s)'%self.pos)
 defset_strength(self,strength):
        """This is a setter for the signal strength of the sensor."""
ifstrength<10:
            strength=10
 ifstrength>100:
            strength=100
 strength=round(strength)
self.strength=strength
self.window.writeln("new strength is "+str(strength))
 defset_decay(self,decay):
        """This is a setter for the signal decay of the sensor."""
ifdecay>2.0:
            decay=2.0
 ifdecay<1:
            decay=1.0
 self.decay=decay
self.window.writeln("new decay is "+str(decay))
 deflist_neighbors(self):
        """This method prints a list of all neighbors of this sensor to the
        GUI, ordered by distance.
        """
ordered_list=[]
forpos,addrinself.neighbors:
            new_dist=self.calc_distance(pos)
iflen(ordered_list)==0:
                ordered_list.append((pos,addr))
continue
 forn,(pos2,_)inenumerate(ordered_list):
                ifnew_dist<self.calc_distance(pos2):
                    ordered_list.insert(n,(pos,addr))
  if(pos,addr)notinordered_list:
                ordered_list.append((pos,addr))
  foreinordered_list:
            self.window.writeln(str(e))
  defget_neighbors(self,sensor):
        """This method returns a list of all neighbors of a sensor that is not
        this sensor itself.
        """
neighbors=[]
forseninself.known_sensors:
            ifsen==sensor:
                continue
 ifself.calc_range(sensor,sen):
                neighbors.append(sen)
  returnneighbors
 defdijkstra(self,dest,typ,source=None):
        """This method uses the dijkstra algorithm to find the shortest path
        from source to dest. If no source is specified we use our own position
        as source. typ specifies whether we find the shortest path based on
        decay or strength of sensors in the network.
        """
strength=False
iftyp==ROUTE_STRENGTH:
            strength=True
 vertices=[]
dist={}
prev={}
forsensorinself.known_sensors:
            ifstrength:
                dist[sensor]=-1
 else:
                dist[sensor]=float("inf")
 prev[sensor]=None
vertices.append(sensor)
 ifsourceisNone:
            source=self.pos
 dist[source]=0
whilevertices:
            top_sensor=""
smallest=float("inf")
biggest=-1
forelinvertices:
                ifstrength:
                    ifdist[el]>biggest:
                        top_sensor=el
biggest=dist[el]
  else:
                    ifdist[el]<smallest:
                        top_sensor=el
smallest=dist[el]
   iftop_sensornotinvertices:
                break
 vertices.remove(top_sensor)
iftop_sensor==dest:
                break
 neighbors=self.get_neighbors(top_sensor)
ifneighbors==[]:
                break
 forneighborinneighbors:
                ifneighbornotinvertices:
                    continue
 value=self.known_sensors[top_sensor][typ]
alt=dist[top_sensor]+value
ifstrength:
                    ifalt>dist[neighbor]:
                        dist[neighbor]=alt
prev[neighbor]=top_sensor
  else:
                    ifalt<dist[neighbor]:
                        dist[neighbor]=alt
prev[neighbor]=top_sensor
    path=[]
curr=dest
ifprev[curr]isnotNoneorcurr==source:
            whilecurrisnotNone:
                path.insert(0,curr)
curr=prev[curr]
  returnpath,dist[dest]
 defcalc_route(self,dest,typ):
        """This method finds a shortest route from ourself to dest. It uses
        the dijkstra method to do so. It gives feedback to the user about the
        found path.
        """
ifdestnotinself.known_sensors:
            self.window.writeln("No sensor at "+str(dest))
return
 path,total_distance=self.dijkstra(dest,typ)
iftotal_distance==float("inf"):
            self.window.writeln("There is no path between "+str(self.pos)+" and "+str(dest)+" in the sensor network")
return
 iftyp==ROUTE_DECAY:
            t="decay"
 else:
            t="strength"
 self.window.writeln("The shortest path to "+str(dest)+" is: "+str(path))
self.window.writeln("with a "+t+" of "+str(total_distance))
 deffind_all_paths(self):
        """This method finds all shortest paths in the network by decay. It
        is used to find the central node in the network.
        """
paths=[]
traversed=[]
forsensor1inself.known_sensors:
            forsensor2inself.known_sensors:
                if((sensor1,sensor2)intraversedor(sensor2,sensor1)intraversedorsensor1==sensor2):
                    continue
 path,length=self.dijkstra(sensor1,ROUTE_DECAY,sensor2)
paths.append(path)
traversed.append((sensor1,sensor2))
  returnpaths
 deffind_central_sensor(self,paths):
        """This method finds the central node in the network, given all
        shortest paths in the network.
        """
centrality={}
forsensorinself.known_sensors:
            centrality[sensor]=0
forpathinpaths:
                ifpath[0]!=sensorandpath[-1]!=sensorandsensorinpath:
                    centrality[sensor]+=1
   biggest=0
central_sensor=None
forsensorincentrality:
            ifcentrality[sensor]>biggest:
                biggest=centrality[sensor]
central_sensor=sensor
  returncentral_sensor
 defsend_jam(self,sensor):
        """This method sends a jam message to the specified sensor. It may
        only do so if this sensor is its neighbor.
        """
msg=message_encode(MSG_JAM,0,self.pos,self.pos,strength=self.strength,decay=self.decay)
addr=None
forneighborinself.neighbors:
            ifneighbor[0]==sensor:
                addr=neighbor[1]
  ifaddrisnotNone:
            self.msg_queue.put((msg,addr))
 else:
            self.window.writeln("No jam possible from this sensor")
  defjam(self):
        """This method is used to jam the central node of the network by
        calculating all shortes paths.
        """
all_shortest_routes=self.find_all_paths()
central=self.find_central_sensor(all_shortest_routes)
ifcentralisNone:
            self.window.writeln("No jam possible from this sensor")
 self.send_jam(central)
 defprint(self,line):
        self.window.writeln(line)


defparse_tuple(line):
    """Parses a string containing a tuple to an actual tuple."""
tup=line.split(',',1)
x=tup[0].lstrip(' (')
y=tup[1].rstrip(' )')
return(int(x),int(y))

defparse_command(line,sensor):
    """Parses a command given to the GUI by the user and calls the appropriate
    methods of the sensor object.
    """
split_line=line.split(' ',1)
command=split_line[0]
ifcommand=="ping":
        sensor.ping()
 elifcommand=="list":
        sensor.list_neighbors()
 elifcommand=="move":
        sensor.move()
 elifcommand=="decay":
        iflen(split_line)<2:
            sensor.print("Usage: decay <new_decay>")
return
 decay=float(split_line[1])
sensor.set_decay(decay)
 elifcommand=="strength":
        iflen(split_line)<2:
            sensor.print("Usage: strength <new_strength>")
return
 strength=float(split_line[1])
sensor.set_strength(strength)
 elifcommand=="echo":
        sensor.echo(None,None,OP_NOOP)
sensor.seq_num+=1
 elifcommand=="size":
        sensor.echo(None,None,OP_SIZE)
sensor.seq_num+=1
 elifcommand=="route_decay":
        iflen(split_line)<2:
            sensor.print("Usage: route_decay <(x,y)>")
return
 dest=parse_tuple(split_line[1])
sensor.calc_route(dest,ROUTE_DECAY)
 elifcommand=="route_strength":
        iflen(split_line)<2:
            sensor.print("Usage: route_strength <(x,y)>")
return
 dest=parse_tuple(split_line[1])
sensor.calc_route(dest,ROUTE_STRENGTH)
 elifcommand=="jam":
        sensor.jam()
 else:
        sensor.print("Invalid Command")


defmain(mcast_addr,sensor_pos,sensor_strength,sensor_decay,grid_size,ping_period):
    """
    The main function sets up the sockets and the sensor object, and contains
    the event loop of the GUI, regulating the input and output through the
    sockets.

    mcast_addr: udp multicast (ip, port) tuple.
    sensor_pos: (x,y) sensor position tuple.
    sensor_strength: initial strength of the sensor ping (radius).
    grid_size: length of the  of the grid (which is always square).
    ping_period: time in seconds between multicast pings.
    """
mcast=socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
mcast.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
mreq=struct.pack('4sl',inet_aton(mcast_addr[0]),INADDR_ANY)
mcast.setsockopt(IPPROTO_IP,IP_ADD_MEMBERSHIP,mreq)
ifsys.platform=='win32':
        mcast.bind(('localhost',mcast_addr[1]))
 else:
        mcast.bind(mcast_addr)
 peer=socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
peer.setsockopt(IPPROTO_IP,IP_MULTICAST_TTL,5)
ifsys.platform=='win32':
        peer.bind(('localhost',INADDR_ANY))
 else:
        peer.bind(('',INADDR_ANY))
 window=MainWindow()
window.writeln('my address is %s:%s'%peer.getsockname())
window.writeln('my position is (%s, %s)'%sensor_pos)
read_list=[mcast,peer]
write_list=[peer]
sensor=Sensor(mcast_addr,sensor_pos,sensor_strength,sensor_decay,window,grid_size)
start=time.time()
whilewindow.update():
        readable,writable,exc=select.select(read_list,write_list,write_list,0)
ifping_period!=0andtime.time()>start+ping_period:
            sensor.ping()
start=time.time()
 forsockinreadable:
            ifsock==mcast:
                data,address=mcast.recvfrom(1024)
ifdata:
                    _,_,pos_init,_,_,str_init,decay_init,_=message_decode(data)
sensor.new_mcast(pos_init,str_init,decay_init)
ifsensor.calc_range(pos_init):
                        sensor.pong(pos_init,address)
   ifsock==peer:
                data,address=peer.recvfrom(1024)
ifdata:
                    sensor.process_message(data,address)
   forsockinwritable:
            ifsock==peer:
                msg=sensor.get_msg()
whilemsg:
                    peer.sendto(msg[0],msg[1])
msg=sensor.get_msg()
   forsockinexc:
            pass
 line=window.getline()
ifline:
            parse_command(line,sensor)
 time.sleep(0.1)


if__name__=='__main__':
    importsys
importargparse
p=argparse.ArgumentParser()
p.add_argument('--group',help='multicast group',default='224.1.1.1')
p.add_argument('--port',help='multicast port',default=50000,type=int)
p.add_argument('--pos',help='x,y sensor position',default=None)
p.add_argument('--grid',help='size of grid',default=100,type=int)
p.add_argument('--strength',help='sensor strength',default=50,type=int)
p.add_argument('--decay',help='decay rate',default=1,type=int)
p.add_argument('--period',help='period between autopings (0=off)',default=5,type=int)
args=p.parse_args(sys.argv[1:])
ifargs.pos:
        pos=tuple(int(n)forninargs.pos.split(',')[:2])
 else:
        pos=random_position(args.grid)
 ifargs.decay>1.0andargs.decay<=2.0:
        decay=args.decay
 else:
        decay=1
 mcast_addr=(args.group,args.port)
main(mcast_addr,pos,args.strength,decay,args.grid,args.period)

<EOF>