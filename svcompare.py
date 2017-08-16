# Copyright 2017 Zachary Navarro
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Script that compares 2 Device settings reports.
This script is looking for differences in the 2 reports in an effort to
identify specific changes to default settings that have been made since
the time of startup.
"""

import os
import sys
import csv
import tkinter
from tkinter.constants import *
from tkinter import filedialog

# Global Variables for the CSV files
file1 = ""
file2 = ""

# Global variable for the App class
frame = None

class CSV(object):
	"""A CSV file processed to an array of strings"""

	def __init__(self, file):
		self.array = self.read_csv(file)

	def read_csv(self, file):
		array = []
		with open(file) as f:
			cr = csv.reader(f)
			for row in cr:
				array.append(row)
		return array

class App(tkinter.Frame):
	"""The GUI of the Program"""

	def __init__(self, master):
		super(App, self).__init__(master)
		self.pack(side=LEFT, fill=BOTH)
		self.create_widgets()

	def create_widgets(self):
		self.label = tkinter.Label(self, text="Open CSV to begin...")
		self.label.pack(side=TOP, anchor=W)

		self.label2 = tkinter.Label(self)
		self.label2.pack(side=TOP, anchor=W, after=self.label)

		self.label3 = tkinter.Label(self)
		self.label3.pack(side=TOP, anchor=W, after=self.label2)

		self.scroll = tkinter.Scrollbar(self)
		self.scroll.pack(side=RIGHT, fill=Y, expand=1)

		self.button = tkinter.Button(self, text="Exit")
		self.button.pack(side=BOTTOM, anchor=E, after=self.scroll, padx=25,
								pady=5)

		self.button2 = tkinter.Button(self, text="Scan for Changes")
		self.button2.pack(side=BOTTOM, anchor=W, after=self.button, padx=25,
								pady=10)

		self.button3 = tkinter.Button(self, text="Open CSV 2")
		self.button3.pack(side=BOTTOM, anchor=W, after=self.button2, padx=25,
								pady=5)

		self.button4 = tkinter.Button(self, text="Open CSV 1")
		self.button4.pack(side=BOTTOM, anchor=W, after=self.button3, padx=25)

		self.txt = tkinter.Text(self, height=30, width=97, wrap=WORD,
								yscrollcommand=self.scroll.set)
		self.txt.pack(side=BOTTOM, fill=BOTH, after=self.button4, expand=1)

		self.scroll.configure(command=self.txt.yview)

def compare(array1, array2):
	index = 0
	list1_id = []
	list2_id = []
	for list in array1:
		list1_id.append(list[2])
	for list in array2:
		list2_id.append(list[2])
	for list in array1:
		if list[2] not in list2_id:
			write_change(list[2], "deleted")
			array1.remove(list)
		else:
			while list[2] != array2[index][2]:
				index += 1
			if list == array2[index]:
				continue
			else:
				find_diff(list, array2[index], array1, array2)
	for list in array2:
		if list[2] not in list1_id:
			write_change(list[2], "added")

def write_change(id, var):
	if var == "deleted":
		with open("differences.txt", "a") as f:
			f.write("* Device {0} was in the original file but is not in the new file.\n".format(id))
	else:
		with open("differences.txt", "a") as f:
			f.write("* Device {0} was not in the original file but is in the new file.\n".format(id))

def find_diff(list1, list2, array1, array2):
	index = 0
	while index < 120:
		if list1[index] == list2[index]:
			index += 1
		else:
			with open("differences.txt", "a") as f:
				f.write("* Difference Found: Original ~ {0} - {1} = {2} / New ~ {3} - {4} = {5} \n".format(
								str(list1[2]), str(array1[0][index]),
								str(list1[index]), str(list2[2]),
								str(array2[0][index]), str(list2[index])))
			index += 1

def print_diff():
	global frame

	text = ""
	if os.path.isfile("differences.txt"):
		text = "Differences found - log generated as differences.txt\n\n"
		with open("differences.txt", "r") as f:
			for line in f:
				frame.txt.insert(END, line)
	else:
		text = "No differences were found.  Original settings intact."
	return text

def getCSV():
	global file1
	global file2
	global frame

	csvFile = filedialog.askopenfilename(title = "Select File",
		filetypes = [("CSV file","*.csv")])

	if file2 == "":
		if file1 == "":
			file1 = csvFile
			frame.label.configure(text="CSV file 1 is loaded...")
		else:
			file2 = csvFile
			frame.label.configure(text="Both CSV files are loaded...")
	else:
		frame.label.configure(text="Error: CSV Files are already loaded! " +
			"Scan for changes instead...")

def scanForChanges():
	global file1
	global file2
	global frame

	objs = []
	objs.append(CSV(file1))
	objs.append(CSV(file2))

	compare(objs[0].array, objs[1].array)
	frame.label3.configure(text=print_diff())

def main():
	global frame
	tk = tkinter.Tk()
	tk.title("Device Settings Report Comparison Tool")
	tk.geometry("800x600")
	frame = App(tk)
	frame.button.configure(command=tk.destroy)
	frame.button4.configure(command=getCSV)
	frame.button3.configure(command=getCSV)
	frame.button2.configure(command=scanForChanges)

	tk.mainloop()

if __name__ == "__main__":
	main()
