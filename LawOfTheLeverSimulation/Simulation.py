###   Libraries   ###


import random
import tkinter as tk
import math


###   Libraries   ###

###   Canvas && Background   ###


root = tk.Tk()

root.title("Law Of The Lever Simulation")

w = 1200
h = 800
x = 50
y = 100

root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.resizable(False, False)
canvas = tk.Canvas(root, width=w, height=h, background="#99ebff")
canvas.pack()
Grass = 600
Floor = canvas.create_rectangle(1200, 800, 50, Grass, fill="green")
Panel = canvas.create_rectangle(0, 0, 400, 1000, fill="grey")

LeverXY = [[550, 530], [1000, 530], [1000, 550], [550, 550]]
FulcrumXY = [[825, 600], [725, 600], [775, 550]]
DistToRot = 0
FulcrumPlace = 0
center = (FulcrumXY[2][0], FulcrumXY[2][1])

Fulcrum = canvas.create_polygon(FulcrumXY, fill="red")


###   Canvas && Background   ###

###   Entries && Labels   ###

# creating the input-boxes and labels lists
Entries = []
Labels = []

''' What every num defines
  0. Lever Length
  1. Fulcrum Place
  2. Rectangle Size 
  3. Rectangle Mass
  4. Rectangle Weight
  5. Rectangle Distance
  6. Rectangle Force
  *7. Delete
'''

# setting the input-boxes and labels Tests
Titles = ["Lever Length", "Fulcrum Place", "Rectangle Size", "Rectangle Mass", "Rectangle Weight", "Rectangle Distance",
          "Rectangle Force"]
Arguments = ["450", "0", "None", "None", "None", "None", "None"]

# creating the input-boxes and labels
for Place in range(7):
    if Place in [4, 5, 6]:
        Entries.append(tk.Label(root, text="0"))
        Entries[Place].config(font=("Courier", 15))
        Entries[Place].place(x=40, y=70 + 90 * Place)
    else:
        Entries.append(tk.Entry(root))
        Entries[Place].place(x=40, y=70 + 90 * Place, width=220, height=30)
        Entries[Place].config(font=("Courier", 20))
        Entries[Place].insert(0, Arguments[Place])

    Labels.append(tk.Label(root, text=Titles[Place] + " : "))
    Labels[Place].config(font=("Courier", 15))
    Labels[Place].place(x=40, y=30 + Place * 90)


###   ENTRIES && LABELS   ###


###   Object   ###


class Object:
    def __init__(self, Mass=2.0, Color="#111", X=500, Y=200, Flying=False, Points=None, Size=100):
        self.Mass = Mass
        self.Size = Size
        self.Color = Color
        self.X = X
        self.Y = Y
        self.MassCenter = self.X + self.Size / 2
        self.Distance = center[0] - self.MassCenter
        self.Force = self.Mass * 9.8
        self.Formula = float(self.Force) * float(self.Distance)
        self.Flying = Flying
        self.HightLight = False

        if Points is None:
            self.Points = [[self.X, self.Y], [self.X, self.Y + self.Size],
                           [self.X + self.Size, self.Y + self.Size],
                           [self.X + self.Size, self.Y]]
        else:
            self.Points = Points
            self.Flying = True
        self.RPoints = self.Points

        self.Rectangle = canvas.create_polygon(self.Points, fill=self.Color, outline=self.Color, width=7)

    def Physics(self):
        self.MassCenter = self.X + self.Size / 2
        if not self.Flying:
            self.Distance = center[0] - self.MassCenter
            self.Force = self.Mass * 9.8
            self.Formula = float(self.Force) * float(self.Distance)
            if self.Y + 20 > LeverXY[0][1] - self.Size:
                self.Y = LeverXY[0][1] - self.Size
            else:
                self.Y += 20

        self.Points = [[self.X, self.Y], [self.X, self.Y + self.Size],
                       [self.X + self.Size, self.Y + self.Size],
                       [self.X + self.Size, self.Y]]

    def Draw(self):
        if self.Size < 30:
            self.Size = 30
        if self.Size > 250:
            self.Size = 250
        if not Restarted:
            canvas.coords(self.Rectangle, self.RPoints[0][0], self.RPoints[0][1], self.RPoints[1][0],
                          self.RPoints[1][1],
                          self.RPoints[2][0], self.RPoints[2][1], self.RPoints[3][0], self.RPoints[3][1])
        else:
            canvas.coords(self.Rectangle, self.Points[0][0], self.Points[0][1], self.Points[1][0], self.Points[1][1],
                          self.Points[2][0], self.Points[2][1], self.Points[3][0], self.Points[3][1])
        if self.HightLight:
            canvas.itemconfig(self.Rectangle, outline="#33FF00")
        else:
            canvas.itemconfig(self.Rectangle, outline=self.Color)

    def Intersects(self, X=50, Y=50, Obj2=None):
        if Obj2 is None:
            if not Restarted:
                if self.RPoints[0][0] < X < self.RPoints[2][0] and self.RPoints[0][1] < Y < self.RPoints[2][1]:
                    return True
            else:
                if self.Points[0][0] < X < self.Points[2][0] and self.Points[0][1] < Y < self.Points[2][1]:
                    return True
        else:
            if ((self.X > Obj2.X + Obj2.Width) or (self.X + self.Size < Obj2.X) or
                    (self.Y > Obj2.Y + Obj2.Height) or (self.Y + self.Size < Obj2.Y)):
                return False
            return True
        return False

    def rotate(self, angle):
        angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        cx, cy = center
        new_points = []
        for x_old, y_old in self.Points:
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append([x_new + cx, y_new + cy])
        self.RPoints = new_points

    def Delete(self):
        canvas.delete(self.Rectangle)
        Rects.remove(self)
        del self


