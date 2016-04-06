# introduction

in this page, we will examine some of the tips that aiming to boost the memory safety and others. 


## ConditionalWeaktable and others. 

`ConditionalWeakTable<TKey, TValue>` is a special table, not an dictionary, it has the good side that it does not hold reference to the key object which Dictionary object may suffer from leaking memories. 

from the MSDN site, it has the following blurbs.

> The ConditionalWeakTable<TKey, TValue> class enables language compilers to attach arbitrary properties to managed objects at run time. A ConditionalWeakTable<TKey, TValue> object is a dictionary that binds a managed object, which is represented by a key, to its attached property, which is represented by a value. The object's keys are the individual instances of the TKey class to which the property is attached, and its values are the property values that are assigned to the corresponding objects.

Comparing the dictionary,  it is different in the following parts.

* It does not persist keys. That is, a key is not kept alive only because it is a member of the collection.
* It does not include all the methods (such as GetEnumerator or Contains) that a dictionary typically has.
* It does not implement the IDictionary<TKey, TValue> interface.

> The ConditionalWeakTable<TKey, TValue> class differs from other collection objects in its management of the object lifetime of keys stored in the collection. Ordinarily, when an object is stored in a collection, its lifetime lasts until it is removed (and there are no additional references to the object) or until the collection object itself is destroyed. However, in the ConditionalWeakTable<TKey, TValue> class, adding a key/value pair to the table does not ensure that the key will persist, even if it can be reached directly from a value stored in the table (for example, if the table contains one key, A, with a value V1, and a second key, B, with a value P2 that contains a reference to A). Instead, ConditionalWeakTable<TKey, TValue> automatically removes the key/value entry as soon as no other references to a key exist outside the table. The example provides an illustration.


below is the code that to demonstrate the ablity of the class.

```
using System;
using System.Runtime.CompilerServices;

namespace ConditionalWeakTableDemo
{
    public class ManagedClass
    {
    }

    public class ClassData
    {
        public DateTime CreationTime;
        public object Data;

        public ClassData()
        {
            CreationTime = DateTime.Now;
            Data = new object();
        }
    }

    /// <summary>
    /// Demon that the WeakTableReference does not keeps the key in collection.
    /// </summary>
    public class Program
    {
        public static void Main()
        {
            var mc1 = new ManagedClass();
            var mc2 = new ManagedClass();
            var mc3 = new ManagedClass();


            var cwt = new ConditionalWeakTable<ManagedClass, ClassData>();
            cwt.Add(mc1, new ClassData());
            cwt.Add(mc2, new ClassData());
            cwt.Add(mc3, new ClassData());

            var wr2 = new WeakReference(mc2);

            // now we ensure that the mc2 is garbage collected
            mc2 = null;
            GC.Collect();

            ClassData data = null;

            if (wr2.Target == null)
            {
                Console.WriteLine("No Strong reference to mc2 exists.");
            }
            else if (cwt.TryGetValue(mc2, out data))
            {
                Console.WriteLine("Data created at {0}", data.CreationTime);
            }
            else
            {
                Console.WriteLine("mc2 not found in the table");
            }

            Console.ReadLine();
        }
    }
}
```

## System.Windows.Interactivity EventTrigger


```
    <i:Interaction.Triggers>
        <i:EventTrigger EventName="PreviewKeyDownEvent">
            <i:InvokeCommandAction Command="{Binding ElementName=SnapSplitter, Path=MoveBottomRightCommand}" />
        </i:EventTrigger>
    </i:Interaction.Triggers>
```
You will need the following xmlns declaration.

```
    xmlns:i="clr-namespace:System.Windows.Interactivity;assembly=System.Windows.Interactivity"
```

it is a Interaction.Trigger which convert an event to Command invocation.

## Keyboard.IsKeyDown and the ModifierKeys.Control & Keyboard.modifers

There are several ways to determine if we there is modifier key has been pressed.let me show two of them.

first is the use of the Keyboard.IsKeyDown() function with the Key property of the `KeyEventArgs`


```
		protected override void OnKeyDown(KeyEventArgs e)
		{
			base.OnKeyDown(e);

			if (e.Handled)
			{
				return;
			}

			if (Keyboard.IsKeyDown(Key.LeftCtrl)
				|| Keyboard.IsKeyDown(Key.RightCtrl))
			{
				switch (e.Key)
				{
					case Key.Left:
					case Key.Up:
						if (CanMoveTopLeft())
						{
							OnMoveTopLeft();
							e.Handled = true;
						}

						return;

					case Key.Right:
					case Key.Down:
						if (CanMoveBottomRight())
						{
							OnMoveBottomRight();
							e.Handled = true;
						}

						break;
				}
			}
			else
			{
				switch (e.Key)
				{
					case Key.Left:
						e.Handled = KeyboardMoveSplitter(-KeyboardIncrement, 0.0);
						return;

					case Key.Up:
						e.Handled = KeyboardMoveSplitter(0.0, -KeyboardIncrement);
						return;

					case Key.Right:
						e.Handled = KeyboardMoveSplitter(KeyboardIncrement, 0.0);
						return;

					case Key.Down:
						e.Handled = KeyboardMoveSplitter(0.0, KeyboardIncrement);
						break;
				}
			}
		}
```


also, you can leverage the `ModifierKeys` enum, the following code demonstrated it.

```
        private void TopWindowPreviewKeyDown(object sender, KeyEventArgs e)
        {
            if ((ModifierKeys.Control & Keyboard.Modifiers) == ModifierKeys.Control)
            {
                switch (e.Key)
                {
                    case Key.Left:
                        if (AssociatedObject.MoveTopLeftCommand.CanExecute())
                        {
                            AssociatedObject.MoveTopLeftCommand.Execute();
                            e.Handled = true;
                        }

                        break;
                    case Key.Right:
                        if (AssociatedObject.MoveBottomRightCommand.CanExecute())
                        {
                            AssociatedObject.MoveBottomRightCommand.Execute();
                            e.Handled = true;
                        }
                        break;
                }
            }
        }
```


