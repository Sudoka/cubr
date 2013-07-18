# app.py
# Chris Barker
# CMU S13 15-112 Term Project

import Tkinter
from Tkinter import N, E, S, W, ALL, BOTH

class App(object):
    """ docstring """
    def __init__(self, width=750, height=500, name='App', bg_color = '#000000'):
        (self.width, self.height) = width, height
        self.name = name
        
        self.clock = 0
        self.dragging = False
        self.drag_val = (0,0)
        self.prev_mouse = (0,0)
        self.bg_color = bgColor

        self.create_window()
        self.bind_events()
        self.init_wrapper()
        self.timer_wrapper()
        
        self.root.mainloop()
        
    def create_window(self):
        self.root = Tkinter.Tk()
        self.root.title(self.name)
        self.canvas = Tkinter.Canvas(self.root, width=self.width,
                                     height=self.height, background=self.bg_color)
        self.canvas.pack(expand=True, fill=BOTH)
        
    def unbind_all(self):
        for event, tag in self.bindings:
            self.root.unbind(event, tag)
        self.bindings = [ ]
        
    def quit(self):
        self.unbind_all()
        self.canvas.after_cancel(self.after)
        self.root.quit()
        
    def bind_events(self):
        self.bindings = [ ('<Button-1>', self.mouse_pressed_wrapper),
            ('<KeyPress>', self.key_pressed_wrapper),
            ('<KeyRelease>', self.key_released_wrapper),
            ('<ButtonRelease-1>', self.mouse_pressed_wrapper),
            ('<B1-Motion>', self.mouse_moved_wrapper),
        ]
        
        for i in xrange(len(self.bindings)):
            event = self.bindings[i][0]
            fn = self.bindings[i][1]
            # Store the binding as the event name and the Tkinter tag
            self.bindings[i] = (event, self.root.bind(event, fn))
            
    def init_wrapper(self):
        self.delay = 20
        self.init()
    def init(self): pass
    
    def timer_fired(self): pass
    def timer_wrapper(self):
        self.redraw_all_wrapper()
        self.timer_fired()
        self.clock += 1
        self.after = self.canvas.after(self.delay, lambda: self.timer_wrapper())
    
    def redraw_all(self): pass
    def redraw_all_wrapper(self):
        self.redraw_all()

    def key_pressed(self, event): pass        
    def key_pressed_wrapper(self, event):
        if event.keysym == 'Escape':
            if hasattr(self, 'cube'):
                if self.cube.help_state != self.cube.INGAME:
                    self.cube.help_state = self.cube.INGAME
                    self.cube.redraw()
                    return
            self.quit()
        else:
            self.key_pressed(event)
            if hasattr(self, 'inCam'):
                if self.in_cam:
                    print event.keysym
            self.redraw_all_wrapper()

    def key_released(self, event): pass
    def key_released_wrapper(self, event):
        self.key_released(event)
        self.redraw_all_wrapper()
        
    def mouse_pressed(self, event): pass
    def mouse_pressed_wrapper(self, event):
        self.dragging = True
        #self.dragVal = (0,0)
        self.prev_mouse = (event.x, event.y)
        self.mouse_pressed(event)

    def mouse_moved(self, event): pass
    def mouse_moved_wrapper(self, event):
        ndx = self.drag_val[0] if abs(self.drag_val[0]) > abs(event.x-self.prev_mouse[0]) else (event.x-self.prev_mouse[0])
        ndy = self.drag_val[1] if abs(self.drag_val[1]) > abs(event.y-self.prev_mouse[1]) else (event.y-self.prev_mouse[1])
        self.drag_val = (ndx, ndy)
        self.prev_mouse = (event.x, event.y)
        self.mouse_moved(event)

    def mouse_released(self, event): pass
    def mouse_released_wrapper(self, event):
        self.mouse_released(event)
        self.dragging = False

    def __str__(self):
        return 'App object size %sx%s' % (self.width, self.height)
