## introduction 
this page will show the principle and design of quick sort algorithm

## the code 


```
package quicksort;

import static java.lang.System.out;

public class QuickSortRightExample {
	public static void main(String[] args) { 
		QuickSortRightExample example = new QuickSortRightExample();
		
		int[] data = new int[] { 34, 21, 42, 7, 19, 69, 5 };
		out.println(" before quick sort, data:");
		example.print_data(data);
		example.quicksort(data, 0, data.length - 1);
		out.println(" after quick sort, data:");
		example.print_data(data);
		
		data = new int[] { 5, 69, 19, 7, 42, 21, 34 };
		
		out.println(" inversed data, before sort: ");
		example.print_data(data);
		out.println(" inversed data, after sort: ");
		example.quicksort(data, 0, data.length - 1);
		example.print_data(data);
	}
	
	private void print_data(int[] data) {
		for (int i = 0; i < data.length; i++) { 
			out.print("" + data[i] + " ");
		}
		
		out.println();
	}

	public int partition(int[] data, int r, int q) {
		int i = r;
		for (int j = i; j < q; j++) { 
			if (data[j] < data[q]) { // it is irrespective of whether we are using the data[j] > data[q];
				// swap i and j
				int temp = data[i];
				data[i] = data[j];
				data[j] = temp;
				i++; // advance the i to next.
			}
		}
		
		// swap i and q
		int temp = data[i];
		data[i] = data[q];
		data[q] = temp;

		return i;
	}
	
	public void quicksort(int[] data, int r, int q) {
		if (r < q) {
			int i = partition(data, r, q);
			quicksort(data, r, i - 1);
			quicksort(data, i + 1, q);
		}
	}

}
```


while you can as well count down from q down to r, here is the code ...

```
public class QuickSortDowntoEnumerate {
	public static void main(String[] args) {
		QuickSortDowntoEnumerate example = new QuickSortDowntoEnumerate();
		
		int[] data = new int[] { 34, 21, 42, 7, 19, 69, 5 };
		out.println(" before quick sort, data:");
		example.print_data(data);
		example.quicksort(data, 0, data.length - 1);
		out.println(" after quick sort, data:");
		example.print_data(data);
		
		data = new int[] { 5, 69, 19, 7, 42, 21, 34 };
		
		out.println(" inversed data, before sort: ");
		example.print_data(data);
		out.println(" inversed data, after sort: ");
		example.quicksort(data, 0, data.length - 1);
		example.print_data(data);
	}
	
	private void print_data(int[] data) {
		for (int i = 0; i < data.length; i++) { 
			out.print("" + data[i] + " ");
		}
		
		out.println();
	}
	
	public int partition(int[] data, int r, int q) {
		int i = q - 1;
		
		for (int j = i; j >= r; j--) {
			if (data[j] > data[q]) { 
				int temp = data[j];
				data[j] = data[i];
				data[i] = temp;
				i--;
			}
		}
		// swap against i+1 and q
		int temp = data[q];
		data[q] = data[i+1];
		data[i+1] = temp;
		
		return i + 1;
	}
	
	public void quicksort(int[] data, int r, int q) {
		if (r < q) {
			int i = partition(data, r, q);
			quicksort(data, r, i - 1);
			quicksort(data, i + 1, q);
		}
	}
}


```
