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

#thickness washer 
t_head_bolt = { 
    "M12" : 8,
    "M16" : 10,
    "M20" : 13,
    "M24" : 15,
    "M30" : 19,
    "M36" : 23,
}

t_washer= {
    "M12" : 2.8,
    "M16" : 3.6,
    "M20" : 3.6,
    "M24" : 4.6,
    "M30" : 4.6,
    "M36" : 6, 
}


t_nuts= {
    "M12" : 11,
    "M16" : 15,
    "M20" : 18,
    "M24" : 22,
    "M30" : 26,
    "M36" : 31, 
}

a_distance= {
    "M12" : 4,
    "M16" : 4,
    "M20" : 4,
    "M24" : 4,
    "M30" : 7,
    "M36" : 7, 
}



Zakleszczenie = {
    "M12.50": 36,
    "M16.50": 32,
    "M20.60": 38,
    "M24.60": 34,
    "M27.80": 51,
    "M30.70": 39,
    "M36.110": 73,
}

#First value are taken for bolts form list Length !! 
Clamping = {
    "M12": 36,
    "M16": 32,
    "M20": 38,
    "M24": 34,
    "M27": 51,
    "M30": 39,
    "M36": 73,
}


thickness_plate = 30 

def finding_clamp(bolt_class,bolts,thickness_plate):
    #Searching for possible length
    keys = [x for x in LENGTH[bolt_class][bolts]]
    #Making proper clamp length
    searching_bolt = int(Clamping[bolts])
    clamps = list(range(searching_bolt,(searching_bolt+10*len(keys)),10))
    result = list(zip(keys,clamps))
    print(result)
    result_which_mach =[(lenght,clamp) for lenght, clamp in result if clamp >= 2 * thickness_plate]
    searching_length_of_bolt = result_which_mach[0][0]
    return searching_length_of_bolt

print(finding_clamp("10.9","M20",30))


start_points = (0, 0)
slope_girder = 10
height_girder = 1
t_top_flange = 0.01
height_column = 1
t_connection_plate = 0.03
class_bolt = "8.8"

