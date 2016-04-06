## introduction
this page will introduce you the algorithms of rb-tree


## code 
the code that does the rb-tree is as follow (as in java)

```
package tree.rbtree;

/** 
 * the red-black properties that holds 
 * 
 * 1. every node is either Red or Black
 * 2. The node is black
 * 3. Every leaf (Nil) is black
 * 4. if a node red, then both its children are black
 * 5. For each node, all simple from the node to descendant leaves contains the same number of black nodes.
 * @author Administrator
 *
 */
public class RbTreeExample {

	public static void main(String[] args) {
	}
	
	/** the color defined for red-black tree */
	enum Color {
		Black,
		Red
	}
	
	/* the tree structure for red-black tree */
	class Tree { 
		int key;
		Tree left;
		Tree right;
		Tree parent;
		Color color;
	}
	
	/** after insertion, fix up the color caused by the insertion
	 * 
	 * w: sibling to x
	 * x: the node which violate the r-b tree properties
	 * z: x' parent??
	 * */
	private void insert_fixup(Tree x) {
		
	}
	
	/** left-rotate 
	 * 
	 * left-rotate and right-rotate are the two basic operations that are supported by the r-b trees.
	 * 
	 * to visually demonstrate how the left/right-rotate works, here is the code 
	 * 
	 *         y                           left-rotate                      x
	 *      /    \                     <---------------                  /     \
	 *     x     gama                                                 alpha     y
	 *  /    \                             right-rotate                       /   \
	 * alpha  beta                     ---------------->                    beta   gama
	 * */
	private void left_rotate(Tree x) {
		Tree y = x.right;
		x.right = y.left;
		if (y.left != nil) { 
			y.left.parent = x;
		}
		
		y.parent = x.parent;
		if (x.parent != nil) { 
			if (x == x.parent.left) {
				x.parent.left = y;
			} else {
				x.parent.right = y;
			}
		} else {
			root = y;
		}
		
		y.left = x;
		x.parent = y;
	}
	
	
	/** 
	 * right-rotate
	 * 
	 * right-rotate rotate the rb-tree in such a way that the rb-tree properties still holds after the rotation.
	 * @param x
	 */
	private void right_rotate(Tree x) {
		Tree y = x.left;
		x.left = y.right;
		
		if (y.right != nil) { 
			y.right.parent = x;
		}
		
		y.parent = x.parent;
		
		if (x.parent != nil) {
			if (x.parent.left == x) {
				x.parent.left = y;
			} else {
				x.parent.right = y;
			}
		} else { 
			root = y;
		}
		
		y.right = x;
		x.parent = y;
	}
	
	
	/** the original implementation of the left-rotate */
	private void left_rotate_original(Tree x) {
		// we have to check if x == nil | null
		
		Tree y = x.right;
		x.right = y.left;
		
		if (y.left != nil) { 
			y.left.parent = x;
		}
		
		y.parent = x.parent;
		
		if (x.parent == nil) {
			root = y;
		} else if (x == x.parent.left) { 
			x.parent.left = y;
		} else if (x == x.parent.right) { 
			x.parent.right = y;
		}
		
		y.left = x;		
		x.parent = y;

	}
	
	
	/** the original implementation of right-rotate */
	private void right_rotate_original(Tree x) { 
		// we have to check if x == nil | null
		Tree y = x.left;
		x.left = y.right;
		
		if (y.right != nil){ 
			y.right.parent = x;
		}
		
		y.parent = x.parent;		
		if (x.parent == nil) { 
			root = y;
		} else if (x == x.parent.left){
			x.parent.left = y;
		} else if (x == x.parent.right){ 
			x.parent.right = y;
		}
		
		y.right = x;
		x.parent = y;
	}
	
	/** insert a tree into the tree
	 * 
	 *  variables:
	 *  
	 *  x: free variale, moving curosr
	 *  y: the parent of node to insert 
	 *  z: the node to insert 
	 *  */
	private void insert(Tree z) {
		
		Tree y = nil;
		Tree x = root;
		
		while (x != nil) {
			y =x;
			if (z.key < x.key) { 
				x = x.left;
			} else { 
				x = x.right;
			}
		}
		
		z.parent = y;
		if (y != nil) { 
			root = z;
		} else if (z.key < y.key) {
			y.left = z;
		} else {
			y.right = z;
		}
		
		z.left = nil;
		z.right = nil;
		z.color = Color.Red;
		
		rb_insertion_fixup(z);
	}
	
	
	/**
	 * r-b tree insertion fix-up . Fix up after insert a new node z into the tree
	 * 
	 * Precondition: 
	 * 
	 * before insertion, the z's node is colored RED
	 * 
	 * @param z
	 * 
	 * free variables: 
	 * 
	 * z: the node newly inserted
	 * y: node z's parent's sibling node 
	 * 
	 * there are three cases involved while case 2 can be transfered to case 3. and the whole case process is inside 
	 * an while loop which iteratively works upwards.
	 * 
	 * (a)                               b.11
	 *                     /                              \
	 *                  r.2                               b.14
	 *         /               \                               \
	 *        b.1              b.7                            r.15
	 *                       /    \       
	 *                     r.5     r.8(y)
	 *                     /
	 *                 (z)r.4
	 * 
	 * (b)                               b.11
	 *                     /                              \
	 *                  r.2                               b.14(y)
	 *         /               \                             \
	 *        b.1              r.7 (z)                      r.15
	 *                       /    \       
	 *                     b.5     b.8
	 *                     /
	 *                   r.4
	 *                 
	 * (c)                               b.11
	 *                     /                              \
	 *                  r.7                               b.14(y)
	 *         /               \                             \
	 *        b.2(z)           b.8                        r.15
	 *     /     \           
	 *   b.1     b.5 
	 *           / 
	 *          r.4 
	 *
	 * (d)                               b.7
	 *                     /                              \
	 *                  r.2                               r.11
	 *         /               \                        /       \
	 *        b.1              b.5                  b.8          b.14
	 *                      /                                      \
     *                    r.4                                      r.15
	 */
	private void rb_insertion_fixup(Tree z) {
		while (z.color == Color.Red) { // inside the while, we have violated 
			if (z.parent == z.parent.parent.left){ 
				Tree y = z.parent.parent.right;
				
				// violation of that Red node must have 
				if (y.color == Color.Red) {
					z.parent.color = Color.Black;
					y.color = Color.Black;
					// move the red color upwards to its parent's parent
					z.parent.parent.color = Color.Red;
					z = z.parent.parent;
				} else if (z == z.parent.right) {
					z = z.parent;
					left_rotate(z);
				}
				
				z.parent.color = Color.Black;
				z.parent.parent.color = Color.Red;
				right_rotate(z);
			} else {
				Tree y = z.parent.parent.left;
				
				if (y.color == Color.Red) {
					z.parent.color = Color.Black;
					y.color = Color.Black;
					
					z.parent.parent.color = Color.Red;
					z = z.parent.parent;
				} else if (z == z.parent.left) {
					z = z.parent;
					right_rotate(z);
				}
				
				z.parent.color = Color.Black;
				z.parent.parent.color = Color.Red;
				left_rotate(z);
			}
		}
		
		root.color = Color.Black;
	}
	
	/**
	 * r-b transplant.
	 * 
	 * slightly modified version of the transplant of balanced tree.
	 * 
	 * @param u
	 * @param v
	 */
	private void rb_transplant(Tree u, Tree v) {
		if (u.parent == nil) {
			root = v;
		} else if (u == u.parent.left) { 
			u.parent.left = v;
		} else {
			u.parent.right = v;
		}
		
		v.parent = u.parent;
	}
	
	/**
	 * 
	 * 	variables:
	 *  
	 *  x: free variable, moving cursor
	 *  y: the parent of node to insert 
	 *  z: the node to insert 
	 *  
	 * @param z
	 */
	private void rb_delete(Tree z) {
		Tree y = z;
		Tree x;
		Color y_original_color = y.color;
		
		if (z.left == nil) {
			x = z.right;
			rb_transplant(z, z.right);
		} else if (z.right == nil) {
			x = z.left;
			rb_transplant(z, z.left);
		} else {
			y = tree_minimum(z.right);
			y_original_color = y.color;
			x = y.right;
			if (y.parent == z) { 
				x.parent = y;
			} else {
				y.right = z.right;
				y.right.parent = y;
			}
			rb_transplant(z, y);
			y.left = z.left;
			
			y.left.parent = y;
			y.color = z.color;
		}
		
		if (y_original_color == Color.Black) {
			rb_delete_fixup(x);
		}
	}
	/**
	 * rb_delete_fixup
	 * 
	 * fix up rb-tree after deletion.
	 * 
	 * a)
     *                             b.B                                                                       b.D
	 *          /                                 \                                                /                          \
	 *         b.A (x)                             r.D (w)                  --->             r.B                               b.E
	 *     /      \                               /       \                              /         \                        /         \
	 *    alpha  beta                         b.C           b.E                     b.A            b.C                 epislon       omiga                    
	 *                                    /        \       /        \          /         \        /     \
	 *                                gama         theta  epislon   omiga    alpha      beta     gama   theta
	 * 
	 * b)
     *                             r.B                                                                       x.B (x)
	 *          /                                 \                                                /                          \
	 *         b.A (x)                             b.D (w)                  --->             r.A                               r.D
	 *     /      \                               /       \                              /         \                        /         \
	 *    alpha  beta                         b.C           b.E                     b.A            b.C                 epislon       omiga                    
	 *                                    /        \       /        \          /         \        /     \
	 *                                gama         theta  epislon   omiga    alpha      beta     gama   theta
	 * 
	 * c)
     *                             x.B (c)                                                                      x.B (c)
	 *          /                                 \                                                /                          \
	 *         b.A (x)                             b.D (w)                  --->             r.A                               b.C (new w)
	 *     /      \                               /       \                              /         \                        /         \
	 *    alpha  beta                         r.C           b.E                     alpha            beta                 gama       r.D                    
	 *                                    /        \       /        \                                                                   \
	 *                                gama         theta  epislon   omiga                                                               b.E
	 *                                                                                                                               /      \
	 *                                                                                                                           epsilon     omiga
	 *                                                                                                                            
	 *                                                                                                                            c)
     *                             x.B (c)                                                                      x.D (c)
	 *          /                                 \                                                /                          \
	 *         b.A (x)                             b.D (w)                  --->             b.B                               b.E 
	 *     /      \                               /       \                              /         \                        /         \
	 *    alpha  beta                         x.C (c')     r.E                         b.A           x.C(c')             epsilon      omiga                    
	 *                                    /        \       /        \                /   \          /   \                                 
	 *                                gama         theta  epislon   omiga         alpha  beta    gama  theta                                            
	 *                                                                                                                         
	 *                                                                                                                         
	 * @param x
	 */
	private void rb_delete_fixup(Tree x) {
		Tree w;
		while (x != root && x.color == Color.Black) { 
			if (x == x.parent.left) {
				w = x.parent.right;
				if (w.color == Color.Red) {
					w.color = Color.Black;
					w.parent.color = Color.Red;
					left_rotate(w.parent);
					w = x.parent.right;
				}
				
				if (w.left.color == Color.Black && w.right.color == Color.Black) {
					w.color = Color.Red;
					x = x.parent;
				} else	{
					if (w.right.color == Color.Black) {
						w.left.color = Color.Black;
						w.color = Color.Red;
						right_rotate(w);
						w = x.parent.right;
					}
					w.color = x.parent.color;
					x.parent.color = Color.Black;
					w.right.color = Color.Black;
					left_rotate(x.parent);
					x = root;
					}
				
			} else {
				w = x.parent.left;
				if (w.color == Color.Red) {
					w.color = Color.Black;
					w.parent.color = Color.Red;
					right_rotate(w.parent);
					w = x.parent.left;
				}
				
				if (w.left.color == Color.Black && w.right.color == Color.Black){
					w.color = Color.Red;
					x = x.parent;
				} else{
					if (w.left.color == Color.Black){
						w.right.color = Color.Black;
						w.color = Color.Red;
						left_rotate(w);
						w = x.parent.left;
					
					}
					
					w.color = x.parent.color;
					x.parent.color = Color.Black;
					w.left.color = Color.Black;
					right_rotate(x.parent);
					x = root;
				}
			}
		}
	}
	/** since maximum used in successor, better maximum to take an parameter */
	public Tree tree_minimum(Tree node) {
		Tree p = node;
		while (p != null && p.left != null) {
			p = p.left;
		}
		
		return p;
	}
	
	/** since maximum used in predecessor, better maximum to take an parameter */
	public Tree tree_maximum(Tree node) {
		Tree p = node;
		while (p != null && p.right != null) { 
			p = p.right;
		}
		
		return p;
	}
	
	/** there is  a new root */
	private Tree root;
	/** the sentinel nil */
	private Tree nil = new Tree();
	
	public RbTreeExample() {
		nil.left = nil;
		nil.right = nil;
		nil.parent = nil;
		nil.color = Color.Black;
	}
}

```
