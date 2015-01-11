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
		
def quit():
	sys.exit()
	
def clear():
	os.system("cls")
	
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
				
	if count < 2:
		clear()
		print("Error: 2 files needed to compare.  Not Enough found in")
		print("the current directory.")
		input("\n\nPress the Enter Key to quit...")
		quit()
	elif count > 2:
		clear()
		print("Error: 2 files needed to compare.  Found more than 2 files")
		print("in the current directory.")
		input("\n\nPress the Enter Key to quit...")
		quit()
	else:
		objs = []
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
			f.write("* Device {0} was in the original file but is not in the new file\n.".format(id))
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
	if os.path.isfile("differences.txt"):
		print ("Differneces found - log generated:\n\n")
		with open("differences.txt", "r") as f:
			for line in f:
				print (line)
	else:
		print ("No differences were found.  Original settings intact.")
		
def main():
	objs = []
	clear()
	print ("Checking CSV files, please wait...\n")
	objs = check_for_csv()
	compare(objs[0].array, objs[1].array)
	print_diff()
	input("\n\nPress the Enter Key to quit...")
	
if __name__ == "__main__":
	main()
