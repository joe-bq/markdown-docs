## Introducotin 

well, it has been proposed many a way to write good unit test... 


## Unit test name convention

Structuring Unit Tests - 
[Structuring Unit Tests - You've Been Haacked](http://haacked.com/archive/2012/01/02/structuring-unit-tests.aspx/)

Highlight:　nested class for each method being tested.

```
using Xunit;

public class TitleizerFacts
{
    public class TheTitleizerMethod
    {
        [Fact]
        public void ReturnsDefaultTitleForNullName()
        {
            // Test code
        }

        [Fact]
        public void AppendsTitleToName()
        {
            // Test code
        }
    }

    public class TheKnightifyMethod
    {
        [Fact]
        public void ReturnsDefaultTitleForNullName()
        {
            // Test code
        }

        [Fact]
        public void AppendsSirToMaleNames()
        {
            // Test code
        }

        [Fact]
        public void AppendsDameToFemaleNames()
        {
            // Test code
        }
    }
}
```

What are some popular naming conventions for Unit Tests? [closed] - 

[What are some popular naming conventions for Unit Tests? - Stack Overflow](http://stackoverflow.com/questions/96297/what-are-some-popular-naming-conventions-for-unit-tests)
highlight:

*MethodName_StateUnderTest_ExpectedBehavior*
```
MethodName_StateUnderTest_ExpectedBehavior

Public void Sum_NegativeNumberAs1stParam_ExceptionThrown() 

Public void Sum_NegativeNumberAs2ndParam_ExceptionThrown () 

Public void Sum_simpleValues_Calculated ()
```


with underscores separating the words
*Separating Each Word By Underscore*

```
public void Sum_Negative_Number_As_1st_Param_Exception_Thrown() 

Public void Sum_Negative_Number_As_2nd_Param_Exception_Thrown () 

Public void Sum_Simple_Values_Calculated ()

```

References: [Naming standards for unit tests - Blog - Osherove](http://osherove.com/blog/2005/4/3/naming-standards-for-unit-tests.html)

