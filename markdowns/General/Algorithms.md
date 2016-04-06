## Introduction 
this page is mainly about the algorithm practices that is meant to improve my sense of the algorithms and keep sharp.


## permutation 

permutation is a brutal force solution. and we sometimes need to get the full permutation, below is the full permutation (implicit recursive) pay attention to how it maintains the invariants of the conditions 

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

## Eight queens problem
with the help of the full permutation, here is a eight_queue problem.... 

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

## balanced parentheses

the problem is to find all the combination of the balanced parentheses around some expression. it is useful to generate some evaluation algorithm based on some expression (like the auto-calculation of the 24 points)

below is one implementation of the balanced parenthesis, here is the code. 

```
#############################################
#
# balanced_parentheses.py
#
#   this is a program to show you how to list all the possible balanced parentheses
#
#############################################

def parenthesized(exprs):
	if len(exprs) == 1:
		yield exprs[0]
	else:
		first_exprs = []
		last_exprs = list(exprs)
		while 1 < len(last_exprs):
			first_exprs.append(last_exprs.pop(0))
			for x in parenthesized(first_exprs):
				if 1 < len(first_exprs):
					x = '(%s)' % x
				for y in parenthesized(last_exprs):
					if 1 < len(last_exprs):
						y = '(%s)' % y
					yield '%s%s' % (x, y)

for x in parenthesized(list(['a', 'b', 'c', 'd'])):
	print x
```

basically it is also a recursion happening here. 

there is also a more concise implementation of the balanced expressions., below is the code. 

```
#############################################
#
# balanced_parentheses_solutionII.py
#
#   this is a program to show you how to list all the possible balanced parentheses
#
#############################################

def association(seq, **kw):
	grouper = kw.get("grouper", lambda x, y: (x, y))
	lifter = kw.get("lifter", lambda x: x)
	if len(seq) == 1:
		yield lifter(seq[0])
	else:
		for i in range(len(seq)):
			left = seq[:i]
			right = seq[i:]
			for x in association(left, **kw):
				for y in association(right, **kw):
					yield grouper(x, y)

for x in association(['a', 'b', 'c', 'd']):
	print x
```

the induction of the concept called 'lifter' and 'grouper' is the key to the problems.

## resources

in order to keep the momentum on the road, here are the resources that can help you gather strength...

> Hi Joe, 
		You can visit the following course from here:  
		https://www.coursera.org/princeton
		the pdf books 
	   Cracking the Coding Interviews: http://www.mktechnicalclasses.com/Notes/Cracking%20the%20Coding%20Interview,%204%20Edition%20-%20150%20Programming%20Interview%20Questions%20and%20Solutions.pdf 
		Or you can try to leetcode
		https://oj.leetcode.com/
	    http://leetcode.com/    



## Longest palindrome problem 

the longest palindrome problem is actually a DP problem. and here is the recursion equation. 

1. for each s[i, i], the m[i, i] = 1
2. for each s[i, i+1], if s[i] == s[i+1], then m[i, i+1] = 2
3. for each s[i, j], if s[i+1, j-1] == j-i-3 and s[i] == s[j] then m[i, j] = j-i+1

given this, we can have a naiive implementation which requires n*n spaces. 

```
#############################################
#
# longest_palindrome.py
#
#   this is the naive implementation of palindrome
#
#############################################

def initialize(s):
	table = [[1 if x == y else 0 for x in range(len(s))] for y in range(len(s))]
	for x in range(len(s) - 1):
		if s[x] == s[x+1]:
			table[x][x+1] = 2
	return table

def printTable(table):
	for i in range(len(table)):
		for j in range(len(table[i])):
			print("{0},{1}: {2}".format(i, j, table[i][j]))

def palindrome(s):
	table = initialize(s)
	start = end = -1
	longest = 0
	for i in range(2, len(s)+1):
		for j in range(len(s) - i):
			k = i + j
			if s[j] == s[k] and table[j+1][k-1] != 0:
				print("Here")
				table[j][k] = i
				if longest < i:
					longest = i
					start = j
					end = k
	printTable(table)
	print("Longest palindrome in {0} is {1}, length = {2}, start = {3}".format(s, s[start: end], longest, start))

if __name__ == "__main__":
	palindrome("abffcycffca")
```

while we can improve the space by a magnitude, check the following code. 

