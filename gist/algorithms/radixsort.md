## Introduction
this page will introduce you the radix sort and how it shall be implemented.

## code 

please see the following code on how the radix sort is implemented.

this is a more C-Style implementation. where the data are copied and... 

```
package radixsort;

import static java.lang.System.out;

public class RadixSortExample {
	public static void main(String[] args) {
		int[] data = new int[] { 323, 145, 773, 281, 127, 422, 369 };
		
		RadixSortExample example = new RadixSortExample();
		example.radixsort(data);
		
		example.print_data(data);
	}
	
	private void print_data(int[] data) {
		for (int i: data) {
			out.print("" + i + " ");
		}
		
		out.println();
	}
	
	/* NOTE: THIS IS A MORE C-STYLE IMPLEMENTATION, BUT WHICH IS QUIT PERFORMANT */
	public void radixsort(int[] data) {
		int base = 10;
		int exp = 1;
		
		int max = data[0];
		for (int i : data) {
			if (i > max) {
				max = i;
			}
		}
		
		// internally we will use the count sort (a stable sort to sort by each digit)
		
		int[] w = new int[data.length];
		
		for (int i = 0; i < data.length; i++) {
			w[i] = data[i];
		}
		
		int[] count = new int[base];
		for (int i = 0; i < base; i++) {
			count[i] = 0;
		}
		
		int[] w2 = new int[data.length];
		
		while (exp < max) {
			for (int i = 0; i < w.length; i++) {
				count[w[i] % base]++;
			}
			
			for (int i = 1; i < count.length; i++) {
				count[i] += count[i-1]; 
			}

			// copy w2 to w1
			for (int i = data.length-1; i >= 0; i--) {
				w2[count[w[i] % base]-1] = data[i];
				count[w[i] % base]--;
			}
			
			for (int i = 0; i < data.length; i++) {
				data[i] = w2[i];
			}
			
			exp *= base;
			
			for (int i = 0; i < data.length; i++) {
				w[i] = data[i] / exp;
			}
			
			for (int i = 0; i < count.length; i++) {
				count[i] = 0;
			}
		}
	}
	
}


```

Please pay attention to the initial value of exp (it shall be 1 and when you try to update the w[i] at the end of each iteration, don't forget to advance its value)

You can also leverage the Java utils, the following are a more Java stle implementation.

```
package radixsort;

import static java.lang.System.out;

import java.util.ArrayList;

public class RadixSortJavaStyleExample {

	/* THIS EXAMPLE WILL SHOW RADIX SORT IN MORE JAVA LIKE STYLE AND WITH INSERSION SORT.. */
	public static void main(String[] args) {
		int[] data = new int[] { 323, 145, 773, 281, 127, 422, 369 };
		
		RadixSortJavaStyleExample example = new RadixSortJavaStyleExample();
		example.radixsort(data);
		
		example.print_data(data);
	}
	
	private void print_data(int[] data) {
		for (int i: data) {
			out.print("" + i + " ");
		}
		
		out.println();
	}
	
	public void radixsort(int[] data) {
		int base = 10;
		ArrayList<ArrayList<Integer>> w = new ArrayList<ArrayList<Integer>>(base); // though we have created ArrayList<ArrayList<Integer>(base) and reserved the space, 
																				   // but it does not mean we have already have the element ready!
		
		for (int i = 0; i < base; i++) {
			w.add(new ArrayList<Integer>());
		}
		
		for (int i = 0; i < w.size(); i++) {
			w.get(i).clear();
		}
		
		int exp = 1;
		int max = data[0];
		for (int i = 1; i < data.length; i++) {
			if (data[i] > max) { 
				max = data[i];
			}
		}
		
		while (max > exp) {
			for (int i = 0; i < data.length; i++) {
				w.get((data[i] / exp) % base).add(data[i]);
			}
			
			int j = 0;
			for (ArrayList<Integer> l : w) {
				for (int k : l) {
					data[j++] = k;
				}
			}
			
			for (ArrayList<Integer> l : w) {
				l.clear();
			}
			
			exp *= base;
		}
	}
	
}

```
