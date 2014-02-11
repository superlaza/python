def init():
        classes=[]
        temp = {}
        list = open("C:\Users\Superlaza2\Documents\TimberCreekPython\class_rosters.txt").readlines()
        for index in range(0,len(list)):
                if list[index].strip() != '&':
                        temp[list[index].strip().lower().split()[0][:-1]]=0
                else:
                        classes.append(temp)
                        temp = {}
        return classes

def search(name, periods):
        for p in periods:
                if name in p:
                        return periods.index(p)+2
        return 0
        


def completed_list():
        list = open("C:\Users\Superlaza2\Documents\TimberCreekPython\pretest_completed.txt").readlines()
        for i in range(0,len(list)):
                list[i]=list[i].split()[len(list[i].split())-1].lower()
        return list

#mark who has completed given assignment
classes = init()
completed = completed_list()
for period in classes:
        for name in period.keys():
                if name in completed:
                        period[name] = 1

#print the list of those who did not complete the assignment

pd_count = 2
for period in classes:
        print "Period "+str(pd_count)
        for name in period.keys():
                if period[name] == 0:
                        print name
        pd_count += 1
        print "\n"
                        

