import pytest
from program2 import Student, Question, compare, calculate

def testStudent():
    student = Student("117-2020", "FELA47", "a", "abcde", "21.9.2023.csv", 85)
    assert student.studentID == "117-2020"
    assert student.studyID == "FELA47"
    assert student.group == "a"
    assert student.answers == ["a", "b", "c", "d", "e"]
    assert student.date == "21.9.2023"
    assert student.result == 85

def testMissingStudentID():
    with pytest.raises(ValueError, match="Missing student's ID"):
        Student("", "FEAL47", "a", "abcde", "21.9.2023.csv", 85)

def testMissingStudyID():
    with pytest.raises(ValueError, match="Missing study's ID"):
        Student("117-2020", "", "a", "abcde", "21.9.2023.csv", 85)

def testMissingGroup():
    with pytest.raises(ValueError, match="Missing student's group"):
        Student("117-2020", "FEAL47", "", "abcde", "21.9.2023.csv", 85)

def testMissingAnswers():
    with pytest.raises(ValueError, match="Missing student's answers"):
        Student("117-2020", "FEAL47", "a", "", "21.9.2023.csv", 85)

def testMissingDate():
    with pytest.raises(ValueError, match="Missing date"):
       Student("117-2020", "FEAL47", "a", "abcde", "", 85)

def testQuestion():
    question = Question("a", 1, 2)
    assert question.answer == "a"
    assert question.positive == 1
    assert question.negative == 2

def testQuestionMissingAnswer():
    with pytest.raises(ValueError, match="Missing question's answer"):
        Question("", 1, 2)

#negative points can be zero
def testQuestionNegativePoints():
    question = Question("b", 5, 0)
    assert question.negative == 0

#negative points should not be negative
def testQuestionNegativePointsNegativeValue():
    with pytest.raises(ValueError, match="Points should not be negative"):
        Question("c", 1, -1)

#positive points should not be negative
def testQuestionPositivePointsNegativeValue():
    with pytest.raises(ValueError, match="Points should not be negative or zero"):
        Question("d", -1, 2)

def testCompareAllCorrect():
    student_answers = ["a", "b", "c"]
    correct_answers = [
        Question("a", 1, 2),
        Question("b", 2, 1),
        Question("c", 1, 1)
    ]
    result = compare(student_answers, correct_answers)
    assert result == 4

def testCompareSomeWrong():
    student_answers = ["a", "x", "c"]
    correct_answers = [
        Question("a", 1, 2),
        Question("b", 2, 1),
        Question("c", 1, 1)
    ]
    result = compare(student_answers, correct_answers)
    assert result == 1 

def testCompareAllWrong():
    student_answers = ["x", "y", "z"]
    correct_answers = [
        Question("a", 1, 2),
        Question("b", 2, 1),
        Question("c", 1, 1)
    ]
    result = compare(student_answers, correct_answers)
    assert result == 0  


def testCalculateZero():
    result = 0
    number = 100
    percentage = calculate(result, number)
    assert percentage == 0

def testCalculateHundred():
    result = 100
    number = 100
    percentage = calculate(result, number)
    assert percentage == 100

def testCalculateResult():
    result = 75
    number = 150
    percentage = calculate(result, number)
    assert percentage == 50 

def testCalculateRound():
    result = 30
    number = 70
    percentage = calculate(result, number)
    assert percentage == 43  