### MAIN FILE THAT CONNECTS TO WEBOTS SIMULATOR VIA WIFI SOCKET CONNECTION - USES THREADING TO HANDLE MULTIPLE ROBOTS IN SWARM

# Socket connection - to mimic bluetooth radio connection
import socket, json, time, threading, copy, queue
from tkinter import *
import gui_map_thread
# Need while loops???

class ThreadedGui():
    def __init__(self, in_q1, in_q2):
        print("GUI INIT")
        threading.Thread(target = self.gui,args = (self.client, self.address, in_q1, in_q2)).start()

    def gui(self, in_q1, in_q2):
        while True:
            ds_dict1, ds_dict2 = 0,0
            print("GUI THREAD")
            # nested if loops to ensure two values in queue are ds_dict1 and ds_dict2, IN ORDER
            if in_q1.empty() == False and in_q2.empty() == False:
                # GUI STUFF

                # .get() clears queue
                ds_dict1 = in_q1.get()
                ds_dict2 = in_q2.get()

                gui = gui_map_thread.Robot.build_gui(ds_dict1, ds_dict2)


class ThreadedServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.num_clients = 0
        self.first_time = True

        self.old_time1 = time.perf_counter()
        self.old_time2 = time.perf_counter()
        self.send_r1_data = True



    
    def spawnClient(self, q1, q2):
        
        while self.num_clients != 2:
            self.sock.listen(5)
            self.client, self.address = self.sock.accept()
            threading.Thread(target = self.listenToClient,args = (self.client, self.address, q1, q2)).start()
            self.num_clients += 1
            print("CLIENT " + str(self.num_clients) + " CONNECTED")
        
        print("DONE LISTENING")

        print("GUI")
        threading.Thread(target = self.gui,args = (q1, q2, self.client)).start()

        

    def gui(self, in_q1, in_q2, client):
        while True:
            ds_dict1, ds_dict2 = 0,0
            #print("GUI THREAD")
            # nested if loops to ensure two values in queue are ds_dict1 and ds_dict2, IN ORDER
            if in_q1.empty() == False and in_q2.empty() == False:
                # GUI STUFF

                # .get() clears queue
                ds_dict1 = in_q1.get()
                ds_dict2 = in_q2.get()
                # DATA is being recieved

                # to only init once
                if self.first_time == True:
                    self.gui = gui_map_thread.gui(ds_dict1, ds_dict2)
                    self.first_time = False
                    print(self.first_time)
                
                self.gui.update_gui(ds_dict1, ds_dict2)

                # get robot coords
                self.robot1_coords = self.gui.robot1.robot_coords
                self.robot2_coords = self.gui.robot2.robot_coords
   
                self.robot1_coords['direction'] = self.gui.robot1.direction
                self.robot2_coords['direction'] = self.gui.robot2.direction



    def listenToClient(self, client, address, out_q1, out_q2):
        size = 1024

        while True:
            
            try:
                data = client.recv(size)

                # if self.first_time == False:
                #     # send data to clients - data is tagged so controller knows
                #     client.send(json.dumps(self.robot1_coords).decode())
                #     client.send(json.dumps(self.robot2_coords).decode())
                
                # WRITE CODE TO IGNORE NO DATA ON ROBOT CONTROLLER
                
                if self.first_time == False:
                    # adding tag to hash map
                    self.robot1_coords['name'] = 'robot1'
                    self.robot2_coords['name'] = 'robot2'
                    
                    # alternate sending data to prevent concatenation of hash map in TCP
                    if time.perf_counter() - self.old_time1 > 0.01:
                        if self.send_r1_data == True:
                            client.send(json.dumps(self.robot1_coords).encode())
                            self.send_r1_data = False
                        else:
                            client.send(json.dumps(self.robot2_coords).encode())
                            self.send_r1_data = True
                        self.old_time1 = time.perf_counter()
                    else:
                        client.send("NO DATA".encode())

                if data:
                    # RESPONSE - send to gui_map class for processing
                    # print("ROBOT 1: " + json.loads(data.decode()))
                    # print("ROBOT 2: " + json.loads(data.decode()))
                    
                    # conceptually - this is two threads so don't treat as normal, it will run both at once

                    ds_dict = json.loads(data.decode())
                
                    # nested if loops to ensure two values in queue are ds_dict1 and ds_dict2, IN ORDER
                    if ds_dict['name'] == 'robot1' and out_q1.empty() == True:
                        out_q1.put(ds_dict)
                    if ds_dict['name'] == 'robot2' and out_q2.empty() == True:
                        out_q2.put(ds_dict)
               
                     
            
                else:
                    print('Client disconnected')
                    
                    
            except:
                pass



cancelled1 = False
cancelled2 = False

def collect_socket_data(conn_copy1, connection1, conn_copy2, connection2):
    # collect sensor data from WEBOTS
    global ds_dict1, ds_dict2
    
    try:

        data1 = conn_copy1.recv(1024)
        data2 = conn_copy2.recv(1024)

        # conn_copy2.send("test")

        if data1:
            ds_dict1 = json.loads(data1.decode())
            #print("ROBOT 1: " + str(ds_dict1))
            # SEND DATA BACK TO ROBOT IF gui_map.COLLISION = TRUE
        # if data2:
        #     ds_dict2 = json.loads(data2.decode())
        #     #print("ROBOT 2: " + str(ds_dict2))

        
        
    except socket.error:
        if (connection1 == True):
            print("Client 1 disconnected")
            connection = True
        if (connection2 == True):
            print("Client 2 disconnected")
            connection = True
    except json.decoder.JSONDecodeError:
        # to prevent dropped values from connection issues
        pass


# create socket
HOST = ''
# constructing two socket servers to handle data from two clients 
PORT1 = 8888
s1 = socket.socket()
s2 = socket.socket()

# try:
#     sock1 = ThreadedServer(HOST, PORT1)
#     sock2 = ThreadedServer(HOST, PORT1)
# except socket.error as e:
#     print("ERROR: " + str(e))


# s1.listen()
# conn1, addr1 = s1.accept()
# print('Socket 1 connected')
# s2.listen()
# conn2, addr2 = s2.accept()
# print('Socket 2 connected')

# collect_socket_data(conn1, cancelled1, conn2, cancelled2)
# gui = gui_map.gui(ds_dict1, ds_dict2)

# collect socket data

# update gui 

old_time = time.perf_counter()
sock1 = ThreadedServer(HOST, PORT1)
# sock2 = ThreadedServer(HOST, PORT1)

# while True:
    # collect_socket_data(conn1, cancelled1, conn2, cancelled2)
    # gui.update_gui(ds_dict1, ds_dict2)

# create queue objects
q1 = queue.Queue()
q2 = queue.Queue()

sock1.spawnClient(q1, q2)
# sock2.listen(q1, q2)





    
