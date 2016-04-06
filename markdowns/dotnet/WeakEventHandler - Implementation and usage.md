# The WeakEventHandlerManager class implemenation

In this chapter, we will study the implemenation of the class WeakEventHandlerManager implemenation, the class is for managing a list of WeakRefernece to EventHandler, which is the base class of a family of event notification handlers. 

## background

first we need to check on the reason why we need to bother creating such Event handler manager.

### why we need the WeakEventHandlerManager? 

suppose that we have a not well implemented class that represents the data, and we have some UI that binds itself to a Command .

now that if the View is to be disposable, and because of the Command may live longer than the View, then there is a hard reference from the command to the View, because of the link exists, the GC cannot clean up the View just because of this. 

### the implementation consideration

the WeakEventHandlerManager should be able to do the following. 

1. it should have dispatcher ability 
2. It should check if the Weak refernece is yes alive, and only fires the event that is yet alive.  

here is the code 
```
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Threading;
using System.Windows;

namespace Common.Utilities
{
    /// <summary>
    /// WeakEvent handler manager
    /// </summary>
    public static class WeakEventHandlerManager
    {

        public static void CallWeakReferenceHandlers(object sender, List<WeakReference> handlers)
        {
            if (handlers == null)
                return;
            EventHandler[] callees = new EventHandler[handlers.Count];
            int count = 0;
            int num = WeakEventHandlerManager.CleanupOldHandlers(handlers, callees, count);
            for (int index = 0; index < num; ++index)
            {
                WeakEventHandlerManager.CallHandler(sender, callees[index]);
            }
        }

        private static void CallHandler(object sender, EventHandler eventHandler)
        {
            DispatcherProxy dispatcher = WeakEventHandlerManager.DispatcherProxy.CreateDispatcher();
            if (eventHandler == null)
                return;
            if (dispatcher != null && !dispatcher.CheckAccess())
              dispatcher.BeginInvoke(new Action<object, EventHandler>(CallHandler), sender, eventHandler);
            else
                eventHandler(sender, EventArgs.Empty);
        }


        /// <summary>
        /// Clean up the old handlers (those that has been claimed by the Event handlers)
        /// </summary>
        /// <param name="handlers">the handlers list</param>
        /// <param name="callees">the callee that are still active</param>
        /// <param name="count">Count of alive callees</param>
        /// <returns></returns>
        private static int CleanupOldHandlers(List<WeakReference> handlers, EventHandler[] callees, int count)
        {
            for (int index = handlers.Count - 1; index >= 0; --index)
            {
                EventHandler eventHandler = handlers[index].Target as EventHandler;
                if (eventHandler == null)
                {
                    handlers.RemoveAt(index);
                }
                else
                {
                    callees[count] = eventHandler;
                    ++count;
                }
            }
            return count;
        }


        public static void AddWeakReferenceHandler(ref List<WeakReference> handlers, EventHandler handler, int defaultListSize)
        {
            if (handlers == null)
                handlers = defaultListSize > 0 ? new List<WeakReference>(defaultListSize) : new List<WeakReference>();

            handlers.Add(new WeakReference((object)handler));
        }

        public static void RemoveWeakReferenceHandler(List<WeakReference> handlers, EventHandler handler)
        {

            if (handlers == null)
                return;
            for (int index = handlers.Count - 1; index >= 0; --index)
            {
                EventHandler eventHandler = handlers[index].Target as EventHandler;
                if (eventHandler == null || eventHandler == handler)
                {
                    handlers.RemoveAt(index);
                }
            }
        }


        /// <summary>
        /// Hides the dispatcher mis-match between the silverlight and .Net ..
        /// </summary>
        private class DispatcherProxy
        {
            private Dispatcher innerDispatcher;

            private DispatcherProxy(Dispatcher dispatcher)
            {
                this.innerDispatcher = dispatcher;
            }


            public static WeakEventHandlerManager.DispatcherProxy CreateDispatcher()
            {
                if (Application.Current == null)
                {
                    return null;
                }
                return new DispatcherProxy(Application.Current.Dispatcher);
            }

            public bool CheckAccess()
            {
                return this.innerDispatcher.CheckAccess();
            }
            public DispatcherOperation BeginInvoke(Delegate method, params object[] args)
            {
                return this.innerDispatcher.BeginInvoke(method, DispatcherPriority.Normal, args);
            }
        }
    }
}

```