## Control.SelectNextControl Method and MoveFocus.. 

Activates the next control.

well, this is from the 'System.Windows.Forms', in WPF, you can use the UIElement.MoveFocus method, which is from the following namespace. `System.Windows` from the PresentationCore.dll.


References:

[Control_SelectNextControl]: http://msdn.microsoft.com/en-us/library/system.windows.forms.control.selectnextcontrol(v=vs.110).aspx
[Control.SelectNextControl][Control_SelectNextControl]


## Double utils

there are some very intricate double mathmetics operations in Program that everybody should be aware of.

First let's see some code from DoubleUtil from Microsoft.. 


```
    /// <summary>
    /// Some helper routines for double type
    /// </summary>
    public static class DoubleUtil
    {
        public static bool AreClose(double value1, double value2)
        {
            if (value1 == value2)
            {
                return true;
            }

            double num = ((Math.Abs(value1) + Math.Abs(value2)) + 10.0) * 2.2204460492503131E-16;
            double num2 = value1 - value2;
            return (-num < num2) && (num > num2);
        }

        public static bool AreClose(Point point1, Point point2)
        {
            return AreClose(point1.X, point2.X) && AreClose(point1.Y, point2.Y);
        }

        public static string ToSafeString(this double? target, string format)
        {
            return target.HasValue ? target.Value.ToString(format) : string.Empty;
        }
    }
```
you may wonder why there is such code .

the reason is because the floating point arithmetic has some limitation that that it cannot represent some very small differences, and the differences between two doubles values that it cannot tell increases when values increases.


