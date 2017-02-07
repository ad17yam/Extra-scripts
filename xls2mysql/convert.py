#!/usr/bin/python

from __future__ import print_function
from os.path import join, dirname, abspath
import xlrd
import string
import MySQLdb
import os


#@TODO Use the following for filtering
FIRSTNAME = {'fname', 'firstname', 'first name'}
LASTNAME = {'lname', 'lastname', 'last name'}
ADDRESS = {'mailing address', 'address'}
HOMEPHONE = {'home phone', 'homephone'}
CELLPHONE = {'cell', 'cellphone', 'mobile phone', 'mobilephone'}
EMAIL = {'email', 'e-mail'}

filelist = os.listdir('./database')

for each in filelist:
    eventname, eventdate, eventarea = None, None, None
    if each.endswith('.xls') or each.endswith('.xlsx'):
        print(each)
        fname = join(dirname(dirname(abspath(__file__))), 'calling', 'database',each)
        details = each[:-5].split('_')
        print(details)
        eventname = details[0]
        eventdate = '%s %s' %(details[1], details[2])

        if len(details) >= 4:
            eventarea = details[3]
        print('%s %s %s' %(eventname, eventdate, eventarea))

        # Open the workbook
        book = xlrd.open_workbook(fname)

        # List sheet names, and pull a sheet by name
        #
        sheet_names = book.sheet_names()
        # Or grab the first sheet by index 
        #  (sheets are zero-indexed)
        #
        sheet = book.sheet_by_index(0)

        # Pull the first row by index
        #  (rows/columns are also zero-indexed)
        #
        # Establish a MySQL connection

#        database = MySQLdb.connect (host="localhost", user = "root", passwd = "password")
#        cursor = database.cursor()

#        createdb = 'CREATE DATABASE IF NOT EXISTS meditator DEFAULT CHARACTER SET utf8  DEFAULT COLLATE utf8_general_ci;' 
#        cursor.execute(createdb)

        database = MySQLdb.connect(host="localhost", user="root", passwd="pass4now", db="ishadb", charset='utf8')
        cursor = database.cursor()

        sql = '''CREATE TABLE IF NOT EXISTS `members` (
               `fname` VARCHAR(100) DEFAULT NULL,
               `lname` VARCHAR(100),
               `email` VARCHAR(100),
               `address` VARCHAR(100),
               `homephone` VARCHAR(100),
               `cellphone` VARCHAR(100),
               `sex` VARCHAR(10), 
               `programdate` VARCHAR(100) DEFAULT NULL,
               `location` VARCHAR(100) DEFAULT NULL, 
               `programtype` VARCHAR(25)
               )
               '''


        cursor.execute(sql)
        # Create the INSERT INTO sql query
        query = """INSERT INTO meditators_adi_test (fname, lname, email, address, homephone, cellphone, sex, programdate, location, programtype) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
       
        all =  string.maketrans('','')
        nodigs=all.translate(all, string.digits)

        # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
        for r in range(1, sheet.nrows):
              fname = sheet.cell_value(r, 0).strip()
              lname = sheet.cell_value(r,1).strip()
              email = sheet.cell_value(r,2).strip()
              address = sheet.cell_value(r,3).strip()
              homephone = str(sheet.cell_value(r,4)).translate(all, nodigs)
              if len(homephone) < 7:
                homephone = 'NULL' 
              cellphone = str(sheet.cell_value(r,5)).translate(all, nodigs)
              if len(cellphone) < 10:
                cellphone = 'NULL' 
              sex = sheet.cell_value(r,6).strip()
              # Assign values from each row
              values = (fname, lname, email, address, homephone, cellphone, sex, eventdate, eventarea, eventname)
        
              # Execute sql Query
              cursor.execute(query, values)
        
        # Close the cursor
        cursor.close()
        
        # Commit the transaction
        database.commit()

        # Close the database connection
        database.close()

        columns = str(sheet.ncols)
        rows = str(sheet.nrows)
        print('Importing to the database completed')


