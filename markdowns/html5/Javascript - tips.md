## Introduction 

this page is about the Javascript tips.

## undefined vs .null

undefined: type of undefined, normally not initialized value
null: a special value (normally thought as an initialized value), such as a sentinel values. 

type of `undefined` is "undefined", type of `null` is "object", but later version might reports just "null"

```
var b;
b === undefined; // true
b === "undefined"; // false
typeof b === "undefined"; // true
typeof b === undefined; // false
```

and for the null values.

```
var a = null;
typeof a; // "object"
```

## Arrays

array's type if "object"

array has a properties that is called "length"

add to an array with the following code 

```
a[a.length] = "five"
```

or with the more directly engligh push

```
a.push(6);
```

delete a member of array 

while, a common pitfallis to use the "delete" function, which does unset really..

```
delete a[3]

a
>>> [1,2,3,6]

a[3] === undefined; return true

```

if you want to remove, you will need to do "splice"

```
a.splice(3, 1);
a.length; lenght has descrased by 1.
```

## Associative Arrays

it is the hash or dictionary in other languages.


create one by literals

```
// JavaScript
var assoc = {'one': 1, 'two': 2};

```


access/add/update by [] or . notation.

```
assoc.three = 3;
```

to remove, you will need to use the "delete" operators.

```
delete assoc.two;

```

## strict comparison


"==" loose comparison
"===" strict comparison

what are the null "falsy" value.

* Empty string ""
* The number 0
* the value false
* null
* undefined
* Special numeric value NaN


with loose comparison, you might get 

```
null == undefined; // ture
"" == 0;           // true
```


but the following. 
```
null === undefined; // false
0 === ""; // false
```

NOTE: empty array by the rule "all object" are casted to true, (excet for 'null')


```
// PHP
if (array()) {
 echo "hello";
 // Not reachable in PHP
}
// JavaScript
if ([]) {
 console.log('hello');
 // Reachable in JavaScript
}
```


## switch 

Note on the switch statements in javascript

1. like PHP, it works on any types
2. expression does not have to be constants
3. the comparison is done with strict comparison (unlike the php)
```
// JavaScript
var a = "";
var result = "";
switch (a) {
case false:
 result = "a is false";
 break;
case a + "hello": // Expressions are allowed here
 result = "what?";
 break;
case "": // Strict comparison
 result = "a is an empty string";
 break;
default:
 result = "@#$";
}
```

## try-catch 

java script has try-catch-finally

while the PHP version may not have the finally (later version might have that..)

some key notes about the javascript try-catch-finally

• An Error object is thrown, not an Exception
• Type is not declared when catching
• A message property is accessed as opposed to calling a getMessage() method

there is a one interesing things about the scope of try-catch, there is no block scope, only function scope. example is as follow. 

```
try {
 throw new Error();
} catch (e) {
 var oops = 1;
}
typeof e; // "undefined"
typeof oops; // "number"

```

## while and loops 
while, do-while is the same as the php-one .

there is also a vanilla for loop which does a count-based looping..

## for-in loops 

while the php-one has the 

```
for ($colllection as $key => value) 
```

or 

```
for ($colllection as $key) 
```


the javascript only has the 

```
for (var key in collection)
```

## Enhance debugger with attributes

http://msdn.microsoft.com/en-us/library/ms228992(v=vs.110).aspx