###   Object   ###

###   Mouse   ###


# if the mouse is pressed an Clicked bool is True
def Mouse(Click):
    global Clicked
    Clicked = Click


root.bind('<Button-1>', lambda event: Mouse(True))
root.bind('<ButtonRelease-1>', lambda event: Mouse(False))


###   Mouse   ###

###  Functions   ###


def MoveFulcrum(PlusX):
    global FulcrumXY, center
    if FulcrumXY[1][0] + PlusX < Rects[0].Points[0][0]:
        PlusX = Rects[0].Points[0][0] - FulcrumXY[1][0]
    if FulcrumXY[0][0] + PlusX > Rects[0].Points[1][0]:
        PlusX = Rects[0].Points[1][0] - FulcrumXY[0][0]

    center = (FulcrumXY[2][0] + PlusX, FulcrumXY[2][1])
    canvas.coords(Fulcrum, FulcrumXY[0][0] + PlusX, FulcrumXY[0][1], FulcrumXY[1][0] + PlusX, FulcrumXY[1][1],
                  FulcrumXY[2][0] + PlusX, FulcrumXY[2][1])


def IsFloat(Float):
    FList = [Dig for Dig in str(Float) if Dig in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]]
    if not FList == []:
        if not (FList.count(".") > 1 or "." in [FList[0], FList[-1]]):
            if (FList.count("-") == 1 and "-" == FList[0]) or FList.count("-") == 0:
                NFloat = ""
                if "-" in FList and len(FList) == 1:
                    return [False, ""]
                for Dig in FList:
                    NFloat += Dig
                return [True, float(NFloat)]
    return [False, ""]


def Sim(On):
    global StartSim, Restarted
    StartSim = On
    Restarted = False


def DeleteLast():
    global ObjectChose, Rects
    if ObjectChose > 0 and ObjectChose != len(Rects)-1:
        Rects[ObjectChose].Delete()
        ObjectChose = -1


def ResetPos():
    global DistToRot, StartSim, Restarted
    for i in range(len(Rects)):
        Rects[i].rotate(0)
    DistToRot = 0
    StartSim = False
    Restarted = True


def RandObject():
    RColor = "%06x" % random.randint(0, 0xFFFFFF)
    Rects.append(Object(X=80, Y=665, Color=f"#{RColor}", Flying=True, Mass=30))


###  Functions   ###

###  Variables   ###


Rects = [Object(Points=LeverXY, Color="red"), Object(30, Y=211, X=center[0] + 50), Object(30, Y=211, X=center[0] - 120)]
HowMuchToRotate = 0
MaxRotationR = -13
MaxRotationL = 13

StartSim = False
Restarted = True
Clicked = False
FirstStick = False
Moving = False
ObjectChose = -1


###  Variables   ###

###   Buttons   ###


StartSimBTN = tk.Button(root, text="Start")
StartSimBTN.place(x=1100, y=25, width=75, height=40)

ResetBTN = tk.Button(root, text="Reset", command=ResetPos, font=('helvetica', 12, 'underline italic'))
ResetBTN.place(x=1000, y=25, width=75, height=40)

DeleteBTN = tk.Button(root, text="Delete", bg="red", font=('helvetica', 12, 'italic'), command=DeleteLast)
DeleteBTN.place(x=220, y=690, width=100, height=50)
RandObject()


###   Buttons   ###

###  Main While Loop   ###


