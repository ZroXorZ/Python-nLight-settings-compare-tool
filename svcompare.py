# Copyright 2015 Zachary Navarro
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
		self.label = tkinter.Label(self, text="Please Wait: Checking CSV's...")
		self.label.pack(side=TOP, anchor=W)
		
		self.label2 = tkinter.Label(self)
		self.label2.pack(side=TOP, anchor=W, after=self.label)
		
		self.label3 = tkinter.Label(self)
		self.label3.pack(side=TOP, anchor=W, after=self.label2)
		
		self.scroll = tkinter.Scrollbar(self)
		self.scroll.pack(side=RIGHT, fill=Y, expand=1)
		
		self.button = tkinter.Button(self, text="Exit")
		self.button.pack(side=BOTTOM, anchor=E, after=self.scroll, padx=25)
		
		self.txt = tkinter.Text(self, height=30, width=97, wrap=WORD,
								yscrollcommand=self.scroll.set)
		self.txt.pack(side=BOTTOM, fill=BOTH, after=self.button, expand=1)
					  
		self.scroll.configure(command=self.txt.yview)
	
def check_for_csv():
	count = 0
	curr_path = []
	for root, dir, file in os.walk("./"):
		for filename in file:
			if root == "./" and filename.endswith("csv"):
				count += 1
				curr_path.append(os.path.join(root, filename))
			else:
				continue
				
	objs = []
	if count < 2:
		objs.append("<2")
		return objs
	elif count > 2:
		objs.append(">2")
		return objs
	else:
		for path in curr_path:
			objs.append(CSV(path))
		return objs
		
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
			
def print_diff(frame):
	text = ""
	if os.path.isfile("differences.txt"):
		text = "Differences found - log generated as differences.txt\n\n"
		with open("differences.txt", "r") as f:
			for line in f:
				frame.txt.insert(END, line)
	else:
		text = "No differences were found.  Original settings intact."
	return text
		
def main():
	tk = tkinter.Tk()
	tk.title("Device Settings Report Comparison Tool")
	tk.geometry("800x600")
	frame = App(tk)
	frame.button.configure(command=tk.destroy)
	objs = []
	objs = check_for_csv()
	if objs[0] == "<2":
		frame.label2.configure(text="Error: 2 files needed to compare.  Only 1 file found in the current directory.")
	elif objs[0] == ">2":
		frame.label2.configure(text="Error: 2 files needed to compare.  Found more than 2 files in the current directory.")
	else:
		compare(objs[0].array, objs[1].array)
		frame.label3.configure(text = print_diff(frame))
	tk.mainloop()
	
if __name__ == "__main__":
	main()
