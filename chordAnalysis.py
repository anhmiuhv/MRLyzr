import music21
import Tkinter
import sys
import argparse



#parsing option from users
parser = argparse.ArgumentParser(description='Process a MusicXML file')
parser.add_argument('filename')
parser.add_argument('-l', '--library', action='store_true', help='Use the pieces in our library')
parser.add_argument('-c','--chordProgression',action='store_true', help='trigger chord identifications')
parser.add_argument('-k', '--keyChange', action= 'store_true' , help='trigger key change identification')
parser.add_argument('-f', '--formFromBarline', action='store_true', help='identify form from the barline of the pieces')
parser.add_argument('-sf','--simpleform', action= 'store_true', help='identify using simpler algorithms, significantly faster');
args = parser.parse_args()

#get the pieces infomation
if args.library:
	b = music21.corpus.parse(args.filename)
else:
	b = music21.converter.parse(args.filename)


class Form:
    def __init__(self, start, firstMelody, key):
        self.start = start
        self.firstMelody = firstMelody
        self.key = key
        self.label = '?'
        
    def isSimilar(self, f1):
        return (f1.firstMelody == self.firstMelody and f1.key == self.key)


listChord = []



def firstMelody(listOfForm):
    bChords = b.chordify()
    b.insert(0,bChords)
    for c in bChords.recurse().getElementsByClass('Chord'):
        c.closedPosition(forceOctave=4, inPlace=True)
    i=0
    count = 0
    diction ={l: [] for l in listOfForm}
    key = b.analyze('key')        
    for c in bChords.recurse().getElementsByClass('Chord'):
        rn = music21.roman.romanNumeralFromChord(c, key)
        listChord.append(str(rn.figure))
        if c.measureNumber == listOfForm[i]:
            diction[listOfForm[i]].append(str(rn.figure))
            count+=1
            if count == 4:
                i+=1
                count = 0
            if len(listOfForm) == i:
                break
    return diction


def findOccurance(diction):
    Occurance = diction
    for key, value in diction.iteritems():
        roman = ' '.join(value)
        Occur = find_sub_list(value, listChord)
        Occurance[key] = Occur
    return Occurance

def find_sub_list(sl,l):
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            results.append(ind)

    return results

def findSimilarForm(first, formList):
    list = []
    i = 0
    for form in formList:
        if first.isSimilar(form):
            list.append(i)
        i+=1
    return list;


def label():
    diction = firstMelody(formFromBarline())
    formList = []
    #list_Of_Key, first = getListOfKey(3)
    i = 0
    for start, list in diction.iteritems():
    	key = b.measures(start, start + 3).analyze('key')
        formList.append(Form(start,list, key))
        i +=1
    char = 97;
    
    for i in xrange(0, len(formList)):
        if formList[i].label == '?':
            similar = findSimilarForm(formList[i], formList)
            for g in similar:
                formList[g].label = chr(char)
            char+=1
        sys.stdout.write(formList[i].label)
                
    sys.stdout.write(" form")
    return formList


#Identify form from Barline
def formFromBarline():
	#search for repeat
	list_Of_Repeat = []
	try:
		if b.parts[0].measure(0) == None:
			first = 1
		else:
			first = 0
	except Exception as e:
		first = 0
	#find the repeat bar
	for c in b.recurse().getElementsByClass(music21.bar.Repeat):
		list_Of_Repeat.append(c.measureNumber)
	list_Of_Repeat = list(set(list_Of_Repeat))

	#Smoothing process
	toSmooth =[]
	for i in xrange(0, len(list_Of_Repeat) - 1):
		if list_Of_Repeat[i + 1] - list_Of_Repeat [i] <= 3:
			toSmooth.append(list_Of_Repeat[i])
	for c in toSmooth:
		list_Of_Repeat.remove(c)

	#search for double barline
	list_of_double = []
	for c in b.recurse().getElementsByClass(music21.bar.Barline):
		if c.style == 'double':
			list_of_double.append(c.measureNumber)

	#Combine list of double barline and repeat barline
	list_Of_Repeat = list_Of_Repeat + list_of_double
	list_Of_Repeat.append(first)
	list_Of_Repeat = list(set(list_Of_Repeat))
	list_Of_Repeat.sort()
	return list_Of_Repeat


#print the form
def printForm(list):
    if len(list) == 0:
        print('no form detected')
        return
    
    i = 0
    for c in b.recurse().getElementsByClass(music21.note.GeneralNote):
		
	    if c.measureNumber == list[i].start:
		    
		    c.addLyric('Section ' + list[i].label)
		    i+=1
		    if i == len(list):
			    break;

    b.show()

#print form for simple algo
def printForm2(list):
    if len(list) == 0:
        print('no form detected')
        return
    
    i = 0
    char = 97
    for c in b.recurse().getElementsByClass(music21.note.GeneralNote):
		
	    if c.measureNumber == list[i]:
		    
		    c.addLyric('Section ' + chr(char))
		    i+=1
		    char+=1
		    if i == len(list):
			    break;

    b.show()

#Identify chord analysis
def chordAna():

	bChords = b.chordify()
	b.insert(0, bChords)
	for c in bChords.recurse().getElementsByClass('Chord'):
		c.closedPosition(forceOctave=4, inPlace=True)

	key = b.analyze('key')
	for c in bChords.recurse().getElementsByClass('Chord'):

		rn = music21.roman.romanNumeralFromChord(c, key)
		c.addLyric(str(rn.figure))
	b.show()		
	return bChords





def getListOfKey(winSize):
	try:
		if b.parts[0].measure(0) == None:
			first = 1;
		else:
			first = 0
	except Exception as e:
		first = 0

    #get the list of key of the pieces
	ka = music21.analysis.floatingKey.KeyAnalyzer(b)
	if winSize == -1:
		list_Of_Key = ka.getRawKeyByMeasure()
	else:
		ka.windowSize = winSize
		list_Of_Key = ka.run()

	if len(list_Of_Key) == 0:
		print('Music score is too short')
		return
	return list_Of_Key, first



#Identify key changes
def keyAna(winSize):
	(list_Of_Key,first) = getListOfKey(winSize)
	prevKey = list_Of_Key[0]
	curKey = list_Of_Key[1]


	#get key change location
	keyChangeLocation = []
	keyChangeLocation.append(first)
	for x in xrange(1,len(list_Of_Key) - 1):
		if prevKey != curKey:
			keyChangeLocation.append(x)
		prevKey = list_Of_Key[x]
		curKey = list_Of_Key[x+1]
	i = 0	
	if len(keyChangeLocation) == 0:
		print('no key change')
		return
	


	#add chord progression of the pieces
	bChords = b.chordify()
	b.insert(0, bChords)
	for c in bChords.recurse().getElementsByClass('Chord'):
		c.closedPosition(forceOctave=4, inPlace=True)
	for c in bChords.recurse().getElementsByClass('Chord'):
		
		if c.measureNumber == keyChangeLocation[i]:
			
			c.addLyric('Key of ' + list_Of_Key[keyChangeLocation[i]].tonicPitchNameWithCase)
			i+=1
			if i == len(keyChangeLocation):
				break
	
	b.show()
	



#Excecution
if args.keyChange:
	keyAna(2)
elif args.chordProgression:
	
	chordAna()
elif args.formFromBarline:
	list = label()
	printForm(list)
elif args.simpleform:
	list = formFromBarline()
	printForm2(list)
else:
	parser.error('No action requested, add -c or -k')	



