## introduction 
this page will introduce some of the operations that invovles the binary search tree. 

## the binary search tree operation impl
well, the binary search tree is a very common used data-structure that we'd like to visit the implementation of this code.
here is the code written in java.

```
package tree.binarysearchtree;

import static java.lang.System.out;

public class BinarySearchTreeExample {
	public static void main(String[] args) { 
		BinarySearchTreeExample example = new BinarySearchTreeExample();
		Tree x = example.new Tree();
		x.key = 7;
		
		example.insert(x);
		x = example.new Tree();
		x.key = 4;
		example.insert(x);
		
		x = example.new Tree();
		x.key = 3;
		example.insert(x);
		
		x = example.new Tree();
		x.key = 13;
		example.insert(x);;
		
		
		x = example.new Tree();
		x.key = 9;
		example.insert(x);
		
		x = example.new Tree();
		x.key = 10;
		example.insert(x);
		
		Tree min = example.minimum(example.root);
		
		Tree max = example.maximum(example.root);
		
		out.println("min " + min.key);
		out.println("max " + max.key);
		
		Tree pred = example.predecessor(max);
		Tree succ = example.successor(min);
		
		out.println("min succ " + succ.key);
		out.println("max pred " + pred.key);
		
		
		example.delete(max);
		max = example.maximum(example.root);
		pred = example.predecessor(max);
		
		out.println("after deleteion, max " + max.key);
		out.println("after deletion, min " + pred.key);
	}
	
	class Tree { 
		int key;
		Tree left;
		Tree right;
		Tree parent;
	}
	
	
	Tree root = null;
	
	/** minimum
	 * 
	 * find the minimum of a node
	 * @param node
	 * @return minimum node found or null
	 * 
	 * you can assume that param node cannot be null
	 */
	public Tree minimum(Tree node) {
		while (node != null && node.left != null)  {
			node = node.left;
		}
		
		return node;
	}
	
	public Tree maximum(Tree node) {
		while (node != null && node.right != null) { 
			node = node.right;
		}
		
		return node;
	}
	
	/** insertion,which shall support parent 
	 * 
	 * @param z node to insert 
	 * 
	 * well the insertion can be iterative or recursive.
	 * assumption: 1) z is not null.
	 */
	public void insert(Tree z) {
		Tree x = root;
		Tree y = null; // init value has to be right
		while (x != null) {
			y = x;
			if (x.key > z.key) { 
				x = x.left;
			} else { 
				x = x.right;
			}
		}
		
		z.parent = y; // set z.parent = y; avoid that when y == null, z.parent may have wrong value
		if (y == null) { 
			 root = z;
		} else { 
			if (z.key < y.key) {
				y.left = z;
			} else {
				y.right = z;
			}
		}
	}
	
	/**
	 *  search for a specific key in the tree rooted at node 
	 * 
	 * @param node the root node
	 * @param key the key to find
	 * */
	public Tree search(Tree node, int key) {
		while (node != null && node.key != key) {
			if (node.key > key) {
				node = node.left;
			} else { 
				node = node.right;
			}
		}
		
		return node;
	}
	
	/**
	 * search_recur - find a key recursively
	 * @param node
	 * @param key
	 * @return the found key
	 */
	public Tree search_recur(Tree node, int key) {
		if (node == null || node.key == key) return node;
		
		if (node.key > key) return search_recur(node.left, key);
		else return search_recur(node.right, key);
	}
	
	
	/** find the successor of the treenode.
	 * 
	 * @param node
	 * @return the successor of the node 
	 * 
	 * assumption that the pare
	 */
	public Tree successor(Tree node) {
		if (node.right != null) {
			return minimum(node.right);
		} else { 
			Tree p = node.parent;
			while (p != null && p.left != node) {
				node = p;
				p = p.parent;
			}
			
			return p;
		}
	}
	
	public Tree predecessor(Tree node) {
		if (node.left != null) {
			return maximum(node.left);
		} else { 
			Tree p = node.parent;
			while (p != null && p.right != node) { 
				node = p;
				p = p.parent;
			}
			
			return p;
		}
	}
	
	/** transplant: transplant one node to another
	 * 
	 * @param u transplanted root
	 * @param v new node.
	 */
	public void transplant(Tree u, Tree v) { 
		if (u.parent == null) {
			root = v;
		} else if (u == u.parent.left) { 
			u.parent.left = v;
		} else {
			u.parent.right = v;
		}
		
		if (v != null) {
			v.parent = u.parent;
		}
	}
	
	/** delete one node from the parent
	 * 
	 *  @param x node to delete
	 *  
	 *  the following variable names are used 
	 *  
	 *  x node to delete
	 *  z node which is the parent of x
	 *  y successor of x (which is the node that transplant x)
	 *  r in case y is not a direct child of z, what is the right child of x
	 *  */
	public void delete_joe_version(Tree x) {
		if (x.left == null) { 
			transplant(x,  x.right);
		} else if (x.right == null) { 
			transplant(x, x.left);
		} else { 
			// both left and right child are there.
			Tree y = minimum(x.right);
			if (y.parent != x) {
				// first transform, transplant y and its right child 
				transplant(y, y.right);
				// splice y to x (as the parent of 
				y.right = x.right;
				y.right.parent = y;
			}
			
			Tree r = x.right;
			transplant(x, x.right);
			y.left = x.left;
			y.left.parent = y;
		}
	}
	
	
	
	/** delete one node from the tree 
	 * this will use the variable name directly from the textbook
	 * 
	 * @param z node to delete
	 * 
	 * where the variable name and its graph is here 
	 * 
	 * z node to delete
	 * x right child of y
	 * y the successor of z
	 * l left child 
	 * r right child/right child of z for case 4) which shall becom the right child of y
	 * q the common root
	 * 
	 * 
	 * 1)
	 *     q
	 *    / \ 
	 *   l   NIL
	 *       
	 * 2)
	 *     q
	 *    /   \
	 *  NIL    r
	 * 
	 * 
	 * 3) 
	 * 
	 *      z
	 *    /    \
	 *   l       y
	 *         /  \
	 *        NIL  x
	 *  
	 * 4) 
	 * 
	 *      z
	 *    /    \
	 *   l      r
	 *         /  \
	 *        y   ...
	 *          \
	 *           x
	 *   the above shall become 
	 *   
	 *      z
	 *    /    \
	 *   l     ...
	 *   
	 *   and 
	 *        y
	 *         \
	 *          r
	 *         / \
	 *        x   ...
	 *          \
	 *           ..
	 *  then turns to 3)  
	 *           
	 */ 
	 
	 public void delete(Tree z) {
		 if (z.left == null) {
			 transplant(z, z.right);
		 } else if (z.right == null) {
			 transplant(z, z.left);
		 } else {
			 Tree y = minimum(z);
			 if (y.parent != z) { 
				 // transform
				 transplant(y, y.right);
				 y.right = z.right;
				 y.right.parent = y;
			 }
			 
			 // splice case 3) 
			 transplant(z, y);
			 y.left = z.left;
			 y.left.parent = y;
		 }
	 }
	 
	 
	 /** delete_cihld_pred
	  * 
	  * @param z: the node to delete 
	  * 
	  * this is a symmetry version to above 'delete' where it find the child predecessor rather than child_successor.
	  * 
	  * variable names to use 
	  * z node to delete
	 * x left child of y
	 * y the predecessor of z
	 * r right child 
	 * l left child/right child of z for case 4) which shall become the left child of y
	 * q the common root
	 * 
	 * 
	 * 
	 * 	  3) 
	 * 
	 *      z
	 *     /  \
	 *    y    r
	 *   /  \       
	 *  x   NIL  
	 *  
	 * 4) 
	 * 
	 *      z
	 *     /  \
	 *    l    r
	 *   /  \       
	 *       y  
	 *      /
	 *    x
	 *   
	 *   the above shall become 
	 *   
	 *      z
	 *    /    \
	 *   l     ...
	 *   
	 *   and 
	 *        
	 *         y
	 *       /  \ 
	 *      l   NIL
	 *    /  \
	 *   ...  x
	 *     
	 *       
	 *  then turns to 3)  
	  */
	  public void delete_child_pred(Tree z) { 
		  if (z.left == null) {
			  transplant(z,  z.right);
		  } else if (z.right == null) { 
			  transplant(z, z.left);
		  } else { 
			  // find the predecessor
			  Tree y = maximum(z.left);
			  if (y.parent != z) { // casae 4)
				  transplant(y, y.left);
				  y.left = z.left;
				  y.left.parent = y;
			  } 
			  
			  // now case 3)
			  transplant(z, y);
			  y.right = z.right;
			  y.right.parent = y;
		  }
	  }
}

```


