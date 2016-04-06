Chapter 1:

install ruby 1.9.1/1.9.3??


command line to use :


irb --simple-prompt

# A comment
x = 1 # A Comment


Variables:

local variable: x, string, __abc__
Instance :   @age, @last_name
class variables: @@runing_total
global variables: $:, $1, $/ 

CONSTANTS:
Beegin with an uppercase letter: A, String, FirstName, STDIN

Keyword:
	class, if, __FILE__

	
METHODS NAMES:
	(methods may have) ?, !, = , otherwise, it is the same as the local variables.

	
Sending messages vs. Methods

bareword-style invocation: 
	message sent to the implicit "self"
	
Built-in classes
	String, Array, Fixnum

Concept of class vs. Concept of object
	...in Ruby, the class isn't hte sole determinant of what the object can do 

Writing and saving a sample program (whether or not to use some IDE)

Feeding program to Ruby 

	ruby 1_1.rb
	irb.bat 1_1.rb

	check for syntax: 
	
	ruby -cw c2f.rb

Anatomy: 
	# preload a ruby pacakge 
	irb --simple-prompt --rrbconfig
	# request that information
	Config::CONFIG["bindir"]

	# ruby 2.1
	RbConfig::CONFIG["bindir"]

	
Ruby library subdirectory 
	# 
	Config::CONFIG["rubylibdir"]

Ruby Extensions Directory: (C Extension)
	# 
	Config::CONFIG["archdir"]
	# Ruby 2.1
	RbConfig::CONFIG["archdir"]
	# "c:/ProgramFiles/ruby-2.1.0/lib/ruby/2.1.0/i386-mswin32_100"
	
The site_ruby, vendor_ruby (where the 3rd party extensions and libraries)

	>> RbConfig::CONFIG["sitedir"]
	=> "c:/ProgramFiles/ruby-2.1.0/lib/ruby/site_ruby"
	>> RbConfig::CONFIG["vendordir"]
	=> "c:/ProgramFiles/ruby-2.1.0/lib/ruby/vendor_ruby"

The gem directory:
	The RubyGems utility is the standard way to package and distribute Ruby libraries. When you install gems (as the packages themselves are called), same level as the site_ruby

require and load
	load: load and run
	require: do not load a module more than once... (seems not searching the currenct directory)

default loading path:
	$: load path
	
	#to check 
	ruby -e 'puts $:'
	
	will check the current directory searching for loading , seems that "require" does not check the current directory
	// http://stackoverflow.com/questions/8510981/in-ruby-how-can-i-require-a-file-from-the-current-working-dir
	
out-of-the-box ruby tools and applications
	erb: templating system
	testrb: high-level tool for use with Ruby test framework
	ri: ???

Interpreter commandline switches
	-c : syntax check
	-w : high level warning
	-e : execute expression
	-v : version
	-l : line mode, new line after every line of output
	-rname: require the named feature, e.g. -rprofile, -rrbconfig
	--version: show ruby version information

Expression have a value	
	>> days = 365
	=> 365
	# call to puts has a return value: nil
	puts "hello"
	hello
	=> nil

Interrupting and exiting
		ctrl-c, ctrl-z: interrupting
		ctrl-d, exit: to exit

ri and RDoc:

	ri: Ruby index, e.g. ri String#upcase
	rdoc: generate documents out of the documentation files. -- SimpleMarkup system
	
	# for class method, do Class::Method
Concept of 
Chapter 2:

1.4.4. rake
which is a makefile inspired project

# call the following command
rake admin:clean_tmp

namespace :admin do 
  desc "Interactively delete all files in C:\Documents and Settings\wangboqi\Local Settings\Temp" 
  task :clean_tmp do 
    Dir["C:/Documents and Settings/wangboqi/Local Settings/Temp/*"].each do |f|
      next unless File.file?(f)
      print "Delete #{f}? "                       
      answer = $stdin.gets 
      case answer 
      when /^y/ 
        File.unlink(f)                            
      when /^q/ 
        break                                     
      end 
    end 
  end 
end 


# find all tasks
rake --tasks

you can nest namespace of the tasks as you like , below is the following 

namespace :admin do 
  namespace :clean do
    task :tmp do 
	  #etc .
	end
  end
end 

1.4.5 Installing packages with the gem command

e.g. 
$gem install rupport

install from local 
$ gem install /home/me/mygems/ruport-1.4.0.gem

# use the gem command to find not-quite-current version of Hoe, you can do the following  

gem 'hoe', '<1.8.2'


2. Objects, Methods, and local variables

In this chapter
¦ Objects and object-orientation
¦ Innate vs. learned object capabilities
¦ Method parameter, argument, and calling
syntax
¦ Local variable assignment and usage
¦ Object references

2.1.2. creating a generic objects 

conceptually, ruby object can learn things that the class does not teach it

2.1.3 methods that takes arguments

def obj.c2f(c)
  c * 9.0 / 5 + 32
end

# parameter is optional

def obj.c2f c
  c * 9.0 / 5 + 32
end


2.1.4 return  values

the last exprssions' value is the return value, or you can explicitly "return"


return a,b,c 
# not a,b,c
# or construct an array to return as well
[a,b,c]
return [a,b,c]

2.1.5   crafting an boject, the behavior

# will show you how to define methods on a single object
ticket = Object.new
def ticket.venue
  "Town Hall"
end 
def ticket.performer
  "Mark Twain"
end
def ticket.event
  "Author's reading"
end
def ticket.price
  5.50
end
def ticket.seat
  "Second Balcony, row J, seat 12"
end
def ticket.date
  "01/02/03"
end

print "This ticket is for: "
print ticket.event + ", at "
print ticket.venue + ", on "
puts ticket.date + "."
print "The performer is "
puts ticket.performer + "."
print "The seat is "
print ticket.seat + ", "
print "and it costs $"
puts "%.2f." % ticket.price


2.2.3 string interoplation

# format is the interoplation operators #{...}
# string concatenation is done via the '+' operator
puts "This ticket is for : #{ticket.event}, at #{ticket.venue}." + 
  "The performer is #{ticket.performer}." +
  "The seat is #{ticket.seat}, " +
  "and it costs $#{"%.2f." % ticket.price}"

2.2.4: true or false value 

# better this 
def ticket.availability_status
"sold"
end

# or this?
def ticket.available?
	false
end


#everything except the "false" or 'nil" has value "true"

2.3 innate behaviors of an object

# get methods of a new object

p Object.new.methods.sort


among all the methods, the following are important:

¦ object_id
¦ respond_to?
¦ send (synonym: __send__)


## there is a basic object, which has barely nothing in it, comparing that to the generic object that you get back from Object.new


2.3.  object_id method

string_1 = "Hello"
string_2 = "Hello"
puts "string_1's id is #{string_1.object_id}."
puts "string_2's id is #{string_2.object_id}."

# object identity vs. ojbect equality comparison


2.3.2 respond_to? method

#respond_to is the reflection  or the "introspection"

obj = Object.new
if obj.respond_to?("talk")
	obj.talk
else
	puts "Sorry, the object doesn't understand the 'talk' message."
end


# when comparing with the python, you can achieve the respond_to with the following code

class Fun:
  def hello(self):
    print "hello"
hasattr(Fun, 'hello')
callable(fun.hello)

or you can do with the callable(Fun.hello) with exception handlign suite

try:
  callable(Fun.goodbye)
except Attribute, e:
  return false


2.3.3. send message (invocation based on reflection)

print "Information desired: "
request = gets.chomp

if ticket.respond_to?(request)
  puts ticket.send(request)
else
  puts "no such information available"
end

#note, there are a public_send and __send__ methods

2.4 method arguments.
 
# we will take a look at the "required" and "optional", and "default"


2.4.1 required and optional arguments

# -- arbitary number of arguments, (*: asterisk)

def obj.multi_args(*x)
	puts "I can take zero or more arguments!"
end

def two_or_more(a,b,*c)
  puts "I require two or more arguments!"
  puts "And sure enough, I got: "
  p a, b, c
end


2.4.2 defualt value argumnet

def default_args(a, b, c = 1)
  puts "Values of variables: ",a,b,c
end

2.4.3 order of parmeters and arguments


def args_unleashed(a,b=1,*c,d,e)
  puts "Arguments:"
  p a,b,c,d,e
end

# though personally I would like to have the list argument to be in the last position

2.4.2 what you cannot do in an argumnet lists

def broken_args(x, *y, z=1)
end


2.6 Local variables and variables assignent

Local variable names start with a lowercase letter or an underscore and are made up
of alphanumeric characters and underscores.

x
_x
name
first_name
plan9
user_ID
_

# local variables have scopes

# -- ruby prefers underscores to the camelCase for local variables


def say_goodbye
  x = "goodbye"
  puts x
end

def start_here
  x = "hello"
  puts x
  say_goodbye
  puts "Let's check whether x remained the same:"
  puts x
end

start_here

2.6.1

the un-reference : immediate values

# immediate values 
some object in Ruby are stored in Variables as immediate values. , includes 
integers
symbols (which looks like :this)
special object (true, false, and nil)


# some ramification on the immediate values rules 
x = 1
x++ # no such operators

2.6.2

2.6.3 References and mehtod argument (show some method to protect object from being changed)
# duping and freezing objects

def change_string(str)
	str.replace("New string content!")
end

s = "Original string content!"
change_string(s.dup)
puts s

# freeze one 
s = "Original string contents!"
s.freeze
change_string(s)

# -- clone vs. dup, dup can return a modifiable object, and clone return just as what the object is before 

2.6.4.

Here’s how Ruby decides what it’s seeing when it encounters a plain identifier:
1 If the identifier is a keyword, it’s a keyword (Ruby has an internal list of these
and recognizes them).
2 If there’s an equal sign (=) to the right of the identifier, it’s a local variable
undergoing an assignment.
3 Otherwise, the identifier is assumed to be a method call.


3. Organizing objects with Classes

in this chapter

¦ Creating multiple objects with classes
¦ Setting and reading object state
¦ Automating creation of attribute read and write
methods
¦ Class inheritance mechanics
¦ Syntax and semantics of Ruby constants

3.1. classes and instances

obj = Object.new


# classes namea are constants, classes contains collection of mehtod definition, the classes exists (also in most cases) for the purpose of being instantiated: 

class Ticket
  def event
    "Canot'r eally be specified here..."
  end
end

3.1.1 instance methods

#  Methods of this kind, defined inside a class and intended for use by all instances of the class, are called instance methods.

# instance method
Class Ticket 
  def price
    5.0
  end
end

# singleton method
ticket = new Object
def ticket.price 
  5.0 
end



3.1.2 overriding methods

class C
  def m
    puts "First definition of method m"
	end
  def m
    puts "Second definition of method m"
  end
end


# second prevail

C.new.m

3.1.3 Reopening classes

# to reopen an object ot make changes

class C
  # classes code here
end

class C
  def y
  end
end


#real world examples, time.rb has enhancement to the time classes 
# check the code below.

>> t = Time.new
=> 2014-01-02 15:18:58 +0800
>> t.xmlschema
NoMethodError: undefined method `xmlschema' for 2014-01-02 15:18:58 +0800:Time
        from (irb):99
        from C:/ProgramFiles/RailsInstaller/Ruby1.9.3/bin/irb:12:in `<main>'
>> require "time"
=> true
>> t.xmlschema
=> "2014-01-02T15:18:58+08:00"

3.2  Instance variables and object state

instance variables have the following attributes:


class Person
  def set_name(string)
    puts "Setting person's name..."
    @name = string
  end
  def get_name
    puts "Returning the person's name..."
    @name
  end
end

joe = Person.new
joe.set_name("Joe")
puts joe.get_name

3.2.1 initializing an object with state (constructor)

class Ticket
  def initialize(venue, date)
    @venue = venue
	@date = date
  end

  # get the value back 
  def venue 
   @venue
  end
  
  def date
    @date
  end
end 

