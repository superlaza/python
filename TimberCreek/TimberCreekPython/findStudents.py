def init():
        p=[]
        for i in range(2,8):
                list = open("C:\Users\User\Documents\Texts\p"+str(i)+".txt").readlines()
                for index in range(0,len(list)):
                        list[index] = list[index].lower().strip().split()[0][:-1]
                p.append(list)
        return p

def search(name, periods):
        for p in periods:
                if name in p:
                        return periods.index(p)+2
        return 0
        


def edmodo_list():
        list = open("C:\Users\User\Documents\Texts\edmodo_list.txt").readlines()
        for i in range(0,len(list)):
                list[i]=list[i].split()[len(list[i].split())-1].lower()
        return list

periods = init()
print edmodo_list()
for name in edmodo_list():
        if search(name, periods)==7:
                print name, search(name, periods)
