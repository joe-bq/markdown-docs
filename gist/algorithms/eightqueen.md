## Introduction 
eighteen queen problem is a very basic all-range search algorithm, which is a foundamental to all lots of other problems.

Below I will give the Python implemnation eightqueen problems.

## code
```
#############################################
#
# eight_queens.py
#
#   this is a solution to the eight queens problem
#
#############################################



solution_number = 1

def check(columnIndices):
	for i in range(len(columnIndices)):
		for j in range(i + 1, len(columnIndices)):
			if j - i == columnIndices[j] - columnIndices[i] or j - i == columnIndices[i] - columnIndices[j]:
				return False
	return True

def permute(columnIndices, index, length):
	global solution_number
	if index == length:
		if check(columnIndices):
			solution_number += 1
			printSolution(columnIndices)
		pass
	else:
		for i in range(index, length):
			temp = columnIndices[i]
			columnIndices[i] = columnIndices[index]
			columnIndices[index] = temp

			permute(columnIndices, index + 1, length)

			temp = columnIndices[i]
			columnIndices[i] = columnIndices[index]
			columnIndices[index] = temp


def solution():
	a = [];
	for x in range(8):
		a.append(x);
	permute(a, 0, len(a))

def printSolution(columnIndices):
	print("Solution no. %d" % (solution_number))
	formatted_string = "\t".join([str(i+1) for i in columnIndices])
	print(formatted_string)


if __name__ == "__main__":
	print(range(3, 8))
	solution();

```
