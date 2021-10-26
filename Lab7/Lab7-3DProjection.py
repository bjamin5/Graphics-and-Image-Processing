import pygame
from math import pi, sin, cos, tan
import numpy as np
import pdb

def rad(x):
    """Convert degree to radians"""
    return x * (pi / 180)

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Point3D:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z
		
class Line3D():
	
	def __init__(self, start, end):
		self.start = start
		self.end = end

def loadOBJ(filename):
	
	vertices = []
	indices = []
	lines = []
	
	f = open(filename, "r")
	for line in f:
		t = str.split(line)
		if not t:
			continue
		if t[0] == "v":
			vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))
			
		if t[0] == "f":
			for i in range(1,len(t) - 1):
				index1 = int(str.split(t[i],"/")[0])
				index2 = int(str.split(t[i+1],"/")[0])
				indices.append((index1,index2))
			
	f.close()
	
	#Add faces as lines
	for index_pair in indices:
		index1 = index_pair[0]
		index2 = index_pair[1]
		lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))
		
	#Find duplicates
	duplicates = []
	for i in range(len(lines)):
		for j in range(i+1, len(lines)):
			line1 = lines[i]
			line2 = lines[j]
			
			# Case 1 -> Starts match
			if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
				if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
					duplicates.append(j)
			# Case 2 -> Start matches end
			if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
				if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
					duplicates.append(j)
					
	duplicates = list(set(duplicates))
	duplicates.sort()
	duplicates = duplicates[::-1]
	
	#Remove duplicates
	for j in range(len(duplicates)):
		del lines[duplicates[j]]
	
	return lines

def loadHouse():
    house = []
    #Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    #Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    #Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    #Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))   
    #Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
	
    return house

def loadCar():
    car = []
    #Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

    #Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
    
    #Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

    return car

def loadTire():
    tire = []
    #Front Side
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

    #Back Side
    tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

    #Connectors
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
    
    return tire

def homogenousLines(object_lines):
    """Convert the 3D (x, y, z) coords to 4-element (x, y, z, 1) homogenouse coordinates"""
    #loop through each of the coordinates
    linelist = []
    for line in object_lines:
        # Add 4th dim to start and end point
        linelist.append(Line3D([line.start.x,line.start.y, line.start.z, 1], [line.end.x, line.end.y, line.end.z, 1]))
    return linelist # list of all the lines

def objectToWorld(object_lines, object_position):
    # Use pre-defined object positions
    linelist = []
    # For each different house position
    for curr_pos in object_position:
        # For each line in the objects list of lines
        for line in object_lines:
            # Do the transformation
            new_start_pnt = np.dot(curr_pos, line.start)
            new_end_pnt = np.dot(curr_pos, line.end)
            linelist.append(Line3D(new_start_pnt, new_end_pnt))
    return linelist

def worldToCamera(object_lines, x_pos, y_pos, z_pos, rotation):
    cx = x_pos
    cy = y_pos
    cz = z_pos
    translate_matrix = np.array([[1, 0, 0, -cx],
                                [0, 1, 0, -cy],
                                [0, 0, 1, -cz],
                                [0, 0, 0,   1]])
    # Plug in normalized axis coords for camara coordinate system
    rotate_matrix = np.array([[cos(rad(rotation)), 0, -sin(rad(rotation)), 0],
                            [0, 1, 0, 0],
                            [sin(rad(rotation)), 0, cos(rad(rotation)), 0],
                            [0, 0, 0, 1]])
    # loop through object_lines and take the dot product of the transformation 
    # with the points one line at a time
    linelist = []
    for line in object_lines:
        # pdb.set_trace()
        start_pt = np.dot(rotate_matrix, np.dot(translate_matrix, line.start))
        end_pt = np.dot(rotate_matrix, np.dot(translate_matrix, line.end))
        # Store new line
        linelist.append(Line3D(start_pt, end_pt))
    return linelist

def cameraToClip(object_lines):
    # Transform the pyramid frustrum into a cube
    # Using the zoom factor I can unstretch the objects
    linelist = []
    for line in object_lines:
        # pdb.set_trace()
        start_pt = np.dot(clip_matrix, line.start)
        end_pt = np.dot(clip_matrix, line.end)
        # Before storing
        # Check if points are in view frustrum with clipping test
        w1 = start_pt[3]
        w2 = end_pt[3]

        in_frustrum_1 = clippingTest(x=start_pt[0], y=start_pt[1], z=start_pt[2], w=start_pt[3])
        in_frustrum_2 = clippingTest(x=end_pt[0], y=end_pt[1], z=end_pt[2], w=end_pt[3])
        # Store new line if in frustrum
        if in_frustrum_1 and in_frustrum_2:
            linelist.append(Line3D(start_pt, end_pt))
    
    # Check if points are in view frustrum, save if they are
    # Rather than dividing by w, compare with clipping tests
    return linelist

