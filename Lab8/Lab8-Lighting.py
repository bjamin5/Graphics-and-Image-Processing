""" Modified code from Peter Colling Ridge 
	Original found at http://www.petercollingridge.co.uk/pygame-3d-graphics-tutorial
"""

import pygame, math, pdb
import numpy as np
import wireframe as wf
import basicShapes as shape

adjust_gloss = False
adjust_specular = False
adjust_diffuse = False
gloss_coef = 20
specular_coef = .15
diffuse_coef = .75

class WireframeViewer(wf.WireframeGroup):
    """ A group of wireframes which can be displayed on a Pygame screen """
    
    def __init__(self, width, height, name="Wireframe Viewer"):
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        
        self.wireframes = {}
        self.wireframe_colours = {}
        self.object_to_update = []
        
        self.displayNodes = False
        self.displayEdges = True
        self.displayFaces = True
        
        self.perspective = False
        self.eyeX = self.width/2
        self.eyeY = 100
        self.light_color = np.array([1,1,1]) # White
        self.view_vector = np.array([0, 0, -1])        
        self.light_vector = np.array([0, 0, -1])  

        self.background = (10,10,50)
        self.nodeColour = (250,250,250)
        self.nodeRadius = 4
        
        self.control = 0
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
        #   If colour is set to None, then wireframe is not displayed
        self.wireframe_colours[name] = (250,250,250)
    
    def addWireframeGroup(self, wireframe_group):
        # Potential danger of overwriting names
        for name, wireframe in wireframe_group.wireframes.items():
            self.addWireframe(name, wireframe)
    
    def display(self):
        global diffuse_coef, specular_coef, gloss_coef
        self.screen.fill(self.background)

        for name, wireframe in self.wireframes.items():
            nodes = wireframe.nodes
            
            if self.displayFaces:
                for (face, colour) in wireframe.sortedFaces():
                    v1 = (nodes[face[1]] - nodes[face[0]])[:3]
                    v2 = (nodes[face[2]] - nodes[face[0]])[:3]

                    normal = np.cross(v1, v2)
                    normal /= np.linalg.norm(normal)
                    towards_us = np.dot(normal, self.view_vector)

                    specular = [0.0, 0.0, 0.0]      
                    diffuse = [0.0, 0.0, 0.0]

                    # Only draw faces that face us
                    if towards_us > 0:
                        m_ambient = 0.1
                        ambient = self.light_color * (m_ambient * colour)

                        #Your lighting code here
                        #Make note of the self.view_vector and self.light_vector 
                        #Use the Phong model
                        specular = [0.0, 0.0, 0.0]
                        diffuse = [0.0, 0.0, 0.0]

                        if np.dot(normal, self.light_vector) > 0:
                            # Diffuse Refelction
                            # I_d = k_d * l_p * O_d * (N dot L)
                            k_d = diffuse_coef
                            l_p = self.light_color # point light source intensity
                            O_d = colour # object diffuse color
                            # diffuse reflected color
                            diffuse = k_d * l_p * O_d * np.dot(normal, self.light_vector)

                            #Specular Reflection
                            # I_s = k_s * I_p * O_s * (V dot R) ^ k_gls
                            k_s = specular_coef # specular coef
                            O_s = colour
                            R = 2 * np.dot(self.light_vector, normal) * normal - self.light_vector
                            k_gls = gloss_coef
                            # specular reflected color
                            specular = k_s * l_p * O_s * np.dot(self.view_vector, R)**(k_gls)
                            # pdb.set_trace()

                        # Phong Model
                        # l_tot = l_a + l_d + l_s
                        # pdb.set_trace()
                        # pdb.set_trace()
                        light_total = ambient + diffuse + specular

                        light_total = np.clip(light_total, 0, 255)
                        # print(light_total)

                        pygame.draw.polygon(self.screen, light_total, [(nodes[node][0], nodes[node][1]) for node in face], 0)

                if self.displayEdges:
                    for (n1, n2) in wireframe.edges:
                        if self.perspective:
                            if wireframe.nodes[n1][2] > -self.perspective and nodes[n2][2] > -self.perspective:
                                z1 = self.perspective/ (self.perspective + nodes[n1][2])
                                x1 = self.width/2  + z1*(nodes[n1][0] - self.width/2)
                                y1 = self.height/2 + z1*(nodes[n1][1] - self.height/2)
                    
                                z2 = self.perspective/ (self.perspective + nodes[n2][2])
                                x2 = self.width/2  + z2*(nodes[n2][0] - self.width/2)
                                y2 = self.height/2 + z2*(nodes[n2][1] - self.height/2)
                                
                                pygame.draw.aaline(self.screen, colour, (x1, y1), (x2, y2), 1)
                        else:
                            pygame.draw.aaline(self.screen, colour, (nodes[n1][0], nodes[n1][1]), (nodes[n2][0], nodes[n2][1]), 1)

            if self.displayNodes:
                for node in nodes:
                    pygame.draw.circle(self.screen, colour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
        
        pygame.display.flip()

    def keyEvent(self, key):
        global adjust_gloss, gloss_coef, diffuse_coef, specular_coef, adjust_specular, adjust_diffuse
        #Your code here
        if key == pygame.K_a:
            # print("a - rotate left")
            light = self.light_vector
            light= np.insert(light,3, 1)
            self.light_vector = np.dot(light, wf.rotateYMatrix(-math.pi/16))[:-1] # Get up to last element (x, y, z, 1)
        if key == pygame.K_d:
            # print("d - rotate right")
            light = self.light_vector
            light= np.insert(light,3, 1)
            self.light_vector = np.dot(light, wf.rotateYMatrix(math.pi/16))[:-1] 

        if key == pygame.K_w:
            # print("w - rotate up")
            light = self.light_vector
            light= np.insert(light,3, 1)
            self.light_vector = np.dot(light, wf.rotateXMatrix(math.pi/16))[:-1] 
        if key == pygame.K_s:
            # print("s - rotate down")
            light = self.light_vector
            light= np.insert(light,3, 1)
            self.light_vector = np.dot(light, wf.rotateXMatrix(-math.pi/16))[:-1] 
        if key == pygame.K_q:
            # print("q - rotate counterclockwise")
            light = self.light_vector
            light= np.insert(light,3, 1)
            self.light_vector = np.dot(light, wf.rotateZMatrix(math.pi/16))[:-1]
        if key == pygame.K_e:
            light = self.light_vector
            light= np.insert(light,3, 1)
            self.light_vector = np.dot(light, wf.rotateZMatrix(-math.pi/16))[:-1]
            # print("e - rotate clockwise")
        
        if key == pygame.K_g:
            adjust_gloss = True
            adjust_diffuse = False
            adjust_specular = False
            print("Increase or decrease Glossiness with Arrow Keys:")
        
        if key == pygame.K_h:
            adjust_gloss = False
            adjust_diffuse = True
            adjust_specular = False
            print("Increase or decrease Diffuse Coefficient with Arrow Keys:")

        if key == pygame.K_j:
            adjust_gloss = False
            adjust_diffuse = False
            adjust_specular = True
            print("Increase or decrease Specular Coefficient with Arrow Keys:")
        
        if key == pygame.K_p:
            print("Gloss: ", gloss_coef)
            print("Diffuse: ", diffuse_coef)
            print("Specular: ", specular_coef)
            
        if key == pygame.K_UP:
            if adjust_gloss:
                gloss_coef += 1
                print("Gloss: ", gloss_coef)
            if adjust_diffuse:
                diffuse_coef += .05
                print("Diffuse: ", diffuse_coef)
            if adjust_specular:
                specular_coef += .05
                print("Specular:", specular_coef)

        if key == pygame.K_DOWN:
                    if adjust_gloss:
                        gloss_coef -= 1
                        print("Gloss: ", gloss_coef)
                    if adjust_diffuse:
                        diffuse_coef -= .05
                        print("Diffuse: ", diffuse_coef)
                    if adjust_specular:
                        specular_coef -= .05
                        print("Specular:", specular_coef)
        return

    def run(self):
        """ Display wireframe on screen and respond to keydown events """
        
        running = True
        key_down = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key_down = event.key
                elif event.type == pygame.KEYUP:
                    key_down = None
            
            if key_down:
                self.keyEvent(key_down)
            
            self.display()
            self.update()
            
        pygame.quit()

		
resolution = 52
viewer = WireframeViewer(600, 400)
viewer.addWireframe('sphere', shape.Spheroid((300,200, 20), (160,160,160), resolution=resolution))

# Colour ball
faces = viewer.wireframes['sphere'].faces
for i in range(int(resolution/4)):
	for j in range(resolution*2-4):
		f = i*(resolution*4-8) +j
		faces[f][1][1] = 0
		faces[f][1][2] = 0
	
viewer.displayEdges = False
viewer.run()
