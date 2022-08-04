########################################################################################################################

# Title: mergeShapefiles

# Author: Audsley, A.

# Description: The script first looks through the desired folder and will take every .shp contained within the folder
#              and merge them together into a single shapefile. This file will be served in a folder of the users
#              choice. The name of the output shapefile is set by the user with the suffix '_merged.shp'.
#              This script will also check that the desired fields are present, if not the field will be added.

# Requirements: This script requires an arcpy interpreter which can only be used with a licenced version of ArcGIS

########################################################################################################################

import arcpy
import os

inputpath = raw_input('paste the path to the folder containing the shapefiles:')
outputpath = raw_input('paste the output path to the folder where you would like the save the result:')
name = raw_input("Desired name of output file?")
out = outputpath
arcpy.env.workspace = inputpath
shplist = arcpy.ListFeatureClasses('*.shp')
print "merging shapefiles"
arcpy.Merge_management(shplist, os.path.join(out, name + '_merged.shp'))
print "______________________"
print "merged shapefile saved in:" + outputpath
print "______________________"

arcpy.env.workspace = outputpath
newlist = arcpy.ListFeatureClasses()

add_fields = [
    ("GUI", "TEXT", "#", "#", 254),
    ("HabType", "TEXT", "#", "#", 254),
    ("HabSubType", "TEXT", "#", "#", 254),
    ("HabStatus", "TEXT", "#", "#", 254),
    ("Certainty", "TEXT", "#", "#", 254),
    ("Determiner", "TEXT", "#", "#", 254),
    ("DetDate", "DATE", "#", "#", "#"),
    ("SurveyKey", "TEXT", "#", "#", 254),
    ("StartDate", "TEXT", "#", "#", 254),
    ("EndDate", "TEXT", "#", "#", 254),
    ("DateType", "TEXT", "#", "#", 254),
    ("PlaceName", "TEXT", "#", "#", 254),
    ("DataOwner", "TEXT", "#", "#", 254),
    ("Accuracy", "LONG", "#", "#", "#"),
    ("AltHabType", "TEXT", "#", "#", 254),
    ("AltHabRel", "TEXT", "#", "#", 20),
    ("RecordKey", "TEXT", "#", "#", 50),
]

for fc in newlist:
    # Add all fields
    print("Adding fields to " + str(fc) + " ...")
    field_name_list = [field.name for field in arcpy.ListFields(fc) if
                       not (field.type in ["OID", "Geometry"] or field.name in ["Shape_Length", "Shape_Area"])]
    for fieldToAdd in add_fields:
        if fieldToAdd[0] not in field_name_list:
            print("Adding field " + str(fieldToAdd[0]) + " to " + str(fc) + " ")
            try:
                arcpy.AddField_management(fc, fieldToAdd[0], fieldToAdd[1], fieldToAdd[2], fieldToAdd[3], fieldToAdd[4])
            except Exception as e:
                print "Error adding field '%s' to %s" % (str(fieldToAdd[0]), str(fc))
                print e.message
            else:
                print "Field successfully added"
        else:
            print "Field '%s' already exists in %s, ignoring..." % (str(fieldToAdd[0]), str(fc))
    print "______________________"

raw_input('Process complete, press enter to quit')