def clippingTest(x, y, z, w):
    if not ((x < -w) or (x > w) or (y < -w) or (y > w) or (z < -w) or (z > w)):
        # Point is inside the view frustrum
        return True
    else:
        # Point is outside the view frustrum
        return False
    
def divide_by_w(object_lines):
    linelist = []
    # Divide by W
    for line in object_lines:
        start_pt = line.start / line.start[3] # w
        end_pt = line.end / line.end[3]

        # Drop the z coordinate
        linelist.append(Line3D([start_pt[0], start_pt[1], 1], [end_pt[0], end_pt[1], 1]))
    return linelist

def toScreenCoordinates(object_lines):
    # Transform 2D Cannonical to screen coordinates
    linelist = []
    for line in object_lines:
        start_pt = np.dot(screen_matrix, line.start)
        end_pt = np.dot(screen_matrix, line.end)
        
        linelist.append(Line3D([start_pt[0], start_pt[1]], [end_pt[0], end_pt[1]]))
    return linelist

def drawHouse(object_lines, x_pos, y_pos, z_pos, angle):
    object_space = homogenousLines(object_lines)
    world_space = objectToWorld(object_space, get_house_position())
    camera_space = worldToCamera(world_space, x_pos, y_pos, z_pos, angle)
    clip_space = cameraToClip(camera_space)
    device_coords = divide_by_w(clip_space)
    screen_space = toScreenCoordinates(device_coords)

    for line in screen_space:
        pygame.draw.line(screen, GREEN, (line.start[0], line.start[1]), (line.end[0], line.end[1]))

def drawCar(object_lines, x_pos, y_pos, z_pos, angle):
    object_space = homogenousLines(object_lines)
    world_space = objectToWorld(object_space, get_car_position())
    camera_space = worldToCamera(world_space, x_pos, y_pos, z_pos, angle)
    clip_space = cameraToClip(camera_space)
    device_coords = divide_by_w(clip_space)
    screen_space = toScreenCoordinates(device_coords)

    for line in screen_space:
        pygame.draw.line(screen, BLUE, (line.start[0], line.start[1]), (line.end[0], line.end[1]))

def drawTires(object_lines, x_pos, y_pos, z_pos, angle):
    object_space = homogenousLines(object_lines)
    world_space = objectToWorld(object_space, get_tire_position())
    camera_space = worldToCamera(world_space, x_pos, y_pos, z_pos, angle)
    clip_space = cameraToClip(camera_space)
    device_coords = divide_by_w(clip_space)
    screen_space = toScreenCoordinates(device_coords)

    for line in screen_space:
        pygame.draw.line(screen, RED, (line.start[0], line.start[1]), (line.end[0], line.end[1]))
        
def get_house_position():
    return np.array([
						[[cos(pi),0,-sin(pi),0],
						 [0,1,0,0],
						 [sin(pi),0,cos(pi),20],
						 [0,0,0,1]],

						[[cos(pi),0,-sin(pi),15],
						 [0,1,0,0],
						 [sin(pi),0,cos(pi),20],
						 [0,0,0,1]],

						[[cos(pi),0,-sin(pi),-15],
						 [0,1,0,0],
						 [sin(pi),0,cos(pi),20],
						 [0,0,0,1]],

						[[1,0,0,0],
						 [0,1,0,0],
						 [0,0,1,-20],
						 [0,0,0,1]],

						[[1,0,0,15],
						 [0,1,0,0],
						 [0,0,1,-20],
						 [0,0,0,1]],

						[[1,0,0,-15],
						 [0,1,0,0],
						 [0,0,1,-20],
						 [0,0,0,1]],
					])
def get_car_position():
    car_position = np.array([
				[[1,0,0,car_offset],
				 [0,1,0,0],
				 [0,0,1,0],
				 [0,0,0,1]]
				])
    return car_position

def get_tire_position():
    # USING HIERACHICAL TRANSFORMATION
    rotation_matrix = [[cos(rad(tire_angle)),sin(rad(tire_angle)),0,0],
						 [-sin(rad(tire_angle)),cos(rad(tire_angle)),0,0],
						 [0,0,1,0],
						 [0,0,0,1]]

    tire1 = rotation_matrix
    tire2 = rotation_matrix
    tire3 = rotation_matrix
    tire4 = rotation_matrix

    tires_position = np.array([
                    [[1,0,0,2 + car_offset],
                    [0,1,0,0],
                    [0,0,1,-2],
                    [0,0,0,1]],

                    [[1,0,0,-2 + car_offset],
                    [0,1,0,0],
                    [0,0,1,2],
                    [0,0,0,1]],

                    [[1,0,0,2 + car_offset],
                    [0,1,0,0],
                    [0,0,1,2],
                    [0,0,0,1]],

                    [[1,0,0,-2 + car_offset],
                    [0,1,0,0],
                    [0,0,1,-2],
                    [0,0,0,1]]
                    ])
    
    # Rotate first then translate
    tires_position[0] = np.dot(tires_position[0], tire1)
    tires_position[1] = np.dot(tires_position[1], tire2)
    tires_position[2] = np.dot(tires_position[2], tire3)
    tires_position[3] = np.dot(tires_position[3], tire4)


    return tires_position

