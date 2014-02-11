#parameters
inputdir = 'C:\Users\Superlaza2\Documents\TimberCreek\TimberCreekPython'+\
           '\\class_rosters.txt'
outputdir = 'C:\Users\Superlaza2\Documents\TimberCreek\AnswerSheets'+\
            '\\answer_sheets.html'

''''''#only even number of questions please!
question_number = 30
line_height = 1
font_size = 20
''''''

def create_name_list():
        classes=[]
        temp = {}
        list = open(inputdir).readlines()
        for index in range(0,len(list)):
                if list[index].strip() != '&':
                        #temp[list[index].split(',')[0].replace('-','')+list[index].split(',')[1][1]]=0
                        temp[list[index].split(',')[0].replace('-','')+list[index].split(',')[1][1]]=0

                else:
                        classes.append(temp)
                        temp = {}
        return classes

classes = create_name_list()

file = open(outputdir,'w')

style='.circle{\n'+\
            '\twidth:50px;\n'+\
            '\theight:50px;\n'+\
            '\tborder-radius:25px;\n'+\
            '\tbackground:#000;}\n'+\
       '#left{float:left;}\n'+\
       '#right{float:right}\n'+\
       '#bottom{\n'+\
            '\twidth:100%;\n'+\
            '\tposition:relative;\n'+\
            '\tbottom:0;\n'+\
            '\tmargin-top:70px}\n'+\
        'P.PageBreak{PAGE-BREAK-AFTER:always;}\n'+\
        '#inline {display:inline;}\n'+\
        'h1 {\n'+\
            '\tfont:60px \'century gothic\' sans-serif;\n'+\
            '\twidth:70%;}\n'+\
        'pre {\n'+\
            '\tline-height: '+str(line_height)+';\n'+\
            '\tfont:'+str(font_size)+'px \'century gothic\' sans-serif;}\n'
        
circle='<div class=\"circle\" id=\"{}\"></div>'

file.write(
'<html>\n'+\
    '<head>\n'+\
        '<style>\n'+\
            style+\
        '</style>\n'+\
    '</head>\n'+\
    '<body>\n'
)

#removed period indicator <pre>P'+str(classes.index(period)+2)+'</pre>
for period in classes:
        for name in period.keys():
                file.write('\t<div>\n')
                file.write('\t\t<h1>'+name+'</h1>\n')
                for index in range(0,question_number/2):
                        file.write('\t\t<pre>'+str(index+1)+'\ta\tb\tc\td'+\
                                   '\t\t+\t\t'+str(index+1+question_number/2)+\
                                   '\ta\tb\tc\td</pre>\n')
                file.write('\t\t<div id=\"bottom\">'+circle.format('left')+circle.format('right')+'</div>\n')
                file.write('\t\t<P class=PageBreak></P>\n')
                file.write('\t</div>\n')

file.write('</body>\n</html>')
file.close()
