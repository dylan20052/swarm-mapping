### THIS INITIALIZES THE CANVAS OBJECT, TAKES THE DATA FROM THE SOCKET CONNECTION OF WEBOTS AND DRAWS THE LINES VIA MAPPING FUNCTION

from tkinter import *
import socket, copy, time

class Robot:
    scale_factor = 100
    robot_x_threshold = 0
    robot_y_threshold = 0
    robot_width = 0.3 * scale_factor
    robot_length = 0.3 * scale_factor

    # init dict for point coordinates
    data = {}
    old_data = {}

    def __init__(self, data, name, canvas):
        # create instance of old data and current data for map_room
        self.old_data = data
        self.name = name
        self.canvas = canvas

        # draw robot
        self.robot_coords = {'tl_x':0, 'tl_y':0, 'center_x':0, 'center_y':0}
        self.old_robot_coords = {'tl_x':0, 'tl_y':0, 'center_x':0, 'center_y':0} # first declared in update_robot
        
        # DIMENSIONS
        self.enviro_width = 0
        self.enviro_height = 0
        self.spike_enviro_width = 0
        self.spike_found = False

        
        # robot direction
        self.direction = ""
        
        self.lines = {}
        self.old_lines = {}

        self.scaled_old_data = {}
        self.scaled_data = {}

        self.old_time = time.perf_counter()

        self.delete = False

    
    def set_robot_pos(self, other_data, other_robot_coords):
        # 2nd init
        # assumes robots always begin in y-stack position
        self.robot_coords['tl_x'] = (self.old_data["left"] * self.scale_factor)
        if other_data["front"] - self.old_data["front"] > 0:
            self.robot_coords['tl_y'] = (self.old_data["front"] + other_data["front"]) * self.scale_factor
        else:
            self.robot_coords['tl_y'] = (self.old_data["front"] * self.scale_factor)

        self.robot = self.canvas.create_rectangle(self.robot_coords["tl_x"], self.robot_coords["tl_y"], self.robot_coords["tl_x"] + self.robot_width, self.robot_coords["tl_y"] + self.robot_length)
        self.robot_coords['center_x'] = self.robot_coords['tl_x'] + (self.robot_width / 2)
        self.robot_coords['center_y'] = self.robot_coords['tl_y'] + (self.robot_length / 2)

        # SET LABEL
        self.name_label = self.canvas.create_text((self.robot_coords['center_x'], self.robot_coords['center_y']), text=self.name, font=('Helvatical bold',5))


    # 1
    def map_room(self, data, other_data, other_robot_coords):
        
        self.other_robot_coords = other_robot_coords

        # get direction to adjust thresholds
        self.get_robot_velocity(data)

        # scaling data to be mapped correctly in room
        for key in list(self.old_data.keys())[:3]:
            # old_data and data have same keys
            self.scaled_old_data[key] = self.old_data[key] * self.scale_factor
            self.scaled_data[key] = data[key] * self.scale_factor

        #print("X SPEED " + str(self.scaled_x_speed))
        #print("Y SPEED " + str(self.scaled_y_speed))

        self.enviro_width = (data['left'] + data['right']) * self.scale_factor  # used in spike detection

        for direction in list(data.keys())[:3]:
        # detect vertical line  
            # if values haven't changed much then it must be a line
            #print(direction.upper() + ": " + str(data[direction]))
            #print(direction.upper() + ": " + str(self.old_data[direction]))
            
            if (self.spike_found == True):
                self.spike_enviro_width = (data['left'] + data['right']) * self.scale_factor
            else:
                self.spike_enviro_width = 0
                
            
            self.robot_coords['center_x'] = self.robot_coords['tl_x'] + (self.robot_width / 2)
            self.robot_coords['center_y'] = self.robot_coords['tl_y'] + (self.robot_length / 2)

            if (direction == 'front'):
                    # if moving perpendicular to front, so side to side
                
                self.front_line = self.canvas.create_line(self.scaled_old_data['left'], self.robot_coords['center_y'] - self.scaled_data[direction], self.scaled_data['left'], self.robot_coords['center_y'] - self.scaled_data[direction])
            # elif (abs(data[direction] - self.old_data[direction]) <= abs(self.scaled_x_speed/self.scale_factor + 0.4) and (direction == 'left' or direction == 'right')):
                self.lines[direction]  = self.front_line
            elif (direction == 'left'):        
                # LINE IS BEING DRAWN IN WRONG SPOT
                # self.canvas.create_line(self.scaled_data[direction], self.scaled_old_data['front'], self.scaled_data[direction], self.scaled_data['front'])
                self.left_line = self.canvas.create_line(self.robot_coords['center_x'] - self.scaled_data[direction], self.scaled_old_data['front'], self.robot_coords['center_x'] - self.scaled_data[direction], self.scaled_data['front'])
                self.lines[direction] = self.left_line
            elif (direction == 'right'):        
                # LINE IS BEING DRAWN IN WRONG SPOT
                # self.canvas.create_line(self.scaled_data[direction], self.scaled_old_data['front'], self.scaled_data[direction], self.scaled_data['front'])
                self.right_line = self.canvas.create_line(self.robot_coords['center_x'] + self.scaled_data[direction], self.scaled_old_data['front'], self.robot_coords['center_x'] + self.scaled_data[direction], self.scaled_data['front'])
                self.lines[direction] = self.right_line

            #  print(direction + ' line')
        # # detect obstacles/spikes
        #     if (abs(data[direction] - self.old_data[direction]) >= self.spike_threshold * self.scale_factor):
        #         # make text that is placed in center of obstacle
                
        #         self.spike_enviro_width = (data['left'] + data['right']) * self.scale_factor
        #         print(direction + " SPIKE")
        #         if (self.spike_found == False):     
        #             self.spike_found = True     # activate trigger
        #             self.spike_enviro_width = (data['left'] + data['right']) * self.scale_factor
        #             if direction == 'left' or direction == 'right':

        #                 self.spike_x = self.enviro_width - data[direction] if (direction == 'left') else self.spike_enviro_width
        #                 self.spike_y = self.robot_coords['center_y'] 
        #             else:
        #                 self.spike_x = self.robot_coords['center_x']
        #                 self.spike_y = self.robot_coords['center_y'] - data['front']
                    
        #             print("Spike trigger")

        #         elif (self.spike_found == True):
        #             self.spike_found = False        # turn off trigger bc/ now spike has been mapped
        #             self.obstacle_lbl = Label(self.master, text="OBSTACLE")
        #             self.obstacle_lbl.place(x=100, y=100)
        #             print("SPIKEEEEEE")
        

        # LINE CHECK: remove long/short lines + remove lines that the robots draw of each other
        threshold = 0
        # print("MY COORDS: " + str(self.robot_coords))
        # print("OTHER COORDS: " + str(other_robot_coords))
        for direction in self.lines:
            line = self.lines[direction]
            dims = self.canvas.bbox(line)

            x_length = dims[2] - dims[0]
            y_length = dims[3] - dims[1]
                # adjust threshold based on direction of robot?????
            if x_length < 4.5  or x_length > 40:
                self.canvas.delete(line)
                #print("delete")
            elif y_length < 4.5 or y_length > 40:
                self.canvas.delete(line)
                #print("delete")
            # print(abs(dims[0] - other_robot_coords['center_x']))
           # print(dims[0])
            #print(self.other_robot_coords['center_x'])
            
            # line-check dependent on robot direction
            # delete front lines if robot is moving forward/backward
            if direction == 'front':
                if self.direction == 'forward' or self.direction == 'backward':
                    self.canvas.delete(line)
                    print(self.name + " DELETING FRONT")
            if direction == 'left' or direction == 'right':
                if self.direction == 'left' or self.direction == 'right':
                    self.canvas.delete(line)
                    print(self.name + " DELETING " + direction)          
            if abs(dims[0] - other_robot_coords['center_x']) < threshold or abs(dims[2] - other_robot_coords['center_x']) < threshold:
                    self.canvas.delete(line)
                    print(self.name + " deleting")
            if abs(dims[1] - self.robot_coords['center_y']) < threshold or abs(dims[3] - self.robot_coords['center_y']) < threshold:
                    self.canvas.delete(line)
                    print(self.name + " deleting")

        
        # set old line lengths
        self.old_lines = copy.deepcopy(self.lines)

    # 2
    def update_robot(self, data):
        # update robot pos based on sensor data

    
        # signs will correct in canvas.move
        self.temp_delta_x_left = (data["left"] * self.scale_factor) - self.robot_coords['tl_x']
        self.temp_delta_x_right = (data["right"] * self.scale_factor) - (self.enviro_width - self.robot_coords['tl_x'])
        self.enviro_width = (data['left'] + data['right']) * self.scale_factor
        
        self.delta_y = (data["front"] - self.old_data["front"]) * self.scale_factor # have to do bc/ no backward sensor

        # MAKE A TEMP_DELTA_Y BC/ WHEN ROBOT MOVES UNDER BOX IT GLITHCES TO TOP - IN UPDATE ROBOT
        #print("DELTA_LEFT: " + str(self.temp_delta_x_left))
        #print("DELTA_RIGHT: " + str(self.temp_delta_x_right))
        
        # threshold only adequate if moving forward
        if (self.direction == 'forward' or self.direction == 'backward'):
            self.robot_x_threshold = 5
            self.robot_y_threshold = 20
        elif (self.direction == 'left' or self.direction == 'right'):
            self.robot_x_threshold = 100
            self.robot_y_threshold = 5


        # prevent glitching to opposite side in x direction
        if (abs(self.temp_delta_x_left) < self.robot_x_threshold):
            self.delta_x = self.temp_delta_x_left
            # only move if not dramatic, unless just reset coords
        elif (abs(self.temp_delta_x_right) < self.robot_x_threshold):
            # move based on right sensor data if left is too weird
            self.delta_x = self.temp_delta_x_right
        else:
            self.delta_x = 0
        
  

        if (abs(self.delta_y) > self.robot_y_threshold):
            self.delta_y = 0


        self.canvas.move(self.robot, self.delta_x, self.delta_y)
        self.canvas.move(self.name_label, self.delta_x, self.delta_y)
        #print("DELTA X: " + str(self.delta_x))
        #print(self.robot_coords)
        
        
        


        # reset robot coords
        # declare old robot coords
        self.old_robot_coords['tl_x'] = self.robot_coords['tl_x']
        self.old_robot_coords['tl_y'] = self.robot_coords['tl_y']

        self.robot_coords['tl_x'] = self.robot_coords['tl_x'] + self.delta_x
        self.robot_coords['tl_y'] = self.robot_coords['tl_y'] + self.delta_y
        self.old_data = data




    def get_robot_velocity(self, data):
        ### GET ROBOT SPEED TO MAKE CUSTOM LINE THRESHOLDS

        # find direction robot is moving
        # get robot velocity in x and y direction w/ robo coords
        # in 0.5m/s bc/ data comes in every 0.5 seconds

        self.direction = data['direction']
        

        



