"""For me to learn how to do GUI tingz"""

import tkinter as tk
import tkinter.ttk as ttk

root=tk.Tk()
root.tk_setPalette('#222')

pot=tk.Toplevel()


too=tk.Spinbox(pot)
too.pack()




too.tk_setPalette()

note=ttk.Notebook(root)
note.pack(expand=1, fill='both')

bt1=tk.LabelFrame(note, text='HEY THERE')
bt1.pack()

bt2=tk.LabelFrame(note, text='HEY THERE2')
bt2.pack()

too.update()
print(too.winfo_ismapped())

note.add(bt1,text='Timer')
note.add(bt2,text='My Activities')


root.mainloop()