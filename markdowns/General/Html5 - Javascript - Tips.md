## Introduction 

this page is mainoly about the best practise of the javascript lanaguage itself. 


## Built-in APIs

there are some general rules about creating and using of the javascript objects and etc..

* Object()
  It’s better to use the object literal {} instead.
* Array()
  Use literal [] instead.
* RegExp()
Use literal /[a-z]/ when the pattern is static.
* Function()
Use a function declaration or a function expression instead.
* String()
Just define a regular primitive "string" and use this constructor only for type casting.
* Number()
Use only for type casting; otherwise, numbers are better defined as primitives.
* Boolean()
Useless; just use true and false literally.
* Error()
Just throw your own errors (e.g., SyntaxError(), etc.).
* Date()
The only constructor you can’t get without.
* Math
Not a constructor, but a useful namespace for math constants and static methods.
* JSON
Also not a constructor, but a global object you’ll see again in Chapter 6.


## Property Attributes 

a property can have value attribute as wella s three boolean attributes, which define whether the property is. 

* Enumerable
* Writable
* Configurable

well, an example is to define one property descriptor, which is a special object special objects called:

```
var stealth_descriptor = {
    value: "can't touch this",
    enumerable: false, // Won't show up in for-in loops
    writable: false, // Can't change my value
    configurable: false // Can't delete me or change my attributes
};
```


## Object.create and the relationship with the Property attributes

e.g. 

```
var human = {name: "John"};
var programmer = Object.create(
human,
{
    secret: stealth_descriptor,
    skill: {value: "Code ninja"}
}
);

```

`stealth_descriptor` set the value as well as the three attributes.

`skill` one have value property, sot the attributes are set to the default value, which is 'false'

if simply set a property without a descriptor, all attributes are true, e.g. 

`programmer.likes = ['pizza', 'beer', 'coffee'];`


## Restricting Object Mutation

there are the following methods that you can control the usage of the Objec, they are:

* freeze
* seal
* preventExtensions

and there are the following explaination.


* freeze() does what seal() does plus sets the writable attribute to false for all properties.
* seal() does what preventExtensions() does plus sets the configurable attribute to false for all properties.
* preventExtensions() doesn’t set any attributes, but it doesn’t let you add more properties afterward.
* None of these actions can be turned back on (i.e., there’s no unfreeze(), defrost(), allowExtensions(), etc.).


## Looping alternatives

```
var pizza = {tomatoes: true, cheese: true};
Object.keys(pizza); // ["tomatoes", "cheese"]
Object.getOwnPropertyNames(pizza); // ["tomatoes", "cheese"]
```


*Note: the keys has something to do with the enumerable attribute*.

```
var pizza_v20 = Object.create(pizza, {
    salami: {value: "lots", enumerable: true},
    sauce: {value: "secret"}
});
```

keys won't have the 'sause' because it is not enumerable, but getOwnPropertyNames() will return all properties. 



## Object.getPrototypeOf()

allow you to get the prototype object. 

like ____proto____ but ____proto____ is not standard, at least IE does not support it


## Array Additions 

### Array.IsArray
Array.isArray() : becareful of its relationship with the Object.prototype.toString() trick

### indexOf() and lastIndexOf(): 

indexOf() and lastIndexOf(): 

### Walking the Arrat Elements

```
["a", "b", "c"].forEach(function () {
console.log(arguments);
})
```

the argument to the callback method is 

```
[the element, its index, the whole array]
```


### Filtering 

let's you do filter

```
function testVowels(char) {
    return (/[aeiou]/i).test(char);
}
var input = ["a", "b", "c", "d", "e"];
var output = input.filter(testVowels);
output.join(', '); // "a, e"
```

### every and some

there are a every and some method. 
```
function isEven(num) {
    return num % 2 === 0;
}
```

e.g.

```
// Are *all* of the numbers even?
[1, 2, 4].every(isEven); // false
// Are at least some (or even one) of the numbers even?
[1, 2, 4].some(isEven); // true
```

### map/reduce method 

```
function entity(char) {
    return "&#" + char.charCodeAt(0) + ";";
}
```


let's apply it to all elements of an array 


```
var input = ['a', 'b', 'c'];
var out = input.map(entity);
out; // ["&#97;", "&#98;", "&#99;"]
```

and the example of the reduce application is as follow. 

```

function sum(running_sum, value, index, array) {
    console.log(arguments);
    return running_sum + value;
}
[1, 2, 3].reduce(sum, 100); // 106

```

There is also a reduceRight method , here is it in action l


## Function.prototype.bind() 

bind give a a bound function back, here is what you you can do with the bind method. 

```
var breakfast = {
    drink: "coffee",
    eat: "bacon",
    my: function () {
        return this.drink + " & " + this.eat;
    }
};
breakfast.my(); // "coffee & bacon""
```


to bind and call.


```

var morning = breakfast.my.bind(breakfast);
morning();

```

## JSON

JSON has two method, stringify and pase, here are they in action.  

```
JSON.stringify({hello: "world"}); // '{"hello":"world"}'
JSON.parse('{"hello":"world"}').hello; // "world"
```

## Shims

Shim or polyfills, are a way to suppor tnew APIs in older environment, example is as follow. 

```
if (!Date.now) { 
	Date.now = function() { 
		return new Date().getTime();
	}
}


// source
// https://developer.mozilla.org/en-US/docs/JavaScript/Reference/
// Global_Objects/String/Trim


if (!String.prototype.trim) {
		String.prototype.trim = function() { 
			return this.replace(/^\s+|\s+$/g, '');
		}

}
```


## the falsy value in javascript
the following values are treated as the falsy values.

* false
* null
* undefined
* the empty string ''
* the number 0
* the number NaN


## the double ~~ operators

while you may wonder why we have this operator sometime.s


e.g.
```
var jdn = function(y, m, d) { 
	var tmp = (m <= 2 ? -1 : 0);
	return ~~ ((1461 * (y + 4800 + tmp)) / 4) + 
	       ~~ ((367 * (m - 2 - 12 * tmp)) / 12 ) - 
	       ~~ ((3 * ((y + 4900 + tmp) / 100) / 4 ) + 
	       d - 2483620;
};
```

[What is the "double tilde" (~~) operator in JavaScript? - Stack Overflow](http://stackoverflow.com/questions/5971645/what-is-the-double-tilde-operator-in-javascript)


## the !~ operator
the !~operator in teh javascript is as follow. 

```

for (c = 0, cl = classNames.length; c < cl; c++) { 
    if (!~setClass.indexOf( " " + classsNames[ c ] + " ") ) { 
    setClass += classNames[c ] + " ";
 }

}


```

Here you might already have figured out what is the use of the !~ operators, because the indexOf operation might return just -1 to indicate if no found the relative string in the target. and in that cause ~ will return an positive number, adn the logic not operator on it will change that to false, while other values will return true .