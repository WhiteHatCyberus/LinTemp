import tkinter as tk
import tkinter.messagebox as messagebox
import psutil
ascii_art = """
          L       IIIIIII       N       N       TTTTTTTTT      EEEEEEEE        M         M   PPPPPP 
         L         III         NN      N           T           E              MM       MM  P      P
        L          III         N N     N           T           E              M M     M M  P      P
       L           III         N  N    N           T           EEEEEEEE       M  M   M  M  PPPPPP 
      L            III         N   N   N           T           E              M   M M   M  P      
     L             III         N    N  N           T           E              M    M    M  P      
    L              III         N     N N           T           EEEEEEEEE      M         M  P      
   L               III         N      NN           T           E              M         M  P      
  L                III         N       N           T           E              M         M  P      
 L                IIIIIII      N       N           T           EEEEEEEE       M         M  P      
LLLLLLLLLL       IIIIIII      N       N           T           EEEEEEEE       M         M  P      
LLLLLLLLLL       IIIIIII      N       N           T           EEEEEEEEE      M         M  P      vAlpha

"""

print(ascii_art)
print("Developed by White Hat Cyberus. For You.")
def update_temperature(label):
    try:
        temperature = psutil.sensors_temperatures()['coretemp'][0].current
        label.config(text=f"CPU Temperature: {temperature}°C")

        flag = getattr(update_temperature, "flag", 0)  # just making sure that's all, i swear its a feature not a bug. It works, so it works.

        if temperature >= 80:
            label.configure(bg='red')
        
            if flag != 2:  # Display warning only if the flag 
                show_warning_dialog("High Temperature Warning", "I'm burning. Help!")
                update_temperature.flag = 2  # flag is 1 to indicate that the warning is displayed already and doesn't have to display again.

        elif temperature >= 70 and temperature < 80:
            label.configure(bg='orange')
            if flag != 1:  
                show_warning_dialog("Potential Danger", "Jeez, It's getting hot in here.")
                update_temperature.flag = 1  
        
        elif temperature >= 40 and temperature < 70:
            label.configure(bg='green')
            update_temperature.flag = 0  # Reset the flag to 0 when temperature is in the normal range

        else:
            label.configure(bg='blue')
            if flag!=-1:
                show_warning_dialog("Low temperature", "Brrrr, it's getting cold?")
                update_temperature.flag = -1  

    except (IndexError, KeyError):
        label.config(text="Cant obtain temperature info rn. Try again later.")
        update_temperature.flag = 0  # big brain error handling, jesbin will be proud.

    label.after(2000, update_temperature, label)

def show_warning_dialog(title, message):
    messagebox.showwarning(title, message)

def main():
    root = tk.Tk()
    root.overrideredirect(True)
    root.wait_visibility(root)
    root.wm_attributes('-alpha', 0.7)

    label = tk.Label(root, text="Please wait, lintemp is checking...", fg='white', font=('Helvetica', 18)) #the text is formality btw, its instantly updated
    label.pack()

    label.bind("<ButtonPress-1>", lambda event: root.start_move(event)) 
    '''
    didnt make a window bar, so i made it so that you can drag the window by clicking anywhere on the window, sleety big brain moments!!
    '''
    label.bind("<B1-Motion>", lambda event: root.on_motion(event))

    root.start_move = lambda event: setattr(root, '_x', event.x) or setattr(root, '_y', event.y)
    root.on_motion = lambda event: root.geometry(f"+{root.winfo_x() + event.x - root._x}+{root.winfo_y() + event.y - root._y}")

    update_temperature.flag = 0  # i actually did this to make sure the warnings are not spammed

    update_temperature(label)

    root.mainloop()

main()
