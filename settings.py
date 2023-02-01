# imports
import pygame,math,random

# window-related
SIZES = (1920,1080)
W,H=SIZES

def internal(func):
    """Enhances code readability."""
    return func

def external(func):
    """Enhances code readability."""
    return func

def abstract(thing):
    """Enhances code readability."""
    return thing

#colors
MAIN_BG_C = (0,0,0)
GRID_COL = (60,60,60)
INNER_GRID_COL = (25,25,25)
AXIS_COL = (200,200,200)
V = 100
EQ_I_C = (0,V,0)
VAR_NAME_I_C = (V,V,0)
VAR_VALUE_I_C = (V,0,V)
SLI_VALUE_C = (0,V,V)
FUNCTION_C = [
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,0),
    (255,0,255),
    (0,255,255),
    (255,255,255),
]

# compute more colors
def coin_flip():
    if random.randint(0,100) <= 50:
        return True
    return False

for i in range(1000):
    if coin_flip():
        r = random.randint(150,255)
    else:
        r =  0
    if r == 0:
        g = random.randint(150,255)
        b = random.randint(150,255)
    else:
        if coin_flip():
            g = random.randint(150,255)
            b = 0
        else:
            b = random.randint(150,255)
            g = 0
    new = (r,g,b)
    if new not in FUNCTION_C:
        FUNCTION_C.append(new)
    
    
# sizes, positions, constants
TOPBAR_H = 40
TOPBAR_BTN_SP = 5
EQ_LIST_TL = (0,TOPBAR_H)
EQ_LIST_H = H-TOPBAR_H
EQ_LIST_W = W/5
BTN_W = 100

TOPBAR_RECT = pygame.Rect(0,0,W,TOPBAR_H)
EQ_LIST_RECT = pygame.Rect(EQ_LIST_TL,(EQ_LIST_W+24,EQ_LIST_H))
SCROLLBAR_RECT = pygame.Rect(EQ_LIST_W,0,30,EQ_LIST_H)
VIEW_RECT = pygame.Rect(EQ_LIST_W+24,TOPBAR_H,W-EQ_LIST_W,H-TOPBAR_H)
FPS_LABEL_RECT = pygame.Rect(W-5-50-5-100,5,100,30)
CLOSE_BTN_RECT = pygame.Rect(W-5-50,5,50,30)
LOAD_BTN_RECT = pygame.Rect(5,5,BTN_W,30)
SAVE_BTN_RECT = pygame.Rect(5*2+BTN_W+30,5,BTN_W,30)
NEW_BTN_RECT = pygame.Rect(5*3+BTN_W*2+30*2,5,BTN_W,30)
REFRESH_BTN_RECT = pygame.Rect(5*4+BTN_W*3+30*3,5,BTN_W,30)
VIEW_BTN_RECT = pygame.Rect(W/2-BTN_W-30,5,BTN_W,30)
PRECISION_BTN_RECT = pygame.Rect(W/2+5,5,BTN_W,30)
if VIEW_BTN_RECT.x < REFRESH_BTN_RECT.right+5:
    old = VIEW_BTN_RECT.x
    VIEW_BTN_RECT.x = REFRESH_BTN_RECT.right+5
    PRECISION_BTN_RECT.x += VIEW_BTN_RECT.x-old

VIEW_OFFSET = pygame.Vector2(VIEW_RECT.topleft)
VIEW_SIZE = pygame.Vector2(VIEW_RECT.w,VIEW_RECT.h)
VIEW_CENTER = pygame.Vector2(VIEW_SIZE.x//2,VIEW_SIZE.y//2)

UNIT = VIEW_SIZE.x/10
SCALE_FACTOR = 0.05
STEP_DIVIDERS = {
    "Potato":10,
    "Very Low":30,
    "Low":60,
    "Medium":150,
    "High":300,
    "Ultra":600,
    "8K":2000,
    "0 FPS":10000
}
COORD_OFFSET = 10
GLOBALS = {
    "tan":math.tan,
    "cos":math.cos,
    "sin":math.sin,
    "sqrt":math.sqrt,
    "poq":math.pow,
    "log":math.log,
    "acos":math.acos,
    "asin":math.asin,
    "atan":math.atan,
    "factorial":math.factorial,
    "degrees":math.degrees,
    "radians":math.radians,
    "floor":math.floor,
    "e":math.e,
    "pi":math.pi,
    "inf":math.inf
}