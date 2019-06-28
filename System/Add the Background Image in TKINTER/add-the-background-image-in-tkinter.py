import os
Image_path=os.environ['TEMP']+r"\comodo_logo_desktop_wallpaper_by_thanhtai2009-d8h3odf.PGM"  # Enter the path of image file.
###### Image_Path only supports GIF or PGM/PPM images.#####


try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk

root = tk.Tk()
root.title('background image')


image1 = tk.PhotoImage(file=Image_path)
w = image1.width()
h = image1.height()
root.geometry("%dx%d+0+0" % (w, h))

panel1 = tk.Label(root, image=image1)
panel1.pack(side='top', fill='both', expand='yes')

panel1.image = image1

root.mainloop()
