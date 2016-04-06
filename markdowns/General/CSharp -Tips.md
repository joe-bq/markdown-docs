## Flag enum

there are a special type of enu, which is called Bit fields, while this is less commonly used in C#, but for the purpose of making it complete, here is the details. 

As in the references, you can see thet key to the C#'s bit fileds is done through the help of the [StructLayoutAttribute] and the \[FieldOffsetAttribute\].


### * Tip 1 - Bit filelds

The C++ 's bit fields are more natively supported.


```
// bit_fields1.cpp
// compile with: /LD
struct Date {
   unsigned short nWeekDay  : 3;    // 0..7   (3 bits)
   unsigned short nMonthDay : 6;    // 0..31  (6 bits)
   unsigned short nMonth    : 5;    // 0..12  (5 bits)
   unsigned short nYear     : 8;    // 0..100 (8 bits)
};
```


### Tip  2 - Flags Attributes
Here we I am going to show you is another atribute, which is called the "FlagsAttribute", while , the flag attribute capability does not come out out of box... let's see an example. 


```
    [Flags]
    public enum LayoutStopCode
    {
        None  = 1,
        
        ChangedToHidden,

        Unpinned,

        MovedToBackground,
    }
```

with the above code, you might expect that the ChangedToHidden to have value of '2', and "Unpinned" the value of 3, and so on....

```
    class Program
    {
        static void Main(string[] args)
        {
            var layoutStopCodeValues = Enum.GetValues(typeof(LayoutStopCode));

            foreach (LayoutStopCode layoutStopCode in layoutStopCodeValues)
            {
                var intValue = (int)layoutStopCode;
                Console.WriteLine("" + layoutStopCode + "" + intValue); // what you might get is the following , None= 1, ChangedToHidden = 2, Unpinned = 3, MovedToBackground = 
            }

            var defaultValue = default(LayoutStopCode);
            Console.WriteLine("the deafult value of LayoutStopCode is {0}", defaultValue);


            Console.ReadLine();
        }
    }
```


While it turns out the next value of the Enum "ChangedToHidden" is actually 2, because is the next interger after None. 

the increment by 1 strategy applies to all enum values, so it won't be affected by the "FlagsAttribute".  


so the expected sequence to do is as follow. 

```
    public enum LayoutStopCode
    {
        None  = 0,
        
        ChangedToHidden = 1,

        Unpinned = 2,

        MovedToBackground = 4,
        
        ALl = ChangeToHidden | Unpinned | MovedToBackground | MovedToBackground
    }
```

### Tip 3 - the default value of enum

the default value of enum is the value of enum with integer value 0, given the following example.


```
    public enum LayoutStopCode
    {
        None  =1,
        
        ChangedToHidden = 2,

        Unpinned = 4,

        MovedToBackground = 8,
        
        ALl = ChangeToHidden | Unpinned | MovedToBackground | MovedToBackground
    }

```


you would expect that the default value of the LayoutStopCode to be "LayoutStopCode.None", well. let check ..


```
var defaultvalue = default(LayoutStopCode);

```

if you inspect the value, you would see that it is "0", which is not even declared inside the enum "LayoutStopCode"....


### Tips 4 - Enum.HasFlag

Working with the flags attributes, there is a HasFlag method which can help you easily test if a flag has been set. 




References:

[C++ Bit Fields]: http://msdn.microsoft.com/en-us/library/ewwyfdbe.aspx
[C++ Bit Fields][C++ Bit Fields]
[Bit fields in C#]: http://stackoverflow.com/questions/14464/bit-fields-in-c-sharp
[Bit fields in C#][Bit fields in C#]
[Enum.HasFlag]: http://msdn.microsoft.com/zh-cn/library/system.enum.hasflag(v=vs.110).aspx
[Enum.HasFlag][Enum.HasFlag]


## Unit test name conventions
the name convention of Unit test can varies according to different concerns and different preferences. 

I will given some examples 

1) Method_Name_DoesWhat_WhenTheseConditions 
Sum_ThrowsException_WhenNegativeNumberAs1stParam
2) UnderTheseTestConditions_WhenIDoThis_ThenIGetThis ( BDD / Gherkin syntax of: Given/When/Then)
WhenNegativeNumberAs1stParam_Sum_ThrowsAnException
3) MethodName_StateUnderTest_ExpectedBehavior (By Roy Osherove) - also know as the ((SSR) - Subject-Scenario-Result)
4) Class Responsibility
testAppendsAdditionalParameterToUrlsInHrefAttributes()


