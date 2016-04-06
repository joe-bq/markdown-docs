## Introduction 

this page will contains some use tips on the python language, well, we will focuse  on how to effectively use the Python classes and others to assist working python language itself.

## how to get qualify names inside nested names

you can get access to the Python object through the use of qualified names (explicitly qualified names) the implicit rules does not apply 
here is an example 

```
class LayoutProcessor:
    class Layout:
        class Document:
            def __init__(self): pass
        def __init__(): pass
        def next_document(self):
            doc = LayoutProcessor.Layout.Documenet(...)
    def __init__(self): pass
    def next_layout(self):
        layout = LayoutProcessor.Layout(...)
```

so as you are now aware you need to qualify the names starting from the top level of the code, which the outer-most symbol name is `LayoutProcessor` so that you have to start your code with the `LayoutProcessor`;
    
## you will need to explicitly return from a function if you want to 
Python don't make the assumption that the last expression of a function becomes the function's return value.

NO, it DOES NOT.

what you will need to do is that you will have to explicitly return the values from the python code . 

```
def __is_match(self, line):
   if self.doc_reg.search(line) True else False
if __name__ == "__main__":
   if __is_match(obj, line) is None: 
      print("None")
   elif __is_match(obj, line): 
      print("True")
   else:
      print("False")
```

the value None is returned because you don't return from the python code, the desired way is to write as follow.

```
def __is_match(self, line):
   return if self.doc_reg.search(line) True else False
if __name__ == "__main__":
   if __is_match(obj, line) is None: 
      print("None")
   elif __is_match(obj, line): 
      print("True")
   else:
      print("False")
```

then it shall return "True" or "False"

## A utility to process the layout configuration and others
we have the following structure 
Layouts Configurations 
    --- Layout
        --- Documents
        
Where the document has been exported by some tool which made it hard to process because of it has to be escaped so that it be used by the tool to process them correctly. so that you can find some string like this: 
```
   &lt;Name value="711a21e0-bdab-4412-9849-2adde02d9f38"/&gt;
```

While  in this case we cannot process it directly via xml, we can of cause by first translate the escaped xml strings to xml and then process the xml, but later we have to persist it back to to escaped xml strings.

to help proces the exported data, I build a tool to help me to do it. I used the following technology in building the tool, they are:

* nested types 
* Nested Method 
* Static/Class method 
* Plan to use singleton class (but failed to use them ) 
* some pattern to chain patttern but with ability to rewind
* regular expression instead of the xml elemnt tree

the code is as follow, 

```
import sys
import re
'''
this program does 

  python input_to_output.py < input > output 

  line by line copy of the content 

'''

class Transcriber:
	def __init__(self, fin = sys.stdin, fout = sys.stdout):
		self.fin = fin
		self.fout = fout
	def execute(self):
		if self.fin is not None:
			for line in self.fin:
				self.fout.write(line + "\n")

class LineUtil:
	@staticmethod
	def is_null_or_empty(line):
		if line is None or line == '': 
			True
		else:
			False


class LayoutProcessor:
	class Layout:
		class Document:
			def __init__(self, layout, fin = sys.stdin, fout = sys.stdout, ferr = sys.stderr):
				self.layout = layout
				self.fin = fin
				self.fout = fout
				self.ferr = ferr
				self.guid = ""
				self.name = ""
				self.prodider_type = None
				self.prefetched_line = ''
			def next(self):
				if self.guid is not None and self.guid != "" and self.name != '':
					self.fout.write(self.guid + ", " + self.name + "\n")
				while self.fin:
					line = self.fin.readline()
					if line == '':
						break
					if LineUtil.is_null_or_empty(line):
						break
					if self.seek_prefetch(line):
						self.layout.prefetched_line = line
						break
			def seek_prefetch(self, line):
				'''Seek with prefected lines it should delegate the job to the parent to determine if 
				the prefetched line is something shall be hanlded by the parent'''
				if line is None or line == '':
					return False
				else:
					return self.layout.seek_prefetch(line)
					# support certains type of prefetch and rolling up the chain

		def __init__(self, layoutProcessor, fin = sys.stdin, fout = sys.stdout, ferr = sys.stderr, print_only_match = True):
			self.layoutProcessor = layoutProcessor
			self.fin = fin
			self.fout = fout
			self.ferr = ferr
			self.doc_reg = re.compile("Name value=\"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})\"")
			self.doc_displayname_reg = re.compile("DisplayName value=\"([^\"]+)\"")
			self.print_only_match = print_only_match
			self.doc = None
			self.prefetched_line = ''
		def next_document(self):
			def step_next_document(obj, line):
					if line == '':
						return
					match = self.doc_reg.search(line)
					if match is not None:
						if not self.doc:
							self.doc = LayoutProcessor.Layout.Document(self, self.fin, self.fout, self.ferr)
						self.doc.name = match.group(1)
					else:
						match = self.doc_displayname_reg.search(line)
						if match:
							if not self.doc:
								self.doc = LayoutProcessor.Layout.Document(self, self.fin, self.fout, self.ferr)
							self.doc.guid = match.group(1)
					if self.doc is not None and self.doc.guid != '' and self.doc.name != '':
						self.doc.next()						

			while self.fin:
				line = self.fin.readline()
				if line == '':
					break
				self.pretched_line = ''
				## JOE 
				## since the function step_next_document is defined nested in next_document, its scope is local to the 
				#   next_document method, so ther is no need to do self.step_next_document() and it is error to do self.step_next_document()
				step_next_document(self, line)
				## While __is_match method is defined in the class where 'next_document' is defined, so that the self.next_document has to be qualified
				if not LineUtil.is_null_or_empty(self.prefetched_line):
					if self.__is_match(self.prefetched_line):
						step_next_document(self, self.prefetched_line)
					elif self.seek_prefetch(self.prefetched_line):
						self.layoutProcessor.prefetched_line = self.prefetched_line
						break

				
		def seek_prefetch(self, line):
			if line is None or line == '':
				return False
			else:
				if not self.__is_match(line):
					return self.layoutProcessor.seek_prefetch(line)
				else:
					return True
		def __is_match(self, line):
			search = self.doc_reg.search(line)
			return  True if search is not None else (
						True if self.doc_displayname_reg.search(line) else (
							False))
	def __init__(self, fin = sys.stdin, fout = sys.stdout, ferr = sys.stderr):
		self.fin = fin
		self.fout = fout
		self.ferr = ferr
		self.name = ""
		self.layout_reg = re.compile("Element category=\"Your:App:LayoutConfig\" id=\"([^\"]+)\"")
		self.prefetched_line = ''

	def next_layout(self):
		def step_next_layout(obj, line):
			if line == '':
				return
			#self.fout.write("Layout: {0}".format(line))
			match = obj.layout_reg.search(line)
			if match is not None:
				layout = LayoutProcessor.Layout(obj, obj.fin, obj.fout, obj.ferr)
				layout.name = match.group(1)
				layout.next_document()

		while self.fin:
			line = self.fin.readline()
			if line == '':
				break
			self.prefeched_line = ''
			step_next_layout(self, line)
			if not LineUtil.is_null_or_empty(self.prefetched_line):
				if self.__is_match(self.prefeched_line):
					step_next_layout(self, self.prefetched_line)


	def seek_prefetch(self, line):
		if LineUtil.is_null_or_empty(line):
			return False
		else:
			return self.__is_match(line)
	# Joe : 
	#  Private Methods: 
	#   http://www4.ncsu.edu/~kaltofen/courses/Languages/PythonExamples/python-lectures/_build/html/lectures/three.html#private-methods
	def __is_match(self, line):
		search = self.layout_reg.search(line)
		# True if search is not None else False
		if search is not None:
			return True
		else:
			return False
	def __search_get_name(self, line):
		search = self.layout_reg.search(line)
		return search.Group(1) if search is not None else None

if __name__ == '__main__':
	lp = LayoutProcessor()
	lp.next_layout()
```

