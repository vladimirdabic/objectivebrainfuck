import sys, os
from pathlib import Path

def returnB(code):
	code = code.replace("\n", "").replace("\t", "")
	code = list(code)
	tempPos = []
	final = {}
	for pos, char in enumerate(code):
		if char in ["[", "("]:
			tempPos.append(pos)
		if char in ["]", ")"]:
			if len(tempPos) > 0:
				val = tempPos.pop()
				final[val] = pos
				final[pos] = val

	return final


def runCode(code):
	positions = returnB(code)
	code = code.replace("\n", "").replace("\t", "")
	code = list(code)
	#print(code)
	cLen = len(code)
	enteredBrackets = []
	curPos = 0
	tape = [0]
	stringTape = [""]
	tPos = 0
	strPos = 0
	stack = []
	fileOpen = None

	while curPos < cLen:
		char = code[curPos]

		#BRAINFUCK INSTRUCTIONS==========

		if char == "+":
			tape[tPos] += 1
			if tape[tPos] == 256:
				tape[tPos] = 0
		if char == "-":
			tape[tPos] -= 1
			if tape[tPos] == -1:
				tape[tPos] = 255
		if char == ">":
			tPos += 1
			if tPos+1 > len(tape):
				tape.append(0)
		if char == "<":
			tPos -= 1
			if tPos == -1:
				tPos = len(tape)-1
		if char == ".":
			print(chr(tape[tPos]), end='')
		if char == ",":
			tape[tPos] = ord(input())
		if char == "[":
			if tape[tPos] == 0:
				curPos = positions[curPos]
		if char == "]":
			if tape[tPos] != 0:
				curPos = positions[curPos]

		# Object-Brainfuck#++ Instructions

		if char == "^":
			if code[curPos+1] != "[":
				stringTape[strPos] = input()
			else:
				valLoop = curPos+2
				strApp = ""
				while code[valLoop] != "]":
					strApp += code[valLoop]
					valLoop += 1
				stringTape[strPos] = strApp
				curPos = valLoop

		if char == "*":
			print(stringTape[strPos].replace("\\n", "\n"), end='')

		if char == "~":
			specFunc = code[curPos+1]
			if specFunc == ">":
				strPos += 1
				if strPos+1 > len(stringTape):
					stringTape.append("")
			if specFunc == "<":
				strPos -= 1
				if strPos == -1:
					strPos = len(stringTape)-1
			if specFunc == "%":
				stack.append(stringTape[strPos])

			if specFunc == "#":
				stack = []

			if specFunc == "@":
				stringTape[strPos] = ""

			if specFunc == ".":
				print(str(tape[tPos]), end='')

			if specFunc == ",":
				tape[tPos] = int(input())

			if specFunc == "$":
				fileOpen.seek(0, os.SEEK_END)
				fileOpen.write(stringTape[strPos].replace("\\n", "\n"))

			if specFunc == "&":
				read = fileOpen.readline()
				if read:
					stringTape[strPos] = read

			if specFunc == ";":
				tape[tPos] = ord(stringTape[strPos][tape[tPos]])

			if specFunc == "`":
				strPos = 0

			curPos +=1

		if char == "%":
			stack.append(tape[tPos])

		if char == "@":
			tape[tPos] = 0

		if char == "#":
			if len(stack) >= 3:
				if stack[0] == 1:
					if str(stack[1]) != str(stack[2]):
						curPos = positions[curPos+1]
			else:
				curPos = positions[curPos+1]

		if char == "!":
			if fileOpen == None:
				fileToOpen = stringTape[strPos]
				fileOpen = open(fileToOpen, 'r+')
			else:
				fileOpen.close()

		if char == "$":
			fileOpen.seek(0, os.SEEK_END)
			fileOpen.write(chr(tape[tPos]))

		if char == "&":
			read = fileOpen.read(1)
			if read:
				tape[tPos] = ord(read)
			else:
				tape[tPos] = 0

		if char == ";":
			stringTape[strPos] += chr(tape[tPos])

		if char == "`":
			tPos = 0






		#=================================

		#print(char)
		curPos+=1

def openf():
	if len(sys.argv) > 1:
		if Path(sys.argv[1]).is_file():
			f = open(sys.argv[1], "r")
			code = f.read()
			f.close()
			runCode(code)
		else:
			print("File not found!")
	else:
		print("Missing codefile path")
		sys.exit()

openf()