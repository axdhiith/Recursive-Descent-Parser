import re

global infile

###  Lexical Analyzer:  ###
charClass = -1
nextChar = ""
nextToken = -1
lexeme = []
errors = []
flag = -1
lineCounter=1
index=-1
errorCount = 0

Special = ['+','-','*','/','\\','^','~',':','.','?',' ','#','$','&']

#Classes
digit=1;upper=2;lower=3;special=4;EOF=5;other=6

#Tokens
add_op=6;sub_op=7;mul_op=8;div_op=9;backslash=10;triangle=11;tilda=12;colon=13;period=14;question=15;whitespace=16;hashtag=17;dollarsign=18;ampersand=19
openP=20;closeP=21
comma=22;exclamation=23;semicolon=24
tokOther = 25
end = 26

def getChar():  #gets a character from the file and assigns charClass
    global nextChar, lineCounter, infile, index, charClass, lbozo
    nextChar= infile.read(1)
    
    if nextChar == '':
        charClass = EOF
    else:
        if nextChar == '\n':
            lineCounter += 1
            index = -1
            charClass = other
        if re.match("[0-9]",nextChar):
            charClass = digit
        elif re.match("[A-Z\_]",nextChar):
            charClass = upper
        elif re.match("[a-z]",nextChar):
            charClass = lower
        elif nextChar in Special:
            charClass = special
        else: charClass = other
    index += 1
    
def addChar():  #adds a character to the lexeme list
    lexeme.append(nextChar)

def lookup(c):  #calls addChar() and assigns nextToken
    global nextToken, lineCounter, index
    if c == '(':
        addChar()
        nextToken = openP
    elif c == ')':
        addChar()
        nextToken = closeP
    elif c == '+':
        addChar()
        nextToken = add_op
    elif c == '-':
        addChar()
        nextToken = sub_op
    elif c == '*':
        addChar()
        nextToken = mul_op
    elif c == '/':
        addChar()
        nextToken = div_op
    elif c == '\\':
        addChar()
        nextToken = backslash
    elif c == '^':
        addChar()
        nextToken = triangle
    elif c == '~':
        addChar()
        nextToken = tilda
    elif c == ':':
        addChar()
        nextToken = colon
    elif c == '.':
        addChar()
        nextToken = period
    elif c == '?':
        addChar()
        nextToken = question
    elif c == '#':
        addChar()
        nextToken = hashtag
    elif c == ' ':
        addChar()
        nextToken = whitespace
    elif c == '$':
        addChar()
        nextToken = dollarsign
    elif c == '&':
        addChar()
        nextToken = ampersand
    elif c == ',':
        addChar()
        nextToken = comma
    elif c == ';':
        addChar()
        nextToken = semicolon
    elif c == '!':
        addChar()
        nextToken = exclamation
    elif c == '\n':
        lineCounter += 1
        index = -1
    elif c != '':
        addChar()
        nextToken = tokOther
    else:
        addChar()
        nextToken = end
        
    return nextToken

        
def lex():  #the main function that will be called to get a character from the file 
    global lexeme, nextChar, nextToken
    
    if charClass == other or charClass == special:
        lookup(nextChar)
        getChar()
    elif charClass == EOF:
        addChar()
    elif charClass == digit:
        addChar()
        getChar()
        nextToken = digit
    elif charClass == lower:
        addChar()
        getChar()
        nextToken = lower
    elif charClass == upper:
        addChar()
        getChar()
        nextToken = upper 
    else:             
        getChar()
    #to skip whitespaces
    if nextChar == " " or nextChar == '\n' or nextChar == '\t':
        while(nextChar == " " or nextChar == '\n' or nextChar == '\t'):
            lookup(nextChar)
            getChar()


###  Syntax Analyzer:  ###
def special():  #checks if it follows the <special> syntax in the given grammar
    global nextToken, nextChar, errorCount
    if (nextToken == add_op or nextToken == sub_op or nextToken == mul_op or nextToken == div_op or nextToken == backslash or nextToken == triangle or nextToken == tilda or nextToken == colon or nextToken == period or nextToken == question or nextToken == whitespace or nextToken == hashtag or nextToken == dollarsign or nextToken == ampersand):
        lex()
        return True
    else:
        errors.append(f'Line and Index ({lineCounter},{index})- Invalid Symbol')
        errorCount += 1
        getChar()
        lex()
        return False
    
def lowercase_char():   #checks if it follows the <lowercase-char> syntax in the given grammar
    global nextChar, charClass
    if charClass == lower:
        return True
    else:
        return False
    
def uppercase_char():   #checks if it follows the <uppercase-char> syntax in the given grammar
    global nextChar, charClass
    if charClass == upper:
        return True
    else:
        return False

def digit():    #checks if it follows the <digit> syntax in the given grammar
    global nextChar, charClass, errorCount
    if charClass == digit:
        return True
    else:
        return False

def numeral():  #checks if it follows the <numeral> syntax in the given grammar
    global nextToken, nextChar
    if digit():
        while digit():
            lex()
        return True
    else:
        return False
    
def alphanumeric(): #checks if it follows the <alphanumeric> syntax in the given grammar
    global nextToken, nextChar
    if lowercase_char() or uppercase_char() or digit():
        return True
    else:
        return False