References:
[What are some popular naming conventions for Unit Tests? - Stack Overflow](http://stackoverflow.com/questions/96297/what-are-some-popular-naming-conventions-for-unit-tests)
[Naming standards for unit tests - Blog - Osherove](http://osherove.com/blog/2005/4/3/naming-standards-for-unit-tests.html)
[Writing Great Unit Tests: Best and Worst Practices - Steve Sanderson’s blog - As seen on YouTube™](http://blog.stevensanderson.com/2009/08/24/writing-great-unit-tests-best-and-worst-practises/)
[Google Testing Blog: TotT: Naming Unit Tests Responsibly](http://googletesting.blogspot.co.uk/2007/02/tott-naming-unit-tests-responsibly.html)

## Various Path, URI, URN and Local, Absolute paths, Code..

Sometimes when we are dealing with path related works, we need to understand how to get paths string to various our needs.

there are a few that you can get from executing assembly or currently working directory.

* Codebase (file://c:/bin/Debug/file.exe)
* Absolute Path (c:\bin\Debug\file.exe)
* Local Path  (bin\Debug\file.exe)
* URN Path (\\sharedhost\share\file.exe)
* Uri (absolute uri (file://c:/bin/Debug/file.exe)

From a Assembly, you can get the following information.

1. Assembly CodeBase
2. Assembly Absolute path
3. Assembly Location

Also, there exist some path which allows you to Unescape data strings. for more details on how that works, please refers to the MSDN.

In this program, we will try to test on various way to get the path strings..

```
    class Program
    {
        static void Main(string[] args)
        {

            Assembly assembly = Assembly.GetExecutingAssembly();

            var codeBase = assembly.CodeBase;
            var location = assembly.Location;

            Console.WriteLine("codeBase = {0}", codeBase);
            Console.WriteLine("location = {0}", location);

            var uriCodebase = new Uri(codeBase);
            var uriLocation = new Uri(location);

            var absoluteCodeBase = uriCodebase.AbsolutePath;
            var absoluteLocation = uriLocation.AbsolutePath;

            Console.WriteLine("absoluteCodeBase = {0}", absoluteCodeBase);
            Console.WriteLine("absoluteLocation = {0}", absoluteLocation);


            // now we will construct some URN paths.

            string nonSchemedUrnPath = @"\\shawd4071\share\UriTest.exe";
            string schemedUrnPath2 = @"file:////shawd4071\share\UriTest.exe";

            var uriNonSchemedUrnPath = new Uri(nonSchemedUrnPath);
            var uriSchemedUrnPath2 = new Uri(schemedUrnPath2);

            Console.WriteLine("uriNonSchemedUrnPath (absolutePath) = {0}", uriNonSchemedUrnPath.AbsolutePath);
            Console.WriteLine("uriNonSchemedUrnPath (localPath) = {0}", uriNonSchemedUrnPath.LocalPath);
            Console.WriteLine("uriNonSchemedUrnPath (absoluteUri) = {0}", uriNonSchemedUrnPath.AbsoluteUri);

            Console.WriteLine("uriSchemedUrnPath2 (absolutePath) = {0}", uriSchemedUrnPath2.AbsolutePath);
            Console.WriteLine("uriSchemedUrnPath2 (localPath) = {0}", uriSchemedUrnPath2.LocalPath);
            Console.WriteLine("uriSchemedUrnPath2 (absoluteUri) = {0}", uriSchemedUrnPath2.AbsoluteUri);


            // now we will check the use of the UriBuilder and UnescapedDataString
            // 
            var uriBuilder1 = new UriBuilder(nonSchemedUrnPath);
            var uriBuilder2 = new UriBuilder(schemedUrnPath2);


            Console.WriteLine("unescapedDataString = {0}", Uri.UnescapeDataString(uriBuilder1.Path));
            Console.WriteLine("unescapedDataString = {0}", Uri.UnescapeDataString(uriBuilder2.Path));
            Console.ReadLine();
        }
    }
```


## Unit Test - Application.Current is null

While it is a bad design to embedded some code such as below in the application's code. 

```
Application.Current.Dispatcher.Invoke(() => { });
```

this can make the Unit Test hard to write. 

You might get an NullReferenceException when running Unit test to test code that has dependencies on the `Application.Current`

Normally you would epxect the following attributes can do the help. 

```
[RequiresSTA]
```

can do the trick. However, this can not apply to the Unit test.

there are a few options to pass around this limitation. I will list them below.

1. Create a new Dispatcher and dedicated thread to run the Dispatcher.
2. Create a new Application in the background
3. Create a new Application in the STA Thread
4. Initialize a new AppDomain and create within a new Application and run Unit test in each AppDomain


1. Create a new Dispathcer.

```
 internal Thread CreateDispatcher()
    {
        var dispatcherReadyEvent = new ManualResetEvent(false);

        var dispatcherThread = new Thread(() =>
        {
            // This is here just to force the dispatcher 
            // infrastructure to be setup on this thread
            Dispatcher.CurrentDispatcher.BeginInvoke(new Action(() => { }));

            // Run the dispatcher so it starts processing the message 
            // loop dispatcher
            dispatcherReadyEvent.Set();
            Dispatcher.Run();
        });

        dispatcherThread.SetApartmentState(ApartmentState.STA);
        dispatcherThread.IsBackground = true;
        dispatcherThread.Start();

        dispatcherReadyEvent.WaitOne();
        SynchronizationContext
           .SetSynchronizationContext(new DispatcherSynchronizationContext());
        return dispatcherThread;
    }
```
and how to use it 

```
 [TestMethod]
    public void Foo()
    {
        Dispatcher
           .FromThread(CreateDispatcher())
                   .Invoke(DispatcherPriority.Background, new DispatcherDelegate(() =>
        {
            _barViewModel.Command.Executed += (sender, args) => _done.Set();
            _barViewModel.Command.DoExecute();
        }));

        Assert.IsTrue(_done.WaitOne(WAIT_TIME));
    }
```

2.  Create new Application in the Background

while the following initalizer should be run in so called Assembly initializer, which should guarantee to run when the assembly is initialized.

```
[TestClass]
public class ApplicationInitializer
{
    [AssemblyInitialize]
    public static void AssemblyInitialize(TestContext context)
    {
        var waitForApplicationRun = new ManualResetEventSlim();
        Task.Run(() =>
        {
            var application = new Application();
            application.Startup += (s, e) => { waitForApplicationRun.Set(); };
            application.Run();
        });
        waitForApplicationRun.Wait();
    }
}

[TestClass]
public class MyTestClass
{
    [TestMethod]
    public void MyTestMethod()
    {
        // implementation can access Application.Current.Dispatcher
    }
}
```

3. Create a new Application in the STA thread

this is rather alike the 2. solution, but instead, it requries the application creation code to run just in the STA thread once. 

```
        public static void ApplicationDispatcherSetup()
        {
            try
            {
                if (_application == null)
                {
                      if (Application.Current == null)
                    {
                        _application = new Application();
                        _application.Resources.MergedDictionaries.Add(
                                Application.LoadComponent(new Uri(@"pack://application,,,/path/to/your/XAML.xaml", UriKind.Absolute)) as ResourceDictionary);
                    }

            }
            catch (Exception)
            {
            }

        }
```

and I have decorated the Test fixture with the following attributes.

```
    [TestFixture, RequiresSTA]
    public class AlertNotificationFactoryTest
    {
      // ...
    }
```

4. Create each AppDomain in the Unit test

```
[TestClass()]
[Serializable]
public class UnitTest
{
    protected void ExecuteInSeparateAppDomain(string methodName)
    {
        AppDomainSetup appDomainSetup = new AppDomainSetup();
        appDomainSetup.ApplicationBase = Environment.CurrentDirectory;
        AppDomain appDomain = AppDomain.CreateDomain(methodName, null, appDomainSetup);

        try
        {
            appDomain.UnhandledException += delegate(object sender, UnhandledExceptionEventArgs e)
            {
                throw e.ExceptionObject as Exception;
            };

            UnitTest unitTest = appDomain.CreateInstanceAndUnwrap(GetType().Assembly.GetName().Name, GetType().FullName) as UnitTest;

            MethodInfo methodInfo = unitTest.GetType().GetMethod(methodName, BindingFlags.NonPublic | BindingFlags.Instance);

            if (methodInfo == null)
            {
                throw new InvalidOperationException(string.Format("Method '{0}' not found on type '{1}'.", methodName, unitTest.GetType().FullName));
            }

            try
            {
                methodInfo.Invoke(unitTest, null);
            }
            catch (System.Reflection.TargetInvocationException e)
            {
                throw e.InnerException;
            }
        }
        finally
        {
            AppDomain.Unload(appDomain);
        }
    }
}
```

and to run it do this
```
[TestMethod()]
public void QualifierViewModel_FlagsAndLoadDatasets()
{
    ExecuteInSeparateAppDomain("TestLoadDataSets");
}
```
References:
[c# - Using the WPF Dispatcher in unit tests - Stack Overflow](http://stackoverflow.com/questions/1106881/using-the-wpf-dispatcher-in-unit-tests)
[c# - Application.Current is Null for Unit Tests - Stack Overflow](http://stackoverflow.com/questions/12625848/application-current-is-null-for-unit-tests)
