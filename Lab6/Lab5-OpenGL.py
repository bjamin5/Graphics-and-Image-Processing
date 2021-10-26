import sys

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho # Set up an orthogonal matrix
    from OpenGL.GLU import gluPerspective # Set up a perspective projection matrix
    from OpenGL.GL import glRotated # glRotate - Multiply the current matrix by a rotation matrix
    from OpenGL.GL import glTranslated # glTranslate - Multiply the current matrix by a translation matrix
    from OpenGL.GL import glLoadIdentity # Replace the current matrix with the identity matrix
    from OpenGL.GL import glMatrixMode # specify which matrix is the current matrix
    from OpenGL.GL import glPushMatrix
    from OpenGL.GL import glPopMatrix
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
    import math
    import pdb

### What is the difference between glMatrixMode(GL_MODELVIEW) and glMatrixMode(GL_PROJECTION)
# The modelview matrix defines how your objects are transformed (meaning translation, rotation
# and scaling) in your world coordinate frame

# The projection matrix defines the properties of the camera that views the objects in the world
# coordinate frame. Here you typically set the zoom factor, aspect ratio and the near and far 
# clipping planes (what pixels are off screen and which are on)

# In most cases you define the projection matrix once and use the modelview matrix all other times.

#v' = M_proj (dot) M_view (dot) M_model (dot) v
except:
    print("ERROR: PyOpenGL not installed properly. ")

x_pos = 0
y_pos = -3
z_pos = -20
angle = 0
isOrtho = False

DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0
ASPECT = DISPLAY_WIDTH / DISPLAY_HEIGHT


def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0) # sets the background color, clears screen
    glShadeModel (GL_FLAT)

def drawHouse ():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    #Floor
    glBegin(GL_LINES) # Constant specifies what kind of graphics will be in here
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    #Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    #Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    #Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    #Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()

def drawCar():
	glLineWidth(2.5)
	glColor3f(0.0, 1.0, 0.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-3, 2, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 2, 2)
	#Back Side
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 2, -2)
	#Connectors
	glVertex3f(-3, 2, 2)
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, -2)
	glEnd()
	
def drawTire():
	glLineWidth(2.5)
	glColor3f(0.0, 0.0, 1.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-1, .5, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, .5, .5)
	#Back Side
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, .5, -.5)
	#Connectors
	glVertex3f(-1, .5, .5)
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, -.5)
	glEnd()

def display():
    global x_pos,y_pos,z_pos, angle, isOrtho


    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)

    # viewing transformation 
    glLoadIdentity() # Reset all graphic/shape's position
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # pdb.set_trace()
    if isOrtho:
        glOrtho(-10.0, 10.0, -10.0, 10.0, -200.0, 200.0) 

    else:
        gluPerspective(45.0, ASPECT, 1.0, 100.0)

    """
    # (GLdouble fovy, GLdouble aspect, GLdouble zNear, GLdouble zFar)
        # fovy - specifies the field of view angle in degrees in the y direction
        # apsect - specifies the aspect ratio that determines the field of view in the x direction
        # The aspect ratio is the ratio of x (width) to y (height)
        # zFar - Specifies the distance from the viewer to the far clipping plane(always positive)
    """
    # Draw initial house
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotate(angle, 0, 1, 0) # applies rotation matrix to model
    glTranslate(x_pos, y_pos, z_pos) # applies translation matrix to model

    glPushMatrix() # Place new object relative to previous house's location
    glTranslate(x_pos + 20, y_pos, z_pos)
    drawHouse()
    glPopMatrix()

    glPushMatrix()
    glTraslate(x_pos -20, y_pos, z_pos)
    drawHouse()
    glPopMatrix

    glFlush()
    

def keyboard(key, x, y):
    global x_pos,y_pos,z_pos, angle, isOrtho
    if key == chr(27):
        import sys
        sys.exit(0)
  
    if key == b'w': # forward
        x_pos -= math.sin(angle * math.pi / 180)
        z_pos += math.cos(angle * math.pi / 180) 
        #z_pos += 1
  
    if key == b's': # back
        x_pos += math.sin(angle * math.pi / 180)
        z_pos -= math.cos(angle * math.pi / 180) 
        # z_pos -= 1

    if key == b'r': # up
        y_pos -= 1
    
    if key == b'f': # down
        y_pos += 1
    
    if key == b'a': # left
        x_pos += math.sin((angle + 90) * math.pi / 180)
        z_pos -= math.cos((angle + 90) * math.pi / 180)
        # x_pos += 1

    if key == b'd': # right
        x_pos -= math.sin((angle + 90) * math.pi / 180)
        z_pos += math.cos((angle + 90) * math.pi / 180)
        # x_pos -= 1

    if key == b'q': # rotate left
        angle -= 1

    if key == b'e': # rotate right
        angle += 1

    if key == b'h': # Return to orginal settings
        x_pos = 0
        y_pos = -3
        z_pos = -20
        angle = 0
        isOrtho = False
        print("Reverting to original settings")

    if key == b'o': # Orthogonal Mode
        isOrtho = True
        print("Switching to Orthogonal mode")
    
    if key == b'p': # Switch to Perspective move
        isOrtho = False
        print("Switching to Perspective mode")
    
    if key == b'n':
        print('x: ', x_pos)
        print('y: ', y_pos)
        print('z: ', z_pos)
        print('angle: ', angle)

    glutPostRedisplay()
    return


glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab 5')
init ()
glutDisplayFunc(display) # Draw this out all the time, not just when user interacts with window
glutKeyboardFunc(keyboard)
# PLACE glutTimerFunc here
glutMainLoop()

"""
o sum it all up, the final transformation of a vertex is the product of the model, view and projection matrices.
v' = M_proj (dot) M_view (dot) M_model (dot) v
"""
