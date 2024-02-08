

import time, os, sys
import Tkinter
tk = Tkinter


import exceptions

class GraphicsError(exceptions.Exception):
    """Generic error class for graphics module exceptions."""
    
        

    pass

OBJ_ALREADY_DRAWN = "Object currently drawn"
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"
DEAD_THREAD = "Graphics thread quit unexpectedly"



from copy import copy
from Queue import Queue
import thread
import atexit


_tk_request = Queue(0)
_tk_result = Queue(1)
_POLL_INTERVAL = 10

_root = None
_thread_running = True
_exception_info = None

def _tk_thread():
    global _root
    _root = tk.Tk()
    _root.withdraw()
    _root.after(_POLL_INTERVAL, _tk_pump)
    _root.mainloop()

def _tk_pump():
    global _thread_running
    while not _tk_request.empty():
        command,returns_value = _tk_request.get()
        try:
            result = command()
            if returns_value:
                _tk_result.put(result)
        except:
            _thread_running = False
            if returns_value:
                _tk_result.put(None) 
            raise 
    if _thread_running:
        _root.after(_POLL_INTERVAL, _tk_pump)

def _tkCall(f, *args, **kw):
   
    if not _thread_running:
        raise GraphicsError, DEAD_THREAD
    def func():
        return f(*args, **kw)
    _tk_request.put((func,True),True)
    result = _tk_result.get(True)
    return result

def _tkExec(f, *args, **kw):
   
    if not _thread_running:
        raise GraphicsError, DEAD_THREAD
    def func():
        return f(*args, **kw)
    _tk_request.put((func,False),True)
   

def _tkShutdown():
   
    global _thread_running
    
    _thread_running = False
    time.sleep(.5) 


thread.start_new_thread(_tk_thread,())


