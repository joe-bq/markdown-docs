## introduction
this page will cover the topic of dynamics programming with cutrod algorithm to illustrate the idea of rod cutting.

## code

well, the example shows here will shows you three way to accomplish the cut-rod 

the first one is the brute-force solution which might solving the sub-problems again and again.

the second solution introduced the memoized version, which is useful if it is foreseenable future queried again. such a technique has been used extensivly in Javascript or other scenarios

the last oen is the most typical solution with bottom-up solution..



well, all three algorigthm is deduced from the tutorial "Introduction to algorithms"

```
package dynamics;

/** with an CutRodExample to demonstrate the use of Dynamic programming in real application 
 * 
 * the structure of dynamic programming is that 
 * 1) sub-problem structure 
 * 2) overlapping sub-problems
 * 3) 
 * 
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
