import sys, os
from pathlib import Path
import re


def runCode(code):
	regexes = ['print\\s(.*)', 
	'string\\s(.*)\\s=\\s(.*)', 
	'int\\s(.*)\\s=\\s(.*)', 
	'printstr\\s(.*)', 
	'printint\\s(.*)', 
	'input\\s(.*)\\s=\\s(.*)', 
	'ifstr\\s(.*)\\s==\\s(.*)', 
	"endstr", 
	"add\\s(\\d)\\s(\\d)", 
	"sub\\s(\\d)\\s(\\d)",
	"openfile\\s(.*)",
	"readchar\\s(\\d)",
	"readline\\s(\\d)",
	"closefile",
	"loop\\s(\\d)",
	"endl\\s(\\d)",
	"ifint\\s(\\d)\\s==\\s(.*)",
	"appendchar\\s(\\d)",
	"resetstr\\s(\\d)",
	"resetint\\s(\\d)",
	"printascii\\s(\\d)"]
	stringMoved = 0
	intMoved = 0
	returnLines = []
	for line in code:
		line = line.replace("\t", "")
		for index, regex in enumerate(regexes):
			args = re.findall(regex, line)
			if args:
				if index == 0:
					returnLines.append("^[" + args[0] + "]*~@")
				if index == 1:
					pos = int(args[0][0])
					text = args[0][1]
					returnLines.append("~>~>" + "~>"*pos + "^[" + text + "]" + "~<~<" + "~<"*pos)
				if index == 2:
					pos = int(args[0][0])
					num = int(args[0][1])
					if num < 10:
						returnLines.append(">>>" + ">>"*pos +"@"+ '+'*num + "<<<" + "<<"*pos)
					else:
						returnLines.append(">>" + ">>"*pos + "@"+'+'*int(num / 10) + '[>++++++++++<-]>' + '+'*(num % 10)  + "<<<" + "<<"*pos)
				if index == 3:
					returnLines.append("~>~>" + "~>"*int(args[0]) + "*" + "~<~<" + "~<"*int(args[0]))
				if index == 4:
					returnLines.append(">>>" + ">>"*int(args[0]) + "~." + "<<<" + "<<"*int(args[0]))
				if index == 5:
					num = int(args[0][0])
					returnLines.append("~>~>" + "~>"*num + "^[" + args[0][1] + "]*^" + "~<~<" + "~<"*num )
				if index == 6: 
					num = int(args[0][0])
					compareTo = args[0][1]
					returnLines.append("~#+%-")
					returnLines.append("~>~>" + "~>"*num + "~%" + "~<~<" + "~<"*num + "^[" + compareTo + "]~%~@")
					returnLines.append("#(")
				if index == 7:
					returnLines.append(")")
				if index == 8:
					pos = int(args[0][0])
					num = int(args[0][1])
					if num < 10:
						returnLines.append(">>>" + ">>"*pos + '+'*num + "<<<" + "<<"*pos)
					else:
						returnLines.append(">>>" + ">>"*pos + '+'*int(num / 10) + '[>++++++++++<-]>' + '+'*(num % 10) + "<<<" + "<<"*pos )
				if index == 9:
					pos = int(args[0][0])
					num = int(args[0][1])
					if num < 10:
						returnLines.append(">>>" + ">>"*pos + '-'*num + "<<<" + "<<"*pos)
					else:
						returnLines.append(">>>" + ">>"*pos + '+'*int(num / 10) + '[>----------<-]>' + '-'*(num % 10) + "<<<" + "<<"*pos)
				if index == 10:
					filename = args[0]
					returnLines.append("^[" + filename + "]!~@")
				if index == 11:
					cell = int(args[0][0])
					returnLines.append(">>>" + ">>"*cell + "&" + "<<<" + "<<"*cell)
				if index == 12:
					cell = int(args[0][0])
					returnLines.append("~>~>" + "~>"*cell + "~&" + "~<~<" + "~<"*cell)
				if index == 13:
					returnLines.append("!")
				if index == 14:
					cell = int(args[0][0])
					returnLines.append(">>>" + ">>"*cell + "[" + "<<<" + "<<"*cell)
				if index == 15:
					cell = int(args[0][0])
					returnLines.append(">>>" + ">>"*cell + "]" + "<<<" + "<<"*cell)
				if index == 16:
					num = int(args[0][0])
					compareTo = int(args[0][1])
					returnLines.append("~#+%-")
					if compareTo < 10:
						returnLines.append(">>>" + ">>"*num + "%" + "<<<" + "<<"*num + '+'*num + "%@")
					else:
						returnLines.append(">>" + ">>"*num + "%" + "<<<" + "<<"*num + '+'*int(num / 10) + '[>++++++++++<-]>' + '+'*(num % 10) + "%@<")
					returnLines.append("#(")
				if index == 17:
					cell = int(args[0][0])
					returnLines.append("~>~>" + "~>"*cell)
					returnLines.append(">>>" + ">>"*cell + ";" + "<<<" + "<<"*cell)
					returnLines.append("~<~<" + "~<"*cell)
				if index == 18:
					cell = int(args[0][0])
					returnLines.append("~>~>" + "~>"*cell + "~@" + "~<~<" + "~<"*cell)
				if index == 19:
					cell = int(args[0][0])
					returnLines.append(">>>" + ">>"*cell + "@" + "<<<" + "<<"*cell)
				if index == 20:
					cell = int(args[0][0])
					returnLines.append(">>>" + ">>"*cell + "." + "<<<" + "<<"*cell)
				#print(returnLines)
	return "\n".join(returnLines)


def openf():
	if len(sys.argv) > 1:
		if Path(sys.argv[1]).is_file():
			f = open(sys.argv[1], "r")
			code = f.readlines()
			f.close()
			f = open("output.txt", 'w')
			f.write(runCode(code).replace("\n", ""))
			f.close()
		else:
			print("File not found!")
	else:
		print("Missing codefile path")
		sys.exit()

openf()