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
import sys
import struct
from socket import *
from random import randint
from gui import MainWindow
from sensor import *
import select
import math
import time
import queue

ROUTE_STRENGTH = 0
ROUTE_DECAY = 1


def random_position(n):
    """Get a random position in nxn grid."""
    x = randint(0, n)
    y = randint(0, n)
    return(x, y)


class Sensor():
    """The Sensor class represents the actual sensor. It contains all the data
    that the sensor needs to operate: its own position in the grid, variables
    used to calculate its range, and a GUI object to print
    messages to the user. It also keeps a lot of data about other sensors
    in the grid in different datastructures. With this it can work in a
    network of sensors, using pings, pongs, and echos that traverse the entire
    network.
    """
    def __init__(self, mcast_addr, pos, strength, decay, window, grid_size):
        """This method sets up all class variables: a lot of empty
        datastructures and a few variables recieved from the main function
        that set up the sensor.
        """
        self.pos = pos
        self.strength = strength
        self.decay = decay
        self.msg_queue = queue.Queue()
        self.neighbors = []
        self.repinged_neighbors = []
        self.mcast_addr = mcast_addr
        self.seq_num = 0
        self.fathers = {}
        self.seen_echos = []
        self.echo_replies = {}
        self.echos_sent = {}
        self.window = window
        self.neighbors_sums = {}
        self.grid_size = grid_size
        self.known_sensors = {}

    def new_mcast(self, pos, strength, decay):
        """Every time we recieved a multicast message we add the sender
        to our known sensors in the network.
        """
        self.known_sensors[pos] = (strength, decay)
        self.known_sensors[self.pos] = (self.strength, self.decay)

    def calc_distance(self, pos1, pos2=None):
        """This method calculates the distance between to sensors in the grid.
        If only one position is given it uses its own coordinates as the
        second position.
        """
        if pos2 is None:
            return math.sqrt(abs(self.pos[0]-pos1[0])**2+abs(self.pos[1]-pos1[1])**2)
        return math.sqrt(abs(pos1[0]-pos2[0])**2+abs(pos1[1]-pos2[1])**2)

    def calc_range(self, pos1, pos2=None):
        """Calculates whether the sensor at pos1 can reach the sensor at
        pos2. If no pos2 is given we calculate whether we can reach pos1 from
        our own sensor. To calculate the range we use the strength and decay
        values of a sensors signal.
        """
        distance = self.calc_distance(pos1, pos2)
        if pos2 is None:
            if distance == 0.0:
                return False
            return math.floor(self.strength-(distance**self.decay)) > 0
        strength, decay = self.known_sensors[pos1]
        return math.floor(strength-(distance**decay)) > 0

    def process_message(self, data, address):
        """When the main function recieves a message from another sensor
        through the peer UDP socket, this method analyses it and calls the
        appropriate methods.
        """
        type, seq_num, init, neighbor, operation, _, _, payload = message_decode(
            data)
        if type == MSG_PONG:
            if self.calc_range(neighbor):
                if(neighbor, address) not in self.neighbors:
                    self.neighbors.append((neighbor, address))
                self.repinged_neighbors.append((neighbor, address))
        elif type == MSG_ECHO:
            self.handle_echo(seq_num, init, neighbor, operation, payload)
        elif type == MSG_ECHO_REPLY:
            self.handle_echo_reply(seq_num, init, neighbor, operation, payload)
        elif type == MSG_JAM:
            self.window.quit()

    def handle_echo(self, seq_num, init, neighbor, operation, payload):
        """This method is part of the echo algorithm. When we recieve an echo
        we determine what to do with it depending on who sent it and whether we
        have seen it before. We keep track of seen echos and fathers for our
        echos in the class variables."""
        key = str((init, seq_num))
        if(init, seq_num) not in self.seen_echos:
            self.window.writeln("Echo recieved from initiator "+str(init))
            self.echo_replies[key] = []
            self.fathers[key] = neighbor
            if len(self.neighbors) == 1:
                if operation == OP_SIZE:
                    payload = 1
                self.echo_reply(neighbor, seq_num, init, operation, payload)
                return
            self.echo(init, seq_num, operation)
            self.seen_echos.append((init, seq_num))
        else:
            self.echo_reply(neighbor, seq_num, init, operation, 0)

    def handle_echo_reply(self, seq_num, init, neighbor, operation, payload):
        """This method determines what to do when we have recieved a reply
        to our echo sent to our neighbors.
        """
        key = str((init, seq_num))
        if neighbor not in self.echo_replies[key]:
            if operation == OP_SIZE:
                self.neighbors_sums[key] += payload
            self.echo_replies[key].append(neighbor)
        if self.pos == init:
            if(len(self.echo_replies[key]) == self.echos_sent[key]):
                self.window.writeln("DECIDE EVENT")
                if operation == OP_SIZE:
                    msg = ("Size of Network: " +
                           str(int(self.neighbors_sums[key]+1))+" sensors.")
                    self.window.writeln(msg)
            return
        if(len(self.echo_replies[key]) == self.echos_sent[key]):
            if operation == OP_SIZE:
                payload = self.neighbors_sums[key]+1
            self.echo_reply(self.fathers[key],
                            seq_num, init, operation, payload)

    def get_msg(self):
        """This method retrieves a message from the message queue of this
        sensor. This method can then be sent through the socket by the main
        function.
        """
        if self.msg_queue.empty():
            return None
        return self.msg_queue.get()

    def ping(self):
        """This method is used to send a multicast ping. It determines which
        sensors are our neighbors by checking which neighbors replied to our
        last ping.
        """
        for neighbor in self.neighbors:
            if neighbor not in self.repinged_neighbors:
                self.neighbors.remove(neighbor)
        self.repinged_neighbors = []
        msg = message_encode(MSG_PING, 0, self.pos, self.pos,
                             strength=self.strength, decay=self.decay)
        self.msg_queue.put((msg, self.mcast_addr))

    def pong(self, pos_init, address):
        """This method sends a pong message in reply to a ping."""
        msg = message_encode(MSG_PONG, 0, pos_init, self.pos,
                             strength=self.strength, decay=self.decay)
        self.msg_queue.put((msg, address))

    def echo(self, init, seq_num, operation):
        """This method sens an echo message to all its neighbors except the
        one it got the echo from. It sets up the datastructures used to
        keep track of how many of its neighbors have replied to the echo.
        """
        if init is None:
            init = self.pos
        if seq_num is None:
            seq_num = self.seq_num
        key = str((init, seq_num))
        msg = message_encode(MSG_ECHO, seq_num, init, self.pos,
                             operation, strength=self.strength, decay=self.decay)
        self.seen_echos.append((init, seq_num))
        if operation == OP_SIZE:
            self.neighbors_sums[key] = 0
        if key not in self.echo_replies:
            self.echo_replies[key] = []
        self.echos_sent[key] = 0
        for neighbor in self.neighbors:
            if neighbor in self.fathers:
                continue
            self.msg_queue.put((msg, neighbor[1]))
            self.echos_sent[key] += 1

    def echo_reply(self, dest, seq_num, init, operation, payload):
        """This method sends an echo reply to a specified sensor."""
        msg = message_encode(MSG_ECHO_REPLY, seq_num, init, self.pos, operation,
                             strength=self.strength, decay=self.decay, payload=payload)
        addr = None
        for neighbor in self.neighbors:
            if neighbor[0] == dest:
                addr = neighbor[1]
        if addr is not None:
            self.msg_queue.put((msg, addr))

    def move(self):
        """This method changes the position of the sensor in the grid to a
        random other position.
        """
        self.pos = random_position(self.grid_size)
        self.window.writeln('new position is (%s, %s)' % self.pos)

    def set_strength(self, strength):
        """This is a setter for the signal strength of the sensor."""
        if strength < 10:
            strength = 10
        if strength > 100:
            strength = 100
        strength = round(strength)
        self.strength = strength
        self.window.writeln("new strength is "+str(strength))

    def set_decay(self, decay):
        """This is a setter for the signal decay of the sensor."""
        if decay > 2.0:
            decay = 2.0
        if decay < 1:
            decay = 1.0
        self.decay = decay
        self.window.writeln("new decay is "+str(decay))

    def list_neighbors(self):
        """This method prints a list of all neighbors of this sensor to the
        GUI, ordered by distance.
        """
        ordered_list = []
        for pos, addr in self.neighbors:
            new_dist = self.calc_distance(pos)
            if len(ordered_list) == 0:
                ordered_list.append((pos, addr))
                continue
            for n, (pos2, _) in enumerate(ordered_list):
                if new_dist < self.calc_distance(pos2):
                    ordered_list.insert(n, (pos, addr))
            if(pos, addr) not in ordered_list:
                ordered_list.append((pos, addr))
        for e in ordered_list:
            self.window.writeln(str(e))

    def get_neighbors(self, sensor):
        """This method returns a list of all neighbors of a sensor that is not
        this sensor itself.
        """
        neighbors = []
        for sen in self.known_sensors:
            if sen == sensor:
                continue
            if self.calc_range(sensor, sen):
                neighbors.append(sen)
        return neighbors

    def dijkstra(self, dest, typ, source=None):
        """This method uses the dijkstra algorithm to find the shortest path
        from source to dest. If no source is specified we use our own position
        as source. typ specifies whether we find the shortest path based on
        decay or strength of sensors in the network.
        """
        strength = False
        if typ == ROUTE_STRENGTH:
            strength = True
        vertices = []
        dist = {}
        prev = {}
        for sensor in self.known_sensors:
            if strength:
                dist[sensor] = -1
            else:
                dist[sensor] = float("inf")
            prev[sensor] = None
            vertices.append(sensor)
        if source is None:
            source = self.pos
        dist[source] = 0
        while vertices:
            top_sensor = ""
            smallest = float("inf")
            biggest = -1
            for el in vertices:
                if strength:
                    if dist[el] > biggest:
                        top_sensor = el
                        biggest = dist[el]
                else:
                    if dist[el] < smallest:
                        top_sensor = el
                        smallest = dist[el]
            if top_sensor not in vertices:
                break
            vertices.remove(top_sensor)
            if top_sensor == dest:
                break
            neighbors = self.get_neighbors(top_sensor)
            if neighbors == []:
                break
            for neighbor in neighbors:
                if neighbor not in vertices:
                    continue
                value = self.known_sensors[top_sensor][typ]
                alt = dist[top_sensor]+value
                if strength:
                    if alt > dist[neighbor]:
                        dist[neighbor] = alt
                        prev[neighbor] = top_sensor
                else:
                    if alt < dist[neighbor]:
                        dist[neighbor] = alt
                        prev[neighbor] = top_sensor
        path = []
        curr = dest
        if prev[curr] is not None or curr == source:
            while curr is not None:
                path.insert(0, curr)
                curr = prev[curr]
        return path, dist[dest]

    def calc_route(self, dest, typ):
        """This method finds a shortest route from ourself to dest. It uses
        the dijkstra method to do so. It gives feedback to the user about the
        found path.
        """
        if dest not in self.known_sensors:
            self.window.writeln("No sensor at "+str(dest))
            return
        path, total_distance = self.dijkstra(dest, typ)
        if total_distance == float("inf"):
            self.window.writeln("There is no path between " +
                                str(self.pos)+" and "+str(dest)+" in the sensor network")
            return
        if typ == ROUTE_DECAY:
            t = "decay"
        else:
            t = "strength"
        self.window.writeln("The shortest path to " +
                            str(dest)+" is: "+str(path))
        self.window.writeln("with a "+t+" of "+str(total_distance))

    def find_all_paths(self):
        """This method finds all shortest paths in the network by decay. It
        is used to find the central node in the network.
        """
        paths = []
        traversed = []
        for sensor1 in self.known_sensors:
            for sensor2 in self.known_sensors:
                if((sensor1, sensor2) in traversed or (sensor2, sensor1) in traversed or sensor1 == sensor2):
                    continue
                path, length = self.dijkstra(sensor1, ROUTE_DECAY, sensor2)
                paths.append(path)
                traversed.append((sensor1, sensor2))
        return paths

    def find_central_sensor(self, paths):
        """This method finds the central node in the network, given all
        shortest paths in the network.
        """
        centrality = {}
        for sensor in self.known_sensors:
            centrality[sensor] = 0
            for path in paths:
                if path[0] != sensor and path[-1] != sensor and sensor in path:
                    centrality[sensor] += 1
        biggest = 0
        central_sensor = None
        for sensor in centrality:
            if centrality[sensor] > biggest:
                biggest = centrality[sensor]
                central_sensor = sensor
        return central_sensor

    def send_jam(self, sensor):
        """This method sends a jam message to the specified sensor. It may
        only do so if this sensor is its neighbor.
        """
        msg = message_encode(MSG_JAM, 0, self.pos, self.pos,
                             strength=self.strength, decay=self.decay)
        addr = None
        for neighbor in self.neighbors:
            if neighbor[0] == sensor:
                addr = neighbor[1]
        if addr is not None:
            self.msg_queue.put((msg, addr))
        else:
            self.window.writeln("No jam possible from this sensor")

    def jam(self):
        """This method is used to jam the central node of the network by
        calculating all shortes paths.
        """
        all_shortest_routes = self.find_all_paths()
        central = self.find_central_sensor(all_shortest_routes)
        if central is None:
            self.window.writeln("No jam possible from this sensor")
        self.send_jam(central)

    def print(self, line):
        self.window.writeln(line)


