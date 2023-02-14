from tkinter import *
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


LENGTH = {
    "8.8": {
        "M12": (40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200),
        "M16": (50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 180, 200),
        "M20": (50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200),
        "M24": (60, 70, 80, 90, 100, 110, 120, 150, 160, 180, 200),
        "M27": (60, 70, 80, 90, 100, 110, 120, 150, 160, 180, 200),
        "M30": (70, 80, 90, 100, 110, 120, 130, 140),
        "M36": (90, 100, 110, 120, 130, 200),
    },


    "10.9": {
        "M12": (50, 60, 70, 80, 90),
        "M16": (50, 60, 70, 80, 90, 100, 180),
        "M20": (60, 70, 80, 90, 100, 110, 120, 140),
        "M24": (60, 70, 80, 90, 100, 110, 120, 140),
        "M27": (60, 70, 80, 90, 100, 110, 120, 140),
        "M30": (70, 80, 90, 100, 110, 120, 130, 140, 150),
        "M36": (110, 120, 140, 150),
    }
}


#czyli jesli teraz zmienie ? 

# thickness washer
T_HEAD_BOLT = {
    "M12": 8,
    "M16": 10,
    "M20": 13,
    "M24": 15,
    "M27": 17,
    "M30": 19,
    "M36": 23,
}


# thickness washer
T_WIDTH_BOLT = {
    "8.8": {
        "M12": 20,
        "M16": 24,
        "M20": 30,
        "M24": 36,
        "M27": 44,
        "M30": 46,
        "M36": 50,
    },
    "10.9": {
        "M12": 22,
        "M16": 27,
        "M20": 32,
        "M24": 41,
        "M27": 46,
        "M30": 50,
        "M36": 60,
    }}
# thickness washer
T_WASHER = {
    "M12": 2.8,
    "M16": 3.6,
    "M20": 3.6,
    "M24": 4.6,
    "M30": 4.6,
    "M36": 6,
}

T_NUTS = {
    "M12": 11,
    "M16": 15,
    "M20": 18,
    "M24": 22,
    "M30": 26,
    "M36": 31,
}

A_DISTANCE = {
    "M12": 4,
    "M16": 4,
    "M20": 4,
    "M24": 4,
    "M30": 7,
    "M36": 7,
}

# First value are taken for bolts form list Length !!
Clamping = {
    "M12": 36,
    "M16": 32,
    "M20": 38,
    "M24": 34,
    "M27": 51,
    "M30": 39,
    "M36": 73,
}
root = Tk()
root.title("Distance checker")
WIDTH = "800"
HEIGHT = "500"
root.geometry(f"{WIDTH}x{HEIGHT}")


start_points = (0, 0)
slope_girder = 10
height_girder = 1
t_top_flange = 0.01
height_column = 1
t_connection_plate = 0.03
class_bolt = "8.8"

# x and y values

# Create function to execute


def getting_value():
    global slope_girder
    global height_girder
    global t_top_flange
    global height_column
    global t_connection_plate
    global diameter_bolt
    global class_bolt
    try:
        slope_girder = float(f_slope_girder.get())
        height_girder = int(f_girder_height.get())*0.001
        t_top_flange = int(f_t_flange_ridge.get())*0.001
        height_column = int(f_column_width.get())*0.001
        t_connection_plate = int(f_t_connection_plate.get())*0.001
        diameter_bolt = used_bolt.get()
        class_bolt = ussed_class.get()
    except ValueError:
        print("error")


def searching_length(class_bolt, bolt, t_plate):

    new_list = []
    basic_length = 2*T_WASHER[bolt] + T_NUTS[bolt] + \
        (2*t_plate*1000) + A_DISTANCE[bolt]
    for x in LENGTH[class_bolt][bolt]:
        if x > basic_length:
            new_list.append(x)
    searched_length_of_bolt = (new_list[0])*0.001 + (T_HEAD_BOLT[bolt])*0.001
    return searched_length_of_bolt


def finding_clamp(class_bolt, bolt, thickness_plate):
    # Searching for possible length
    keys = [x for x in LENGTH[class_bolt][bolt]]
    # Making proper clamp length
    searching_bolt = int(Clamping[bolt])
    clamps = list(range(searching_bolt, (searching_bolt+10*len(keys)), 10))
    result = list(zip(keys, clamps))
    result_which_mach = [(lenght, clamp) for lenght,
                         clamp in result if clamp > 2 * thickness_plate*1000]
    searched_length_of_bolt = (
        result_which_mach[0][0])*0.001 + (T_HEAD_BOLT[bolt])*0.001
    return searched_length_of_bolt


def min_distance(class_bolt, distance, bolt):

    offset = 0.5*T_WIDTH_BOLT[class_bolt][bolt] + (distance*1000)
    return int(offset)