## How to use the WeakEventHandler,

suppose that you are the author of the command, then your command is suppose to remember the list of EventHandler that has been advised to be added to the Command implementaion. 


then we tries to subclass it to create a base class on top of the CheckedCommand. 

When a client advice to add a listen to one event, we can provide a overriden event handler to store the even thandler in the list. 

```
        public override event EventHandler CanExecuteChanged
        {
            add
            {
                WeakEventHandlerManager.AddWeakReferenceHandler(ref this._canExecuteChangedHandlers, value, 2);
            }
            remove
            {
                WeakEventHandlerManager.RemoveWeakReferenceHandler(this._canExecuteChangedHandlers, value);
            }
        }
```

As you can see, that first we have the event handler implementation that does the Add/Removing of the Event handler and store it back to a List of WeakRerence. 

then we have the code that iterate through the list of WeakReference and calls the event handler one by one. 

```
                    WeakEventHandlerManager.CallWeakReferenceHandlers(sender, this._canExecuteChangedHandlers);

```

let's see the compelte code : 

Now supposet that we first haVe those command base:

```
using System;
using System.Windows.Input;

namespace Common.Commands
{
    public abstract class CheckedCommand : ICommand
    {
        protected CheckedCommand(Predicate<object> canExecute)
        {
            _canExecute = canExecute;
        }

        public virtual void Execute(object parameter)
        {}

        private readonly Predicate<object> _canExecute;

        // todo - use a method similar to that used in the Dispose pattern, so this gets called automatically
        public virtual bool CanExecute(object parameter)
        {
            return _canExecute == null || _canExecute(parameter);
        }

        public virtual event EventHandler CanExecuteChanged
        {
            add { CommandManager.RequerySuggested += value; }
            remove { CommandManager.RequerySuggested -= value; }
        }
    }
}
```

now, let's see the code that does the real implementation.

```
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Input;
using System.Collections.Specialized;
using System.ComponentModel;



namespace Common.Commands
{
    /// <summary>
    /// TODO: Update 
    /// </summary>
    public class SelectedItemsAwareCheckedCommand : CheckedCommand
    {
        private IHaveSelectedItems _itemSource;

        protected SelectedItemsAwareCheckedCommand(Predicate<object> canExecute, IHaveSelectedItems itemSource)
            : base(canExecute)
        {
            _canExecute = canExecute;
            _itemSource = itemSource;
            _itemSource.SelectedItems.CollectionChanged += new NotifyCollectionChangedEventHandler(SelectedItemsCollectionChanged);
        }


        void SelectedItemsCollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
        {
            switch (e.Action)
            {
                case NotifyCollectionChangedAction.Add:
                case NotifyCollectionChangedAction.Replace:
                case NotifyCollectionChangedAction.Reset:
                  WeakEventHandlerManager.CallWeakReferenceHandlers(sender, this._canExecuteChangedHandlers);
                    break;
                case NotifyCollectionChangedAction.Remove:
                    break;
                case NotifyCollectionChangedAction.Move:
                    break;
            }
        }

        private readonly Predicate<object> _canExecute;

        private List<WeakReference> _canExecuteChangedHandlers;

        public override event EventHandler CanExecuteChanged
        {
            add
            {
                WeakEventHandlerManager.AddWeakReferenceHandler(ref this._canExecuteChangedHandlers, value, 2);
            }
            remove
            {
                WeakEventHandlerManager.RemoveWeakReferenceHandler(this._canExecuteChangedHandlers, value);
            }
        }
    }
}

```




