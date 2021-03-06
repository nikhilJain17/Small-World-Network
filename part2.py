import tkinter as tk
import random
from math import sqrt

# generate one wire according to section 2.1 of paper
# returns list of [p1, p2] where p1 and p2 are tuples


	# FOR TESTING
	# TEST TEST TEST
	# DELETE LATER

random.seed(9)

def generate_wire(l):
    
	# FOR TESTING
	# TEST TEST TEST
	# DELETE LATER

    # q1 and q2 are distinct values of random var Q
    # Q is discrete cont. random var over [0,3]
    # the purpose of q1 and q2 is to "anchor" a wire's endpoints 
    # to distinct sides of the simulation
    q1 = -1
    q2 = -1
    
    while q1 == q2:
        q1 = random.randint(0,3)
        q2 = random.randint(0,3)
        
#     print("Q values: ", q1, q2)
    
    # x1, y1, x2, y2 are the endpoints of the wire
    # they are from uniform rand var T over [0, l]
    x1 = random.uniform(0, l)
    x2 = random.uniform(0, l)
    y1 = random.uniform(0, l)
    y2 = random.uniform(0, l)
    
#     print("Initial endpoints:", x1, y1, x2, y2)
    
    # apply the adjustment table to q1, q2 to anchor endpoints
    # @TODO clean this code up
    if q1 == 0:
        y1 = 0
    elif q1 == 1:
        x1 = 0
    elif q1 == 2:
        y1 = l
    elif q1 == 3:
        x1 = l
        
    # handle q2
    if q2 == 0:
        y2 = 0
    elif q2 == 1:
        x2 = 0
    elif q2 == 2:
        y2 = l
    elif q2 == 3:
        x2 = l
        
    p1 = (x1, y1)
    p2 = (x2, y2)
    
#     print("P1:", p1)
#     print("P2:", p2)
    
    return[p1, p2]
    
            
# determine if an electrode is touching a wire
# takes in tuple of coordinates of electrode
# takes in list of tuples of endpoints of wire
def electrode_touching_wire(electrode_points, wire_points, r_e):
    # the formula for min distance between wire and electrode is given in sec 2.1
    
    x_e, y_e = electrode_points
    x1, y1 = wire_points[1]
    x2, y2 = wire_points[0]
    
#     numerator = abs(x_e * (y2 - y1) - y_e * (x2 - x1) + x2 * y1 - y2 * x1)
#     denominator = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
#     distance = numerator / denominator
    
    numer = abs(x_e * (y2 - y1) - y_e * (x2 - x1) + x2 * y1 - y2 * x1)
    denom = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
    
    distance = numer / denom
    
    # wire is touching if min distance is less than electrode radius
    return distance <= r_e
# determine if two electrodes share the same wire
def adjacent_electrodes(electrode1, electrode2, electrode_wire_dict):

    for wire1 in electrode_wire_dict[electrode1]:
        for wire2 in electrode_wire_dict[electrode2]:
        	# check if wire start/end points are equal
        	s1, e1 = wire1[0], wire1[1]
        	s2, e2 = wire2[0], wire2[1]
        	
        	equal_starts = (s1[0] == s2[0] and s1[1] == s2[1])
        	equal_ends = (e1[0] == e2[0] and e1[1] == e2[1])

        	if equal_starts and equal_ends:
        		return 1
        
    return 0


# function to make gui to show simulation
def gui(adjacency_matrix, electrodes, wires, r_e, l):

	WINDOW_SIZE = 800
	# CANVAS_SIZE = 700
	# delete?
	scaled_unit = WINDOW_SIZE / l

	n_e = len(electrodes)
	n_w = len(wires)

	# dynamically scale radius based on number of electrodes
	# so that the electrodes all fit on the screen
	scaled_radius = r_e * WINDOW_SIZE / (n_e + 1)

	base = tk.Tk()
	base.resizable(width=False, height=False)

	# add gui components
	canvas = tk.Canvas(master=base, width=WINDOW_SIZE, height=WINDOW_SIZE, bg='white')

	# draw electrodes
	# spacing = WINDOW_SIZE / n_e

	counter = 0
	for electrode in electrodes:
		center_x = electrode[0] * WINDOW_SIZE
		center_y = electrode[1] * WINDOW_SIZE
		# drawing function takes in a bounding box, not center and radius
		canvas.create_oval(center_x, center_y,
			center_x + scaled_radius, center_y + scaled_radius, outline="#f11", 
			fill="#f11", width=scaled_radius)
		canvas.create_text(center_x + 0.5 * scaled_radius, 
			center_y + 0.5 * scaled_radius, text=str(counter))
		counter += 1

	# draw wires
	for wire in wires:
		start_x = l - wire[0][0]
		start_y = l - wire[0][1]
		end_x = l - wire[1][0]
		end_y = l - wire[1][1]

		# scale 

		# DRAWING WIRES OPPOSITE????
		# TOP LEFT IS 0,0
		# TODO FIX FIX FIX FIX FIX FIX FIX DRAWING WIRES!!!!!!!!!!!!!!

		# scaled_start_x = (start_x / l) * WINDOW_SIZE
		# scaled_start_y = (start_y / l) * WINDOW_SIZE
		scaled_start_x = start_y * (WINDOW_SIZE / l)
		scaled_start_y = start_x * (WINDOW_SIZE / l)
		scaled_end_x = (end_y / l) * WINDOW_SIZE
		scaled_end_y = (end_x / l) * WINDOW_SIZE

		canvas.create_line(scaled_start_x, scaled_start_y, scaled_end_x, scaled_end_y,
			width=3, fill="blue")

	canvas.pack()

	base.mainloop()



