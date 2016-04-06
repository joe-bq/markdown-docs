## introduction

this page will show you the implementation of count sort, the count sort is a stable sort algorithm..


## Code 

the following code are my implementation of count sort.

```
package countsort;

import static java.lang.System.out;

public class CountSortExample {
	public static void main(String[] args) {
		int[] data = new int[] { 2, 5, 3, 0, 2, 3, 0, 3};
		CountSortExample example = new CountSortExample();
		example.countsort(data);
		example.print_data(data);
	}
	
	public void countsort(int[] data) {
		int max = data[0];
		for (int i : data) {
			if (i > max) { 
				max = i;
			}
		}
		
		int[] count = new int[max+1];
		
		for (int i = 0; i < count.length; i++) {
			count[i] = 0;
		}
		
		for (int i : data) { 
			count[i]++;
		}
		
		for (int i = 1; i < count.length; i++) {
			count[i] += count[i-1];
		}
	
		int[] copy = new int[data.length];
		// we will iterate downward so that we can maintain a stable sort
		for (int i = data.length-1; i >= 0; i--) {
			copy[count[data[i]]-1] = data[i];
			count[data[i]]--;
		}
		
		for (int i = 0; i < data.length; i++) {
			data[i] = copy[i];
		}
	}
	
	private void print_data(int[] data) {
		for (int i : data) {
			out.print("" + i + " ");
		}
		
		out.println();
		
	}
}

```
