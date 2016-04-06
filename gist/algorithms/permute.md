## introduction

Because the full-range search is a basic to a whole set of problems, here is a python implemenation which demonstrate/depict/elucidate/emoby/epitomize/illuminate/illustrate/manifest... a typical implementation of sarch.


## code

```
#############################################
#
# full_permute.py
#
#   This is to show how to do full permutation 
#
#############################################



solution_number = 1


def permute(columnIndices, index, length):
	global solution_number
	if index == length:
			solution_number += 1
			printPermutation(columnIndices)
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

def printPermutation(columnIndices):
	formatted_string = '\t'.join([str(i + 1) for i in columnIndices])
	print("the {:d}th solution is:".format(solution_number))
	print(formatted_string)

if __name__ == "__main__":
	print(range(3, 8))
	solution();

```
