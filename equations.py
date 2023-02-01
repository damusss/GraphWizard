import pygame,sympy,random
from settings import *

# linear equation
class Equation:
    def __init__(self,is_x,equation_str,color,condition):
        self.equation = str(equation_str)
        self.color = color
        self.is_x = is_x
        self.condition = condition
    
    @external
    def render_x(self,scale,offset,step,x,end,locals,surface,view):
        last_point = None
        while x < end:
            #y = self.get_y(x)
            try:
                locals["x"] = x
                y = -eval(self.equation,GLOBALS,locals)
                
                p = (
                    int(x*UNIT*scale+VIEW_CENTER.x*scale+offset.x*scale),
                    int(y*UNIT*scale+VIEW_CENTER.y*scale+offset.y*scale)
                )
                locals["y"] = -y
                if eval(self.condition,GLOBALS,locals):
                    if last_point != None:
                        if (p[0] >= 0 and p[0] <= VIEW_SIZE.x and p[1] >= 0 and p[1] <= VIEW_SIZE.y) or (last_point[0] >= 0 and last_point[0] <= VIEW_SIZE.x and last_point[1] >= 0 and last_point[1] <= VIEW_SIZE.y):
                            if view == 0:
                                pygame.draw.line(surface,self.color,last_point,p,1)
                            else:
                                pygame.draw.circle(surface,self.color,p,2)
                last_point = p
            except:pass
            x += step
        
            
    @external
    def render_y(self,scale,offset,step,y,end,locals,surface,view):
        last_point = None
        while y > end:
            try:
                #y = self.get_y(x)
                locals["y"] = y
                x = eval(self.equation,GLOBALS,locals)
                
                p = (
                    int(x*UNIT*scale+VIEW_CENTER.x*scale+offset.x*scale),
                    int(-y*UNIT*scale+VIEW_CENTER.y*scale+offset.y*scale)
                )
                locals["x"] = x
                if eval(self.condition,GLOBALS,locals):
                    if last_point != None:
                        if (p[0] >= 0 and p[0] <= VIEW_SIZE.x and p[1] >= 0 and p[1] <= VIEW_SIZE.y) or (last_point[0] >= 0 and last_point[0] <= VIEW_SIZE.x and last_point[1] >= 0 and last_point[1] <= VIEW_SIZE.y):
                            if view == 0:
                                pygame.draw.line(surface,self.color,last_point,p,1)
                            else:
                                pygame.draw.circle(surface,self.color,p,2)
                    
                last_point = p
                
            except:
                pass
            y -= step
                
    @external
    def destroy(self):
        del self

