import os
from datetime import date

#This file contains useful functions to sort and search in the files

def already_applied(job_id):
    file_object_new = open("OldJobs.txt", 'r')
    read_file = file_object_new.read()
    if str(read_file).find(job_id) > 0:
        return True
    return False


def findFileLocationForCompany(company_name):
    # After every change file should be reopened since file has changed
    file_object = open("Jobs", "r")
    for line in file_object.readline():
        if line == company_name:
            return file_object.tell()
    return None


def moveOldJobs():
    file_object_old = open("OldJobs.txt", 'a')
    file_object_old.write(f'\n{date.today()}\n')
    file_object_new = open("NewJobs.txt", 'r')

    for row in file_object_new.read():
        file_object_old.write(row)

    file_object_old.close()
    file_object_new.close()
    os.remove('NewJobs.txt')