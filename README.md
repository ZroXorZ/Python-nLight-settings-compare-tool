Python-settings-compare-tool
===================================

Takes 2 Device Settings Reports and compares them.  If any differences are found, a text file with the differences is created.

This script requires 2 Device Settings reports to compare. (Preferably, one from the startup and one from a later time)

This script requires that Python be installed on the machine where the comparison is taking place.  Python can be found here: <http://www.python.org>
This script was built in and tested on Python 3.6.

This script should be compatible across multiple platforms as it was written in python using standard libraries, however, it was only tested on Windows 10.

####################
TO USE:
####################

Run svcompare.bat.  When the program is opened, use the controls to select 2 device settings reports.  Use the controls to scan for changes.
Any changes between the old file and the new file will print in the program and a text file will be generated.
