import sys
import csv
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


#class Student which contains student's ID, study's ID, student's group, list of results, date and final percentage
class Student:
    def __init__ (self, studentID, studyID, group, answers, date, result):
        if not studentID:
            raise ValueError("Missing student's ID")
        if not studyID:
            raise ValueError("Missing study's ID")
        if not group:
            raise ValueError("Missing student's group")
        if not answers:
            raise ValueError("Missing student's answers")
        if not date:
            raise ValueError("Missing date")
        
        self.studentID = studentID.strip()
        self.studyID = studyID.strip()
        self.group = group.strip()
        self.answers=list(answers.strip())
        self.date = date.strip(".csv")
        self.result = result


#class Question which contains correct answer, positive and negative points for that question
class Question:
    def __init__ (self, answer, positive, negative):
        if not answer:
            raise ValueError("Missing question's answer")
        if int(positive) <= 0:
            raise ValueError("Points should not be negative or zero")
        if int(negative) < 0:
            raise ValueError("Points should not be negative")
        
        self.answer = answer.strip()
        self.positive = int(positive)
        self.negative = int(negative)


def main():

    students = readStudentCSV()
    correctAnswers = readCorrectAnswers()


    for student in students:
        
        questions = extractQuestions(correctAnswers, student.studyID, student.group)      
        
        result = compare(student.answers, questions)

        maximumPoints = calculateLimit(questions)
        student.result  = calculate(result,maximumPoints)

    createCSV(students,students[0].studyID + "_" + students[0].date)
    
    csvfile = "results_" + students[0].studyID + "_" + students[0].date + ".csv"
    pdffile = "results_" + students[0].studyID + "_" + students[0].date + ".pdf"
    createPDF(csvfile, pdffile)


#function that reads from CSV student's ID, study's ID, group and list of students' answers
def readStudentCSV():

    students = []

    studyID, date = sys.argv[1].split("_")

    with open(sys.argv[1]) as file:
        for line in file:
            studentID, group, answers = line.split(",")

            if not any(student.studentID  == studentID for student in students):
                students.append(Student(studentID, studyID, group, answers, date, 0))
            
    return students


#function that reads from CSV and returns a list of objects that contains study's ID, group and questions(answer,positive and negative points)
def readCorrectAnswers():

    correctAnswers = {}

    with open(sys.argv[2], 'r') as file:

        reader = csv.reader(file)

        for row in reader:
            key = (row[0],row[1])

            questions = Question(row[2], row[3], row[4])

            if key in correctAnswers:
                correctAnswers[key].append(questions)
            else:
                correctAnswers[key] = [questions]

    return correctAnswers


def extractQuestions(correctAnswers, studyID, group):

    target_key = (studyID, group)

    if target_key in correctAnswers:
        return correctAnswers[target_key]
    else:
        return None


def calculateLimit(questions):

    maximum = 0

    for question in questions:
        maximum = maximum + question.positive

    return maximum


#function that compares student's list of answers with the correct one
def compare(studentAnswers, correctAnswers):

    result = 0

    for i in range(len(studentAnswers)):
        if studentAnswers[i] == correctAnswers[i].answer:
            result = result + correctAnswers[i].positive
        else:
            result = result - correctAnswers[i].negative

    if result < 0:
        return 0
    else:
        return result


#function that calculates the student's final result
def calculate(result,number):
    return round(result/number * 100)


def get_result(student):
    return student.result

#function that creates CSV with the student's ID and final result
def createCSV(students,name):

    with open("results_"+ name +".csv", 'w', newline='') as csvfile: 
     
        writer = csv.writer(csvfile) 
        
        for student in sorted(students, key = get_result, reverse = True):
            writer.writerow([student.studentID,f'{student.result}{"%"}'])



#function that creates PDF from the CSV file
def createPDF(csvfile, pdffile):
    df = pd.read_csv(csvfile, header = None)
    data = df.values.tolist()

    column_labels = ["INDEX", "RESULTS"]
    data.insert(0, column_labels)

    page_width, page_height = landscape(letter)
    doc = SimpleDocTemplate(pdffile, pagesize=(page_width, page_height))
    elements = []

    num_cols = len(data[0])
    col_widths = [(page_width - 200) / num_cols] * num_cols  

    table = Table(data, colWidths=col_widths)
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    elements.append(table)

    doc.build(elements)


if __name__ == "__main__":
    main()