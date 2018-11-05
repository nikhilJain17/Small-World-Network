import tkinter as tk
import random
from math import sqrt

class Point:
	x = -1
	y = -1

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

class Wire:
	start = Point(-1, -1)
	end = Point(-1, -1)

	def __init__(self, start, end):
		self.start = start
		self.end = end

	def __str__(self):
		return self.start.__str__() + self.end.__str__()

class Electrode:
	radius = 0
	center = Point(-1, -1)
	wires = []

	def __init__(self, radius, center):
		self.radius = radius
		self.center = center

	def __str__(self):
		return self.center.__str__()

def create_wire(l):
	'''
	Input: l, dimension of grid 
	Output: (Point1, Point2) which are start and end points of wire
	'''

	# pick unique ints q1, q2 from [0, 4]
	q1 = random.randint(0, 3)
	q2 = random.randint(0, 3)
	while q1 == q2:
		q2 = random.randint(0, 3)

	# generate random points
	x1 = random.uniform(0, l)
	y1 = random.uniform(0, l)
	x2 = random.uniform(0, l)
	y2 = random.uniform(0, l)
	
	# use q to "anchor" points to a wall using table 2
	if q1 == 0:
		y1 = 0
	elif q1 == 1:
		x1 = 0
	elif q1 == 2:
		y1 = l
	elif q1 == 3:
		x1 = l

	if q2 == 0:
		y2 = 0
	elif q2 == 1:
		x2 = 0
	elif q2 == 2:
		y2 = l
	elif q2 == 3:
		x2 = l

	return Wire(Point(x1, y1), Point(x2, y2))

def create_electrodes(n_e, l, r_e):
	'''
	Input: 	n_e, number of electrodes
			l, dimension of grid
			r_e, radius of electrode

	Output: electrodes, list of electrodes
	'''
	electrodes = []

	# spacing in x and y direction between electrode centers
	spacing = l / (int(sqrt(n_e) + 1))

	x = spacing
	y = spacing

	while y < l:
		while x < l:
			center = Point(x, y)
			electrodes.append(Electrode(r_e, center))
			x += spacing
		y += spacing
		x = spacing

	# for e in electrodes:
	# 	print(e)

	return electrodes


def electrode_touching_wire(electrode, wires):
	'''
	Input: 	electrode, a singular Electrode object
			wires, a list of Wire objects

	Output:	touching_wires, a list of Wires touching the Electrode
	'''
	touching_wires = []
	for wire in wires:
		xe, ye = electrode.center.x, electrode.center.y
		x2, y2 = wire.end.x, wire.end.y
		x1, y1 = wire.start.x, wire.start.y

		numer = abs(xe * (y2 - y1) - ye * (x2 - x1) + x2 * y1 - y2 * x1)
		denom = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

		if (numer / denom) <= electrode.radius:
			# print(numer / denom, electrode.radius)
			touching_wires.append(wire)

	return touching_wires

def adjacent_electrodes(e1, e2):
	'''
	Input: 	e1, e2, Electrodes
	Output: touching, int that is 1 if e1 and e2 share a wire, 0 else
	'''
	wires1 = e1.wires
	wires2 = e2.wires

	for w1 in wires1:
		for w2 in wires2:

			start1 = w1.start
			start2 = w2.start

			end1 = w1.end
			end2 = w2.end

			equal_start = (start1.x == start2.x) and (start1.y == start2.y)
			equal_end = (end1.x == end2.x) and (end1.y == end2.y)

			if equal_start and equal_end:
				return 1

	return 0

def gui(adjacency_matrix, electrodes, wires, r_e, l):
	'''
	Input: 	adjacency_matrix, a matrix of adjacencies
			electrodes, a list of electrodes
			wires, a list of wires

	Output: a gooey
	'''
	WINDOW_SIZE = 800

	n_e = len(electrodes)
	n_w = len(wires)

	scaled_radius = r_e * 2 * WINDOW_SIZE / l

	# base gui components
	base = tk.Tk()
	base.resizable(width=False, height=False)

	canvas = tk.Canvas(master=base, width=WINDOW_SIZE, height=WINDOW_SIZE, bg='white')

	counter = 0
	# draw electrodes
	for electrode in electrodes:
		r_e = electrode.radius
		center_x, center_y = electrode.center.x, electrode.center.y
		center_x *= WINDOW_SIZE / l
		center_y *= WINDOW_SIZE / l 

		# fill circle
		i = 0
		while i < scaled_radius:
			canvas.create_oval(center_x - r_e, center_y - r_e, 
				center_x + r_e, center_y + r_e, 
				outline="red", fill="red", width=scaled_radius - i)

			i += scaled_radius / 25 

	

		canvas.create_text(center_x, 
			center_y, text=str(counter))

		counter += 1

	# draw wires
	for wire in wires:
		startx, starty = wire.start.x, wire.start.y
		endx, endy = wire.end.x, wire.end.y 

		startx *= WINDOW_SIZE / l
		starty *= WINDOW_SIZE / l
		endx *= WINDOW_SIZE / l
		endy *= WINDOW_SIZE / l

		# print("original ", wire.start.x, wire.start.y)
		# print("after", startx, starty, "\n_______________")

		# print("original222222 ", wire.end.x, wire.end.y)
		# print("after2222", endx, endy, "\n_ _ _ _ _ _ _ _ _ _ _ _ _ _")

		# TODO UNCOMMENT
		canvas.create_line(startx, starty, endx, endy,
			width=3, fill="blue")

	canvas.pack()
	base.mainloop()

def main(a, r_e, n_e, density_constant):
	'''
	This is the main function that runs the simulation.

	Input: 	a, spacing between electrodes
			r_e, electrode radius
			n_e, number of electrodes
			density_constant, denoted as lambda in the paper

	Output: adjacency_matrix, an adjacency matrix of electrodes
	'''

	l = a * (1 + sqrt(n_e))					# dim of grid
	n_w = int(density_constant * sqrt(n_e))	# num of wires

	# Generate wires
	wires = [create_wire(l) for x in range(0, n_w)]
	
	# Generate electrodes
	electrodes = create_electrodes(n_e, l, r_e)

	# Generate list of wires touching electrodes
	for e in electrodes:
		e.wires = electrode_touching_wire(e, wires)

	# Generate adjacency list
	sqrt_ne = int(sqrt(n_e))
	adjacency_matrix = [[0] * n_e] * n_e
	
	for i in range(0, n_e):
		adjacency_matrix[i] = [0]*n_e
		for j in range(0, n_e):
			if i != j:
				electrode1 = electrodes[i]
				electrode2 = electrodes[j]

				adjacency_matrix[i][j] = adjacent_electrodes(electrode1, electrode2)

	for i in range(0, n_e):
		s = ""
		for j in range(0, n_e):
			s += str(adjacency_matrix[i][j]) + " "
		print(s)

	gui(adjacency_matrix, electrodes, wires, r_e, l)

main(a=1, r_e=0.4, n_e=9, density_constant=30)



