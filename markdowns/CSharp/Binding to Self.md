
## Binding to self

--

README.txt

--


in this project we will discuss whether it is possible to bind and notify when self changes. let's show you an example of why you sometimes want to do that ?


suppose that you have a content control, which binds to the ViewModel itself, if some of the ViewModel has changed, you want to notify the UI to refresh the whole UI.


the default binding without any parameter 

```
<Label   Content = "{Binding}" />
```

is equivalent to the following code 

```
<Label Content="{Binding Path=.}" />
```

as it is been said on this page 



> * Optionally, a period (.) path can be used to bind to the current source. For example, Text="{Binding}" is equivalent to Text="{Binding Path=.}".



--

Reference:

[Binding class](http://msdn.microsoft.com/en-us/library/system.windows.data.binding(v=vs.110).aspx)
[Data Binding Overview](http://msdn.microsoft.com/en-us/library/ms752347(v=vs.110).aspx)
[Binding.Path Property](http://msdn.microsoft.com/en-us/library/system.windows.data.binding.path(v=vs.110).aspx )