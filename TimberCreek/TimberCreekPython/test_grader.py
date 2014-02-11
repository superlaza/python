#import regular expression module and the native operating system
import re, os

'''========================   parameters  ========================'''

'''directories'''
#directory containing folders representing reach period
dirPeriods = 'C:\Users\Superlaza2\Documents\\Grading\\Recognized'
#directory containing list of student names
dirStudents = 'C:\Users\Superlaza2\Documents\TimberCreek\TimberCreekPython\\'+\
              'class_rosters.txt'

'''fixed values'''
number_of_questions = 30

'''========================   variables  ========================'''
corrupt_files = []
flagged_students = []
#temporary dict to hold each period's answers, which are then added to master list
student_answers = {}

#list containing dict of all periods
master_answer_list = []
master_scores = []


debug = 1
answer_key = ['a','c','b','b','d','b','c','b','c','b','b','a','b','c','d',\
              'a','c','b','b','d','b','c','b','c','b','b','a','b','c','d']

#init that reads file with first and last names
def init():
        classes=[]
        temp = {}
        list = open(dirStudents).readlines()
        for index in range(0,len(list)):
                if list[index].strip() != '&':
                        temp[list[index].strip().lower().split()[0][:-1]]=0
                else:
                        classes.append(temp)
                        temp = {}
        return classes

#init that reads file with just last names
def create_name_list():
        classes=[]
        temp = {}
        list = open(dirStudents).readlines()
        for index in range(0,len(list)):
                if list[index].strip() != '&':
                        #pull last name and first letter of first name
                        temp[(list[index].split(',')[0].replace('-','')+list[index].split(',')[1][1]).lower()]=0
                else:
                        classes.append(temp)
                        temp = {}
        return classes


classes = create_name_list()
print classes

#returns period that the student belongs to (0-5)
#if student isn't found, returns -1
def search(name):
        for period in classes:
            if(name in period.keys()):
                return classes.index(period)
        #couldn't find name in class roster list
        return -1


#this function only gets called on valid student names, recevies student name
#to flag if line is bad
def find_answer(line, student_name):
    results = re.findall("[\[l\|tj] *[a-dA-D] *[\]l\|tj]", line)
    results = map(str.lower, results)
    #remove spaces
    for answer in results:
        results[results.index(answer)] = answer.replace(' ','')
    if len(results)<3:
        flagged_students.append(student_name)
        return -1
    else:
        if(len(results)>=4):
            return -1
        else:
            if '[a]' not in results:
                return 'a'
            if '[b]' not in results:
                return 'b'
            if '[c]' not in results:
                return 'c'
            if '[d]' not in results:
                return 'd'

'''The answers will be in the following format...'''
'''
1) [a] [b] [c] [d]     +     9) [a] [b] [c] [d]
2) [a] [b] [c] [d]     +     10) [a] [b] [c] [d]
3) [a] [b] [c] [d]     +     11) [a] [b] [c] [d]
4) [a] [b] [c] [d]     +     12) [a] [b] [c] [d]
5) [a] [b] [c] [d]     +     13) [a] [b] [c] [d]
6) [a] [b] [c] [d]     +     14) [a] [b] [c] [d]
7) [a] [b] [c] [d]     +     15) [a] [b] [c] [d]
8) [a] [b] [c] [d]     +     16) [a] [b] [c] [d]
'''
#so we input answers into a list in this fashion...
# [ 1, 9, 2, 10, 3, 11, ....  , 8 , 16]
#thus, we must make sure to disentagle the answers before checking against key
#this is the purpose of the function 'disentangle'

def disentangle():
        for period in master_answer_list:
                for student in period.keys():
                        period[student] = [period[student][i] for i in range(0,number_of_questions,2)]+\
                                          [period[student][i] for i in range(1,number_of_questions,2)]

def compile_answers(filename):
    #initialize list to hold students answers
    answer_list = []

    #'with' handles closing of file
    with open(filename, 'r') as file:
        line_iterator = file.__iter__()

        try:
            #name should be on second line, if it's on the first comment next line
            line_iterator.next()
            student_name = line_iterator.next().strip().lower()
            if debug == 1:
                    print student_name
            line_iterator.next()
        except StopIteration:
            #couldn't read file contents
            corrupt_files.append(filename)
            return

        #search for student in roster
        if(search(student_name)!=-1):
            while True:
                try:
                    line_group = line_iterator.next().strip().lower().split('+')
                    #this checks if we have a blank line. if we do, go to next line
                    if '' in line_group:
                        continue
                    #if length of results is <2, split didn't work so return
                    if(len(line_group)<2):
                        corrupt_files.append(filename)
                        return
                    line_answer1 = find_answer(line_group[0], student_name)
                    line_answer2 = find_answer(line_group[1], student_name)
                    #if any answer is flagged, discontinue
                    #find_answer deals with adding students to check list
                    if(line_answer1 == -1 or line_answer2 == -1):
                        return
                    answer_list.append(line_answer1)
                    answer_list.append(line_answer2)
                    if(len(answer_list)==number_of_questions):
                        break
                except StopIteration:
                    break
                
        #student name wasn't found, add file to check list and discontinue
        else:
            corrupt_files.append(filename)
            return
        
        student_answers[student_name] = answer_list

#student_answers represents a structure containing the answers for an entire period
'''student_answers = {student1: [answers1], ... , studentN: [answersN]}'''
#this function returns a structure with the same format, except with the student's
#score as the value
def grade(student_answers):
    score = 0
    student_scores = {}
    for student in student_answers:
        answers = student_answers[student]
        for index in range(0,len(answers)):
            if answers[index] == answer_key[index]:
                score += 1
        student_scores[student] = score
        score = 0
    return student_scores

def find_ungraded():
    ungraded = []
    for period in classes:
        temp = []
        for student in period:
            student_found = False
            for period in master_scores:
                if(student in period.keys()):
                    student_found = True
            if(student_found == False):
                temp.append(student)
        ungraded.append(temp)

    #now add students from the flagged list, removing duplicates
    for student in list(set(flagged_students)):
        if(search(student)!=-1):
            ungraded[search(student)].append(student)

    #remove possible duplicates in each period
    for period in ungraded:
        ungraded[ungraded.index(period)] = list(set(period))
    
    return ungraded

#pretty printing scores, separated by periods
def print_master():
    for period in master_scores:
        print "Period "+str(master_scores.index(period)+2)+"\n"
        for student in sorted(period.iterkeys()):
            print student, period[student]
        print "\n"

#compile an answer set for all students, structured as list of dicts as follows:
'''[ {P1stud1: [ans1], P1stud2: [ans2]}
    ...
    {P7stud1: [ans1], P7stud2: [ans2]} ]'''
for period in range(2,3):
    files_dir = dirPeriods+"\\P"+str(period)
    student_answers = {}
    for filename in os.listdir(files_dir):
        if debug == 1:
                print filename
        compile_answers(files_dir+"\\"+filename)
    master_answer_list.append(student_answers)

#returns a structure similar to the one obtained above except each student is
#matched with their particular score
for period_answer_set in master_answer_list:
    master_scores.append(grade(period_answer_set))

print_master()
#print corrupt_files
#print flagged_students

#print the list of students whose quizzes weren't graded for whatever reason
#print find_ungraded()
