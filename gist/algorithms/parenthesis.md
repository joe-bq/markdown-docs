## introduction

the parenthesis problem is a problem that a divide and conquer problem where divide a bigger problem into two smaller problems.

## code

Solution I

```
#############################################
#
# balanced_parentheses.py
#
#   this is a program to show you how to list all the possible balanced parentheses
#
#############################################

def parenthesized(exprs):
	if len(exprs) == 1:
		yield exprs[0]
	else:
		first_exprs = []
		last_exprs = list(exprs)
		while 1 < len(last_exprs):
			first_exprs.append(last_exprs.pop(0))
			for x in parenthesized(first_exprs):
				if 1 < len(first_exprs):
					x = '(%s)' % x
				for y in parenthesized(last_exprs):
					if 1 < len(last_exprs):
						y = '(%s)' % y
					yield '%s%s' % (x, y)

for x in parenthesized(list(['a', 'b', 'c', 'd'])):
	print x
```

Solution II:
```
#############################################
#
# balanced_parentheses_solutionII.py
#
#   this is a program to show you how to list all the possible balanced parentheses
#
#############################################

def association(seq, **kw):
	grouper = kw.get("grouper", lambda x, y: (x, y))
	lifter = kw.get("lifter", lambda x: x)
	if len(seq) == 1:
		yield lifter(seq[0])
	else:
		for i in range(len(seq)):
			left = seq[:i]
			right = seq[i:]
			for x in association(left, **kw):
				for y in association(right, **kw):
					yield grouper(x, y)

for x in association(['a', 'b', 'c', 'd']):
	print x
```
