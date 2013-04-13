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

    self.DrawGrid()

  def _d2c(self, val):
    if self.data_to_color.has_key(val):
      return self.data_to_color[val]
    else:
      return "white"

  def _DrawCell(self,x,y):
    if not self.arr.exists(x,y):
      return
    val,rect=self.arr.get(x,y)
    self.w.itemconfig(rect,fill=self._d2c(val))

  def _SetGridCell(self,x,y,val):
    if not self.arr.exists(x,y):
      rect=self.w.create_rectangle(x*self.cellx,y*self.celly,(x+1)*self.cellx,(y+1)*self.celly,fill="white")
    else:
      oldval,rect=self.arr.get(x,y)
    self.arr.set(x,y,(val,rect))
    self._DrawCell(x,y)

  def _RefreshCell(self,x,y):
    if not self.arr.exists(x,y):
      return
    val,rect=self.arr.get(x,y)
    rect=self.w.create_rectangle(x*self.cellx,y*self.celly,(x+1)*self.cellx,(y+1)*self.celly,fill="white")
    self.arr.set(x,y,(val,rect))

  def DrawGrid(self):
    self.w.delete('*')
    self.w.create_rectangle(0,0,self.w.winfo_reqwidth(),self.w.winfo_reqheight(),fill="white")
    for x in range(0,self.w.winfo_reqwidth(),self.cellx):
      self.w.create_line(x,0,x,self.w.winfo_reqheight())
    for y in range(0,self.w.winfo_reqheight(),self.celly):
      self.w.create_line(0,y,self.w.winfo_reqwidth(),y)

    for x in range(self.arr.maxx+1):
      for y in range(self.arr.maxy+1):
        self._RefreshCell(x,y)
        self._DrawCell(x,y)

  def _Click(self,e):
    if self.current_value==None:
      print "No current value set"
    else:
      self._SetGridCell(e.x/self.cellx,e.y/self.celly,self.current_value)

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
  w=GridWindow()
  w.data_to_color={0:"#F7FCFD", 1:"#E5F5F9", 2:"#CCECE6", 3:"#99D8C9", 4:"#66C2A4", 5:"#41A376", 6:"#238B45", 7:"#006D2C", 8:"#00441B"}
  w.data_to_color={0:"#E5F5F9",1:"#99D8C9",2:"#2CA25F"}

  if len(sys.argv)==2:
    w.LoadFile(sys.argv[1])

  mainloop()

main()
