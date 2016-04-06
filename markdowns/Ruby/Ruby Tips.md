# Introduction

this page will introduce you some of the tips of writing the Ruby program.

## Ruby ternary operators
it is normally writeen as such the ternary operator in Ruby as such 

```

a = true  ? 'a' : 'b' #=> "a"
b = false ? 'a' : 'b' #=> "b"
```



however, it is also possible to write as such, basedon the fact that the && operator will return the first "true" value (so that a value like 'a' is a value that can bve evaluated true in the boolean context) 

```
a = (true  && 'a') || b #=> "a"
b = (false && 'a') || b #=> "b"

```

Given this, we might be able to write some code as such 
```
user_name = (user.authenticated? && user.name) || "gueset"
```


## Case equality operators

we will first give you an example on how to use the case equality operators. 

```
if "yes" === answer
  puts "Good-bye!"
  exit
elsif "no" === answer
  puts "OK, we'll continue"
else
  puts "That's an unknown answer—assuming you meant 'no'"
end
```

the `===` in infix operator position (that is , between a left-hand term and a right-hand term) is really  syntactical sugar for a method call: 

the `when` statement wraps that method call in yet another sugar, you don't have to use `===` operator explicitly or method position. it is done for you.


## Simple truth test with case/when 

> If you start a case statement with the case keyword by itself—that is, with no test
expression—followed by some when clauses, the first when clause whose condition is
true will be the winner:

```
when user.first_name == "David", user.last_name == "Black"
  puts "You might be David Black."
when Time.now.wday == 5
  puts "You're not David Black, but at least it's Friday!"
else
  puts "You're not David Black, and it's not Friday."
end

```

note the use of the ',' separator, which is served as the separator to separate different clauses.

while the code above will evaluate to the following code as such  

```
if user.first_name == "David" or user.last_name == "Black"
  puts "You might be David Black."
elsif Time.now.wday == 5
  puts "you are not David black, but at least  it is Friday!"
else 
   puts "you are not David Black, and it is not Friday."

```


another use or a more important use of the case statement is that it 
> An important final point to keep in mind about case statements is that every case statement evaluates to a single object. That means you could rewrite the test-less example like this:


## repeat one and repeat at most once

if you write as follow with the until modifier statements.

if you write as such , the code will not execute 

```
a = 1
a += 1 until true
```

and if you write as such  , then the code will repeat at least once.  

```
a = 1
begin
a += 1
end until true
```

## curly brances vs. do/end in code block syntax

the difference between the two delimiting a code block is a different in precedence, one example can explain that pretty well.

```
array = [1,2,3]
puts array.map {|n| n * 10 } 

puts array.map do |n| n * 10 end
```


the output are different , the first is that the array (new) that has value (10, 20, 30), and the second it it returns an iterator;

the reason is because the precedence of the do/end and the curly branecs, the {} has higher precedence and bound more closely to the function to the left, while the do/end pair has lower precedence and bound less close to the left, so the net result is that second statement, the `do |n| n * 10 end` bind to the `puts` statements, but the `puts` function will ignore the code block that behinds it.



### example of implementing iterators

we will show you an examples that implements each and times. 

first, the _my_times_ methods

```
class Integer
  def my_times
    c = 0
    until c == self
      yield(c)
      c += 1
    end
   self
  end
end
```

the important thing here is that there is a "self" that we will need to return the self out again. 


second the each method, _my_each_ mehtod.  

```
class Array
  def my_each
  c = 0
  until c == size
    yield(self[c])
    c += 1
   end
   self
  end
end
```

while it is good practise to implements one iterator based on another. 

```
class Array 
   def my_each 
      size.my_times do |i|
          yield  self[i]
      end
      self
    end
end
```

while it is also possible to define map , which is quite some useful  operations.  

```
class Array
  def my_map
    c = 0
    acc = []
    until c == size
      acc << yield(self[c])
      c += 1
  end
  acc
 end
end
```

from the map method, there is a "<<" method that append new element to new array. we might revisit when we are dealing with the map types, which is not a simple array underneath.


## Block parameter and method parameter semantic . 
the semantic that guide/govern the method parameter and the block parameter 

while in block, it does not start a new scope, you may have access to the variable that has the same scope as the parameter, (not precisely), while the method paramter are a little different, whereas the method paramter will start a new local scope, the local variable might shield /hide the variables from outside.


an example is as such 

```
def block_scope_demo
  x = 100
  1.times do 
     puts x
  end
end
```

while, ifyou try to modify the variable inside it?


```
def block_scope_demo2
   x = 100
   1.times do
       x = 200 
  end
  puts x
 end
block_scope_demo_3
```

however, if you have defined a block variable, and the block variable happens to be have the same name in the enclosing (scope), then they are not the same

