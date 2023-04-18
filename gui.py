from tkinter import *

window = Tk() # Initiate an instance of a window 
window.geometry("800x400")
window.title("Turret Shoots Planes")
icon = PhotoImage(file="car.png")
window.iconphoto(True,icon)
window.config(background="#5b98c7")

window.grid_columnconfigure(0, minsize=40)
window.grid_columnconfigure(2, minsize=60)


def hardMode():
    print("Hard mode activated!")
    ModeStatus["text"] = "Difficulty mode: Hard"

hardButton = Button(window,
                text="Hard",
                padx = "100",
                command=hardMode,
                font=("Comic Sans",30),
                fg="black",
                bg="#c72828",
                activeforeground="black",
                activebackground="#a62121")
hardButton.grid(row=0,column=2,columnspan=2,padx=(0,30),pady=(40,0))


def easyMode():
    print("Easy mode activated!")
    ModeStatus["text"] = "Difficulty mode: Easy"    

easyButton = Button(window,
                text="Easy",
                padx = "100",
                command=easyMode,
                font=("Comic Sans",30),
                fg="black",
                bg="#319e3c",
                activeforeground="black",
                activebackground="#236e2b")
easyButton.grid(row=0,column=5,columnspan=2,pady=(40,0))



motorButtonClicked = False

def motorButtonColourChange():
    global motorButtonClicked
    if motorButtonClicked == False:
        print("motor on!")
        motorButton["bg"] = "green"
        motorButtonClicked = True
        MotorLabel["text"] = "Motor mode: ON"
    elif motorButtonClicked == True:
        print("motor off")
        motorButton["bg"] = "red"
        motorButtonClicked = False
        MotorLabel["text"] = "Motor mode: OFF"

motorButton = Button(window,
                text = "Motor",
                command= lambda: motorButtonColourChange(),
                font=("Comic Sans",30),
                fg="black",
                bg="#a32424")
motorButton.grid(row=1,column=6,pady=(40,0))

MotorLabel = Label(window,
            text="Motor mode: OFF",
            font=("Calibri 15 bold"),
            bg="#5b98c7")
MotorLabel.grid(row=3,column=2)


ModeStatus = Label(window,
            text="Difficulty mode: Easy",
            font=('Calibri 15 bold'),
            bg="#5b98c7")
ModeStatus.grid(row=2,column=2)



window.mainloop() # Place window on computer screen, listens for events