# not a function
class SquaredEquation:
    def __init__(self,is_x,equation_str1,equation_str2,color,condition):
        self.equation1 = str(equation_str1)
        self.equation2 = str(equation_str2)
        self.color = color
        self.is_x = is_x
        self.condition = condition
    
    @external
    def render_x(self,scale,offset,step,x,end,locals,surface,view):
        last_point1 = None
        last_point2 = None
        while x < end:
            try:
                locals["x"] = x
                y1 = eval(self.equation1,GLOBALS,locals)
                y2 = eval(self.equation2,GLOBALS,locals)
                
                p1 = (
                    int(x*UNIT*scale+VIEW_CENTER.x*scale+offset.x*scale),
                    int(y1*UNIT*scale+VIEW_CENTER.y*scale+offset.y*scale)
                )
                p2 = (
                    int(x*UNIT*scale+VIEW_CENTER.x*scale+offset.x*scale),
                    int(y2*UNIT*scale+VIEW_CENTER.y*scale+offset.y*scale)
                )
                if last_point1 != None and last_point2 != None:
                    locals["y"] = -y1
                    if eval(self.condition,GLOBALS,locals):
                        if (p1[0] >= 0 and p1[0] <= VIEW_SIZE.x and p1[1] >= 0 and p1[1] <= VIEW_SIZE.y) or (last_point1[0] >= 0 and last_point1[0] <= VIEW_SIZE.x and last_point1[1] >= 0 and last_point1[1] <= VIEW_SIZE.y):
                            if view == 0:
                                pygame.draw.line(surface,self.color,last_point1,p1,1)
                            else:
                                pygame.draw.circle(surface,self.color,p1,2)
                    locals["y"] = -y2
                    if eval(self.condition,GLOBALS,locals):
                        if (p2[0] >= 0 and p2[0] <= VIEW_SIZE.x and p2[1] >= 0 and p2[1] <= VIEW_SIZE.y) or (last_point2[0] >= 0 and last_point2[0] <= VIEW_SIZE.x and last_point2[1] >= 0 and last_point2[1] <= VIEW_SIZE.y):
                            if view == 0:
                                pygame.draw.line(surface,self.color,last_point2,p2,1)
                            else:
                                pygame.draw.circle(surface,self.color,p2,2)
                else:
                    locals["y"] = -y1
                    cond1 = eval(self.condition,GLOBALS,locals)
                    locals["y"] = -y2
                    cond2 = eval(self.condition,GLOBALS,locals)
                    if cond1 and cond2:
                        if (p1[0] >= 0 and p1[0] <= VIEW_SIZE.x and p1[1] >= 0 and p1[1] <= VIEW_SIZE.y) or (p2[0] >= 0 and p2[0] <= VIEW_SIZE.x and p2[1] >= 0 and p2[1] <= VIEW_SIZE.y):
                            if view == 0:
                                pygame.draw.line(surface,self.color,p1,p2,1)
                            else:
                                pass
                                #pygame.draw.circle(surface,self.color,p1,2)
                last_point1 = p1
                last_point2 = p2
            except:
                if last_point1 != None and last_point2 != None:
                    try:
                        locals["y"] = -y1
                        cond1 = eval(self.condition,GLOBALS,locals)
                        locals["y"] = -y2
                        cond2 = eval(self.condition,GLOBALS,locals)
                        if cond1 and cond2:
                            if (last_point2[0] >= 0 and last_point2[0] <= VIEW_SIZE.x and last_point2[1] >= 0 and last_point2[1] <= VIEW_SIZE.y) or (last_point1[0] >= 0 and last_point1[0] <= VIEW_SIZE.x and last_point1[1] >= 0 and last_point1[1] <= VIEW_SIZE.y):
                                if view == 0:
                                    pygame.draw.line(surface,self.color,last_point1,last_point2,1)
                                else:
                                    pass
                                    #pygame.draw.circle(surface,self.color,p1,2)
                    except:
                        pass
                last_point1 = None
                last_point2 = None
            x += step
            
    @external
    def render_y(self,scale,offset,step,y,end,locals,surface,view):
        last_point1 = None
        last_point2 = None
        while y > end:
            try:
                locals["y"] = y
                x1 = eval(self.equation1,GLOBALS,locals)
                x2 = eval(self.equation2,GLOBALS,locals)
                
                p1 = (
                    int(x1*UNIT*scale+VIEW_CENTER.x*scale+offset.x*scale),
                    int(-y*UNIT*scale+VIEW_CENTER.y*scale+offset.y*scale)
                )
                p2 = (
                    int(x2*UNIT*scale+VIEW_CENTER.x*scale+offset.x*scale),
                    int(-y*UNIT*scale+VIEW_CENTER.y*scale+offset.y*scale)
                )
                if last_point1 != None and last_point2 != None:
                    locals["x"] = x1
                    if eval(self.condition,GLOBALS,locals):
                        if (p1[0] >= 0 and p1[0] <= VIEW_SIZE.x and p1[1] >= 0 and p1[1] <= VIEW_SIZE.y) or (last_point1[0] >= 0 and last_point1[0] <= VIEW_SIZE.x and last_point1[1] >= 0 and last_point1[1] <= VIEW_SIZE.y):
                            if view == 0:
                                pygame.draw.line(surface,self.color,last_point1,p1,1)
                            else:
                                pygame.draw.circle(surface,self.color,p1,2)
                    locals["x"] = x2
                    if eval(self.condition,GLOBALS,locals):
                        if (p2[0] >= 0 and p2[0] <= VIEW_SIZE.x and p2[1] >= 0 and p2[1] <= VIEW_SIZE.y) or (last_point2[0] >= 0 and last_point2[0] <= VIEW_SIZE.x and last_point2[1] >= 0 and last_point2[1] <= VIEW_SIZE.y):
                            if view == 0:
                                pygame.draw.line(surface,self.color,last_point2,p2,1)
                            else:
                                pygame.draw.circle(surface,self.color,p2,2)
                else:
                    locals["x"] = -x1
                    cond1 = eval(self.condition,GLOBALS,locals)
                    locals["x"] = -x2
                    cond2 = eval(self.condition,GLOBALS,locals)
                    if cond1 and cond2:
                        if (p1[0] >= 0 and p1[0] <= VIEW_SIZE.x and p1[1] >= 0 and p1[1] <= VIEW_SIZE.y) or (p2[0] >= 0 and p2[0] <= VIEW_SIZE.x and p2[1] >= 0 and p2[1] <= VIEW_SIZE.y):
                            if view == 0:
                                pygame.draw.line(surface,self.color,p1,p2,1)
                            else:
                                pass
                                #pygame.draw.circle(surface,self.color,p1,2)
                last_point1 = p1
                last_point2 = p2
            except:
                if last_point1 != None and last_point2 != None:
                    try:
                        locals["x"] = -x1
                        cond1 = eval(self.condition,GLOBALS,locals)
                        locals["x"] = -x2
                        cond2 = eval(self.condition,GLOBALS,locals)
                        if cond1 and cond2:
                            if (last_point2[0] >= 0 and last_point2[0] <= VIEW_SIZE.x and last_point2[1] >= 0 and last_point2[1] <= VIEW_SIZE.y) or (last_point1[0] >= 0 and last_point1[0] <= VIEW_SIZE.x and last_point1[1] >= 0 and last_point1[1] <= VIEW_SIZE.y):
                                if view == 0:
                                    pygame.draw.line(surface,self.color,last_point1,last_point2,1)
                                else:
                                    pass
                                    #pygame.draw.circle(surface,self.color,p1,2)
                    except:
                        pass
                last_point1 = None
                last_point2 = None
            y -= step
                
    @external
    def destroy(self):
        del self