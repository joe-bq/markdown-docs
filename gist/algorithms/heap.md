## introduction 
this page contains the implementation of the heap algorithm

## code

```
package heap;

import java.lang.*;
import static java.lang.System.*;

public class HeapExample {
	public static void main(String[] args) {
		// below we will use some example to test our applications.
		int[] heap = new int[] { 2, 4, 49, 8, 3, 10, 20, 53 };
		
		HeapExample heapExample = new HeapExample(heap.length);
		out.println(" before build heap: ");
		heapExample.print_heap(heap);
		heapExample.build_heap(heap);
		out.println(" after build heap: ");
		heapExample.print_heap(heap);
		
		heap = new int[] { 2, 4, 49, 8, 3, 10, 20, 53 };
		heapExample.heap_sort(heap);
		out.println(" after heap sort");
		heapExample.print_heap(heap);
	}
	
	private void print_heap(int[] heap) { 
		for (int i = 0; i < heap.length; i++) {
			System.out.print("" + heap[i] + " ");
		}
		
		System.out.println();
	}
	
	/* fields */
	private int length;
	
	public HeapExample(int length) {
		this.length = length;
	}
	
	public int left(int i) {
		return i * 2;
	}
	
	public int right(int i) {
		return i * 2 + 1;
	}
	
	public int parent(int i) {
		return i / 2;
	}
	
	public void max_heapify(int[] heap, int i) throws UnsupportedOperationException {
		if (i < this.length && i >= 0) {
			int left = left(i);
			int right = right(i);
			int largest = heap[i];
			int r = i;
			if (left < this.length && heap[left] > largest) {
				largest = heap[left];
				r = left;
			}
			if (right < this.length && heap[right] > largest) {
				largest = heap[right];
				r = right;
			}
			
			if (r != i) {
				int temp = heap[i];
				heap[i] = heap[r];
				heap[r] = temp;
				
				max_heapify(heap, r);
			}
		}
	}
	
	/**
	 * shift down the element at param i for the heap param heap.
	 * @param heap
	 * @param i
	 * 
	 * <p>shift down maintains the invariance of heap so that when you are building the heaps you can establish the heap invariance.</p>
	 */
	public void shift_down(int[] heap, int i) { 
		if (i < this.length && i >= 0) {
			int left = left(i);
			int right = right(i);
			int largest = heap[i];
			int r = i;
			if (left < this.length && heap[left] > largest) {
				largest = heap[left];
				r = left;
			}
			if (right < this.length && heap[right] > largest) {
				largest = heap[right];
				r = right;
			}
			
			if (r != i) {
				int temp = heap[i];
				heap[i] = heap[r];
				heap[r] = temp;
				
				max_heapify(heap, r);
			}
		}
	}
	
	/** 
	 * shift up the element at param i for the heap param heap
	 * @param heap
	 * @param i
	 * 
	 * <p>shit up maintain the invariance of heap so that when you insert or increase key of a certain element, the element can be shift up the tree hierarchy so that 
	 * the heap invariance can be maintained.</p>
	 */
	public void shift_up(int[] heap, int i) {
		while (i < this.length && i >= 0) {
			int parent = parent(i);
			if (heap[parent] < heap[i]) {
				int temp = heap[parent];
				heap[parent] = heap[i];
				heap[i] = temp;
				i = parent;
			}
		}
	}
	
	public void heap_sort(int[] heap) {
		// assert that the heap has been sorted
		build_heap(heap);
		
		while (this.length > 0) {
			int temp = heap[this.length - 1];
			heap[this.length - 1] = heap[0];
			heap[0] = temp;
			this.length--;
			max_heapify(heap, 0);
		}
	}
	
	public void build_heap(int[] heap) throws UnsupportedOperationException {
		for (int i = this.length; i >= 0; i--) {
			max_heapify(heap, i);
		}
	}
	
	public int heap_maximum(int[] heap) throws UnsupportedOperationException {
		if (this.length < 0) {
			throw new UnsupportedOperationException();
		}

		return heap[0];
		
	}
	
	public void heap_increase_key(int[] heap, int i, int key) {
		if (i < this.length && i >= 0) { 
			heap[i] = key;
			shift_up(heap, i);
		}
	}
	
	public void heap_insert(int[] heap, int key) {
		// TODO:
		// check if length overflow.
		heap[this.length] = Integer.MIN_VALUE;
		this.length++;
		heap_increase_key(heap, this.length, key);
	}
	
	public int heap_extract_maximum(int[] heap) throws UnsupportedOperationException {
		if (this.length < 0) {
			throw new UnsupportedOperationException();
		}
		
		int max = heap[0];
		int temp = heap[this.length - 1];
		heap[this.length - 1] = heap[0];
		heap[0] = temp;
		this.length--;
		max_heapify(heap, 0);
		
		return max;
	}
}
```
