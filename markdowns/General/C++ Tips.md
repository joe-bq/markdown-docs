## Introduction
this page will introduce you some of the new C++ 11/C++ 14 features.

one of the features that C++ is move semantic.

from the [c++ - What are move semantics? - Stack Overflow](http://stackoverflow.com/questions/3106110/what-are-move-semantics) there are two contributor who answered the questions.

1. highlight of "copy and swap idiom".

one simple explaination is as follow.

> C++0x introduces a new mechanism called "rvalue reference" which, among other things, allows us to detect rvalue arguments via function overloading. All we have to do is write a constructor with an rvalue reference parameter. Inside that constructor we can do anything we want with the source, as long as we leave it in some valid state:

```
string(string&& that)   // string&& is an rvalue reference to a string
    {
        data = that.data;
        that.data = 0;
    }
```

as comparing to the copy semantic 

```
 ~string()
    {
        delete[] data;
    }

    string(const string& that)
    {
        size_t size = strlen(that.data) + 1;
        data = new char[size];
        memcpy(data, that.data, size);
    }
```
which creates a lot of temporaries and calls to the memory management system.

2. number2 highlight Move semantice with the Auto_ptr.. NRVO (Named return value optimization).


#### what is a move?
about auto_ptr
> its purpose is to guarantee that a dynamically allocated object is always released, even in the face of exceptions:

as a comparison.

this is how visualized 

```
auto_ptr<Shape> a(new Triangle);

      +---------------+
      | triangle data |
      +---------------+
        ^
        |
        |
        |
  +-----|---+
  |   +-|-+ |
a | p | | | |
  |   +---+ |
  +---------+

auto_ptr<Shape> b(a);

      +---------------+
      | triangle data |
      +---------------+
        ^
        |
        +----------------------+
                               |
  +---------+            +-----|---+
  |   +---+ |            |   +-|-+ |
a | p |   | |          b | p | | | |
  |   +---+ |            |   +---+ |
  +---------+            +---------+
```

and this is how it might be implemented.

```
auto_ptr(auto_ptr& source)   // note the missing const
{
    p = source.p;
    source.p = 0;   // now the source no longer owns the object
}
```

#### Dangerous and harmless moves

what is dangerous?

```
auto_ptr<Shape> a(new Triangle);   // create triangle
auto_ptr<Shape> b(a);              // move a into b
double area = a->area();           // undefined behavior
```

well, it is not always dangerous, 

```
auto_ptr<Shape> make_triangle()
{
    return auto_ptr<Shape>(new Triangle);
}

auto_ptr<Shape> c(make_triangle());      // move temporary into c
double area = make_triangle()->area();   // perfectly safe
```


#### Value categories

which basically illustrate the lvalues and rvalues, however, from the post

> Note that the letters l and r have a historic origin in the left-hand side and right-hand side of an assignment. This is no longer true in C++, because there are lvalues which cannot appear on the left-hand side of an assignment (like arrays or user-defined types without an assignment operator), and there are rvalues which can (all rvalues of class types with an assignment operator).

#### Rvalue references

the syntax of a rvalue references is `x&&`

```
            lvalue   const lvalue   rvalue   const rvalue
---------------------------------------------------------              
X&          yes
const X&    yes      yes            yes      yes
X&&                                 yes
const X&&                           yes      yes

```
above is the table when the lvalue,rvalue and const are all coming into play


#### implicit conversions

basically means if there is an implicit conversion from Y to X, x&& can bind to all values categories of Y.

```
void some_function(std::string&& r);

some_function("hello world");
```

#### Move Constructor

well, in the old world, you might expect that the auto_ptr is implemented as follow.

> note, auto_ptr<T> has been replaced by std::unique_ptr<T>

```
template<typename T>
class unique_ptr
{
    T* ptr;

public:

    T* operator->() const
    {
        return ptr;
    }

    T& operator*() const
    {
        return *ptr;
    }
 explicit unique_ptr(T* p = nullptr)
    {
        ptr = p;
    }

    ~unique_ptr()
    {
        delete ptr;
    }
// 

```


but now after the move constructor

```
  unique_ptr(unique_ptr&& source)   // note the rvalue reference
    {
        ptr = source.ptr;
        source.ptr = nullptr;
    }

```

now it can be  ONLY supplied with R-Value
```
unique_ptr<Shape> a(new Triangle);
unique_ptr<Shape> b(a);                 // error
unique_ptr<Shape> c(make_triangle());   // okay
```


#### Move assignment operators

now there adds a new "Move assignment" operators , there is also an "copy assignment" operator. Note the differenc es between teh two

```
unique_ptr& operator=(unique_ptr&& source)   // note the rvalue reference
    {
        if (this != &source)    // beware of self-assignment
        {
            delete ptr;         // release the old resource

            ptr = source.ptr;   // acquire the new resource
            source.ptr = nullptr;
        }
        return *this;
    }
};
```
and this can also be implemented with the move-and-swap idiom.

```
unique_ptr& operator=(unique_ptr source)   // note the missing reference
    {
        std::swap(ptr, source.ptr);
        return *this;
    }
};
```


#### Moving from lvalues

there is an standard library function template called std::move inside `<utility>`

what it does is to cast an lvalue into a rvale.
```
unique_ptr<Shape> a(new Triangle);
unique_ptr<Shape> b(a);              // still an error
unique_ptr<Shape> c(std::move(a));   // okay
```


#### Xvalues
though std::move(a) is a rvalue, it does not create a temporary object. so the committee introduce a third value category.

Sometimes that can be bound to an rvalue reference. even though it is not a rvalue in the traditional sense.

```
  expressions
          /     \
         /       \
        /         \
    glvalues   rvalues
      /  \       /  \
     /    \     /    \
    /      \   /      \
lvalues   xvalues   prvalues
```
NOTE:
> C++98 rvalues are known as prvalues in C++11. Mentally replace all occurrences of "rvalue" in the preceding paragraphs with "prvalue".

the prvalue now denote the "Pure R-Value"


#### Moving out of functions

Well, there is a question of whether or not we can move a return value .... 

```
unique_ptr<Shape> make_triangle()
{
    return unique_ptr<Shape>(new Triangle);
}          \-----------------------------/
                  |
                  | temporary is moved into c
                  |
                  v
unique_ptr<Shape> c(make_triangle());
```

Perhaps surprisingly, automatic objects (local variables that are not declared as static) can also be implicitly moved out of functions:

Note the missing *std::move*

```
unique_ptr<Shape> make_square()
{
    unique_ptr<Shape> result(new Square);
    return result;   // note the missing std::move
}
```
> C++11 has a special rule that allows returning automatic objects from functions without having to write std::move.

> Never use std::move to move automatic objects out of functions. as it will inhit "named return value optimization"


>  Rvalue references are still references, and as always, you should never return a reference to an automatic object; the caller would end up with a dangling reference if you tricked the compiler into accepting your code, like this:


> Never return automatic objects by rvalue reference. Moving is exclusively performed by the move constructor, not by std::move, and not by merely binding an rvalue to an rvalue reference.


#### Moving into memebers
Soone ror later, you are going to write code like this:

```
class Foo
{
    unique_ptr<Shape> member;

public:

    Foo(unique_ptr<Shape>&& parameter)
    : member(parameter)   // error
    {}
};
```

"Basically, the compiler will complain that parameter is an lvalue."..

> A named rvalue reference is an lvalue, just like any other variable.
The soltion is to manually enable the move:

```
class Foo
{
    unique_ptr<Shape> member;

public:

    Foo(unique_ptr<Shape>&& parameter)
    : member(std::move(parameter))   // note the std::move
    {}
};
```

#### Special member functions

C++98 add this by default
```
X::X(const X&);              // copy constructor
X& X::operator=(const X&);   // copy assignment operator
X::~X();                     // destructor
```

well, Rvalue references wen though several version.  

> Since version 3.0, C++11 declares two additional special member functions on demand:

However, C++11 declares two additional special member functions on demand, but neither VC10 nor VC11 conforms to version 3.0 yet.. so you have to add your self.


```
X::X(X&&);                   // move constructor
X& X::operator=(X&&);        // move assignment operator
```


#### Forwarding references (previously known as Universal references)

```
template<typename T>
void foo(T&&);
```

You might expect T&& to only bind to rvalues, because at first glance, it looks like an rvalue reference. As it turns out though, T&& also binds to lvalues:

```
foo(make_triangle());   // T is unique_ptr<Shape>, T&& is unique_ptr<Shape>&&
unique_ptr<Shape> a(new Triangle);
foo(a);                 // T is unique_ptr<Shape>&, T&& is unique_ptr<Shape>&
```

> If the argument is an rvalue of type X, T is deduced to be X, hence T&& means X&&. This is what anyone would expect. But if the argument is an lvalue of type X, due to a special rule, T is deduced to be X&, hence T&& would mean something like X& &&. But since C++ still has no notion of references to references, the type X& && is collapsed into X&. This may sound confusing and useless at first, but reference collapsing is essential for perfect forwarding (which will not be discussed here).

SO SOMETHING THAT WE HAVE TO BE REALLY CAREFUL:

> T&& is not an rvalue reference, but a forwarding reference. It also binds to lvalues, in which case T and T&& are both lvalue references.

#### Implementation of move

Now that you understand reference collapsing, here is how std::move is implemented:

```
template<typename T>
typename std::remove_reference<T>::type&&
move(T&& t)
{
    return static_cast<typename std::remove_reference<T>::type&&>(t);
}
```

As you can see, move accepts any kind of parameter thanks to the forwarding reference T&&, and it returns an rvalue reference. The std::remove_reference<T>::type meta-function call is necessary because otherwise, for lvalues of type X, the return type would be X& &&, which would collapse into X&. Since t is always an lvalue (remember that a named rvalue reference is an lvalue), but we want to bind t to an rvalue reference, we have to explicitly cast t to the correct return type. 

Reference:

[c++ - What are move semantics? - Stack Overflow](http://stackoverflow.com/questions/3106110/what-are-move-semantics)