def parse_tuple(line):
    """Parses a string containing a tuple to an actual tuple."""
    tup = line.split(',', 1)
    x = tup[0].lstrip(' (')
    y = tup[1].rstrip(' )')
    return (int(x), int(y))


def parse_command(line, sensor):
    """Parses a command given to the GUI by the user and calls the appropriate
    methods of the sensor object.
    """
    split_line = line.split(' ', 1)
    command = split_line[0]
    if command == "ping":
        sensor.ping()
    elif command == "list":
        sensor.list_neighbors()
    elif command == "move":
        sensor.move()
    elif command == "decay":
        if len(split_line) < 2:
            sensor.print("Usage: decay <new_decay>")
            return
        decay = float(split_line[1])
        sensor.set_decay(decay)
    elif command == "strength":
        if len(split_line) < 2:
            sensor.print("Usage: strength <new_strength>")
            return
        strength = float(split_line[1])
        sensor.set_strength(strength)
    elif command == "echo":
        sensor.echo(None, None, OP_NOOP)
        sensor.seq_num += 1
    elif command == "size":
        sensor.echo(None, None, OP_SIZE)
        sensor.seq_num += 1
    elif command == "route_decay":
        if len(split_line) < 2:
            sensor.print("Usage: route_decay <(x,y)>")
            return
        dest = parse_tuple(split_line[1])
        sensor.calc_route(dest, ROUTE_DECAY)
    elif command == "route_strength":
        if len(split_line) < 2:
            sensor.print("Usage: route_strength <(x,y)>")
            return
        dest = parse_tuple(split_line[1])
        sensor.calc_route(dest, ROUTE_STRENGTH)
    elif command == "jam":
        sensor.jam()
    else:
        sensor.print("Invalid Command")


