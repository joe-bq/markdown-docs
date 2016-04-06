## Introduction
this page will contains all the necessary information about some tips/usage of C#language.



## enum and attributes pattern

in Java you can do something like 

```java
public enum Month {

   Month("January", MonthFamily.Spring);
   Month("February", MonthFamily.Spring);
}
```

well in C# this is not supported.

```c#
public enum Month {

  January,
  February
}
```

well, C# does not have the enum  constructor.

```C#
public enum MonthFamily 
    {
        Spring, 
        Summer,
        Autumn,
        Winter,
    }

    [AttributeUsage(AttributeTargets.Field)]
    public class MonthFamilyAttribute : Attribute
    {
        public MonthFamily MonthFamily { get; set; }
        public MonthFamilyAttribute(MonthFamily monthFamily)
        {
            MonthFamily = monthFamily;
        }
    }

    public enum MonthEnum2
    {
        [MonthFamily(MonthFamily.Spring)]
        JANUARY,
        [MonthFamily(MonthFamily.Spring)]
        FEBRUARY,
        [MonthFamily(MonthFamily.Spring)]
        MARCH,
        [MonthFamily(MonthFamily.Spring)]
        APRIL,
        [MonthFamily(MonthFamily.Summer)]
        MAY,
        [MonthFamily(MonthFamily.Summer)]
        JUNE,
        [MonthFamily(MonthFamily.Summer)]
        JULY,
        [MonthFamily(MonthFamily.Summer)]
        AUGUST,
        [MonthFamily(MonthFamily.Winter)]
        SEPTEMBER,
        [MonthFamily(MonthFamily.Winter)]
        OCTOBER,
        [MonthFamily(MonthFamily.Winter)]
        NOVEMBER,
        [MonthFamily(MonthFamily.Winter)]
        DECEMBER,
    }
   ```
to use the Attribute, we need to have either create a static class or add a static method to the MonthFamilyAttribute class.

```C#
    public class MonthFamilyException : Exception
    {
        public MonthFamilyException(MonthEnum2 month) :  base(string.Format("Cannot get MonthFamily for {0}", month))
        {
        }
    }

    public static class MonthFamilyUtil
    {
        public static MonthFamily GetMonthFamily(MonthEnum2 month)
        {
            FieldInfo field = typeof(MonthEnum2).GetField(Enum.GetName(typeof(MonthEnum2), month));
            if (field != null) 
            {
                MonthFamilyAttribute attr = (MonthFamilyAttribute) MonthFamilyAttribute.GetCustomAttribute(field, typeof(MonthFamilyAttribute));
                if (attr != null)
                {
                    return attr.MonthFamily;
                }
            }

            throw new MonthFamilyException(month);
        }
    }
```

now to use it, write the following.

```C#
            MonthEnum2 month = MonthEnum2.AUGUST;
            var monthFamily = MonthFamilyUtil.GetMonthFamily(month);
            Console.WriteLine("month {0}'s family is {1}", month, monthFamily);
 ```
another way is to add the util method to the MonthFamilyAttribute

```
    [AttributeUsage(AttributeTargets.Field)]
    public class MonthFamilyAttribute : Attribute
    {
        public MonthFamily MonthFamily { get; set; }
        public MonthFamilyAttribute(MonthFamily monthFamily)
        {
            MonthFamily = monthFamily;
        }

        public static MonthFamily GetMonthFamily(MonthEnum2 month)
        {
            return MonthFamilyUtil.GetMonthFamily(month);
        }
    }
```