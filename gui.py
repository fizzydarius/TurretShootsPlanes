from tkinter import *

window = Tk() # Initiate an instance of a window 
window.geometry("800x800")
window.title("Turret Shoots Planes")
icon = PhotoImage(file="car.png")
window.iconphoto(True,icon)
window.config(background="#5b98c7")

def clickFunction():
    print("button clicked")

def switchMotorButton():
    print("motor")
window.grid_columnconfigure(0, minsize=40)
hardButton = Button(window,
                text="Hard",
                padx = "100",
                command=clickFunction,
                font=("Comic Sans",30),
                fg="black",
                bg="#c72828",
                activeforeground="black",
                activebackground="#a62121").grid(row=0,column=2,columnspan=2,padx=(0,30))


easyButton = Button(window,
                text="Easy",
                padx = "100",
                command=clickFunction,
                font=("Comic Sans",30),
                fg="black",
                bg="#319e3c",
                activeforeground="black",
                activebackground="#236e2b").grid(row=0,column=5,columnspan=2)

global motorButton
motorButton = False

def motorButtonColourChange():
    if motorButton == False:
        motorButton.configure(bg="#1c6b21")
    elif motorButton == True:
        motorButton.configure(bg="#a32424")
    
motorButton = Button(window,
                text = "Motor",
                command= motorButtonColourChange,
                font=("Comic Sans",30),
                fg="black",
                bg="#a32424",).grid(row=1,column=6)



window.mainloop() # Place window on computer screen, listens for events