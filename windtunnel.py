import tkinter
import tkinter.filedialog
import pygame
import pygame_widgets
from pygame_widgets.button import Button 
pygame.init()

wind_source_rect = None
wintsourcerect_dragging = False
wind_source_active = False
simulation_runing = False
running = True
fileopen = False
asdaasd = False
svg_surface = None
svg_rect = None
dragging = False
offset_x = 0
offset_y = 0
wind_source_active = False
partickles = []
dt = []
for i in range(400):
    dt.append(0)
keeper = True
simbuttontext = "Start Simulation"

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
butotnf = []
butotnf2 = []

button1 = Button(screen, 10, 10, 85, 40, text="File", onClick=lambda: fileman(screen), inactiveColour="white", shadowDistance=4, shadowColour="black")
button2 = Button(screen, 90, 10, 90, 40, text="Shape", onClick=lambda: shapeman(screen), inactiveColour="white", shadowDistance=4, shadowColour="black")
button3 = Button(screen, 180, 10, 95, 40, text="Quit", onClick=lambda: exitprog(), inactiveColour="white", shadowDistance=4, shadowColour="black")
buttonadfadf = Button(screen, 496, 10, 190, 40, text="Create Wind Source", onClick=lambda: add_wind_source(), inactiveColour="white", shadowDistance=4, shadowColour="black")
startsim = Button(screen, 10, 640, 150, 40, text=simbuttontext, onClick=lambda: srtat(), inactiveColour="white", shadowDistance=4, shadowColour="black")

def srtat():
    global simulation_runing, simbuttontext, startsim, partickles,dt
    if wind_source_rect is None:
        print("please add a wind source to start")
        return
    if svg_surface is None:
        print("please add an svg first")
        return
    if not simulation_runing:
        print("sim started")
        simulation_runing = True
        simbuttontext = "Stop Simulation"
    else:
        print("sim stopped and reset")
        simulation_runing = False
        simbuttontext = "Start Simulation"  
        partickles = []
        dt = []
        for i in range(400):
            dt.append(0)

        if wind_source_rect is not None:
            creatparticles(wind_source_rect)
    startsim = Button(screen, 10, 640, 150, 40, text=simbuttontext, onClick=lambda: srtat(), inactiveColour="white", shadowDistance=4, shadowColour="black")


def updaterrrasdsaparticles(windsourcerect):
    global simulation_runing
    if not simulation_runing:
        for index, particle in enumerate(partickles):
            partickles[index] = [windsourcerect.x + 40, windsourcerect.y + index]


def creatparticles(windsourcerect):
    for i in range(400):
        partickles.append([windsourcerect.x + 40, windsourcerect.y + i])
        


def add_wind_source():
    global wind_source_active, wind_source_rect
    wind_source_active = True
    if wind_source_rect is None:
        wind_source_rect = pygame.Rect(322, 322, 40, 400)

def prompt_file():
    top = tkinter.Tk()
    top.withdraw()
    file_name = tkinter.filedialog.askopenfilename(parent=top, filetypes=[("SVG files", "*.svg")])
    top.destroy()
    return file_name

def exitprog():
    global running 
    running = False


def fileman(dddd):
    global fileopen
    if not fileopen:
        filecreate = Button(dddd, 10, 57, 85, 33, text="New", onClick=lambda: reset(), inactiveColour="white", shadowDistance=4, shadowColour="black")
        fileopenge = Button(dddd, 10, 96, 85, 40, text="Open", onClick=lambda: print("oepenened"), inactiveColour="white", shadowDistance=4, shadowColour="black")
        savde = Button(dddd, 10, 140, 85, 47, text="Save", onClick=lambda: print("saved"), inactiveColour="white", shadowDistance=4, shadowColour="black")
        butotnf.append(filecreate)
        butotnf.append(fileopenge)
        butotnf.append(savde)
        fileopen = True
    else:
        for btn in butotnf:
            pygame_widgets.WidgetHandler.removeWidget(btn)
        butotnf.clear()
        fileopen = False

def reset():
    global svg_surface, svg_rect, wind_source_rect, wintsourcerect_dragging, wind_source_active, running, asdaasd, dragging, offset_y, offset_x, partickles
    wind_source_rect = None
    wintsourcerect_dragging = False
    wind_source_active = False
    running = True
    asdaasd = False
    dragging = False
    offset_x = 0
    offset_y = 0
    wind_source_active = False
    svg_surface = None
    svg_rect = None
    partickles = []
    if fileopen:
        fileman(screen)
    

def shapeman(dddd):
    global asdaasd
    if not asdaasd:
        shapeopen = Button(dddd, 90, 57, 180, 33, text="Open SVG as shape", onClick=lambda: importsvg(), inactiveColour="white", shadowDistance=4, shadowColour="black")
        butotnf2.append(shapeopen)
        asdaasd = True
    else:
        for btn in butotnf2:
            pygame_widgets.WidgetHandler.removeWidget(btn)
        butotnf2.clear()
        asdaasd = False


def importsvg():
    global svg_surface, svg_rect
    fafialfe = prompt_file()
    if fafialfe:
        original_surface = pygame.image.load(fafialfe).convert_alpha()
        target_size = (400, 400)
        svg_surface = pygame.transform.smoothscale(original_surface, target_size)
        svg_rect = svg_surface.get_rect()
        svg_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    for btn in butotnf2:
        pygame_widgets.WidgetHandler.removeWidget(btn)
    butotnf2.clear()

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not simulation_runing:
                    if svg_rect is not None and svg_rect.collidepoint(event.pos):
                        dragging = True
                        offset_x = svg_rect.x - event.pos[0]
                        offset_y = svg_rect.y - event.pos[1]
                    elif wind_source_rect is not None and wind_source_rect.collidepoint(event.pos):
                        wintsourcerect_dragging = True
                        offset_x = wind_source_rect.x - event.pos[0]
                        offset_y = wind_source_rect.y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                wintsourcerect_dragging = False   
        elif event.type == pygame.MOUSEMOTION:
            if dragging and svg_rect is not None:
                svg_rect.x = event.pos[0] + offset_x
                svg_rect.y = event.pos[1] + offset_y
            if wintsourcerect_dragging and wind_source_rect is not None:
                wind_source_rect.x = event.pos[0] + offset_x
                wind_source_rect.y = event.pos[1] + offset_y
    
    if wind_source_rect is not None and keeper:
        creatparticles(wind_source_rect)
        keeper = False
    if wind_source_rect is not None and not keeper and not simulation_runing:
        updaterrrasdsaparticles(wind_source_rect)
    #simulatisonfadf affda fd fad adf f d                   commentss are funny :D
    if simulation_runing:
        updated_particles = []
        for idx, particle in enumerate(partickles):
            if not particle[0] > 700:
                updated_particles.append([particle[0] + 10, particle[1]])
                if dt[idx]+5 > 255:
                    dt[idx] = 0
                else:    
                    dt[idx] = dt[idx]+5

            else:
                updated_particles.append([wind_source_rect.x + 40, particle[1]])
                dt[idx] = 0
        partickles = updated_particles
    
    mx, my = pygame.mouse.get_pos()
    screen.fill("purple")
    if wind_source_active and wind_source_rect is not None:
        pygame.draw.rect(screen, "white", wind_source_rect)
        

    pygame_widgets.update(events)

    if svg_surface is not None and svg_rect is not None:
        screen.blit(svg_surface, svg_rect)
    for i, particle in enumerate(partickles):
        disctance = dt[i]
        pygame.draw.circle(screen, (disctance, 0, 0), (particle), 1)
    pygame.display.flip()
    clock.tick(120)

pygame.quit()