atexit.register(_tkShutdown)


        
class GraphWin(tk.Canvas):

    """A GraphWin is a toplevel window for displaying graphics."""

    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=False):
        _tkCall(self.__init_help, title, width, height, autoflush)
 
    
    def __init_help(self, title, width, height, autoflush):
        master = tk.Toplevel(_root)
        master.protocol("WM_DELETE_WINDOW", self.__close_help)
        tk.Canvas.__init__(self, master, width=width, height=height)
        self.master.title(title)
        self.pack()
        master.resizable(0,0)
        self.foreground = "black"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self.bind("<Button-1>", self._onClick)
        self.height = height
        self.width = width
        self.autoflush = autoflush
        self._mouseCallback = None
        self.trans = None
        self.closed = False
        master.lift()
        if autoflush: _root.update()

    def __checkOpen(self):
        if self.closed:
            raise GraphicsError, "window is closed"

    def setBackground(self, color):
        """Set background color of the window"""
        self.__checkOpen()
        _tkExec(self.config, bg=color)
        
        
    def setCoords(self, x1, y1, x2, y2):
        """Set coordinates of window to run from (x1,y1) in the
        lower-left corner to (x2,y2) in the upper-right corner."""
        self.trans = Transform(self.width, self.height, x1, y1, x2, y2)

    def close(self):
        if self.closed: return
        _tkCall(self.__close_help)
        
    def __close_help(self):
        """Close the window"""
        self.closed = True
        self.master.destroy()
        _root.update()

    def isClosed(self):
        return self.closed

    

        
  
        
    def getMouse(self):
        """Wait for mouse click and return Point object representing
        the click"""
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            
            _tkCall(self.update)
            if self.isClosed(): raise GraphicsError, "getMouse in closed window"
            time.sleep(.1) 
        x,y = self.toWorld(self.mouseX, self.mouseY)
        self.mouseX = None
        self.mouseY = None
        return Point(x,y)

    def checkMouse(self):
        """Return last mouse click or None if mouse has
        not been clicked since last call"""
        if self.isClosed():
            raise GraphicsError, "checkMouse in closed window"
        _tkCall(self.update)
        if self.mouseX != None and self.mouseY != None:
            x,y = self.toWorld(self.mouseX, self.mouseY)
            self.mouseX = None
            self.mouseY = None
            return Point(x,y)
        else:
            return None
            
    def getHeight(self):
        """Return the height of the window"""
        return self.height
        
    def getWidth(self):
        """Return the width of the window"""
        return self.width
    
    def toScreen(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.screen(x,y)
        else:
            return x,y
                      
    def toWorld(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.world(x,y)
        else:
            return x,y
        
    def setMouseHandler(self, func):
        self._mouseCallback = func
        
    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self._mouseCallback:
            self._mouseCallback(Point(e.x, e.y)) 
                      
class Transform:

    """Internal class for 2-D coordinate transformations"""
    
    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        
        xspan = (xhigh-xlow)
        yspan = (yhigh-ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan/float(w-1)
        self.yscale = yspan/float(h-1)
        
    def screen(self,x,y):
        
        xs = (x-self.xbase) / self.xscale
        ys = (self.ybase-y) / self.yscale
        return int(xs+0.5),int(ys+0.5)
        
    def world(self,xs,ys):
        
        x = xs*self.xscale + self.xbase
        y = self.ybase - ys*self.yscale
        return x,y



DEFAULT_CONFIG = {"fill":"",
		  "outline":"black",
		  "width":"1",
		  "arrow":"none",
		  "text":"",
		  "justify":"center",
                  "font": ("helvetica", 12, "normal")}

class GraphicsObject:

    """Generic base class for all of the drawable objects"""
   
    
    def __init__(self, options):
       
        
        
        self.canvas = None
        self.id = None

        
        config = {}
        for option in options:
            config[option] = DEFAULT_CONFIG[option]
        self.config = config
        
    def setFill(self, color):
        """Set interior color to color"""
        self._reconfig("fill", color)
        
    def setOutline(self, color):
        """Set outline color to color"""
        self._reconfig("outline", color)
        
    def setWidth(self, width):
        """Set line weight to width"""
        self._reconfig("width", width)

    def draw(self, graphwin):

        """Draw the object in graphwin, which should be a GraphWin
        object.  A GraphicsObject may only be drawn into one
        window. Raises an error if attempt made to draw an object that
        is already visible."""

        if self.canvas and not self.canvas.isClosed(): raise GraphicsError, OBJ_ALREADY_DRAWN
        if graphwin.isClosed(): raise GraphicsError, "Can't draw to closed window"
        self.canvas = graphwin
        
        self.id = _tkCall(self._draw, graphwin, self.config)
        if graphwin.autoflush:
            
            _tkCall(_root.update)

  

    def move(self, dx, dy):

        """move object dx units in x direction and dy units in y
        direction"""
        
        self._move(dx,dy)
        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            if trans:
                x = dx/ trans.xscale 
                y = -dy / trans.yscale
            else:
                x = dx
                y = dy
            
            _tkExec(self.canvas.move, self.id, x, y)
            if canvas.autoflush:
                
                _tkCall(_root.update)
           
    def _reconfig(self, option, setting):
        
        if not self.config.has_key(option):
            raise GraphicsError, UNSUPPORTED_METHOD
        options = self.config
        options[option] = setting
        if self.canvas and not self.canvas.isClosed():
            
            _tkExec(self.canvas.itemconfig, self.id, options)
            if self.canvas.autoflush:
                
                _tkCall(_root.update)

    def _draw(self, canvas, options):
        """draws appropriate figure on canvas with options provided
        Returns Tk id of item drawn"""
        pass 

    def _move(self, dx, dy):
        """updates internal state of object to move it dx,dy units"""
        pass 
         
class Point(GraphicsObject):
    def __init__(self, x, y):
        GraphicsObject.__init__(self, ["outline", "fill"])
        self.setFill = self.setOutline
        self.x = x
        self.y = y
        
    def _draw(self, canvas, options):
        x,y = canvas.toScreen(self.x,self.y)
        return canvas.create_rectangle(x,y,x+1,y+1,options)
        
    def _move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        
    def clone(self):
        other = Point(self.x,self.y)
        other.config = self.config.copy()
        return other
                
    def getX(self): return self.x
    def getY(self): return self.y

class _BBox(GraphicsObject):
   
    
    def __init__(self, p1, p2, options=["outline","width","fill"]):
        GraphicsObject.__init__(self, options)
        self.p1 = p1.clone()
	self.p2 = p2.clone()

    def _move(self, dx, dy):
        self.p1.x = self.p1.x + dx
        self.p1.y = self.p1.y + dy
        self.p2.x = self.p2.x + dx
        self.p2.y = self.p2.y  + dy
                
    def getP1(self): return self.p1.clone()

    def getP2(self): return self.p2.clone()
    
    def getCenter(self):
        p1 = self.p1
        p2 = self.p2
        return Point((p1.x+p2.x)/2.0, (p1.y+p2.y)/2.0)
    
class Rectangle(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)
    
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_rectangle(x1,y1,x2,y2,options)
        
    def clone(self):
        other = Rectangle(self.p1, self.p2)
        other.config = self.config.copy()
        return other
        
class Oval(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)
        
    def clone(self):
        other = Oval(self.p1, self.p2)
        other.config = self.config.copy()
        return other
   
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_oval(x1,y1,x2,y2,options)
    
class Circle(Oval):
    
    def __init__(self, center, radius):
        p1 = Point(center.x-radius, center.y-radius)
        p2 = Point(center.x+radius, center.y+radius)
        Oval.__init__(self, p1, p2)
        self.radius = radius
        
    def clone(self):
        other = Circle(self.getCenter(), self.radius)
        other.config = self.config.copy()
        return other
        
    def getRadius(self):
        return self.radius
              
class Line(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2, ["arrow","fill","width"])
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill
   
    def clone(self):
        other = Line(self.p1, self.p2)
        other.config = self.config.copy()
        return other
	
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_line(x1,y1,x2,y2,options)
        
    def setArrow(self, option):
        if not option in ["first","last","both","none"]:
            raise GraphicsError, BAD_OPTION
        self._reconfig("arrow", option)
        


class Text(GraphicsObject):
    
    	def __init__(self, p, text):
    		GraphicsObject.__init__(self, ["justify","fill","text","font"])
    		self.setText(text)
    		self.anchor = p.clone()
    		self.setFill(DEFAULT_CONFIG['outline'])
                self.setOutline = self.setFill
    		
    	def _draw(self, canvas, options):
    		p = self.anchor
    		x,y = canvas.toScreen(p.x,p.y)
    		return canvas.create_text(x,y,options)
    		
    	def _move(self, dx, dy):
    		self.anchor.move(dx,dy)
    		
    	def clone(self):
    		other = Text(self.anchor, self.config['text'])
    		other.config = self.config.copy()
    		return other

    	def setText(self,text):
    		self._reconfig("text", text)
    		
    	def getText(self):
    		return self.config["text"]
    	    	
    	def getAnchor(self):
    		return self.anchor.clone()

        def setFace(self, face):
            if face in ['helvetica','arial','courier','times roman']:
                f,s,b = self.config['font']
                self._reconfig("font",(face,s,b))
            else:
                raise GraphicsError, BAD_OPTION

        def setSize(self, size):
            if 5 <= size <= 36:
                f,s,b = self.config['font']
                self._reconfig("font", (f,size,b))
            else:
                raise GraphicsError, BAD_OPTION

        def setStyle(self, style):
            if style in ['bold','normal','italic', 'bold italic']:
                f,s,b = self.config['font']
                self._reconfig("font", (f,s,style))
            else:
                raise GraphicsError, BAD_OPTION

        def setTextColor(self, color):
            self.setFill(color)







