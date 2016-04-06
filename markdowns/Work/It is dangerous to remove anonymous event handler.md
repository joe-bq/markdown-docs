***** VERY IMPORTANT ****

I saw some code that does something like below. 

```
            _refreshing++;

            _viewColumnsCollection.ForEach(column =>
            {
                column.ContentChanged -= ColumnContentChanged;

                var descriptor = DependencyPropertyDescriptor.FromProperty(ColumnBase.SortOrderProperty, typeof(ColumnBase));
                if (descriptor != null)
                {
                    descriptor.RemoveValueChanged(column, (s, e) => DoSave());
                }
            });

            _propertyDescriptor.RemoveValueChanged(_gridControl.View, VisibleColumnsChanged);

            _viewColumnsCollection.ForEach(column =>
            {
                column.ContentChanged += ColumnContentChanged;
                var descriptor = DependencyPropertyDescriptor.FromProperty(ColumnBase.SortOrderProperty, typeof(ColumnBase));
                if (descriptor != null)
                {
                    descriptor.AddValueChanged(column, (s, e) => DoSave());
                }
            });

            _propertyDescriptor.AddValueChanged(_gridControl.View, VisibleColumnsChanged);

            _refreshing--;
```

the red-herring that I found is that it tries to remove 
`DoSave()`
as inside the context of a anonymous lambda expression 
`(o, e) => DoSave()`

However, it is very dangerous, in that it may not remove the handler after all.. 

as shown in the following test code , which I tried both the vanialla delegate removal as well as the one used by the DependencyPropertyDescriptor.


```
using System;
using System.ComponentModel;
using System.Windows;

namespace LambdaHandler
{
    class Program
    {
        // Reference:
        //   How to I access an attached property in code behind?: http://stackoverflow.com/questions/541420/how-to-i-access-an-attached-property-in-code-behind
        // 
        public static readonly DependencyProperty SampleProperty =
            DependencyProperty.RegisterAttached("Sample", typeof(string), typeof(Program), new PropertyMetadata(default(string)));

        private DependencyObject _depObj;
        
        public static string GetSample(DependencyObject component)
        {
            return (string)component.GetValue(SampleProperty);
        }

        public static void SetSample(DependencyObject component, string value)
        {
            component.SetValue(SampleProperty, value);
        }

        [STAThread]
        static void Main(string[] args)
        {
            Program p = new Program();
            
            p.Start();
            p.RaiseSampleEvent();
            p.Stop();
            p.RaiseSampleEvent();

            // you will see that the handler is still registered.
            // this won't work ...

            // let's do with the DependencyProperty things.
            Application app = new Application();
            Window window = new Window();
            p.DepObj = window;

            // this has to be done before the window is shown , otherwise, you won't be able to get back the Right DependencyProperty back 
            // through this code 
            //   DependencyPropertyDescriptor descriptor = DependencyPropertyDescriptor.FromProperty(SampleProperty, typeof(Window);
            // 
            Program.SetSample(window, string.Empty);
            if (string.Empty != Program.GetSample(window))
            {
                Console.WriteLine("Something goes wrong!");
            }

            window.Initialized += (o, e) => 
            {
                p.StartDep();
                p.RaiseSampleEventDep("a");
                p.StopDep();
                p.RaiseSampleEventDep("b");
            };
            app.Run(window);
            Program.SetSample(window, string.Empty);
            if (string.Empty != Program.GetSample(window))
            {
                Console.WriteLine("Something goes wrong!");
            }
        }

        public event EventHandler SampleEvent;

        public DependencyObject DepObj
        {
            get
            {
                return _depObj;
            }

            set
            {
                _depObj = value;
            }
        }

        public void DoSave()
        {
            Console.WriteLine("to save settings");
        }

        public void Start()
        {
            AddValueChanged((e, o) => DoSave());
        }

        public void Stop()
        {
            RemoveValueChanged((e, o) => DoSave());
        }


        public void AddValueChanged(EventHandler eventHandler)
        {
            SampleEvent += eventHandler;
        }

        public void RemoveValueChanged(EventHandler eventHandler)
        {
            SampleEvent -= eventHandler;
        }

        public void RaiseSampleEvent()
        {
            EventHandler temp = SampleEvent;
            if (temp != null)
            {
                temp(this, EventArgs.Empty);
            }
        }

        public void StartDep()
        {
            //DepObj.SetValue(SampleProperty, default(string));

            // The dependencyProperty may refer to a dependency property or an attached property. targetType is the type of object you want to set the property for. For dependency properties, that type is equivalent to the OwnerType for the dependencyProperty. For attached properties the targetType is typically some other DependencyObject type.
            // for AttachedProperty, the targetType is typically some other DependencyObject type

            var descriptor = DependencyPropertyDescriptor.FromProperty(Program.SampleProperty, typeof(Window));
            if (descriptor != null)
            {
                descriptor.AddValueChanged(DepObj, (s, e) => DoSaveDep());
            }
        }

        public void StopDep()
        {
            var descriptor = DependencyPropertyDescriptor.FromProperty(Program.SampleProperty, typeof(Window));
            if (descriptor != null)
            {
                descriptor.RemoveValueChanged(DepObj, (s, e) => DoSaveDep());
            }

            DepObj.SetValue(SampleProperty, default(string));
        }

        public void DoSaveDep()
        {
            Console.WriteLine("to save settings Dep");
        }

        public void RaiseSampleEventDep(string newValue)
        {
            SetSample(DepObj, newValue);
        }
    }
}

```


## TO READ

you can follow this link on the "alternatives to the PropertyDescriptor". 

[Alternative to Dependency properties](http://agsmith.wordpress.com/2008/04/07/propertydescriptor-addvaluechanged-alternative/) 