th = ticket.new("Town Hall", "11/12/13"
cc = ticket.new("Convention Center", "12/13/14"

puts "We've created two tickets."
puts "The first is for a #{th.venue} event on #{th.date}."
puts "The second is for an event on #{cc.date} at #{cc.venue}."

3.3 setter method

# better not to use the equal sign (=) method set_name is not nature 

3.3.1 the equal sign (=) in method name

class Ticket
  def initialize(venue, date, price) 
    @venue = venue
	@date = date
	@price = price
  end
  #etc
  def price
    @price
  end
  
  #ugly way 
  def set_price(amount) 
    @price =  amount
  end

  def price=(amount)
    @price = amount
  end
  
end

ticket = Ticket.new("Town Hall", "11/12/13")
ticket.set_price(63.00)
ticket.price=(63.00)

3.3.2 syntactic sugar for assignment methods

ticket.price= 63.00 


3.3.3 Setter method unleased

# what you can do with the setter methods?

# you can do the following with the setter methods
#   data normalization
#   filter or gate keeper


#note, Ruby takes the assignment semantice seriously , 

*** the value of the expression ticket.price = 63.00 is 63.00, even if the ticket= method returns the
string “Ha ha!”



3.4 attributes and attr_* method family

An attribute is a property of an object whose value can be read and/or written through
the object.

3.4.1. Automating the creation of attributes

class Ticket
  def initialize(venue, date)
    @venue = venue
	@date = date 
  end
  
  def price=(price)
    @price = price
  end
  def venue
    @venue
  end
  def date
    @date
  end
  def price
    @price
  end

end

# this is very repetive, and ruby has provide shortcut, as follow 
class Ticket
  attr_reader :venue, :date, :price
  #the automatic writer
  attr_writer :price
  
  def initialize(venue, date)
    @venue = venue
	@date = date
  end
end

# accessor: both has the reader and writer

class Ticket
  attr_reader :venue, :date
  attr_accessor :price
  def initialize(venue, date)
    @venue = venue
	@date = date
  end
end


# anonym called 'attr'

attr :price, true

3.4.2 Summary of attr_* methods

3.5. inheritance  and the Ruby class hierarchy

# inheritance is the is-a relationship

class Publication
  attr_accessor :publisher
end

class Magazine < Publication
  attr_accessor :editor
end

class Ezine < Magazine
end


mag = Magazine.new
mag.publisher = "David A. Black"
mag.editor = "Joe Smith"



3.5.1 Single inheritance : one to a customer

# ruby only support single inheritance
# ruby in additional provides the modules, which can be grafted to your classes

3.5.2 Object ancestry and the not-so-missing link: the Object class

class C
end
class D < C
end

puts D.superclass
puts D.superclass.superclass

3.5.3. BasicObject

BasicObject is even older than the Object class.

The idea behind BasicObject is to offer a
kind of blank-slate object—an object with almost no methods.

> BasicObject.new
NoMethodError: undefined method `inspect' for #<BasicObject:0x538298>


3.6 Classes as objects and messgae receivers

Classes are also object, special objects. you can create Classes, this shows you how :

# formal way
class Ticket
  # your code here
end

# whic is a nice-looking, easily accessed class-definition block.

my_class = Class.new

# with the new class "my_class"< you can create object/instance of that clases

instances_of_my_class = my_class.new

3.6.1 the chick and egs paradox,  (you can ignore this for now)

If you want to create an anonymous class using Class.new, and you also want to add
instance methods at the time you create it. you can do so by appending a code block
after the call to new.

c = Class.new do
  def say_hello
    puts "Hello!"
  end
end


*** what is a "code block"

A code block is a fragment of code that you supply as part of a
method call, which can be executed from the method.


3.6.2 HOw classes objects call methods

Tickets.some_message
*** in this case, the Class is playing the role of the default object self. it looks like this: 
class Ticket
  some_message
  
*** module is the ancestor of Class
*** class Class has method 'new' , and the class module has 'attr_accessor'

3.6.3. A singleton method by any other name

single method on the Class object is the Class method for objects of that classes

e..g 
class Ticket
end

create a Class Ticket, and a Ticket object, and you can create singleton method on the Ticket object

class Ticket
  attr_accessor :price
  def Ticket.most_expensive(*tickets)
    tickets.max_by(&:price)
  end
  
  th = Ticket.new("Town Hall","11/12/13")
  cc = Ticket.new("Convention Center","12/13/14/")
  fg = Ticket.new("Fairgrounds", "13/14/15/")
  th.price = 12.55
  cc.price = 10.00
  fg.price = 18.00
  highest = Ticket.most_expensive(th,cc,fg)
end

*** interesting reading, class Class have one class method "new" and a instance method version of "new"

3.6.4.  when , and why, to write a class method 


when:
  operations pertaining to a class can't be performed by individual instance of the classes, like the new method
  built-in ruby method File.open 
  
Remember:
¦ Classes are objects.
¦ Instances of classes are objects, too.
¦ A class object (like Ticket) has its own methods, its own state, its own identity. It
doesn’t share these things with instances of itself. Sending a message to Ticket isn’t
the same thing as sending a message to fg or cc or any other instance of
Ticket.

name conventions: 
Ticket#price
Ticket.most_expensive
Ticket::most_expensive



3.7  Constants up close


Basic use of Constants:

class Ticket 
  VENUES = ["Convention Center", "Fairgrounds", "Town Hall"]
end


puts "We've closed the class definition."
puts "So we have to uset he patch notation to reach the constant."
puts Ticket::VENUES

# other ruby constants

MATH::PI
>> RUBY_VERSION
=> "1.9.1"
>> RUBY_PATCHLEVEL
=> 0
>> RUBY_RELEASE_DATE
=> "2008-12-30"
>> RUBY_REVISION
=> 21203
>> RUBY_COPYRIGHT
=> "ruby - Copyright (C) 1993-2008 Yukihiro Matsumoto"

3.7.2 Reassigning vs. Modifying constants

A = 1
A = 2

you will receive the following message:

  warning: already initialized constants A

you can modify the object that it reference to: REMEMBER THIS PARADOX

venues = Ticket::VENUES
venues << "High School Gym"


3.8 Nature vs nurture in Ruby objects. 

general/specific relationship

is-a relationship between base clases and derived classes.


mag = Magazine.new
mag.is_a?(Magazine)
mag.is_a?(Publication)



object has natured capability 

mag = Magazine.new
def mag.wings
 puts 'Look! I can fly!'
end



4. Modules and Program Organization

Encapsulation of behavior in modules
¦ Modular extension of classes
¦ The object method-lookup path
¦ Handling method-lookup failure
¦ Establishing namespaces with modules and nesting


Like classes, modules are bundles of methods and constants. Unlike
classes, modules don’t have instances; you specify that you want the functionality
of a particular module to be added to the functionality of a class or of a
specific object.

Class is a subclass of class Module, so every object is a module object

Kernel: where the majority of hte methods common to all object lives


4.1 Basic of module creation and use

module MyFirstModule
  def say_hello
    puts "Hello"
  end
end

module are "mixed in" to class, using the include method.

class ModuleTester
  include MyFirstModule
end

mt = ModuleTester.new
mt.say_hello

from a class and mixing in a module is
that you can mix in more than one module. No class can inherit from more than one
class.

4.1.1. A module encapsulate "stack-like-ness"


module Stacklike

  def stack
    @stack ||= []                                                   #1
  end  

  def add_to_stack(obj)                                             #2
    stack.push(obj)
  end

  def take_from_stack                                               #3
    stack.pop
  end
end


# some note on the ||= (or-equals), the net effect of this operator is that it return the object if it is not nil or false; otherwise, set it to a new empty array.
# NOTE "or-equals", you can rewrite the function as array ||= []
# how this works out? 
# the short-cut operators, it requires the object to have the relevant underlying method.


4.1.2 Mixing a module into a class
s = Stacklike.new   # this is wrong.

but you have to mix that in.

#require "stacklike"
require_relative "stacklike"
class Stack
  include Stacklike                                             #1
end
s = Stack.new                                                   #1
s.add_to_stack("item one")                                      #2
s.add_to_stack("item two")                                      #2
s.add_to_stack("item three")                                    #2
puts "Objects currently on the stack:"
puts s.stack
taken = s.take_from_stack                                       #3
puts "Removed this object:"
puts taken
puts "Now on stack:"
puts s.stack

# note, normally the class is a noun, but the module to mixed in is a adjective. , that is the engligh, not the law..
the above code is relevant to the following code.
class Stack 
  attr_reader :stack 

  def initialize 
    @stack = [] 
  end 

  def add_to_stack(obj) 
    @stack.push(obj) 
  end 

  def take_from_stack 
    @stack.pop 
  end 
end 


4.1.3 Leveraging the module further

we will show an example on how to use the module more effectively 

require_relative "stacklike"

class Suitcase
end

class CargoHold
  include Stacklike                                                #1
  def load_and_report(obj)                                         #2
    print "Loading object "
    puts obj.object_id
    add_to_stack(obj)                                              #3
  end
  def unload
    take_from_stack                                                #4
  end
end
ch = CargoHold.new                                                 #5
sc1 = Suitcase.new
sc2 = Suitcase.new
sc3 = Suitcase.new
ch.load_and_report(sc1)
ch.load_and_report(sc2)
ch.load_and_report(sc3)
first_unloaded = ch.unload
print "The first suitcase off the plane is...."
puts first_unloaded.object_id


4.2. Modules, classes adn method lookup 

we will examine how the instance discover the appropriate method to invoke 

module M
  def report
    puts "'report' method in module M"
  end
end

class C
  include M
end

class D < C
end

so this is how that works.

:: Class, modules reversed (there might be multiple modules that has been mixed-in), then up one level and repeat

class Object mixin the module named "Kernel"
obj = D.new
obj.report

4.2.2 the rule of mehtod lookup summarized 

¦ Its class
¦ Modules mixed into its class, in reverse order of inclusion
¦ The class’s superclass
¦ Modules mixed into the superclass, in reverse order of inclusion
¦ Likewise, up to Object (and its mix-in Kernel) and BasicObject


4.2.3 Defininig the same name more than once

last win -- first win

in the same class, if you have method of the same name, the LAST WIN
when more classes and modules are involved, like both the module and class has the same name, the FIRST WIN

module InterestBearing
  def calculate_interest
    puts "Placeholder! We're in module InterestBearing."
  end
end

class BankAccount
  include InterestBearing
  def calculate_interest
    puts "Placeholder! We're in class BankAccount."
    puts "And we're overriding the calculate_interest method!"
  end
end

account = BankAccount.new
account.calculate_interest


#**** INCLUDING A MODULE MORE THAN ONCE (has no effect)

module M
  def report
    puts "'report' method in module M"
  end
end

module N
  def report
    puts "'report' method in module N"
  end
end

class C
  include M
  include N
  include M
end


c = C.new
c.report

4.2.4. Going up the method searc path with super

you can use the "super" keyword to jump up to the next-highest definition. e.g.

module M
  def report                                      #1
    puts "'report' method in module M"
  end
end
class C
  include M
  def report                                        #2
    puts "'report' method in class C"
    puts "About to trigger the next higher-up report method..."
    super                                           #3
    puts "Back from the 'super' call."
  end
end

c = C.new
c.report                                           #4

#*** NOTE:
# why not calling "super.report" but rather just "super"?
# think this way, keep looking for next match (rather than just up one level in the class hierarchy, you may include the module in the path of finding as well)

class Bicycle
  attr_reader :gears, :wheels, :seats

  def initialize(gears = 1)                                  #1
    @wheels = 2
    @seats = 1
    @gears = gears
  end
end

class Tandem < Bicycle
  def initialize(gears)
    super
    @seats = 2                                               #2
  end
end

# rules regarind when calling the super


¦ Called with no argument list (empty or otherwise), super automatically forwards
the arguments that were passed to the method from which it’s called.
¦ Called with an empty argument list—super()—it sends no arguments to the
higher-up method, even if arguments were passed to the current method.
¦ Called with specific arguments—super(a,b,c)—it sends exactly those
arguments.

4.3 The method_missing method  (when method looks up fails)

called wheen the search hit top but there is no such method defined.

o = object.new
o.blah
def o.method_missing(m, *args)
   puts "you cannot call #{m} on this object; please try again."
end
o.blah

4.3.1 Combining method_missing and super

it is common to intercept an unrecognized message and decide, on the spot,
whether to handle it or to pass it along to the original method_missing (or possibly an
intermediate version, if another one is defined).

class Student
  def method_missing(m, *args)
    if m.to_s.start_with?("grade_for_") # convert symbol to string before testing..
      # return the appropriate grade, based on parsing the method name
    else
      super
    end
  end
end

a more extensive examples is as follow.

class Person
  PEOPLE = []                              #1
  attr_reader :name, :hobbies, :friends    #2

  def initialize(name)
    @name = name
    @hobbies = []                          #3
    @friends = []
    PEOPLE << self                         #4
  end

  def has_hobby(hobby)                     #5
    @hobbies << hobby
  end

  def has_friend(friend)
    @friends << friend
  end

# Continues in 4_13.rb

# Continuation of 4_12.rb

  def self.method_missing(m, *args)
    method = m.to_s
    if method.start_with?("all_with_")                #1
      attr = method[9..-1]                            #2
      if self.public_method_defined?(attr)            #3
        PEOPLE.find_all do |person|                   #4
          person.send(attr).include?(args[0])
        end
      else
        raise ArgumentError, "Can't find #{attr}"     #5
      end
    else
      super                                           #6   
    end
  end
end

j = Person.new("John")
p = Person.new("Paul")
g = Person.new("George")
r = Person.new("Ringo")
j.has_friend(p)
j.has_friend(g)
g.has_friend(p)
r.has_hobby("rings")
Person.all_with_friends(p).each do |person|
  puts "#{person.name} is friends with #{p.name}"
end
Person.all_with_hobbies("rings").each do |person|
  puts "#{person.name} is into rings"
end

# in the code above, args[0] is the first argument, in our case, it is the p reference

# a note on why we can just do PEOPLE.find_all do |person| { person.send(attr).include?(args[0] } is because 
# find_all is a filter method.
# when you return 'true' on iterator (the code block if iterator, then next iterator will include the item (like a filter)
# so you don't need to wirte
#   if person.send(attr).include? (args[0])
#     yield person

4.4 class/module design and naming

all that matters to object is whether a given method exists, not what class or module the method's definition is in.


4.4.1. Mix-ins and/or inheritance
 
#a design choice, the mix-in is more a language level composition (functionality) and the inheritance is more a is-a relationship (the inheritance)
# check below an alternative design with inheritance.

class Stack
  attr_reader :stack

  def initialize
    @stack = []
  end

  def add_to_stack(obj)
    @stack.push(obj)
  end

  def take_from_stack
    @stack.pop
  end
end

class Suitcase
end

class CargoHold < Stack
  def load_and_report(obj)
    print "Loading object "
    puts obj.object_id
    add_to_stack(obj)
  end
  def unload
    take_from_stack
  end
end

# design choice
# two consideration to bear in mind:
#   Modules don't have instance
#   A class have only one superclass, but it can mix in as many modules as it wants.


4.4.2 Nesting Modules and classes

# *** very important, ruby also has nesting modules and classes, but unlike the Python code which has 
# nesting function, and nesting classes, ruby does not allow you to nesting module/classes inside a function

module Tools
  class Hammer
  end
end

# to create the inner classes, you might do the following (while python may not allow you to refer to the inner classes/modules.

h = Tools::Hammer.new


4.5. summary 


5. The default object (self), scope, and visibility

in this chapter:

¦ The role of the current or default object, self
¦ Scoping rules for local, global, and class variables
¦ Constant lookup and visibility
¦ Method access rules

two major aspect of the ruby programming will be covered in this chapter, that are:


5.1 Understanding self, the current/default object


the default object, or current object, accessible to you 


5.1.1.who gets to be self, and where.? there is a table showing which is condition

the table is as follow. 

Context Example Which object is self?

Context                      Example                    which object is self?

Top level of program    Any code of their block           Main(built-in top level default object)
Class definition       Class C                               the class object c
                        self
module definition     Module M                            the module object M
                        self
Method definition    1.Top level (outside any definition)   whatever object is self when 
                         def method_name                     the method is called, private methods to 
						    self                             to all objects
                    2. instance method definition in module  any instance of C, responding to mehtod_name
					   module M
					      def method_name
						    self
				    3. instance method definition in module  I.indiviaul object extended by M
					   module M                              II.Instance of class that mixes in M
					     def method_name
						    self
                   4. singleton method on a specific         obj
				   object
				       def obj.method_name
					     self

						 

the default main (self)

ruby -e "puts self"

# to get hold of top-level self, then it 
m = self

5.1.2. Self inside class, module, and method definitions

class C
  puts "Just started class C:"
  puts self
  module M
    puts "Nested module C::M:"
    puts self
  end
  puts "Back in the outer level of C:"
  puts self
end

5.1.2 Self in instance method definition

to rig a method to show youself as it runs.

class C
  def x
    puts "Class C, method x:"
    puts self
  end
end
c = C.new
c.x
puts "That was a call to x by: #{c}"


# and the self in the single object

obj = Object.new
def obj.show_me
  puts "Inside singleton method show_me of #{self}" # you cannot just do #{obj} becase??
end
obj.show_me
puts "back from the call to show meby ${obj}"

# class method, the singleton method attached to a class
class C
  def C.x # or you can just write "self.x" because self in the class scope is the "C"
    puts "Class method of class c"
	puts "self: #{self}"
  end
end

# prefer to write as "self.x" because that can gives  you the advantage when you rename class names.
# e.g. 
class C
  def self.x
    puts "Methods name"
  end
end

class D < C
end

5.1.3 self as the default receive of message

# generally you can omit the self when it is necessary 

# some tips: 
# when method name conflict with variable names, you can use bareword e.g. 'talk' for the variable, and you can 
# use the 'self.talk()' for the method 


# some guidance on the dot operation
class C
  def C.no_dot
    puts "As long as self is C, you can call this method with no dot"
  end
  
  no_dot
end

C.no_dot


5.1.4 Resolving instance variables trough self

# this chapter will include some tips on how to resolve the scope of the variables, whether it is the class object scope or the 


5.2. Determing scope

#** instance variable are self-bound, rather than scope-bound..

we will discuss the global, local and class variables.

5.2.1 Global scope and global variables.

global vars has scope rules, and 
#*** BUILT_IN GlOBAL VARIABLES
$0: the startup file or the currently running program
$: contains the directory that make up the path Ruby searches.

#*** you can use the TIP
require "English" 

# to get english name for the global variables.

PROS and CONS

5.2.2 Local scope

Local Scope is basic layer of hte fabric of every Ruby program

#difference of one scope to another is the supply of the local scopes variables.

¦ The top level (outside of all definition blocks) has its own local scope.
¦ Every class or module definition block (class, module) has its own local scope,
even nested class/module definition blocks.
¦ Every method definition (def) has its own local scope; more precisely, every call
to a method generates a new local scope, with all local variables reset to an
undefined state


class C
  a = 5
  module M
    a = 4
    module N
      a = 3
      class D
        a = 2
        def show_a
          a = 1
          puts a
        end
        puts a       #1
      end
      puts a         #2
    end
    puts a           #3
  end
  puts a             #4
end

d = C::M::N::D.new
d.show_a 

# the output would be 2,3,4,5,1


5.2.3 The interaction between local scope and self

when you start a new block, (dyanmically) you create a new scope. here is what you might get 

class C
  def x(value_for_a,recurse=false)
    print "Here's the inspect-string for 'self':"
    p self
    a = value_for_a
    puts "And here's a:"
    puts a
    if recurse
      puts "Recursing by calling myself..."
      x("Second value for a")
      puts "Back after recursion; here's a:"
      puts a
    end
  end
end

c = C.new
c.x("First value for a", true)

# so every call to x generates a new local scope,  even though self doesn't change

5.2.4 scope and resolution of constants
constants lookup: the process of resolving a constant identifier, finding the right match for it - bears a close resemblance to searching a filesystem.

module M
  Class C
    class D
	  moudle N
	    X = 1
      end
	end
  end
end

# as you can see, the resolution is done via relative path


FORCING AN ABSOLUTE CONSTANT PATH

class Violin
  class String
    ..
  end
  def initialize()
    @e = String.new("E")
  end
end


# it resolve to however, if you want to resolve to the global String object, then you can do 
# starting global root suffix 
#   ::String.new(maker + ", " + date)


5.2.5 Class variable syntax, scope and visibility

@@var


#**NOTE: 
#  CLASS VARIABLE ARE NOT CLASS SCOPED, RATHER, IT IS CLASS-HIERARCHY SCOPED. except sometimes.
# CLASS VARIABLES ACROSS CLASSES AND INSTANCES
# visibility to a class and its instances, and to no one else.


class Car 
  @@makes = []
  @@cars = {} 
  @@total_count = 0 

  attr_reader :make

  def self.total_count
    @@total_count 
  end 

  def self.add_make(make)
    unless @@makes.include?(make) 
      @@makes << make 
      @@cars[make] = 0 
    end 
  end 

  def initialize(make) 
    if @@makes.include?(make) 
      puts "Creating a new #{make}!" 
      @make = make
      @@cars[make] += 1
      @@total_count += 1 
    else 
      raise "No such make: #{make}."
    end 
  end 

  def make_mates
    @@cars[self.make] 
  end 
end 

#* CLASS variables and the class hierarchy

class Parent
  @@value = 100
end

class Child < Parent
  @@value = 200
end

class Parent
  puts @@value
end

#* a note on the class variables, DO NOT OVERUSE IT

# there are a principle that can help you handle the 
# situation when the class variables is required
# MAINTAINING PER-CLASS STATE WITH INSTANCE VARIABLES OF CLASS OBJECTS

class Car 
  @@makes = [] 
  @@cars = {} 

  attr_reader :make 

  def self.total_count  # do not use Car.total_count, because self is a scope based reference
    @total_count ||= 0
  end 

  def self.total_count=(n) # do not use Car.total_count= because self is a scope based reference
    @total_count = n
  end 

  def self.add_make(make) 
    unless @@makes.include?(make) 
      @@makes << make 
      @@cars[make] = 0 
    end 
  end 

  def initialize(make) 
    if @@makes.include?(make) 
      puts "Creating a new #{make}!" 
      @make = make 
      @@cars[make] += 1 
      self.class.total_count += 1
    else 
      raise "No such make: #{make}." 
    end 
  end 

  def make_mates 
    @@cars[self.make] 
  end 
end 

class Hybrid < Car
end

Car.add_make("Honda")
Car.add_make("Ford")
h3 = Hybrid.new("Honda")
h2 = Hybrid.new("Ford")

puts "There are #{Hybrid.total_count} hybrids on the road!"


5.3. Deploying method-access rules.

this guard which object can send which method to an object

5.3.1 Private methods

class Cake
  def initialize(batter)
    @batter = batter
    @baked = true
  end
end

class Egg
end

class Flour
end

class Baker
  def bake_cake
    @batter = []
    pour_flour
    add_egg
    stir_batter
    return Cake.new(@batter)
  end

  def pour_flour
    @batter.push(Flour.new)
  end

  def add_egg
    @batter.push(Egg.new)
  end

  def stir_batter
  end

  private :pour_flour, :add_egg, :stir_batter

end

b = Baker.new
b.add_egg  # this is not allowed 

# the key here is the private modifier (comparing to the python code where you can hide what you want to hide in the nested function

#** Private seter (=) methods

#the key to the access rule is the "self" accessing rule - a.k.a "No explicit receiver", so that suppose a field is "private :field"
# then self.field is accessible, but obj.field is not allowed 

# e.g of the private setter (=) methods is as follow

class Dog 
  attr_reader  :age, :dog_years
  def dog_years=(years)
    @dog_year = years
  end
  def age=(years)
    @age = years
	self.dog_years = years * 7
  end
  private :dog_years=
end

rover = Dog.new
rover.age = 10
puts "Rover is #{rover.dog_years} in dog years."

dog = self
dog.dog_years = years * 7 # you cannot accesss the private setter

5.3.2 Protected methods

only instance of the class X or the ancestor or descendant class of x's class (remember, this include both the ancestor and the descendant)

class C 
  def initialize(n) 
    @n = n 
  end 

  def n 
    @n 
  end 

  def compare(c) 
    if c.n > n #1 
      puts "The other object's n is bigger." 
    else 
      puts "The other object's n is the same or smaller." 
    end 
  end 

  protected :n 
end 

c1 = C.new(100) 
c2 = C.new(101) 
c1.compare(c2) 

5.4.1 Defining a top-level method
method defined at the top level is by default a private method 

def talk
  puts "Hello"
end

which is equivalent to the following 

class Object
  private
  def talk
    puts "Hello"
  end
end

# Defining private instance methods of Object has some interesting implications
#    First, these methods not only can but must be called in bareword style. call on "self' and with explicit style
#    second, private instance methods of Object can be called from anywhere in your code, because Object lies in the method lookup path of every class


def talk
  puts "Hello"
end
puts "Trying 'talk' with no receiver..."
talk
puts "Trying 'talk' with an explicit receiver..."
obj = Object.new  
obj.talk  # this will fail, because it is like calling a private method with a explicit receiver


5.4.2 Predefiend (built-in) top-level methods

puts "hello"

# to get all the methods , running this:
$ ruby -e 'print Kernel.private_instance_methods(false).sort'


6. Control-flow techniques

In this chapter
¦ Conditional execution
¦ Loops and looping techniques
¦ Iterators
¦ Exceptions and error handling

the following will be discussed

¦ Conditional execution—Execution depends on the truth of an expression.
¦ Looping—A single segment of code is executed repeatedly.
¦ Iteration—A call to a method is supplemented with a segment of code that the method can call one or more times during its own execution.
¦ Exceptions—Error conditions are handled by special control-flow rules.

6.1 Conditional code execution

the most canonical

if condition
  # code here, executed if condition is true
end

you can do that in a single line

if x > 10 then puts x end


semicolon can also be used
if x > 10; puts x; end


if-else-elsif


print "Enter an integer: "
n = gets.to_i
if n > 0
  puts "Your number is positive."
elsif n < 0
  puts "Your number is negative."
else
  puts "Your number is zero."
end



negating:

both the not and ! can be used as the negating operator

e.g.

if not (x == 1)
if !(x == 1)

this is OK:

if not x == 1
if (!x) = 1


unless keyword

x = 1

unless x > 100
   puts "Small number!"
else
  puts "Big number!"
end


CONDITIONAL MODIFIERS

you can start by the conditional modifiers

puts "Big number!" if x > 100

whichi equited

if x > 100
  puts "Big number!"
end

ASSIGNMNET SYNTAX IN CONDITION BODIES AND TESTS

if x = 1
  y = 2
end


local variable assignment in a conditional body: 
which is quite a bit different from the python rules, only when a variable has been initialized, can you be able to access it..

the assignment test is useful when you are dealing with regular expresions

name = "David A. Black"
if m = /la/.match(name)
  puts "Found a match!"
  print "Here's the unmatched start of the string: "
  puts m.pre_match
  print "Here's the unmatched end of the string: "
  puts m.post_match
else
  puts "No match"
end


6.1.3 Case statement

when-case-else statement

print "Exit the program? (yes or no): "
answer = gets.chomp
case answer                                                    #1
when "yes"                                                     #2
  puts "Good-bye!"
  exit
when "no"
  puts "OK, we'll continue"
else                                                            #3
  puts "That's an unknown answer -- assuming you meant 'no'"
end                   

puts "Continuing with program...."
# etc.

more than one possible values to the when clause


6.1.4 HOW when WORKS

the case equality operator called "==="

NOTE: you might want to find out might be exactly difference between the "==" and the "===" operator.


PROGRAMMING OBJECTS CASE STATEMENT BEHAVIOR

class Ticket
  attr_accessor :venue, :date
  def initialize(venue, date)
    self.venue = venue
    self.date = date
  end

  def ===(other_ticket)
#1
    self.venue == other_ticket.venue
  end
end

ticket1 = Ticket.new("Town Hall", "07/08/06")
ticket2 = Ticket.new("Conference Center", "07/08/06")
ticket3 = Ticket.new("Town Hall", "08/09/06")

puts "ticket1 is for an event at: #{ticket1.venue}."

case ticket1    
  when ticket2
#2
    puts "Same location as ticket2!"
  when ticket3
#3
    puts "Same location as ticket3!"
  else
    puts "No match"
end

THE SIMPLE CASE TRUTH TEST

this can be very useful when you have one statement to return multiple possbile values. 

puts case
	when user.first_name == "David", user.last_name == "Black"
	  "You might be David Black."
	when Time.now.wday == 5
	  "You're not David Black, but at least it's Friday!"
	else
	  "You're not David Black, and it's not Friday."
	end


6.2 Repeating actions with loops

you can loop while a given condition is true; simple do the following 


loop { puts "Looping forever!" }
loop do
  puts "Looping forever!"
end

well, you can contrl the loop as follow 

n = 1
loop do
  n = n + 1
  break if n > 9
end

or the next one (there is no continue in ruby)
n = 1
  loop do
  n = n + 1
  next unless n == 10
  break
end

loop with while 

n = 1
while n < 11
	puts n
	n = n + 1
end
puts "Done!"

loop with until.


n = 1
until n > 10
	puts n
	n = n + 1
end

WHILE AND UNTIL MODIFIERS

n = 1
n = n + 1 until n == 10
puts "We've reached 10!"


6.2.3 LOOPING BASED ON A LIST OF VALUES.

celsius = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
puts "Celsius\tFahrenheit"
for c in celsius
  puts "c\t#{Temperature.c2f(c)}"
end

6.3. Iterators and code blocks

answer is that loop is an iterator. An iterator is a Ruby method that has an extra
ingredient in its calling syntax: it expects you to provide it with a code block.

Iteration, home-style

def my_loop 
  while true
    yield
  end
end

or you can write as follow.. 


def my_loop
  yield while true
end


6.3.3 the anatomy of a method call


¦ A receiver object or variable (usually optional, defaulting to self)
¦ A dot (required if there’s an explicit receiver; disallowed otherwise)
¦ A method name (required)
¦ An argument list (optional; defaults to ())
¦ A code block (optional; no default)


6.3.4 Curly braces vs d_o /end in code block styntax


array = [1, 2, 3]

array.map { |n| n * 10 }

array.map {n| n * 10 }

# the puts will ignore the code block
puts array.map do |n| n * 10 end


6.3.5 Implementing times

class Integer
  def my_times
    c = 0
    until c == self
      yield(c)     # yield something, you can yield more than one values. 
      c += 1
    end
    self  # return something in a iterator
  end
end


6.3.6 The importance of being each


array = [1,2,3,4,5]
array.each {|e| puts "The block just got handed #{e}." }


one of the implementation is as follow

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

6.3.7 Fom each to Map 

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


and you can building on top of EACH 
class Array 
    # Put the definition of my_each here
  def my_map
    acc = []
    my_each {|e| acc << yield(e) }
    acc
  end
end


6.3.8  Block parameter and variables semantics

you have to watch for the scope of the local varaible.


the rules are 

1. in the code block, you can still access the outside local variable
2. bound variable (or a.k.a. ) get a new value each iteration
3. you can have "local" varaible semantic

def block_local_variable
  x = "Original x!"
  3.times do |i;x|
    x = i
    puts "x in the block is now #{x}"
  end
  puts "x after the block ended is #{x}"
end


6.4. Error handlign and exceptions

before the code is run

$ ruby -cw filename.rb

6.4.1 Raising and rescuing exceptions

TO see exception in action, try dividing by zero:


common exception and how to raise them

RuntimeError              raise
NoMethodError            a = object.new
                         a.some_unknown_method_name
NameError                a = some_random_identifier
IOError                  STDIN.puts("Dont'write to STDIN!")
Errno::error             File.open(-12)
TypeError                a = 3 + "can't add a string to a number"
ArgumentError            def m(x); end; m(1,2,3,4,5)


6.4.2. the rescue keyword to the rescue!

print "Enter a number: "
n = gets.to_i
begin
  result = 100 / n
rescue
  puts "Your number didn't work. Was it zero???"
  exit
end
puts "100/#{n} is #{result}"


you can catch on exact type of exception that you specified

rescue ZeroDivisionError

you can use the rescue inside methods code blocks

def open_user_file
  print "File to open:" 
  filename = gets.chomp
  fh = File.open(filename)
  yield fh
  fh.close
  rescue
    puts "Couldn't open your file!"
end

and you can be more fine-grained, such as 

def open_user_file
  print "File to open: "
  filename = gets.chomp
  begin
    fh = File.open(filename)
  rescue
    puts "Couldn't open your file!"
    return
  end
  yield fh
  fh.close
end


6.4.3. Raising exceptions explicitly


def fussy_method(x)
  raise ArgumentError, "I need a number under 10" unless x < 10
end
  fussy_method(20)

begin
  fussy_method(20)
rescue ArgumentError
  puts "That was not an acceptable number!"
end


also, though not what I would prefere, you can let the system to construct the runtime Exception to raise

raise "Problem!"
raise RuntimeError, "Problem!"


6.4.4 Capturing an exception in a rescue clause

begin 
  fussy_method(20)
rescue ArgumentError => e
  puts "That was not an acceptable number!"
  puts "Here's the backtrace for this exception"
  puts e.backtrace
  puts "Adn here's the exception object's message"
  puts e.message
end

# in reality, the instance rather the class itself is raised., e.g is as follow. 


RE-RAISING AN EXCEPTION

begin 
  fh = File.open(filename)
rescue => e
  logfile.puts("User tried to open #{filename}, #{Time.now}")
  logfile.puts("Exception: #{e.message}")
  raise
end

6.4.5 The ensure clause 

the ensure is like the finally block that will execute exactly once whatever the exception happens or not 


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
line_from_file("6_4_5EnsureClause.rb", "hello")

we will have another chapter that tells the more advanced way to ensure a resource is closed properly.


6.4.6 Creating your own exception class

class MyNewException < Exception

end



class InvalidLineError < StandardError

end


def line_from_file(filename, pattern)
  fh = File.open(filename)
  line = fh.gets
  raise InvalidLineError unless line.include?(pattern)
  return line
  rescue InvalidLineError
    puts "Invalid line!"
    raise
  ensure
    fh.close
end


7. Built-in clases and modules.

:  strings, arrays, files, and so forth

¦ In this chapter
¦ Literal object constructors
¦ Syntactic sugar
¦ "Dangerous" an_d/or destructive methods
¦ The to_* family of conversion methods
¦ Boolean states and objects, and nil
¦ Object-comparison techniques
¦ Runtime inspection of objects’ capabilities

7.1 Ruby’s literal constructors


String  "new string" | 'new string'
Symbol :symbol, :"symbol with spaces"

Array   [1,2, 3,4,5]
Hash       {"New York" => "NY" , "Oregon" => "OR"}
Range    0..9, 0...9
Regexp   /([a-z]+)/
Proc   ->(x, y) { x * y}

7.2 Recurrent syntactic sugar

7.2.1 Defining operators by defining methods


class Account
  attr_accessor :balance
  def initialize(amount=0)
    self.balance = amount
   end
  def +(x)
    self.balance += x
  end
  def -(x)
    self.balance -= x
  end
  def to_s
    balance.to_s
  end
end

acc = Account.new(20)
acc -= 5
puts acc

TYPE OF OPERATORS THAT SHALL BE SUPPORTED

Arithmetic method/operators
Get/set/append data
Comparison method/operators
Case equality operator
Bit-wise operators



7.2.2 Customizing unary operators

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

you can as well define the operator "not" ! 

class Banner
  def !
    reverse
  end
end


7.3 Bang(!) methods and "danger"

bang method is treated no specially by the python code system, but it has some convention that has been imposed by them...

7.3.1 Destructive (receiver-changing) effects as danger

str = "Hello"
str.upcase
str
str.upcase!
str


7.3.2 Destructive  and "danger" vary independently 

some guidelines on the methods pairs

DON'T USE ! EXCEPT IN M/M! METHOD PAIRS'
DON’T EQUATE ! NOTATION WITH DESTRUCTIVE BEHAVIOR, OR VICE VERSA


7.4 Built-in and custom to_* (conversion) methods

to_s method is called by certain method to print the string representation of one object.

obj = Object.new

puts obj

def obj.to_s
  "I'm an object!"
end

puts obj


THE inspect, to_s, AND eigen 

puts object
puts object.to_s
puts object.inspect



BORN TO BE OVERRIDEN: inspect

e.g. the regular expression, with to_s, it returns the parsed regular expression and with inspect, it returns what ias been input from the command line.

>> re = /\(\d{3}\) \d{3}-\d{4}/
=> /\(\d{3}\) \d{3}-\d{4}/
>> puts re
(?-mix:\(\d{3}\) \d{3}-\d{4})
=> nil
>> puts re.inspect
/\(\d{3}\) \d{3}-\d{4}/
=> nil

inspect is used when you call p


DISPLAY method 

"hello".display


how and when the display method shall be used

fh = File.open("/tmp/display.out", "w")
"hello".display(fh)
fh.close


# is there a with statment as in Python?


begin
  fh = File.open("c:\temp\displayout.out", "w")
  "hell".display(fh)
  fh.close
  puts(File.read('c:\temp\displayout.out')
rescue
  if not fh == nil
    fh.close()
  end
end

7.4.2 ARRAY CONVERSION WITH to_a and * operator
* The * operator (pronounced “star,” “unarray,”  or, among the whimsically inclined, “splat”

the star turns any array, or any object that responds to to_a, into
the equivalent of a bare list.

what is a bare-list 
[1,2,3,4,5] 

notation lying between the brackets isn’t, itself, an
array; it’s a list, and the array is constructed from the list, thanks to the brackets

e.g.


array = [1,2,3,4,5]
[*array]

you can use * operator to turn a array to a list, which can be used in the following example.


def combine_names(first_name, last_name)
  first_name + " " + last_name
end

names = ["David", "Black"]
puts combine_names(*names)

NOTE : this can be very useful and you can analogy this to the python's * operator, which used to indicate a list arguments, and ** to means a dictionary arguments' 

7.4.3


for non conforming conversion, 0 will be returned and stop processing any further, comparing that to C#'s implementatoin'
"hello".to_i
"1.23hello".to_f

but if you want to do some strict conversion, you 'd better to use the integer or float function'                


7.4.4 The role-playing to_* methods


STRING role-playing with to_str

to_s used when you puts the string
to_str used when you want the obejct to be a string

"hello" + 10  # this will fail , and there is where the string will kicks in


class Person 
  attr_accessor :name
  
  def to_str
    name
  end
end
david = Person.new

david.name = "David"

puts "david is named" + david + "."

ARRAY ROLE-PLAYING WITH to_ary

object can masquerade as an array 

to_ary

class Peson
  attr_accessor :name, :age, :email
  
  def to_ary
    [name, age, email]
  end
end

david = Peson.new 
david.name = "David"
david.age = 49
david.email = "david@wherever"
array = []
array.concat(david)
p array


7.5. Boolean state, boolean object, and nil

true and false are object, 


true.class
false.class

some boolean values :

class definition: empty one is false
class definition: return the last expression
method definition : is false, whatever values return in the method definition


TRUE/FALSE AND true/false: STATES VS. VALUES


some mantra to call: 
  TRUE /FALSE is the state.

true/false is the object. 

every object has a boolean value , which gives you the boolean truth, however, it is not mean the boolean truth is true/false object, true/false object itself returns boolean truth..


7.5.3. the special object nil


# which is the same as the None in python

nil.class

the class of nil is "NilClass"


nil denote the absense of anything....

puts @x
["one", "two", "three"][9]



>> ["one","two","three"][9]
=> nil
>> nil.to_s
=> ""
>> nil.to_i
=> 0
>> nil.object_id
=> 4


SOME INTERESTING object_ids


false.object_id = 0
0.object_id = 1
true.object_id = 2
1.object_id = 3
nil.object_id = 4

boolean provide segue to next topic, the object comparison..

7.6 Comparing two objects


normally you can mix in the module called "Comparable"


7.6.1 Equality tests

following is the equality test

>> a = Object.new
=> #<Object:0x401c653c>
>> b = Object.new
=> #<Object:0x401c4bd8>
>> a == a
=> true
>> a == b
=> false
>> a != b
=> true
>> a.eql?(a)
=> true
>> a.eql?(b)
=> false
>> a.equal?(a)
=> true
>> a.equal?(b)
=> false


If you want objects of class MyClas to have the full suite of comparison methods, all you have to do is the following

1 Mix a module called Comparable (which comes with Ruby) into MyClass.
2 Define a comparison method with the name <=> as an instance method in MyClass

The comparison method <=> (usually called the spaceship operator or spaceship method)
is the heart of the matter


SPACESHIP METHOD, SPACESHIP METHOD, SPACESHIP METHOD.


an e.g.

class Bid
  include Comparable
  attr_accessor :estimate
  
  def <=> (other_bid)
    if self.estimate < other_bid.estimate
	  -1
	elsif self.estimate > other_bid.estimate
	  1
	else
	  0
	end
  end
end


or an even simpler implementation is

def <=> (other_bid)
  self.estimate <=> other_bid.estimate
end

# the  test code below


bid1 = Bid.new
bid2 = Bid.new
bid1.estimate = 100
bid2.estimate = 105
bid1 < bid2

7.7 Inspecting object capability

inspection and reflection refer, collectively, to the various ways in which you can get Ruby objects to tell you about 

7.7.1 Listing an object's methods'.


object has an methods. 

Class object also has a methods method

"I am a String object".methods
String.method.sort

conveniently, you can just query for the singleton methods of a single object

str.signleton_methods



str = "Another plain old string."
module StringExtras
  def shout
    self.upcase + "!!!"
  end
end

class String
  include StringExtras
end

str.methods.include?(:shout)

7.7.2 Querying class and module objects

you can query on the instance methods on a Class object


String.instance_methods.sort

Enumerable.instance_methods.sort


7.7.3 filtered and selected methods list

to show methods just in that class. 

String.instance_methods(false).sort

other methods listing methods

obj.private_methods
obj.public_methods
obj.protected_methods
obj.singleton_methods


and even more combination

¦ MyClass.private_instance_methods
¦ MyClass.protected_instance_methods
¦ MyClass.public_instance_methods

public_instance_methods is the same as the instance_methods


8. Strings, Symbols, and other scalar objects

In this chapter
¦ String object creation and manipulation
¦ Methods for transforming strings
¦ Symbol semantics
¦ String/symbol comparison
¦ Integers and floats
¦ Time and date objects



8.1 Working with Strings

Strings and symbols are deeply different from each other, but they’re similar enough in their
shared capacity to represent text that they merit being discussed in the same chapter


string interpolation details

puts "Backslashes (\\) have to be escaped in double quotes."
puts 'You can just type \ once in a single quoted string.'
puts "But whichever type of quotation mark you use..."
puts "...you have to escape its quotation symbol, such as \"."
puts 'That applies to \' in single-quoted strings too.'
puts 'Backslash-n just looks like \n between single quotes.'
puts "But it means newline\nin a double-quoted string."
puts 'Same with \t, which comes out as \t with single quotes...'
puts "...but inserts a tab character:\tinside double quotes."
puts "You can escape the backslash to get \\n and \\t with double quotes."


other quoting mechanisms

puts %q{You needn't escape apostrophes when using %q.}


# %q for single quote and %Q for double quote
%q-A string-
%Q/Another string/
%[Yet another string]

If you’re using right/left matching braces and Ruby sees a left-hand one inside the
string, it assumes that the brace is part of the string and looks for a matching righthand
one. you have to do escape if you want to use a unmatched one


%Q[I can put [] in here unescaped.]
%q(I have to escape \( if I use it alone in here.)
%Q(And the same goes for \).)


one note though:
  irb doesn’t play well with some of this syntax
  
  
"HERE" DOCUMENTS

a "here" document, or here-doc, is a string, usually multiline string. that ofetn takes the form of a template or a set of date lines

>> text = <<EOM
This is the first line of text.
This is the second line.
Now we're done.
EOM


to switch off the FLUSH-LEFT requirement

>> text = <<-EOM
The EOM doesn't have to be flush left!
EOM
=> "The EOM doesn't have to be flush left!\n"


you can use the Here document in a literal constructor , here is an example where we put a string into an array .



a = <<EOM.to_i * 10
5
EOM
puts a



array = [1,2,3,<<EOM, 4]
This is the here-doc!
It becomes array[3].
EOM

p array


or even more esoteric, here is what you might getting 

array = [1,2,3,<<EOM, <<LAST]
This is the here-doc!
It becomes array[3].
EOM
And this is the array[4]
LAST

p array 

8.1.2 Basic string manipulation

Basic in this context means manipulating the object at the lowest levels. Retrieving and setting sbustrings, and combining strings with each other.


GETTINGS AND SETTINGS SUBSTRINGS

>> string = "Ruby is a cool language."
=> "Ruby is a cool language."
>> string[5]
=> "i"
>> string[-12]
=> "o"
>> string[5,10]
=> "is a cool "


# stirng object can also expect a range operator, and also, it can accept negative number, to indicate some backward operation.

>> string[7..14]
=> " a cool "
>> string[-12..-3]
=> "ol languag"


# while if you pass some string operation, you are looking for the index of the operator

string["cool lang"] # if not found, then nil shall be returned, if found it is returned. (why not returns the index?)
string["very cool lang"]

# you can do the similar things to the regular expressions

string[/c[ol ]+/]

# [] is aliased with slice.. well, you have a slice! methods as well

string.slice!("cool ")  # means slicing literally 
string

# the replace methods 
string["cool"] = "great"
string[-1] = "!"
string[-9..-1] = "thing to learn!"

# you try part of a string that does not exit, - a tool high or too-low numeric index, or a string or regular expression that does not match the string - you get a fatal error.



COMBINNING STRINGS
"a" + "b"
"a" + "b" + "c"

APPENDING STTRINGS

str = "H1"
str << "there"


STRING COMBINATION VIA INTERPOLATION
str = "Hi"

"#{str} there."


anything is allowed in the interpolation

"My name is #{class Person
               attr_accessor :name
			 end
			 d = Person.new
			 d.name = "David"
			 d.name
			 }."
"

you can define the to_s which shall be called by the string interpolation

class Person
  attr_accessor :name
  def to_s
    name
  end
end

david = Person.new
david.name = "David"

"hello,#{david}"

8.1.3 Querying strings


BOOLEAN STRING QUERIES

include?

  string.include?("Ruby")

  string.incldue?("Engligh")

start_with?  
end_with?
  #some tips, if you are working with Pascal, camcel then it should be startsWith or endsWith, notice the small 's' in-between'
  string.start_with?("Ruby")
  string.end_with?("!!!")
  
string.empty?

"".empty?
CONTENT QUERIES

string.size
  string.size 
string.count

  string.count("g-m")  # you can pass in a range (why not directly passing a regular expression?
  string.count('aey')
  
  You can combine the specification syntaxes and even provide more than one arguments:


  string.count("ag-m")
  string.count("ag-m")

  >_ anchor style (assert style)
  string.count("ag-m", "^")
  string.count("ag-m")
  
  you can do some reverse look up ,just like this:
  
  string.index("cool")
  string.index("l")
  
string.index
  
  string.index("cool")
  string.index("1")
  stirng.rindex("1")
  
  although strings are  made up of characters, Ruby has no separate character class. 

   string.ord method 

the string.Ord method will take single string object and return the ordinal of the single string object (the character) 



  
-----
BELOW ARE USED IN THE MARKDOWN SYNTAX
-----

### 8.1.4 String comparison and ordering

the **String** class mixed in the __Comparable__ method and define a `<=>` mehtod. 

```
>> "a" <=> "b"
=> -1
>> "b" > "a"
=> true
>> "a" > "A"
=> true
>> "." > ","
=> true
```

COMPARING TWO STRINGS FOR EQUALITY

```
>>> "string" == "string"
=> true
>>> "String" == "house"
=> false
```

string#eql? almost the same as the == operator, and the equals? method compare the object identity equality.


```
>> "a" == "a"
=> true
>> "a".equal?("a")
=> false
>> "a".equal?(100)
=> false
```


### String Tranformation

CASE TRANSFORMATION

```
>> string = "David A. Black"
=> "David A. Black"
>> string.upcase
=> "DAVID A. BLACK"
>> string.downcase
=> "david a. black"
>> string.swapcase
=> "dAVID a. bLACK"
```


#### CAPITALIZE
```
string = "david"
string.capitalize
```

FORMATTING TRANSFORMATIONS

formatting transformation is part of the content transformation.

#### rjust and ljust

```
>> string = "David A. Black"
=> "David A. Black"
>> string.rjust(25)
=> " David A. Black"
>> string.ljust(25)
=> "David A. Black "
```

well, you can tell a different padding 


```
>> string.rjust(25,'.')
=> "...........David A. Black"
>> string.rjust(25,'><')
=> "><><><><><>David A. Black"
```

    well, you can see, that not just single padding can be used, a pattern can be used. 


#### center

`"the Middle".center(20, "*")`


#### CONTENT TRANSFORMATION

##### Chop and Chomp

chop will chop the last character, no matter it is a space or not
"David A. Black".chop

chomp will chomp out the empty ones.

`"David A. Black\n".chomp`

well the target of the chomp can be specified.

"David A. Black".chomp('ck')

A complete example is as follow. 

```
>> "David A. Black".chop
=> "David A. Blac"
>> "David A. Black\n".chomp
=> "David A. Black"
>> "David A. Black".chomp('ck')
=> "David A. Bla"
```

##### clear

clear as the name says, clear a string.

##### replace

```
>> string = "(to be named later)"
=> "(to be named later)"
>> string.replace("David A. Black")
=> "David A. Black"
```

#### delete and count

need to mention that the delete and count method support operation with regular expression syntax.

```
>> "David A. Black".delete("^abc")
=> "aac"
```

#### crypt

the _string.crypt_ method is very similar to the the __crypt(3)__ library function. 

```
>> "David A. Black".crypt("34")
=> "347OEY.7YRmio"
```

#### succ 
    NOTE: there is no prev method that as opposed to the succ methods.

the succ method is engineered specially to make sense.

```
>> "a".succ
=> "b"
>> "abc".succ
=> "abd"
```

### 8.1.6. String conversions

the conversion families take cares of convering string to other types, such as integer or floating point numbers.

e.g. you can do a conversion to a base 17 nubmer strings.

`"100".to_i(17)`

there are also special cases on the base 8 and base 16.. 

```
>> "100".oct
=> 64
>> "100".hex
=> 256
```

and below are exammple of the to_f, to_i which you might commonly see usual operators.

```
>> "1.2345".to_f
=> 1.2345
>> "Hello".to_s
=> "Hello"
>> "abcde".to_sym
=> :abcde
```

    NOTE above, there are methods which does the conversion not only to the numeric values, but also to the values of symbols and etc..

### 8.1.7 String encoding: a brief introduction

In this chapter, we will discuss the encoding intelligence and funtionalities to strings.

#### SETTING THE ENCODING OF THE SOURCE FILE

> HOWTO : get the encoding of the source file

```
puts __ENCODING__
US-ASCII
```

ruby can get the encoding from the current locale settings.

`LANG=en_US.iso885915 ruby -e 'puts __ENCODING__'`

it was supposed that when you put in the encoding directive, you should be able to get the correct character displayed.

```
# coding: UTF-8
Euros are designated with this symbol: €
```

however, that I have locally tested it out, that it is not well recognized by the ruby interpreter on the utf-8 character.


#### ENCODING OF INDIVIDUAL STRINGS

strings can tell you their encoding:
```
>> str = "Test string"
=> "Test string"
>> str.encoding
=> #<Encoding:US-ASCII>
```

encode a string with a different encoding, as long as the conversion fro the original encoding to the new one - the transcoding - is permitted.

`str.encode("UTF-8")`

there is a bang version, which is `encode!`; There is a encoding promotion logic, which are affect from the ASCII to ASCII-8, to UTF-8 and etc..

```
>> str = "Test string"
=> "Test string"
>> str.encoding
=> #<Encoding:US-ASCII>
>> str << ". Euro symbol: \u20AC"
=> "Test string. Euro symbol: ?"
>> str.encoding
=> #<Encoding:UTF-8>
```

## Symbols and their uses

symbols begin with a colon, :;

#### to_s, intern
you can convert a string to a symbol with the _to_s_ or the _intern_ methods.

```
>> "a".to_sym
=> :a
>> "Converting string to symbol with intern....".intern
=> :"Converting string to symbol with intern...."
```


### 8.2.1. The chief characteristics of symbols

#### IMMUTABLITY


#### UNIQUENESS
all symbols with the same symbol names are the same. 

```
>> :abc.object_id
=> 160488
>> :abc.object_id
=> 160488
```


#### 8.2.2 Symbols and identifiers

This code includes one _Symbol_ object (:x) and one local variable identifier(s)

`s=:x`

you can get all the symbols that the ruby interperter has kepts so fary, you can do the following.

`>>Symbol.all_symbols`

you can check for existence of one symbol from the symbol table as such...

`>> Symbol.all_symbols.include?(:x)`

### 8.2.3 Symbols in practise

normally the symbols are used in the following two categories

* SYMBOLS AS METHOD ARGUMENTS
* SYMBOLS AS HASH KEYS

#### SYMBOLS AS METHOD ARGUMENTS

```
attr_accessor :name
attr_reader :age
```

another example would be the _send_ method

`"abc".send(:upcase)`

however, you can also do the 
`"abc".send("upcase")`

> Consider allowing symbols or strings as method arguments
When you're writing a method that will taken an argument that could conceivably be a string or a symbol, it's often  nice to allow both.


#### SYMBOLS AS HASH KEYS

we already know that string can be mutable, so that they are not used internally in the hash implementation. (actually a copy of the string has been saves as the key to the hash). and the admonition is that if you want to work with string based key with hash, USE SYMBOLS.

```
>> d_hash = { :name => "David", :age => 49 }
=> {:name=>"David", :age=>49}
>> d_hash[:age]
=> 49
```

the reason can be summarized as with no exception of others (among others)
1. run faster
2. symbols looks good as hash keys.


**NOTE  the Ruby interpreter allows for a better way of special form of symbol representation in the hash-key position**

`hash = {:name => "David", :age => 49 } `

can be also be wrriten like this:

`hash = { name: "David", age: 49 }`


### 8.2.4 Strings and Symbols in Comparison

Symbols is increasingly string-like in successive veresions of ruby, That is not to say that they've shed their salient features.

```
>> Symbol.instance_methods(false).sort
=> [:<=>, :==, :===, :=~, :[], :capitalize, :casecmp, :downcase,
:empty?, :encoding, :id2name, :inspect, :intern, :length, :match, :next,
:size, :slice, :succ, :swapcase, :to_i, :to_proc, :to_s, :to_sym, :upcase]
```
underneath, symbols are more like integer than like strings. (the Symbol talbe is bascically an integer-based hash)

## 8.3 Numerical objects

we will check the following three operations

* round
* zero?
* chr

in the following example.

```
n = 99.6
m = n.round
puts m
x = 12
if x.zero?
puts "x is zero"
else
puts "x is not zero"
end
puts "The ASCII character equivalent of 97 is #{97.chr}"
```

### 8.3.1 Numeric classes


Numeric 
   Float
   Integer
      FixNum
      Bignum
     
### 8.3.2 Performing arithmetic operations

Numbers in Ruby behave as the rule of arithmetic and arithmetic notation lead you to expect. 

you can operate on numbers in non-decimal bases. Hexadecimal integers are indicated by a leading 0x

```
>> 0x12
=> 18
>> 0x1
```

and the base of the 8 is interpreted as octal (base eight):

```
>> 012
=> 10
>> 012 + 12
=> 22
```


you can do a conversion from the string to the proper numeric values such as integer and others.

```
"10".to_i(17)
"12345".to_i(13)
```

if you want to dig into the details, you will find that the operators are just methods calls.

```
>> 1.+(1)
=> 2
>> 12./(3)
=> 4
```


## 8.4 Times and dates

the extent and variety of the classes that represents times and/or dates,  and the class and instances methods available through those classes, can be bewildering.

```
>> require 'date'
=> true
>> Date.parse("April 24 1705").england.strftime("%B %d %Y")
=> "April 13 1705"
```

Times and dates are manipulated through three classses: Time, Date and DateTime. (For convenience, the instances of all of these classes can be referred to collectively as date/time objects.)
```
require 'date'
require 'time'
```

### 8.4.1 Instantiating date/time objects

#### CREATING DATE OBJECTS

you can get today's date with the Date.today constructor:

`>> Date.today`

Create a date through the use of _Date.new_ method.

```
>> puts Date.new(1959, 2, 1)
1959-02-01
```

It has default value, if not provided, will be default to **1**

You can get a new Date object from its string representation 

`>> puts Date.parse("2003/6/9")`

By default, the Ruby programming language will does the expanding of the century. however, it treat number from 69-99 and 0-68 differently .

```
>> puts Date.parse("03/6/9")
>> puts Date.parse("33/6/9")
>> puts Date.parse("77/6/9")
```

the Date.parse method is quite strong, and below is what might be understood by the Date.parse methods.

```
>> puts Date.parse("January 2 2009")
2009-01-02
>> puts Date.parse("Jan 2 2009")
2009-01-02
>> puts Date.parse("2 Jan 2009")
2009-01-02
>> puts Date.parse("2009/1/2")
2009-01-02
```

#### Creating TIME OBJECTS

You can create  a time object using any of several constructors: new (a.k.a now) , at, local, (a.k.a mktime), and parse...

```
>> Time.new
=> 2008-12-03 12:16:21 +0000
>> Time.at(100000000)
=> 1973-03-03 09:46:40 +0000
>> Time.mktime(2007,10,3,14,3,6)
=> 2007-10-03 14:03:06 +0100
>> require 'time'
=> true
>> Time.parse("March 22, 1985, 10:35 PM")
=> 1985-03-22 22:35:00 +0000
```

Be careful that you need to do a `require 'time'` in order ot use the Time.parse method.

#### CREATING DATETIME OBJECTS
DateTime is a subclass of Date, but its constructors are a little different thanks to some overrides and privatizing of methods.

```
>> puts DateTime.new (2009, 1, 2, 3, 4, 5)
2009-01-02T03:04:05+00:00
>> puts DateTime.now
2008-12-04T09:09:28+00:00
=> nil
>> puts DateTime.parse("October 23, 1973, 10:34 AM")
1973-10-23T10:34:00+00:00
```

DateTime also features the specialized _jd_ (Julian date), _commercial_, and _strptime_ constructors mentioned earlier in connection with the Date class.

### 8.4.2 Date/time query methods

```
dt = DateTime.now
dt.year
dt.hour
t = Time.now
t.month
t.sec
d = Date.today
d.day
```

there are also these types of query on method to determine the weeks of the day 

```
d.monday?
dt.thursday?
```
### 8.4.3 Date/time formatting methods


| Specifier |  Description |
| :-------- | :-------|
| %Y  | Year (four digits) |
| %y     |  Year (last two digits) |
| %b, %B      |    Short month, full month |
| %m  | Month (number) |
| %d     |   Day of month (Left-padded with zeros) |
| %e  |  Day of month (left-padded with zeros) |
| %a,%A  | Short day name, full day name |
| %H, %I     |  Hour(24-hour clock), hour (12-hour clock) |
| %M      |    Minute |
| %S      |    Second |
| %c      |    Equivalent to "%a %b %d %H:%M:%S %Y" |
| %x      |    Equivalent to "%m/%d/%y" |

    when you are dealing with the format, you have to bear into mind that some locale do entail different format to another.


```
>> t.strftime("Today is %x")
=> "Today is 01/17/06"
>> t.strftime("Otherwise known as %d-%b-%y")
=> "Otherwise known as 17-Jan-06"
>> t.strftime("Or even day %e of %B, %Y.")
=> "Or even day 17 of January, 2006."
>> t.strftime("The time is %H:%m.")
=> "The time is 17:01."
```
there are some precooked output formats for speciallied cases like RFC 2822 (email) 

```
>> Date.today.rfc2822
=> "Tue, 14 Jan 2014 00:00:00 +0000"
>> DateTime.now.httpdate
=> "Tue, 14 Jan 2014 06:07:56 GMT"
```

### 8.4.4 Date/time conversion methods

Time class has *to_date*, *to_datetime*
Date has *to_time* and *to_datetime*
DateTime has *to_time* and *to_date*

#### DATE/TIME ARITHMETIC

you can do arithmetic operations on the Date time ...

*Time* object let you do a second-wise operations.

```
>> t = Time.now
>> t - 20
>> t + 20
```

*Date and Datetime* objects interpret + and - as day-wise operations. and it also allow you to do the Month-wise operators.

```
dt =  DateTime.now
puts dt + 100
puts dt >> 3
puts dt << 10
```

there are also a _next_unit_ family that allow you to contorl the unit of the operations.

```
>> d = Date.today
=> #<Date: 2014-01-14 ((2456672j,0s,0n),+0s,2299161j)>
>> puts d.next
2014-01-15
>> puts d.next_year
2015-01-14
>> puts d.next_month(3)
2014-04-14
>> puts d.prev_day(10)
2014-01-04
```
Date and DateTime allows for some range operations.

```
>>d = Date.today 
next_week = d + 7 
>>d.upto(next_week) {|date| puts "#{date}  is a #{date.strftime("%A")}" }
2014-01-14  is a Tuesday
2014-01-15  is a Wednesday
2014-01-16  is a Thursday
2014-01-17  is a Friday
2014-01-18  is a Saturday
2014-01-19  is a Sunday
2014-01-20  is a Monday
2014-01-21  is a Tuesday
```


## 8.5 Summary 

In this chapter, you've seen the basic of the most commmon and important scalar objects in Ruby: strings, symbols, numeric objects and time/date objects. 

# 9. Collection and Container objects

what will be covered

* search through a collection
* sort collection for further processing or virtual presentation
* filter collection to include or exclude particular items

two other special types of collection will be discussed, they are _Range_ and _Set_.

Ruby represents collections of objects by putting inside _container_ objects. two built-in classes dominate the container-object landscape: _arrays_ and _hashes_. 

Hashes are called _associative arrays_ or _dictionary_ in other languages.

hashes exhibit a kind of “meta-index” property, based on the fact that they have a certain number of key/value pairs and that those pairs can be counted off consecutively.

```
hash = { "red" => "ruby", "white" => "diamond", "green" => "emerald" }
hash.each_with_index {|(key,value),i| puts "Pair #{i} is: #{key}/#{value}"
}
```


## 9.2 Collection handling with arrays

An array is an object whose job is to store other objects. Arrays are ordered collections;

Arrays are the bread-and-butter way to handle collections of objects.

## 9.2.1 Creating a new array 

with the following methods

* With the new method 
* With the literal array constructor (square brackets)
* With the top-level method called Array 
* With the special %w{...} notation

#### ARRAY#NEW

`a = Array.new`

```
>> Array.new(3)
=> [nil, nil, nil]
>> Array.new(3,"abc")
=> ["abc", "abc", "abc"]
```

you can pass a code block to Array new as the generator 

```
>> n = 0
=> 0
>> Array.new(3) { n += 1; n * 10 }
=> [10, 20, 30]
```

> NOTE: when you initialize with Array.new(3,"abc"), evey element are initialized to the same object, when you modify one, you are actually modify many...

#### THE LITERAL ARRAY CONSTRUCTOR: []

`a = [1,2,"three",4, []]`

you can nest the array to as many level as you like.

#### THE ARRAY METHOD

The third way to create an array is **Array** method. **Array** is a class name as well as a Method name.


The Array method creates an array from its single argument

internally the Array method t_a, example is as follow 

```
>> string = "A string"
=> "A string"
>> string.respond_to?(:to_ary)
=> false
>> string.respond_to?(:to_a)
=> false
>> Array(string)
=> ["A string"]
>> def string.to_a
>> split(//)
>> end
=> nil
>> Array(string)
=> ["A", " ", "s", "t", "r", "i", "n", "g"]
```

#### THE %w AND %W ARRAY CONSTRUCTORS

generate arrays from space-separated strings.

```
%w{ David A. Black }
=> ["David", "A.", "Black"]
```

to escape the space. do this :

```
>> %w{ David\ A.\ Black is a Rubyist. }
=> ["David A. Black", "is", "a", "Rubyist."]
```
if you want to have the duoble quoted string 

```
>> %W{ David is #{2008 - 1959} years old. }
=> ["David", "is", "49", "years", "old."]
```

9.2.2 Inserting, retrieving, and removing array elements

**[]=** insertion

```
a = []
a[0] = "first"
```

**[]** retrieving
```
a = [1,2,3,4,5]
p a[2]
```

#### SETTING OR GETTING MORE THAN ONE ARRAY ELEMENT AT A TIME

```
=> ["red", "orange", "yellow", "purple", "gray", "indigo", "violet"]
>> a[3,2]
=> ["purple", "gray"]
>> a[3,2] = "green", "blue"
=> ["green", "blue"]
>> a
=> ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]

```

becareful that you are not assigning an array but instead a _bare-list_ to `a[3,2]`

you can do with the **values_at** method. you can pass in a list of indexes in.

```
array = ["the", "dog", "ate", "the", "cat"]
articles = array.values_at(0,3)
p articles
```

#### SPECIAL METHODS FOR MANIPULATING THE BEGINNINGS AND ENDS OF ARRAYS

* unshift means prepend

```
a = [1,2,3,4]
a.unshift(0)
```

* push/<< means append
```
a = [1,2,3,4]
a.push(5)
a = [1,2,3,4]
a << 5
```

* shift to remove at head
```
shifted = a.shift
print "The shifted item: "
puts shifted
print "The new state of the array: "
p a
```
* pop to remove at end

```
a = [1,2,3,4,5]
print "The original array: "
p a
popped = a.pop
print "The popped item: "
puts popped
print "The new state of the array: "
p a
```

### 9.2.3 Combining arrays with other arrays

* concat to add one array to another 
```
>> [1,2,3].concat([4,5,6])
=> [1, 2, 3, 4, 5, 6]
```

* \+ create a temporary array with contents combined
```
>> a = [1,2,3]
=> [1, 2, 3]
>> b = a + [4,5,6]
=> [1, 2, 3, 4, 5, 6]
>> a
=> [1, 2, 3]
```

* replace to replace the contents (not the same as the assignment)

9.2.4 Array transformations

* flatten 
you can flatten a nested array by calling the flatten methods .

```
>> array = [1,2,[3,4,[5],[6,[7,8]]]]
=> [1, 2, [3, 4, [5], [6, [7, 8]]]]
>> array.flatten
=> [1, 2, 3, 4, 5, 6, 7, 8]
```

* **reverse** to reverse
`[1,2,3,4].reverse`

* **join** to join (string representation)

```
>> ["abc", "def", 123].join
=> "abcdef123"
```

join can accept one joiner.

```
>> ["abc", "def", 123].join(", ")
=> "abc, def, 123"
```

* **uniq** gives you a new array 

```
>> [1,2,3,1,4,3,5,1].uniq
=> [1, 2, 3, 4, 5]
```

* **compat** will remove all those *nil* element

```
>> zip_codes = ["06511", "08902", "08902", nil, "10027",
"08902", nil, "06511"]
=> ["06511", "08902", "08902", nil, "10027", "08902", nil, "06511"]
>> zip_codes.compact
=> ["06511", "08902", "08902", "10027", "08902", "06511"]
```

### Array querying

| Method names/sample call |  Meaning |
| :----------------------- | :---------------------------------|
| a.size (synonym: length) | Number of elements in the array |
| a.empty?    |  True if a is an empty array; false if it has any elements |
| a.include?(item)   |  True if the array includes items; false otherwise |
| a.count(item) | Number of occurrences of item in array |
| a.first(n=1)      |  First n elements of array |
| a.last(n=1) | Last n elements of array |


## 9.3 Hashes

```
state_hash = { "Connecticut" => "CT",
               "Delaware" => "DE", 
               "New Jersey" => "NJ",
               "Virginia" => "VA" }
print "Enter the name of a state: "
state = gets.chomp
abbr = state_hash[state]
puts "The abbreviation is #{abbr}."

```

### 9.3.1 Creating a new hash

* Literal hash construction

`h = {}`

* traditional **new** method 

`Hash.new`

* the **[]** method 

```
>> Hash["Connecticut", "CT", "Delaware", "DE" ]
=> {"Connecticut"=>"CT", "Delaware"=>"DE"}
```

9.3.2 Inserting, retrieving, and removing hash pairs

* Adding with the *[]=* method or the **store** method 

`state_hash["New York"] = "NY"`

`state_hash.store("New York", "NY")`

#### RETRIEVING VALUES FROM A HASH

* use the **[]** method or the **fetch** method 

`conn_abbrev = state_hash["Connecticut"]`

`conn_abbrev = state_hash.fetch("Connecticut")`


### 9.3.3 Specifying default hash values and behavior

*nil* are returned when key not exist in the hash.

```
>> h = Hash.new
=> {}
>> h["no such key!"]
=> nil
```

change to a different default value

```
>> h = Hash.new(0)
=> {}
>> h["no such key!"]
=> 0
```

You can cause hte nonexisting itemt come into existence. You can so arrange by supplying a code block to Hash.new

`h = Hash.new { |hash, key| hash[key] = 0  }`

9.3.4 Combining hashes with other hashes

two flavors, destructive flavor or the non-destructive flavor. 

* destructive way 
```
h1 = {"Smith" => "John",
"Jones" => "Jane" }
h2 = {"Smith" => "Jim" }
h1.update(h2)
puts h1["Smith"]
```


* non-destructive way 

use the **merge** method and there is a **merge!**.

```
h1 = {"Smith" => "John",
"Jones" => "Jane" }
h2 = {"Smith" => "Jim" }
h1.merge(h2)
puts h1
```

### 9.3.5 Hash transformations

#### INVERTING A HASH
tell to flip the key and value, so that the key becomes the value and the values become the keys

```
>> h = { 1 => "one", 2 => "two" }
=> {1=>"one", 2=>"two"}
>> h.invert
=> {"two"=>2, "one"=>1}
```

only invert a hash when you are sure that there is no duplicate keys inside the hash.

#### CLERAING A HASH

**clear** method

```
>> {1 => "one", 2 => "two" }.clear
=> {}
```

#### REPLACING THE CONTENTS OF A HASH

```
>> { 1 => "one", 2 => "two" }.replace({ 10 => "ten", 20 => "twenty"})
=> {10 => "ten", 20 => "twenty"}
```

### 9.3.6. Hash querying

| Method name/sample call  |  Meaning |
| :----------------------- | :---------------------------------|
| h.has_key?(1) | True if h has the key 1 |
| h.include?(1)?    | Synonym for has_key? |
| h.key?(1)   |  Synonym for has_key? |
| h.member?(1) | NumberAnother synonym for has_key? |
| h.has_value?("three")      |  True if any value in h is “three” |
| h.value?("three") | Synonym for has_value? |
| h.empty?      |  True if h has no key/value pairs |
| h.size | Number of key/value pairs in h |


### 9.3.7. Hashes as method arguments

it is about one syntax sugar that has used in Ruby, when the Hash argument is the last key to the function call, ruby allows you to write the hash without curly braces. 

```
link_to "Click here"
  :controller => "Work"
  :action => "show"
  :id => work.id
```


which is equivalent to the following 

```
link_to ("Click here", {:controller => "work",
                        :action     => "show",
                        :id         => work.id })
                        
                        
```

why having this type of sugar???  because this gives you the STANZA FROM A CONFIGURATION FILE THAN A METHOD CALL.

and with the special form of hash literal , you can write as follow 

```
link_to ("Click here", controller:  "work",
                        action:  "show",
                        id: work.id })

```

another example is the 

```
add_to_city_database("New York City", :state => "New York",
                     :population => 7000000,
                     :nickname => "Big Apple"

# in this case, you can use special syntax sugar for hashes whose keys are symbols:

add_to_city_database("New York City", state: "New York",
                    population: 7000000,
                    nickname: "Big Apple"

```
if you were to implement the method *add_to_city_database*, you will probably  do more the those parameter passed in as  a list through left-to-right order

```
def add_to_city_databae(name, *info) 
   c = City.new
   c.name = name
   c.state = info[:state]
   c.populate = info[:population]
```


## 9.4 Ranges

the semantics of a range operations involves two major concepts:

* Inclusion  - Does a given value fall inside the range?
* Enumeration - The range is treated as a traversable collection of individual items. 

### 9.4.1 Creating a range

```
r = Range.new(1, 100)
```

or with literal 

`r = 1..10`


to create a exclusive range, do this:

```
>> Range.new(1,100)
=> 1..100
>> Range.new(1,100,true)
=> 1...100
```

#### REMEMBERING .. VS. ...

value 100 is included in the range:
`1..10`
but in this exclusive range, the value 100 lies beyond the effective end of the range.  

`1...100`

### 9.4.2 range-inclusion logic 

Range have *begin* and *end* methods. 

```
>> r = 1..10
=> 1..10
>> r.begin
=> 1
>> r.en
```

#### TESTING RANGE INCLUSION WITH COVER?
the *cover?* method performs a simple test.

```
>> r = "a".."z"
=> "a".."z"
>> r.cover?("a")
=> true
>> r.cover?("abc")
=> true
>> r.cover?("A")
=> false
```

if not comparable, then it will return false.

#### TESTING RANGE INCLUSION WITH INCLUDE?
*include?* does compare by comparing the discrete values within.

but if the range cannot be represent as the discrete values, then it shall be done with the "cover?" method. 

RANGES GOES IN ONE WAY. KEEP THE MENTAL NOTE OF THE FACTS THAT RANGES ONLY GO ONE WAY.


## 9.5 Sets

to use 'set' with the following code.

`require 'set'`



### 9.5.1 Set Creation

* with Set.new method 

```
 >> new_england = ["Connecticut", "Maine", "Massachusetts",
"New Hampshire", "Rhode Island", "Vermont"]
>> state_set = Set.new(new_england)
=> #<Set: {"Connecticut", "Maine", "Massachusetts",
"New Hampshire”, "Rhode Island", "Vermont"}>
```

as always, you can accept a code block to insert the transformed data. 

```
>> names = ["David", "Yukihiro", "Chad", "Amy"]
=> ["David", "Yukihiro", "Chad", "Amy"]
name_set = Set.new(names) { |name| name.upcase }
=> #<Set: {"AMY", "YUKIHIRO", "CHAD", "DAVID"}>
```

### 9.5.2 Manipulating set elements

Like arrays, sets have two nodes of adding elements. 

#### ADDING/REMOVING ONE OBJECT TO/FROM A SET

as always, you can use the `<<` operator to add new element.

```
>> tri_state = Set.new(["New Jersey", "New York"])
=> #<Set: {"New Jersey", "New York"}>
>> tri_state << "Connecticut"
=> #<Set: {"New Jersey", "New York", "Connecticut"}>
```

and if you want to remove some element you 'd try the function `delete`. 
```
>> tri_state << "Pennsylvania"
=> #<Set: {"New Jersey", "New York", "Connecticut", "Pennsylvania"}>
>> tri_state.delete("Connecticut")
=> #<Set: {"New Jersey", "New York", "Pennsylvania"}>
```

#### SET INTERSECTION, UNION, AND DIFFERENCE

`Set` has provided both the english name set of functions as well as the symbolic ones. 

* intersection, aliased as &
*  union, aliased as + and |
* difference, aliased as -


```
>> tri_state = Set.new(["Connecticut", "New Jersey", "New York"])
=> #<Set: {"Connecticut", "New Jersey", "New York"}>
# Subtraction (difference/-)
>> state_set - tri_state
=> #<Set: {"Maine", "Massachusetts", "New Hampshire", "Rhode Island",
"Vermont"}>
# Addition (union/+/|)
>> state_set + tri_state
=> #<Set: {"Connecticut", "Maine", "Massachusetts", "New Hampshire",
"Rhode Island", "Vermont", "New Jersey", "New York"}>
# Intersection (&)
>> state_set & tri_state
=> #<Set: {"Connecticut"}>
>> state_set | tri_state
=> #<Set: {"Connecticut", "Maine", "Massachusetts", "New Hampshire",
"Rhode Island", "Vermont", "New Jersey", "New York"}>
```

#### MERGING A COLLECTION INTO ANOTHER SET

you can use the merge operation. remember that the merge is an in-place operation.  

```
tri_state = Set.new(["Connecticut", "New Jersey"])
tri_state.object_id
tri_state.merge(["New York"])
tri_state.object_id
```

### 9.5.3 Subsets and Supersets

there are predicate methods called `superset?' or `subset`..

```
small_states = Set.new(["Connecticut", "New Jersey", "Rhode Island"])
small_states.subset?(state_set)
state_set.superset?(small_states)
```

## 9.6 Exploring the set.rb source code

when you feel that you have learned enough, you can explore the contnet of the set.rb files for details. 

### 9.6.1 Set#initialize

first let's see an good implementation on the Set#initialize

```
def initialize(enum = nil, &block)
  @hash ||= Hash.new B
  enum.nil? and return
  if block
    enum.each { |o| add(block[o]) }
  else
    merge(enum)
end
```

### 9.6.3 Set#include?

```
def include?(o)
  @hash.include?(o)
end
```


### 9.6.3. Set#add and Set#add?

to show that you can do with predicate version of a method or a non-predicate version of a method.  

```
def add(o)
  @hash[o] = true
  self
end
```

```
def add?(o)
  if include?(o)
   nil
  else
   add(o)
  end
end
```

## 9.7 Summary 

We have covered Ruby's major core container classes.

# 10 Collections central: Enumerable and Enumerator

what shall be covered in this chapter:

1. Mixing Enumerable into  your module
2. The use of Enumerable methods in collection objects
3. Strings as a quasi-enumerable objects
4. Sorting enumerable with Comparable module  
5. Enumerators

the collection sorts of operations is endowed by `Enumerable` in terms of `each`

To mix the `Enumerable`

```
class C
  includes Enumerable
end
```

however, mixing `Enumerable`  does not give you much, you provides the `each ` method.
```
class C
  include Enumerable
  def each 
    #relevant code here 
  end
end
```

## 10.1 Gaining enumerability through each 

`each` method whose job is to _yield items to a supplied block_, one at a time.

check out the following example.

```
class Rainbow
  include Enumerable
  def each
    yield "red"
    yield "orange"
    yield "yellow"
    yield "green"
    yield "blue"
    yield "indigo"
    yield "violet"
  end
end

r = Rainbow.new
  r.each do |color|
  puts "Next color: #{color}"
end
```
you may want to ask what kind of operations has been brought in by the Enumerable module, you can check by this:

```
Enumerable.instance_methods(false).sort
```

to list a few, there are such methods 

    :all?, :each_slice, :each_with_index


## 10.2 Enumerable boolean queries 

by example to show what kind of queries that you can do 

```
#Does the array include Louisiana
states.include?("Louisiana")
# Do all states include a space?
states.all? {|state| state =~ / / }
# Does any state include a space?
states.any? {|state| state =~ / / }
# Is there one, and only one, state with "West" in its name?
states.one? {|state| state =~ /West/ }
# Are there no states with "East" in their names?
states.none? {|state| state =~ /East/ }
```

**NOTE: ** with range object, you cannot do some of the Enumerable operation, such as for float ranges, you cannot do .. one? none?

## 10.3 Enumerable searching and selecting

the operations that falls under the searching and selecting are:
* find
* find_all

### 10.3.1 Getting the first match with find

e.g.

```
[1,2,3,4,5,6,7,8,9,10].find {|n| n > 5 }
```

you can also provide a `Proc` object as an argument to find, in which case that function will be called if the find operation failed

```
failure = lambda { 11 }
over_ten = [1,2,3,4,5,6].find(failure) {|n| n > 10 }
```

**NOTE:** the dominance of array

normally when you do a Enumerable selecting and filtering operations, the result returned is an array , it is a quasi-rule, it hold widely. (when you work with Hash, normally you get back a hash)

### 10.3.2 Getting all matches with find_all (a.k.a. select) and reject

```
a = [1,2,3,4,5,6,7,8,9,10]
a.find_all {|item| item > 5 }
a.select {|item| item > 100 }
```

and you can do a reverse select with the function "reject", here is the code. 

```
a.reject {|item| item > 5 }
```

### 10.3.3 Selecting on "threeequal" matches with grep 

the case equality operator can help you do some magic match (such as the reange match of the regular expression match) 

```
colors = %w{ red orange yellow blue indigo violet }
colors.grep(/o/)
```

another example is to find from a collection those instance which are *String* 

```
miscellany = [75, "hello", 10...20, "goodbye"]
miscellany.grep(String0
```


### 10.3.4 Organizing selection results with group_by and partition


* group_by

This internally is built with some kind of hash internally.

```
colors = %w{ red orange yellow blue indigo violet }
=> ["red", "orange", "yellow", "blue", "indigo", "violet
colors.group_by {|color| color.size }
```
* partition
```
class Person
  attr_accessor :age
  def initialize(options)
    self.age = options[:age]
  end
  def teenager?
   (13..19) === age
  end
end

people = 10.step(25,3).map {|i| Person.new(:age => i) }
teens = people.partition {|person| person.teenager? }
puts "#{teens[0].size} teens; #{teens[1].size} non-teens"
```

the result, which contains two sub-arrays, the first one is the array of item which returns false from the predicate, the other part is from the items which returns true. 

## 10.4 Element-wise enumerable operations

Collections are born to be traversed, but they also contain special-status individual objects: the first object or last in the collection, and the greatest ...

### 10.4.1 The first method 

* first on array 
```
[1,2,3,4].first
```

* first on hash 

the first will return the first inserted pair to the hash

```
hash = {3 => "three", 1 => "one", 2 => "two" }
hash.first
hash[3] = "trois"
hash.first
```


**NOTE:** there is no method called "last" because the Enumeration might go on forever.


### 10.4.2 The take and drop methods

takes , take sthe first few element from the enumerable
drops,  drops few element from the enumerable

```
states = %w{ NJ NY CT MA VT FL }
states.take(2)
states.drop(2)
```

you can constrain the take and drop operation by providing a block and using the variant forms `take_while` and `drop_while`

```
states.take_while {|s| /N/.match(s) }
states.drop_while {|s| /N/.match(s) }
```

### 10.4.3 the min and max methods 

simple kind of aggregation.

```
[1,3,5,4,2].max
%w{ Ruby C APL Perl Smalltalk }.min
```

to do the min/max based on the non-defualt criterion, do with the `min_by` and `max_by`

```
%w{ Ruby C APL Perl Smalltalk }.min_by {|lang| lang.size }
```

`minmax_by` gives back two values (min,max) in a single go 

```
%w{ Ruby C APL Perl Smalltalk }.minmax
%w{ Ruby C APL Perl Smalltalk }.minmax_by {|lang| lang.size }
```

and if you try to invoke the min/max method on a hash, provide the *xxx_by* method. The default min/max method determins the ordering with the key.

```
state_hash = {"New York" => "NY", "Maine" => "ME",  "Alaska" => "AK", "Alabama" => "AL" }
state_hash.min
state_hash.min_by {|name, abbr| name }
state_hash.min_by {|name, abbr| abbr }
```

## 10.5 the relative of each 

Enumerable makes serveral  methods available to you which you are similar to each. in that they go through the whole collectoin and yield elements from it .

so the general varaint of each includes the following. 

* each_with_index
* each_slice
* each_cons
* cycle
* inject

### 10.5.1 the each_with_index method 

```
names = ["George Washington", "John Adams", "Thomas Jefferson",
"James Madison"]
names.each_with_index do |pres, i| 
  puts "#{i+1}. #{pres}" 
end
```


### 10.5.2 the each_slice and each_cons methods 
 
the each_slice and each_cons methods walks through a certain number of elements at a time. 

the difference is that the `each_slice` will cut sequence into parts, while the `each_cons` will slide through a window once at a time. 

```
array = [1,2,3,4,5,6,7,8,9,10]
array.each_slice(3) {|slice| p slice }
array.each_cons(3) {|cons| p cons }
```

### 10.5.3 the cycle method 

`cycle` will runs through the object again and again. if you provide a number to it, it runs that many times, otherwise, it runs infinitely.

```
class PlayingCard
  SUITS = %w{ clubs diamonds hearts spades }
  RANKS = %w{ 2 3 4 5 6 7 8 9 10 J Q K A }
  class Deck
  attr_reader :cards
    def initialize(n=1)
      @cards = []
      SUITS.cycle(n) do |s|
        RANKS.cycle(1) do |r|
        @cards << "#{r} of #{s}"
        end
      end
    end
  end
end

# e.g. to get two sets of cards, you can do the following 
deck = PlayingCard::Deck.new(2)
```


### 10.5.4 Enumerable reduction with inject 

the inject method is also known as "fold" or "reduce" in other functional programming language. 

let's shown an example

```
[1,2,3,4].inject(0) { |acc,n| acc + n}
```

one variant you can choose not to set the initial acc, but that works for this situation as well.  

a souped-up example, shown as below. 

```
[1,2,3,4].inject do |acc, n|
   puts "adding #{acc} and #{n} ... #{acc+n}"
   acc + n
end
```
the code above shown you how to process each step with the acc and the argument in each iteration.  
NOTE: **reduce** is a alias to the inject method.

### 10.6 the map method 

map does what we called transformation, ONE note on the map method is that _Whatever enumerable it starts with, map always returns an array_

e.g.

```
names = %w{ David Yukihiro Chad Amy }
names.map {|name| name.upcase }
```

### 10.6.1 the return value of map 

NOTE: unlike each, which alays return the receiver (that you can chain the cdoe together), the map returns new object.

#### BE CAREFUL WITH BLOCK EVALUATION

```
array = [1,2,3,4,5]
result = array.map {|n| puts n * 100 }
```
the result should be [nil, nil,..] because the nil is the return value of puts call.

### 10.6.2 In-place mapping with map!

the in-place version of map is _map!_

check the following.

```
names = %w{ David Yukihiro Chad Amy }
names.map!(&:upcase)
```

A note on the & (ampersand) operator, it is a "to_proc" converter. where you can apply to ta block, to a lambda or to other object (on which the #to_proc method will be invoked)


## 10.7 Strings as quasi-enumerables

You can iterate through the raw bytes or the characters of a string using convenient iterators methods that treat the strign as a collection of bytes, characters , lines;

```
str = "abcde"
str.each_byte |b| p b }
```

and to demonstrate the use of each_char, here is the code 
```
str = "abcede"
str.each_char {|c| p c }
```

and maybe less common, you can iterate by codepoint, as shown 
```
str = "100\u20ac"
str.each_codepoint {|cp| p cp }
```

(NOTE: usually one code ponit corresponds to one character)

and each lines' example is as follow. 

```
str = "This tring \n has three\n lines"
str.each_line{|l| puts "Next line: #{1}" }
```
you can control the concept of line by the **$/** global variable.

```
str = "David!Alan!Black"
$/ = "!"
str.each_line {|l| puts "Next line: #{l}" }
```

## 10.8 Soriting enumerables

if you have a class, and you want to be able to arrange multiple instances of it in order. You need to do the following. 

1. Define a comparison method for the class (<=>)
2. Place hte multiple instance in a container, probably an array 
3. Sort the container 

the ability to sort is granted by Enumerable.  the Enumerable has two sort method, **sort** and **sort_by** 

e.g.

```
[3,2,5,4,1].sort
```

For your object to be sortable, your object has to implement the **<=>** method. 

### 10.8.1 Where the Comparable module fits nto enumerable sorting (or doesn't)

there are three types:

* defined _<=>_, put inside an array or other enumerable for sorting.
* don't define <=>, still sort by providing a block 
* defined  _<=>_, include _Comparable_ in your classes, then you get sort-ability inside an array and you can perform sorting as well as comparison between two object.

### 10.8.2 Defining sort-order logic with a block

```
year_sort = [pa1, pa2, pa3, pa4, pa5].sort do |a,b|
   a.year <=> b.year
end
```

another examples is as follow.

```
>> ["2",1,5,"3",4,"6"].sort {|a,b| a.to_i <=> b.to_i }
=> [1, "2", "3", 4, 5, "6"]
```

### Concise sorting with sort_by

```
>> ["2",1,5,"3",4,"6"].sort_by {|a| a.to_i }
=> [1, "2", "3", 4, 5, "6"]
```

## 10.9 Enumerator and the next dimension of enumerability

the each method can hele define some more advanced method such as map, find, take, drop and the rest.

### 10.9.1 Creating enumerators with a code block 
first let take a look at the enumerator.

```
e = Enumerator.new do |y|
y << 1
y << 2
y << 3
end
```

First thing, what is a y?

y is a yielder, an instance of Enumerator::Yielder.

you can use the Enumerator, such as the examples shows below. 


```
>> e.to_a
=> [1, 2, 3]
>> e.map {|x| x * 10 }
=> [10, 20, 30]
>> e.select {|x| x > 1 }
=> [2, 3]
>> e.take(2)
=> [1, 2]
```


The enumerator iterates once for every time that << (or the yield method) is called on the yielder.

so we can rewrite the previous method as such.

```
e = Enumerator.new do |y|
(1..3).each {|i| y << i }
end
```

Note, that you don't yield from the block, that is , you don't do this:

```
e = Enumerable.new do 
   yield 1
   yield 2
   yield 3
end
```


```
a = [1,2,3,4,5]
e = Enumerator.new do |y|
  total = 0 
  until a.empty?
     total += a.pop
     y << total
  end
end
```

### 10.9.2 Attaching enumerator to other object

The other way to endow an enumerator with each is to hook the enumerator up to another object - specifically, to an iterator.

You can create the enumerator with the **enum_for** method.

```
scale.enum_for(:play)
names = %w{ David Black Yukihiro Matsumoto }
e = names.enum_for(:select)
```

now, you have bind the enumerator to method "select", now that you can use the "each" as a front end to array's select :

```
e.each {|n| n.include?('a') }
```

it has the same effect as 
```
e.select { |n| n.include?('a') }
```


similarily, we can do the folllowing 

```
>> e = names.enum_for(:inject, "Names: ")
=> #<Enumerator:0x3b6c80>
>> e.each {|string, name| string << "#{name}..." }
=> "Names: David...Black...Yukihiro...Matsumoto..."
```
which is the same as the following 

```
e = names.inject("Names:") {|string, name| string << "#{name}..." }
```

NOTE: you can well use the Enumerator.new(obj, method_name, arg1, arg2..) ,however, it is not encouraged to use the Enumerator.new method, but instead encouraged to use the enum_for method.

### 10.9.3 Implicit creation of enumerator by blocks iterator calls

most built-in iterators return an enumerator when they're called without a block . here is the example.

```
>> str = "Hello"
=> "Hello"
>> str.bytes {|b| puts b }
72
101
...
>> str.bytes
=> #<Enumerator:0x3dbddc>

```

## 10.10  Enumerator semantics and uses

### 10.10.1  how to use an enuemrators's each 

#### THE UN-OVERRIDING PHENOMENON

the un-overridding is that the override collection such as Hash when it is visited by he means of the  Enumerable, some of the override method might revert back to the un-override version, whch may generate some unexpected behavior for you.

e.g.

```
>> e = h.enum_for(:select)
=> #<Enumerator:0x3e0bfc>
>> e.each {|key,value| key =~ /c/ }
=> {"cat"=>"feline", "cow"=>"bovine"}
```

you get back a hash by calling the enum_for on the select method on the hash and then calling the each on the enumerator. that is because the hash has override the enumerator method.

the Enumerator's each is front-end to the hash's each.  see below.

```
>> e = h.to_enum
=> #<Enumerator:0x3dcf34>
>> h.each { }
=> {"cat"=>"feline", "dog"=>"canine", "cow"=>"bovine"}
>> e.each { }
=> {"cat"=>"feline", "dog"=>"canine", "cow"=>"bovine"}
```

but the enumerator's each method stil returns array not the hash... so you get.

```
>> e.select {|key,value| key =~ /c/ }
=> [["cat", "feline"], ["cow", "bovine"]]
```

### 10.10.2 Protecting objects with Enumerators

sometimes we want to protected the internal from the outside tampering, so that instead directly expose the object back to the outside,  it is preferred to expose the enumerator back . (comparing to the freeze to freeze some collection, the enumerator is better)

e.g.

```
class PlayingCard
  SUITS = %w{ clubs diamonds hearts spades }
  RANKS = %w{ 2 3 4 5 6 7 8 9 10 J Q K A }
  class Deck
  def cards
    @cards.to_enum
  end
  def initialize(n=1)
    @cards = []
    SUITS.cycle(n) do |s|
      RANKS.cycle(1) do |r|
        @cards << "#{r} of #{s}"
      end
    end
   end
 end
end
```

### 10.10.3 Fine-grained iteration with enumerators

because the enumerator has maintained some states inside the object. so that you can finer controlled the iteration.

```
names = %w{ David Yukihiro }
e = names.to_enum
puts e.next
puts e.next
e.rewind
puts e.next
```

### 10.4 Addig enumerability with an enumerator

It’s a matter of wiring: if you hook up an enumerator’s each method to any iterator, then you can use the enumerator to perform enumerable operations on the object that owns the iterator

e.g.

```
module Music
  class Scale
    NOTES = %w{ c c# d d# e f f# g a a# b }
    def play
      NOTES.each {|note| yield note }
    end
  end
end
```

But the scale isn't technically an enumerable. The standard methods from Enumerable won't work because the class Music::Scale does not mix in Enumerable and doesn't define each 

However, you can use the enum_for method to do the enumeration

```
enum = scale.enum_for(:play)
```

by doing this, you can get all the standard enumerability.

## 10.11  Enumerator method chaining 
method chaining is a common techniques in Ruby programming. 

```
puts names.select {|n| n[0] < 'M' }.map(&:upcase).join(", ")
```

### 10.11.1 Economizing on intermediate objects


#### Enumerator literacy

by taking an example. 

```
string = "An arbitrary string"
string.bytes.map {|b| b + 1 }
```
in fact the string.bytes returns an enumerator, The key is that an enumerator is a collection.

### 10.11.2 Indexing enumerables with with_index

```
names = %w{ David Yukihiro Joe Jim John Joan Jeff Judy }
names.each_with_index do |name,i|
  puts name
  if (i+1) % 3 == 0
    puts "-------"
  end
end

```

besides the with_index method, you may want to have some type of map_with_index,it is not hard to implement like below .

```
('a'..'z').map.with_index {|letter,i| [letter,i] }
```

and if there is such method called "map_with_index" then it would be soemthing like below. 

`('a'..'z').to_a.map_with_index {|letter,i| [letter,i] }`

### 10.11.3 Exlusive-or operators on strings with enumerators

the xor operator has the speical attribute that when (a^b)^b == a, so that it can be used to obsfucate the original information. here is the details.

```
class String
  def ^(key)
    kenum = key.bytes.cycle
    bytes.map {|byte| byte ^ kenum.next }.pack("C*")
  end
end
```

the pack method can be thought as a special type of formatter, where the C* means that the "treat each element of the array as an unsigned integer representing a single character"...

e.g

```
str = "Nice little string"
key = "secret!"
x = str ^ key 
orig = x ^ key 

```


NOTE: the above code is not robust to the encoding issue, so you might want to guard against the encoding issues. So here is a more encoding-safe method 

```
bytes.map {|byte| byte ^ kenum.next }.pack("C*").force_encoding(self.encoding)
```

# Regular Expressions and regexp-based string operations

in this chapter, the following:
regular expression syntax
pattern-matching operations
the matchdata class 
bulit-in method based on pattern matching

## 11.1 What are regular expressions?

NOTE: the ruby's regular expression is not identical to those of the vi, emacs, and perl...

## 11.2 writing regular expressions.

### 11.2.1 Seeing pattern

### 11.2.2 Simple matching with literal regular expression 

regular expression has a literal constructor for easy instantiation, here it is .

`//`

you can check on the class of the regular expression as follow. 

```
//.class
```

the simplest way to use an regular expression is with the match method.  (the match can work in two ways)

```
puts "Match!" if /abc/.match("The alphabet starts with abc.")
puts "Match!" if "The alphabet starts with abc.".match(/abc/)
```

## 11.3 Building a pattern in regular expression 

* Literal characters, meaning "Matching this character"
* The dot wildcard character (.), meaning “match any character”
* Character classes, meaning “match one of these characters”

### 11.3.1 Literal character in patterns.

NOTE: the character _\ _ is used for  escape.

### 11.3.2 the wildcard character . (dot) 

### 11.3.3 Character classes.
a character class is an explicit list of character placed inside the regexp in square brackets.

#### SPECIAL ESCAPE SEQUENCES FOR COMMON CHARACTER CLASSES

the character class `/[0-9]/` can be represented as follow. 

`/\d/`

* \w matches any digit, alphabetical character, or underscore (_).
* \s matches any whitespace character (space, tab, newline).

each also has an negate form. 

* /\D/ matches on non-digit
* \S matches any non whitespace 
* \W matches non word

## 11.4 Matching , substring capture, and MatchData.
what we want to know beside the true, false test, what does the match can give you 

### 11.4.1 Capturng submatches with parenthesis

first create some regular expression.

`/([A-Za-z]+),[A-Za-z]+,(Mrs?\.)/`

note the special use of the parenthesis of the regular expression, and then ou can duse that to match against string.

`/([A-Za-z]+),[A-Za-z]+,(Mrs?\.)/.match("Peel,Emma,Mrs.,talented amateur")`

what we get?

* We get a MatchData object that gives us access to the submatches
* Ruby automatically populates a series of variables for us, which also give us access to those submatches.

NOTE: Perl uses the $0 for the entire match, however, in ruby $0 stands for the program's name. so Ruby provide some method for this.

```
line_from_file = "Peel,Emma,Mrs.,talented amateur"
/([A-Za-z]+),[A-Za-z]+,(Mrs?\.)/.match(line_from_file)
puts "Dear #{$2} #{$1},"
```

### 11.4.2 Match success and failure
Every match operation either succeeds or fail. if fail, result is always nil.

```
>> /a/.match("b")
=> nil
```


to use the matchobject, you first need to store it in a variable.

```
string = "My phone number is (123) 555-1234."
phone_re = /\((\d{3})\)\s+(\d{3})-(\d{4})/
m = phone_re.match(string)
unless m
  puts "There was no match—sorry."
  exit
end
print "The whole string we started with: "
puts m.string
print "The entire part of the string that matched: "
puts m[0]
puts "The three captures: "
3.times do |index|
  puts "Capture ##{index + 1}: #{m.captures[index]}"
end
puts "Here's another way to get at the first capture:"
print "Capture #1: "
puts m[1]
```

### 11.4.3 Two ways of getting the captures

you can find the the match witht the indexer or with the capture methods, here are the same. 

```
m[1] == m.captures[0]
m[2] == m.captures[1]
```

### 11.4.4 Other MatchData information.

the following methdods that are covered are :

* pre_match
* post_match
* begin
* end

we will further study the component of the regular expression, they are 

* quantifier
* anchors
* modifiers

some advanced may even have certain construct that is called *assert*.


## 11.5 Fine-tuning regular expression with quantifiers, anchors, and Modifiers


### 11.5.1 Constraining matches with quantifiers

#### ZERO OR ONE
\?
#### Zero or more
\*
#### ONE or more 
\+

### 11.5.2 Greedy (and non-greedy) quantifiers

#### SPECIFIC NUMBERS OF REPETITIONS

an example of the quantifiers are as follow. 

```
/\d{3}-\d{4}/
```

to match three or more,  you can write as follow. 

`/\d{3,}/`

#### THE LIMITATION ON PARENTHESES

with an exanple, you can only get the 'K' back if you do match like below. 
```
>> /([A-Z]){5}/.match("David BLACK")
=> #<MatchData "BLACK" 1:"K">
```

the correct way to match is like this: 

```
>> /([A-Z]{5})/.match("David BLACK")
=> #<MatchData "BLACK" 1:"BLACK">
```

### 11.5.3 Regular expression anchors and assertions.

An assertion or an anchor, on the other hand, doesn’t consume any characters. Instead, it expresses a constraint: a condition that must be met before the matching of characters is allowed to proceed.

`/^\\s*#/`

regular expression anchors.

| Notation         | Description    | Example          | Sample Matching string 
 ------------------|------------------------------------------|-----------------------
| ^ | Beginning of line   | /^\s*#/ |  " # A ruby comment line with leading spaces"
| \$ | End of line   | /\\.$/ |  "one\ntwo\nthree.\nfour"
| \A | Beginning of string   | /\AFour score/ | "Four score"
| \z | End of string   | /from the earth.\z/ |  "from the earth."
| \Z | end of string (except for final newline   | /from the earth. \Z/ |  "from the earth\n"
| \b | word boundary   | /\b\w+\b/ |  " !!!word***" (matches "word")


#### LOOKAHEAD ASSERTIONS

Let’s say you want to match a sequence of numbers only if it ends with a period. Butyou don’t want the period itself to count as part of the match.

```
str = "123 456. 789"
m = /\d+(?=\.)/.match(str)
```

there are terminology regarding the regular expression.

* _Zero-width_ means it doesn’t consume any characters in the string
* _Positive_ means you want to stipulate that the period be present. there are also negative lookaheads, they use _(?!...)_ rather than _(?=...)_.
* _Lookahead assertion_ means you want to know that you’re specifying what would be next, without matching it.


#### LOOKBEHIND ASSERTIONS

suppose that we only want ot match BLACK when it is preceded by "David". 

`re = /(?<=David )BLACK/`

and the negative look back assertion is like below. 

`re = /(?<!David )BLACK/`

NOTE: the non-capture group. 

#### NON-CAPTURE GROUP

the non-capture group can be represented as follow. 

`?:`


### 11.5.4 Modifiers

Modifiers can modify the behavior of the match. 
e.g.
`/abc/i`

there are modifiers that can be used.

* \i ignore case
* \x changes the wa the regex parser treat whitespaces (so you can insert comment)
* \m multile  multiple line mode

## 11.6 Converting strings and reglar expressions to each other.
regular expression is not a string. 


### 11.6.1 String to regexp idioms

this can be done with the string interpolation. 

```
>> str = "a.c"
=> "a.c"
>> re = /#{str}/
=> /a.c/
>> re.match("a.c")
=> #<MatchData "a.c">
```

and if ther string has special character, you can do escape on the string. 

```
>> Regexp.escape("a.c")
=> "a\\.c"
```

with the escape, you can make the regular expression to match exact mode. 

```
>> str = "a.c"
=> "a.c"
>> re = /#{Regexp.escape(str)}/
=> /a\.c/
>> re.match("a.c")
=> #<MatchData "a.c">
```

another string to regular expression conversion can be done with the Regexp.new method.

```
>> Regexp.new('(.*)
```


### 11.6.2 Going from a regular expression to a string

by puts, you can inspect the string representation. 

```
>> puts /abc/
(?-mix:abc)
```

you can also inspect the regular expression.

```
>> /abc/.inspect
=> "/abc/"
```

## 11.7 Common methods that use regular expressions

The payoff for gaining facility with regular expressions in Ruby is the ability to use the methods that take regular expressions as arguments and do something with them

```
array.find_all {|e| e.size > 10 and  /\d/.match(e)  }
```


## 11.7.1 String\#scan

```
>> "testing 1 2 3 testing 4 5 6".scan(/\d/)
=> ["1", "2", "3", "4", "5", "6"]
```

if you use parenthetical groupings as the regexp you give to scan, the opreation returns an array of array .

```
>> str = "Leopold Auer was the teacher of Jascha Heifetz."
=> "Leopold Auer was the teacher of Jascha Heifetz."
>> violinists = str.scan(/([A-Z]\w+)\s+([A-Z]\w+)/)
=> [["Leopold", "Auer"], ["Jascha", "Heifetz"]]
```

if you want to do some scanning of some scale, you might want to give a shot to the StringScanner classs. For the space of discussion, we will ignore the StringScanning class.

### 11.7.2 String\#split

first let's see an example that does the string split with regular expression.

```
>> "Ruby".split(//)
=> ["R", "u", "b", "y"]
```

### 11.7.3 sub/sub! and gsub/gsub!

#### SINGLE SUBSTITUTIONS WITH SUB

```
>> "capitalize the first vowel".sub(/[aeiou]/) {|s| s.upcase }
=> "cApitalize the first vowel"
```

#### GLOBAL SUBSTITUTIONS WITH GSUB

```
>> "capitalize every word".gsub(/\b\w/) {|s| s.upcase }
=> "Capitalize Every Word"
```

#### USING THE CAPTURES IN A REPLACEMENT STRING
it is available that you can use the special notation (consist of backslash-escaped) numbers.

```
>> "aDvid".sub(/([a-z])([A-Z])/, '\2\1')
=> "David"
```

### 11.7.4 Case equality and grep
the _=== _ operator has been overloaded for the regular expression.

by showing you an example, you can get this: 

```
print "Continue? (y/n) "
answer = gets
case answer
when /^y/i
  puts "Great!"
when /^n/i
  puts "Bye!"
exit
else
  puts "Huh?"
end
```

then continue with the grep method, by example we can show you something like below. 

```
>> ["USA", "UK", "France", "Germany"].grep(/[a-z]/) {|c| c.upcase }
=> ["FRANCE", "GERMANY"]
```

# File, I/O and system operations

the topic in this chapter - Keyboard I/O , fiels, and sytem commands, are united by the fact that they operate on entities that aren't strictly speaking , objects. 

in this chapter, we will expect to see more Standard library (as opposed to core) packages in this chapter than anywhere else in this book. the higlighted by the _FileUtils_, _pathname_ and _StringIO_ packages. 


### 12.1.1 the IO classes


IO objects represent readable and/or writable connections to disk files, keyboards, screens, and other devices.

```
>> STDERR.class
=> IO
>> STDERR.puts("Problem!")
Problem!
=> nil
```

In addition to _puts_, IO objects have the _print_ the  method , which there is no automatic newline output.

### 12.1.2 IO objects as enumerables

show you an example to treat the IO as enumerables

```
>> $/ = "NEXT"
=> "NEXT"
>> STDIN.each {|line| p line}
First line
NEXT
"First line\nNEXT"
```


### 12.1.3 STDIN, STDOUT, STDERR

Ruby gives you the global variables, $stdin, $stdout, and $stderr;

#### THE STANDARD I/O GLOBAL VARIABLES

why we have such an variable alongside with the CONSTANTS? the reason is because variale allow you to reasig to the variable..

```
record = File.open("/tmp/record", "w")
old_stdout = $stdout
$stdout = record
$stderr = $stdout
puts "This is a record"
z = 10/0
```

if you open the '/tmp/record', you will see the following contents.

```
This is a record
chapter12_redirect_stderr.rb:6:in `/': divided by 0 (ZeroDivisionError)
	from chapter12_redirect_stderr.rb:6:in `<main>'
```


###  12.1.4  A litttle more about keyboard input 

```
line = gets 
char=  STDIO.getc
```


NOTE : Both the gets and the getc are buffered, that means you have to press Enter in order to get anything happen.

You can turn on the raw mode, in Unix-ish system, you can select the terminal into raw mode with the "stty"

## 12.2 Basic file operations

File is a subclass to the IO class. 
we will check the following in the File class, they are 

* opening
* reading
* writing
* closing

to read from file, first simply open the file with the File.new method. File.read method is a simple way to get contents out of the file. 

```
f = File.new("code/ticket2.rb")
f.read
```

### 12.2.2  Line-based file reading
the easiest way to read the next line from a file with gets.

file objects are enumerable, so that you can just do the following 

```
f.each{|line| puts "Next line: #{ine} }
```

or there is more low-level finer grained operation on the file object, htere it is.

```
f.gets
f.gets

f.read
f.readline # if you reach the end of the file, you will get a EOFError

# you can rewind the file handler, like below. 
f.rewind

```

### 12.2.3 Byte- and Character-based file reading

you can get a character out of a file and "unget" it back to the buffer.

```
>> f.getc
=> "c"
>> f.ungetc("X")
=> nil
```

you can do via the byte boundary, you can do with getbyte.

There are some variant of the form "readXXX", while the XXX can be byte, char, or line .... 

the difference being that if you getXX yo will not get eror when at the EOF, while you have the readXXX overloaed, you might get EOFError .

### 12.2.4 Seeking and querying file position

you can tell the current position of the File object by the File.pos method.

```
>> f.pos
=> 0
```

you can use the **File.rewind** method to rewind the file to the begining of the file; while it is also possible that you can calll **File.seek** method.

```
f.seek(20, IO::SEEK_SET)
f.seek(15, IO::SEEK_CUR)
f.seek(-10, IO::SEEK_END)
```

### 12.2.5 Reading file with File class method


two method that we will discussed here;

* File.read
* File.readlines

```
full_text = File.read("myfile.txt")
lines_of_text = File.readlines("myfile.txt")
```

#### Low-level I/O methods

IO classs has offers you the low-level operation at the class level., an example can be shown as below.

```
File.open("output.txt", "w") do  |f|
   f.print("Hello")
   f.syswrite(" there!")
end

puts File.read("output.txt")

```

the output might be a little different from what you might have expected, the reason is because the syswrite and print does not operate under the same rule.

```
 there!Hello
```

### 12.2.6 Writing to files
 
you can just use the normal File.puts or the  File.print method as you might with the STDIN/STDERR or ...

Ruby lets you economize on explicit closing of File objects—and enables you to keep your code nicely encapsulated—by providing a way to perform file operations inside a code block. We’ll look at this elegant and common technique next.

### 12.2.7 Using block to scope file operations

as we said before the scoped way is the prefeered way to handle File closing in Ruby. let's see another example below.

suppose that we have  a file 

```
Pablo Casals|Catalan|cello|1876-1973
Jascha Heifetz|Russian-American|violin|1901-1988
Emanuel Feuermann|Austrian-American|cello|1902-1942
```

and then we will read them back with the scoped operation.

```
File.open("records.txt") do |f|
  while record = f.gets
     name, nationality, instrument, date = record.chomp.split('|')
     puts "#{name} (#{date}), who was #{nationality}, played #{instrument}."
  end
end
```

### 12.8.8 File enumerablity
Thanks to the fact that Enumerable is among the ancestors of File, you can replace the While idiom with the following 

```
File.open("records.txt") do |f|
  f.each do |record|
     name, nationality, instrument, date = record.chomp.split('|')
     puts "#{name} (#{date}), who was #{nationality}, played #{instrument}."
     end
end
```

and you can do an inject operaton to the file directly here is an example .

```
count = 0 
total_age = File.open("member.txt") do |f|
   f.inject(0) do |total, line|
      count += 1
      fields  = line.split
      age =  fields[3].to_i
      total + age
  end
end

puts "Average age of group: #{total_age / count}."

```

the sample input is 
```
David Black male 49
```

### 12.2.9 File I/O exceptions and errors

When somethign goes wrong with file operations, bury raises an exception.  Most of the errors you'll get in the course of workign with files can be found in the _Errorno_ namespace.
e.g.

* Errno::ENOENT
* Errno::EISDIR
* Errno::EACCESS

in the system, each error is internally represented as a integer, the Errno has knowledge of the integer to which its corresponding system error maps.

## 12.2 Querying IO and File objects

if you desire to get attributes on a file or want to do some test, here it is.

The files that helps you with the querying are:

* File::State
* FileTest

beside the querying class, The File class also has some query methods.

e.g.

```
>> File.size("./README")
=> 2884
>> FileTest.size("./README")
=> 2884
>> File::Stat.new("./README").size
=> 2884
```


### 12.3.1 Getting information from the File class and the FileTest module

the classes can help you answering questions like below.

* what is it?
* what can it do?
* How big is it? 

I will show below with some examples on some of the quetsion

* Does a fie exits?

```
FileTest.exist?("/usr/local/src/ruby/README")
```

* Is the file directory? a regular file? a symbolic link?

```
FileTest.directory?("/home/users/dblack/info")
FileTest.file?("/home/users/dblack/info")
FileTest.symlink?("/home/users/dblack/info")
```

* Is a file readable? writable? executable?

```
FileTest.readable?("/tmp")
FileTest.writable?("/tmp")
FileTest.executable?("/home/users/dblack/setup")
```

* What is the size of this file? Is this a empty (zero bytes)?
```
FileTest.size("/home/users/dblack/setup")
FileTest.zero?("/tmp/tempfile")
```

### 12.3.2  Deriving file information with File::Stat

the File::Stat has the attribute correspnding to the structure in the standard C library 

```
File::Stat.new("README")
```

and you can as well do is first open the file and then call .stat file. 

```
File.open("README") { |f| f.stat }
```

the details willl not be covered here.  

## 12.4 Directory manipulation with the Dir class

to get hold of an Dir's instance, you can directly 
```
d = Dir.new("/usr/local/src/ruby/include")
```

### 12.4.1 Reading a directory's entries

YOu can get hold of the entries in one of the two ways., using the *entries* method or using the *glob* technique.

#### THE ENTRIES METHOD

```
>> d.entries
=> [".", "..", ".svn", "ruby", "ruby.h", "rubyio.h", "rubysig.h"]
```


you can as well call the Class-method as 
```
Dir.entires("/usr/local/src/ruby/include")
```

Let's shown an example that gives out the total size of the files inside a directory

```
d = Dir.new('C:\ProgramFiles\ruby-2.1.0\include\ruby-2.1.0\ruby')
entries = d.entries
entries.delete_if {|entry| entry =~ /^\./ }
entries.map! {|entry| File.join(d.path, entry) } 
entries.delete_if {|entry| !File.file?(entry) }

print "Total bytes: "
puts entries.inject(0) {|total, entry| total + File.size(entry) }
```

#### DIRECTORY GLOBBING

first let's introduce what is called the globbing, the globbing is something taken from the Unix shell, it has something like this ...

```
$ ls *.rb
$ rm *.?xt
$ for f in [A-Z]* # etc.
```

how to use the globbing, here it is .

* Dir.glob
* Dir.[]

e..g of the globbing is like below. 

```
>> Dir["/usr/local/src/ruby/include/*.h"]
=> ["/usr/local/src/ruby/include/ruby.h",
"/usr/local/src/ruby/include/rubyio.h",
"/usr/local/src/ruby/include/rubysig.h"]
```

the _glob_ can as well accept some flags.  e.g. File::FNM_CASEFOLD

```
Dir.glob("info*") #1 []
Dir.glob("info", File::FNM_CASEFOLD # ["Info", "INFORMATION"]
```

glob returns by default with the following options.

* Does not include filenames
* return full pathnames, not just filenames


so we can rewrite the code above with the code below.


```
dir = 'C:/ProgramFiles/ruby-2.1.0/include/ruby-2.1.0/ruby'
entries = Dir["#{dir}/*"].select {|entry| File.file?(entry) }
print "Total bytes: "
puts entries.inject(0) {|total, entry| total + File.size(entry) }
```

However, it seems that the code above does not work well on windows platform? ??

### 12.4.2 Directory manipulation and querying

we will learn something about the creation and removig the directories

Here are a complete example.

```
newdir = "/tmp/newdir"               #1
newfile = "newfile"

Dir.mkdir(newdir)                    #2
Dir.chdir(newdir) do                          #3
  File.open(newfile, "w") do |f|              #4
    f.puts "Sample file in new directory"
  end

  puts "Current directory: #{Dir.pwd}"       #5
  puts "Directory listing: "
  p Dir.entries(".")                         #6

  File.unlink(newfile)                       #7

end

Dir.rmdir(newdir)                            #8

print "Does #{newdir} still exist? "
if File.exist?(newdir)                         #9
  puts "Yes"
else
  puts "No"
end

```


## 12.5 File tools from the Standard library 

We will first look at the versatile FileUtils package and then at the more specialied but useful Pathname class. 


### 12.5.1 The FileUtils module 

Many of the method in FileUtils are named in honor of the System commands with Particlar command-line options. 


#### COPYING, MOVING, AND DELETING FILES

Firts will show you an example that does the copying( copying files to another file and coping of files to a directory) 
```
>> require 'fileutils'
=> true
>> FileUtils.cp("baker.rb", "baker.rb.bak")
=> nil
>> FileUtils.mkdir("backup")
=> ["backup"]
>> FileUtils.cp(["ensure.rb", "super.rb"], "backup")
=> ["ensure.rb", "super.rb"]
>> Dir["backup/*"]
=> ["backup/ensure.rb", "backup/super.rb"]
```

to remove a file recursively, unconditionally removes a directory , here it is 

```
>> FileUtils.rm_rf("backup")
=> ["backup"]
>> File.exist?("backup")
=> false
```

#### THE DRYRUN AND NOWRITE MODULES

If you want to see what would happen if you were to run particular FileUtils command, 

the dry run will gives you the output that represent the unix style comand. 
e.g.

```
>> FileUtils::DryRun.rm_rf("backup")
rm -rf backup
```

ir you want to prevent accident delete , yo can give it a  FileUtils::NoWrite call, here it is what you will get. 

```
>> FileUtils::NoWrite.rm("backup/super.rb")
=> nil
>> File.exist?("backup/super.rb")
=> true
```

### 12.5.2 The Pathname class

the Pathname class lets you create Pathname objects and query and manipulate them so you can determine the bae name, extension and other.

```
require 'pathname'
path = Pathname.new("/Users/dblack/hacking/test1.rb")
```


then you can examine the base, extensio and other parts of the path name.

```
>> path.basename
=> #<Pathname:test1.rb>
>> puts path.basename
test1.rb
>> path.dirname
=> #<Pathname:/Users/dblack/hacking>
>> path.extname
=> ".rb"
```

the path also has some navigation method such as ascend, here is the example. 

```
>> path.ascend do |dir|
?> puts "Next directory up: #{dir}"
>> end
```
it outputs 
```
Next directory up: /Users/dblack/hacking/test1.rb
Next directory up: /Users/dblack/hacking
Next directory up: /Users/dblack
Next directory up: /Users
Next directory up: /
```


### The StringIO class

StringIO let you treat string like IO objects, you can seek through them rewind them, and so forth.

we will see thourgh a use case, suppose that we have a DeCommenter class, which like this: 

```
module DeCommenter
  def self.decomment(infile, outfile, comment_re = /\A\s*#/)
    infile.each do |inline|
      outfile.print inline unless inline =~ comment_re
    end
  end
end
```

then we use it like this: 

```
File.open("myprogram.rb") do |inf|
   File.open("myprogram.rb.out", "w") do |outf|
   DeCommenter.decomment(inf, outf)
  end
end
```

but what if you write a test for the module? it is difficult to maintian input files but StringIO makes it easier by allowing all the code to stay in one place witout the need to write or read actual fiels.

with the StringIO you can do 


```
require 'stringio'
require 'decommenter'
string = <<EOM
# This is a comment.
This isn't a comment.
# This is.
# So is this.
This is also not a comment.
EOM
infile = StringIO.new(string)
outfile = StringIO.new("")
DeCommenter.decomment(infile,outfile)
puts "Test succeeded" if outfile.string == <<EOM
This isn't a comment.
This is also not a comment.
EOM
```


#### The open-url library 

the open-uri standard library packages lets you retrieve information from the network, using the HTTP and HTTPS protocols. 

```
require 'open-uri'
rubypage = open('http://www.ruby-lang.org')
puts rubypage.gets
```


### 12.6 Summary 

we have learned the following. 

IO and File class (File is a subclass to the IO class) 
FileUtils and Pathname are for manipulation of the standard-library faciliites, the StringIO class let you address the string as if it were an I/O stream.


# Ruby Dynamics

# 13. Object individuation

what will convered in this chapter include the following.

1. the singleton method, singleton method to Class or singleton method to object
2. extend method, which does something similar to module inclusion but for one object at time.


## 13.1 Where the singleton method are: the singleton class


Let's take a running leap at it, starting with the basic and including a quick review '

the most common singleton method is the class method.

```

class Car
  def self.makes
   %w{ Honda Ford Toyota Chevrolet Volvo }
  end
end
```

the ability to define method-driven behavior on a per-object basis is one of the hallmarks of Ruby's design.

### 13.1.1 Dula determination through singleton classs 
Ruby true to character, Evey object has two classes:

1. the class of which it's an instance
2. its singleton classs

"its singeleton class" is also known as the eigen-class

Joe's comment, you cannot compare the dual determination to the meta-class of the Python object.

### 13.1.2 Examing and modify a singleton class.

```
str = "I am a string"
class << str
  def twice
    self + " " + self
  end
end
puts str.twice
```

it is used by the `<< object` notation, which mens the "the anonymous, singleton class of object"

#### difference between the class << obj; def meth and def obj. obj?

the answer is that they are mostly the same, but with minor difference being, how the constant is resolved. 

```
N = 1
obj = Object.new
class << obj
  N = 2
end

def obj.a_method
  puts N
end

class << obj
  def another_method
    puts N
  end
end
obj.a_method  # output : 1 (Outer-level N)
obj.another_method  # output 2 (N belongs to obj's singleton class)
```

NOTE: By far the most frequent use of the class << object notation for entering a singleton-
method class is in connection with class-method definitions

#### DEFINING CLASS METHODS WITH CLASS <<

```
class Ticket
  class << self
    def most_expensive(*tickets)
      tickets.max_by(&:price)
    end
  end
end
```

which is the same as the

```
def Ticket.most_expensive(*tickets) # etc..
```


### 13.1.3 Singleton classes on the method-lookup path

#### INCLUDING A MODULE IN A SINGLETON CLASS
#### SINGLETON MODULE INCLUSION VS. ORIGINAL-CLASS MODULE INCLUSION


#### Some objects are more individualizable than others

1. first in own singleton class
2. look sin modules the singleton class may have
3. search proceed to the original class
4. repeat

Alsmot every object in Ruby can have methods added to it, the exceptions are instances of certain Numeric subclasses, including classes and floats, and symbols, if you try this:

`def 10.some_method; end`

you get syntax error, and you get a type error 
`class << 10; end `

### 13.1.4 Class methods in (even more) depth
You’re allowed to call C’s singleton methods on a subclass of C in addition to C because of a special setup involving the singleton classes of class objects. In our example, the singleton class of C (where the method a_class_method lives) is considered _the superclass of the singleton class of D_.

```

class C
end

def C.a_class_method
  puts "Singleton method defined on C"
end

C.a_class_method

class D < C
end
D.a_class_method

```

## 13.2 Modifying Ruby's core classes and modules

Ruby's classes and modules are opened, programmers can get under the hood of the language and change what it does - is one of the most important features of Ruby and also one of the hardest to come to terms with..  

### 13.2.1 The risk of changing core functionality

risk is that the changes are global.

One commonly cited candidate for d hoc change is the Regexp class.

#### CHANGING REGEXP#MATCH (AND WHY NOT TO)

You might get an error if you try to index one element on the failed match 

`some_regexp.match(some_string)[1]`

you might be tempted to do the following to avoid error when index nil.

```
class Regexp
  alias __old_match__ match
  def match(string)
    __old_match__(string) || []
  end
end
```

now, you are able to do 

`/abc/.match("X")[1]`

the problem is that the person using your code may depend on the match operation to return nil on failure. 

```
if regexp.match(string)
  do something
else
  do something else
end
```

that might fail.

#### THE RETURN VALUE OF STRING#GSUB! AND WHY IT SHOULD STAY THAT WAY

e.g. the String.gsub! operation result in returning `nil` when there is no change made.  which might blow things up.


#### the tap method 
As a side node, here is a tap method, the tap method performs odd but potentially useful task of executing a code block .

what tap does is, yield the receiver to the block and then return the receiver back... be careful of using the tap method, it might introduce complexity on his own.

back to the modifying the gsub! method , we might have this

```
class String
  alias __old_gsub_bang__ gsub!
  def gsub!(*args, &block)
     __old_gsub_bang__(*args, &block)
    self
  end
end
```

as above, the code will break when you try to find out if a substitute has ever happend.

### 13.2.2 Additive changes 

Most common category of changes to buildin Ruby classes is the additive change. 

Additive change is that it does not clobber existing Ruby methods.

#### SOME OLD STANDARDS: MAP_WITH_INDEX AND SINGLETON_CLASS

it is a common practice to write user's own version of the map_with_index

```
class Array
   def map_with_index 
      mapping = []
      each_with_index do |e, i|
        mapping << yield(e, i)
      end
      mapping
    end
end
```

and the code inaction would be 
```
cardinals = %w{ first second third fourth fifth }
puts [1,2,3,4,5].map_with_index {|n,i|
"The #{cardinals[i]} number is #{n}."
}
```

another example would be creating a method that captures the singleton class of an instance, here is the example.

```
class Object 
  def singleton_class
     class <<self
        self
     end
  end
end
```

and an example that uses it

```
david = Person.new 
def david.talk
  puts "HI"
end

dsc = david.singleton_class
if dsc.instance_methods.include?(:talk)
  puts "Yes, we have a talk method!"
end
```


### 13.2.3 Pass-through overrides


the pass-through means the old code is called along with the new code. here is the example as follow. 

```
class String
  alias __old_reverse__ reverse
  def reverse
    $stderr.puts "Reversing a string!"
    __old_reverse__
  end 
end

puts "David".reverse
```

there is a method version of the alias method, the name of the method is "alias_method"

consider the keyword form:
```
class String
alias __old_reverse__ reverse
```

as to the method form

```
class String
alias_method :__old_reverse__, :reverse
```

#### ADDITIVE/PASS-THROUGH HYBRIDS

It is an override that offers a superset of the functionality of the original method.

e.g. the ActiveSupport library that pats of Rails web application , has to_s that accepts overloaded parameters.


to see what has been overloaded for the to_s method, let's see some examples.

```
>> Time.now.to_s
=> "2008-08-25 07:41:40 -0400"

>> Time.now.to_s(:db)
=> "2008-08-25 07:46:25"
If you want the date represented

# and if you want to display the content as number format., 
>> Time.now.to_s(:number)
=> "20080825074638"

```


### 13.2.4 per-Object chagnes with extend

Object#extend is a kind of homecoming in terms of topic flow.


#### ADDING TO AN OBJECT’S FUNCTIONALITY WITH EXTEND

using extend except explicitly opening up the signleclass. 

```
module Secretive
  def name
   "[not available]"
  end
end

class Person
  attr_accessor :name
end

david = Person.new
david.name = "David"
matz.name = "Matz"
ruby = Person.new
ruby.name = "Ruby"
david.extend(Secretive)
ruby.extend(Secretive)

puts "We've got on person named #{matz.name}, " + 
   "one named #{david.name}, "   +
   "and one named #{ruby.name}. "
```

#### ADDING CLASS METHOD With EXTEND
if you write a singleton method on a class object, like so 

```
class Car
   def self.makes
     %w {Honda Ford Toyota CHevrolet Volvo }
   end
end
```

or like so 

```
class Car
  class << self
    def makes 
      %w {Honda Ford Toyota Chevrolet Volvo}
    end
   end
end
```

or with the extend method, while you first createa  Mixin, liek below. 

```
module Makers
   def makes 
      %w {Honda Toyota Chevrolet Volvo }
   end
end

class car 
  extend Makers
end

# or you can do more simply by 
Car.extend(Makers)
```

#### MODIFYING CORE BEHAVIOR WITH EXTEND

LEFT OUT FOR SIMPLICITY.

## BasicObject as ancestor and class

BasicObject sits at the top of the RUby's class tree, or any Ruby object _obj_, the followng is true 

`obj.class.ancestors.last == BasicObject`

### 13.3.1 Using BasicObject

BasicObject is the base of all object, while this barely have anything useful, the most useful thing inside the BasicObject is the method_missing. 

first let's check on some code. 

```
require 'rubygems'
require 'builder'
xml = Builder::XmlMarkup.new(:target => STDOUT, :indent => 2)
xml.instruct!
xml.friends do
  xml.friend(:source => "college") do
  xml.name("Joe Smith")
  xml.address do
    xml.street("123 Main Street")
    xml.city("Anywhere, USA 00000")
  end
 end
end
```
while it has uses the method_missing and it will translate the method_missing to a tag in the xml schema. 

you might expect the xaml to produce the following code.  

```
<?xml version="1.0" encoding="UTF-8"?>
<friends>
  <friend source="college">
  <name>Joe Smith</name>
  <address>
    <street>123 Main Street</street>
    <city>Anywhere, USA 00000</city>
  </address>
 </friend>
</friends>
```

### 13.3.2 Implementing a subclass of BasicObject

we will use an example to show you how to create a class that does the output of the Lister.

```
class Lister < BasicObject
  attr_reader :list
  def initialize
    @list = ""
    @level = 0
  end
  
  def indent(string) 
     " " * @level + string.to_s
  end
  
  def method_missing(m, &block)
    @list << indent(m) + ":"
    @list << "\n"
    @level += 2
    @list << indent(yield(self)) if block
    @level -= 2
    @list << "\n"
    return ""
  end
end
```

the key here is the code 

`@list << indent(yield(self)) if block`

where it has the yeild(self) call which will evaluate the block if it is defined (and the key here is that the block will receive the 'self' that is the Lister as the argument to the block) .

Now, with the code implemented, we can have the following. 

```
lister = Lister.new
lister.groceries do |item|
  item.name { "Apples" }
  item.quantity { 10 }
  item.name { "Sugar" }
  item.quantity { "1 lb" }
end
lister.freeze do |f|
  f.name { "Ice cream" }
end
lister.inspect do |i|
  i.item { "car" }
end

```
then you might get this back from the stdout 

```
groceries:
  name:
   Apples
  quantity:
    10
  name:
    Sugar
  quantity:
    1 lb
freeze:
  name:
    Ice cream
  inspect:
    item:
      car
```

## 13.4 Summary
In this chapter, you've seen some of the ways that Ruby objects live up to the philosophy of Ruby, which is what happpens at runtime is all about individual objects and what they can do at any given piont. 

# 14. Callable and Runnable objects

* in this chapter, Proc objects as anonymous functions 
* the lambda (a.ka.a proc) method
* Code blocks
* The Symbol#to_proc method 
* Methods objects
* Bindings
* The eval family of methods 
* Threads
* Executing external programs

This chapter is about objects that you can call, execute, or run: threads, anonymous functions, strings, even methods that have been turned into objects (rather than called by objects). 

## 14.1 asic anonymous functions: the Proc class

The main callable objects in Ruby are *methods* (which you've already seen), *Proc objects*, and *lambdas*.

lambda method, and the literal lambda constructor ->, there is a lot going on here, but it all fits together if you take it one layer at at time. 

### 14.1.1 Proc object

e.g of creating a proc object with a clode block 

`pr = Proc.new { puts "Inside a Proc's block" }`

when you are calling the code, the block that you provided is executed, thus you call the pr then it 

`pr.call`

NOTE: the lambda and the Proce.new create Procs that are different. 


### 14.1.2 Procs and blocks, and how they differ

block not necessary will be converted to Proc, e.g. 

```
[1,2,3].each{|x| puts x * 10 }
```

invovles a code block but does not create proc, yet the plot is the little thicker than that. 

```
def call_a_proc(&block)
  block.call
end

call_a_proc { puts "I'm the block .. or Proc.. Or something"}
```

also, it is possible for a proc to serve in place of code lbock in a method call, using a similar special syntax: 

```
p = Proc.new {|x| puts x.upcase }
%w {David Black}.each(&b)
```

#### SYNTAX (BLOCKS) AND OBJECTS (PROCS)

An important and often misunderstood fact is that a Ruby code block is not an object. The familar trivial example has a receiver, a dot operator, a method name, and a code block:

`[1,2,3].each {|x| puts x * 10 }`

NOTE: the code block is _part of the syntax_ of the method call. Code block isa syntactical construct ad not an object is that code blocks aren't method arguments.

### 14.1.3 Block-Proc conversions

Conversion between code block and the Proc is easy.

the methods are shown as below. 

#### CAPTURING A CODE BLOCK AS A PROC

```
def capture_block(&blok)
  puts "Got block as proc"
  block.call
end
capture_block {puts "Inside the block" }
```

#### USING PROCS FOR BLOCKS

shows you how ot call capture_block using a proc instead of a code block 

```
p = Proc.new { puts "This proc argument will serve as a code block." }
capture_block(&p)
```

remember that you stil neede the &, if you do this 
`capture_block(p)`

or this
`capture_block(p.to_proc)`

the proc is serves as a regular argument to the method, You aren't triggering the special behavior whereby a proc argument does the job of a code block .

#### GENERALIZING TO_PROC

you can add a to_proc method to any class, but the most useful are the Proc (discused earlier) and Symbol (discussed in the next section)  

```
class Person 
  attr_accessor :name
  def self.to_proc
      Proc.new {|person| person.name }
  end
 end
d = Person.new
d.name = "David"
m = Person.new
m.name = "Matz"
puts [d,m].map(&Person)
```

### 14.1.4 Using Symbol#to_proc for conciseness

the built-in mthod Symbol#to_proc comes into play in situation liike this: 

`%w{david black}.each(&:capitalize)`

the output is 
`["David", "Black"]`

the above code can be equivalent to the following .

`%w{ david black }.each {|str| str.capitalize }`

#### IMPLEMENTING SYMBOL#TO_PROC 

for the to_proc case for the symbol class, here it is:

`%w{ david black }.each(&:capitalize)`
We know it’s equivalent to this:
`%w{ david black }.each {|str| str.capitalize }`
And the same thing could also be written like this:
`%w{ david black }.each {|str| str.send(:capitalize) }`

if you take a look at the implementation of the Symbol class, here it is 

```
class Symbol
  def to_proc
     Proc.new {|obj| obj.send(self) }
  end
end
```

### 14.1.15 Procs as closures

You’ve also seen that code blocks preserve the variables that were in existence at the time they were created.

```
def multiply_by(m)
Proc.new {|x| puts x * m }
end
```

then cal it with the followingt code. 
```
mult = multiply_by(10)
mult.call(12)```
```

to show you the effect of the local context, here is the code 

```
def make_counter
  n = 0
  return Proc.new { n += 1 }
end

c = make_counter
puts c.call
puts c.call

d = make_counter
puts d.call

puts c.call
```

### 14.1.6 Proc parameters and arguments

remembers that we have method argument and the block argument, not sure if the Proc has the block argument semantic, but you can try the following code.  

```
pr = Proc.new  {|x| puts "called with argument #{x}" }
pr.call(100)
```

Procs differ from methods,  with respect to arguments handling, in that they don't care whether they get the right numnber of arguments, a one-argument proc, like this: 

```
>> pr = Proc.new {|x| p x }
=> #<Proc:0x401f326c@(irb):1>
```

can be called with any number of arguments. 

```
# if called with  no argument, it single parameters get set to nil:
>> pr.call
nil
```
if called with more than one, the first one is bound
```
>> pr.call(1,2,3)
1
```

if you do the argument sponge, such as the following. 

```
pr = Proc.new {|*x| p x }
pr.call
pr.call(1)
pr.call(1,2)
```

you will seee that the following output 
```
[]
[1]
[1, 2]
```

##14.2 Creating functions with lambda and ->

Like Proc.new , the lambda method returns a Proc object, using the provided code block as the function body: 

```
>> lam = lambda { puts "A lambda!" }
=> #<Proc:0x441bdc@(irb):13 (lambda)>
>> lam.call
A lambda!
```

as you can see that there is no lambda class, but a distinct lambda "flavor" of the Proc class. 

> First, lambdas require explicit creation. Wherever Ruby creates Proc objects implicitly, they’re regular procs and not lambdas. That means chiefly that when you grab a code block in a method, like this

> Second, lambdas differ from procs in how they treat the return keyword. return inside a lambda triggers an exit from the body of the lambda to the code context immediately containing the lambda. return inside a proc triggers a return from the method in which the proc is being executed.

we can examine the return in the lambda and the proc as such 

```
def return_test
   l = lambda  { return }
   l.call
   puts "Still here!"
   p = Proc.new { return }
   p.call
   puts "You won't see this messagew!"
end
``` 

> WARNING: Because *return* from inside a (non-lambda-flavored) proc triggers a return from the enclosing method, calling a proc that contains *return* where you are not inside the any method produces a fatal error ,to see a Demo of this error, try this `ruby -e 'Proc.new { return }.call'`

And there is a yet another difference

> Finally ,  and most important, is how they treat the argument, lambda-flavored procs don’t like being called with the wrong number of arguments. They’re fussy

## 14.3 Methods as objects

> Treating methods as objects involves “objectifying” them.


### 14.3.1 Capturing Method objects

```
class C
  def talk
     puts "Method-grabbing test! self is #{self}."
  end
end

c = C.new
meth = c.method(:talk)
```

> At this point, you have a Method object—specifically, a bound Method object

if you send a call message to `meth`, it knows to cal itself which c in the role of `self`

`meth.call`

you can unbind and bind it tno another objec t

```
class D < C
end
d = D.new
unbound = meth.unbind
unbound.bind(d).call
```

### 14.3.2 the rationale for method as object 

with some exampels to show that the "with unbound methods" can be useful, here is the idea

```
class A
  def a_method
    puts "Definition in class A"
  end
end

class B < A
  def a_method
   puts "Definition in class B (subclass of A)"
  end
end

class C < B
end
```


normally when you do 
`c.a_method` it calls the B's version of hte a_method, however, if you want to up the level, like the below. 

`A.instance_method(:a_method).bind(c).call`

you can even stash this behavior inside a method in a Class C
```
class C
  def call_original
    A.instance_method(:a_method).bind(self).call
  end
end
```

## 1.4.4 the eval faimily of methods 

like many languages, Ruby has a facility for executing code stored inthe form strings at runtime. 


the most straightforward method for evaluating a string as code, and the most dangerous, is the eval, 



### 14.4.1 Executing arbitrary strings as code with eval 

when you eval, you can pass in a separate Binding instance encapsulate the local variables bindings in feect at a given point in execution. 

the most useful part of the Binding object is in the position of second argument to eval, 

> thetop-level method called *binding* returns whatever the current binding is .

```
def use_a_binding(b)
  eval("puts str", b)
end

str = "I'm a string in top-level binding!"
use_a_binding(binding)
```


### 14.4.2 The dangers of eval 
it is dangerous, what if the user has something like below. 
`abc; end; system("rm  -rf /*"); #Don't do this !!`


### 14.4.3 the instance_eval method  


*instance_eval* is a specializded cousin of `eval`, it evalute the string or `code block `you give it, chaning `self` to the receiver of the call too `instance_eval`

```
p self 
a = []
a.instance_eval {p self }
```

> instance_eval is most useful for breaking in to what would normally be another object's private data

```
class C
  def initialize
    @x = 1
  end
end

c = C.new
c.instance_eval { puts @x}
```

> instance_exec
> a cousin to the `instance_eval` method, the `instance_exec` can take arguments, any arguments you pass it will be passed, in turn , to the code block 

e.g. 
```
string = 'A sample string"
string.instance_exec("s") {|delim| self.split(delim)}
```


### 14.4.4 the most useful eval: class_eval (a.k.a module_eval) 

in essence, *classs_eval* puts you inside a class-definition body:

```
c = Class.new
c.class_eval do
  def some_method
    puts "Created in class_eval"
  end
end

c = C.new
c.some_method
```

but why do you need such *class_eval* ,it was becuse you can do with the *class_eval* something that you can not do with the regular *class* keyword. 

* Evaluate a string in a class-definition context
* Open the class definition of any anonymous class (not just singleton classes)
* Use existing local variables inside a class definition body

the third is the most noteworthy. 

let's give an example to show the point 3. 


when you use the "class" keyword, you starts a new local-variable scope. and because of that, you cannot do the following - to open the class scope and puts the var, but you can do class_eval to put the vars. 

```
>> var = "initialized variable"
=> "initialized variable"
>> class C
>> puts var
>> end
NameError: undefined local variable or method `var' for C:Class
  from (irb):3
>> C.class_eval { puts var }
initialized variable
```
likewide, the following won't help, because the def method open a new scope as well. 

```
>> C.class_eval { def talk; puts var; end }
=> nil
>> C.new.talk
NameError: undefined local variable or method `var' for #<C:0x350ba4>
```

However, you can do the following 

```
C.class_eval { define_method("talk") { puts var }} 
>> C.new.talk
initialized variable
```

NOTE: you should not be using such technique often as the class and method-definition techniques.  

## 14.5 Parallel Exeuction with Threads

First we create a thread, and let it run 

```
Thread.new do
  puts "Starting the thread"
  sleep 1
  puts "At the end of the thread"
end
  
puts "Outside the thread"
```

you will get the following output, the reason why the separate thread does not run to completion is because the main thread has exit.

to let the background thread finish, you can do Thread.join
```
t = Thread.new do
  puts "Starting the thread"
  sleep 1
  puts "At the end of the thread"
end
  
puts "Outside the thread"
t.join
```


### 14.5.1 Killing, stopping and starting threads 

to exit a thread, call the Thread.exit method, a contrived example is as follow.


```
puts "Trying to read in some files..."
t = Thread.new do
  (0..2).each do |n|
  begin
    File.open("part0#{n}") do |f|
     text << f.readlines
   end
  rescue Errno::ENOENT
    puts "Message from thread: Failed on n=#{n}"
    Thread.exit
  end
 end
end

t.join
puts "Finished!"

```

you can stop and then awake it , by calling the Thread.stop followed by a t.wakeup clal.

```
t = Thread.new do
  puts "[Starting thread]"
  Thread.stop
  puts "[Resuming thread]"
end

puts "Status of thread: #{t.status}"
puts "Is thread stopped? #{t.stop?}"
puts "Is thread alive? #{t.alive?}"
puts
puts "Waking up thread and joining it..."
t.wakeup
t.join
puts

puts "Is Thread alive? #{t.alive?}"
puts "Ipsect string for thread: #{t.inspect}"
```

#### Fiber: vs. thread

the Fiber is what is used to impleent what is called the "coroutine". which can be yield back to their calling context multiple times. 

```
f = Fiber.new { puts "Hi."; Fiber.yield; puts "Nice day.";
iber.yield; puts "Bye!" }
f.resume
puts "Back to the fiber:"
f.resume
puts "One last message from the fiber:"
f.resume
puts "That's all!"

```

and the output 

```
Hi.
Back to the fiber:
Nice day.
One last message from the fiber:
Bye!
That's all!
```
and you can pass parameter to the fiber and its calling context, for details check other materials.


### 14.5.2 A Threaded date server

thisby example show you to create a Threaded Dated server

here is a server that responds to a single quest. 

```
require 'socket'
s = TCPServer.new(3939)
conn = s.accept
conn.puts "Hi. Here's the date."
conn.puts `date`
conn.close

```

then you can test the telnet application with the following command.

`telnet localhost 3939`

to accept more requests? put it inside a loop 

```
require 'socket'
s = TCPServer.new(3939)
while true
  conn = s.accept
  conn.puts "Hi. Here's the date."
  conn.puts `date`
 conn.close
end
```

now, a threaded one that back up (might be blocking client) is via the following.  

```
require 'socket'
s = TCPServer.new(3939)
while (conn = s.accept)
  Thread.new(conn) do |c|
    c.print "Hi. What's your name? "
    name = c.gets.chomp
    c.puts "Hi, #{name}. Here's the date."
    c.puts `date`
   c.close
  end
end
```

there is a chatters program, which broadcasts the messages to each of the chatter.

### 14.5.4 Threads and variables

Thread using code block, and code block can see variables createed in their local scope , that means Threads have closure. 

something are thread-local, in the face of thread, such as the $, $2, .., $n.

```
/(abc)/.match("abc")
t = Thread.new do
/(def)/.match("def")
puts "$1 in thread: #{$1}" # output : $1 in thread: def 
end.join
puts "$1 outside thread: #{$1}" # Output : $1 outside thread: abc
```

### 14.5.5 Manipulating thread keys 

thread can have a thread keys (is this a thread-local storage implementation?) 

a simple example would be 

```
t = Thread.new do
    Thread.current[:message] = "Hello"
end

t.join
p t.keys
puts t[:message]
```

we will check thhe thread keys with an example, such as 

not threaded one => 

```
module Games
  class RPS
    include Comparable
    WINS = [%w{ rock scissors },
           %w{ scissors paper },
           %w{ paper rock }]
           
  attr_accessor :move
  def initialize(move)
    @move = move.to_s
  end
  
  def <=>(other) 
  if move == other.move
   0
 elsif WINS.include?([move, other.move])
   1
 elsif WINS.include?([other.move, move])
  -1
  else
    raise ArgumentError, "Something's wrong"
  end
end

  def display(other)
     if self > other 
        self 
     elseif other > self
       other
     else
       false
     end
   end
 end
end
```

now with thread added in 

```
require 'socket'
require 'rps'
s = TCPServer.new(3939)
threads = []
2.times do |n|
  conn = s.accept
  threads << Thread.new(conn) do |c|
    Thread.current[:number] = n + 1
    Thread.current[:player] = c
    c.puts "Welcome, player #{n+1}!"
    c.print "Your move? (rock, paper, scissors) "
    Thread.current[:move] = c.gets.chomp
    c.puts "Thanks... hang on."
  end
end

a,b = threads
a.join
b.join

rps1, rps2 = Games::RPS.new(a[:move]), Games::RPS.new(b[:move])

winner = rps1.play(rps2)
if winner
  result = winner.move
else
  result = "TIE!"
end

threads.each do |t|
  t[:player].puts "The winner is #{result}!"
end

```


## 14.6 Issuing system commands from inside Ruby Programs

you can issue a command system , by the backtick (``). 

#### EXECUTING SYSTEM PROGRAMS WITH THE SYSTEM METHOD
e.g.
```
>> system("date")
Wed Feb 4 11:27:15 EST 2009
=> true
```

after executing, you can set the global variables `$?` to Process::Status object that contains information about the call. 

```
>> system("date")
Wed Feb 4 11:28:42 EST 2009
=> true
>> $?
=> #<Process::Status: pid 28025 exit 0>
```

`$?` is thread local 

#### CALLING SYSTEM PROGRAMS WITH BACKTICKS

> The main difference between system and backticks is that the return value of the backtick call is the output of the program you run

```
>> d = `date`
=> "Wed Feb 4 11:33:18 EST 2009\n"
>> puts d
Wed Feb 4 11:33:18 EST 2009
```
#### Some system command bells and whistles

you can run the `%$x` operator, such as 
`%x{date}`


### 14.6.2 Communicating with programs via open and popen3

#### 14.6.2 Communication with program via open and popen3


#### TALKING TO EXTERNAL PROGRAMS WITH OPEN 

```
>> d = open("|cat", "w+")
=> #<IO:0x1ccf28>
>> d.puts "Hello to cat"
=> nil
>> d.gets
=> "Hello to cat\n"
>> d.close
=> nil
```

we can leverage the block form of the open method 
```
>> open("|cat", "w+") {|p| p.puts("hi"); p.gets }
=> "hi\n"

```

#### TWO-WAY COMMUNICATION WITH OPEN3.POPEN3

the popen3 method opens communication with an external gives you handles on the extern al program's standard input, stand error stream,

```
>> require 'open3'
=> true
>> stdin, stdout, stderr = Open3.popen3("cat")
=> [#<IO:0x3a7758>, #<IO:0x3a771c>, #<IO:0x3a7668>,
#<Thread:0x3a74d8 run>]
>> stdin.puts("Hi.\nBye")
=> nil
>> stdout.gets
=> "Hi.\n"
>> stdout.gets
=> "Bye\n
```

and next example is the example that open the stdin, stdout and stderr with two threads. 


```
require 'open3'
stdin, stdout, stderr = Open3.popen3("cat")
t = Thread.new do
  loop { stdin.puts gets }
end

u = Thread.new do
  n = 0
  str = ""
  loop do
    str << stdout.gets
    n += 1
    if n % 3 == 0
       puts "--------\n"
       puts str
       puts "--------\n"
       str = ""
    end
  end
end

t.join
u.join
```



# Callbacks, hooks and runtime introspection 


In this chapter, we will cover the following 

* Runtime callback: inherited , included and more 
* the respond_to? and method_missing methods
* introspection of object and class method lists 
* Examing in-scope variables and constants 
* Parsing caller and stack trace information. 

> Thus you can rig a module so that a particular method gets called every time a class includes that module, or write a callback method for a class that gets called every time the class is inherited, and  so on.

## 15.1 Callbacks and hooks

callback and hooks are common meta-programming techniques , these methods are called when a particular event takes place during the run of a ruby program.  
* A nonexistent method being called on an object
* A module being mixed into a class or another module .
* An object being extended with a module
* A class being subclassed (inherited from)
* A reference being made to a nonexistent constant
* An instance method being added to a class
* A singleton method being added to an object


the callback are per-object or per-class, not global. 


### 15.1.1 Intercepting unrecognized messages with method_missing

an example of the method_missing method, 

```
class Cookbook
  attr_accessor :title, :author

  def initialize
    @recipes = []
  end

  def method_missing(m,*args,&block)
    @recipes.send(m,*args,&block)
  end
end
```

Ruby's method-delegating techniques
the method_missing example, we delegate the processing message to array @pages, we have a *Delegator* and the *SimpleDelegator*.


#### THE ORIGINAL: BASICOBJECT#METHOD_MISSING

you can define a top level method_missing , such as 

```

>> def method_missing(m,*args,&block)
>> raise NameError, "What on earth do you mean by #{m}?"
>> end
=> nil
>> a
NameError: What on earth do you mean by a?
  from (irb):2:in `method_missing'
>> BasicObject.new.a
NoMethodError: undefined method `a' for #<BasicObject:0x4103ac>
```

### 15.1.2 Trapping include operations with Module#included 

when a module is included in (mixed in to) a class, if a method called include is defined for that module, then that method is caled. the method receives the name of the class as its singele argument. 

```
module M
  def self.included(c)
    puts "I have just been mixed into #{c}."
  end
end

class C
  include M
end

```
then you can see that the message "I have just been mixed into C"


however, this example make little real case meaning, we might include a new class method with the "included" event. here is the example. 


```
module M
  def self.included(cl)
  def cl.a_class_method
    puts "Now the class has a new class method."
   end
  end

  def an_inst_method
    puts "This module supplies this instance method."
  end
end

class C
  include M
end

c = C.new
c.an_inst_method
C.a_class_method
```

### 15.1.3 Intercepting extend 

Module#extended method. 

extend event can also be extended .

```
module M
  def self.extended(obj)
    puts "Module #{self} is being used by #{obj}."
  end

  def an_inst_method
     puts "This module supplies this instance method."
  end
end

my_object = Object.new 
my_object.extend(M)
my_object.an_inst_method 
```

the output from the listing 15.2 is 
```
Module M is being used by #<Object:0x28ff0>.
This module supplies this instance method.
```

### 15.1.3 SINGLETON-CLASS BEHAVIOR WITH EXTENDED AND INCLUDED

extending an object with a module is the same as including that module in the object singleton classes. 

```
module M
  def self.included(c)
    puts "#{self} included by #{c}."
  end
  def self.extended(obj)
    puts "#{self} extended by #{obj}."
   end
end

obj = Object.new
puts "Including M in object's singleton class:"
class << obj
  include M
end

puts

obj = Object.new
puts "Extending object with M:"
obj.extend(M)
```

and the output from List above is as follow. 

```
Including M in object's singleton class:
M included by #<Class:#<Object:0x1c898c>>.

Extending object with M:
M extended by #<Object:0x1c889c>.
```

### 15.1.4 Intercepting inheritance with Class#Inherited 

there is a limit on the inheritance, while you can inherit from C to D, where C is the super class to D, however, you cannot make C's instance class 's inherited triggered. 

here is the example. 

```
class 
  class << self 
     def self.inherited
       puts "Singleton class of C just got inherited"
       puts "But you'll never see this message"
    end
  end
  
  class D < C
     class << self 
       puts "D's singleton class now exists, but no callback!"
      end 
   end
 end
 ```
 
 where  the output is 
 ```
 D's singleton class now exists, but no callback!
 ```
 
 ### 15.1.5 The Module#const_missing method 
 
 const_missing iss another commonly used callback, s the name implies, this method is called when a unidentifiable constant is referred to inside a given module or class. 
 
 ```
class C
  def self.const_missing(const)
    puts "#{const} is undefined—setting it to 1."
    const_set(const,1)
  end
end

puts C::A
puts C::A

```

### 15.1.6 the method_added and singleton_method_added methods 

we can capture the event on the names implies. 
```
class C
  def self.method_added(m)
    puts "Method #{m} was just defined."
  end
  
def a_new_method
end
end
```

there is a also a singleton_method_added callback does much the same thing. 

the examples are ignored. 

## 15.2 Interpreting object capability queries  

you can query a object's capability 

### 15.2.1 Listing an object's non-private methods 

you can query what method are available, here. 


```
>> string = "Test string"
=> "Test string"
>> string.methods.grep(/case/).sort
=> [:casecmp, :downcase, :downcase!, :swapcase, :swapcase!, :upcase,
:upcase!]
```

we can leverage methods a bit further, we can do complex operations. 
```
string = "Test string"
methods = string.methods
bangs = string.methods.grep(/.!/)
unmatched = bangs.reject do |b|
  methods.include?(b[0..-2].to_sym)
end

if unmatched.empty?
  puts "All bang methods are matched by non-bang methods."
else
  puts "Some bang methods have no non-bang partner: "
  puts unmatched
end
```

### 15.2.2 Listing Private and protected methods

we can query private methods and no protected methods, example. 

```
>> object = Object.new
=> #<Object:0x3a1a24>
>> object.private_methods.size
=> 66
>> object.protected_methods.size
=> 0
```

#### Method queries, method_missing, and respond_to?

while the respond_to? method might only return if a pblic method can be responded to, but it does not considered the method_missing. 

### 15.2.3 Getting class and module instance methods

Classes and modules come with a somewhat souped-up set of method-querying methods.

there are more methods here .

* instance_methods return all public and protected instance methods 
* public_instance_methods returns all public instance methods 
* protected_instance_methods and private_instance_methods return all protected and private instance method ,respectively. 

where you can find out the instance methods pertaining to that class. 

```
>> Range.instance_methods(false).sort
=> [:==, :===, :begin, :cover?, :each, :end, :eql?, :exclude_end?, :first,
:hash, :include?, :inspect, :last, :max, :member?, :min, :step, :to_s]
```

#### GETTING ALL THE ENUMERABLE OVERRIDES 



## 15.3 Introspection of variables and constants

ruby can tell which variables and constants that you have access to at a given point of time. 

### 15.3.1 Listing local, global, and instance variables

to get access to the global variabes are straightforward, you use the top-level method local_variables, and global_variables. In this case, you get back an array of symbols corresponding to the local or global variables of a class or module, and the constatnts of a class or module. 

```
x = 1
p local_variables
[:x]
```

and to get he global variables, you can simply ydo the following. 


```
p global_variables
[:$;, :$-F, :$@, :$!, :$SAFE, :$~, :$&, :$`, :$', :$+, :$=,
:$KCODE, :$-K, :$,, :$/, :$-0, :$\, :$_, :$stdin, :$stdout,
:$stderr, :$>, :$<, :$.,...
```

Not that the local_variables and global_variables don't give you the values of the variables they report on.

```
class Person
  attr_accessor :name, :age
  def initialize(name)
   @name = name
  end
end

david = Person.new("David")
david.age = 49

p david.instance_variables
```

## 15.4 Tracing execution 

the *caller* method provides an array of string, Each string represents one step in the stack trace. 

the method is the `caller`.

```
def x
  y
end
def y
 z
end
def z
  puts "Stacktrace: "
  p caller
end
x
```


we might get back a stack trace, courtesy of `caller`, here is the output from running trace demo.rb.


### 15.4.2 Writing a tool for parsing stack traces

here in an example that we wil discuss a tool that can be developed by ourselves, which does the parsing of the output (store that in to a class called `Call` object)

```
module CallerTools
  class Call
   CALL_RE = /(.*):(\d+):in `(.*)'/
   attr_reader :program, :line, :meth
  def initialize(string)
    @program, @line, @meth = CALL_RE.match(string).captures
  end
  def to_s
   "%30s%5s%15s" % [program, line, meth]
  end
end

```

#### THE CALLLERTOOLS::sTACK CLASS

where the call stack class will stored a list of Call objects, which can help in displaying the Call objects. 

```
class Stack
  def initialize
    stack = caller
  stack.shift
  @backtrace = stack.map do |call|
    Call.new(call)
  end
end

def report
  @backtrace.map do |call|
    call.to_s
  end
end

def find(&block)
  @backtrace.find(&block)
  end
end

```
#### USING THE CALLERTOOLS MODULE
now that you can use the CALLERTOOLS MODULE, here is the code 

```
require 'callertools'

def x 
  y 
end

def y 
  z
end

def z 
  stack = CallerTools::Stack.new
  puts stack.report
end

x
```


## 15.5 Callbacks and method inspection in practise
we will show an example that uses implements a MicroTest, a tiny test framework, just as to show how to write a tool with the inspection turned on 

### 15.5.1 The MicroTest background : MiniTest

MiniTest is a test framework that shipped with Ruby installation. 

Again suppose that we have the PlayingCards class, here it is (for revisiting) 


```
module PlayingCards
  RANKS = %w{ 2 3 4 5 6 7 8 9 10 J Q K A }
  SUITS = %w{ clubs diamonds hearts spades }
  class Deck
    def initialize
      @cards = []
      RANKS.each do |r|
        SUITS.each do |s|
          @cards << "#{r} of #{s}"
        end
     end
     @cards.shuffle!
   end
   
   def deal(n=1)
     n.times.map { @cards.pop }
   end
   def size
     @cards.size
   end
 end
end
```

now with the MiniTest framework, you might just as well write the unit test as such 

```
require 'minitest/unit'
require 'minitest/autorun'
require 'cards'

class CardTest < MiniTest::Unit::TestCase
  def setup
    @deck = PlayingCards::Deck.new
  end

 def test_deal_one
   @deck.deal
   assert_equal(51, @deck.size)
  end
  def test_deal_many
    @deck.deal(5)
    assert_equal(47, @deck.size)
  end
end
```

### 15.2.2 Specyfing and implementing MicroTest


what we want from the MicroTest utility.


* Automatic execution of the setup method and test methods, based on the class inheritance.
* A simple assertion method that either succeeds or fail.

the basic principle is the same as most of other language but there are somethign that is not present in other language, they are

* callback , method added, clas inherited


while, it does have some limitation comparing to the other languages, such as Java/C#, in that 

* it does not have some annotation type system, which make it disadvantageous in terms of declarative way of programing. 

let' s see the mock up implementation of the MicroTest as below. 

```
require 'callertools'
class MicroTest
  def self.inherited(c)
    c.class_eval do
      def self.method_added(m)
        if m =~ /^test/
          obj = self.new
          if self.instance_methods.include?(:setup)
            obj.setup
          end
          obj.send(m)
        end
      end
    end
  end

  def assert(assertion)
    if assertion
      puts "Assertion passed"
      true
    else
      puts "Assertion failed:"
      stack = CallerTools::Stack.new
      failure = stack.find {|call| call.meth !~ /assert/ }
      puts failure
      false
    end
  end
  def assert_equal(expected, actual)
    result assert(expected == actual)
   puts "(#{actual} is not #{expected})" unless result
   result
  end
end
```
 

then to use it ? here ist the code that shows you some how to ?

```
require 'microtest'
require 'cards'

class CardTest < MicroTest
  def setup
    @deck = PlayingCards::Deck.new
  end
  def test_deal_one
    @deck.deal
    assert_equal(51, @deck.size)
  end
  def test_deal_many
    @deck.deal(5)
    assert_equal(47, @deck.size)
  end
end
```