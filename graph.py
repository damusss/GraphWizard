import pygame,random, sympy
from settings import *
from equations import Equation,SquaredEquation
from pygameUI.global_input import GlobalInput

# holds the equations and draws the plane
class Graph:
    def __init__(self):
        self.surface = pygame.Surface(VIEW_SIZE)
        self.equations: list[Equation] = list()
        self.offset = pygame.Vector2()
        self.scale = 1
        self.was_clicking = False
        self.locals = {"x":0,"y":0}
        self.coordinate_font = pygame.font.SysFont("Segoe UI",15)
        self.super_offset = 0
        self.done = False
        self.view = 0
        self.precision = "High"
        self.render()
    
    @external
    def refresh_locals(self,locals):
        self.locals = locals.copy()
        self.locals["x"] = 0
        self.locals["y"] = 0
    
    @external
    def refresh_equations(self,equations_str):
        old_colors = list()
        for e in self.equations:
            old_colors.append(e.color)
            e.destroy()
        self.equations.clear()
        for i,eq in enumerate(equations_str):
            try:
                col = "black"
                if i < len(old_colors):
                    col = old_colors[i]
                else:
                    col = random.choice(FUNCTION_C)
                self.parse_equation(eq,col)
                
            except:
                pass
        self.render()
    
    @internal
    def parse_equation(self,eq,col):
        condition = "True"
        symbol = "y"
        isx = False
        if "[x]" in eq:
            symbol = "x"
            eq = eq.replace("[x]","")
            isx = True
        elif "[y]" in eq:
            eq = eq.replace("[y]","")
        left,right = eq.split("=",1)
        right = right.replace("^","**")
        left = left.replace("^","**")
        
        if "{" in right:
            right,cond = right.split("{")
            condition = cond.replace("}","")
        
        sympy_symbol = sympy.Symbol(symbol)
        
        equation = sympy.Eq(sympy.sympify(left),sympy.sympify(right))
        
        final = sympy.solve(equation,sympy_symbol)
        
        if len(final) == 1:
            self.equations.append(Equation(isx,final[0],col,condition))
        else:
            self.equations.append(SquaredEquation(isx,final[0],final[1],col,condition))
        
        del equation
        del sympy_symbol
    
    @internal
    def wheel_event(self,ey,force=False):
        oldx = (self.offset.x+VIEW_CENTER.x)*self.scale
        oldy = (self.offset.y+VIEW_CENTER.y)*self.scale
        if not force:
            self.scale += ey*SCALE_FACTOR*self.scale
            if self.scale <= 0.001:
                self.scale = 0.001
        else:
            self.scale = ey
        if self.scale <= 0:
            self.scale = 1
        newx = (self.offset.x+VIEW_CENTER.x)*self.scale
        newy = (self.offset.y+VIEW_CENTER.y)*self.scale
        dx = oldx-newx
        dy = oldy-newy
        self.offset.x += dx/self.scale
        self.offset.y += dy/self.scale
        if not force:
            self.render()

    @external
    def event(self, e):
        if e.type == pygame.MOUSEWHEEL:
            pos = GlobalInput.mouse_pos
            if VIEW_RECT.collidepoint(pos):
                self.wheel_event(e.y)
        elif e.type == pygame.MOUSEMOTION:
            if VIEW_RECT.collidepoint(GlobalInput.mouse_pos) or self.was_clicking:
                if GlobalInput.mouse_pressed[2] or self.was_clicking:
                    self.offset.x += e.rel[0]/self.scale
                    self.offset.y += e.rel[1]/self.scale
                    self.render()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if VIEW_RECT.collidepoint(GlobalInput.mouse_pos):
                self.was_clicking = True
            else:
                self.was_clicking = False
        elif e.type == pygame.MOUSEBUTTONUP:
            self.was_clicking = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_c:
                self.wheel_event(1,True)
                self.offset = pygame.Vector2()
                self.render()
    
    @external    
    def draw(self, surface):
        surface.blit(self.surface, VIEW_OFFSET)

    def render(self):
        self.surface.fill(MAIN_BG_C)
        self.render_grid()
        self.render_equations()
     
    @internal   
    def render_equations(self):
        visible_units = (VIEW_SIZE.x/UNIT)/self.scale
        visible_units_y = (VIEW_SIZE.y/UNIT)/self.scale
        step = visible_units/STEP_DIVIDERS[self.precision]
        stepy = visible_units_y/STEP_DIVIDERS[self.precision]
        
        offsetx = (self.offset.x+VIEW_CENTER.x)*self.scale
        offsety = (self.offset.y+VIEW_CENTER.y)*self.scale
        x = -(offsetx/UNIT)/self.scale
        y = (offsety/UNIT)/self.scale
        cooly = -(offsety/UNIT)/self.scale
        end = x + visible_units
        endy = y-visible_units_y
        for e in self.equations:
            if not e.is_x:
                e.render_x(self.scale,self.offset,step,x,end,self.locals,self.surface,self.view)
            else:
                e.render_y(self.scale,self.offset,stepy,y,endy,self.locals,self.surface,self.view)
        self.render_coordinates_x(x,end)
        self.render_coordinates_y(y,endy,cooly)
            
    @internal
    def render_coordinates_x(self,x,end):
        cx = 0
        if x < 0:
            if int(x) >= -4:
                realx = int(x)-1
            else:
                realx = int(x)
        else:
            realx = int(x)
        step = UNIT*self.scale
        toskip = 0
        if self.scale != 0:
            toskip = int(1/round(self.scale,int(1/self.scale)))
        if self.centered_offset_y >= 0 and self.centered_offset_y <= VIEW_SIZE.y-COORD_OFFSET*2:
            ypos = self.centered_offset_y+COORD_OFFSET
        else:
            if self.centered_offset_y < 0:
                ypos = COORD_OFFSET
            else:
                ypos = VIEW_SIZE.y-20-COORD_OFFSET
        while realx < end+1:
            if int(self.scale) >= 2:
                subdivisions = int(self.scale)
                littlestep = step/subdivisions
                xstep = 1/subdivisions
                for i in range(subdivisions):
                    t = self.coordinate_font.render(str(round(int(realx)+xstep*i,3)),True,"white")
                    pos = (cx+self.origin_offset_x+littlestep*i-t.get_width()-COORD_OFFSET,ypos)
                    if pos[0] >= 0 and pos[0] < VIEW_SIZE.x:
                        self.surface.blit(t,pos)
            elif self.scale <= 0.5 and self.scale != 0:
                if realx% toskip == 0:
                    t = self.coordinate_font.render(str(int(realx)),True,"white")
                    self.surface.blit(t,(cx+self.origin_offset_x-t.get_width()-COORD_OFFSET,ypos))
            else:
                t = self.coordinate_font.render(str(int(realx)),True,"white")
                self.surface.blit(t,(cx+self.origin_offset_x-t.get_width()-COORD_OFFSET,ypos))
            
            cx += step
            realx += 1
    
    @internal 
    def render_coordinates_y(self,y,end,cooly):
        cy = self.origin_offset_y
        realy = int(y)+1
        
        step = UNIT*self.scale
        toskip = 0
        if self.scale != 0:
            toskip = int(1/round(self.scale,int(1/self.scale)))
        mul = 1
        if self.centered_offset_x >= 20 and self.centered_offset_x <= VIEW_SIZE.x-COORD_OFFSET*2:
            xpos = self.centered_offset_x-COORD_OFFSET
        else:
            if self.centered_offset_x < 20:
                xpos = COORD_OFFSET
                mul = -1
            else:
                xpos = VIEW_SIZE.x-COORD_OFFSET
                mul = 1
        while realy > end-1:
            if int(self.scale) >= 2:
                subdivisions = int(self.scale)
                littlestep = step/subdivisions
                ystep = 1/subdivisions
                for i in range(subdivisions):
                    t = self.coordinate_font.render(str(round(int(realy)-ystep*i,3)),True,"white")
                    pos = (xpos-t.get_width()*mul,cy+self.origin_offset_y*0+littlestep*i+t.get_height()-COORD_OFFSET)
                    if pos[1] >= 0 and pos[1] < VIEW_SIZE.y:
                        self.surface.blit(t,pos)
            elif self.scale <= 0.5 and self.scale != 0:
                if realy% toskip == 0:
                    t = self.coordinate_font.render(str(int(realy)),True,"white")
                    self.surface.blit(t,(xpos-t.get_width()*mul,cy+self.origin_offset_y*0+t.get_height()-COORD_OFFSET))
            else:
                t = self.coordinate_font.render(str(int(realy)),True,"white")
                self.surface.blit(t,(xpos-t.get_width()*mul,cy+self.origin_offset_y*0+t.get_height()-COORD_OFFSET))
            cy += step
            realy -= 1

    @internal
    def render_grid(self):
        step = UNIT*self.scale
        subdivisions = 0
        if int(self.scale) >= 2:
            subdivisions = int(self.scale)
            littlestep = step/subdivisions
        
        if step <= 20:
            self.render_axis()
            return
        
        v_line_amount = int(VIEW_SIZE.x/step)
        h_line_amount = int(VIEW_SIZE.y/step)
        
        self.origin_offset_x = self.offset.x*self.scale-int(self.offset.x/UNIT)*step
        self.origin_offset_y = self.offset.y*self.scale-int(self.offset.y/UNIT)*step-self.super_offset*self.scale
        
        for col in range(v_line_amount + 2):
            x = self.origin_offset_x + col * step
            if subdivisions != 0:
                for iv in range(subdivisions):
                    xpos = x+iv*littlestep
                    if xpos >= 0 and xpos <= VIEW_SIZE.x:
                        pygame.draw.line(self.surface,INNER_GRID_COL,(xpos,0),(xpos,VIEW_SIZE.y))
            pygame.draw.line(self.surface, GRID_COL,
                                (x, 0), (x, VIEW_SIZE.y))
            
        for row in range(h_line_amount + 2):
            if row == 4 and not self.done:
                self.centered_offset_y = (self.offset.y + VIEW_CENTER.y)*self.scale
                self.super_offset = (self.origin_offset_y + row * step)-self.centered_offset_y
                self.done = True
            y = self.origin_offset_y + row * step
            if subdivisions != 0:
                for ih in range(subdivisions):
                    ypos = y+ih*littlestep
                    if ypos >= 0 and ypos <= VIEW_SIZE.y:
                        pygame.draw.line(self.surface,INNER_GRID_COL,(0,ypos),(VIEW_SIZE.x,ypos))
            pygame.draw.line(self.surface,GRID_COL, (0,y), (VIEW_SIZE.x,y))
        self.render_axis()
    
    @internal    
    def render_axis(self):
        self.centered_offset_x = (self.offset.x + VIEW_CENTER.x)*self.scale
        self.centered_offset_y = (self.offset.y + VIEW_CENTER.y)*self.scale
        if self.centered_offset_x >= 0 and self.centered_offset_x <= VIEW_SIZE.x:
            pygame.draw.line(self.surface,AXIS_COL,(self.centered_offset_x,0),(self.centered_offset_x,VIEW_SIZE.y),2)
        if self.centered_offset_y >= 0 and self.centered_offset_y <= VIEW_SIZE.y:
            pygame.draw.line(self.surface,AXIS_COL,(0,self.centered_offset_y),(VIEW_SIZE.x,self.centered_offset_y),2)