class gui:
    # gui class - can create multiple?

    # need threshold bc/ robot wavers a bit from slippage

    # 
    spike_threshold = 0.1

    # parallel to movement, needs to be smaller bc/ robots movement forward triggers regular threshold
    line_threshold = 0.02
    robot_x_threshold = 0
    robot_y_threshold = 0

    scale_factor = 100

    # accessed in main to send info to robots
    collision = False
    

    def __init__(self, data1, data2):
        
        # Init canvas widget on tkinter
        self.master = Tk()

        self.canvas_width=600
        self.canvas_height=600
        self.canvas = Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.robot1 = Robot(data1, "ROBOT 1", self.canvas)
        self.robot2 = Robot(data2, "ROBOT 2", self.canvas)

        self.robot1.set_robot_pos(data2, self.robot2.robot_coords)
        self.robot2.set_robot_pos(data1, self.robot1.robot_coords)

        self.robots = [self.robot1, self.robot2]

        self.old_time = time.perf_counter()
    
    def detect_robot_collision(self):
        # unused
        # prevent robot collision
            threshold = 50
            current_time = time.perf_counter()
            if (current_time - self.old_time) > 5:
                if (abs(self.robot1.robot_coords['center_x']  - self.robot2.robot_coords['center_x'] < threshold) and abs(self.robot1.robot_coords['center_y']  - self.robot2.robot_coords['center_y']) < threshold):
                    collision = True
                    
    def update_gui(self, data1, data2):
        self.master.update_idletasks()
        self.master.update()
        data = [data1, data2]
        # for i in range(len(data)):
        #     self.robots[i].map_room(data[i])
        #     self.robots[i].update_robot(data[i])
        self.robots[0].map_room(data[0], self.robots[1].data, self.robots[1].robot_coords)
        self.robots[0].update_robot(data[0])
        self.robots[1].map_room(data[1], self.robots[0].data, self.robots[0].robot_coords)
        self.robots[1].update_robot(data[1])
        gui.detect_robot_collision(self)

     

        




                
                
    