the 10.0 here is the magic number, whlie for the value of 2.2204460492503131E-16; there are more explaination from the following pages. [C# - I'm trying to understand Microsoft's DoubleUtil.AreClose() code that I reflected over][microsoft_doubleutil_areclose].  Which leads to the fundamental of double precision calculation, one important concept is called the [machine epsilon][machine_epsilon].

now back to the magic number 10.0, which I guess that the utility assumes that the most common rounding source comes from the conversion from decimal numbers to the machine floating points numbers.

there are more fundamental floating-point knowledge such as [Double-precision floating-point format][double_precision_floating_point_format]. and [wikipedia floating point about conversion and rounding][floating_point_conversion_rounding].



References:
[microsoft_doubleutil_areclose]: http://stackoverflow.com/questions/5758726/c-sharp-im-trying-to-understand-microsofts-doubleutil-areclose-code-that-i
[C# - I'm trying to understand Microsoft's DoubleUtil.AreClose() code that I reflected over][microsoft_doubleutil_areclose]
[machine_epsilon]: http://en.wikipedia.org/wiki/Machine_epsilon
[machine epsilon][machine_epsilon]

[double_precision_floating_point_format]:http://en.wikipedia.org/wiki/Double_precision
[Double-precision floating-point format][double_precision_floating_point_format]
[floating_point_conversion_rounding]: http://en.wikipedia.org/wiki/Floating_point#Representable_numbers.2C_conversion_and_rounding
 [wikipedia floating point about conversion and rounding][floating_point_conversion_rounding]


## SizeToContent WidthAndHeight has this extra border

it has been known to all that there is some problem when the SizeToContent property is set to SizeToContent.WidthAndHeight... 

one of the post suggested the following..

```
ublic class RoundConverter : IValueConverter {
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture) {
        return Math.Ceiling((double)value);
    }
    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture) {
        return value;
    }
}
```

and then create the following elements from the XAML file. 

```
<c:RoundConverter x:Key="RoundConverter"/>

<Style TargetType="{x:Type Border}" x:Key="WindowBorder">
    <Setter Property="Width" Value="{Binding RelativeSource={RelativeSource Self}, Path=ActualWidth, Converter={StaticResource RoundConverter}}"/>
    <Setter Property="Height" Value="{Binding RelativeSource={RelativeSource Self}, Path=ActualHeight, Converter={StaticResource RoundConverter}}"/>
</Style>
```

and listen to the Window loaded events. 

```
private void Window_Loaded(object sender, RoutedEventArgs e) {
    GetVisualChild(0).SetValue(StyleProperty, Application.Current.Resources["WindowBorder"]);
}
```

However, I tried but not helpful.


while, the last one suggested by Li na is as follow.  

```
        public override void OnApplyTemplate()
        {
          base.OnApplyTemplate();
          Dispatcher.BeginInvoke(
            DispatcherPriority.Loaded,
            (Action)(() =>
              {
                SizeToContent = SizeToContent.WidthAndHeight;
                double height = SystemParameters.WorkArea.Height;
                double width = SystemParameters.WorkArea.Width;
                Top = (height - Height) / 2;
                Left = (width - Width) / 2;
              }));
        }
```



References:
[(utomatic resizing when border content has changed)](http://stackoverflow.com/questions/11895814/automatic-resizing-when-border-content-has-changed)
[(SizeToContent paints an unwanted border)](http://stackoverflow.com/questions/16356507/sizetocontent-paints-an-unwanted-border)



## Center to center of monitor

while you can get from the SystemParameters.PrimaryScreenWidth and SystemParameters.PrimaryScreenHeight and etc.. to get the dimension/stretch of the primary screen, but times now that multiple screen are common in nowadays. what if you want to center to the monitor where the mouse is?

You will need to reference the System.Windows.Forms and the System.Drawing.

Screen.AllScreens will return you the collection Screens. and Control.MousePosition to get the mouse position relative to the screen.

the code is as below. 

```
		var point = Control.MousePosition;
        foreach (var screen in Screen.AllScreens)
        {
           if (screen.Bounds.Contains(point))
           {
              Top = screen.Bounds.Top + (screen.Bounds.Height - Height) / 2;
              Left = screen.Bounds.Left + (screen.Bounds.Width - Width) / 2;
           }
       }

```

While if you don't want to introduce System.Windows.Forms as your assembly, you can also try to use P/Invoke to query for the System Metrics. (GetMonitorInfo together with GetSystemMetrics)  

Another alternative to get the mouse position is by the P/Invoke, the reference is [How do I get the current mouse screen coordinates in WPF? - Stack Overflow](http://stackoverflow.com/questions/4226740/how-do-i-get-the-current-mouse-screen-coordinates-in-wpf)

References
[How to show() a wpf window in secondary monitor](http://social.msdn.microsoft.com/Forums/en-US/32d60663-8264-4153-9fb0-7053468191f2/how-to-show-a-wpf-window-in-secondary-monitor?forum=wpf)
[GetSystemMetrics function (Windows)](http://msdn.microsoft.com/en-us/library/ms724385%28v=vs.85%29.aspx)
[GetMonitorInfo function (Windows)](http://msdn.microsoft.com/en-us/library/dd144901%28v=vs.85%29.aspx)
[c++ - How detect current screen resolution? - Stack Overflow](http://stackoverflow.com/questions/4631292/how-detect-current-screen-resolution)
[winforms - How do I find what screen the application is running on in C# - Stack Overflow](http://stackoverflow.com/questions/549751/how-do-i-find-what-screen-the-application-is-running-on-in-c-sharp)
[How to Exploit Multiple Monitor Support in Memphis and Windows NT 5.0](http://www.microsoft.com/msj/0697/monitor/monitor.aspx)
[How do I get the current mouse screen coordinates in WPF? - Stack Overflow](http://stackoverflow.com/questions/4226740/how-do-i-get-the-current-mouse-screen-coordinates-in-wpf)

## KeyBinding with Key+Modifiers and/or Gestures

*  specifier more than one modifiers
suppose that you want to specify more than one modifiers, such as Ctrl+Shift, they are two modifiers enum values, how do you specify it in xaml file?

it is simple, you can just use the '+' key to specify it...

```
    <KeyBinding
     Gesture="Ctrl+Shift+Add"
      Command="{Binding CtrlPlusCommand}" />
```
as compare to only specify one modifiers key, e.g. as below. 
```
    <KeyBinding
     Gesture="Ctrl+Add"
      Command="{Binding CtrlPlusCommand}" />
```

* Gestures vs. Keys and Modifiers
it has been stated that from [KeyBinding.Key 属性 (System.Windows.Input)](http://msdn.microsoft.com/zh-cn/library/system.windows.input.keybinding.key(v=vs.110).aspx) it is interchangeable to use either gestures or Keys+Modifiers. 

e.g. the above code can be changed to the following respectively.

```
    <KeyBinding
     Gesture="Ctrl+Shift+Add"
      Command="{Binding CtrlPlusCommand}" />
```
and 

```
    <KeyBinding
     Gesture="Ctrl+Add"
      Command="{Binding CtrlPlusCommand}" />
```   


* Special Keys
you might be tempted to do the following. 

```
    <KeyBinding
     Gesture="Ctrl+Shift++"
      Command="{Binding CtrlPlusCommand}" />

    <KeyBinding
     Gesture="Ctrl++"
      Command="{Binding CtrlPlusCommand}" />
```

It does not tell you error, but you won't be able to trigger the sequence because '+' is not recognized as the proper key recognied by WPF.

however, if you change that to "Ctrl+Shift+Add", where Add is recognied the valid Key then it just works fine

* OemAdd or Add
from [Key 枚举 (System.Windows.Input)](http://msdn.microsoft.com/zh-cn/library/system.windows.input.key(v=vs.110).aspx), there are two "Add", one is "OemAdd" and the other is "Add".

the "Add" is for the numpad '+' sign, while there is also a '+' at the main keyboard area. and its name is "OemAdd", why such a stupid name, don't ask me...

references:

[WPF: Creating KeyBinding with more than 1 modifier keys - Stack Overflow](http://stackoverflow.com/questions/4050066/wpf-creating-keybinding-with-more-than-1-modifier-keys)
[Key 枚举 (System.Windows.Input)](http://msdn.microsoft.com/zh-cn/library/system.windows.input.key(v=vs.110).aspx)
[ModifierKeys 枚举 (System.Windows.Input)](http://msdn.microsoft.com/zh-cn/library/system.windows.input.modifierkeys(v=vs.110).aspx)
[KeyBinding.Key 属性 (System.Windows.Input)](http://msdn.microsoft.com/zh-cn/library/system.windows.input.keybinding.key(v=vs.110).aspx)

## Focus related

about binding a property to a control to get it focused, there are several ways that has been proposed. they are 

1. send message
```
 Messenger.Default.Send<string>("focus", "DoFocus");
```

then from the View, does the SetFocus

```
		public MyView()
        {
            InitializeComponent();

            Messenger.Default.Register<string>(this, "DoFocus", doFocus);
        }
        public void doFocus(string msg)
        {
            if (msg == "focus")
                this.txtcode.Focus();
        }
```

2. Attached properties

```

<TextBox ... h:FocusBehavior.IsFocused="True"/>

```

then 

```
/// <summary>
/// Behavior allowing to put focus on element from the view model in a MVVM implementation.
/// </summary>
public static class FocusBehavior
{
    #region Dependency Properties
    /// <summary>
    /// <c>IsFocused</c> dependency property.
    /// </summary>
    public static readonly DependencyProperty IsFocusedProperty =
        DependencyProperty.RegisterAttached("IsFocused", typeof(bool?),
            typeof(FocusBehavior), new FrameworkPropertyMetadata(IsFocusedChanged));
    /// <summary>
    /// Gets the <c>IsFocused</c> property value.
    /// </summary>
    /// <param name="element">The element.</param>
    /// <returns>Value of the <c>IsFocused</c> property or <c>null</c> if not set.</returns>
    public static bool? GetIsFocused(DependencyObject element)
    {
        if (element == null)
        {
            throw new ArgumentNullException("element");
        }
        return (bool?)element.GetValue(IsFocusedProperty);
    }
    /// <summary>
    /// Sets the <c>IsFocused</c> property value.
    /// </summary>
    /// <param name="element">The element.</param>
    /// <param name="value">The value.</param>
    public static void SetIsFocused(DependencyObject element, bool? value)
    {
        if (element == null)
        {
            throw new ArgumentNullException("element");
        }
        element.SetValue(IsFocusedProperty, value);
    }
    #endregion Dependency Properties

    #region Event Handlers
    /// <summary>
    /// Determines whether the value of the dependency property <c>IsFocused</c> has change.
    /// </summary>
    /// <param name="d">The dependency object.</param>
    /// <param name="e">The <see cref="System.Windows.DependencyPropertyChangedEventArgs"/> instance containing the event data.</param>
    private static void IsFocusedChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        // Ensure it is a FrameworkElement instance.
        var fe = d as FrameworkElement;
        if (fe != null && e.OldValue == null && e.NewValue != null && (bool)e.NewValue)
        {
            // Attach to the Loaded event to set the focus there. If we do it here it will
            // be overridden by the view rendering the framework element.
            fe.Loaded += FrameworkElementLoaded;
        }
    }
    /// <summary>
    /// Sets the focus when the framework element is loaded and ready to receive input.
    /// </summary>
    /// <param name="sender">The sender.</param>
    /// <param name="e">The <see cref="System.Windows.RoutedEventArgs"/> instance containing the event data.</param>
    private static void FrameworkElementLoaded(object sender, RoutedEventArgs e)
    {
        // Ensure it is a FrameworkElement instance.
        var fe = sender as FrameworkElement;
        if (fe != null)
        {
            // Remove the event handler registration.
            fe.Loaded -= FrameworkElementLoaded;
            // Set the focus to the given framework element.
            fe.Focus();
            // Determine if it is a text box like element.
            var tb = fe as TextBoxBase;
            if (tb != null)
            {
                // Select all text to be ready for replacement.
                tb.SelectAll();
            }
        }
    }
    #endregion Event Handlers
}
```

3. Behavior
```
using System.Windows;
using System.Windows.Controls;
using System.Windows.Interactivity;

namespace MyProject.Behaviors
{
    public class FocusBehavior : Behavior<Control>
    {
        protected override void OnAttached()
        {
            this.AssociatedObject.Loaded += AssociatedObject_Loaded;
            base.OnAttached();
        }

        private void AssociatedObject_Loaded(object sender, RoutedEventArgs e)
        {
            this.AssociatedObject.Loaded -= AssociatedObject_Loaded;
            if (this.HasInitialFocus || this.IsFocused)
            {
                this.GotFocus();
            }
        }

        private void GotFocus()
        {
            this.AssociatedObject.Focus();
            if (this.IsSelectAll)
            {
                if (this.AssociatedObject is TextBox)
                {
                    (this.AssociatedObject as TextBox).SelectAll();
                }
                else if (this.AssociatedObject is PasswordBox)
                {
                    (this.AssociatedObject as PasswordBox).SelectAll();
                }
                else if (this.AssociatedObject is RichTextBox)
                {
                    (this.AssociatedObject as RichTextBox).SelectAll();
                }
            }
        }

        public static readonly DependencyProperty IsFocusedProperty =
            DependencyProperty.Register(
                "IsFocused",
                typeof(bool),
                typeof(FocusBehavior),
                new PropertyMetadata(false, 
                    (d, e) => 
                    {
                        if ((bool)e.NewValue)
                        {
                            ((FocusBehavior)d).GotFocus();
                        }
                    }));

        public bool IsFocused
        {
            get { return (bool)GetValue(IsFocusedProperty); }
            set { SetValue(IsFocusedProperty, value); }
        }

        public static readonly DependencyProperty HasInitialFocusProperty =
            DependencyProperty.Register(
                "HasInitialFocus",
                typeof(bool),
                typeof(FocusBehavior),
                new PropertyMetadata(false, null));

        public bool HasInitialFocus
        {
            get { return (bool)GetValue(HasInitialFocusProperty); }
            set { SetValue(HasInitialFocusProperty, value); }
        }

        public static readonly DependencyProperty IsSelectAllProperty =
            DependencyProperty.Register(
                "IsSelectAll",
                typeof(bool),
                typeof(FocusBehavior),
                new PropertyMetadata(false, null));

        public bool IsSelectAll
        {
            get { return (bool)GetValue(IsSelectAllProperty); }
            set { SetValue(IsSelectAllProperty, value); }
        }

    }
}
```
and from the Xaml file, it has the following. 

```
xmlns:i="http://schemas.microsoft.com/expression/2010/interactivity"
xmlns:beh="clr-namespace:MyProject.Behaviors"

<TextBox Text="{Binding Email, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}">
    <i:Interaction.Behaviors>
        <beh:FocusBehavior IsFocused="{Binding EmailFocus}" IsSelectAll="True"/>
    </i:Interaction.Behaviors>
</TextBox>
```

References
[Set focus on textbox in WPF from view model (C#) & wPF - Stack Overflow](http://stackoverflow.com/questions/1356045/set-focus-on-textbox-in-wpf-from-view-model-c-wpf)

## FocusManager.FocusElement


```
UserControl x:Class="WpfApplication3.UserControl1"
         xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
         xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
<Grid FocusManager.FocusedElement="{Binding ElementName=MyTextBox, Mode=OneWay}">
    <TextBox x:Name="MyTextBox"/>
</Grid>
```

References:

[wpf - Can't set focus to a child of UserControl - Stack Overflow](http://stackoverflow.com/questions/673536/cant-set-focus-to-a-child-of-usercontrol)

[Part 3: Shifting focus to the first available element in WPF - JulMar Technology](http://www.julmar.com/blog/programming/part-3-shifting-focus-to-the-first-available-element-in-wpf/)

[Part 1: It's Basically Focus - JulMar Technology](http://www.julmar.com/blog/programming/part-1-its-basically-focus/)

[Part 2: Changing WPF focus in code - JulMar Technology](http://www.julmar.com/blog/programming/part-2-changing-wpf-focus-in-code/)

[Focus | 2,000 Things You Should Know About WPF](http://wpf.2000things.com/tag/focus/)


##Force the visual tree to load

the original post's problem is as follow. 

> I have a tab control and it's not loading the controls on any of the hidden tabs until the user clicks on that tab. But I have code when the form first opens that's walking the visual tree setting properties on various controls.  But since it can't see what's not loaded yet, the properties don't get set. And then when the user switches to that tab, they're not rendering correctly.

> How can I force the tab control, expander control, etc to force load their visual tree?

Well, I have a simlar situation that the ComboBox is initially hidden, and it has a binding which convert the Visibility

```
			Visibility="{Binding DisplayInstrumentSelection, Converter={StaticResource BooleanToVisibilityConverter}}">
```

I have a behavior which tries to set focus to a control once it has become visible. the code that hooks in the behavior is as follow.

```
          <i:Interaction.Behaviors>
            <behaviors:FocusBehavior
              IsFocused="{Binding DisplayInstrumentSelection, Mode=OneWay}" />
          </i:Interaction.Behaviors>
```
and in the callback `GotFocus` method, I have the following. 

```
    private void GotFocus()
    {
      AssociatedObject.Focus();
    }
```

the ComboBox is not focused, though the IsVisible, IsEnabled, and IsFocused value are all "True" values after the code. 

the answers posted by the support guy suggest two ways, they are 

1. LoadContent 
2. Unload/Load? property

the reason for this is because:
> the VisualTree will only consider elements that are visible, so that really is a dead end for what you have in mind. If you need to perform operations on controls that aren't (yet) visible, consider using LogicalTreeHelper instead.

the `LoadContent` call is essential that it force applying the data template. Our combobox does have a implicit/default style applied. 

Also, some one suggested to call "UpdateLayout()", an example is as follow

```
    private T GetChildOfType<T>(DependencyObject depObj) where T : DependencyObject
    {
      if (depObj == null) return null;

      var childCount = VisualTreeHelper.GetChildrenCount(depObj);
      if (childCount == 0)
      {
        if (depObj is UIElement)
        {
          ((UIElement)depObj).UpdateLayout();
        }
      }

      for (int i = 0; i < VisualTreeHelper.GetChildrenCount(depObj); i++)
      {
        var child = VisualTreeHelper.GetChild(depObj, i);
        var result = (child as T) ?? GetChildOfType<T>(child);
        if (result != null) return result;
      }

      return null;
    }
```

without the UpdateLayout call, if a control Visual Tree is not rendered, you might get 0 from `VisualTreeHelper.GetChildrenCount(depObj)` call. 

Also, I tried to call the ApplyTemplate on the control. you just replace the following code in the above snippet's relevant places. 

```
      if (childCount == 0)
      {
        if (depObj is Control)
        {
          ((Control)depObj).ApplyTemplate();
        }
      }
```


I tried to forcibly call the `UpdateLayout` to make sure AssociatedObject are fully loaded/rendered, but failed, instead, I have the following code. 

```
    private void GotFocus()
    {
      //TextBox comboboxEdit = GetChildOfType<TextBox>(AssociatedObject);
      //if (comboboxEdit != null)
      //{
      //  new DelayTask(TimeSpan.FromMilliseconds(300), _delayTasks).Task.ContinueWith(
      //    t => comboboxEdit.Focus(),
      //    CancellationToken.None,
      //    TaskContinuationOptions.OnlyOnRanToCompletion,
      //    UITaskSchedulerService.Instance.GetUITaskScheduler());
      //}
      new DelayTask(TimeSpan.FromMilliseconds(300), _delayTasks).Task.ContinueWith(
        t => AssociatedObject.Focus(),
        CancellationToken.None,
        TaskContinuationOptions.OnlyOnRanToCompletion,
        UITaskSchedulerService.Instance.GetUITaskScheduler());
    }
```

it was suggested that the LogicTreeHelper is not affected by the render issue, I wrote the following. 

```
    private T GetLogiclaChildOfType<T>(DependencyObject depObj) where T : DependencyObject
    {
      if (depObj == null) return null;

      foreach (DependencyObject child in LogicalTreeHelper.GetChildren(depObj))
      {
        var result = (child as T) ?? GetLogiclaChildOfType<T>(child);
        if (result != null) return result;
      }
      
      return null;
    }
```

the combobox does not have a child?? and it returns null.


References:
[How can I force the visual tree to load](http://social.msdn.microsoft.com/Forums/vstudio/en-US/bf691a3d-c77e-4faa-b5c5-0e6a4f0f559f/how-can-i-force-the-visual-tree-to-load?forum=wpf)
[c# - Appropriate way to force loading of a WPF Visual - Stack Overflow](http://stackoverflow.com/questions/16224986/appropriate-way-to-force-loading-of-a-wpf-visual)
[DataTemplate.LoadContent Method (System.Windows)](http://msdn.microsoft.com/en-us/library/system.windows.datatemplate.loadcontent(VS.95).aspx)
[C# combobox only allow list items BUT allow typing - CodeProject](http://www.codeproject.com/Questions/99037/C-combobox-only-allow-list-items-BUT-allow-typing)


##ComboBox IsReadonly and IsEditable combination and IsTextSearchable
To give the ComboBox the ability to search through the fields, there are some properteis that you can control the behavior of the ComboBox, among them, there are values such as:

* IsReadOnly
* IsEditable
* IsTextSearchEnabled
* TextSearch.TextPath

#### IsReadOnly and IsEditable

IsReadOnly comes hand in hand with the IsEditable, as in the following quote:

> The IsEditable and IsReadOnly properties specify how the ComboBox behaves when the user does one of the following:
Enters a string to select an item in the ComboBox.
Enters a string that does not correspond to an item in the ComboBox.
Selects part of the string that is in the text box.
Copies or pastes a value into the text box.

There is a table 

|  _  |    IsReadOnly is true | IsReadOnly is false  |
| -------- | -----------------------------| ----------------------------------------------- |
| IsEditable is true | Cannot select; Cannot enter; can partly select; Can copy but not paste  | Can select; can enter; can select part; can copy or paste |
| IsEditable is false | Can select; cannot enter, cannot select, cannot copy;   | the same..   |

#### TextSearch.TextPath 
while the TextSearch.TextPath is used to refer to the property of the bound object that contains the text that you can type in order to select an item.

If you can using an item template to set conent for each item, rather than DisplayMemberPath, you can sepcify the properly used when typing text by setting the **TextSearch.TextPath** property.

#### Search text in Multiple binding situations

when the Text displayed in the ComboBox has multiple binding enabled, it requires more works  in order to support search on the sources. 
Please refers to the Stack Overflow question: [wpf - Can I do Text search with multibinding - Stack Overflow](http://stackoverflow.com/questions/4750220/can-i-do-text-search-with-multibinding)

#### the combination of IsReadOnly and IsEditable with the Focus issue
the focus issue talked above has special behavior when regards to the combination of the IsReadOnly and IsEditable. 

when IsReadOnly is false, and IsEditable is false, with the delay task , the control will have focus correctly and you can directly type after pressing the Ctrl+Shift+"+/=" key.

However, with other combination of IsEdiable and IsReadonly values, or if without the delay task, when the Visual is focused, you can only select by up/down keys.

#### References
[TextSearch.TextPath Attached Property (System.Windows.Controls)](http://msdn.microsoft.com/en-us/library/system.windows.controls.textsearch.textpath(v=vs.110).aspx)
[TextSearch.TextPath | 2,000 Things You Should Know About WPF](http://wpf.2000things.com/tag/textsearch-textpath/)
[wpf - Can I do Text search with multibinding - Stack Overflow](http://stackoverflow.com/questions/4750220/can-i-do-text-search-with-multibinding)


## VisibilityToBoolean Converter

the converter which does hte reverse of conversion... from the Visibility to the Boolean . 

```
  public class VisibilityToBooleanConverter : IValueConverter
  {

    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
      if (value == DependencyProperty.UnsetValue)
      {
        return false;
      }

      if (!(value is Visibility))
      {
        throw new ArgumentException("Expecting a Visibility type");
      }

      var visibility = (Visibility)value;
      return visibility == Visibility.Visible;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
      throw new NotImplementedException();
    }
  }
```


## Attempt to Resolve the ComboBox issues
Spent some time searching for alternatives, tried the followings.

*	call UpdateLayout/ApplyTemplate to force the visual tree
*	register handlers to the Loaded/Unloaded event
*	register handlers to the outer border's Visibility change event
*	binding to the Visibility property of the outer border's with a Visibility to Boolean converter

None of above is working.... Might come back to this with more ideas suggestions come up.


## Default Style in Design mode
When you wrote up a custom control, the next step is to define a custom template for it. 


e.g.


```
class EditControlMaster : Control 
{

 static EditControlMaster()
        {
            DefaultStyleKeyProperty.OverrideMetadata(typeof(BusyIndicator),
                new FrameworkPropertyMetadata(typeof(BusyIndicator)));

        }
}
```


then you can create the default style for that control with the the following way

```
<Style TargetType="{x:Type shareduc:EditControlMaster}">
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="{x:Type shareduc:EditControlMaster}">
                <Grid>
                    <Grid.ColumnDefinitions></Grid.ColumnDefinitions>
                    <Grid.RowDefinitions>
                        <RowDefinition Height="auto"></RowDefinition>
                        <RowDefinition Height="*"></RowDefinition>
                    </Grid.RowDefinitions>

                    <Border BorderBrush="{DynamicResource xxBorderBrush}" 
                                BorderThickness="0,1,0,1" Background="White" Grid.Row="0">
                        <Grid >
                            <Grid.ColumnDefinitions>
                                <ColumnDefinition Width="auto"></ColumnDefinition>
                                <ColumnDefinition Width="*"></ColumnDefinition>
                            </Grid.ColumnDefinitions>
                            <Grid.RowDefinitions>
                                <RowDefinition Height="auto"></RowDefinition>
                                <RowDefinition Height="auto"></RowDefinition>
                            </Grid.RowDefinitions>

                            <ContentPresenter Grid.Row="0" Grid.Column="0" Grid.RowSpan="2" Margin="10" Content="{TemplateBinding Image}"  />
                            <ContentPresenter Grid.Row="0" Grid.Column="1" Margin="2" Content="{TemplateBinding Title}"  />
                            <ContentPresenter Grid.Row="1" Grid.Column="1" Margin="2" Content="{TemplateBinding Abstract}"  />
                        </Grid>
                    </Border>

                    <ContentPresenter Grid.Row="1" Margin="2" Content="{TemplateBinding Content}" />

                </Grid>

            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```


this can be in a separate .xaml file, but how can the WPF runtime knows which default style to load (given that the style can be defined in many a xaml files )


the Assembly.cs file needs to contain the following attributes 
```
[assembly: ThemeInfo(
    ResourceDictionaryLocation.None, //where theme specific resource dictionaries are located
    //(used if a resource is not found in the page, 
    // or application resource dictionaries)
    ResourceDictionaryLocation.SourceAssembly //where the generic resource dictionary is located
    //(used if a resource is not found in the page, 
    // app, or any theme specific resource dictionaries)
)]
```

References:
[wpf - Creating default style for custom control - Stack Overflow](http://stackoverflow.com/questions/1237611/creating-default-style-for-custom-control)



## ContentProperty attribute

you can decorate a conttrol with the "ContentProperty" attribute which means without enclosing name, the default content name will be used. 

```
    [TemplatePartAttribute(Name = PART_ViewBox, Type = typeof(Viewbox))]
    [TemplatePartAttribute(Name = PART_Canvas, Type = typeof(Canvas))]
    [TemplatePartAttribute(Name = PART_ContainerGrid, Type = typeof(System.Windows.Controls.Grid))]
    [ContentProperty("BusyContent")]
    public class BusyIndicator : Control
```


## Replace the Delegate asynchronous pattern with the Task Asynchronous pattern

suppose that we have a method like this

```
        public void BeginGetTopics(List<string> instruments, Action<List<InstrumentSubjectMap>> callback)
        {
            Func<List<string>, List<InstrumentSubjectMap>> getTopics = GetTopics;
            AsyncCallback asyncCallback = ar =>
                {
                    var topics = getTopics.EndInvoke(ar);
                    
                    if (callback != null)
                    {
                        callback(topics);
                    }
                };

            getTopics.BeginInvoke(instruments, asyncCallback, null);
        }
```

now we can change that to the following.

```
        public void BeginGetTopics(List<string> instruments, Action<List<InstrumentSubjectMap>> callback)
        {
            var task = Task.Factory.StartNew(
                () => GetTopics(instruments));
            if (callback != null)
            {
                task.ContinueWith(t => callback(t.Result));
            }
        }
```


another example would be 

```
        public void AsyncLogon(string login, string password, PartitionState partition = null)
        {
            BeginLogonCallback(login, password, partition, ar =>
                {
                    var asyncResult = ar as AsyncResult;
                    if (asyncResult != null)
                    {
                        ((AsyncCallback)asyncResult.AsyncDelegate).EndInvoke(ar);
                    }
                }, null);
        }
```

Changed to the following.

## C# Asynchronous Programming Patterns

there are a bunch of asynchronous pattern that has been vouched by the .NET and C# language itself. here is the patterns. 


1. synchronous patterns 
2. Begin/End pattern (including the delegate patterns)
3. Async/Event pattern
4. Task pattern
5. async/await keyword
6. concurrency/parallel programming model
7. manual thread
8. background thread pool

1. example of the Synchronous pattern is as such 
```
public class MyClass
{
    public int Read(byte [] buffer, int offset, int count);
}
```

2. then you can have the APM pattern. 
```
public class MyClass
{
    public IAsyncResult BeginRead(
        byte [] buffer, int offset, int count, 
        AsyncCallback callback, object state);
    public int EndRead(IAsyncResult asyncResult);
}
```

3. EAP counterpart would expose teh following set of types and memebers
```
public class MyClass
{
    public void ReadAsync(byte [] buffer, int offset, int count);
    public event ReadCompletedEventHandler ReadCompleted;
}
```

4. the TAP counterparty would expose the following single ReadAsync method: 
```
public class MyClass
{
    public Task<int> ReadAsync(byte [] buffer, int offset, int count);
}
```


References:
[Asynchronous Programming Patterns](http://msdn.microsoft.com/en-us/library/jj152938(v=vs.110).aspx)
[Parallel Processing and Concurrency in the .NET Framework](http://msdn.microsoft.com/en-us/library/hh156548(v=vs.110).aspx)
[Parallel Tasks](http://msdn.microsoft.com/en-us/library/ff963549.aspx)

## Use TaskScheduler.UnobservedTaskScheduler to handle unobserved exception

while according to the [Parallel Tasks](http://msdn.microsoft.com/en-us/library/ff963549.aspx), 

>Another important aspect of task-based applications is how they handle exceptions. In .NET, an unhandled exception that occurs during the execution of a task is deferred for later observation. For example, the deferred exception is automatically observed at a later time when you call one of the task class's wait methods. At that time, the exception is rethrown in the calling context of the wait method. This allows you to use the same exception handling approach in parallel programs that you use in sequential program

while in the section called Unobserved Task Executions part, there is an introduction on the use of UnobservedTaskException of the TaskScheduler static class. 

Here I will use one little example to show you how to use UnobservedTaskException. 

```
public void AsyncGetInstruments(Action<List<Instrument>> callback, Action<Exception> exceptionCallback = null)
        {
            var task = Task.Factory.StartNew(() => GetInstruments());
            if (callback != null)
            {
                task.ContinueWith(t => callback(t.Result), TaskContinuationOptions.OnlyOnRanToCompletion);
            }

            if (exceptionCallback != null)
            {
                EventHandler<UnobservedTaskExceptionEventArgs> exceptionHandler = null;
                exceptionHandler = (o, e) =>
                    {
                        TaskScheduler.UnobservedTaskException -= exceptionHandler;
                        if (!e.Observed)
                        {
                            exceptionCallback(e.Exception);
                            e.SetObserved();
                        }
                    };
                TaskScheduler.UnobservedTaskException += exceptionHandler;
            }
        }
```

## Custom Numeric Format Strings

vs the Custom Numeric Format Strings, there must be a Standard Numeric Format Strings.
what are the typical Standard Numeric Format Strings

* "C" or "c"
* "D" or "d"

while the Custom Numeric Format Strings has the followings.

* "0"
* "#"
* "."
* ","
* "E0"
* ";" this is the Section Separator.


References
[Custom Numeric Format Strings](http://msdn.microsoft.com/en-us/library/0c899ak8(v=vs.110).aspx)
[Standard Numeric Format Strings](http://msdn.microsoft.com/en-us/library/dwhawy9k(v=vs.110).aspx)

## Good use of truncate to create the "..." ellipses 

you can use the string.truncate method to create ellipses. such as if you have a label and due to space limitation, you want only the first (all) 30 characters at most and only the last "..." 


the problem is that the C# language itself does not have the truncate method. to fill what is missing. here is a home-made version.

```
        public static string Truncate(this string str, int length, string truncateMarker = null)
        {
            if (str.Length > length)
            {
                return str.Substring(0, length) + truncateMarker;
            }

            return str;
        }
```

or there is a more fancy linq version. 


```
        public static string Truncate(this string str, int length, string pad)
        {
            if (String.IsNullOrEmpty(str)) return str;

            return new string(str.Take(length).ToArray()) + pad;
        }
```
References
[c# - How do I truncate a .NET string? - Stack Overflow](http://stackoverflow.com/questions/2776673/how-do-i-truncate-a-net-string)


## ServiceLocator and Unity Container
the ServiceLocator class resides in the following namespace

the UnityContainer class reside in the following namespace.

the type definition of the ServiceLocatorProvider delegate is as follow.

```
namespace Microsoft.Practices.ServiceLocation { 
  public delegate IServiceLocator ServiceLocatorProvider();
}
```

the Use of the ServiceLocatorProvider is to provide an instance of the ServiceLocatorProvider; as manifested in the signature of the delegate.


the `UnityServiceLocator` from the Microsoft.Practices.Unity.UnityServiceLocator provides a implemenation of IServiceLocation with UnityContanier. so that you can use `UnityServiceLocator`  to fill the real implemenation of the ServiceLocator.

ServiceLocation actually implemented what is called the "Proxy" pattern, which it delegate the job to the real object underneath.

Check the `ServiceLocator.SetLocatorProvider(ServiceLocatorProvider newProvider)` methods.

Now that we have all the necessary information in-mind, we can bridge the the UnityContainerLocator and the ServiceLocator to the same platform.


First let's define a helper class that provide the basic service;
```
  public static class ConfigurableServiceLocator
  {
    [ThreadStatic]
    private static ServiceLocatorProvider _currentThreadProvider;
    private static bool _isThreadStatic;

    public static IServiceLocator Current
    {
      get
      {
        if (!ConfigurableServiceLocator._isThreadStatic)
          return ServiceLocator.Current;
        else
          return ConfigurableServiceLocator._currentThreadProvider() ?? ServiceLocator.Current;
      }
    }

    public static void SetLocatorProvider(ServiceLocatorProvider newProvider)
    {
      ServiceLocator.SetLocatorProvider(newProvider);
      if (!ConfigurableServiceLocator._isThreadStatic)
        return;
      ConfigurableServiceLocator._currentThreadProvider = newProvider;
    }

    public static void TurnOnThreadStaticMode()
    {
      ConfigurableServiceLocator._isThreadStatic = true;
    }
  }
```

then we create a extension method 
```
    public static void SetAsServiceLocator(this IUnityContainer container)
    {
      UnityServiceLocator unityServiceLocator = new UnityServiceLocator(container);
      ConfigurableServiceLocator.SetLocatorProvider((ServiceLocatorProvider) (() => (IServiceLocator) unityServiceLocator));
    }
```

Last we can use it as such 

```
            _container.SetAsServiceLocator();
```



## ServiceLocator and its relationship with the Activator

Where in the references page below, we can see the [A tutorial on Service locator pattern with implementation - CodeProject].

While, there is one class that is involved, that class is the Activator, the Activator does is to create instance of a specified type. 

you can check the definition of the class Activator from the following materials. [Activator Class (System)]


References:
[A tutorial on Service locator pattern with implementation - CodeProject]: http://www.codeproject.com/Articles/597787/A-tutorial-on-Service-locator-pattern-with-impleme
[A tutorial on Service locator pattern with implementation - CodeProject][A tutorial on Service locator pattern with implementation - CodeProject]

[Activator Class (System)]: http://msdn.microsoft.com/zh-cn/library/system.activator(v=vs.110).aspx
[Activator Class (System)][Activator Class (System)]


## a sample implementation of ServiceLocator
Here I will present you with a sample presentation of ServiceLocator. here is the code. 
```
    /// <summary>
    /// Test Util ServiceLocator - provide easy to access/use service locator
    /// </summary>
    public static class ServiceLocator
    {
        public static Dictionary<Type, object> _services = new  Dictionary<Type, object>();

        static Dictionary<Type, object> Services
        {
            get
            {
                return ServiceLocator._services;
            }
        }

        static ServiceLocator()
        {
        }

        public static void Add<T>(T service)
        {
            ServiceLocator.Services[typeof(T)] = (object)service;
        }

        public static T Resolve<T>()
        {
            object obj;
            if (ServiceLocator.Services.TryGetValue(typeof(T), out obj))
            {
                return (T)obj;
            }
            return default(T);
        }

        public static T Resolve<T, V>() where V : T
        {
            object obj;
            if (ServiceLocator.Services.TryGetValue(typeof(T), out obj))
            {
                return (T)obj;
            }
            else
            {
                ServiceLocator.Add((T)Activator.CreateInstance<V>()); // V provides the implemenmtation of K
                obj = ServiceLocator.Resolve<T>();
            }

            return (T)obj;
        }


        public static T Remove<T>()
        {
            object obj;
            if (ServiceLocator.Services.TryGetValue(typeof(T), out obj))
            {
                ServiceLocator.Services.Remove(typeof(T));
            }

            return (T)obj;
        }

    }

```



## nesting use of the lock as the using blocks

while you can do the following type of code 

```
using(new DisposableInstance1 = new DisposableClass1())
using(new DisposableInstance2 = new DisposableClass2())
using(new DisposableInstance3 = new DisposableClass3())
{
	// your code goes here.
}
```


Well you can do pretty much the same for the lock statement.s

Here is the live example on how you can do that.

```
lock (_orderIDToToastMap) lock (_rejOrderIDToToastMap) lock (_cancelledOrderIDToToastMap)
            {
                alertTokenList.AddRange(_orderIDToToastMap.Select(toast => toast.Value));

                alertTokenList.AddRange(_cancelledOrderIDToToastMap.Select(toast => toast.Value));

                alertTokenList.AddRange(_orderIDToToastMap.Select(toast => toast.Value));

                foreach (var alertToken in alertTokenList)
                {
                    Unregister(alertToken);
                }

                _toasterClient.CloseAll();

                _outstandingToastNumber = 0;
                _rejOrderIDToToastMap.Clear();
                _cancelledOrderIDToToastMap.Clear();
                _orderIDToToastMap.Clear();
            }

```



## Flexible use of theNullable and its operators

I have a code which uses the int? as the Value input. while there is a Incr/Decr method which is meant to decrease/increase its values.


here is the code that without use of the `??` operator.

```

if (Value.hasValue) {
	Value += Increment;
} else {
	Value = Increment;
}
```

Instead you can just do the following


```
Value = (Value ?? 0) + Increment;
```


and there is yet another method like belo.w

```
if (Value.HasValue && Value - 1 > 0)
{
	Value -= Increment;
}
```