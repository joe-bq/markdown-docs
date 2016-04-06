## Introduction 
this page serves as a central place to host contents on topics on RX (Reactive Extension) and etc...

## My initial draft
before going into details about the use of the Reactive Extension from references materials, I would like to show you an example that exemplify the basic use of hte Reactive Extension and its basic classes

First let me given an use scenario, suppose that I am writing a service providing class, and due to the fact that my class serves some information that has a dynamic characteristic - which means that the data is keeping coming at a uncertain time...  Thus it is more difficult for me to prepare the data in advance and then presented to the user all at once, then I would like to have the ability to notify the user when data does comes... 

the paradigm describe above is rather familiar, this is so-called "pull" vs. "push" mode.l

Now, suppose that the information that I want to share with the client of the data is "Subject", which has a very basic definition as below. 

```
    public class Subject
    {
        public int Vintage { get; set; }
        public string Vendor { get; set; }
    }
```
Then I am going to write the "Producer". because it produce something and it is the subject of concerns.  Let's write our "Producer" class. 

To adapt into the ReactiveExtension framework, we found the famous dual, "IObserver" and "IObservable". Reactive Extensino now extend the idea to include a new concept called "ISubject" to better conceptually capture its intents. so we are making the Produer class to implements the "ISubject" interface. 

```
    // if a class itself is an ISubject, then it implicit implements the IObservable interface. 
    // check the implemntation of the ISubject<T> interface definition then you can see 
    //
    //public interface ISubject<T> : ISubject<T, T>, IObserver<T>, IObservable<T>
    //{
    //}

    public class SubjectProducer : IObservable<Subject>, ISubject<Subject>
    {
```

we need to implement the  ISubject Members. there are 

* OnNext
* OnComplete
* OnError
* Subscribe

Suppose the Producer class does its own management of its class (though we can delegate the management of the Producer client to a central observable management class). 


```
        #region ISubject fields 

        private List<IObserver<Subject>> _observers = new List<IObserver<Subject>>();
        #endregion

        /* Implementation of the ISubject interface */
        #region ISubject interfaces
        public void OnCompleted()
        {
            foreach (var observer in _observers)
            {
                observer.OnCompleted();
            }
        }

        public void OnError(Exception error)
        {
            foreach (var observer in _observers)
            {
                observer.OnError(error);
            }
        }

        public void OnNext(Subject value)
        {
            foreach (var observer in _observers)
            {
                observer.OnNext(value);
            }
        }

        public IDisposable Subscribe(IObserver<Subject> observer)
        {
            _observers.Add(observer);
            return new Unsubscriber(_observers, observer);
        }
        #endregion
```

You may wonder why we have to return a IDisposable interface instance in the Subscribe method. this is used to further decouple the IObserver from its subject IObservable. 

To unsubscribe from the subject, the you just do the call the Dispose method on the returned Subscribe methods.  Let's see how is Unsubscribe class is defined. 

```
SubjectProducer : IObservable<Subject>, ISubject<Subject>
{
	//... 
        // Normally the Subscribe will give you back a wrapped unsubscriber, so that 
        // the Observer is futher decoupled from the Subejct, (or in another word, the IObservable...)
        private class Unsubscriber : IDisposable
        {
            private List<IObserver<Subject>> _observers;
            private IObserver<Subject> _observer;


            public Unsubscriber(List<IObserver<Subject>> observers, IObserver<Subject> observer)
            {
                this._observers = observers;
                this._observer = observer;
            }

            #region IDisposable
            public void Dispose()
            {
                if (_observer != null && _observers.Contains(_observer))
                {
                    _observers.Remove(_observer);
                }
            }
            #endregion
        }
        
}
```
last, we add a method called "Produce" to simuate the producing of the data. 

```

public class SubjectProducer : IObservable<Subject>, ISubject<Subject>
{

// ...
        public Subject Produce()
        {
            int random = new Random((int)DateTime.UtcNow.Ticks).Next(100);
            var subject =  new Subject() { Vintage = random, Vendor = "Vendor" + random };
            OnNext(subject);

            return subject;
        }
// ...        
}
```


As you know, if we code everything from this pattern from zero up, it would takes us ages to build anthing useful, Luckily Reactive has identify the needs to build common patterns with common classes., it provides several class to help the tasks easier. 

Among one of the class is the "ReplaySubject", which can easily let you translate some pre-cooked data to IObservable(ISubject)...  You can use the "ReplaySubject" as the seeds to generate a lots of other sequences.

Below we will use the Generator (ReplaySubject") to bootstrapp the Producer. 

in our drive code (class "Program"). we create the ReplaySubject and the Producer code.

```
    class Program
    {
        // we can get observable from ISubject, while the IObserver is the observer to the Observable.
        #region Private Fields 
        private readonly ISubject<Unit> _unitSubject = new ReplaySubject<Unit>(1); 
        private readonly SubjectProducer _subjectProduer = new SubjectProducer();
        #endregion
    }
```

we expose the the Producer, through one public methods 


```
    class Program
    {
        #region Public methods 
        public IObservable<Subject> SubscribeProducer()
        {
            return _unitSubject.Take(1).SelectMany(_ => _subjectProduer);
        }
        #endregion

    }
```

to boot strap the Producer, we want to trigger the seeds. let's write the code in the constructor

```
    class Program
    {
        #region Constructor(s)
        public Program()
        {
            _unitSubject.OnNext(Unit.Default);
        }
        #endregion

    }
```

Next is to set the real drive code to wires in one client and put it in a dry-run.


```
    class Program
    {
        static void Main(string[] args)
        {
            Program program = new Program();
            var producer = program.SubscribeProducer();
            producer.Subscribe(m =>
                {
                    Console.WriteLine("ReplaySubjectTest.Subject Vintage = {0}", m.Vintage);
                    Console.WriteLine("ReplaySubjectTest.Subject.Vendro = {0}", m.Vendor);
                });
            program._subjectProduer.Produce();

        }

    }
```

as you can see, when the harness class is initialized, it bootstrap the Producer, then we hook to the producers's observer methods then we call "Produce" to simuate the ticking of data, then everything just rolls.


## References

this topic deserves some good section of Reference on its own, 
the references that I used on this topic include the following. 

[Intro to Rx - Why Rx?]: http://www.introtorx.com/Content/v1.0.10621.0/01_WhyRx.html#WhyRx
[Intro to Rx - Why Rx?][Intro to Rx - Why Rx?]
[LeeCampbell: Reactive Extensions for .NET an Introduction]: http://leecampbell.blogspot.hk/2010/08/reactive-extensions-for-net.html
[LeeCampbell: Reactive Extensions for .NET an Introduction][LeeCampbell: Reactive Extensions for .NET an Introduction]
[Reactive Extensions]:http://msdn.microsoft.com/en-us/data/gg577609.aspx
[Reactive Extensions][Reactive Extensions]