def character():    #checks if it follows the <character> syntax in the given grammar
    global nextToken, nextChar, errorCount
    if alphanumeric() | special():
        return True
    else:
        errors.append(f'Line and Index ({lineCounter},{index})- Invalid Character')
        errorCount += 1
        return False
    
def string():   #checks if it follows the <string> syntax in the given grammar
    global nextToken, nextChar
    if character():
        while (character()):
            lex()
        return True
    else:
        return False
    
def character_list():   #checks if it follows the <character-list> syntax in the given grammar
    global nextToken, nextChar
    if alphanumeric():
        while(alphanumeric()):
            lex()
        return True
    else:
        return False
    
def variable(): #checks if it follows the <variable> syntax in the given grammar
    global nextToken, nextChar
    if uppercase_char():
        lex()
        if character_list():
            return True
        return True
    else:
        return False

def small_atom():   #checks if it follows the <small-atom> syntax in the given grammar
    global nextToken, nextChar
    if lowercase_char():
        lex()
        if character_list():
            return True
        return True
    else:
        return False

def atom(): #checks if it follows the <atom> syntax in the given grammar
    global nextToken, nextChar
    if small_atom():
        return True
    elif nextChar == "'":
        lex()
        if string():
            lex()
            if nextChar == "'":
                lex()
                return True
            else:
                errors.append(f"Line and Index ({lineCounter},{index})- No ending '")
                return False
        else:
            return False           
    return False

def structure():    #checks if it follows the <structure> syntax in the given grammar
    global nextToken, nextChar, errorCount
    if atom():
        if nextChar == '(':
            lex()
            if term_list():
                if nextChar == ')':
                    return True
                else:
                    errors.append(f'Line and Index ({lineCounter},{index})- Missing Parenthesis')
                    errorCount += 1
                    return False
            else:
                errors.append(f'Line and Index ({lineCounter},{index})- Missing Term List')
                errorCount += 1
    return False
        
def term(): #checks if it follows the <term> syntax in the given grammar
    global nextToken, nextChar, errorCount
    if atom():
        if nextChar == "(":
            lex()
            if term_list():
                if nextChar == ')':
                    lex()
                    return True
            else:
                errors.append(f'Line and Index ({lineCounter},{index})- Missing Parenthesis')
                errorCount += 1
                return False
        return True
    elif variable() or numeral():
        return True
    return False

def term_list():    #checks if it follows the <term-list> syntax in the given grammar
    global nextToken, nextChar, errorCount
    if term():
        if nextChar == ',':
            lex()
            term_list()
        return True
    else:
        errors.append(f'Line and Index ({lineCounter},{index})- Not a Term List')
        errorCount += 1
        return False

def predicate():    #checks if it follows the <predicate> syntax in the given grammar
    global nextToken, nextChar, errorCount 
    if atom():
        if nextChar == '(':
            lex()
            if term_list():
                if nextChar == ')':
                    lex()
        return True
    errors.append(f'Line and Index ({lineCounter},{index})- Not a Term List')
    errorCount += 1
    return False

def predicate_list():   #checks if it follows the <predicate-list> syntax in the given grammar
    global nextToken, nextChar
    if predicate():
        if nextChar == ',':
            lex()
            predicate_list()
        return True
    else:
        return False   

def query():    #checks if it follows the <query> syntax in the given grammar
    global nextToken, nextChar, errorCount
    if nextChar == '?':
        lex()
        if nextChar == '-':
            lex()
            if predicate_list():
                if nextChar == '.':
                    lex()
                    return True
                else:
                    errors.append(f'Line and Index ({lineCounter},{index})- Not a valid Query')
                    errorCount += 1
    return False

def clause():   #checks if it follows the <clause> syntax in the given grammar
    global nextToken, nextChar
    if predicate():
        if nextChar == '.':
            lex()
            return True
        elif nextChar == ':':
            lex()
            if nextChar == '-':
                lex()
                if predicate_list():
                    if nextChar == '.':
                        lex()
                        return True
    return False

def clause_list():  #checks if it follows the <clause-list> syntax in the given grammar
    if clause():
        while (clause()):
            continue
        return True
    return False

def program():  #checks if it follows the <program> syntax in the given grammar
    global flag
    lex()
    if query():
        flag = 0
        return True
    elif clause_list():
        if query():
            flag = 0
            return True
    return False


#### Driver ####
import os

infile = None
files = []
out = open("parser_output.txt","w")
for f in os.listdir(os.getcwd()):
    if '.txt' in f and f!='parser_output.txt':
        files.append(f)
if (len(files)==0):
    print('There are no files in this directory.')

counter = 1                         #counter for text file numbers
while str(counter)+".txt" in files:
    try:
        f = str(counter)+".txt"
        infile = open(f,'r')
        out.write("\n\n"*(counter >= 2)+"File: "+ f + "\n")     #eliminates blank lines for File1
        program()
        if flag == 0:
            out.write("It is Syntactically Correct!")
        elif (len(errors)>0):
            out.write(str(len(errors)) + " error" + ("s" if len(errors)>1 else "") + " found!\n")
            for i in errors:
                out.write(i)
                out.write('\n')
                
        #resets all the global variables so that program() can be called again
        counter += 1
        charClass = -1
        nextChar = ""
        nextToken = -1
        lexeme = []
        errors = []
        flag = -1
        lineCounter=1
        index=-1
        errorCount = 0

    except FileNotFoundError:
        out.write("File not found")

out.close()
infile.close()