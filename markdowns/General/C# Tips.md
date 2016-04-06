## Introduction

this page will introduce you some of the gotchas that you might not be aware of.


## Remove hanlders from an delegate can reduce it to null

You might believe that if a delegate has handler unsubscribed from it, it won't go down to null

```
// WRONG
EventHandler handler = new EventHandler(eventHandler);
handler -= eventHandler;

Debug.Assert(handler != null);

```

well, that is WRONG.

here is the code that to test it.


```
    class Program
    {
        static void Main(string[] args)
        {
            Program p = new Program();
            p.AddTestEventHandler(p.HandleEvent);
            p.RemoveEventHandler(p.HandleEvent);
        }

        public Program()
        {
        }

        private EventHandler eventHandler;
        public void AddTestEventHandler(EventHandler handler)
        {
            if (eventHandler != null)
                eventHandler += handler;
            else
            {
                eventHandler = handler;
            }
        }
        public void RemoveEventHandler(EventHandler handler)
        {
            if (eventHandler != null)
                eventHandler -= handler;

            if (eventHandler == null
                )
            {
                Console.WriteLine("Event Handler reduced to 0");
            }

        }


        public void HandleEvent(object sender, EventArgs args)
        {
            
        }
    }

```


## Summary on the sync-up with the author J on the Reactive core presentation

there are something that He has introduced, the following are included:


