import os
import pickle
import xlsxwriter as xw

def readData():
    assignments = []
    if os.path.exists("assignments.dat"):
        with open("assignments.dat", "rb") as file:
            assignments = pickle.load(file)
    return assignments

def makeData(assignments):
    oldAssignments = readData()
    for assignment in assignments:
        if assignment not in oldAssignments:
            oldAssignments.append(assignment)
    with open("assignments.dat", "wb") as file:
        pickle.dump(oldAssignments, file)
    wb = xw.Workbook("assignments.xslx")
    ws = wb.add_worksheet()

    r = 1
    c = 0

    ws.write(0, 0, "Subject")
    ws.write(0, 1, "Title")
    ws.write(0, 2, "Type")
    ws.write(0, 3, "Date")
    ws.write(0, 4, "Description")

    for assignment in oldAssignments:
        ws.write(r, c, assignment["Subject"])
        ws.write(r, c+1, assignment["Title"])
        ws.write(r, c+2, assignment["Type"])
        ws.write(r, c+3, assignment["Date"])
        ws.write(r, c+4, assignment["Description"])
        r += 1

    wb.close()