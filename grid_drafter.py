#!/usr/bin/python
from Tkinter import *
import sys

class array2d:
  def __init__(self):
    self.data={}
    self.minx=0
    self.miny=0
    self.maxx=0
    self.maxy=0

  def set(self, x, y, z):
    if not self.data.has_key(y):
      self.data[y]={}
    self.data[y][x]=z
    self.maxy=max(y,self.maxy)
    self.miny=min(y,self.miny)
    self.maxx=max(x,self.maxx)
    self.minx=min(x,self.minx)

  def get(self, x, y):
    if self.exists(x,y):
      return self.data[y][x]
    else:
      return None

  def exists(self, x, y):
    return (self.data.has_key(y) and self.data[y].has_key(x))

class GridWindow:
  def __init__(self, keys_to_data=None, data_to_color={}, cellx=20, celly=20, grid_color="black"):
    self.master=Tk()
    self.master.wm_title("Grid Drafter")
    self.w = Canvas(self.master, width=1000, height=500)
    self.arr=array2d()
    self.w.pack()

    self.w.bind("<ButtonPress-1>", lambda event: self._click(event))
    self.w.bind("<B1-Motion>", lambda event: self._click(event))
    self.w.bind_all('<Key>', lambda event: self._key(event))

    if not keys_to_data:
      self.keys_to_data={"r":4,"l":3,"g":2,"w":0,"b":1}
    else:
      self.keys_to_data=colors

    if not data_to_color:
      self.data_to_color={0:"white",1:"black",2:"green",3:"blue",4:"red"}
    else:
      self.data_to_color=data_to_color

    self.cellx=20
    self.celly=20
    self.grid_color=grid_color
    self.current_value=None

    self.draw_grid()

  def _d2c(self, val):
    if self.data_to_color.has_key(val):
      return self.data_to_color[val]
    else:
      return "white"

  def _draw_cell(self,x,y):
    if not self.arr.exists(x,y):
      return
    val,rect=self.arr.get(x,y)
    self.w.itemconfig(rect,fill=self._d2c(val))

  def _set_grid_cell(self,x,y,val):
    if not self.arr.exists(x,y):
      rect=self.w.create_rectangle(x*self.cellx,y*self.celly,(x+1)*self.cellx,(y+1)*self.celly,fill="white")
    else:
      oldval,rect=self.arr.get(x,y)
    self.arr.set(x,y,(val,rect))
    self._draw_cell(x,y)

  def _refresh_cell(self,x,y):
    if not self.arr.exists(x,y):
      return
    val,rect=self.arr.get(x,y)
    rect=self.w.create_rectangle(x*self.cellx,y*self.celly,(x+1)*self.cellx,(y+1)*self.celly,fill="white")
    self.arr.set(x,y,(val,rect))

  def draw_grid(self):
    self.w.delete('*')
    self.w.create_rectangle(0,0,self.w.winfo_reqwidth(),self.w.winfo_reqheight(),fill="white")
    for x in range(0,self.w.winfo_reqwidth(),self.cellx):
      self.w.create_line(x,0,x,self.w.winfo_reqheight())
    for y in range(0,self.w.winfo_reqheight(),self.celly):
      self.w.create_line(0,y,self.w.winfo_reqwidth(),y)

    for x in range(self.arr.maxx+1):
      for y in range(self.arr.maxy+1):
        self._refresh_cell(x,y)
        self._draw_cell(x,y)

  def _click(self,e):
    if self.current_value:
      self._set_grid_cell(e.x/self.cellx,e.y/self.celly,self.current_value)
    else:
      print "No current value set"

  def _zoom(self,direction):
    if(self.cellx+direction*10<10 or self.celly+direction*10<10):
      return
    self.cellx+=direction*10
    self.celly+=direction*10
    self.draw_grid()

  def save_grid(self,filename="gout"):
    try:
      fout=open(filename,"w")
    except:
      return

    fout.write("ncols\t" + str(self.arr.maxx+1) + "\n")
    fout.write("nrows\t" + str(self.arr.maxy+1) + "\n")
    for y in range(self.arr.maxy+1):
      for x in range(self.arr.maxx+1):
        if self.arr.exists(x,y):
          val,rect=self.arr.get(x,y)
          fout.write(str(val)+" ")
        else:
          fout.write("0 ")
      fout.write("\n")

    fout.close()

  def _key(self,e):
    if e.keysym == 'Escape':
      self.master.destroy()
      return
    elif e.keysym == 'minus':
      self._zoom(-1)
    elif e.keysym == 'plus':
      self._zoom(1)
    elif e.char=='S':
      self.save_grid()
      return
    elif e.char.isdigit():
      self.current_value=int(e.char)
    elif self.keys_to_data.has_key(e.char):
      self.current_value=self.keys_to_data[e.char]
      return
    elif self.keys_to_data.has_key(e.char.lower()):
      for x in range(self.arr.maxx+1):
        for y in range(self.arr.maxy+1):
          if self.arr.exists(x,y):
            val,rect=self.arr.get(x,y)
            if val==self.keys_to_data[e.char.lower()]:
              self._set_grid_cell(x,y,0)

  def loadfile(self,fname):
    try:
      fin=open(fname,"r")
    except:
      return

    y=-1
    for line in fin:
      line=line.strip()
      if len(line)==0:
        continue
      elif line[0]=='#':
        continue
      try:
        int(line[0])
      except:
        continue
      y+=1
      line=line.split()
      for x in range(len(line)):
        self._set_grid_cell(x,y,int(line[x]))

def main():
  print "hello"
  w=GridWindow()

  if len(sys.argv)==2:
    w.loadfile(sys.argv[1])

  mainloop()

main()