def LoopyLoop():
    global DistToRot, HowMuchToRotate, ObjectChose, Clicked, FirstStick, Moving
    global FulcrumPlace, MaxRotationR, MaxRotationL

    Entries[4].config(text=(str(int(Rects[ObjectChose].Force)) + "[g]"))
    Entries[5].config(text=(str(abs(int(Rects[ObjectChose].Distance)))) + "[cm]")

    FormulaText = str(abs(int(Rects[ObjectChose].Formula)))
    if int(Rects[ObjectChose].Formula) > 0:
        FormulaText = "Left <-- " + FormulaText
    elif int(Rects[ObjectChose].Formula) < 0:
        FormulaText = "Right --> " + FormulaText
    Entries[6].config(text=(FormulaText+"[n]"))


    MouseX = root.winfo_pointerx() - root.winfo_rootx()
    MouseY = root.winfo_pointery() - root.winfo_rooty()

    if StartSim:
        DistToRot -= HowMuchToRotate / 10000
        if DistToRot > MaxRotationL:
            DistToRot = MaxRotationL
        if DistToRot < MaxRotationR:
            DistToRot = MaxRotationR

        for rect in Rects[:-1]:
            rect.rotate(DistToRot)

        if HowMuchToRotate == 0:
            DistToRot = 0
        StartSimBTN.config(text="Stop", command=(lambda: Sim(False)))
    else:
        StartSimBTN.config(font=('helvetica', 12, 'underline italic'), text="Start", command=(lambda: Sim(True)))

    HowMuchToRotate = 0
    for i in range(len(Rects)):
        Rects[i].Draw()
        if i != 0:
            if i != len(Rects)-1:
                Rects[i].Physics()
                if Rects[i].Y == LeverXY[0][1] - Rects[i].Size:
                    HowMuchToRotate += Rects[i].Formula

            # checking for a new height-lighted object and replacing it
            if Rects[i].Intersects(MouseX, MouseY) and not Clicked and not FirstStick:
                if ObjectChose != i:
                    Rects[ObjectChose].HightLight = False
                    Rects[i].HightLight = True
                    Entries[2].delete(0, 'end')
                    Entries[2].insert(0, str(Rects[i].Size))
                    Entries[3].delete(0, 'end')
                    Entries[3].insert(0, str(Rects[i].Mass))
                ObjectChose = i

    # if the mouse is intersecting and clicked start moving the object
    if Clicked and Rects[ObjectChose].Intersects(MouseX, MouseY):
        Moving = True
    if not Clicked:
        Moving = False

    # change the object x,y relative to the mouse position and not out of bounds
    if Moving and not FirstStick:
        Rects[ObjectChose].Flying = True
        if ObjectChose == len(Rects) - 1:
            FirstStick = True
        else:
            if MouseX <= Rects[0].Points[0][0]:
                Rects[ObjectChose].X = Rects[0].Points[0][0]
            elif MouseX >= Rects[0].Points[1][0] - Rects[ObjectChose].Size:
                Rects[ObjectChose].X = Rects[0].Points[1][0] - Rects[ObjectChose].Size
            else:
                Rects[ObjectChose].X = MouseX
            if MouseY <= 0:
                Rects[ObjectChose].Y = 0
            elif MouseY >= root.winfo_height() - Rects[ObjectChose].Size:
                Rects[ObjectChose].Y = root.winfo_height() - Rects[ObjectChose].Size
            else:
                Rects[ObjectChose].Y = MouseY

    # if the object click is the last in the list(the new one) don't let the user place it out side the bounds
    if FirstStick:
        Rects[ObjectChose].X = MouseX
        Rects[ObjectChose].Y = MouseY
        if Rects[0].Points[0][0] < MouseX < Rects[0].Points[1][0] and 0 < MouseY < root.winfo_height():
            FirstStick = False
            RandObject()
        Rects[ObjectChose].Physics()

    if not ObjectChose == len(Rects) - 1 and not Clicked and ObjectChose >= 0:
        Rects[ObjectChose].Flying = False

    if IsFloat(Entries[0].get())[0]:
        Len = IsFloat(Entries[0].get())[1]

        if Len < 200:
            Len = 200
        elif Len > 800:
            Len = 800

        Rects[0].Points = [[775 - Len/2, 530], [775 + Len/2, 530], [775 + Len/2, 550], [775 - Len/2, 550]]

    if IsFloat(Entries[1].get())[0]:
        MoveFulcrum(IsFloat(Entries[1].get())[1])

        if FulcrumPlace != IsFloat(Entries[1].get())[1]:
            ThisRotation = 0
            Rects[0].rotate(0)
            while not int(Rects[0].RPoints[2][1]) >= Grass:
                Rects[0].rotate(ThisRotation)
                ThisRotation += 1
            MaxRotationL = ThisRotation - 2
            ThisRotation = 0
            Rects[0].rotate(0)
            while not int(Rects[0].RPoints[3][1]) >= Grass:
                Rects[0].rotate(ThisRotation)
                ThisRotation -= 1
            MaxRotationR = ThisRotation + 2
            Rects[0].rotate(DistToRot)
            FulcrumPlace = IsFloat(Entries[1].get())[1]

    if IsFloat(Entries[2].get())[0]:
        Rects[ObjectChose].Size = IsFloat(Entries[2].get())[1]

    if IsFloat(Entries[3].get())[0]:
        Rects[ObjectChose].Mass = IsFloat(Entries[3].get())[1]

    root.after(100, LoopyLoop)


root.after(100, LoopyLoop)
root.mainloop()


###  Main While Loop   ###
