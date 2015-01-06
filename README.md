Python-nLight-settings-compare-tool
===================================

Takes 2 Device Settings Reports generated from nLight's SensorView application and compares them.  If any differences are found, a text file with the differences is created.

This script must be ran from the same directory as the Device Settings Reports.  It will not work properly if ran from another directory!!!

This script requires 2 Device Settings reports to compare. (Preferably, one from the startup and one from a later time)

This script requires that Python be installed on the machine where the comparison is taking place.  Python can be found here: <http://www.python.org>

This script should be compatible accross multiple platforms as it was written in python using standard libraries, however, it was only tesed on Windows.

####################
TO USE:
####################

Place this script in the same directory as 2 (and only 2) Device Settings reports.  Double Click the script and away it goes.  Alternatively, you can open a console in the directory and enter the following: python svcompare.py
