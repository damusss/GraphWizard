import pygame
from pygameUI import pygameUI
from settings import *

# creates the imputs and their logic
@abstract
class Input:
    inputtype = "null"
    def __init__(self,id,top_pos,container,manager):
        self.id = str(id)
        self.top_pos = top_pos
        self.cont = container
        self.manager = manager
        self.height = 0
    
    @external
    def get(self):
        pass
    
    @external
    def destroy(self):
        pass
    
    @external
    def move(self,amount):
        pass
    
    @external
    def set(self):
        pass
        
class EquationInput(Input):
    inputtype = "equation"
    def __init__(self, id, top_pos,container,manager):
        super().__init__(id, top_pos,container,manager)
        
        self.input = pygameUI.UIEntryLine(pygame.Rect(5,self.top_pos,EQ_LIST_W-5*3-30,40),self.manager,self.cont,id="equation_input_"+self.id)
        #self.input._shape_renderer.oc = EQ_I_C
        self.delete_button = pygameUI.UIButton(pygame.Rect(EQ_LIST_W-5-30,self.top_pos,30,40),self.manager,self.cont,"X",id="delete_input_"+self.id)
        self.height = 40+5
    
    @external
    def get(self):
        return self.input.get_text()
    
    @external
    def destroy(self):
        self.input.destroy()
        self.delete_button.destroy()
    
    @external
    def move(self, amount):
        self.input.update_position(0,amount)
        self.delete_button.update_position(0,amount)
    
    @external
    def set(self,equation):
        self.input.set_text(equation)
        
class VariableInput(Input):
    inputtype = "variable"
    def __init__(self, id, top_pos,container,manager):
        super().__init__(id, top_pos,container,manager)
        
        self.nameinput = pygameUI.UIEntryLine(pygame.Rect(5,self.top_pos,EQ_LIST_W/2-5*2-30/2,40),self.manager,self.cont,id="variable_name_input_"+self.id)
        #self.nameinput._shape_renderer.oc = VAR_NAME_I_C
        self.valueinput = pygameUI.UIEntryLine(pygame.Rect(5*2+self.nameinput.relative_rect.w,self.top_pos,EQ_LIST_W/2-5*2-30/2,40),self.manager,self.cont,id="variable_value_input_"+self.id)
        #self.valueinput._shape_renderer.oc = VAR_VALUE_I_C
        self.delete_button = pygameUI.UIButton(pygame.Rect(EQ_LIST_W-5-30,self.top_pos,30,40),self.manager,self.cont,"X",id="delete_input_"+self.id)
        self.height = 40+5
    
    @external 
    def get(self):
        return (self.nameinput.get_text(),self.valueinput.get_text())
    
    @external
    def destroy(self):
        self.nameinput.destroy()
        self.valueinput.destroy()
        self.delete_button.destroy()
    
    @external  
    def move(self, amount):
        self.nameinput.update_position(0,amount)
        self.valueinput.update_position(0,amount)
        self.delete_button.update_position(0,amount)
        
    @external
    def set(self,name,value):
        self.nameinput.set_text(name)
        self.valueinput.set_text(value)
        
class SliderInput(Input):
    inputtype = "slider"
    def __init__(self, id, top_pos,container,manager):
        super().__init__(id, top_pos,container,manager)
        
        self.nameinput = pygameUI.UIEntryLine(pygame.Rect(5,self.top_pos,EQ_LIST_W/2-5*2-30/2,40),self.manager,self.cont,id="slider_name_input_"+self.id)
        #self.nameinput._shape_renderer.oc = VAR_NAME_I_C
        self.valueinput = pygameUI.UIEntryLine(pygame.Rect(5*2+self.nameinput.relative_rect.w,self.top_pos,EQ_LIST_W/2-5*2-30/2,40),self.manager,self.cont,id="slider_value_input_"+self.id)
        #self.valueinput._shape_renderer.oc = SLI_VALUE_C
        self.delete_button = pygameUI.UIButton(pygame.Rect(EQ_LIST_W-5-30,self.top_pos,30,40),self.manager,self.cont,"X",id="delete_input_"+self.id)
        self.slider = pygameUI.UISlider(pygame.Rect(5,top_pos+40+5+5,EQ_LIST_W-5*2,30),self.manager,0,1,0.5,container=self.cont,id="slider_slider_"+self.id)
        #self.slider._handle_button._shape_renderer.oc = SLI_VALUE_C
        self.height = 40+5+30
        self.set_value_as_slider()
    
    @internal
    def set_value_as_slider(self):
        self.valueinput.set_text(f"{self.slider._min}, {round(self.slider._value,2)}, {self.slider._max}")
    
    @external
    def on_slider_change(self):
        self.set_value_as_slider()
        
    @external
    def on_value_change(self):
        try:
            min,cur,max = self.valueinput.get_text().split(",")
            self.slider.set_range(eval(min),eval(max))
            self.slider.set_value(eval(cur))
        except:
            pass
    
    @external
    def get(self):
        v = "0"
        try:
            min,cur,max = self.valueinput.get_text().split(",")
            v = cur
        except:
            pass
        return (self.nameinput.get_text(),v)
    
    def get_full(self):
        v = "0.5"
        min = "0"
        max = "1"
        try:
            min,v,max = self.valueinput.get_text().split(",")
        except:pass
        return (self.nameinput.get_text(),min,v,max)
    
    @external
    def destroy(self):
        self.nameinput.destroy()
        self.valueinput.destroy()
        self.delete_button.destroy()
        self.slider.destroy()
    
    @external
    def move(self, amount):
        self.nameinput.update_position(0,amount)
        self.valueinput.update_position(0,amount)
        self.delete_button.update_position(0,amount)
        self.slider.update_position(0,amount)
        
    @external
    def set(self,name,min,cur,max):
        self.nameinput.set_text(name)
        self.valueinput.set_text(f"{min}, {cur}, {max}")
        self.on_value_change()