def animate_car():
        # Animate Car
        global car_offset, tire_angle
        car_offset += .5
        tire_angle += 10
        # print('its working')

# Initialize the game engine
pygame.init()
# Inititalize animation
car_animation = pygame.USEREVENT + 1
# pygame.time.event[car_animation] = animate_car
pygame.time.set_timer(car_animation, 500)
# Define the colors we will use in RGB format
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE =  (0,0,255)
GREEN = (0,255,0)
RED =   (255,0,0)

# Set the height and width of the screen
size = [512, 512]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Lab 7")
 
# Set needed variables #
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)
# Load models
house_list = loadHouse()
car_list = loadCar()
tire_list = loadTire()
# Position Variables
x_pos = 78
y_pos = 10
z_pos = 6
car_offset = 0
tire_angle = 0
angle = -90
fov = rad(60) # 60 degrees in both directions
zoom_x = 1 / (tan(fov/2))
zoom_y = zoom_x # 1.73
n = 0 # near plane
f = 1000 # far plane
clip1 = (f+n)/(f-n) # 1.002
clip2 = (-2*n*f)/(f - n) # -2.002

clip_matrix = np.array([[zoom_x, 0, 0, 0],
                        [0, zoom_y, 0, 0],
                        [0, 0, clip1, clip2],
                        [0, 0, 1, 0]])
# pdb.set_trace()
screen_matrix = np.array([[512/2, 0, 512/2],
                          [0, -512/2, 512/2],
                          [0, 0, 1]])
#Add timer info

#Loop until the user clicks the close button.


while not done:
    clock.tick(100)
    # This limits the while loop to a max of 100 times per second.
    # Leave this out and we will use all CPU we can.
    # Clear the screen and set the screen background
    screen.fill(BLACK)

    # Check the event queue
    if pygame.event.get(car_animation): # check if event queue contains car_animation
        animate_car()

    #Controller Code#
    #####################################################################
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_w]:
        x_pos += sin(rad(angle))
        z_pos += cos(rad(angle)) 
        # print("w - forward")
        
    if pressed[pygame.K_s]:
        x_pos -= sin(rad(angle))
        z_pos -= cos(rad(angle)) 
        # print("s - forward")

    if pressed[pygame.K_d]:
        x_pos += cos(rad(angle))
        z_pos -= sin(rad(angle))
        # print("d - right")
        
    if pressed[pygame.K_a]:
        x_pos -= cos(rad(angle))
        z_pos += sin(rad(angle))
        # print("a - left")

    if pressed[pygame.K_r]:
        y_pos += 1
        # print("r - up")

    if pressed[pygame.K_f]:
        y_pos -= 1
        # print("f - down")

    if pressed[pygame.K_q]:
        angle -= 1
        # print("q - rotate left")
    if pressed[pygame.K_e]:
        angle += 1
        # print("e - rotate right")

    # if pressed[pygame.K_y]:
    #     print('x:',x_pos)
    #     print('y:',y_pos)
    #     print('z:',z_pos)
    #     print('angle:',angle)
    #     # print("e - rotate right")

    if pressed[pygame.K_h]:
        x_pos = 78
        y_pos = 10
        z_pos = 6
        car_offset = 0
        tire_angle = 0
        angle = -90

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            done = True

    #Viewer Code#
    #####################################################################       
    
    drawHouse(house_list, x_pos, y_pos, z_pos, angle)
    drawCar(car_list, x_pos, y_pos, z_pos, angle)
    drawTires(tire_list, x_pos, y_pos, z_pos, angle)
    # for line in linelist:
    #     pygame.draw.line(screen, BLUE, (20 * line.start.x + 200, -20*line.start.y+200), (20 * line.end.x + 200, -20*line.end.y+200))
    # for s in linelist:
    #     #BOGUS DRAWING PARAMETERS SO YOU CAN SEE THE HOUSE WHEN YOU START UP
    #     pygame.draw.line(screen, BLUE, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()   
 
# Be IDLE friendly
pygame.quit()
