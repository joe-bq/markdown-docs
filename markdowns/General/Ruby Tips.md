## Introduction 
this page will introduce you the ruby language by codecademy, where the codecademy is from [Ruby | Codecademy](https://www.codecademy.com/en/tracks/ruby)

## contents
1. combined operand

`<=>`

e.g.

```words.sort! { |first, second| second <=> first }```



2. special way of saying symbol
```
menagerie = { :foxes => 2,
  :giraffe => 1,
  :weezards => 17,
  :elves => 1,
  :canaries => 4,
  :ham => 1
}
```

3. symbol is a special concept in ruby

```
to_sym
string.intern
```
convert to a symbol

4. to_x method, 
where the x can be s for string, i for integer, d to double... ,sym for symbol

5. well, the older hash syntax is 
```
menagerie = { :foxes => 2,
  :giraffe => 1,
  :weezards => 17,
  :elves => 1,
  :canaries => 4,
  :ham => 1
}
```
the new one is 

```
menagerie = { :foxes => 2,
  giraffe: 1,
  weezards: 17,
  elves: 1,
  canaries: 4,
  ham: 1
}
```
6. select
```
movie_ratings = {
  memento: 3,
  primer: 3.5,
  the_matrix: 3,
  truman_show: 4,
  red_dawn: 1.5,
  skyfall: 4,
  alex_cross: 2,
  uhf: 1,
  lion_king: 3.5
}
good_movies = movie_ratings.select{|name, rating| rating > 3}
```

there is functions with the following names.

```
	each_key
	each_value
```

7. check null?
```
	movies[title.to_sym].nil?
	movies[title.to_sym] == nil
```
8.

case.. when .. statements
```
movies =  {wind: 3.4, intestellar: 3, gravity: 4}
puts "please input choice"
choice = gets.chomp

case choice
when "add"
    puts "Added!"
when "update"
    puts "Updated!"
when "delete"
    puts "Deleted!"
else
    puts "Error!"
end
```

9. if modifier unless modifiers languages.

10. conditional assignmnet

11. upto and downto

95.upto(100) {|num| print num, " "}

12. repond_to? reflection getting started

13. shove and pop - the `<<`- the append operator

```
alphabet = ["a", "b", "c"]
alphabet << "d" # Update me!

caption = "A giraffe surrounded by "
caption << "weezards!" # Me, too!
```
14. string interoplation



15. reflection `is_a?`

```
$VERBOSE = nil    # We'll explain this at the end of the lesson.
require 'prime'   # This is a module. We'll cover these soon!

def first_n_primes(n)

  unless n.is_a? Integer
    return "n must be an integer."
  end

  if n <= 0
    return "n must be greater than 0."
  end
  
  prime_array = [] if prime_array.nil?
  
  prime = Prime.new
  for num in (1..n)
    prime_array.push(prime.next)
  end
  return prime_array
end

first_n_primes(10)
```
16. Collect methods - what is the difference between collect and select?

collect does select.. 


17. Ruby's yield is not the same as the python's yield - this is called the co-routine strategy

```
def block_test
  puts "We're in the method!"
  puts "Yielding to the block..."
  yield
  puts "We're back in the method!"
end

block_test { puts ">>> We're in the block!" }

and 

def double(n)
    yield(n)
end

double(10) {|n| n * 2}
```
18. you can create Proc using block

```
multiples_of_3 = Proc.new do |n|
  n % 3 == 0
end

(1..100).to_a.select(&multiples_of_3)

```

18. Proc.new can be called with .call
19. symbol to proc conversion, which is really common in ruby
```
numbers_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

strings_array = numbers_array.map(&:to_s)
```
20. lambda are identical to Proc (not all the same)

	lambda check parameter passed to it
	lambda passes control back to calling method, proc does not 

>A block is just a bit of code between do..end or {}. It's not an object on its own, but it can be passed to methods like .each or .select.
A proc is a saved block we can use over and over.
A lambda is just like a proc, only it cares about the number of arguments it gets and it returns to its calling method rather than returning immediately.


21. define classes

```
class Language
  def initialize(name, creator)
    @name = name
    @creator = creator
  end
	
  def description
    puts "I'm #{@name} and I was created by #{@creator}!"
  end
end

ruby = Language.new("Ruby", "Yukihiro Matsumoto")
python = Language.new("Python", "Guido van Rossum")
javascript = Language.new("JavaScript", "Brendan Eich")

ruby.description
python.description
javascript.description
```

22. global, local, instance, class variables.

global variables.
```

class MyClass
  $my_variable = "Hello!"
end

puts $my_variable
```


class variables
```

class Person
  # Set your class variable to 0 on line 3
  @@people_count = 0
  
  def initialize(name)
    @name = name
    # Increment your class variable on line 8
    @@people_count += 1
  end
  
  def self.number_of_instances
    # Return your class variable on line 13
    @@people_count
  end
end

matz = Person.new("Yukihiro")
dhh = Person.new("David")

puts "Number of Person instances: #{Person.number_of_instances}"
```

23. reflection - `block_given?`

```
def create_record(attributes, raise_error = false)
  record = build_record(attributes)
  yield(record) if block_given?
  saved = record.save
  set_new_record(record)
  raise RecordInvalid.new(record) if !saved && raise_error
  record
end
```

24. inherit syntax


`ClassA < ClassB`


25. Class method and self. (class method) 


26. Object oriented programming


27. attr_reader, attr_writer


28. Module. ? is there namespace?
```
module Math
PI = 3.14
end


puts Math::PI
```

29. to use module 


```
require 'date'
puts Date.today
```

or 

```
include Math
```


30. Module is to implement the Mixin - include 

```
module Action
  def jump
    @distance = rand(4) + 2
    puts "I jumped forward #{@distance} feet!"
  end
end

class Rabbit
  include Action
  attr_reader :name
  def initialize(name)
    @name = name
  end
end

class Cricket
  include Action
  attr_reader :name
  def initialize(name)
    @name = name
  end
end

peter = Rabbit.new("Peter")
jiminy = Cricket.new("Jiminy")

peter.jump
jiminy.jump
```


- extend 


> Whereas include mixes a module's methods in at the instance level (allowing instances of a particular class to use the methods), the extend keyword mixes a module's methods at the class level.