# main backend function to generate wires, electrodes, and adj matrix
def generate_simulation(a=1, r_e=0.4, n_e=9, lambda_constant=3):
        
    # height/width of grid
    l = a * (1 + sqrt(n_e)) 
    
    # number of wires
    n_w = int(lambda_constant * sqrt(n_e))
    
    # generate wire coordinates
    wires = []
    for i in range(n_w):
        wires.append(generate_wire(l))

    print("___________________________")
    print("Wires:")
    print("___________________________")
    for w in wires:
    	print(w)
        
    # generate electrode coordinates
    # they are evenly spaced out along the lxl grid
    electrodes = []
    sqrt_ne = int(sqrt(n_e))
    for i in range(sqrt_ne):
        for j in range(sqrt_ne):
            x = i * (l / n_e)
            y = j * (l / n_e)
            electrodes.append((x, y))
        
    # generate dictionaries of electrodes and the wires they touch
    electrode_wire_dict = {}

    # TEST TEST TEST TEST
    # testing electrode_touching_wire
    # ex, ey = electrodes[8]
    # wire_x1 = 0
    # wire_x2 = l
    # wire_y1 = ey
    # wire_y2 = ey

    # wires = []
    # wires.append([(wire_x1, wire_y1), (wire_x2, wire_y2)])

    for electrode in electrodes:
        wires_touching = []
        for wire in wires:
            if electrode_touching_wire(electrode, wire, r_e):
                wires_touching.append(wire)
            electrode_wire_dict[electrode] = wires_touching
        del wires_touching


    # generate adjacency matrix for electrodes
    # neighboring electrodes share a common wire
    # @todo make this more efficient instead of brute forcing through all electrodes?
    adjacency_matrix = [[None]*n_e]*n_e
    
    
    # testing
    # electrode_wire_dict[electrodes[0]] = [[(0, 0), (1, 1)]]
    # electrode_wire_dict[electrodes[1]] = [[(0, 0), (1, 1)]]
    # electrode_wire_dict[electrodes[4]] = [[(0, 0), (1, 1)]]
    # electrode_wire_dict[electrodes[8]] = [[(0, 0), (1, 1)]]
    # electrode_wire_dict[electrodes[3]] = [[(0, 0), (1, 1)]]



    print("___________________________")
    print("Number of wires", len(wires))
    print("___________________________")


    print("___________________________")
    print("Electrode-Wire Dictionary")
    print("___________________________")
    for key, value in electrode_wire_dict.items():
    	print(key, value, "\n")

    print("___________________________")
    print("Human-readable adjacencies")
    print("___________________________")
    for i in range(n_e):
        adjacency_matrix[i] = [0]*n_e
        s = "electrode " + str(i) + " adjacent to "
        for j in range(n_e):
           
            current_electrode = electrodes[i]
            other_electrode = electrodes[j]
            result = adjacent_electrodes(current_electrode, 
                                            other_electrode, electrode_wire_dict)
            
            # electrodes are not adjacent to themselves
            if i == j:
            	result = 0
            adjacency_matrix[i][j] = result

            if result:
            	s += " " + str(j)
        print(s)
            

    print("___________________________")
    print("Adjacency Matrix:")
    print("___________________________")
    for i in range(len(adjacency_matrix)):
        print(adjacency_matrix[i])

    gui(adjacency_matrix, electrodes, wires, r_e, l)

    return adjacency_matrix

generate_simulation()