```
#############################################
#
# longest_Palindrome_nspaces.py
#
#   this program will show you how to get the longest palindrome sequence from a string with only n extra spaces. 
#
#############################################

def initialize(s, n):
	m = [[1, 0] for i in range(n)]
	for i in range(n - 1):
		if (s[i] == s[i+1]):
			m[i][1] = 2
	return m

def longest_palindrome(s):
	length = len(s)
	start = end = -1
	longest = -1
	m = initialize(s, length)
	# 
	# two groups:
	# 0, 2, 4, ... 
	# 1, 3, 5,...
	# given an example, if the current difference is 2, then it value is calculated 
	# based on s[i] === s[i+2] and m[i+1][0]; and if the current difference is 3, then the value is 
	# calcaulted based on the s[i] == s[i+2] and m[i+1][1]
	for i in range(2, length):
		for j in range(0, length - i):
			if s[j] == s[i+j] and m[j+1][j%2] == i - 1:
				m[j][(j+1)%2] = i + 1
				if m[j][(j+1)%2] > longest:
					longest = m[j][(j+1)%2]
					start = j
					end = i + j
	print("The longest palindrome for string {0} is {1}, start = {2}, length = {3}".format(s, s[start:end], start, end - start))


longest_palindrome("adjabhhehchehhba")
```

the key here is that we only need to keep record of the longest palindrome values for one set of (0, 2, 4, ....) length, and another record for the values of another set of (1, 3, 5, ...)


## left-truncatable prime

the problem can be read as below. 

>Problem #4:  Write a program that reads in a single integer N (such that:  1 <= N <= 2166), and outputs the nth left-truncatable prime. a left-truncatable prime is a prime number which, in a given base, contains no 0, and if the leading("left") digit is successively removed, then all resulting numbers are prime, For example 9137, since 9137, 137, 37, and 7 are all prime.

here is my solution

```
#############################################
#
# left_truncatable.py
#
#   left trancatable prime
#
# background:
#   left truncatable prim is the prime that if you take out each digit from left and the remaining 
#############################################

prime_list = [2, ]
def get_prime_array(n):
	''' get the nth prime '''
	for x in range(n):
		if len(prime_list) > x:
			continue
		else:
			k = prime_list[-1]
			while True:
				k += 1
				isPrime = True
				for x in range(len(prime_list)):
					if k % prime_list[x] == 0:
						isPrime = False
						break

				if isPrime:
					prime_list.append(k)
					if len(prime_list) >= n:
						break;
	return prime_list

def is_left_truncatable_prime(n):
	''' n is a prime number, tell whether it is a left_truncatable prime number '''
	while prime_list[-1] < n:
		get_prim_array(len(prime_list))

	while str(n)[1:] != '' and n in prime_list:
		n = int(str(n)[1:])

	if n < 10 and n in prime_list:
		return True
	else:
		return False


def nth_truncatable_prim(n):
	i = j = 1

	truncatable_prime_list = []
	while True:
		get_prime_array(i)
		i += 1
		if is_left_truncatable_prime(prime_list[-1]):
			truncatable_prime_list.append(prime_list[-1])
			if j >= n:
				break
			j += 1
	return truncatable_prime_list[-1]


if __name__ == "__main__":
	print("100th of the left-truncatable prime is {0}".format(nth_truncatable_prim(100)))
```


## return list of numbers inclusive

the original questions is as follow. 

> Return the set of all integers in the range [r1,r2] inclusive (r1,r2 > 0), which are multiples of m1,m2.
Example:   m1=4, m2=6 ; r1=3, r2=12 returns { 4, 6, 8, 12 }

here is my solution, shown belwo. 

```
#############################################
#
# inclusive_set.py
#
#   Find all the inclusive set of numbers
#
# the original questions is as follow.
#    Return the set of all integers in the range [r1,r2] inclusive (r1,r2 > 0), which are multiples of m1,m2.
#    Example:   m1=4, m2=6 ; r1=3, r2=12 returns { 4, 6, 8, 12 }
#############################################

def return_inclusive_set(m1, m2, r1, r2):
	def iter_inclusive_set(m1, m2, r1, r2):
		i = j = 1
		while True:
			if i * m1 > r2 and j * m2 > r2: 
				break
			if i * m1 < j * m2:
				if i * m1 >= r1 and i * m1 <= r2:
					yield i * m1
				i += 1
			elif i * m1 == j * m2:
				if i * m1 >= r1 and i * m1 <= r2:
					yield i * m1
				i += 1
				j += 1
			else:
				if j * m1 >= r1 and j * m2 <= r2:
					yield j * m2
				j += 1
	return iter_inclusive_set(m1, m2, r1, r2)
if __name__ == "__main__":
	for x in return_inclusive_set(4, 6, 3, 12):
		print x
```

