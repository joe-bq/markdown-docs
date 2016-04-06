## introduction

this page will introduce you the doubly linked list and some of the implementation with 

* sentinel
* w/ sentinel


## code 

the following shows the code

```
package doublylinklist;

import static java.lang.System.out;


/** This example composes of two examples which shows 
 * 1. the List operation (search, delete, insert_head, insert_end) when there is no sentinel
 * 2. the List operation (search, delete, insert_head, insert_end) when there is a sentinel
 */
public class DoublyLinkedListExample {

	/* For all our discussion, we are dealing with list which does not circle */
	public static void main(String[] args) {
		DoublyLinkedListExample example = new DoublyLinkedListExample();
		example.list_insert_end(3);
		example.list_insert_end(4);
		example.list_print();
		
		
		example = new DoublyLinkedListExample();
		example.list_insert_head_sentinel(3);
		example.list_insert_head_sentinel(4);
		example.list_print_sentinel();
	}
	
	public DoublyLinkedListExample() {
		Nil.next = Nil;
		Nil.prev = Nil;
	}
	
	/* NOTE: a NIL is a sentinels which simplifies the insertion/searching/etc in the doubly linked list */
	
	class List{
		/** next */
		List next;
		/** prev */
		List prev;
		/** key - where the key can have satellite data along with it */
		int key; 
	}
	
	/** sentinel - nil */
	List Nil = new List();
	
	
	List head = null;
	
	void list_print() {
		List list = head;
		while (list != null) {
			out.print("" + list.key + " ");
			list = list.next;
		}
		out.println();
	}
	
	/** non-sentinel sets */
	List list_search(int key) {
		
		List list = head;
		while (list != null && list.key != key) {
			list = list.next;
		}
		
		return list;
	}
	
	
	/** insert_head: key */
	List list_insert_head(int key) {
		List x = new List();
		x.key = key;
		return list_insert_head(x);
	}
	
	/** insert_head */
	List list_insert_head(List x) {
		
		x.next = head;
		if (head != null) {
			head.prev = x;
		}
		
		head = x;
		x.prev = null;
		
		return x;
	}
	
	
	/** insert_end */
	List list_insert_end(List x) {
		List p = head;
		List q = p;
		
		while (q != null) {
			p = q;
			q = q.next;
		}
		
		q = x;
		q.prev = head;
		q.next = null;
		
		if (p == null) { 
			p = head = q;
		} else {
			p.next = q;
		}
		
		return p;
	}
	
	/** insert_end: why not insert_head, which shall be faster */ 
	List list_insert_end(int key) {
		List x = new List();
		x.key = key;
		
		return list_insert_end(x);
		
	}
	
	
	/** list_delete: delete a node from the list */
	List list_delete(List x) {
		if (x.prev != null) {
			x.prev.next = x.next;
		} else { 
			head = x.next;
		}
		
		if (x.next != null) { 
			x.next.prev = x.prev;
		}
		
		return x;
	}
	
	/** sentinel sets */
	
	/* the key difference, for one is that given the sentinel there is no need to keep the head field. we can treat NIL as the pointer to head */
	
	/** list_search_sentinel: search for a key from the list with the */
	List list_search_sentinel(int key) {
		List x = Nil.next; // Given that if we have a sentinel, there is no need to go starting from the 
		
		while (x != Nil && x.key != key) {
			x = x.next;
		}
		
		return x;
	}
	
	List list_delete_sentinel(List x)  {
		// well the deletion can be much simpler if we have the sentinel 
		// there is no need to check for the boundary condition
		x.prev.next = x.next;
		x.next.prev = x.prev;
		
		return x;
	}
	
	
	List list_insert_head_sentinel(List x) {
		// 
//		x.next = Nil.next;
//		Nil.next.prev = x;
//		Nil.next = x;
//		x.prev = Nil;
		
		x.next = Nil.next;
		x.prev = Nil;
		
		Nil.next.prev = x;
		Nil.next = x;
		return x;
	}
	
	List list_insert_head_sentinel(int k) { 
		List x = new List();
		x.key = k;
		
		return list_insert_head_sentinel(x);
	}
	
	
	List list_insert_end_sentinel(List x) {
		
		x.prev = Nil.prev;
		x.next = Nil;
		
		Nil.prev.next = x;
		Nil.prev = x;
		return x;
	}
	
	
	List list_insert_end_sentinel(int k) {
		List x = new List();
		x.key = k;
		
		return list_insert_end_sentinel(x);
	}
	
	
	
	void list_print_sentinel() {
		List list = Nil.next;
		while (list != Nil) {
			out.print("" + list.key + " ");
			list = list.next;
		}
		out.println();
	}
}

```
