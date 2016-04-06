## introduction
this page will shows you how to use the dynamics programing techniques to work out the multiply chain problems.
this is a typical dynamic programming problems.
the key to a dynamic programming solution consists of the following ingredient

1) optimal solution: an optimal solution contains solution to sub-problems
2) overlapping subproblems: where dynamic programming applies when the subproblems can occurs repeatly
3) reconstructing an optimal solution: we often store *choice* in each subproblems to save cost
4) memoization: with memoization, it can help maintains the top-down manner in contract of the bottom-up form of a dynamic programming model

## code 
the code for the MultiplyChainExample is shown as below.


```

package dynamics;

/** with an CutRodExample to demonstrate the use of Dynamic programming in real application 
 * 
 * the structure of dynamic programming is that 
 * 1) optimal-solution structure: characterize of a optimal solution is that an optimal solution contains solution to subproblems.
 * 2)overlapping sub-problems: for dynamic programming to apply, there should exist overlapping sub-problems, which occurs repeatly so that dynamic programming can optimize by memoize the result in a table
 * 3) reconstructing an optimal solution: we often store *choice* in each subproblems to save cost
 * 4) Memoization: memoization maintains the top-down manner in contract of the bottom-up manner of dynamic programming.
 * @author Administrator
 *
 */
public class CutRodExample {
	public static void main(String[] args) {
		
		CutRodExample example = new CutRodExample();
		
		int[] p =new int[] { 3, 5, 5, 7, 10, 17, 17, 20, 30 } ;
		for (int i = 0; i < p.length; i++)  {
			int result = example.cut_rod(p, i + 1);
			System.out.println("number " + i + " " + result);
		}
		
		int[] r = new int[p.length+1];
		for (int i = 0; i < r.length; i++) {
			r[i] = CutRodExample.NEGATIVE_INFINITY;
		}
		
		for (int i = 0; i < p.length; i++){ 
			int result = example.cut_rod_memoized(p, i+1, r);
			System.out.println("number " + i + " " + result);
		}
		
		for (int i = 0; i < p.length; i++) { 
			int result = example.cut_rod_bottom_up(p, i+1);
			System.out.println("number " + i + " " + result);
		}
		
		for (int i = 0; i < p.length; i++) {
			int result = example.cut_rod_memoized_original(p, i + 1);
			System.out.println("number " + i + " " + result);
		}
	}
	
	private static final int NEGATIVE_INFINITY = Integer.MIN_VALUE;
	private static final int POSITIVE_INFINITY = Integer.MAX_VALUE;
	
	/** the solution to the cut_rod 
	 * 
	 * this is the recursive solution
	 * 
	 * this is a dynamic programming problems.
	 * @param p
	 * @param n
	 * @return the dynamic programming issues
	 */
	public int cut_rod(int[] p, int n) { 
		if (n == 0) { 
			return 0;
		}
		
		int q = NEGATIVE_INFINITY;
		
		for (int i = 0; i < n; i++) { 
			q = Math.max(q, p[i] + cut_rod(p, n - i - 1));
		}
		
		return q;
	}
	
	
	public int cut_rod_memoized_original(int[] p, int n) {
		int[] r = new int[p.length + 1];
		for (int i = 0; i < r.length; i++) {
			r[i] = NEGATIVE_INFINITY;
		}
		
		return cut_rod_memoized_original_aux(p, n, r);
	}
	
	public int cut_rod_memoized_original_aux(int[] p, int n, int[] r) {
		
		if (r[n] != NEGATIVE_INFINITY) {
			return r[n];
		}
		
		
		int q = NEGATIVE_INFINITY;
		if (n == 0) {
			q = 0;
		} else {
			for (int i = 0; i < n; i++) {
				q = Math.max(q, p[i] + cut_rod_memoized_original_aux(p, n - i - 1, r));
			}
		}
		r[n] = q;
		return q;
	}
	
	/** this is a recursive dynamic problems with memoized structure */
	public int cut_rod_memoized(int[] p, int n, int[] r) { 
		if (r[n] != NEGATIVE_INFINITY) { 
			return r[n];
		} 
		
		int q = NEGATIVE_INFINITY;
		if (n == 0) {
			q = 0;
			r[n] = 0;
		} else {
			for (int i = 0; i < n; i++) {
				q = Math.max(q, p[i] + cut_rod_memoized(p, n - i - 1, r));
			}
			r[n] = Math.max(r[n], q);
		}
		
		return q;
	}
	
	/** well, the third phase, if we worked bottom-up, we can declare the memoized space in-place
	 * as compared with the cut_rod_memozed version mentioned above.
	 *  */
	public int cut_rod_bottom_up(int[] p, int n) { 
		int[] r = new int[p.length + 1];
		
		for (int i= 0; i < r.length; i++) {
			r[i] = NEGATIVE_INFINITY;
		}
		
		r[0] = 0;
		
		for (int i = 1; i <= n; i++) { 
			int q = NEGATIVE_INFINITY;
			for (int j = 0; j < i; j++) { 
				q = Math.max(q, r[i - j - 1] + p[j]);
			}
			r[i] = q;
		}
		
		return r[n];
	}
}

```