def myclick():
    getting_value()
    if class_bolt == "10.9":
        distance = finding_clamp(class_bolt, diameter_bolt, t_connection_plate)
    else:
        distance = searching_length(
            class_bolt, diameter_bolt, t_connection_plate)
    # drawings first line top flange column
    A = Point(start_points[0], start_points[1])
    B = Point(start_points[0], start_points[0]-2)
    line_ab = LineString([A, B])

    # drawings second line bottom flange column

    line_cd = line_ab.parallel_offset(height_column, "left")

    C = Point(line_cd.coords[0])
    D = Point(line_cd.coords[1])

    # drawings third line top flange
    E = Point(2, (math.tan(math.radians(slope_girder)))*2)
    line_ae = LineString([A, E])
    flange_ae = line_ae.parallel_offset(t_top_flange, "right")

    # drawings forth line bottom flange
    line_fg = line_ae.parallel_offset(height_girder, "right")

    F = Point(line_fg.coords[0])
    G = Point(line_fg.coords[1])

    # drawings line for connection
    H = line_cd.intersection(line_fg)
    line_ah = LineString([A, H])

    # bottom_flange_view_ridge
    line_gh = LineString([G, H])

    # bottom_flange_view_column
    line_dh = LineString([D, H])

    # offset to find distance for bolts height

    line_ij = line_ah.parallel_offset(distance + t_connection_plate, "left")

    # intersection height of bolt and flange

    K = line_ij.intersection(flange_ae)

    L = nearest_points(line_ah, K)

    line_kl = LineString([K, L[0]])

    looking_value = A.distance(L)

    fig = Figure(figsize=(3, 3), dpi=100)

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(
        *line_ab.xy,
        # *line_cd.xy
        *line_ae.xy,
        *line_ae.xy,
        # *line_fg.xy
        # *flange_ae.xy
        *line_ah.xy,
        *line_kl.xy,
        # *line_ij.xy,
        *line_gh.xy,
        *line_dh.xy
    )
    # Make axis equal
    plot1.axis('equal')

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=root)

    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=10, column=0, columnspan=2)

    # printing output
    result = min_distance(class_bolt, looking_value[0], diameter_bolt)
    result_label = Label(root, text=result)
    result_label.grid(row=9, column=1, sticky="W")
    result_label1 = Label(root, text="Searching value",
                          font='Helvetica 10 bold')
    result_label1.grid(row=9, column=0, sticky="E")

# Create text boxes


f_slope_girder = Entry(root, width=20)
f_slope_girder.grid(row=0, column=1, padx=20),
f_slope_girder.insert(0, "10.5")

f_girder_height = Entry(root, width=20)
f_girder_height.grid(row=1, columnspan=1, column=1, padx=20)
f_girder_height.insert(0, "900")

f_t_flange_ridge = Entry(root, width=20)
f_t_flange_ridge.grid(row=2, column=1, padx=20)
f_t_flange_ridge.insert(0, "20")

f_column_width = Entry(root, width=20)
f_column_width.grid(row=3, column=1, padx=20)
f_column_width.insert(0, "900")

f_t_flange_column = Entry(root, width=20)
f_t_flange_column.grid(row=4, column=1, padx=20)
f_t_flange_column.insert(0, "20")

f_t_connection_plate = Entry(root, width=20)
f_t_connection_plate.grid(row=5, column=1, padx=20)
f_t_connection_plate.insert(0, "30")

#f_used_bolt = Entry(root, width=20)
#f_used_bolt.grid(row=6, column=1, padx=20)
#f_used_bolt.insert(0, "M16")

ussed_class = StringVar(root)
ussed_class.set("Select class")
possible_class = [x for x in LENGTH]
f_ussed_class = OptionMenu(root, ussed_class, *possible_class)
f_ussed_class.grid(row=6, column=1, sticky="N")

# Variable to keep track of the option
# selected in OptionMenu
used_bolt = StringVar(root)
possible_bolts = [x for x in LENGTH[class_bolt]]
# Set the default value of the variable
used_bolt.set("Select an bolt")
f_used_bolt = OptionMenu(root, used_bolt, *possible_bolts)
f_used_bolt.grid(row=6, column=2, sticky="N")

# Create text labels
slope_girder_units = Label(root, text="Degree []",)
slope_girder_units.grid(row=0, column=2, sticky="W")

slope_girder_label = Label(root, text="Insert angle of girder",)
slope_girder_label.grid(row=0, column=0, sticky="E")


girder_height_label = Label(root, text="Girder width",)
girder_height_label.grid(row=1, column=0, sticky="E")

profiles_units = Label(root, text="[mm]",)
profiles_units.grid(row=1, rowspan=5,  column=2, sticky="W")

t_flange_girder_label = Label(root, text="Thickness of flange in girder", )
t_flange_girder_label.grid(row=2, column=0, sticky="E")

column_width_label = Label(root, text="Column width",)
column_width_label.grid(row=3, column=0, sticky="E")

t_flange_column_label = Label(root, text="Thickness of flange in column",)
t_flange_column_label.grid(row=4, column=0, sticky="E")

t_connection_plate_label = Label(
    root, text="Thickness of plate in connection",)
t_connection_plate_label.grid(row=5, column=0, sticky="E")

used_bolt_label = Label(root, text="Used bolt in connection",)
used_bolt_label.grid(row=6, column=0, sticky="E")

# Create button to execute

myButton = Button(root, text="Check minimum distance", command=myclick)
myButton.grid(row=8, column=0, columnspan=2)

root.mainloop()