## in-order preorder issue

given an in-order sequence and a pre-order sequence, found the post-order sequence.

```
package tree.binarysearchtree;

/** the problem is based on two list given by the traversal methods, one is pre-order and the other is in-order, given the two tree, 
 * find out the orginal tree is by printing out the post-order visit result
 *
 */
public class InorderPreorderTree {

	/* there is a link to an existing soluiton */
	public static void main(String[] args) {
		String inorder = "DBEAFC";
		String preorder = "ABDECF";
		
		InorderPreorderTree tree = new InorderPreorderTree();
		TreeNode root = tree.solution(preorder, inorder);
		
		StringBuilder sb = new StringBuilder();
		tree.postorder(root, sb);
		
		System.out.println("post order " + sb.toString());
		
	}
	
	class TreeNode
	{
		TreeNode left;
		TreeNode right;
		char key;
	}
	
	
	public TreeNode solution(String preorder, String inorder) {
		
		if (!"".equals(preorder)) {
			char root = preorder.charAt(0);
			TreeNode p = new TreeNode();
			p.key = root;
			int index = inorder.indexOf(root); // you can change to use the .split method.
			String left = inorder.substring(0, index);
			String right = inorder.substring(index + 1);
			p.left = solution(preorder.substring(1, left.length()+1), left);
			p.right = solution(preorder.substring(1+left.length()), right);
			
			return p;
		}
		
		return null;
	}
	
	public void postorder(TreeNode tree, StringBuilder sb) {
		if (tree != null) {
			postorder(tree.left, sb);
			postorder(tree.right, sb);
			sb.append(tree.key);
		}
	}
}

```
well, the solution can be implemented this way.


```
	public TreeNode solution(String preOrder, String inOrder) {
		
		if (!preOrder.isEmpty()) {
			String[] subTrees = inOrder.split(Character.toString(preOrder.charAt(0)));
			String left = subTrees.length > 0 ? subTrees[0] : ""; 
			String right = subTrees.length > 1 ? subTrees[1] : "";
			
			TreeNode root = new TreeNode();
			root.key = preOrder.charAt(0);
			root.left = solution(preOrder.substring(1, left.length()+1), left);
			root.right = solution(preOrder.substring(left.length()+1), right);
			
			return root;
		}
		
		return null;
		
	}
```
