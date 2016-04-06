# file: php_formatter.py
# description: format php source files
# author: joe
# 

'''php_formatter.py - module to format php source file based on state of "{" and "}"'''


import sys
import StringIO

def format():
	char = sys.stdin.read(1)
	output = StringIO.StringIO()
	indent = 0
	newline = False
	while True:
		char = sys.stdin.read(1)
		if char == "": break
		if char == "{":
			indent += 1
		elif char == "}":
			indent -= 1
		elif char == "\n":
			newline = True

		if newline and not char == "\n":
			output.write("  " * indent)
			newline = False
		output.write(char)
	return output.getvalue()


if __name__ == "__main__":
	print format()