def main(mcast_addr, sensor_pos, sensor_strength, sensor_decay, grid_size, ping_period):
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
    mcast = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    mcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    mreq = struct.pack('4sl', inet_aton(mcast_addr[0]), INADDR_ANY)
    mcast.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
    if sys.platform == 'win32':
        mcast.bind(('localhost', mcast_addr[1]))
    else:
        mcast.bind(mcast_addr)
    peer = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    peer.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 5)
    if sys.platform == 'win32':
        peer.bind(('localhost', INADDR_ANY))
    else:
        peer.bind(('', INADDR_ANY))
    window = MainWindow()
    window.writeln('my address is %s:%s' % peer.getsockname())
    window.writeln('my position is (%s, %s)' % sensor_pos)
    read_list = [mcast, peer]
    write_list = [peer]
    sensor = Sensor(mcast_addr, sensor_pos, sensor_strength,
                    sensor_decay, window, grid_size)
    start = time.time()
    while window.update():
        readable, writable, exc = select.select(
            read_list, write_list, write_list, 0)
        if ping_period != 0 and time.time() > start+ping_period:
            sensor.ping()
            start = time.time()
        for sock in readable:
            if sock == mcast:
                data, address = mcast.recvfrom(1024)
                if data:
                    _, _, pos_init, _, _, str_init, decay_init, _ = message_decode(
                        data)
                    sensor.new_mcast(pos_init, str_init, decay_init)
                    if sensor.calc_range(pos_init):
                        sensor.pong(pos_init, address)
            if sock == peer:
                data, address = peer.recvfrom(1024)
                if data:
                    sensor.process_message(data, address)
        for sock in writable:
            if sock == peer:
                msg = sensor.get_msg()
                while msg:
                    peer.sendto(msg[0], msg[1])
                    msg = sensor.get_msg()
        for sock in exc:
            pass
        line = window.getline()
        if line:
            parse_command(line, sensor)
        time.sleep(0.1)


if __name__ == '__main__':
    import sys
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--group', help='multicast group', default='224.1.1.1')
    p.add_argument('--port', help='multicast port', default=50000, type=int)
    p.add_argument('--pos', help='x,y sensor position', default=None)
    p.add_argument('--grid', help='size of grid', default=100, type=int)
    p.add_argument('--strength', help='sensor strength', default=50, type=int)
    p.add_argument('--decay', help='decay rate', default=1, type=int)
    p.add_argument(
        '--period', help='period between autopings (0=off)', default=5, type=int)
    args = p.parse_args(sys.argv[1:])
    if args.pos:
        pos = tuple(int(n) for n in args.pos.split(',')[:2])
    else:
        pos = random_position(args.grid)
    if args.decay > 1.0 and args.decay <= 2.0:
        decay = args.decay
    else:
        decay = 1
    mcast_addr = (args.group, args.port)
    main(mcast_addr, pos, args.strength, decay, args.grid, args.period)
