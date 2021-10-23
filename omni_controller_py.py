### THIS IS THE CONTROLLER FOR THE OMNI-DIRECTIONAL SWARM ROBOTS CONSTRUCTED IN WEBOTS

"""omni_controller_py controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor
import socket, time, json, copy

# create the Robot instance.
robot = Robot()
name = robot.getName()
    
# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

def initMotors():
    # init motors
    global rr_wheel, rl_wheel, fr_wheel, fl_wheel
      
    rr_wheel = robot.getDevice("rear_right_wheel");
    rl_wheel = robot.getDevice("rear_left_wheel");
    fr_wheel = robot.getDevice("front_right_wheel");
    fl_wheel = robot.getDevice("front_left_wheel");
        
    rr_wheel.setPosition((float('inf')))
    rl_wheel.setPosition((float('inf')))
    fr_wheel.setPosition((float('inf')))
    fl_wheel.setPosition((float('inf')))
    
    rr_wheel.setVelocity(0)
    rl_wheel.setVelocity(0)
    fr_wheel.setVelocity(0)
    fl_wheel.setVelocity(0)
    
def initDS():
    # init distance sensors
    global ds_front, ds_left, ds_right
    
    ds_front = robot.getDevice("ds1")
    ds_left = robot.getDevice("ds2")
    ds_right = robot.getDevice("ds3")
    
    # enable distance sensors
    ds_front.enable(timestep)
    ds_left.enable(timestep)    
    ds_right.enable(timestep)

def readDS(direction):
    # read distance sensor specified in parameter
    if (direction=="front"):
        return ds_front.getValue()
    elif (direction=="left"):
        return ds_left.getValue()       
    elif (direction=="right"):
        return ds_right.getValue()
          
def forward(speed):
    rr_wheel.setVelocity(speed)
    rl_wheel.setVelocity(-speed)
    fr_wheel.setVelocity(speed)
    fl_wheel.setVelocity(-speed)
def backward(speed):
    rr_wheel.setVelocity(-speed)
    rl_wheel.setVelocity(speed)
    fr_wheel.setVelocity(-speed)
    fl_wheel.setVelocity(speed)    
def right(speed):
    rr_wheel.setVelocity(speed)
    rl_wheel.setVelocity(speed)
    fr_wheel.setVelocity(-speed)
    fl_wheel.setVelocity(-speed)    
def left(speed):
    rr_wheel.setVelocity(-speed)
    rl_wheel.setVelocity(-speed)
    fr_wheel.setVelocity(speed)
    fl_wheel.setVelocity(speed)  
 
def reset_motors(old_t):
    rr_wheel.setVelocity(0)
    rl_wheel.setVelocity(0)
    fr_wheel.setVelocity(0)
    fl_wheel.setVelocity(0)
    
    stop_timer = 5 if direction == 'stop' else 2
    if (time.perf_counter() - old_t) < stop_timer:   # wait 2 seconds
        print(name + ": " + "moving " + direction)
        return False
    else:
        return True
    
my_coords = 0
other_coords = 0

def collect_socket_data(sock):
    ##collect sensor data from WEBOTS 
    global my_coords, other_coords
    try:   
        coords = sock.recv(4096)
        if coords:
            try:
                if json.loads(coords.decode())['name'] == name:
                    my_coords = json.loads(coords.decode())
                    #print(name + ": " + str(my_coords))
                elif json.loads(coords.decode())['name'] != name:
                    other_coords = json.loads(coords.decode())
                    #print(name + ": " + str(other_coords))
            except:
                pass
    except:
        pass
        
        
collision = False

old_motor_time = time.perf_counter()
col_time = time.perf_counter()
# default direction
direction = "left" if (name=='robot1') else "forward"
force_forward = False
# could be more robust
def prevent_collisions(init_time, init_front):    
    global collision, old_motor_time, col_time, direction, force_forward
    if my_coords and other_coords:
        threshold = 150
        current_time = time.perf_counter()
        if (current_time - init_time) > 10:
            if (abs(my_coords['center_x']  - other_coords['center_x'] < threshold) and abs(my_coords['center_y']  - other_coords['center_y']) < threshold):
                if time.perf_counter() - col_time > 8:
                    collision = True
                    col_time = time.perf_counter()

            else:
                collision = False
                
    if collision == True:
        collision = False
        # logic to ensure not moving in colliding directions
        # detect if y, x, or orthagonal collision
        print("DETECTING COLLISION")
        # y collision
    
             # might have to add another if using second half of this one to prevent parallel movement
        # x collision
        if my_coords['direction'] == 'left' and other_coords['direction'] == 'right':
            # 3 options
            if readDS("front") > readDS("right") and readDS("front") > 0.5:
                direction = "forward"
            elif readDS("right") > readDS("front") and readDS("right") > 0.5:
                direction = "right"
            else:
                direction = "backward"
        elif my_coords['direction'] == 'right' and other_coords['direction'] == 'left':
            # 3 options
            if readDS("front") > readDS("left") and readDS("front") > 0.5:
                direction = "backward"
            elif readDS("left") > readDS("front") and readDS("left") > 0.5:
                direction = "left"
            else:
                direction = "stop"
        # y collision
        elif my_coords['direction'] == 'forward' and other_coords['direction'] == 'backward':
            if readDS("right") > 0.5:
                direction = "right"
            elif readDS("left") > 0.5:
                direction = "left"
            else:
                direction = "stop"
            
        elif my_coords['direction'] == 'backward' and other_coords['direction'] == 'forward':
            if readDS("front") > 0.5:
                direction = "forward"
            elif force_forward != True:
                direction = "backward"
            else:
                direction = "right"
        # PERPENDICULAR collision
        elif my_coords['direction'] == 'left' and other_coords['direction'] != 'right' and other_coords['direction'] != 'left':
            # perpendicular collision
            if other_coords['direction'] == 'forward':
                if readDS("left") > 0.5:
                    direction = "left"
                elif readDS("front") > 0.5:
                    direction = "forward"
                elif readDS("right") > 0.5:
                    direction = "right"
                    # OTHER CAN'T GO FORWARD
                else:
                    direction = "backward"
            elif other_coords['direction'] == "backward":
                if readDS("left") > 0.5:
                    direction = "left" # keep going right
                    # OTHER CAN'T GO BACKWARD
                elif readDS("right") > 0.5:
                    direction = "right"
                else:
                    direction = "backward"
                    
        elif my_coords['direction'] == 'right' and (other_coords['direction'] != 'left' and other_coords['direction'] != 'right'):
            # perpendicular collision
            if other_coords['direction'] == 'forward':
                if readDS("right") > 0.5:
                    direction = "right"
                elif readDS("front") > 0.5:
                    direction = "forward"
                elif readDS("left") > 0.5:
                    direction = "left"
                else:
                    direction = "backward"
                
                    # OTHER CAN'T GO FORWARD
            elif other_coords['direction'] == "backward":
                if readDS("right") > 0.5:
                    direction = "right" # keep going right
                    # OTHER CAN'T GO BACKWARD
                elif readDS("left") > 0.5:
                    direction = "left"
                else:
                    direction = "backward"
        
        # perpendicular, travelling forward, complements above elif      
        elif my_coords['direction'] == 'forward' and (other_coords['direction'] != 'backward' and other_coords['direction'] != 'forward'):
            direction == 'stop'
            # if other_coords['direction'] == 'left':
                # #DON'T CONTINUE FORWARD
                # if readDS("right") > 0.5:
                    # direction = "right"
                # elif readDS("front") < init_front:
                    # direction = "backward"
                # elif readDS("left") > 0.5:
                    # direction = "left"
                # else:
                    # direction = "backward"
            # elif other_coords['direction'] == 'right':
                # #DON'T CONTINUE FORWARD
                # if readDS("left") > 0.5:
                    # direction = "left"
                # elif readDS("front") < init_front:
                    # direction = "backward"
                # elif readDS("right") > 0.5:
                    # direction = "right"
                # else:
                    # direction = "backward"       
        elif my_coords['direction'] == 'backward' and (other_coords['direction'] != 'forward' and other_coords['direction'] != 'backward'):
            direction = 'stop'
            # if other_coords['direction'] == 'left':
                ##DON'T CONTINUE FORWARD
                # if readDS("right") > 0.5:
                    # direction = "right"
                # elif readDS("front") >= init_front:
                    # direction = "forward"
                # elif readDS("left") > 0.5:
                    # direction = "left"
                # else:
                    # direction = "forward"
            # elif other_coords['direction'] == 'right':
                ##DON'T CONTINUE FORWARD
                # if readDS("left") > 0.5:
                    # direction = "left"
                # elif readDS("front") >= init_front:
                    # direction = "forward"
                # elif readDS("right") > 0.5:
                    # direction = "right"
                # else:
                    # direction = "forward"            
        
        print(name.upper() + ": " + direction + " after collision")
        old_motor_time = time.perf_counter()

            
        


# create socket connection to send data to GUI
HOST = '127.0.0.1'
PORT=8888
# if name == 'robot1':
    # PORT=8888
# elif name == 'robot2':
    # PORT = 8889
    
s = socket.socket()
s.connect((HOST, PORT))
s.settimeout(2)
print("connected")

global test

if __name__ == '__main__':  
     
    initMotors()
    initDS()
    init_time = time.perf_counter()
    
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    

    old_time = time.perf_counter()
    snake_left = False # simple switch - TRUE: move left after backward
    
    init = False  
    first_time = True
    counter = 0
    
    init_front = 0
    
    while robot.step(timestep) != -1:

        # send distance data every 0.1 seconds to GUI
        current_time = time.perf_counter()
        if (current_time - old_time > 0.1):
            # use json to serialize ds dictionary to send via socket
            # name at end is signifier
            ds_dict = {'front':readDS('front'),'left':readDS('left'),'right':readDS('right'), 'direction':direction, 'name':name}
            if init == False:
                # assume robot 1 starts directly behind robot 2
                if name == 'robot2':
                    init_front = ds_dict['front']
                    init = True
            if name == 'robot1':
                counter+= 1
                if counter == 20: # 3 seconds
                    init_front = ds_dict['front']
                    # gives time from robot 1 to shift left and init a new front distance
                    init = True
            ser_ds_dict = json.dumps(ds_dict) # serialized
            s.send(ser_ds_dict.encode())
            old_time = current_time
            if first_time == True:
                first_time = False
            else:
                collect_socket_data(s)
                
            
        print("TIME: " + str((time.perf_counter() - init_time)))

        
        # simple obstacle avoidance - snake pattern
        if (direction == 'forward' and readDS('front') <= 0.5):
            direction = 'left'
            old_motor_time = time.perf_counter()
            #print(name + ' moving ' + direction)
            
        if (direction == 'left' and readDS('left') <= 0.5):
            direction = 'backward'
            old_motor_time = time.perf_counter()
            #print(name + ' moving ' + direction)
            snake_left = False
            
        if (direction == 'backward' and time.perf_counter() - old_motor_time > 4):   # backward for 3 seconds
            if snake_left:
                direction = 'left'
            else:
                direction = 'right'
            old_motor_time = time.perf_counter()
            #print('moving ' + direction)
            
        if (direction == 'right' and readDS('right') <= 0.5):
            direction = 'backward'
            old_motor_time = time.perf_counter()
            prevent_collisions(init_time, init_front)
            #print('moving ' + direction)
            snake_left = True
       
            
        if (init == True and readDS('front') > init_front and direction == 'backward'):
            direction = 'forward'
            old_motor_time = time.perf_counter()
            force_forward = True
            #print('moving ' + direction)
        prevent_collisions(init_time, init_front)
        #print(name + ": " + direction)
        # moves motors after reset time
        if (reset_motors(old_motor_time)):
                
            if (direction == 'forward'):
                forward(10)
            elif (direction == 'left'):
                 left(10)
            elif (direction == 'right'):
                 right(10)
            elif (direction == 'backward'):
                 backward(10)
            elif (direction == 'stop'):
                 pass

        pass
    
    # Enter here exit cleanup code.
    s.close()
    