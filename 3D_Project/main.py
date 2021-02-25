from pyglet.gl import *                                     #importing relavent pyglet components

class Triangle:                                             #creates a triangle class to hold the information about the vertices that make up the triangle
    def __init__(self):
        self.vertices = pyglet.graphics.vertex_list(3,\
        ('v3f',[-0.5,-0.5,0.0, -0.5,0.0,0.0, 0.0,0.5,0.0]), 
        ('c3B', [100,200,220, 200,110,100, 100,250,100]))

class MyWindow(pyglet.window.Window):                       #creates the window class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400,300)                      #minimum size (in pixels) of the window (prevents crash when shrinking window too small)
        glClearColor(0.2,0.3,0.2,1.0)                       #sets the colour of the background of the window
        self.triangle = Triangle()                          #sets an attribute of the window "triangle" to be the triangle object

    def on_draw(self):
        self.clear()                                        #clears the window
        self.triangle.vertices.draw(GL_TRIANGLES)           #draws the triangle with GL_TRIANGLES draw mode

    def on_resize(self,width, height):                      #allows the window to be resized
        glViewport(0,0,width,height)

if __name__ == "__main__":
    window = MyWindow(1080, 720, "Pyglet Window", resizable = True) #creates a window using the window class
    pyglet.app.run()                                                #pyglet function calling on_draw and on_resize as needed