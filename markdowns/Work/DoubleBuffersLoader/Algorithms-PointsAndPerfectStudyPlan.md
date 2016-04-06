## introduction 
this page will introduce some of the answers to the new algorithms questions that we introduced below.


## perfect study plan

well, the problem on the perfect study plan is available here 

[OpenJudge - C15F:Study Plan](http://poj.openjudge.cn/practice/C15F/)

the idea is to search through 2*n days study plan, and we know that we can insert a k-days plan on day i and a review plan on day i+k+1. so in summary 
1. keeps a map which tells if a k-days study plan has been attempted so-far
2. attempt to i (starting from 0) to 2*n and try to find next study k-days plan
3. given current plan there is no way to continue, we will restore the study and attempt next k-days study plan
4. if we reached 2*n day and all the days are successfully inserted then we have one solution
5. otherwise, we return false.

given the above analysis we have the following algorithms


```
package search;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
// import java.util.StringJoiner;
import java.util.Scanner;



public class PerfectStudyPlan {
	/*
	public static void main(String[] args) {
		PerfectStudyPlan solution = new PerfectStudyPlan();

		
		/ *
		for (int i = 1; i < 10; i++) {
			List<Integer> result = solution.solution(i);
			
			for (int j : result) { 
				System.out.print(j);;
				System.out.print(" ");
			}
			
			System.out.println();
		}
		* /
		
		// a far better way to solve the issue is as follow
		for (int i = 1; i < 10; i++) {
			List<Integer> result = solution.solution(i);
			//StringJoiner strJoiner = new StringJoiner(",", Arrays.toString(result))
			String[] strings = new String[result.size()];
			for (int j = 0; j < result.size(); j++) { 
				strings[j] = String.valueOf(result.get(j));
			}
			
			// for more details on how to use the StringJoiner, you can find it here:
			//   https://docs.oracle.com/javase/8/docs/api/java/util/StringJoiner.html
			StringJoiner sj = new StringJoiner(" ");
			for (int j = 0; j < strings.length; j++) {
				sj.add(strings[j]);
			}
			
			System.out.println(sj.toString());
		}
	}
	
	*/
	
	public static void main(String[] args) {
		PerfectStudyPlan solution = new PerfectStudyPlan();
		Scanner scanner = new Scanner(System.in);
		int numberOfLines = scanner.nextInt();
		
		for (int j = 0; j < numberOfLines; j++) { 
			int n = scanner.nextInt();
			List<Integer> result = solution.solution(n);
//			String[] strings = new String[result.size()];
//			for (int i = 0; i < strings.length; i++) {
//				strings[i] = String.valueOf(result.get(i));
//			}
			
//			StringJoiner sj = new StringJoiner(" ");
//			for (int i = 0; i < strings.length; i++) {
//				sj.add(strings[i]);
//			}
			StringBuffer sb = new StringBuffer();
			int i = 0;
			while (i < result.size()) {
				sb.append(String.valueOf(result.get(i)));
				i++;
				if (i < result.size()) {
					sb.append(" ");
				}
			}
			
			System.out.println(sb.toString());
		}
		/*
		while (scanner.hasNextInt()) {
			int n = scanner.nextInt();
			List<Integer> result = solution.solution(n);
//			String[] strings = new String[result.size()];
//			for (int i = 0; i < strings.length; i++) {
//				strings[i] = String.valueOf(result.get(i));
//			}
			
//			StringJoiner sj = new StringJoiner(" ");
//			for (int i = 0; i < strings.length; i++) {
//				sj.add(strings[i]);
//			}
			StringBuffer sb = new StringBuffer();
			int i = 0;
			while (i < result.size()) {
				sb.append(String.valueOf(result.get(i)));
				i++;
				if (i < result.size()) {
					sb.append(" ");
				}
			}
			
			
			System.out.println(sb.toString());
			
		}
		*/
	}
	
	
	public List<Integer> solution(int n) { 
		
		if (n < 3) {
			return Arrays.asList(0);
		}
		
		boolean[] planInAction = new boolean[n+1];
		int[] startDay = new int[2*n+1];
		
		for (int i = 1; i < startDay.length; i++) {
			startDay[i] = -1;
		}
		
		if (search(startDay, planInAction, 1))  {
			List<Integer> ret = new ArrayList<Integer>(2*n);
			for (int i = 0; i < 2*n; i++) { 
				ret.add(startDay[i+1]);
			}
			
			return ret;
			
		} else {
			return Arrays.asList(0);
		}
		
	}
	
	
	private boolean search(int[] startDay, boolean[] planInAction, int start) {
		
		int nslot = nextSlot(start, startDay);
		int nplan = nextPlan(1, planInAction);
		
		if (nslot == -1) return true;
		if (nplan == -1) return true;
		
		for (int i = nplan; i < planInAction.length; i++) {
			// find next nplan...
			if (!planInAction[i]) {
				int endDay = nslot+i+1;
				
				if (endDay < startDay.length && startDay[nslot] == -1 && startDay[endDay] == -1) {
					 planInAction[i] = true;
					 startDay[nslot] = startDay[nslot+i+1] = i;
					 if (search(startDay, planInAction, nslot+1)) {
						 return true;
					 }
					 else {
						planInAction[i] = false;
						startDay[nslot] = startDay[nslot+i+1] = -1;
					 }
				 }
			}
		}
		
		// if we have enumerate all the possibility, then we will exit and return false
		return false;
	}

	
	private int nextSlot(int start, int[] map) {
		for (int i = start; i < map.length; i++) {
			if (map[i] == -1)
				return i;
		}
		
		return -1;
	}
	/*
	private int nextPlan(boolean[] plan) {
		for (int i = 0; i < plan.length; i++) {
			if (!plan[i]) { 
				return i;
			}
		}
		
		return -1;
	}
	*/
	
	private int nextPlan(int start, boolean[] plan) {
		for (int i = start; i < plan.length; i++) {
			if (!plan[i]) {
				return i;
			}
		}
		
		return -1;
	}
	
}

```


## points on a plane

the original problem is posted here:

[Max Points on a Line | LeetCode OJ](https://leetcode.com/problems/max-points-on-a-line/)

basically the whole idea to the solution is as follow.


1. if p1.x == p2.x but p1.y != p2.y, which means that there is a vertical line, we can keep a vertical counts
2. if p1.x == p2.x and p1.y == p2.y which means they are the same points, this can keep a same point counts
3. otherwise, we tries to find most number of points which are not same points and not vertical lines points and increment the nubers by "same points counts" - think of why...

given that thought we can come up with the following algorithms

```
# Definition for a point.
# class Point(object):
#     def __init__(self, a=0, b=0):
#         self.x = a
#         self.y = b

class Solution(object):
    def maxPoints(self, points):
        """
        :type points: List[Point]
        :rtype: int
        """
        maxp = 0
        for i in range(len(points)):
        	p = points[i]
        	tangent = {}
        	vline = 1
        	for j in range(i+1, len(ponts)):
        		p2 = points[j]
        		if p2.y == p.y:
        			vline += 1
        		else:
        			tan = abs((p2.y - p.y) / (p2.x - p.x))
        			tangent[tan] = tangent.get(tan, 2) + 1
        	pmax = max(vline, max([0] + tangent.values()))
        	if pmax > maxp:
        		maxp = pmax
```


well, one thing that we can optimize is that on the way to find the same slope, if one slop has been attempted and can we ignore the slopes with the same value? like this:


```
#############################################
#
#  points_plane2.py.py
#
#   we will try to find the max points on a line with a little optimization to ignore finding tangent wich we have already considered.
#
# background:
#   Well, we will print out the max number of Points on a line
#############################################


class Point(object):
	def __init__(self, a = 0, b = 0):
		self.x = a
		self.y = b

# if p2.x == p.x and p2.y == p.y:
# 	for k in tangent.keys():
# 		tangent[k] += 1

class Solution(object):
	def maxPoints(self, points):
		"""
		:type points: List[Point]
		:rtype: int
		"""
		maxp = 0
		checked_tangent = {}
		for i in range(len(points)):
			p = points[i]
			tangent = {}
			vline = 1
			samepoint = 0
			for j in range(i+1, len(points)):
				p2 = points[j]
				if p2.x == p.x:
					vline += 1
					if p2.y == p.y:
						samepoint += 1
				else:
					tan = float(p2.y - p.y) / (p2.x - p.x) # float is built-in in python and double comes from numpy
					if not checked_tangent.has_key(tan):
						 tangent[tan] = tangent.get(tan, 1) + 1
			if samepoint > 0:
				for k in tangent.keys():
					tangent[k] += samepoint
			pmax = max(vline, samepoint + 1, max([0] + tangent.values()))
			if pmax > maxp:
				maxp = pmax
		return maxp

if __name__ == "__main__":
	solution = Solution();
	print solution.maxPoints(list([Point(0, 0), Point(1, 0)])) # 2
	
	print solution.maxPoints(list([Point(0, 0), Point(1, 1), Point(0, 0)])) # 3
	print solution.maxPoints(list([Point(0, 0), Point(1, 1), Point(0, -1)])) # 2
	print solution.maxPoints(list([Point(0, 0), Point(0, 0)])) # 2
	print solution.maxPoints(list([Point(1, 1), Point(1, 1), Point(2, 3)])) # 3
	print solution.maxPoints(list([Point(84, 250), Point(0, 0), Point(1, 0), Point(0, -70), Point(0, -70), Point(1, -1), Point(21, 10), Point(42, 90), Point(-42, -230)]))
```

Turns out that we cannot, because that same slope may means that they are parallel lines, but we can keeps track of the points, if same points and same slope then we can ignore considering the slope again.