## Microprocessor simulator
The Microprocessor simulator itself is not a very complicated exercise, however, it requires some solid understanding of program composition. 

the origin of this question is from the PKU online code test. 
Question: [Microprocessor Simulation](http://poj.org/problem?id=1049)

the complete my anser is:

```
package simulation.microprocessor;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;


/*
 * Problem ID: http://poj.org/problem?id=1049
 * 
 */
public class MicroprocessorSimSolution {

	/* =================== 
	 * Constants
	 *  =================== */
	
	// http://en.wikipedia.org/wiki/List_of_Java_keywords
	// Though reserved as a keyword in java, const is not used and has no function for defining constants in java, you can see the "final" reserved word instead
	// [Why is there no Constant keyword in Java? - Stack Overflow](http://stackoverflow.com/questions/2735736/why-is-there-no-constant-keyword-in-java)
	// 
	public static final int LD = 0;
	public static final int ST = 1;
	public static final int SWP = 2;
	public static final int ADD = 3;
	public static final int INC = 4;
	public static final int DEC = 5;
	public static final int BZ = 6;
	public static final int BR = 7;
	public static final int STP = 8;
	public static final int INVALID = -1;
	public static final int INVALID_MEMORY = -1;
	public static final int SIZE = 256;
	
	/* =================== 
	 * private fields
	 *  =================== */
	public volatile int A;
	public volatile int B;
	
	public volatile int _pointer;
	
	
	private final byte[] _memory;
	private boolean _stop = false;
	
	
	/* =================== 
	 * Constructor(s)
	 *  =================== */
	public MicroprocessorSimSolution() 	{
		_memory = new byte[256];
		for (int i = 0; i < 256; i++) { 
			_memory[i] = 0;
		}
	}
	
	public String dump() {
		StringBuilder sb = new StringBuilder();
		
		for (byte i : _memory)  
		{
			sb.append(Integer.toHexString(i).toUpperCase());
		}
		
		return sb.toString();
	}
	
	public void load() {
		// Use of the BufferedRead
		BufferedReader reader =new BufferedReader(new InputStreamReader(System.in));
		int character = -1;
		try
		{
			int readp= -1;
			while ((character = reader.read()) != -1) { 
				_memory[++readp] = parseMemory(character);
			}
			
			assert readp == 255: "Invalid memory inputs"; // what does the java assert do.
		} catch (Exception ex) { 
			//
			ex.printStackTrace();
		}
	}
	
	public void loadFromString(String string) {
		BufferedReader reader = new BufferedReader(new InputStreamReader(new ByteArrayInputStream(string.getBytes())));
		int character = -1;
		try {
			int readp = -1;
			while ((character = reader.read()) != -1) {
				_memory[++readp] = parseMemory(character);
			}
			
			assert readp == 255: this;
		} catch (Exception ex) { 
			ex.printStackTrace();
		}
	}
	
	private byte parseMemory(int character) { 
		if (character >= '0' && character <= '9') { 
			return (byte)(character - '0');
		}
		
		if (character >= 'A' && character <= 'F') { 
			return (byte)(character - 'A' + 10) ;
		}
		
		return INVALID_MEMORY;
	}
	
	public void processLoad() 	{
		A = readAddress(readNext(), readNext());
	}
	
	public void processStore()	{
		writeAddress(readNext(), readNext(), A);
	}
	
	public void processSwap()	{
		int temp = A;
		A = B;
		B = temp;
	}
	
	public void processAdd()	{
		int tempA = A;
		int tempB = B;
		A = (tempA + tempB) % 16;
		B = (tempA + tempB) / 16;
	}
	
	public void processInc()	{
		A = (A + 1) % 16;
	}
	
	public void processDec() {
		A = (A + 15) % 16;
	}
	
	
	public void processBz() {
		byte hi = readNext();
		byte low = readNext();
		if (A == 0) { 
			_pointer = readAddress(hi, low);
		}
	}
	
	public void processBr() { 
		byte hi = readNext();
		byte low = readNext();
		_pointer = readAddress(hi, low);
	}
	
	public void processStop() { 
		_pointer = -1;
		_stop = true;
	}
	
	public int address(byte hi, byte low) {
		return hi * 16 + low;
	}
	
	public byte readAddress(byte hi, byte low) {
		return _memory[address(hi, low)];
	}

	public void writeAddress(byte hi, byte low, int value) { 
		 _memory[address(hi, low)] = (byte) value;
	}
	
	private byte readNext() {
		return _memory[_pointer++];
	}
	
	public void execute() {
		while (!_stop) { 
			int code = nextInstruction();
			switch (code) { 
				case LD:
					processLoad();
					break;
				case ST:
					processStore();
					break;
				case SWP:
					processSwap();
					break;
				case ADD:
					processAdd();
					break;
				case INC:
					processInc();
					break;
				case DEC: 
					processDec();
					break;
				case BZ:
					processBz();
					break;
				case BR:
					processBr();
					break;
				case STP:
					processStop();
					break;
			}
		}
	}
	
	public int nextInstruction() { 
		return _memory[_pointer++];
	}
	
	
	
	/* =================== 
	 * Private helpers
	 *  =================== */
	
	
	public static void main(String[] args) { 
		MicroprocessorSimSolution solution = new MicroprocessorSimSolution();
//		solution.load();
		solution.loadFromString("0102011311321128FF0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000");
		solution.execute();
		String memory = solution.dump();
		System.out.println(memory);
	}
}
```

## Bitwise operations - to find a number which appears only odd times in an array of numbers which appears even times.

```
import java.util.ArrayList;

/* suppose that there is array of numbers, one nubmer appears odd times, while all other numbers appears even times */

public class BitWiseSolution {
	
	public static void main(String[] args) 	{
		ArrayList<Integer> array = new ArrayList<Integer>();
		array.add(3);
		array.add(3);
		array.add(5);
		array.add(6);
		array.add(6);
		array.add(7);
		array.add(7);
		
		int number = 0;
		for (int i : array)	{
			number ^= i;
		}
		
		System.out.println("the number that we want to find is " + number);
	}
}

```

## Bit operations - general find a number which appears only once whlie other numbers appears thrice.

the key to this kind of problem is that you can treat each number as a sequence of digitis (bits). the digits can be only 1 or 0, indicating whether it exists or not.

here is one solution that does it.

```
import java.util.ArrayList;
import java.util.Arrays;


/* Suppose that for an array of numbers, one appears once, while the others appears three times, find it */
public class BitWiseSolution2 {
	
	public static void main(String[] args) 	{
		ArrayList<Integer> array = new ArrayList<Integer>();
		array.addAll(Arrays.asList(2, 2, 2, 3, 3, 3, 1, 5, 5, 5, 6,6,6));
		
		int[] bits = new int[32]; /* suppose that we are working with a 32-bit numbers */
		
		/*
		for (int i : array) {
			for (int j = 0; j < 32; j++) { 
				bits[j] += (((1 << j) & array.get(i)) == 0 ? 0 : 1);
			}
		}
		*/
		for (int i : array) { 
			int j = 0;
		
		/*
			do {
				if (1 == (i & 1)) {
					bits[j]++;
				}
				j++;
				i <<= 1;
			} while (i != 0);
		*/
			while (i != 0) {
				if (1 == (i & 1)) {
					bits[j]++;
					
				}
				j++;
				i <<=1 ;
			}
		}
		
//		int number = -1; // whose binary representation should be 11111111
		int number = 0;
		for (int i = 0; i < 32; i++) { 
			 if (bits[i] % 3 == 1) { 
				 number |= (1 << i);
			 }
		}
		
		System.out.println("the number which appears only once is " + number);
		
	}
}
```

## the string number codecs problems

given that we know each of the code comprises of CAPITAL digits from 'A' to 'Z'. the length of the string is n where the 1<=n<=26; we know that each of the capital is different in the string. and suppose that the for n = 3, 

```
ABC 0
ABD 1
.... 
ZYX 15599
```

while you may wonder how comes the value 15599, it is the result of 
`26*25*24 - 1`

now, given that my first attempt has the following code. 

```
public class Main {

	public static void main(String[] args) {
		
		Scanner scanner = new Scanner(System.in);
		
		int length = 0;
		String code = "";
		
		while ((length = scanner.nextInt()) != 0) { 
			scanner.nextLine();
			code = scanner.nextLine();
			int number = 0;
			char[] chars = new char[26];
			for (int i = 0; i < 26; i++) {
				chars[i] = 0;
			}
			
			for (int i = 0; i < length; i++) {
				char found = 'A';
				for (int j = 0; j < 26; j++) { 
					if (chars[j] == 0) { 
						found += j;
						break;
					}
				}
				
				number += (code.charAt(i) - found) * pow(i, length);
				chars[code.charAt(i) - 'A'] = 1;
			}
			System.out.println(number);
		}
	}
	
	public static int pow(int i, int length) {
		int dis = 26 - i;
		int number = 1;
		i++;
		dis--;
		for (; i < length; i++) {
			number *= dis;
			dis --;
			
		}
		
		return number;
	}
}
```

it failes because it fail to consider the situation such as

`ADE`, were the last digits 's base does begin with 'B", but in the middle we cannot count 'D' which appears in the previous strings. 

so here is my second attempt

```
import java.util.Scanner;

public class Main {

	public static void main(String[] args) {
		
		Scanner scanner = new Scanner(System.in);
		
		int length = 0;
		String code = "";
		
		while ((length = scanner.nextInt()) != 0) { 
			scanner.nextLine();
			code = scanner.nextLine();
			int number = 0;
			char[] chars = new char[26];
			for (int i = 0; i < 26; i++) {
				chars[i] = 0;
			}
			
			for (int i = 0; i < length; i++) {
				char base = 'A';
				boolean foundBase = false;
				int biggerThanBase= 0;
				for (int j = 0; j < 26; j++) { 
					if (chars[j] == 0) {
						if (!foundBase) {
							base += j;
							foundBase = true;
							continue;	
						}
					} else if (chars[j] == 1) {
						if (foundBase) {
							if (j+ 'A' < code.charAt(i)) {
								biggerThanBase++;	
							}
						}
					}
					
				}
				
				number += (code.charAt(i) - base - biggerThanBase) * pow(i, length);
				chars[code.charAt(i) - 'A'] = 1;
			}
			System.out.println(number);
		}
	}
	
	public static int pow(int i, int length) {
		int dis = 26 - i;
		int number = 1;
		i++;
		dis--;
		for (; i < length; i++) {
			number *= dis;
			dis --;
			
		}
		
		return number;
	}
}
```

this time, it is still a failure, because the code does not take into the account of the overflow when the numbers are greater.

So my last attempt is 

```
import java.math.BigInteger;
import java.util.Scanner;

public class Main {

	public static void main(String[] args) {
		
		Scanner scanner = new Scanner(System.in);
		
		int length = 0;
		String code = "";
		
		while ((length = scanner.nextInt()) != 0) { 
			scanner.nextLine();
			code = scanner.nextLine();
			// int number = 0;
			BigInteger number = new BigInteger(new byte[] { 0 });
			char[] chars = new char[26];
			for (int i = 0; i < 26; i++) {
				chars[i] = 0;
			}
			
			for (int i = 0; i < length; i++) {
				char base = 'A';
				boolean foundBase = false;
				int biggerThanBase= 0;
				for (int j = 0; j < 26; j++) { 
					if (chars[j] == 0) {
						if (!foundBase) {
							base += j;
							foundBase = true;
							continue;	
						}
					} else if (chars[j] == 1) {
						if (foundBase) {
							if (j+ 'A' < code.charAt(i)) {
								biggerThanBase++;	
							}
						}
					}
				}
				
				number = number.add( new BigInteger(new byte[]  {(byte)(code.charAt(i) - base - biggerThanBase)}).multiply(pow(i, length)));
				chars[code.charAt(i) - 'A'] = 1;
			}
			System.out.println(number);
		}
	}
	
	public static BigInteger pow(int i, int length) {
		int dis = 26 - i;
		BigInteger number = new BigInteger(new byte[] {1});
		i++;
		dis--;
		for (; i < length; i++) {
			number = number.multiply(new BigInteger(new byte[] { (byte) dis }));
			dis --;
		}
		
		return number;
	}
}
```

## Reverse bits discussion

with a normal xor (you can do other ways - like check each and every of the bit then OR or AND to set or clear on bit in the number).

the code is as such 

```
	/* since the limitation of java platform, we will use long 's lowest 32 bits to represent the unsigned value */
	public static long swapBits(long x, int i, int j) {
		
		long lo = ((x >> i) & 1);
		long hi = ((x >> j) & 1);
		if ((lo ^ hi) != 0) { 
			x ^= ((1 << i) | (1 << j));
		}
		
		return x;
	}
	
	public static long reverseXor(long x) { 
		
		// long n = sizeof(int) * 8;  /* in java, there is no size of operator */
		int n = Integer.SIZE;
		for (int i = 0; i < n/2; i++) {
			x = swapBits(x, i, 32 - i - 1);
		}
		return x;
	}
```

this given the 32-bit length integer, which requires at least 16 operations to complete the task.

there are more tricks to the problem mentioned above. For one, there is a solution that is inspired from the Merge Sort. 
```
/**
 * 
 * this uses a merge type of trick to reverse the order of bits.
 * 
 * 
 * 				87654321
 * 			/				\
 * 		4321			    8765
 * 		/						\
 *    2143						6587
 * 	  /							  \
 *  1234						  5678
 * 
 * @param x the mask that to reverse the orders. 
 * @return
 */
public static long reverseMask(long x) { 
	x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1); 
	x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2);
	x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4);
	x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8);
	x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16);
	return x;
}
```

> The first step is to swap all odd and even bits. After that swap consecutive pairs of bits, and so on…

this is just an introduction to some of quirk use of the bit operations.

see the [Bit Twiddling Hacks](http://graphics.stanford.edu/~seander/bithacks.html#BitReverseObvious) for more details.


References:
[Reverse Bits | LeetCode](http://leetcode.com/2011/08/reverse-bits.html)
[Bit Twiddling Hacks](http://graphics.stanford.edu/~seander/bithacks.html#BitReverseObvious)


## Insertion Sort

so much for the advanced s


## it is not just bubble sort


while this might be the first textbook of any computer student, here is the most simple bubble sort...


```
import sys


def bubble_bruteForce(a):
	length = len(a)
	for i in range(length):
		for j in range(length):
			if a[i] < a[j]:
				temp = a[i]
				a[i] = a[j]
				a[j] = temp

def printArray(a):
	for x in a:
		print x,
	print

if __name__ == "__main__":
	stock_prices = [5, 10, 12, 3, 8, 18, 1, 14]
	bubble_bruteForce(stock_prices)
	printArray(stock_prices)
```

this is so called bubble sort( brual force), and the complexity , no doubt woudl be n^2 and there is no argue on that.

A better (cut the complexity bu half) is to assume that when next ieration comes, the first half of the array is already sort. here it is

```
def bubble_bruteForce_cutHalf(a):
	length = len(a)
	for i in range(length):
		for j in range(i+1, length):
			if a[i] < a[j]:
				temp = a[i]
				a[i] = a[j]
				a[j] = temp
```

Also, it is possilbe that you just bubbles adjoining elements. so that you have this..

```
def bubble_rampDown(a):
	length = len(a)
	for i in range(length):
		for j in range(length-1, i, -1):
			if a[j] < a[j-1]:
				temp = a[j]
				a[j] = a[j-1]
				a[j-1] = temp

```

the rationale behind this is that in each pass, the smallest/biggest value will moved to the tail/head in relay.  Notice that the inner loop goes the opposite direction as the outter loop(think of why :)))

as advised, there is a rampUp down version, then there would be a rampDown version, followed by the ramp down version.

```
def bubble_rampUp(a):
	length = len(a)
	for i in range(length-1, -1,-1):
		for j in range(0, i):
			if a[j] > a[j+1]:
				temp = a[j]
				a[j] = a[j+1]
				a[j+1] = temp

```

then you may wonder do we have to do the iteration in exactly the dec/inc order, the answer is no. Here is the example.

```
def bubble_rampUp_highToLowIter(a):
	length = len(a)
	for i in range(length-1, -1,-1):
		for j in range(i-1, -1, -1):
			if a[j] > a[j+1]:
				temp = a[j]
				a[j] = a[j+1]
				a[j+1] = temp

```


## kth elements from two sorted arrays

well, the most intuitive way is to do with the merge way, here is the code 

```
	private int[] merge(int[] a, int[] b) {
		int[] c = new int[a.length + b.length];	
		for (int i = 0, j = 0, k = 0; i < a.length && j < b.length;) {
			if (a[i] < b[j]) {
				c[k++] = a[i++];
			} else {
				c[k++] = b[j++];
			}
			
			if (i == a.length) {
				for (;j < b.length; j++) {
					c[k++] = b[j++];
				}
			}
			
			if (j == b.length) { 
				for (;i < a.length; i++) { 
					c[k++] = a[i++];
				}
			}
		}
		
		return c;
	}

```

well, it requires extra spaces and that is causing O(m+n) complexity.

Another but better way is to use the in-place kind of merge,w here it does not do all the way merge, so the complexity is reduced to O(k).

```

	private int kthElement(int[] a, int[] b, int k) { 
		for (int i = 0, j = 0, p = 0; i < a.length && j < b.length && p <= k;) {
			if (p == k) {
				if (a[i] < b[j]) {
					return a[i];
				} else {
					return b[j];
				}
			}
			
			if (a[i] < b[j]) {
				i++;
				p++;
			} else { 
				j++;
				p++;
			}
		}
		
		return 0; // beter return some pre-defiend values.
	}
```


Yet, we can do the optimized way, given the references has already convereted the principles, here is the code with explaination.

```
	/**
	 * find the kth elemnt from two sorted array, a and b.
	 * @param a the a array
	 * @param b the b array
	 * @param m the index to look at array a
	 * @param n the index to look at array b
	 * @param k the number k
	 * @return the number if found
	 * 
	 * for the following discussion, we are assuming the arrays are sorted in decreasing order.
	 * 
	 * the core of the algorithm is to keep the following invariance
	 * 
	 *  i + j = k - 1
	 * 
	 *  If Bj-1 < Ai < Bj, then Ai must be the k-th smallest,
	 *  or else if Ai-1 < Bj < Ai, then Bj must be the k-th smallest.
	 * 
	 * given i + j == k - 1, if we cannot find Ai or Bj that meet the condition, we will divide the arrays to seek when the conditions are meet.
	 * 
	 * The key problem is how to divide the arrays?
	 * 
	 *  when Ai < Bj-1, we can safely discard lower bound of a of size i, and the upper bound of array b (size n - j : well we don't really care about the upper bound).
	 *  when Bj < Ai-1, we can safely discard lower bound of b of size j, and the upper bound of array a (size m - i : well we don't really care about the upper bound).
	 *  
	 *  Given all this, we can come up with some code.
	 *  
	 *  For two sorted array in increasing order, we can apply similar solution.
	 */
	private int kthElement(int[] a, int[] b, int m, int n, int aoff, int boff, int k) {
		int i = (int)((double)m  * (k - 1) / (m + n));
		int j = k - 1 -i;
		
		assert(i >= 0);
		assert(j >= 0);
		assert(i <= m);
		assert(j <= n);
		
		int Ai_1 = ((i + aoff == 0) ? INT_MIN : a[i + aoff - 1]);
		int Bj_1 = ((j + boff == 0) ? INT_MIN : b[j + boff - 1]);
		int Ai =  ((i + aoff == m) ? INT_MAX : a[i + aoff]);
		int Bj = ((j + boff == n) ? INT_MAX : b[j + boff]);
		
		
		if (Bj_1 < Ai && Ai < Bj) {
			return Ai;
		} else if (Ai_1 < Bj && Bj < Ai) {
			return Bj;
		}
		
		assert((Ai > Bj && Ai_1 > Bj) || 
		         (Ai < Bj && Ai < Bj_1));
		
		// if none of hte cases above, then it is either 
		
		if (Ai < Bj) {
			// exclude Ai and below portion
		    // exclude Bj and above portion
			return kthElement(a, b, m - i - 1, j, aoff + i, boff,  k - i - 1);
		} else {
			// exclude Ai and above portion
		    // exclude Bj and below portion
			return kthElement(a, b, k - j - 1, n - j - 1, aoff, boff + j,  k - j - 1);
		}
	}

```

I have come up with a iterative way, well, it is similar to the solution above but it always divide from the middle.

```
	/**
	 * find the kth element from two sorted array.
	 * @param a the input array a
	 * @param b the input array b
	 * @param k the k
	 * @param m index of a under check
	 * @param n index of b under check
	 * @return the kth value of union of a and b
	 */
	private int kthElement(int[] a, int[] b, int k, int m, int n) {
		int mlow = 0, nlow = 0, mhigh = a.length, nhigh = b.length;
		
		while (m + n != k - 1) {
			if (m + n > k - 1) { 
				if (a[m] > b[n]) {
					if (mlow != m) { // pre-check before infinite loop.
						int temp = m;
						m = (mlow + m) / 2;
						mhigh = temp;	
					} else {
						int temp = n;
						n = (nlow + m) / 2;
						nhigh = temp;
					}
					
				} else {
					if (nlow != n) {
						int temp = n; 
						n = (nlow + n) / 2;
						nhigh = temp;
					} else {
						int temp = m;
						m = (mlow + m) / 2;
						mhigh = temp;
					}
				}
			} else if (m + n < k - 1) {
				if (a[m] > b[n]) { 
					if (nhigh != n) { 
						int temp = n;
						n = (n + nhigh + 1) / 2;
						nlow = temp;
					} else {
						int temp = m;
						m = (m + mhigh + 1) / 2;
						mlow = temp;	
					}
					
				} else {
					if (mhigh != m) {
						int temp = m;
						m = (m + mhigh + 1) / 2; // the reason for '+1' is when moving upward, 
						mlow = temp;	
					} else 
					{
						int temp = n;
						n = (n + nhigh + 1) / 2;
						nlow = temp;
					}
				}
			}
			
		} 
		
		return a[m] < b[n] ? a[m] : b[n];
	}
```

For the above code, more test and proof taking is required.
References:


[Find the k-th Smallest Element in the Union of
 Two Sorted Arrays | LeetCode](http://leetcode.com/2011/01/find-k-th-smallest-element-in-union-of.html)


## Cornfields and the states compression algorithms

well, the original problem is here:　[CornFields](http://poj.org/problem?id=3254)

there is a references solution which is posted here: [状态压缩dp入门 （poj3254 Corn Fields） - 大神养成中..... - 博客频道 - CSDN.NET](http://blog.csdn.net/y990041769/article/details/24658419)

well, my solution based on the discussion is available here.

```
package states.compression;

import java.util.Scanner;

public class CowPlants_StatesCompression_Handwritting {

	static final int N = 13;
	static final int M = 1 << N;
	static final int[] st = new int[M];
	static final int[] map = new int[N];
	static final int[][] dp = new int[N][M];
	static final int mod = 100000000;

	
	public static void main(String[] args) {
		
		Scanner in = new Scanner(System.in);
		while (in.hasNext()) {
			int n = in.nextInt();
			int m = in.nextInt();
			
			for (int i = 0; i < st.length; i++) { 
				st[i] = 0;
			}
			
			for (int i = 0; i < map.length; i++) { 
				map[i] = 0;
			}
			
			for (int i = 0; i < dp.length; i++) { 
				for (int j = 0; j < dp[i].length; j++) {
					dp[i][j] = 0;
				}
			}
			
			// build map
			for (int i = 1; i <= n; i++ ) {
				for (int j = 1; j <= m; j++) {
					int x = in.nextInt();
					if (x == 0) {
						map[i] += (1 << (j -1 ));
					}
				}
			}
			
			int k = 0;
			// build states
			for (int i = 0; i < (1<<m); i++) {
				if (!judge1(i)) {
					st[k++] = i;
				}
			}
			
			for (int i = 0; i < k; i++) {
				if (!judge2(1, i)) 
					dp[1][i] = 1;
			}
			
			// d-p solving the problems.
			for (int i = 2; i <= n; i++) {
				for (int j = 0; j < k; j++) {
					if (judge2(i, j)) {
						continue;
					}
					
					for (int f = 0; f < k; f++) {
						if (judge2(i-1, f)) {
							continue;
						}
						
						if ((st[f] & st[j]) == 0) {
							dp[i][j] += dp[i-1][f];
						}
					}
				}
			}
			
			int ans = 0;
			for (int i = 0; i < k; i++) {
				ans += dp[n][i];
				ans = ans % mod;
			}
			System.out.println("" + ans);
		}
	}
	
	public static boolean judge1(int x) { 
		return (x & (x << 1)) != 0;
	}
	
	public static boolean judge2(int i, int k) { 
		return (map[i] & st[k]) != 0;
	}
}

```
