import tkinter as tk
import tkinter.messagebox as messagebox
import psutil
ascii_art = """
 __     _       _____                  
|  |   |_| ___ |_   _| ___  _____  ___ 
|  |__ | ||   |  | |  | -_||     || . |
|_____||_||_|_|  |_|  |___||_|_|_||  _|
                                  |_|     vAlpha
"""

print(ascii_art)
print("Developed by White Hat Cyberus. For You.")

def update_temperature(label):
    try:
        temperature = psutil.sensors_temperatures()['coretemp'][0].current
        label.config(text=f"CPU Temp: {temperature}°C")

        flag = getattr(update_temperature, "flag", 0)       # just making sure that's all, i swear its a feature not a bug. It works, so it works.
        # red zone , cpu's hot
        if temperature >= 80:
            label.configure(bg='red')
        
            if flag != 2:
                show_warning_dialog("High Temperature Warning", "I'm burning. Help!")
                update_temperature.flag = 2          # flag is 1 to indicate that the warning is displayed already and doesn't have to display again.
        # orange zone, cpu's getting warm
        elif temperature >= 76 and temperature < 80:
            label.configure(bg='orange')
            if flag != 1:  
                show_warning_dialog("Potential Danger", "Jeez, It's getting hot in here.")
                update_temperature.flag = 1  
        # green zone, cpu's normal
        elif temperature >= 40 and temperature < 76:
            label.configure(bg='green')
            update_temperature.flag = 0          # Reset the flag to 0 when temperature is in the normal range
        # blue zone, cpu's cold
        else:
            label.configure(bg='blue')
            if flag != -1:
                show_warning_dialog("Low temperature", "Brrrr, it's getting cold?")
                update_temperature.flag = -1  
    # incase something's wrong with the sensor
    except (IndexError, KeyError):
        label.config(text="Cant obtain temperature info rn. Try again later.")
        update_temperature.flag = 0         # big brain error handling, jesbin will be proud.

    label.after(2000, update_temperature, label)

def show_warning_dialog(title, message):
    messagebox.showwarning(title, message)

def main():
    root = tk.Tk()
    root.overrideredirect(True)
    root.wait_visibility(root)
    root.wm_attributes('-alpha', 0.7)

    label = tk.Label(root, text="Please wait, lintemp is checking...", fg='white', font=('Calibre', 13))        #the text is formality btw, its instantly updated
    label.pack()

    def start_move(event):
        root._x = event.x
        root._y = event.y

    def on_motion(event):
        root.geometry(f"+{root.winfo_x() + event.x - root._x}+{root.winfo_y() + event.y - root._y}")

    label.bind("<ButtonPress-1>", start_move)
    label.bind("<B1-Motion>", on_motion)
    '''
    didnt make a window bar, so i made it so that you can drag the window by clicking anywhere on the window, sleety big brain moments!!
    '''
    update_temperature.flag = 0

    def close_app():
        root.after_cancel(update_temperature)  # Stop the periodic update
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_app)
    update_temperature(label)
    root.mainloop()

main()
