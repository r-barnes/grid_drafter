#!/usr/bin/python
from Tkinter import *
import sys
cellx=20
celly=20
color="black"
colors={"r":"red","l":"blue","g":"green","w":"white","b":"black"}
color_numbers={"white":0,"black":1,"green":2,"blue":3,"red":4}
rcolor_numbers={0:"white",1:"black",2:"green",3:"blue",4:"red"}

class array2d:
	data={}
	minx=0
	miny=0
	maxx=0
	maxy=0
	def sete(this, x, y, z):
		if not this.data.has_key(y):
			this.data[y]={}
		this.data[y][x]=z
		this.maxy=max(y,this.maxy)
		this.miny=min(y,this.miny)
		this.maxx=max(x,this.maxx)
		this.minx=min(x,this.minx)

	def gete(this, x, y):
		try:
			return this.data[y][x]
		except:
			return "white"

	def draw(this,w):
		for x in range(this.maxx+1):
			for y in range(this.maxy+1):
				w.create_rectangle(x*cellx,y*celly,(x+1)*cellx,(y+1)*celly,fill=this.gete(x,y))

def set_grid_cell(x,y,color):
	global w,arr
	arr.sete(x,y,color)
	w.create_rectangle(x*cellx,y*celly,(x+1)*cellx,(y+1)*celly,fill=color)

def draw_grid():
	global w,master,cellx,celly,arr
	w.delete('*')
	w.create_rectangle(0,0,w.winfo_reqwidth(),w.winfo_reqheight(),fill="white")
	for x in range(0,w.winfo_reqwidth(),cellx):
		w.create_line(x,0,x,w.winfo_reqheight())
	for y in range(0,w.winfo_reqheight(),celly):
		w.create_line(0,y,w.winfo_reqwidth(),y)
	arr.draw(w)

def canvas_click(e):
	global w,arr,cellx,celly
	set_grid_cell(e.x/cellx,e.y/celly,color)

def zoom(direction):
	global cellx,celly
	if(cellx+direction*10<10 or celly+direction*10<10):
		return
	cellx+=direction*10
	celly+=direction*10
	draw_grid()

def save_grid():
	try:
		fout=open("gout","w")
	except:
		return

	fout.write("ncols\t" + str(arr.maxx+1) + "\n")
	fout.write("nrows\t" + str(arr.maxy+1) + "\n")
	for y in range(arr.maxy+1):
		for x in range(arr.maxx+1):
			fout.write(str(color_numbers[arr.gete(x,y)])+" ")
		fout.write("\n")

	fout.close()

def key(e):
	global color,colors

	print e.keysym
	if e.keysym == 'Escape':
		master.destroy()
		return
	elif e.keysym == 'minus':
		zoom(-1)
	elif e.keysym == 'plus':
		zoom(1)
	elif e.char=='S':
		save_grid()
		return
	elif colors.has_key(e.char):
		color=colors[e.char]
		return
	elif colors.has_key(e.char.lower()):
		for x in range(arr.maxx+1):
			for y in range(arr.maxy+1):
				if arr.gete(x,y)==colors[e.char.lower()]:
					set_grid_cell(x,y,"white")

def loadfile(fname):
	try:
		fin=open(fname,"r")
	except:
		return

	y=-1
	for line in fin:
		try:
			int(line[0])
		except:
			continue
		y+=1
		line=line.split()
		for x in range(len(line)):
			set_grid_cell(x,y,rcolor_numbers[int(line[x])])

def main():
	global master,w,arr
	master=Tk()
	w = Canvas(master, width=1000, height=500)
	arr=array2d()
	w.pack()

	draw_grid()
	w.bind("<ButtonPress-1>", canvas_click)
	w.bind("<B1-Motion>", canvas_click)
	w.bind_all('<Key>', key)

	if len(sys.argv)==2:
		loadfile(sys.argv[1])

	mainloop()

main()
