## introduction
This page is about the PHP, it includes some useful tips and as well as some reading digest that we have comed together recently.


# reading digest

PHP Objects Patterns and Practices

## Chapter 3 - Object Basics

$this pointer pseudo variable to refer to this object 


constructor is __construct.. PHP4 are still using the ShopProduct (if the class is ShopProduct)

Type Checking Functions: 
* is_bool
* is_integer
* is_double
* is_string
* is_object
* is_array
* is_resource
* *is_null*


1 php's type hint does not enforce at the compile time, while it might throws up at the runtime.

2 instanceof operator(the same effect as the java instance of)

3 extends to create inheritance (just the same as the java extends keywords)

4 :: => To refer to a method in the context of a class rather than an object you use :: rather than ->. 

5 'parent' used instead of the 'base' , e..g parent::_construct

6 parent::__construct

7 one reason to use parent::_construct over the parent::parent_class_name, it decouples
8 parent::base_method

9 var keyword default to use public

10 create a new array with the function (array())

11 add to array with the \$array_var[] = \$element



## Chapter 4 Advanced features

what features that I may be quit interestd in in this chapter would comprise of the following. 

* Interceptor methods: Automating delegation
* Error handling: Introducing exceptions
* Callbacks: Adding functionality to components with anonymous functions

1 static methods and properties
2 constatns Properties
3 Abstract on the class as well on the methods
4 interface (not common on the scripting languages)

5 Static bindings 
5.1    parent:: resolver context, static:: late static binding (in 'static context')
5.2    self is to class what \$this pseudo-variable is to object (self is to class as $this pseudo-variable to object)

6 exception and what it is equipped with 
6.1 methods 
    * getMessage
    * getCode()
    * getFile()
    * getLine()
    * getPrevious
    * getTrace
    * getTraceAsString()
    * __toString()
6.2 throw with `throw`
6.3 catch with a `catch`
6.3 subclass `Exception` class to aid errors handlings.

6 final classes and Methods, you can subclass to the class itself or Method in questions.

7. Interceptors - intercept messages sent to undefined methods
and properties.

7.1 interceptor methods 
  * __get(\$prop)
  * __set(\$prop, \$value) 
  * __isset( \$property )
  * __unset(\$property)
  * __call(\$method, \$arg_array)

8 destructor method : __destruct()

9 unset , calls __unset(\$property) can be really handy when handling with memory (garbage collection).

10 clone (function or keyword) and its interceptor method `__clone()`

11 deep copy vs. shallow copy

12 __toString (the java toString, C# ToString method)

13 callbacks, in the simplest form of anonymous function... and closure..

14 is_callable - test if a \$var is a anonymous function

15 ```create_function(\$args, \$code)``` to create function on the fly..