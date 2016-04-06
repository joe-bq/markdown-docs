## How to initialize hashset values by construction

Two ways that I have learned is 
1. Arrays.asList
2. new HashSet&lt;String&gt;() {{ add("a"); add("b"); }}

the second uses the so-called "anonymous initializer" - or what is so called "initialization block"
References
[java - How to initialize HashSet values by construction? - Stack Overflow](http://stackoverflow.com/questions/2041778/how-to-initialize-hashset-values-by-construction)
[java - Accessing constructor of an anonymous class - Stack Overflow](http://stackoverflow.com/questions/362424/accessing-constructor-of-an-anonymous-class)
[Initializing Fields (The Java™ Tutorials > Learning the Java Language > Classes and Objects)](http://docs.oracle.com/javase/tutorial/java/javaOO/initial.html)
[java - What is an initialization block? - Stack Overflow](http://stackoverflow.com/questions/3987428/what-is-an-initialization-block)

## java assertion

first let 's see an example 
```
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
```
in the above code, the assumption is that there would be exact 255 counts of instructions and each instruction is a single digit of hexadecimal number.

normally the assumption will hold true, and you won't do the unnecessary test in your code everywhere, but you want to state that the presumption is holding there.  then you can add the assertion.

Interesting the assertion here is not a function, but rather a keyword. that means the Java language has provided specifically a keyworwd to alllow you easy work with the assertion.


References
[Java Practices -> Assert use cases](http://www.javapractices.com/topic/TopicAction.do?Id=102)
[Programming With Assertions](http://docs.oracle.com/javase/7/docs/technotes/guides/language/assert.html)


## Java use BufferedReader to read from string
while the Java's pattern on the reader is a very good example on the use of the decorator pattern, to enable unified interfaces (like reading from a stream such as socket, console inputs) as well as reading from in-memory bytes such as internal structure of a java String instance. 

some of the most common cases is to read something from the string to simulate the input from a real Stream.

the key here is the String.getBytes then pass that bytes to the ByteArrayInputStream. 

here is an example from reference [How to convert String to InputStream in Java][How to convert String to InputStream in Java].


```
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
 
public class StringToInputStreamExample {
    public static void main(String[] args) throws IOException {
	String str = "This is a String ~ GoGoGo";
 
	// convert String into InputStream
	InputStream is = new ByteArrayInputStream(str.getBytes());
 
	// read it with BufferedReader
	BufferedReader br = new BufferedReader(new InputStreamReader(is));
 
	String line;
	while ((line = br.readLine()) != null) {
		System.out.println(line);
	}
 
	br.close();
   }
}
```

References
[How to convert String to InputStream in Java]:http://www.mkyong.com/java/how-to-convert-string-to-inputstream-in-java/
[How to convert String to InputStream in Java][How to convert String to InputStream in Java]


## Java does not have the unsigned keyword.
Java does not have the unsigned keyword

## Java does not have sizeof operator and alternative
java does not have the sizeof operator to get size of a primitive or structure (java does not have structure neither)'s size in byte (the bytes in all system are fixed to 8 bits length)

partly because that the Java platform has fixed length bits for all the primitive types.

However, the 

* Integer
* Long
* Float 
* ...

all have a .SIZE property... and it returns, please remember that it returns a length in "bits"

so 

`Integer.Size` returns 32.



## Java Integer Literals - Gotchas

I recently encounter one issue related to the integer's literal represenation. 

```
long bit1 = 0b10000000000000000000000000000000; // 
long bit2 = 0b10000000000000000000000000000000l;
```

the only diffrence is that bit1does not have the 'l' letter, and the other has. And I wrote the following util class to dump its contents.

```
	public static String dumpReverseLong(long x) { 
		StringBuffer buffer = new StringBuffer();
		
		int n = Long.SIZE;
		Stack<Character> stack = new Stack<Character>();
		for (int i = 0; i < n; i++) { 
			if ((x & 1) == 0) { 
				stack.push('0');
			} else { 
				stack.push('1');
			}
			x >>= 1;
		}
		
		while (!stack.empty()) {
			buffer.append(stack.pop());
		}
		
		return buffer.toString();
	}
```

Now, we dumped it and we get 

```
1111111111111111111111111111111110000000000000000000000000000000
0000000000000000000000000000000010000000000000000000000000000000
```

the first one is a negative number stored with "complement binary" representation. 

How this happens. the reason is that 	`0b10000000000000000000000000000000` is a integer with value -24xxx...xxx and when this is promotted to a long value, the negative sign is reserved.

So if you intended to store a literal as long, especially when it is crossing the boundary values, better suffix it with the ending 'l' or 'L'.

References:
[Primitive Data Types (The Java™ Tutorials > Learning the Java Language > Language Basics)](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html)


## Java tuples
well, if you are coming from the C# background, you may be familiar with the C# tuple constrauct, well, it is also possible that you can create your ownset of tuple with java programs.


```
class Tuple<X, Y>
{
   public final X x;
   public final Y y;
   public Tuple(X x ,Y, y) { 
      this.x = x;
      this.y = y;
   }

}

```


## Java/C#/Javascript/D allows labeled break and continues

well, in the languages mentioned above, there are a bunch of conditions that allows you to do labeled breaks and continues

the labeled breaks and continues has the following format.

```
outer: while(fn1())
{
   while(fn2())
   {
     if(fn3()) continue outer;
     if(fn4()) break outer;
   }
}
```