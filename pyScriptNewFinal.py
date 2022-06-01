import nltk
from nltk import tokenize

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
hold = True
t1, t2 = "", ""
file1 = open('Niantic_2-9-21.ann', encoding="utf8")
Lines = file1.readlines()
file = open("Niantic_2-9-21.txt", encoding="utf8")
fileReadTemp = file.read()
#sentences = tokenize.sent_tokenize(fileReadTemp)
sentences = list()
s2char = list()

holdString = ''
begin, end = 1, 1
for letter in fileReadTemp:
    holdString += letter
    if letter == '.':
        sentences.append(holdString)
        holdString = ''
        s2char.append((begin, end))
        begin = end+1
        end = begin-1
    end += 1

print(sentences[223])
print(s2char[223])

'''
holder = 0
for sentence in sentences:
    start = holder
    for word in sentence:
        for letter in word:
            holder += 1
        end = holder
    s2char.append((start, end))
'''


# Strips the newline character
for line in Lines:
    if hold == False:
        break
    line = line.split()
    if line.count("Flow"):
        t1 = line[2][5:]
        t2 = line[3][5:]
        hold = False
    #print(t1, t2)
data = dict()


for Line in Lines:
    hold = Line.split()
    data[hold[0]] = Line

hold = True
lst = []
count = 1
h1 = t1
total = dict()
flows = dict()

for line in Lines:
    line = line.split()
    if line.count("Flow"):
        t1 = line[2][5:]
        t2 = line[3][5:]
        if (h1 == t1):
            lst.append(line)
            h1 = t2
        else:
            total[count] = lst
            flows[count] = list()
            lst = list()
            count += 1
            lst.append(line)
            h1 = t2



def convE(str):
    temp = data[str]
    test = ""
    while temp[-1].isspace():
        temp = temp[:-1]
    while temp[-1].isnumeric():
        test += temp[-1]
        temp = temp[:-1]
    test += temp[-1]
    test = test[::-1]
    return test

def readfun(c1, c2):
    x = 0
    s = ""
    file = open ('Niantic_2-9-212.txt', encoding="utf8")
    while x < c2:
            # read by character
            char = file.read(1)         
            if x < c1:
                x +=1
                continue
            s += char
            x += 1
    file.close()
    return s


def addSentences (c1, c2, temp):
    for i in range(len(s2char)):
        a, b = s2char[i]
        if c1 >= a-5 and c2 <= b+5:
            temp.add(i)


for x in total:
    tempSet = set()
    dataType = dict()
    dataType['Attribute'], dataType['Subject'], dataType['Modality'], dataType['Recipient'], dataType['Sender'], dataType['Condition'], dataType['Aim'], dataType['Consequence'] = list(), list(), list(), list(), list(), list(), list(), list()
    for ls in total[x]:
        hold1 = ls[2][5:]
        if (hold1.startswith('E')):
            hold1 = convE(hold1.split()[0])
        c1 = int(data[hold1].split()[2])
        c2 = int(data[hold1].split()[3])
        addSentences(c1, c2, tempSet)
        flows[x].append((c1, c2))
        s = readfun(c1, c2)
        dataType[data[hold1].split()[1]].append(s)
    
    s2Flow = list()
    for y in tempSet:
        s2Flow.append(sentences[y])
    
    hold1 = total[x][-1][3][5:]
    if (hold1.startswith('E')):
        hold1 = convE(hold1.split()[0])
    c1 = int(data[hold1].split()[2])
    c2 = int(data[hold1].split()[3])
    s = readfun(c1, c2)
    if s is None:
        print(hold1, s, c1, c2)
    dataType[data[hold1].split()[1]].append(s)


        

    with open("Flow" + str(x) + ".txt", "w") as fp:
        line = ""
        for i in s2Flow:
            line += i + " "
        fp.write(line + '\n')
        for dt in dataType:
            line = dt + ": " + "[" + '/'.join(dataType[dt]) + "]"
            fp.write(line + '\n')


print(total[66])