1.  ISubscribable - which is a transform of the IObservable of the Rx Core
2. ConditionalWeakTable - to observe object being finalized and then destroying targets (objects which depends on the key)
3. SyncWith - to minimize the cost between synchronizing two list.
4. the member path observable something like the following (Subscription.ObservePropertyChanged(x => x.GrandParent.Parent.Child)
5. how to get event out of the Fast Reflection (which uses the Expression treee) : something like the following (Subscription.FromEvent(x => x.SomeEvent += null );
6. Delay executor and Throttling
7. Create a list instead of Closure single variable.
look at the following code and think of why?
```
8. RealProxy for intercepting.... you can intercept some class to hijack your own process.
var detaches = new Action[] { null };
            Action detach = () =>
                {
                    if (detaches[0] == null) return;
                    lock (detaches)
                    {
                        if (detaches[0] == null) return;
                        detaches[0]();
                        detaches[0] = null;
                    }
                };
```

Reason: 1. lock local variable won't be regarded well by the C# closure. 2. local variable (single) without colleciton may not do well when it is handles well with closure bug introduced by C#.


## Event-Driven http server in C# with Rx and HttpListener

well in the below post, 
[Event-driven http server in C# with Rx and HttpListener](http://joseoncode.com/2011/06/17/event-driven-http-server-in-c-with-rx-and-httplistener/)

there is the following code 


```
public class HttpServer : IObservable<RequestContext>, IDisposable
{
    private readonly HttpListener listener;
    private readonly IObservable<RequestContext> stream;

    public HttpServer(string url)
    {
        listener = new HttpListener();
        listener.Prefixes.Add(url);
        listener.Start();
        stream = ObservableHttpContext();
    }

    private IObservable<RequestContext> ObservableHttpContext()
    {
        return Observable.Create<RequestContext>(obs =>
                            Observable.FromAsyncPattern<HttpListenerContext>(listener.BeginGetContext,
                                                                             listener.EndGetContext)()
                                      .Select(c => new RequestContext(c.Request, c.Response))
                                      .Subscribe(obs))
                         .Repeat()
                         .Retry()
                         .Publish()
                         .RefCount();
    }
    public void Dispose()
    {
        listener.Stop();
    }

    public IDisposable Subscribe(IObserver<RequestContext> observer)
    {
        return stream.Subscribe(observer);
    }
}
```


Given by an example use case

```
static void Main()
{
        //a stream os messages
        var subject = new Subject<string>();

        using(var server = new HttpServer("http://*:5555/"))
        {
            var handler = server.Where(ctx => ctx.Request.Url.EndsWith("/hello"))
                  .Subscribe(ctx => ctx.Respond(new StringResponse("world")));

            Console.ReadLine();
            handler.Dispose();
        }    
}
```

well, this code requires a lot of supporting class which is not mentioned in the post, but you can find the github port [Anna-Rx/Anna](https://github.com/Anna-Rx/Anna)


well, to use a cut-down version of the HttpServer with HttpListener, here is hte modified code

```
public class StubHttpServer : IObservable<HttpListenerContext>, IDisposable
    {
        private readonly HttpListener listener;
        private readonly IObservable<HttpListenerContext> stream;

        public StubHttpServer(string url)
        {
            listener = new HttpListener();
            listener.Prefixes.Add(url);
            listener.Start();
            stream = ObservableHttpContext();

            string requestString = listener.GetContext().Request.RawUrl;
        }
        private IObservable<HttpListenerContext> ObservableHttpContext()
        {
            return Observable.Create<HttpListenerContext>(obs =>
                                Observable.FromAsyncPattern<HttpListenerContext>(listener.BeginGetContext,
                                                                                 listener.EndGetContext)()
                                    //.Select(c => new RequestContext(c.Request, c.Response))
                                          .Subscribe(obs))
                             .Repeat()
                             .Retry()
                             .Publish();

        }


        public void Dispose()
        {
            listener.Stop();
        }

        public IDisposable Subscribe(IObserver<HttpListenerContext> observer)
        {
            return stream.Subscribe(observer);
        }
    }
```

well, it has errors when you try 
```
public void Test()
{
   HttpServer server = new HttpServer ("http://*:1234/");
   server.Subscribe(x => Observer.Create(ctx => ctx.Request.OutputStream.Write(stream, 0, stream.Length));

}
```

the problem is that you get a "Access Denied" exception. and  solution are 

[c# - HttpListenerException "access denied" for non-admins - Stack Overflow](http://stackoverflow.com/questions/14962334/httplistenerexception-access-denied-for-non-admins)

the post has the following advice
```
netsh http add urlacl http://+:8008/ user=Everyone listen=true
```

```
netsh http add urlacl http://+:8008/ user=Administrators listen=true
```
Or you can run the test by runas admnistrator.

## the magic use of single array in closure

well, if you read the code from J, you will find that there is a lot of places where the following code paradigm is used.


```
        public virtual IDisposable Execute(T arg)
        {
            lock (_lock)
            {
                ITimer[] timer = { null };
                var disp = Disposable.Create(() =>
                {
                    lock (_lock)
                    {
                        timer[0].Dispose();
                        _executingTimers.Remove(timer[0]);
                    }
                });

                timer[0] = TimerController.Instance.Construct(() =>
                {
                    disp.Dispose();
                    lock (_actionLock)
                    {
                        _action(arg);
                    }
                }, _delayTime, -1);
                _executingTimers[timer[0]] = arg;
                return disp;
            }
        }
```

why cannot just we have one timer variable and added to the closure??

the reasons is simple. that the first lambda will need to access the first element in the array, and which is not yet initialized. and the second clause which create/construct the timer will then initialize the array's first element. 

so the array which is a reference (a container pointing to the element) which get passed between two lambda.

So this is a very useful technique and can be used in many a place.


## Unit Test Synchronization context setup 
where in our unit test there are code which written using Dispatcher, and test cases are not running in the full WPF environment, so that we need sometimes to write the following code 



```
[SetUp
public void Setup()
{
	SynchronizationContext.SetSynchronizationContext(new SynchronizationContext());
}
```


and there are many places where this code are called, and each are running in a different synchronization context and that can bring severe problem when code does requires the SynchronizationContext to work. 


so we have to restore the scene. here are the code that does Setup as well as TearDown


private SynchronizationContext _savedSynchronizationContext;

```
[SetUp]
public void Setup()
{
	_savedSynchronizationContext = SynchronizationContext.Current;
	SynchronizationContext.SetSynchronizationContext(new SynchronizationContext());
}
```


and the TearDown method 
```

	[TearDown]
    public void TearDown()
    {
	              SynchronizationContext.SetSynchronizationContext(_savedSynchronizationContext);
    }
```


## Binding to ViewModel or UserControl.
well I have a custom control called DepthGrid

inside the DepthGrid

```
public class DepthGrid
{

        public static readonly DependencyProperty VisibleRowCountProperty =
                DependencyProperty.Register("VisibleRowCount", typeof(int), typeof(DepthGrid));

        public int VisibleRowCount
        {
            get { return (int)GetValue(VisibleRowCountProperty); }
            set { SetValue(VisibleRowCountProperty, value); }
        }
}

```
and there is one behavior attached to the control

```
					<behaviors:GridControlDisplayableRowCountBehavior 
						VisibleRowCount="{Binding VisibleRowCount, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}" />
```

And in the client of the user control, the client e.g. can be VerticalDepth, I have this: 

```
<flexDepth:DepthGrid
...
VisibleRowCount="{Binding VisibleRowCount, Mode=TwoWay}"
/>
```
the problem is that it complains there is no VisibleRowCount in Client view model ---

the reason being that the binding `"{Binding VisibleRowCount, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}"` means binding to DataContext of user control, rather than the dependency property of the User control. 

To fix that, otherwise we will have unnecessary binding errors.

in the UserControl's xaml file, does this:

```
<UserControl
	x:Name="UserControl" ...>
<behaviors:GridControlDisplayableRowCountBehavior 
						VisibleRowCount="{Binding VisibleRowCount, ElementName=UserControl, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}" />

</UserControl>
```

the key being `ElementName=UserControl` and `UpdateSourceTrigger`, also `TwoWay` binding.

and in the Client to the UserControl, use the following.
```
<flexDepth:DepthGrid
...
VisibleRowCount="{Binding VisibleRowCount, Mode=TwoWay, UpdateSource=PropertyChanged}"
/>
```

the key being `UpdateSource=PropertyChanged`;


## Raie property changed the smarter way

Well, you can raise the Property changed event in a smater way. check the following ViewModelBase definition 

```

    public class ViewModelBase : NotificationObject 
    {
        public void ProcessOnUiThread(SynchronizationContext context, Action action)
        {
            //Dispatcher dispatcher = Dispatcher.CurrentDispatcher;
            if (context == null)
            {
                action();
            }
            else
                context.Post((s) => action(), null);
        }

        public void OnPropertyChanged<T>(Expression<Func<T>> propertyExpression)
        {
            RaisePropertyChanged(propertyExpression);
        }

        public void OnPropertyChanged(string propertyName)
        {
            RaisePropertyChanged(propertyName);
        }

        protected void CompareSet<T>(T value, ref T prop, params Expression<Func<T>>[] propertyExpressions)
        {
            if (!EqualityComparer<T>.Default.Equals(value, prop))
            {
                prop = value;
                foreach (var expression in propertyExpressions)
                {
                    RaisePropertyChanged(expression);
                }
            }
        }

        public void NotifyPropertyChanged([CallerMemberName] string propertyName = null)
        {
            RaisePropertyChanged(propertyName);
        }
    }

```

the use of `[CallerMemberName]` attribute can help to reduce amount of work that is required to do a Runtime fast reflection with static compiler time check.