```
def block_local_parameter
  x = 100 
  [1,2,3] each do |x|
     puts "Parameter x is #{x}"
     x = x + 10 
       puts " reassigned to x in block; it is now #{x}"
     end
     puts "Outer x is still #{x}"
end

```


and ruby has given you the ability to explicitly tell the Ruby that you want to use a temporary variable and not to worry about the accidentally reusing a variable from outside the block.


```
def block_local_variable
    x = "Original x!"
    3.times do |i;x|
        x = i
        puts "X in the block is now #{x}"
    end
    puts "x after the block ended is #{x}"
end
block_local_variable
```

## Exception related 

1. raise an exception  
```
def fussy_method(x)
  raise ArgumentError, "I need a number under 10" unless x < 10
end
```
2. Catch an exception 
```
begin
  fussy_method(20)
rescue ArgumentError => e
  puts "That was not an acceptable number!"
  puts "Here's the backtrace for this exception:"
  puts e.backtrace
  puts "And here's the exception object's message:"
  puts e.message
end
```


while you can omit either the capturing variable parts (then we don't care about the instance of the exception that are raised), or you can omit the Type parts, which means capture every exception type. (catch -all clause) 

```
begin
  fh = File.open(filename)
rescue => e
  logfile.puts("User tried to open #{filename}, #{Time.now}")
  logfile.puts("Exception: #{e.message}")
  raise
end
```

to "ensure" something get a clean up, there is a code. 

```

def line_from_file(filename, pattern)
  fh = File.open(filename)
  begin
   line = fh.gets
   raise ArgumentError unless line.include?(pattern)
 rescue ArgumentError
   puts "Invalid line!"
    raise
  ensure
   fh.close
  end
  return line
end

```

## define unary operators

while you know how to define binary operators, such as +/-, such as the following example shows.

```
class Account
  attr_accessor :balance
  def initialize(amount=0)
    self.balance = amount
  end

  def +(x)
   self.balance += x
  end
  def –(x)
    self.balance -= x
   end
  def to_s
    balance.to_s
  end
end

acc = Account.new(20)
acc -= 5
puts acc
```


while, how can do actually use unary operator, such as + and -;

the key is `+@` and the `-@` operators

```
class Banner < String
  def +@
    upcase
  end
  def -@
    downcase
  end
end

banner = Banner.new("Eat at David's!")
puts +banner
puts -banner
```

## array conversion with to_a and the * operator


check the difference of the two:

```
array = [1,2,3,4,5]
[*arrray]
[array]
```
the first `[*array]` will return `[1,2,3,4,5]` while the `[array]` will get back you `[[1,2,3,4,5]]`;

## to_ary Array ROLE play 


```
class Person  
   attr_accessor :name, :age, :email
   def to_ary
      [name, age, email]
   end
end

david = Person.new
david.name = "David"
david.age = 49
david.email = "david@wherever"
```


## String quotation
single quote do not evaluate the interpolation strings

you can quote string other than `'` or `"`, you can use 


```
%q-A string-
%Q/Another string/
%[Yet another string]
```

## usage of Symbols

Symbols are strings, in that the symbols are 

1. Immutable
2. Uniqueness

## make a JDBC connection from JRuby with JDBC to sqlite3

sqlite3 is a in-memory file backed database, where it is natively developed for C language, while there is a bridge from Java to the native C. 

you can try to install the jdbc-sqlite adn activerecord-jdbcsqlite3-adapter, those two packages will give you access to the libraries. 

run the following commands to get the packages installed. 
```
jruby -S gem install activerecord-jdbcsqlite3-adapter
```

and 

```
jruby -S gem install jdbc-sqlite3
```

then to test the JDBC connection can be successfully made, you can do the following

```
# Gemfile
source 'https://rubygems.org'

gem 'jdbc-sqlite3'
```

then you can write the following code 
```
# reference this page 
##   http://stackoverflow.com/questions/1717674/how-to-initialize-the-sqlite3-jdbc-driver-in-jruby


require 'rubygems'
require 'jdbc/sqlite3'
require 'java'

Jdbc::SQLite3.load_driver

Java::OrgSqlite::JDBC

connection = java.sql.DriverManager.getConnection 'jdbc:sqlite:test.sqlite3'

begin
	statement = connection.createStatement
	begin
		statement.executeUpdate("create table user (name varchar, pass varchar)")
		statement.executeUpdate("insert into user values ('alice', 1234)")
		statement.executeUpdate("insert into user values ('bob', 5678)")
		statement.executeUpdate("insert into user values ('charlie', 'asdf')")


		rs = statement.executeQuery("select * from user")
		begin
			puts "user\tpass"
			while rs.next
				puts ["#{rs.getString(1)}",
				      "#{rs.getString(2)}"].join("\t")
			end
		ensure
			rs.close
		end
	ensure
		statement.close
	end
ensure
	connection.close
end

```

when you run it , here is the output 

    $ jruby -S sql.rb
    user    pass
    alice   1234
    bob     5678
    charlie asdf
    
## Ruby 2.0 has introduced the named/keyword parameters

You can check the reference [Ruby 2.0.0 by Example][ruby_200_by_example].

```
def name({required_arguments, ...}
         {optional_arguments, ...}
         {*rest || additional_required_arguments...} # Did you know?
         {keyword_arguments: "with_defaults"...}
         {**rest_of_keyword_arguments}
         {&block_capture})
```

an example of such is as follow. 


in the erb samples here, 

```
<%= stylesheet_link_tag    'application', media: 'all', 'data-turbolinks-track' => true %>
<%= javascript_include_tag 'application', 'data-turbolinks-track' => true %>

```
while in Ruby 1.9.x or 1.8.x you might only be able to do the following. 

```
<%= stylesheet_link_tag :depot %>
<%= javascript_include_tag :defaults %>
```


References:
[ruby_200_by_example]: http://blog.marc-andre.ca/2013/02/23/ruby-2-by-example/
[Ruby 2.0.0 by Example][ruby_200_by_example]

## Comparing the named arguments of Ruby agains Python

While Python has different, yet a bit simpler version of defining the arguments. here [Python Tutorial: Defining functions][python_tutorial_defining_function].

and there is a language reference [Python Language Reference: Function definitions][python_language_references_defining_function]


```
decorated      ::=  decorators (classdef | funcdef)
decorators     ::=  decorator+
decorator      ::=  "@" dotted_name ["(" [argument_list [","]] ")"] NEWLINE
funcdef        ::=  "def" funcname "(" [parameter_list] ")" ":" suite
dotted_name    ::=  identifier ("." identifier)*
parameter_list ::=  (defparameter ",")*
                    (  "*" identifier ["," "**" identifier]
                    | "**" identifier
                    | defparameter [","] )
defparameter   ::=  parameter ["=" expression]
sublist        ::=  parameter ("," parameter)* [","]
parameter      ::=  identifier | "(" sublist ")"
funcname       ::=  identifier
```

References 
[python_tutorial_defining_function]: https://docs.python.org/3.4/tutorial/controlflow.html#defining-functions
[Python Tutorial: Defining functions][python_tutorial_defining_function]
[python_language_references_defining_function]: https://docs.python.org/2.7/reference/compound_stmts.html#function-definitions
[Python Language Reference: Function definitions][python_language_references_defining_function]


## Rails - Default scope 
where you can control how to display certain produts to users, whether the products should be sorted, whether they should be grouped or something.

well, you can do this, simply by using the default_scope function (this is a class function) 

suppose that we have the product model, now we can add the following 

```
Product < ActiveRecord::Base
    default_scope { order (:title) }
end

```

whlie used you can write as such 

```
Product < ActiveRecord::Base
    default_scope :order => "title"
end
```

## Ruby package/module search path

to get the search path of Ruby when it calls requires, you can do one of the two followings. 

```
jruby -e 'puts $:'
```

or you can invoke the interative console, and you can input the following 

```
puts ($LOAD_PATH)
```
or simply 

```
$LOAD_PATH
```

Reference
[require_looks_up_by_default]: http://stackoverflow.com/questions/9474299/what-are-the-paths-that-require-looks-up-by-default
[What are the paths that “require” looks up by default?][require_looks_up_by_default]

## about adding the comment to the .erb file

You can add comment to the .erb files while there are certain restriction. while this is OK 

```
<!-- 
#
#		<%= yield %>
#
#
-->
```

this is not OK

```
<!-- 
#
#		<%= # yield %>
#
-->
```
there would be some errors being threw out. 

while the first part has some errors. 

the reason is because the Ruby runtime will do the template replacement by doing evaluation the strings between the '<%' and the '%>'

and the problem with 
```
<%= # yield %>
```

is that it will be replaced with 

```
<%
```

with comment being stripped out


so to reduce the aount of replacement that has been done, you can do the following. 

```
<#%= yield %>

```

whatever means that stop the <% and %> expansion.


## flash in rails

> Rails has a convenient way of dealing with errors and error reporting. It defines
a structure called a flash. A flash is a bucket (actually closer to a Hash) in which
you can store stuff as you process a request. The contents of the flash are
available to the next request in this session before being deleted automatically.


also find the discussion about the use of flash vs. instance variabel for displaying the error messages.

why we need a flash, consider the action when a invalid cart_id is given, the best choice is to display error message and then redirect to the catalog pages, while the instance variables this issues that when redirect a new request has been generated which the instance variable has gone.

> hash data is available 