import pygame,json,os
from pygameUI import pygameUI
from settings import *
from graph import Graph
from inputs import *

# creates the interface and its interaction
class Interface:
    def __init__(self,manager,quit):
        self.manager = manager
        self.graph = Graph()
        self.graph.refresh_equations(
            ["y=cos(x)*2",
             "y=x**2+x**2",
             "y=x",
             "y=-x",
            "x=y**2 [x]",
            "x=sin(y)+cos(y) [x]"],
        )
        self.quit = quit
        
        self.topbar_cont = pygameUI.UIContainer(TOPBAR_RECT,self.manager,colored=True)
        self.eq_list_cont = pygameUI.UIScrollableContainer(EQ_LIST_RECT,self.manager,colored=True)
        self.eq_list_scrollbar = pygameUI.UIVerticalScrollbar(SCROLLBAR_RECT,self.manager,self.eq_list_cont)
        self.eq_list_cont.set_vertical_scrollbar(self.eq_list_scrollbar)
        self.FPS_label = pygameUI.UILabel(FPS_LABEL_RECT,self.manager,"60 FPS")
        self.close_btn = pygameUI.UIButton(CLOSE_BTN_RECT,self.manager,self.topbar_cont,"X",id="close")
        self.load_btn = pygameUI.UIDropDown(LOAD_BTN_RECT,self.manager,[""],"Load",id="load")
        self.save_dropdown = pygameUI.UIDropDown(SAVE_BTN_RECT,self.manager,["Current","As New"],"Save",id="save")
        self.new_dropdown = pygameUI.UIDropDown(NEW_BTN_RECT,self.manager,["Equation","Variable","Slider"],"New",id="new")
        self.refresh_btn = pygameUI.UIButton(REFRESH_BTN_RECT,self.manager,text="Refresh",id="refresh")
        self.view_dropdown = pygameUI.UIDropDown(VIEW_BTN_RECT,self.manager,["View Lines","View Points"],"View Lines",id="view")
        self.precision_dropdown = pygameUI.UIDropDown(PRECISION_BTN_RECT,self.manager,list(STEP_DIVIDERS.keys()),"Precision",id="precision")
        
        self.inputs:list[Input] = list()
        self.id = 0
        self.currently_loaded = -1
        self.loaded = list()
        
        self.load_start()
    
    @internal
    def save(self):
        if self.currently_loaded != -1:
            data = self.get_data()
            self.loaded[self.currently_loaded] = data
    
    @internal
    def save_as_new(self):
        data = self.get_data()
        self.loaded.append(data)
        self.currently_loaded += 1
        items = [i for i in range(len(self.loaded)-1)]
        self.load_btn.set_options(items)
    
    @external
    def save_to_files(self):
        for fil in os.listdir("saved"):
            if ".json" in fil:
                os.remove("saved/"+fil)
        for i,data in enumerate(self.loaded):
            with open("saved/"+str(i)+".json","w") as file:
                json.dump(data,file)
    
    @internal
    def get_data(self):
        equations = list()
        variables = list()
        sliders = list()
        for i in self.inputs:
            if i.inputtype == "equation":
                equations.append(i.get())
            elif i.inputtype == "varaible":
                name,val = i.get()
                variables.append({"name":name,"value":val})
            elif i.inputtype == "slider":
                name,min,cur,max = i.get_full()
                sliders.append({"name":name,"value":cur,"min":min,"max":max})
        return {"equations":equations,"variables":variables,"sliders":sliders}
    
    @internal
    def load(self,id):
        self.save()
        self.currently_loaded = int(id)
        for i in self.inputs:
            i.destroy()
        self.inputs.clear()
        curdict = self.loaded[self.currently_loaded]
        for eq in curdict["equations"]:
            self.new_input("Equation",eq=eq)
        for var in curdict["variables"]:
            self.new_input("Variable",data=var)
        for sli in curdict["sliders"]:
            self.new_input("Slider",data=sli)
        self.refresh()
    
    @internal
    def load_start(self):
        items = list()
        i = 0
        for file in os.listdir("saved"):
            if ".json" in file:
                with open("saved/"+file,"r") as iofile:
                    dict_ = json.loads(iofile.read())
                    self.loaded.append(dict_)
                items.append(str(i))
                i += 1
        self.load_btn.set_options(items)
    
    @internal
    def new_input(self,name,**kwargs):
        h = 5
        self.id += 1
        for i in self.inputs:
            h += i.height
        if name == "Equation":
            new = EquationInput(self.id,h,self.eq_list_cont,self.manager)
            if "eq" in kwargs.keys():
                new.set(kwargs["eq"])
            self.inputs.append(new)
        elif name == "Variable":
            new = VariableInput(self.id,h,self.eq_list_cont,self.manager)
            if "data" in kwargs.keys():
                new.set(kwargs["data"]["name"],kwargs["data"]["value"])
            self.inputs.append(new)
        elif name == "Slider":
            new = SliderInput(self.id,h,self.eq_list_cont,self.manager)
            if "data" in kwargs.keys():
                new.set(kwargs["data"]["name"],kwargs["data"]["min"],kwargs["data"]["value"],kwargs["data"]["max"])
            self.inputs.append(new)
        self.refresh()
    
    @internal  
    def refresh(self):
        equations = list()
        localvars = {}
        for i  in self.inputs:
            if i.inputtype == "equation":
                equations.append(i.get())
            elif i.inputtype == "variable" or i.inputtype == "slider":
                name,value = i.get()
                name = name.strip()
                if name != "" and name not in GLOBALS.keys():
                    try:
                        value = eval(value,GLOBALS)
                        localvars[name]=value
                    except Exception as e:
                        print(f"Error on variable '{name}': '{e}'")
                
        self.graph.refresh_locals(localvars)
        self.graph.refresh_equations(equations)
    
    @internal
    def delete(self,id):
        todestroy = None
        for i,input in enumerate(self.inputs):
            if input.id == id:
                todestroy = input
                w = input.height
                for newi,inp in enumerate(self.inputs):
                    if newi > i:
                        inp.move(-w)
        if todestroy != None:
            todestroy.destroy()
            self.inputs.remove(todestroy)
            del todestroy
        self.refresh()
    
    @internal
    def slider_event(self,id,is_slider):
        selected = None
        for input in self.inputs:
            if input.id == id:
                selected = input
        if selected != None:
            if is_slider:
                selected.on_slider_change()
            else:
                selected.on_value_change()
        self.refresh()
    
    @internal
    def change_precision(self,new):
        self.graph.precision = new
        self.graph.render()
    
    @external 
    def event(self,e):
        if e.type == pygameUI.BUTTON_PRESSED:
            if e.element_ID == "close":
                self.quit()
            elif e.element_ID == "refresh":
                self.refresh()
            elif e.element_ID.startswith("delete_input_"):
                id = e.element_ID.replace("delete_input_","")
                self.delete(id)
        elif e.type == pygameUI.DROPDOWN_SELECTED:
            if e.manual == False:
                if e.element_ID == "new":
                    self.new_dropdown.set_selected("New")
                    self.new_input(e.new)
                elif e.element_ID == "save":
                    if e.new == "Current":
                        self.save()
                    elif e.new == "As New":
                        self.save_as_new()
                    self.save_dropdown.set_selected("Save")
                elif e.element_ID == "view":
                    if e.new != e.old:
                        if self.graph.view == 0:
                            self.graph.view = 1
                        else:
                            self.graph.view = 0
                        self.graph.render()
                elif e.element_ID == "precision":
                    self.graph.precision = e.new
                    self.graph.render()
                    self.precision_dropdown.set_selected("Precision")
                elif e.element_ID == "load":
                    id = e.new
                    self.load(id)
                    self.load_btn.set_selected("Load")
        elif e.type == pygameUI.SLIDER_MOVED:
            if e.element_ID.startswith("slider_slider_") and not e.manual:
                self.slider_event(e.element_ID.replace("slider_slider_",""),True)
        elif e.type == pygameUI.ENTRYLINE_TEXT_CHANGED:
            if e.element_ID.startswith("slider_value_input_") and not e.manual:
                self.slider_event(e.element_ID.replace("slider_value_input_",""),False)
            elif e.element_ID.startswith("variable_name_input_") or e.element_ID.startswith("variable_value_input_") or e.element_ID.startswith("slider_name_input_") or e.element_ID.startswith("equation_input_"):
                self.refresh()