After this project (this tool), I had the following havest/gain, reap:

* Python is *explicit*, if you want to return something, returns it, don't expect the last expression will help return the value you want
* To hide something, uses ‘__', which means it won't be usable outside the class it is defined (there might be runtime checks before you do __identifiers)
* Types, Method, all can be nsted, the nested gives you better organization and information hiding (so this is a advanced private mechanism than the __tricks)
* It is flexible most readable, take the comparison to None for e.g. you can  either do `if a is not None:` or do `if a:`, or `if not a` if an negate condition is what you want to get 
* The magic of decorator, decorator is class/method factory, with which you can create new class/method with decorated attached.
* Method is also an object, so that you can see `method.attribute = value`, the attributes of Python is all backed by the internal ```__dict__``` hash
* the power of Python comes from the `__get__`, `__set` method, which built the contract between the class and the runtime  which it is in . Such `core atttributes` defines the shape of the Pythohn object
* `__meta__` class is the template of a type, it is the type of type, the method of _____metaclasss_____ becomes the class method of the type which has it as the metaclass.
* new object and old object, new objects are objects that inherits from the class 'object', while the object do not have defined base class.  

## _____new_____ and _____init_____

_____new_____ takes care of the instance creation 
_____init_____ takes care of the instance initialization

it might be same in your eye, they are quite different, while an object is created, the normal process is as follow.

First _____new_____ is called , which takes cares normally by the 'type' class, then the __init__ method should be called. with this knowledge in mind, let's try to do some singleton with overriding the _____new_____ method. 

```
class Singleton(object):
  _instance = None
  def ___new__(cls, *args, **kwargs):
    if not cls.instance:
        cls._instance = super(Singleton, cls).__new__(*args, **kwargs)
    return cls._instance
```

while to test this code, you can write the following code.  

```
if __name_ '__main__':
    f1 = Singleton()
    f2 = Singleton()
    if id(f1) == id(f2): # you can write as if f1 is f2:
      print "the same"
    else:
       print "the same"
```

However, this has the issue that the __init__ method of `Singleton` will be run twice, reason

1. Singleton() means will run into the __new__ method of Singleton, while the Singleton() method will also call __init__ after the __new__ method 
2. the Singleton.__new__ method calls into the super(Singleton, cls).__new__... which in turns will call __init__ again.

beside the major __init__ called twice issue, there are other issues related to the above code. 

1. the 'Singleton' symbol direclty inside the super(Singleton, cls).__new__ method, what if we have a derived class to Singleton classs.?


Some reap/harvest that we had so far:
1. `id(a) == id(b)` can be written as `a is b`
2. `super(ChildType, inst)` as well as `super(ChildType, cls)` (depending on the context) now in Python 3.0 can be simply write as `super().__some_method__`

## try to implements my_class_method decorator
NOT DONE!

the initial idea, declare a global function which has the following signature 

```
def my_class_method(cls, *arg, **kwargs):
  pass
```


## define my own my_static_method decorator

NOT DONE!

you can define your own static method decorator, where you can just do the following
```
def my_static_method(*args, **kwargs)
  pass
```


## null, nil, and None

while the major languages has used all the synonyms for no value. 
in c/C++/c#/java, it is null which is used. 
in perl/ruby/lisp, it is nil which is useed 
in Python, it is None which is used. 