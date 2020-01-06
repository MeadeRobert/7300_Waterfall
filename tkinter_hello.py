import Tkinter as tk

root = tk.Tk()

def task():
	print "asdf"
	root.after(16, task)

root.after(16, task)
root.mainloop()
