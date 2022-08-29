#!/usr/bin/env python2
import tkinter as tk
import ttk, Tkconstants, tkFileDialog
from tkinter import *
from tkinter import messagebox
import os
import subprocess

### Changelog
# 1.2 - 2018-03-05
### Added global pop-up window output, option to disable output file creation
# 1.3 - 2018-03-06
### Added recursive file searching functionality

version = '1.3'
global selection
selection = ''
global disable
disable = False
runcom = "***Running Command: "

## Check if user is root
user = subprocess.check_output('whoami').rstrip()
if user != 'root':
	print "Must be root!"
	exit()

def mountDir():
	global dirName
	dirName = tkFileDialog.askdirectory(initialdir=e1.get(),title="Select Mount Location")
	# Avoid Clearing Entry Box
	if dirName:
		e1.delete(0, END)
		e1.insert(0, dirName)
	else: 
		return

def outputFile():
	global fileName	
	fileName = tkFileDialog.asksaveasfilename(initialdir=e2.get(),title="Select Output File")
	# Avoid Clearing Entry Box
	if fileName:
		e2.delete(0, END)
		e2.insert(0, fileName)
	else: 
		return

def printAbout():
	messagebox.showinfo('About Creddump GUI', "Created by Kyle Schuette\nVersion %s" % version)

def selector():
	global selection
	selection = str(toolVar.get())
	newStatus = selection + " selected"
	status.config(text = newStatus)

## Disable output file, just popup window
def disableOutput():
	global disable
	disable = disableVar.get()
	if disable == True:
		e2.config(state=DISABLED)
		outputButton.config(state=DISABLED)
	else:
		e2.config(state=NORMAL)
		outputButton.config(state=NORMAL)

## Global Output Pop-up
def popup(var):
	results = tk.Toplevel()
	results.wm_title("Results")
	results.geometry('700x400')

	t = tk.Text(results)
	t.pack(fill=BOTH, expand=True)
	t.insert('1.0', var)

## Exit Button
	exitButton = Button(results, text="Exit", width=10, command=results.destroy)
	exitButton.pack(side=BOTTOM, pady=2, expand=False)
	

		
def go():
	mountLocation = e1.get()
	outputFilename = e2.get()
	## Search directories top down for key files
	for root, dirs, files in os.walk(mountLocation, topdown=True):
		for name in files:
			if name == 'SAM':
				sam = os.path.join(root,name)
			elif name == 'SYSTEM':
				system = os.path.join(root,name)
			elif name == 'SECURITY':
				security = os.path.join(root,name)
		for name in dirs:
			if name == 'Windows' or 'System32' or 'config':
				break
	
	vista_win7 = ''
	## Cachedump
	if selection == 'Cachedump':
		result = messagebox.askyesnocancel("Windows Version", "Windows Vista or 7?")
		if result == True:
			vista_win7 = 'true'
		elif result == False:
			vista_win7 = 'false'
		else:
			return
		print runcom + '"./cachedump.py %s %s %s"' % (system, security, vista_win7)
		out = subprocess.check_output("./cachedump.py %s %s %s" % (system, security, vista_win7), shell=True)
	## Lsadump
	elif selection == 'Lsadump':
		result = messagebox.askyesnocancel("Windows Version", "Windows Vista or 7?")
		if result == True:
			vista_win7 = 'true'
		elif result == False:
			vista_win7 = 'false'
		else:
			return
		print runcom + '"./lsadump.py %s %s %s"' % (system, security, vista_win7)
		out = subprocess.check_output("./lsadump.py %s %s %s" % (system, security, vista_win7), shell=True)
	## Pwdump
	elif selection == 'Pwdump':
		print runcom + '"./pwdump.py %s %s"' % (system, sam)
		out = subprocess.check_output("./pwdump.py %s %s" % (system, sam), shell=True)
	## None Selected
	else:
		messagebox.showerror("Error", "No Tool Selected!")
		return
	## Output
	popup(out)
	if disable == False:
		with open('%s' % outputFilename, 'w') as f:
			f.write(out)

## Initialize Window
root = tk.Tk()
root.title("Creddump GUI")
root.resizable(width=True,height=False)

menu = tk.Menu(root)
root.config(menu=menu)

## Frames
	## Top Frame
topFrame = tk.Frame(root, height=100)
topFrame.pack(fill=BOTH)
	## Mid Frame
midFrame = tk.Frame(root, height=100)
midFrame.pack(fill=BOTH)
	## Bottom Frame
bottomFrame = tk.Frame(root, height=100)
bottomFrame.pack(fill=BOTH)
	## GO Frame
goFrame = tk.Frame(root, height=100)
goFrame.pack(fill=BOTH)


## File Menu
subMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=subMenu)
	## Separator
subMenu.add_separator()
	## Exit Application
subMenu.add_command(label="Exit", command=root.quit)
	## Help Menu
helpMenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=helpMenu)
	## Print About
helpMenu.add_command(label="About", command=printAbout)

## Status Bar
statusVar = "Select a Tool"
status = tk.Label(root, text=statusVar, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## Radio Button Selector
toolVar = StringVar()
R1 = Radiobutton(topFrame, text='Cachedump', variable=toolVar, value='Cachedump', command=selector)
R1.pack(side=LEFT, fill=X, padx=5, pady=5, expand=True)
R2 = Radiobutton(topFrame, text='Lsadump', variable=toolVar, value='Lsadump', command=selector)
R2.pack(side=LEFT, fill=X, padx=5, pady=5, expand=True)
R3 = Radiobutton(topFrame, text='Pwdump', variable=toolVar, value='Pwdump', command=selector)
R3.pack(side=LEFT, fill=X, padx=5, pady=5, expand=True)

## Separator
sep1 = ttk.Separator(midFrame, orient=HORIZONTAL)
sep1.pack(side=TOP, fill=X, padx=40, pady=5)

## Mount Location
lf1 = LabelFrame(midFrame, text='Mount Location', height=100)
lf1.pack(fill=X, padx=10, pady=10, expand=True)
	## Entry
e1 = Entry(lf1,width=50)
e1.insert(0, "/mnt")
e1.pack(side=LEFT, fill=X, padx=5, pady=5, expand=True)
	## File Dialog Button
mountButton = Button(lf1, text='Select', command=mountDir)
mountButton.pack(side=LEFT, padx=5, pady=5)

## Output Filename
lf2 = LabelFrame(bottomFrame, text='Output File', height=300)
lf2.pack(side=LEFT, fill=BOTH, padx=10, expand=True)
	## Entry
e2 = Entry(lf2,width=50)
e2.insert(0, "/root/Desktop/out.txt")
e2.pack(side=LEFT, fill=X, padx=5, pady=5, expand=True)
	## File Dialog Button
outputButton = Button(lf2, text='Select', command=outputFile)
outputButton.pack(side=LEFT, padx=5, pady=5)
	## Disable Output File/Pop-up
disableVar = BooleanVar()
disableBox = Checkbutton(lf2, text='Disable Output File', variable=disableVar, onvalue=True, offvalue=False, command=disableOutput)
disableBox.pack(side=LEFT, padx=5, pady=5)

## Go Button
goButton1 = Button(goFrame, text="GO!", width=10, command=go)
goButton1.pack(padx=150, pady=2, expand=True)

## Window Loop
root.mainloop()
