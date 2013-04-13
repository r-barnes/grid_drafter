#!/usr/bin/python
from Tkinter import *
import sys

class array2d:
  def __init__(self):
    self.data=[]

  def set(self, x, y, z):
    if y>=len(self.data):
      self.data+=[[]]*(y-len(self.data)+1)
    if x>=len(self.data[y]):
      self.data[y]+=[0]*(x-len(self.data[y])+1)
    self.data[y][x]=z

  def get(self, x, y):
    if y>=len(self.data):
      return None
    elif x>=len(self.data[y]):
      return None
    else:
      return self.data[y][x]

  def height(self):
    return len(self.data)

  def width(self):
    return max([len(i) for i in self.data])


class GridWindow:
  def __init__(self, gtype="square", keys_to_data=None, data_to_color={}, cellx=20, celly=20, grid_color="black"):
    self.master=Tk()
    self.master.wm_title("Grid Drafter")
    self.w = Canvas(self.master, width=1000, height=500)
    self.arr=array2d()
    self.obj_tags={}
    self.w.pack()

    self.w.bind("<ButtonPress-1>", lambda event: self._Click(event))
    self.w.bind("<B1-Motion>", lambda event: self._Click(event))
    self.w.bind_all('<Key>', lambda event: self._Key(event))

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

    if gtype=="square":
      self.drawer=self._DrawSquare
    elif gtype=="hex":
      self.drawer=self._DrawHex
    else:
      raise Exception("Unrecognised grid type")

    self.DrawGrid()

  def _d2c(self, val):
    if self.data_to_color.has_key(val):
      return self.data_to_color[val]
    else:
      return "white"

  def _DrawHex(self, x, y, fillcolour):
    oneseg = self.cellx/4
    twoseg = oneseg*2  # same as cellx/2
    orgy=y*self.cellx+(x%2)*self.cellx/2
    orgx=x*self.cellx*3/4.

    # Create a new one
    cell = self.w.create_polygon( 
    orgx,                   orgy + twoseg,
    orgx + oneseg,          orgy,
    orgx + oneseg + twoseg, orgy,
    orgx + self.cellx ,     orgy + twoseg,
    orgx + oneseg + twoseg, orgy + self.cellx,
    orgx + oneseg,          orgy + self.cellx,
    orgx,                   orgy + twoseg,
    outline="black",fill=fillcolour)
    return cell

  def _DrawSquare(self, x, y, fillcolour):
    orgx=x*self.cellx
    orgy=y*self.celly
    cell = self.w.create_polygon(
      orgx,            orgy,
      orgx+self.cellx, orgy,
      orgx+self.cellx, orgy+self.celly,
      orgx,            orgy+self.celly,
      orgx,            orgy,
      outline="black", fill=fillcolour
    )
    return cell

  def _MakeCell(self,x,y):
    if self.arr.get(x,y):
      val,cell=self.arr.get(x,y)
      cell=self.drawer(x,y,self._d2c(val))
    else:
      val=0
      cell=self.drawer(x,y,"white")
    self.w.tag_bind(cell, '<ButtonPress-1>', self._Click)
    self.obj_tags[cell]=(x,y)
    self.arr.set(x,y,(val,cell))

  def _SetGridCell(self,x,y,val):
    if not self.arr.get(x,y):
      cell=self.drawer(x,y,"white")
    else:
      oldval,cell=self.arr.get(x,y)
    self.arr.set(x,y,(val,cell))
    self._DrawCell(x,y)

  def _DrawCell(self, x, y):
    if not self.arr.get(x,y):
      return
    val,cell=self.arr.get(x,y)
    self.w.itemconfig(cell,fill=self._d2c(val))

  def DrawGrid(self):
    self.w.delete('*')
    for x in range(0,int(self.w.winfo_reqwidth()/self.cellx)+1):
      for y in range(0,int(self.w.winfo_reqheight()/self.celly)+1):
        self._MakeCell(x,y)

  def _Click(self,e):
    closest_object=e.widget.find_closest(e.x, e.y)[0]
    x,y=self.obj_tags[closest_object]
    if self.current_value==None:
      print "No current value set"
    else:
      self._SetGridCell(x,y,self.current_value)

  def _Zoom(self,direction):
    if(self.cellx+direction*10<10 or self.celly+direction*10<10):
      return
    self.cellx+=direction*10
    self.celly+=direction*10
    self.DrawGrid()

  def SaveGrid(self,filename="gout"):
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

  def _Key(self,e):
    if e.keysym == 'Escape':
      self.master.destroy()
    elif e.keysym == 'minus':
      self._Zoom(-1)
    elif e.keysym == 'plus':
      self._Zoom(1)
    elif e.char=='S':
      self.SaveGrid()
    elif e.char.isdigit():
      self.current_value=int(e.char)
    elif self.keys_to_data.has_key(e.char):
      self.current_value=self.keys_to_data[e.char]
    elif self.keys_to_data.has_key(e.char.lower()):
      for x in range(self.arr.maxx+1):
        for y in range(self.arr.maxy+1):
          if self.arr.exists(x,y):
            val,rect=self.arr.get(x,y)
            if val==self.keys_to_data[e.char.lower()]:
              self._SetGridCell(x,y,0)

  def LoadFile(self,fname):
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
        self._SetGridCell(x,y,int(line[x]))

def main():
  w=GridWindow(gtype="hex")
  w.data_to_color={0:"#F7FCFD", 1:"#E5F5F9", 2:"#CCECE6", 3:"#99D8C9", 4:"#66C2A4", 5:"#41A376", 6:"#238B45", 7:"#006D2C", 8:"#00441B"}
#  w.data_to_color={0:"#E5F5F9",1:"#99D8C9",2:"#2CA25F"}

  if len(sys.argv)==2:
    w.LoadFile(sys.argv[1])

  mainloop()

main()
