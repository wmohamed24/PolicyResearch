import nltk
from nltk import tokenize
import os

#tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#sentences = tokenize.sent_tokenize(fileReadTemp)




def breakSentence(txtData):
    '''
    breakes the txt file into sentences and each sentence has a starting and ending letter
    Note: not the optimum way of breakingdown the sentences. The mapping of sentences and begin/end letter
    needs to match that of the mapping in the annotations
    '''

    sentences, s2char = list(), list()
    holdString, begin, end = '', 1, 1

    for letter in txtData:
        holdString += letter
        if letter == '.':
            sentences.append(holdString)
            holdString = ''
            s2char.append((begin, end))
            begin = end+1
            end = begin-1
        end += 1
    return sentences, s2char



def createFlows(annotations):
    '''
    Create a dictionary of Flows as well as a dictionary of mapping 
    between labels such as T1 and the annotation
    '''

    hold, t1, t2 = True, "", ""
    for ann in annotations:
        if hold == False:
            break
        ann = ann.split()
        if ann.count("Flow"):
            t1 = ann[2][5:]
            t2 = ann[3][5:]
            hold = False
    data = dict()

    for ann in annotations:
        hold = ann.split()
        data[hold[0]] = ann

    hold, lst, count, h1, total, flows = True, list(), 1, t1, dict(), dict()

    for ann in annotations:
        ann = ann.split()
        if ann.count("Flow"):
            t1 = ann[2][5:]
            t2 = ann[3][5:]
            if (h1 == t1):
                lst.append(ann)
                h1 = t2
            else:
                total[count] = lst
                flows[count] = list()
                lst = list()
                count += 1
                lst.append(ann)
                h1 = t2

    return data, flows, total



def convE(str, data):
    '''
    some annotations start with an E label instead of T, which directs the annotation to another 
    one that start with a T. This function gets the annotation with the T for each annotation with an E
    '''

    ann = data[str]
    toReturn = ""
    while ann[-1].isspace():
        ann = ann[:-1]
    while ann[-1].isnumeric():
        toReturn += ann[-1]
        ann = ann[:-1]
    toReturn += ann[-1]
    toReturn = toReturn[::-1]
    return toReturn

def readSentence(c1, c2):
    '''
    get the sentences between specified letters. The file used here is the one downloaded directly from the website. 
    '''
    x = 0
    s = ""
    file = open ('Data/Niantic_2-9-21_Pure.txt', encoding="utf8")
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
    '''
    adds the indices of the sentences in the flow to the temporary set. Since the matching 
    in the annotation letters and the txt sentences2letters isn't the same, we're allowing a margin of 5 letters for now.
    '''
    for i in range(len(s2char)):
        a, b = s2char[i]
        if c1 >= a-5 and c2 <= b+5:
            temp.add(i)


def processData(sentences, s2char, data, flows, total):

    for x in total:
        tempSet = set()
        dataType = dict()
        dataType['Attribute'], dataType['Subject'], dataType['Modality'], dataType['Recipient'], dataType['Sender'], dataType['Condition'], dataType['Aim'], dataType['Consequence'] = list(), list(), list(), list(), list(), list(), list(), list()
        for ls in total[x]:
            hold1 = ls[2][5:]
            if (hold1.startswith('E')):
                hold1 = convE(hold1.split()[0], data)
            c1 = int(data[hold1].split()[2])
            c2 = int(data[hold1].split()[3])
            addSentences(c1, c2, tempSet)
            flows[x].append((c1, c2))
            s = readSentence(c1, c2)
            dataType[data[hold1].split()[1]].append(s)
        
        s2Flow = list()
        for y in tempSet:
            s2Flow.append(sentences[y])
        
        hold1 = total[x][-1][3][5:]
        if (hold1.startswith('E')):
            hold1 = convE(hold1.split()[0], data)
        c1 = int(data[hold1].split()[2])
        c2 = int(data[hold1].split()[3])
        s = readSentence(c1, c2)
        if s is None:
            print(hold1, s, c1, c2)
        dataType[data[hold1].split()[1]].append(s)
        with open("TrainData/Flow" + str(x) + ".txt", "w") as fp:
            line = ""
            for i in s2Flow:
                line += i + " "
            fp.write(line + '\n')
            for dt in dataType:
                line = dt + ": " + "[" + '/'.join(dataType[dt]) + "]"
                fp.write(line + '\n')


annFile = open('Data/Niantic_2-9-21.ann', encoding="utf8") #Read the annotation file
txtFile = open("Data/Niantic_2-9-21.txt", encoding="utf8") #Read the txt file of the Policy. Note that the file need
#to be processed so that '.' are only included at the end of the sentences
txtData = txtFile.read() 
annotations = annFile.readlines()

sentences, s2char = breakSentence(txtData)
data, flows, total = createFlows(annotations)

if not os.path.exists('TrainData'):
    os.makedirs('TrainData')
processData(sentences, s2char, data, flows, total)
