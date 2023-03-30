from tkinter import *

window = Tk() # Initiate an instance of a window 
window.geometry("800x800")
window.title("Turret Shoots Planes")
icon = PhotoImage(file="car.png")
window.iconphoto(True,icon)
window.config(background="#5b98c7")

def hardMode():
    print("Hard mode activated!")
    ModeStatus["text"] = "Difficulty mode: Hard"


def easyMode():
    print("Easy mode activated!")
    ModeStatus["text"] = "Difficulty mode: Easy"    

def switchMotorButton():
    print("motor")


window.grid_columnconfigure(0, minsize=40)
window.grid_columnconfigure(2, minsize=60)
hardButton = Button(window,
                text="Hard",
                padx = "100",
                command=hardMode,
                font=("Comic Sans",30),
                fg="black",
                bg="#c72828",
                activeforeground="black",
                activebackground="#a62121")
hardButton.grid(row=0,column=2,columnspan=2,padx=(0,30))


easyButton = Button(window,
                text="Easy",
                padx = "100",
                command=easyMode,
                font=("Comic Sans",30),
                fg="black",
                bg="#319e3c",
                activeforeground="black",
                activebackground="#236e2b")
easyButton.grid(row=0,column=5,columnspan=2)


#testing failed, im not sure how to do it however I may just add a Motor ON , Motor OFF button 
global motorButton
motorButton = False

def motorButtonColourChange():
    if motorButton == False:
        motorButton.configure(bg="#1c6b21")
    elif motorButton == True:
        motorButton.configure(bg="#a32424")

#testing


motorButton = Button(window,
                text = "Motor",
                command= motorButtonColourChange,
                font=("Comic Sans",30),
                fg="black",
                bg="#a32424")
motorButton.grid(row=1,column=6)

ModeStatus = Label(window,
            text="Difficulty mode: Easy",
            font=('Calibri 15 bold'),
            bg="#5b98c7")
ModeStatus.grid(row=2,column=2)

window.mainloop() # Place window on computer screen, listens for events