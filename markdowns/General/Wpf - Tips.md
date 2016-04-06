1. there are more tips on the WPF programming model

## the SubmitTextBoxBehavior

sometimes that we want a text box to accept the enter button as submit the text content. There are some ways that we can do that..

the behavior code is as follow. 
```
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Input;
using System.Windows.Interactivity;

namespace Behaviors
{
    /// <summary>
    /// Make a text box to accept return as commit
    /// </summary>
    public class SubmitTextBoxBehaviour : Behavior<TextBox>
    {
        #region Behavior<TextBox>

        protected override void OnAttached()
        {
            base.OnAttached();
            AssociatedObject.PreviewKeyDown += HandlePreviewKeyDown;
        }

        protected override void OnDetaching()
        {
            base.OnDetaching();
            AssociatedObject.PreviewKeyDown -= HandlePreviewKeyDown;
        }

        #endregion


        #region Textbox handlers

        private void HandlePreviewKeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                BindingExpression be = AssociatedObject.GetBindingExpression(TextBox.TextProperty);
                if (be != null)
                {
                    be.UpdateSource();
                }
            }
        }
        #endregion
    }
}
    
```

and to use it, there are the following code in action. 


```
                    <TextBox 
                        Text="{Binding EditingLayoutName, UpdateSourceTrigger=LostFocus, NotifyOnSourceUpdated=True, ValidatesOnDataErrors=True}"
                        IsEnabled="{Binding EditingLayout.IsTemplate, Converter={StaticResource _invertBooleanConverter}}"
                        Grid.Row="0"
                        Grid.Column="1"
                        HorizontalContentAlignment="Left"
                        HorizontalAlignment="Stretch"
                        VerticalAlignment="Center"
                        VerticalContentAlignment="Center"
                        ext:LayoutExtension.RenameCommand="{Binding RenameSelectedLayoutCommand}"
                        ToolTip="{Binding EditingLayoutNameTooltip}">
                        <i:Interaction.Behaviors>
                            <behaviour:SubmitTextBoxBehaviour />
                        </i:Interaction.Behaviors>
                    </TextBox>
```


## Implement your own Autocomplete Combobox

first let's see an example of the code (the behavior code that turns a combobox to a source of autocomplete source) 


```
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Input;
using System.Windows.Interactivity;
using Services.StaticData;
using Views.FlexDepth;
using Extensions; // extension Extension namespace
using Threading; // extension Extension Threading 
using Common.Extensions; // extension Common.Extensions
using log4net;

namespace Behaviors
{
    /// <summary>
    /// Focus Behavior, control shall be focused if the IsFocus dependency property is true
    /// </summary>
    public class InstrumentComboBehavior : Behavior<ComboBox>
    {
        private static readonly ILog Log = LogManager.GetLogger(MethodBase.GetCurrentMethod().DeclaringType);

        public static readonly DependencyProperty IsFocusedProperty = 
            DependencyProperty.Register(
            "IsFocused", 
            typeof(bool), 
            typeof(InstrumentComboBehavior), 
            new PropertyMetadata(default(bool), IsFocusedChanged));

        public static readonly DependencyProperty HasInitialFocusProperty = 
            DependencyProperty.Register(
            "HasInitialFocus", 
            typeof(bool), 
            typeof(InstrumentComboBehavior), 
            new PropertyMetadata(default(bool)));

        public static readonly DependencyProperty MaxInstrumentInDropDownProperty =
            DependencyProperty.Register(
            "MaxInstrumentInDropDown",
            typeof(int),
            typeof(InstrumentComboBehavior),
            new PropertyMetadata(20));

        public static readonly DependencyProperty InstrumentServiceProperty =
            DependencyProperty.Register(
            "InstrumentService",
            typeof(InstrumentService),
            typeof(InstrumentComboBehavior),
            new PropertyMetadata(null));

        private readonly List<DelayTask> _delayTasks = new List<DelayTask>();
        private readonly Delegate _textChangeHandler;

        private CancellationTokenSource _searchCancellationToken;
        private IList<InstrumentVm> _instrumentSource;
        private TextBox _editableTextBox;

        public InstrumentComboBehavior()
        {
            _searchCancellationToken = new CancellationTokenSource();
            _textChangeHandler = new TextChangedEventHandler(ComboBox_TextChanged);
        }

        public bool HasInitialFocus
        {
            get
            {
                return (bool)GetValue(HasInitialFocusProperty);
            }
            set
            {
                SetValue(HasInitialFocusProperty, value);
            }
        }

        public bool IsFocused
        {
            get
            {
                return (bool)GetValue(IsFocusedProperty);
            }
            set
            {
                SetValue(IsFocusedProperty, value);
            }
        }

        public InstrumentService InstrumentService
        {
            get
            {
                return (InstrumentService)GetValue(InstrumentServiceProperty);
            }

            set
            {
                SetValue(InstrumentServiceProperty, value);
            } 
        }

        public int MaxInstrumentInDropDown
        {
            get
            {
                return (int)GetValue(MaxInstrumentInDropDownProperty);
            }
            set
            {
                SetValue(MaxInstrumentInDropDownProperty, value);
            }
        }

        protected override void OnAttached()
        {
            AssociatedObject.Loaded += AssociatedObjectLoaded;
            AssociatedObject.DropDownOpened += AssociatedObject_DropDownOpened;
            AssociatedObject.AddHandler(TextBoxBase.TextChangedEvent, _textChangeHandler);
            base.OnAttached();
        }

        protected override void OnDetaching()
        {
            AssociatedObject.DropDownOpened -= AssociatedObject_DropDownOpened;

            if (_textChangeHandler != null)
            {
                AssociatedObject.RemoveHandler(TextBoxBase.TextChangedEvent, _textChangeHandler);
            }

            base.OnDetaching();
        }

        private void AssociatedObject_DropDownOpened(object sender, EventArgs e)
        {
            var combo = (ComboBox)sender;

            // prevent the inner text box from highlighting all after drop down opened.
            if (_editableTextBox != null && combo.SelectedItem == null)
            {
                _editableTextBox.Select(_editableTextBox.Text.Length, 0);
            }
        }

        private void ComboBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            var combo = (ComboBox)sender;

            var viewModel = combo.DataContext as DepthViewerViewModel;

            if (viewModel != null && !viewModel.IsInstrumentComboValid)
            {
                viewModel.IsInstrumentComboValid = true;
            }

            if (combo.SelectedItem == null)
            {
                var newCallCancellation = new CancellationTokenSource();
                Interlocked.Exchange(ref _searchCancellationToken, newCallCancellation).Cancel();

                new DelayTask(TimeSpan.FromMilliseconds(300), _delayTasks)
                     .Task.ContinueWith(
                         t => SearchInstrument(combo, combo.Text),
                         _searchCancellationToken.Token,
                         TaskContinuationOptions.OnlyOnRanToCompletion,
                         UITaskSchedulerService.Instance.GetUITaskScheduler())
                     .LogTaskExceptionIfAny(Log);
            }
        }

        private void SearchInstrument(ComboBox combo, string key)
        {
            if (string.IsNullOrEmpty(key))
            {
                combo.ItemsSource = _instrumentSource.Take(MaxInstrumentInDropDown);
            }
            else
            {
                combo.ItemsSource = _instrumentSource.Where(r => r.Alias.ToLower().Contains(key.ToLower())).OrderBy(r=>r.Alias)
                    .Concat(_instrumentSource.Where(r=>r.InstrDisplay.ToLower().Contains(key.ToLower())).OrderBy(r=>r.Alias))
                    .Distinct()
                    .Take(MaxInstrumentInDropDown);
            }
            
            combo.IsDropDownOpen = true;
        }


        private void AssociatedObjectLoaded(object sender, RoutedEventArgs e)
        {
            AssociatedObject.Loaded -= AssociatedObjectLoaded;

            _editableTextBox = AssociatedObject.FindChild<TextBox>("PART_EditableTextBox");

            if (_editableTextBox != null)
            {
                _editableTextBox.MinWidth = 100;
            }

            _instrumentSource = new List<InstrumentVm>();
            
            if (InstrumentService != null)
            {
                InstrumentService.SearchInstruments("").ForEach(i => _instrumentSource.Add(GetInstrumentVm(i)));
            }

            AssociatedObject.ItemsSource = _instrumentSource.Take(MaxInstrumentInDropDown);
            if (HasInitialFocus || IsFocused)
            {
                GotFocus();
            }
        }

        private InstrumentVm GetInstrumentVm(Instrument inst)
        {
            return new InstrumentVm
                {
                    Alias = inst.Alias,
                    InstrDisplay = string.Format("{0, -12}\t {1,-30}", inst.Alias, inst.Description),
                };
        }

        private static void IsFocusedChanged(DependencyObject sender, DependencyPropertyChangedEventArgs args)
        {
            if ((bool)args.NewValue)
            {
                ((InstrumentComboBehavior)sender).GotFocus();
            }
            else
            {
                ((InstrumentComboBehavior)sender).ClearFocus();
            }
        }

        private void GotFocus()
        {
            new DelayTask(TimeSpan.FromMilliseconds(300), _delayTasks).Task.ContinueWith(
              t => AssociatedObject.Focus(),
              CancellationToken.None,
              TaskContinuationOptions.OnlyOnRanToCompletion,
              UITaskSchedulerService.Instance.GetUITaskScheduler());
        }

        private void ClearFocus()
        {
            AssociatedObject.MoveFocus(new TraversalRequest(FocusNavigationDirection.Previous));
        }
    }
}

```

Basically what it does is to create an internal datasource (List&lt;InstrumentVm&gt;) and turn that dynamically hijack the TextBox ItemsSource.

There are some thing that worth noticing now. 

the default Combobox has issues that when you type first time, the text is highlighted. and this is due to some Internal problem that when the combobox 's drop down is opened. the Text is highlighted, we can fix that by the following code. 

```
        private void AssociatedObject_DropDownOpened(object sender, EventArgs e)
        {
            var combo = (ComboBox)sender;

            // prevent the inner text box from highlighting all after drop down opened.
            if (_editableTextBox != null && combo.SelectedItem == null)
            {
                _editableTextBox.Select(_editableTextBox.Text.Length, 0);
            }
        }
```

you may wonder where the control `_editableTextBox`is coming from:

```
        private void AssociatedObjectLoaded(object sender, RoutedEventArgs e)
        {
            AssociatedObject.Loaded -= AssociatedObjectLoaded;

            _editableTextBox = AssociatedObject.FindChild<TextBox>("PART_EditableTextBox");
            // ...
        }
```

with the help of theVIsualTreeExtension, you can have find parent/child. the utility code is as follow. 

```
public static T FindChild<T>(this DependencyObject parent, string childName) where T : DependencyObject
    {
      if (parent == null)
        return default (T);
      T obj = default (T);
      int childrenCount = VisualTreeHelper.GetChildrenCount(parent);
      for (int childIndex = 0; childIndex < childrenCount; ++childIndex)
      {
        DependencyObject child = VisualTreeHelper.GetChild(parent, childIndex);
        if ((object) (child as T) == null)
        {
          obj = VisualTreeExtensions.FindChild<T>(child, childName);
          if ((object) obj != null)
            break;
        }
        else if (!string.IsNullOrEmpty(childName))
        {
          FrameworkElement frameworkElement = child as FrameworkElement;
          if (frameworkElement != null && frameworkElement.Name == childName)
          {
            obj = (T) child;
            break;
          }
        }
        else
        {
          obj = (T) child;
          break;
        }
      }
      return obj;
    }
```


there are also some problems with width (the ComboBox's TextBox control has MinWidth issue), which can be resolved by the following hack.

```
        private void AssociatedObjectLoaded(object sender, RoutedEventArgs e)
        {
            _editableTextBox = AssociatedObject.FindChild<TextBox>("PART_EditableTextBox");

            if (_editableTextBox != null)
            {
                _editableTextBox.MinWidth = 100;
            }
            // ...
		}
```

the xaml file for the combobox is as follow. 


```
				<ComboBox
					x:Name="cmbx"
					Grid.Row="1" 
					Grid.Column="0"
					Style="{DynamicResource AutoCompleteComboBox}" 
					Margin="4"
					Text="{Binding SearchTxt, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}"
					SelectedValue="{Binding SearchTxt}"
					SelectedValuePath="Alias"
					DisplayMemberPath="InstrDisplay"  
					TextSearch.TextPath="Alias"
					IsTextSearchEnabled="False"
					IsEditable="True"
					ToolTip="{Binding InstrumentInputErrorMessage, ValidatesOnDataErrors=True, NotifyOnValidationError=True}"
					>
					<ComboBox.Resources>
						<SolidColorBrush x:Key="{x:Static SystemColors.WindowBrushKey}" Color="LightGray" />
					</ComboBox.Resources>
          <i:Interaction.Behaviors>
            <behaviors:InstrumentComboBehavior
							InstrumentService="{Binding InstrumentService}"
              IsFocused="{Binding DisplayInstrumentSelection, Mode=OneWay}" />
          </i:Interaction.Behaviors>
				</ComboBox>
```

## string.Contains vs. string.Empty

it is an interesting question, what is the response when you try to test contains with string.Empty.

Given that if a string str = "hello", what is the expected result if  you try to run 

```
str.Contains("");
```

it is True. so that you can leverage this for some advanced (Null State object), here is an example. 

```
        private void SearchInstrument(ComboBox combo, string key)
        {
            if (string.IsNullOrEmpty(key))
            {
                combo.ItemsSource = _instrumentSource.Take(MaxInstrumentInDropDown);
            }
            else
            {
                combo.ItemsSource = _instrumentSource.Where(r => r.Alias.ToLower().Contains(key.ToLower())).OrderBy(r=>r.Alias)
                    .Concat(_instrumentSource.Where(r=>r.InstrDisplay.ToLower().Contains(key.ToLower())).OrderBy(r=>r.Alias))
                    .Distinct()
                    .Take(MaxInstrumentInDropDown);
            }
            
            combo.IsDropDownOpen = true;
        }
```

so that if you try todo 

```
SearchInstrument("").Take(MaxInstrumentInDropDown)
```

then you will be able to take/filter out of the full sources. 


## Base knowledge - DependencyProperty 

This post is excerpted from one open blog "[Dependency Property][Dependency_Property]"


in that post, the following has been covered:

1. DependencyObject
1.1. Part 1: The class
1.2. Part 2: Declaring the Property
1.3 Part 3: Instantiation
1.4. Wrapping the DP
2. LocalValue vs. Effective Value
3. FrameworkPropertyMetaData
4. ValidateValueCallback

I will skip most of the part which has someting to do with the background introduction, here are the code that can introduce most of the use/idiosynchrosy/quiks of the DependncyProperty. 

Here is the code that we use to demon the use of a Car class.

```
public class Car : DependencyObject
    {
        #region Dependency Properties
 
        public static readonly DependencyProperty SpeedProperty;
 
        public static readonly DependencyProperty MinSpeedProperty;
 
        public static readonly DependencyProperty MaxSpeedProperty;
 
        #endregion
 
 
        #region Dependency Properties Wrappers
 
        /// <summary>
        /// Wrapper for the Speed dependency property
        /// </summary>
        public int Speed
        {
            get { return (int)GetValue(SpeedProperty); }
            set { SetValue(SpeedProperty, value); }
        }
 
        /// <summary>
        /// Wrapper for the MinSpeed dependency property
        /// </summary>
        public int MinSpeed
        {
            get { return (int)GetValue(MinSpeedProperty); }
            set { SetValue(MinSpeedProperty, value); }
        }
 
        /// <summary>
        /// Wrapper for the MaxSpeed dependency property
        /// </summary>
        public int MaxSpeed
        {
            get { return (int)GetValue(MaxSpeedProperty); }
            set { SetValue(MaxSpeedProperty, value); }
        }
 
        #endregion
 
        /// <summary>
        /// Static constructor where all dependecy properties are being initialized
        /// </summary>
        static Car()
        {
            Trace.WriteLine("Static Constructor");
            //configure and register speed property
            FrameworkPropertyMetadata speedMetadata = new FrameworkPropertyMetadata(0, null, CoerceSpeed);
            SpeedProperty = DependencyProperty.Register("Speed", typeof (int), typeof (Car), speedMetadata,
                                                        ValidateSpeed);
 
            //configure and register min speed property
            FrameworkPropertyMetadata minMetadata = new FrameworkPropertyMetadata(0, OnMinSpeedChanged);
            MinSpeedProperty = DependencyProperty.Register("MinSpeed", typeof (int), typeof (Car), minMetadata,
                                                           ValidateSpeed);
 
            //configure and register max speed property
            FrameworkPropertyMetadata maxMetadata = new FrameworkPropertyMetadata(1,OnMaxSpeedChanged, CoerceMaxSpeed);
            MaxSpeedProperty = DependencyProperty.Register("MaxSpeed", typeof (int), typeof (Car), maxMetadata,
                                                           ValidateSpeed);
        }
 
        #region Validate methods
 
        public static bool ValidateSpeed(object value)
        {
            Trace.WriteLine("ValidateSpeed");
            int speed = (int)value;
            return speed >= 0;
        }
 
        #endregion
 
        #region Coerce methods
 
        /// <summary>
        /// method for adjusting the speed according to the min and max
        /// </summary>
        /// <param name="d"></param>
        /// <param name="baseValue"></param>
        /// <returns></returns>
        public static object CoerceSpeed(DependencyObject d, object baseValue)
        {
            Trace.WriteLine("CoerceSpeed");
            Car car = (Car)d;
            int speed = (int)baseValue;
            //the speed can't be lower than the min speed
            speed = Math.Max(car.MinSpeed, speed);
            //the speed can't be greater than the max speed
            speed = Math.Min(car.MaxSpeed, speed);
            return speed;
        }
 
        /// <summary>
        /// method for adjusting the max speed according to me min speed.
        /// </summary>
        /// <param name="d"></param>
        /// <param name="baseValue"></param>
        /// <returns></returns>
        public static object CoerceMaxSpeed(DependencyObject d, object baseValue)
        {
            Trace.WriteLine("CoerceMaxSpeed");
            Car car = (Car)d;
            int maxSpeed = (int) baseValue;
            //the max speed can't be lower than the main speed
            return Math.Max(car.MinSpeed, maxSpeed);
        }
 
        #endregion
 
        #region Property changed methods
 
        /// <summary>
        /// this method is fired when the MaxSpeedProperty is changed
        /// </summary>
        /// <param name="d"></param>
        /// <param name="e"></param>
        private static void OnMaxSpeedChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            Trace.WriteLine("OnMaxSpeedChanged");
            Car car = (Car)d;
            car.CoerceValue(SpeedProperty);
        }
 
        /// <summary>
        /// this method is fired when the MinSpeedProperty is changed
        /// </summary>
        /// <param name="d"></param>
        /// <param name="e"></param>
        private static void OnMinSpeedChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            Trace.WriteLine("OnMinSpeedChanged");
            Car car = (Car)d;
            //coerce the max speed to ajdust to the new min speed
            car.CoerceValue(MaxSpeedProperty);
            //coerce the speed to adjust to the new min speed
            car.CoerceValue(SpeedProperty);
        }
 
        #endregion
 
    }
```

and below is the code that drive the use of it 


```
Car car = new Car();
Trace.WriteLine(string.Format("Speed:{0} Min:{1} Max:{2}",car.Speed,car.MinSpeed,car.MaxSpeed));
Trace.WriteLine(string.Format("Speed LocalValue:{0} EffectiveValue:{1}", car.ReadLocalValue(Car.SpeedProperty),
                car.GetValue(Car.SpeedProperty)));
car.Speed = 60;
Trace.WriteLine(string.Format("Speed: {0} Min:{1} Max:{2}",car.Speed,car.MinSpeed,car.MaxSpeed));
Trace.WriteLine(string.Format("Speed LocalValue:{0} EffectiveValue:{1}", car.ReadLocalValue(Car.SpeedProperty),
                car.GetValue(Car.SpeedProperty))); 
car.MinSpeed = 40;
Trace.WriteLine(string.Format("Speed: {0} Min:{1} Max:{2}",car.Speed,car.MinSpeed,car.MaxSpeed));
Trace.WriteLine(string.Format("Speed LocalValue:{0} EffectiveValue:{1}", car.ReadLocalValue(Car.SpeedProperty),
                car.GetValue(Car.SpeedProperty))); 
car.MaxSpeed = 80;
Trace.WriteLine(string.Format("Speed: {0} Min:{1} Max:{2}",car.Speed,car.MinSpeed,car.MaxSpeed));
Trace.WriteLine(string.Format("Speed LocalValue:{0} EffectiveValue:{1}", car.ReadLocalValue(Car.SpeedProperty),
                car.GetValue(Car.SpeedProperty)));
```

References:
[Dependency_Property]: http://perezgb.com/2009/09/24/dependency-properties
[Dependency Property][Dependency_Property]


## TextBoxBehavior.ClearTextOnEscape
once you click on the escape, you should be escape the text by clear its contents. 

This can be avchieved by the Attached property by the use of OnKeyUp event handlers.

```
    /// <summary>
    /// TextBox Behavior
    /// </summary>
    public class TextBoxBehavior
    {
        #region AttachedProperty : ClearTextOnEscape

        public static DependencyProperty ClearTextOnEscapeProperty =
            DependencyProperty.RegisterAttached(
                "ClearTextOnEscape",
                typeof(bool),
                typeof(TextBoxBehavior),
                new UIPropertyMetadata(ClearTextOnEscapeChanged));


        /// <summary>
        /// Gets the value of the ClearTextOnEscape attached property for a given <see cref="FrameworkElement"/>.
        /// </summary>
        /// <param name="element">The framework element from which to read the property value.</param>
        /// <returns>The value of the SelectAllOnFocus attached property.</returns>
        public static bool GetClearTextOnEscape(TextBox element)
        {
            return (bool)element.GetValue(ClearTextOnEscapeProperty);
        }

        /// <summary>
        /// Sets the value of the ClearTextOnEscape attached property for a given <see cref="FrameworkElement"/>.
        /// </summary>
        /// <param name="element">The element on which to set the attached property.</param>
        /// <param name="value">The value that will be set to SelectAllOnFocus attached property</param>
        public static void SetClearTextOnEscape(TextBox element, bool value)
        {
            element.SetValue(ClearTextOnEscapeProperty, value);
        }

        /// <summary>
        /// Registered property change callback method for ClearTextOnEscape
        /// </summary>
        /// <param name="d">The object that has experienced a change in value.</param>
        /// <param name="e">The event arguments for this change.</param>
        private static void ClearTextOnEscapeChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var textBox = (TextBox)d;
            var newValue = (bool)e.NewValue;
            var oldValue = (bool)e.OldValue;
            if ((newValue == true) && (oldValue == false))
            {
                textBox.KeyUp += TextBoxOnKeyUp;
            }
            else if ((newValue == false) && (oldValue == true))
            {
                textBox.KeyUp -= TextBoxOnKeyUp;
            }
        }

        private static void TextBoxOnKeyUp(object sender, KeyEventArgs keyEventArgs)
        {
            var textBox = sender as TextBox;
            if (null != textBox && keyEventArgs.Key == Key.Escape)
            {
                var value = GetClearTextOnEscape(textBox);
                if (value)
                {
                    textBox.Dispatcher.BeginInvoke(new Action(() => textBox.Text = string.Empty));
                }
            }
        }
        #endregion
    }
```

and the test harness code is as follow. 

```
<Window x:Class="TextBoxBehaviorLib.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
				xmlns:behavior="clr-namespace:TextBoxBehaviorLib"
        Title="MainWindow" Height="350" Width="525">
    <Grid>
        <TextBox
					behavior:TextBoxBehavior.ClearTextOnEscape="True"
				></TextBox>
    </Grid>
</Window>
```


## Border Trigger get called for every value changed. 

we have  a Converter, which convert based on the business rle. here is the code.
```
    public class DepthRowBorderConverter : IMultiValueConverter
    {
        private static readonly Brush _organizationDataGridBorderBrush = (Brush)Application.Current.FindResource("YourDataGridBorderBrush");

        /// <summary>
        /// Convert inputs to Border brush for Depth Row.
        /// </summary>
        /// <param name="values">Inputs values. Expecting two ints, values[0] is depth level of the particular row. values[1] is the configured levels of the Depth Viewer ViewModel.</param>
        /// <param name="targetType">Convert targe type</param>
        /// <param name="parameter">conversion parameter</param>
        /// <param name="culture">Convert cultures info</param>
        /// <returns>YourDataGridBorderBrush if it is a border row, otherwise, Brushes.Transparent</returns>
        public object Convert(object[] values, Type targetType, object parameter, CultureInfo culture)
        {
            if (values.Length != 2 || !(values[0] is int) || !(values[1] is int))
            {
                return Brushes.Transparent;
            }

            try
            {
                var level = (int)values[0];
                var depthLevels = (int)values[1];

                if (level == 0 || depthLevels -1 == level)
                {
                    return _organizationDataGridBorderBrush;
                }
            }
            catch (Exception)
            {
               // do nothing
            }

            return Brushes.Transparent;
        }

        public object[] ConvertBack(object value, Type[] targetTypes, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
```

and here is the xaml file. 

```
		<Style x:Key="RowStyle" TargetType="{x:Type dxg:RowControl}">
			<Setter Property="Foreground" Value="{DynamicResource ForegroundBrush}"/>
			<Setter Property="BorderBrush">
				<Setter.Value>
				<MultiBinding Converter="{StaticResource DepthRowBorderConverter}">
						<Binding Path="DataContext.Level" Mode="OneWay" />
						<Binding ElementName="depthGrid" Path="DataContext.DepthLevels" Mode="OneWay" />
				</MultiBinding>
				</Setter.Value>
			</Setter>
		</Style>
```


however, it was found that the converter get called everytime the data value changes. 

So I changed to the DataTrigger, however, it still not working. 

```
			<Setter Property="BorderBrush" Value="Transparent" />

				<DataTrigger Value="True">
					<DataTrigger.Binding>
						<MultiBinding Converter="{StaticResource DepthRowIsBorderRowConverter}">
							<Binding Path="DataContext.Level" Mode="OneWay" />
							<Binding ElementName="depthGrid" Path="DataContext.DepthLevels" Mode="OneWay" />
					</MultiBinding>
					</DataTrigger.Binding>
					<Setter Property="BorderBrush" Value="{DynamicResource YourDataGridBorderBrush}" />
				</DataTrigger>
```


and the new converter code is as follow. 

```
    public class DepthRowIsBorderRowConverter : IMultiValueConverter
    {
        public object Convert(object[] values, Type targetType, object parameter, CultureInfo culture)
        {
             if (values.Length != 2 || !(values[0] is int) || !(values[1] is int))
             {
                 return false;
             }

            try
            {
                var level = (int)values[0];
                var depthLevels = (int)values[1];

                if (level == 0 || depthLevels -1 == level)
                {
                    return true;
                }
            }
            catch (Exception)
            {
               // do nothing
            }

            return false;
        }

        public object[] ConvertBack(object value, Type[] targetTypes, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
```

## Attached Behaviors MVVM


http://nnish.com/2012/04/22/attached-behaviors-mvvm/


## IsKeyboardFocusWithin

this can tell if the keyboard is currently focused within the control.

## Binding.DoNothing and the DependencyProperty.UnsetValue

In Summary the Binding.DoNothing means that it instructs the binding engine to not update the value of the target property at all. 
DependendencyProperty.UnsetValue is not a instruction , but simply a null value that can be interpreted by the WPF binding engine as the value of absent values.  

Here is an good example which I took from the  reference page called "Preventing a binding from Updating too frequently"

FIrst i will show you the xaml contents.

```
<Window x:Class="BindingDoNothing.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
				xmlns:local="clr-namespace:BindingDoNothing"
        Title="MainWindow" Height="350" Width="525">
				<Window.DataContext>
					<local:RandomNumberEngine />
				</Window.DataContext>
    <Grid>
        <Grid.Resources>
					<local:UpdateThresholdConverter x:Key="thresholdConv" UpdateThreshold="1000" />
				</Grid.Resources>

				<!-- 
				replace the following to disable the thresholdConv 
				
					Text="{Binding Path=Current}"
				
				-->

				<TextBlock
					HorizontalAlignment="Center"
					Text="{Binding Path=Current, Converter={StaticResource thresholdConv}}"
					VerticalAlignment="Center"
				></TextBlock>
    </Grid>
</Window>
```

Below is Converter. 

```
    /// <summary>
    /// Update Threshold converter
    /// </summary>
    public class UpdateThresholdConverter : IValueConverter
    {
        private int _updateThreshold;

        private DateTime _lastUpdate = DateTime.MinValue;

        public int UpdateThreshold
        {
            get
            {
                return _updateThreshold;
            }

            set
            {
                if (value < 0)
                {
                    throw new ArgumentOutOfRangeException("UpdateThreshold", value, "Cannot be less than zero.");
                }
                _updateThreshold = value;
            }
        }

        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            DateTime now = DateTime.Now;
            TimeSpan elapsed = now - _lastUpdate;
            bool canUpdate = this.UpdateThreshold <= elapsed.TotalMilliseconds;
            if (canUpdate)
            {
                _lastUpdate = now;
                return value;
            }

            // you can change to DependencyProperty.UnsetValue to see what is the difference
            return Binding.DoNothing;
            //return DependencyProperty.UnsetValue;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            // there is no support for applying a threshold for updating the datasource 
            return value;
        }
    }
```

and last but not the least, the RandomNumberEngine. here is the code. 

```
    /// <summary>
    /// Random Number ENgine
    /// </summary>
    public class RandomNumberEngine : INotifyPropertyChanged
    {
        public RandomNumberEngine()
        {
            DispatcherTimer timer = new DispatcherTimer(DispatcherPriority.Normal);
            timer.Tick += (o, e) => OnPropertyChanged("Current");
            timer.Interval = TimeSpan.FromMilliseconds(100);
            timer.Start();
        }

        public int Current
        {
            get
            {
                var nextCursor = NextCursor;
                if (nextCursor == 0)
                {
                    for (int i = 0; i < _maxbuckets; i++)
                    {
                        _buckets[i] = _random.Next(100);
                    }
                }

                return _buckets[nextCursor];
            }
        }

        internal int NextCursor
        {
            get
            {
                return ++_cursor % _maxbuckets;
            }
        }


        private readonly Random _random  = new Random();
        private int _cursor = -1;

        private const int _maxbuckets = 50;
        private int[] _buckets = new int[_maxbuckets];

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(propertyName));
            }
        }
    }
```


-- 
introduction 

--

this page will introduce you the information on how to use the Binding.DoNothing and/or DependencyProperty.UnsetValue to indicate some not-so-common return values. 

--


References

Prevent a binding from updating too frequently: http://joshsmithonwpf.wordpress.com/2007/08/20/prevent-a-binding-from-updating-too-frequently/
What are the special values of WPF's binding engine when converting values?: http://stackoverflow.com/questions/10384599/what-are-the-special-values-of-wpfs-binding-engine-when-converting-values


## Data binding Path 

How to notify itself, how to notify this[]?

First let's check the how to notify self.


References:
[Binding.Path Property (System.Windows.Data)](http://msdn.microsoft.com/en-us/library/system.windows.data.binding.path.aspx)
[data binding - WPF Bind to itself - Stack Overflow](http://stackoverflow.com/questions/1906587/wpf-bind-to-itself)

## alias self/this

it is a good idea to alias self/this , so given an example 

```
public class GridRow : NotificationObject
{
	public GridRow RowObject 
	{ 
	   get { 
	         return this;
	   }
   }
}
```

then you can do binding to itself with the following. 

```
{Binding RowObject}
```


## ICollectionView.Refresh

This is usually used when you have done a batch set of view model changes and then you want to apply (resync) the viewmodel changes back to the Views altogether. 


## TextBox.CharacterCasing
TextBox.CharacterCasing property exists both in the System.Windows.Forms and the System.Windows.Controls.

That shall be controlled by the enum called CharacterCasing.. It has three values. 

```
1. Lower
2. Normal
3. Upper

```


This can help you transfer casing for an input to the TextBox automaticlaly sometimes. (but be careful when it is not working properly, when the TextBox is part of a container element which initialize it later)

## Wires up ComboBox's TextChanged event
The ComboBox does not inherits from the TextBox directly or indirectly, but from its visual tree that it has a visual sub-component called PART_EditBox.

Though the ComboBox does not have the TextChanged event, but since the RoutedEvent can be propagated up from its child element, in this case, it is the inner text box that can bubble up the textchanged event. then you can try to hook an handler to its top leve. 

So if you are writing in the xaml file, you can do the following. 
```
<ComboBox IsEditable="True" TextBoxBase.TextChanged="ComboBox_TextChanged" x:Name="_comboBox" />
```

while if you are working from the code behind, you can do the following.

```
AssociatedObject.AddHandler(TextBox.TextChangedEvent,  _textChangedHandler);
```

e.g.

in my MainWindow.xaml file we have this: 

```
    <Grid>
        <Grid.RowDefinitions>
					<RowDefinition />
				</Grid.RowDefinitions>

				<ComboBox
					x:Name="_Combobox"
					Grid.Row="0"
					IsEditable="True"
					IsReadOnly="False"
					IsTextSearchEnabled="True"
					IsTextSearchCaseSensitive="False"
				></ComboBox>
    </Grid>
```

and then from the code behind, we have this: 

```
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            _Combobox.AddHandler(TextBoxBase.TextChangedEvent, new TextChangedEventHandler(_textChangedEventHandler));
        }

        private void _textChangedEventHandler(object sender, TextChangedEventArgs e)
        {
            Debug.WriteLine(string.Format("_Text has changed within the ComboBox, the changed elements includes {0}",  string.Join(",", e.Changes)));
        }
    }
```

You can watch the result from the debugger console.

References
[wpf - How do I get TextChanged events from an editable ComboBox - Stack Overflow](http://stackoverflow.com/questions/6914942/how-do-i-get-textchanged-events-from-an-editable-combobox)
[How to listen to the editable combobox value changed](https://social.msdn.microsoft.com/Forums/en-US/a895fc43-9e0b-45ae-bc29-1e48a600dfc1/how-to-listen-to-the-editable-combobox-value-changed?forum=wpf)

## ScrollIntoView
there are a bunch of controls that offers the ScrollIntoView method. the method can be used to scroll to the necessary elements .

while the overload of the method "ScrollIntoView" is available from [DataGrid.ScrollIntoView Method (System.Windows.Controls)](http://msdn.microsoft.com/en-us/library/system.windows.controls.datagrid.scrollintoview(v=vs.110).aspx).

Let's review one of the Behavior which scroll to the new item and focus it when necessary.

An example to show you how that is accomplished .

```
 private void ItemSource_CollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
        {
            if (AssociatedObject.IsLoaded && e.Action == NotifyCollectionChangedAction.Add)
            {
                // AssociatedObject.LoadingRow += AssociatedObject_LoadingRow;
                AssociatedObject.ScrollIntoView(e.NewItems[0]);
                DelayedHandler(() =>
                {
                    var cell = GetBeginEditingCell(AssociatedObject, BeginEditColumnIndex);

                    if (cell != null && cell.IsVisible)
                    {
                        var combo = GetVisualChild<ComboBox>(cell);
                        if (combo != null && combo.IsVisible)
                        {
                            combo.Focus();
                        }
                    }
                });
            }
        }
```

References:
[DataGrid.ScrollIntoView Method (System.Windows.Controls)](http://msdn.microsoft.com/en-us/library/system.windows.controls.datagrid.scrollintoview(v=vs.110).aspx)
[wpf - Make ListView.ScrollIntoView Scroll the Item into the Center of the ListView (C#) - Stack Overflow](http://stackoverflow.com/questions/2946954/make-listview-scrollintoview-scroll-the-item-into-the-center-of-the-listview-c)

## DataGrid.ColumnWidth

what is the difference of the DataGrid.ColumnWidth and the Width property of each DataGridColumn?

The official site has this: 
[DataGrid.ColumnWidth Property (System.Windows.Controls)](http://msdn.microsoft.com/en-us/library/system.windows.controls.datagrid.columnwidth(v=vs.110).aspx)

the difference is that the ColumnWidth is at the DataGrid level which has the global visibility, while the each DataGridColumn's Width property take precedence over this value.

References:
[DataGrid.ColumnWidth Property (System.Windows.Controls)](http://msdn.microsoft.com/en-us/library/system.windows.controls.datagrid.columnwidth(v=vs.110).aspx)


## Difference between WPF DataGrid's EnableRowVirtualization and VirtualizingStackPanel.IsVirtualizing properties

this is an excerpt of the SO post on the same topic., the reference to the topic is as follow.

the original questions is about, the difference of the two

```
VirtualizingStackPanel.IsVirtualizing="True" 
```

and 

```
EnableRowVirtualization="True"/EnableColumnVirtualization="True". 
```

and the proposed answer is as follow.

> Both IsVirtualizing and EnableRowVirtualization/EnableColumnVirtualization operate on the same principle, which is that items are visualized only when needed and the containers are reused.

>Essentially, the Panel (or Grid) keeps track of what is visible and if this is changed, it uses an internal class, 'ItemContainerGenerator', to size and build new items (http://msdn.microsoft.com/en-us/library/system.windows.controls.itemcontainergenerator.aspx).

>The motivation for both is that the containers are only generated on demand thus saving memory and improving performance.

>As to why there are two: the Panel is designed to extend in a single direction only, either horizontal or vertical; so they implemented a single attached property for it. A Grid, on the other hand, extends in two dimensions, so they implemented a property for each dimension.

>The other difference is academic:  IsVirtualizing is an attached property, wherease its counterparts for the Grid are native properties. No clue as to why they opted for this difference...

>Relevant links are http://msdn.microsoft.com/en-us/library/system.windows.controls.datagrid.enablerowvirtualization(v=vs.100).aspx and http://msdn.microsoft.com/en-us/library/system.windows.controls.virtualizingstackpanel.isvirtualizing.aspx

References:
[c# - Difference between WPF DataGrid's EnableRowVirtualization and VirtualizingStackPanel.IsVirtualizing properties - Stack Overflow](http://stackoverflow.com/questions/18976856/difference-between-wpf-datagrids-enablerowvirtualization-and-virtualizingstackp)

## BufferedObservableCollection

BufferedObservableCollection, a performance experiments to better performances.

```
    public class BufferedObservableCollection<T> : ObservableCollection<T>
    {
        #region Fields 
        private NotifyCollectionChangedAction? _lastAction = null;
        private List<T> _itemBuffer = new List<T>();
        private List<NotifyCollectionChangedEventArgs> _cachedCollectionEventArgs = new List<NotifyCollectionChangedEventArgs>();
        #endregion

        #region Constructor(s)
        public BufferedObservableCollection()
        {
            base.CollectionChanged += new NotifyCollectionChangedEventHandler(ObservableCollectionUpdate_CollectionChanged);
        }
        #endregion

        #region Events
        // new event
        public override event NotifyCollectionChangedEventHandler CollectionChanged;
        #endregion

        #region Protected Properties
        protected bool UpdateDisabled { get; private set; }
        #endregion

        #region Public Methods
        /// <summary>
        ///  Begin Updates
        /// </summary>
        /// <Remarks>
        /// <para>BeginUpdate should be called on the UI thread.</para>
        /// </Remarks>
        public void BeginUpdate()
        {
            if (UpdateDisabled)
            {
                return;
            }

            UpdateDisabled = true;
        }

        /// <summary>
        ///  Begin Updates
        /// </summary>
        /// <Remarks>
        /// <para>EndUpdate should be called on the UI thread.</para>
        /// </Remarks>
        public void EndUpdate()
        {
            if (UpdateDisabled)
            {
                foreach (var cachedArgs in _cachedCollectionEventArgs)
                {
                    RaiseCollectionChanged(this, cachedArgs);
                }

                _cachedCollectionEventArgs.Clear();
                Flush(false);
                UpdateDisabled = false;
            }
        }

        /*
        public void Flush()
        {
            if (_lastAction.HasValue && (_itemBuffer.Count > 0))
            {
                RaiseCollectionChanged(this, new NotifyCollectionChangedEventArgs(_lastAction.Value, _itemBuffer));
                _itemBuffer.Clear();
                _lastAction = null;
            }
        }
        */

        #endregion

        #region Protected
        protected void RaiseCollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
        {
            if (this.CollectionChanged != null)
                CollectionChanged(sender, e);
        }
        #endregion

        #region Private Helpers
        public void FlushToCache()
        {
            Flush(true);
        }
        #endregion

        #region Handlers
        private void ObservableCollectionUpdate_CollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
        {
            if (UpdateDisabled)
            {
                switch (e.Action)
                {
                    case NotifyCollectionChangedAction.Move:
                    case NotifyCollectionChangedAction.Replace:
                    case NotifyCollectionChangedAction.Reset:
                        FlushToCache();
                        _cachedCollectionEventArgs.Add(e);
                        break;
                    default:
                        // if we have a last action, check if it is changed and should be flush else only change the lastaction
                        if (_lastAction.HasValue)
                        {
                            if (_lastAction != e.Action)
                            {
                                //Flush();
                                FlushToCache();
                                _lastAction = e.Action;
                            }
                        }
                        else
                            _lastAction = e.Action;
                        if (e.Action == NotifyCollectionChangedAction.Add)
                        {
                            _itemBuffer.AddRange(e.NewItems.Cast<T>());
                        }
                        else if (e.Action == NotifyCollectionChangedAction.Remove)
                        {
                            _itemBuffer.AddRange(e.OldItems.Cast<T>());
                        }
                        break;
                }
            }
            else
            {
                RaiseCollectionChanged(this, e);
            }
        }

        private void Flush(bool toCache)
        {
            if (_lastAction.HasValue && _itemBuffer.Count > 0)
            {
                if (toCache)
                {
                    _cachedCollectionEventArgs.Add(new NotifyCollectionChangedEventArgs(_lastAction.Value, _itemBuffer));
                }
                else
                {
                    RaiseCollectionChanged(this, new NotifyCollectionChangedEventArgs(_lastAction.Value, _itemBuffer));
                }

                _itemBuffer.Clear();
                _lastAction = null;
            }
        }
        #endregion
    }
```


References:
[Increasing WPF ObservableCollection performance - Stack Overflow](http://stackoverflow.com/questions/1398519/increasing-wpf-observablecollection-performance)


## KeyboardNavigation Class
Due to some occasion, I happen to know that there is a possible solution to navigation without programmaticlaly set focus/unset focus on certain elements. while, you can delegate the Keyboard (focus) navigation to the Control itself. 


the key to the clean/snappy solution is the [KeyboardNavigation Class (System.Windows.Input)]. 

the solution does override one of the Dependencies properties of the Class - [KeyboardNavigation.TabNavigationProperty Field (System.Windows.Input)]

here is the code 

```
KeyboardNavigation.TabNavigationProperty.OverrideMetadata(typeof(ColorPickerControl), new FrameworkPropertyMetadata(KeyboardNavigationMode.Local));
```

then depends on the input key(which you can control, you can do something as below)

```
            var elementWithFocus = Keyboard.FocusedElement as UIElement;

            var focusDirection = FocusNavigationDirection.Next;
            switch (input)
            {
                case KeyType.Tab:
                    focusDirection = FocusNavigationDirection.Next;
                    break;
                case KeyType.Down:
                    focusDirection = FocusNavigationDirection.Down;
                    break;
                case KeyType.Up:
                    focusDirection = FocusNavigationDirection.Up;
                    break;
                case KeyType.Left:
                    focusDirection = FocusNavigationDirection.Left;
                    break;
                case KeyType.Right:
                    focusDirection = FocusNavigationDirection.Right;
                    break;
            }

            var request = new TraversalRequest(focusDirection);
            // Change keyboard focus. 
            if (elementWithFocus != null)
            {
                elementWithFocus.MoveFocus(request);
            }

```

References
[KeyboardNavigation Class (System.Windows.Input)]: http://msdn.microsoft.com/en-us/library/system.windows.input.keyboardnavigation(v=vs.110).aspx
[KeyboardNavigation Class (System.Windows.Input)][KeyboardNavigation Class (System.Windows.Input)]
[KeyboardNavigation.TabNavigationProperty Field (System.Windows.Input)]: http://msdn.microsoft.com/en-us/library/system.windows.input.keyboardnavigation.tabnavigationproperty(v=vs.110).aspx
[KeyboardNavigation.TabNavigationProperty Field (System.Windows.Input)][KeyboardNavigation.TabNavigationProperty Field (System.Windows.Input)]

## FocusNavigation

the Focus navigation is done through the use of the [FrameworkElement.MoveFocus Method (System.Windows)]

this method has a [FocusNavigationDirection][FocusNavigationDirection Enumeration (System.Windows.Input)].

it has the following values

* Down
* First
* Last
* Left
* Next
* Previous
* Right 
* Up

the usage of the MoveFocus can be found below.

```
        private void SetNextFocusedItem(KeyType input)
        {
            if (!IsColorsDropDownOpen)
                return;
            // Gets the element with keyboard focus.
            var elementWithFocus = Keyboard.FocusedElement as UIElement;
            var colorLabel = elementWithFocus as Label;
            if (colorLabel == null)
            {
                var validButton = elementWithFocus as Button;
                if (validButton == null || !IsColorPickerButtons(validButton.Name))
                {
                    //Set Default Button as focused UIElement
                    if (_defaultButton != null)
                    {
                        Keyboard.Focus(_defaultButton);
                        elementWithFocus = Keyboard.FocusedElement as UIElement;
                    }
                }
            }

            // MoveFocus takes a TraveralReqest as its argument.
            var focusDirection = FocusNavigationDirection.Next;
            switch (input)
            {
                case KeyType.Tab:
                    focusDirection = FocusNavigationDirection.Next;
                    break;
                case KeyType.Down:
                    focusDirection = FocusNavigationDirection.Down;
                    break;
                case KeyType.Up:
                    focusDirection = FocusNavigationDirection.Up;
                    break;
                case KeyType.Left:
                    focusDirection = FocusNavigationDirection.Left;
                    break;
                case KeyType.Right:
                    focusDirection = FocusNavigationDirection.Right;
                    break;
            }

            var request = new TraversalRequest(focusDirection);
            // Change keyboard focus. 
            if (elementWithFocus != null)
            {
                elementWithFocus.MoveFocus(request);
            }
        }
```
One requirement for your element to participate in the focus navigation is that it shoud have 

* Focusable = true
* IsTabstop = true (may not be necesssary)

References
[FrameworkElement.MoveFocus Method (System.Windows)]: http://msdn.microsoft.com/en-us/library/system.windows.frameworkelement.movefocus(v=vs.110).aspx
[FrameworkElement.MoveFocus Method (System.Windows)][FrameworkElement.MoveFocus Method (System.Windows)]
[FocusNavigationDirection Enumeration (System.Windows.Input)]: http://msdn.microsoft.com/en-us/library/system.windows.input.focusnavigationdirection(v=vs.110).aspx
[FocusNavigationDirection Enumeration (System.Windows.Input)][FocusNavigationDirection Enumeration (System.Windows.Input)]

## Custom Focus Visual

Inspired by the posts in the references tabs. You can design your resusable focus style. the key is to 

1. create a style that Draw some focused visual 
2. Set the property "FocusVisualStyle" to the element that you want to change 

the example is:

1. creat the focus visual style
```
    <Style x:Key="CustomFocusVisual">
        <Setter Property="Control.Template">
            <Setter.Value>
                <ControlTemplate>
                    <Rectangle StrokeThickness="1" Stroke="#FFDDDDDD" SnapsToDevicePixels="true"/>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
```

and then 
2. apply the "FocusVisualStyle" on the element that you want to change.
```
    <Style TargetType="Label" x:Key="ColorStyle">
        <Setter Property="IsTabStop" Value="True"></Setter>
        <Setter Property="Focusable" Value="True"></Setter>
        <Setter Property="FocusVisualStyle" Value="{StaticResource CustomFocusVisual}"></Setter>
        <Setter Property="ContentTemplate">
            <Setter.Value>
                <DataTemplate>
                    <Rectangle Width="10" Height="10" Focusable="False"
                     VerticalAlignment="Center" HorizontalAlignment="Center"
                     Fill="{Binding Path=Color, Converter={StaticResource ColorToBrushConverter}}" />
                </DataTemplate>
            </Setter.Value>
        </Setter>
        <Style.Triggers>
            <Trigger Property="IsMouseOver" Value="true"> 
                <Setter Property="BorderThickness" Value="1"/>
                <Setter Property="Padding" Value="1"/>
                <Setter Property="BorderBrush" Value="#FFDDDDDD"/>
                <Setter Property="Background" Value="Transparent"/>
            </Trigger>
            <DataTrigger Value="true">
                <!-- ... -->
            </DataTrigger>
        </Style.Triggers>
    </Style>
```


References
[c# - Reusable way to put a bright red box around whatever element currently has focus? - Stack Overflow]:http://stackoverflow.com/questions/10771504/reusable-way-to-put-a-bright-red-box-around-whatever-element-currently-has-focus
[c# - Reusable way to put a bright red box around whatever element currently has focus? - Stack Overflow][c# - Reusable way to put a bright red box around whatever element currently has focus? - Stack Overflow]
[Styling for Focus in Controls, and FocusVisualStyle]:http://msdn.microsoft.com/en-us/library/bb613567.aspx:
[Styling for Focus in Controls, and FocusVisualStyle][Styling for Focus in Controls, and FocusVisualStyle]


## dual focus style @Mouse & @Focus
It is possible to set show Focus style (appearance) for the element at mouse and the element at with focus.

the key is 
1. FocusVisualStyle for the focused element
2. Trigger IsMouseOver property 

I will illustrate the idea with code shown above. 

1. FocusVisualStyle
```
    <Style x:Key="CustomFocusVisual">
        <Setter Property="Control.Template">
            <Setter.Value>
                <ControlTemplate>
                    <Rectangle StrokeThickness="1" Stroke="#FFDDDDDD" SnapsToDevicePixels="true"/>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
```

then 
```
    <Style TargetType="Label" x:Key="ColorStyle">
        <Setter Property="IsTabStop" Value="True"></Setter>
        <Setter Property="Focusable" Value="True"></Setter>
        <Setter Property="FocusVisualStyle" Value="{StaticResource CustomFocusVisual}"></Setter>
        ...
```

2. IsMouseOver Trigger

```
    <Style TargetType="Label" x:Key="ColorStyle">
        <Style.Triggers>
            <Trigger Property="IsMouseOver" Value="true"> 
                <Setter Property="BorderThickness" Value="1"/>
                <Setter Property="Padding" Value="1"/>
                <Setter Property="BorderBrush" Value="#FFDDDDDD"/>
                <Setter Property="Background" Value="Transparent"/>
            </Trigger>
        ...
```

## Keyboard focus - yet explicit way to move focus 
As we have discussed before that you can set focus with the KeyboardNavigation class, you can as well just call 
[Keyboard.Focus Method (System.Windows.Input)](http://msdn.microsoft.com/en-us/library/system.windows.input.keyboard.focus(v=vs.110).aspx).

the [Keyboard.Focus][Keyboard.Focus Method (System.Windows.Input)] method can be useful when you want to jump focus to an arbitrary control/framework elements.

I will show you an live example that leverage both the KeyboardNavigation as well as the Keyboard.Focus method.

```
        protected override void OnMouseMove(MouseEventArgs e)
        {
            base.OnMouseMove(e);
            if (!IsColorsDropDownOpen)
                return;
            var element = Mouse.DirectlyOver as FrameworkElement;
            if (element == null) return;

            var colorInfo = element.DataContext as IColorInfo;
            var actionButton = element as Button;
            if (colorInfo == null && actionButton == null) return;
            if (element is Border)
            {
                var parentLabel = VisualTreeHelper.GetParent(element) as Label;
                if (parentLabel != null)
                {
                    parentLabel.Focusable = true;
                    parentLabel.Focus();
                    Keyboard.Focus(parentLabel);
                }
                else
                {
                    element.Focusable = true;
                    element.Focus();
                    Keyboard.Focus(element);
                }
            }
        }
```

then the Keyboard handlers

```
        protected override void OnKeyDown(KeyEventArgs e)
        {
            base.OnKeyDown(e);
            if (e.Handled)
            {
                return;
            }
            bool handled;
            Key key = e.Key;
            switch (key)
            {
                case Key.Escape:
                    handled = true;
                    if (IsColorsDropDownOpen)
                        IsColorsDropDownOpen = false;
                    break;
                case Key.Enter:
                    handled = true;
                    OnEnterKeyDown();
                    break;
                case Key.Down:
                    handled = true;
                    SetNextFocusedItem(KeyType.Down);
                    break;
                case Key.Up:
                    handled = true;
                    SetNextFocusedItem(KeyType.Up);
                    break;
                case Key.Right:
                    handled = true;
                    SetNextFocusedItem(KeyType.Right);
                    break;
                case Key.Left:
                    handled = true;
                    SetNextFocusedItem(KeyType.Left);
                    break;
                case Key.Tab:
                    handled = true;
                    SetNextFocusedItem(KeyType.Tab);
                    break;
                default:
                    handled = false;
                    break;
            }

            if (handled)
            {
                e.Handled = true;
            }

        }

        private void OnEnterKeyDown()
        {
            if (!IsColorsDropDownOpen)
                IsColorsDropDownOpen = true;
            else
            {
                var elementWithFocus = Keyboard.FocusedElement as UIElement;

                var focusedButon = elementWithFocus as Button;
                if (focusedButon != null)
                {
                    focusedButon.Command.Execute(null);
                }
                else
                {
                    var item = elementWithFocus as Label;
                    if (item != null)
                    {
                        var colorInfo = item.DataContext as IColorInfo;
                        if (colorInfo == null)
                        {
                            IsColorsDropDownOpen = false;
                            return;
                        }
                        SelectedColorInfo = colorInfo;
                    }
                }
                IsColorsDropDownOpen = false;
            }
        }

        private void SetNextFocusedItem(KeyType input)
        {
            if (!IsColorsDropDownOpen)
                return;
            // Gets the element with keyboard focus.
            var elementWithFocus = Keyboard.FocusedElement as UIElement;
            var colorLabel = elementWithFocus as Label;
            if (colorLabel == null)
            {
                var validButton = elementWithFocus as Button;
                if (validButton == null || !IsColorPickerButtons(validButton.Name))
                {
                    //Set Default Button as focused UIElement
                    if (_defaultButton != null)
                    {
                        Keyboard.Focus(_defaultButton);
                        elementWithFocus = Keyboard.FocusedElement as UIElement;
                    }
                }
            }

            // MoveFocus takes a TraveralReqest as its argument.
            var focusDirection = FocusNavigationDirection.Next;
            switch (input)
            {
                case KeyType.Tab:
                    focusDirection = FocusNavigationDirection.Next;
                    break;
                case KeyType.Down:
                    focusDirection = FocusNavigationDirection.Down;
                    break;
                case KeyType.Up:
                    focusDirection = FocusNavigationDirection.Up;
                    break;
                case KeyType.Left:
                    focusDirection = FocusNavigationDirection.Left;
                    break;
                case KeyType.Right:
                    focusDirection = FocusNavigationDirection.Right;
                    break;
            }

            var request = new TraversalRequest(focusDirection);
            // Change keyboard focus. 
            if (elementWithFocus != null)
            {
                elementWithFocus.MoveFocus(request);
            }
        }
        private bool IsColorPickerButtons(string buttonName)
        {
            return string.Equals(buttonName, PART_DefaultButton, StringComparison.Ordinal) ||
                   string.Equals(buttonName, PART_MoreColorsButton, StringComparison.Ordinal) ||
                   string.Equals(buttonName, PART_TransparentButton, StringComparison.Ordinal);
        }
```

References
[Keyboard.Focus Method (System.Windows.Input)]:http://msdn.microsoft.com/en-us/library/system.windows.input.keyboard.focus(v=vs.110).aspx.
[Keyboard.Focus Method (System.Windows.Input)][Keyboard.Focus Method (System.Windows.Input)]


## Mouse.DirectlyOver

This can give you an element that the Mouse is directly over...

References:
[Mouse.DirectlyOver Property (System.Windows.Input)](http://msdn.microsoft.com/en-us/library/system.windows.input.mouse.directlyover(v=vs.110).aspx)

## UIElement.InputHitTest Method vs. VisualTreeHelper.HitTest

as according to the [Hit Testing in the Visual Layer], 

> The UIElement class provides the InputHitTest method, which allows you to hit test against an element using a given coordinate value. In many cases, the InputHitTest method provides the desired functionality for implementing hit testing of elements. However, there are several scenarios in which you may need to implement hit testing at the visual layer.

why we use the VisualTreeHelper.HitTest?
That is because 
1. test against UIElement (UIElement is parent of FrameworkElement, but there are Visual DispatcherObject, DependencyObject which are not decendant of UIElement)
2. VisualTreeHelper can do Hit test using a geometry (rather just a point)
3. Hit test against multiple object (not just the Topmost Z-Order)
4. can have policy.

References
[Hit Testing in the Visual Layer]:http://msdn.microsoft.com/en-us/library/ms752097(v=vs.110).aspx
[Hit Testing in the Visual Layer][Hit Testing in the Visual Layer]
[UIElement.InputHitTest Method (System.Windows)]:http://msdn.microsoft.com/en-us/library/system.windows.uielement.inputhittest(v=vs.110).aspx
[UIElement.InputHitTest Method (System.Windows)][UIElement.InputHitTest Method (System.Windows)]

## Commonly used MouseOperations utils class

```
    public class MouseOperations
    {
        [Flags]
        public enum MouseEventFlags
        {
            LeftDown = 0x00000002,
            LeftUp = 0x00000004,
            MiddleDown = 0x00000020,
            MiddleUp = 0x00000040,
            Move = 0x00000001,
            Absolute = 0x00008000,
            RightDown = 0x00000008,
            RightUp = 0x00000010
        }

        [DllImport("user32.dll", EntryPoint = "SetCursorPos")]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool SetCursorPos(int X, int Y);

        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool GetCursorPos(out MousePoint lpMousePoint);

        [DllImport("user32.dll")]
        private static extern void mouse_event(int dwFlags, int dx, int dy, int dwData, int dwExtraInfo);

        public static void SetCursorPosition(int X, int Y)
        {
            SetCursorPos(X, Y);
        }

        public static void SetCursorPosition(MousePoint point)
        {
            SetCursorPos(point.X, point.Y);
        }

        public static MousePoint GetCursorPosition()
        {
            MousePoint currentMousePoint;
            var gotPoint = GetCursorPos(out currentMousePoint);
            if (!gotPoint) { currentMousePoint = new MousePoint(0, 0); }
            return currentMousePoint;
        }

        public static void MouseEvent(MouseEventFlags value)
        {
            MousePoint position = GetCursorPosition();

            mouse_event
                ((int)value,
                 position.X,
                 position.Y,
                 0,
                 0)
                ;
        }

        [StructLayout(LayoutKind.Sequential)]
        public struct MousePoint
        {
            public int X;
            public int Y;

            public MousePoint(int x, int y)
            {
                X = x;
                Y = y;
            }

        }
  }
```

## FallbackValue and TragetNullValue

there are two values that you can uses in the Xaml binding files. 

one is the FallbackValue. 

> This is used when a binding cannot determine a value at all, based on the the data source and the path. Or in other words, FallbackValue is used when the property bound to the source is not at all available. In that case, the value supplied for FallbackValue will be considered at the target end

another is the TargetNullValue.

> As the name suggests, when a source object's property is null, the TargetNullValue is the alternate value you want to set for the target. So, whatever value is set for TargetNullValue will be set for the target. Pretty simple, isn't it ?

[FallbackValue in WPF](http://www.c-sharpcorner.com/UploadFile/41e70f/fallbackvalue-in-wpf/)


## WPF NotifyPropertyChanged with string.Empty arguments

as you already be aware that if you pass the string.Empty as the arguent to the PropertyChangedEventArgs. then you will notify the views that all the properties of the Obejct ViewModel can be changed.

this is convenient for writing code. however, according to one of my test, I found that it is somewhat conter-intuitive regarding the performance.

It was used to have this
```
        public void RaisePropertiesChanges()
        {
            RaisePropertyChanged("BidTrend");
            RaisePropertyChanged("BidPrice");
            RaisePropertyChanged("BidPriceDisplay");
            RaisePropertyChanged("BYieldDisplay");
            RaisePropertyChanged("BYield");
            RaisePropertyChanged("AskTrend");
            RaisePropertyChanged("AYield");
            RaisePropertyChanged("AYieldDisplay");
            RaisePropertyChanged("AskPrice");
            RaisePropertyChanged("AskPriceDisplay");

...
            RaisePropertyChanged("LastTrdPrice");
            RaisePropertyChanged("LastTrdQty");
            RaisePropertyChanged("LastTrdBS");
            RaisePropertyChanged("LastTrdTime");
            RaisePropertyChanged("LastInfo");
        }
```


now if I changed that to the following. 

```
        public void RaiseAllPropertiesChanged()
        {
            RaisePropertyChanged(string.Empty);
        }
```

I guess that would cut down the CPU usage, on the contrary, the values of that CPU usages does go up massively. 

as I can tell from the Task manager, I can see that the RaisePropertyChanged with the string.Empty has the problems the CPU usages is actually higher.

I would guess that means that given very high frequency of the data is coming. 

I can see from my 4 cores machines with 8 GB bytes memories, that the enumerations parts has even better performances... 

References
[INotifyPropertyChanged.PropertyChanged 事件 (System.ComponentModel)](http://msdn.microsoft.com/zh-cn/library/system.componentmodel.inotifypropertychanged.propertychanged(v=vs.110).aspx)


## ScrollIntoView sometimes not working
the ScrollIntoView some times does not work, it was because when using the MVVM pattern, when the data is added to the Items source and when the Generator generates container that actually holds the newly added/modified object. 

We know for the Items controls, it has the ItemContainerGenerator, the ItemContainerGenerator creates a container to hold contents for each item. 

The ItemContainerGenerator has a Status, which you can query to get the Status of the ItemContainerGenerator.

Given an example , suppose that your application want to scroll to the last rows when new item is added, you may probably want to do the following. 

```
void ItemContainerGenerator_StatusChanged(object sender, EventArgs e)
{
    if(listView.ItemContainerGenerator.Status ==
GeneratorStatus.ContainersGenerated)
    {
        var info = listView.Items[listView.Items.Count - 1] as FileInfo;
        if (info == null)
            return;

        listView.ScrollIntoView(info);
    }
}
```

If you are scrolling to already existed items, you may not require to do the above. 


```
dataGridView.ScrollIntoView(DataGrid1.Items[DataGrid1.Items.Count - 1];
dataGridView.UpdateLayout();
dataGridView.ScrollIntoView(DataGrid1.Items[itemindex]);
```

the trick above is first scroll to the bottom most row and then scroll back to what row index that you want. the UpdateLayout() call in-between asking the WPF system to handle the messages in-between.

References
[The DotNet Experience: WPF ListView – ScrollIntoView](http://dotnet-experience.blogspot.com.es/2010/12/wpf-listview-scrollintoview.html)
[wpf(C#) DataGrid ScrollIntoView - how to scroll to the first row that is not shown? - Stack Overflow](http://stackoverflow.com/questions/9667475/wpfc-datagrid-scrollintoview-how-to-scroll-to-the-first-row-that-is-not-sho)

## Custom Color picker based on an image.

first of all, we need to get a Color from a bitmap, you can leverage the following code snippet to aid that.

```
        public static Color GetColor(this BitmapSource bitmapSource, double x, double y)
        {
            if (bitmapSource == null) throw new ArgumentNullException("bitmapSource");

            var croppedImage = new CroppedBitmap(bitmapSource, new Int32Rect((int)Math.Round(x), (int)Math.Round(y), 1, 1));
            var colorBytes = new byte[4];
            croppedImage.CopyPixels(colorBytes, 4, 0);
            var color = Color.FromArgb(colorBytes[3], colorBytes[2], colorBytes[1], colorBytes[0]);
            return color;
        }
```
basically it creates a Cropped Image to do the color mapping.

because we have to supports

1. when click somewhere, (the pointer) update will also update the RGB values. 
2. when users types value inside the RGB text box, the canvas should search to find the most close color on canvas.

in the style file, the template declaration has something like this 

```
    <Style TargetType="{x:Type local:CustomColorPicker}">
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="{x:Type local:CustomColorPicker}">
                    <Border  ...>
                        <StackPanel Orientation="Vertical" ..>
                        <Grid>
                            ...
                            <Border Grid.Column="0" ...>
                                            <Grid VerticalAlignment="Stretch" HorizontalAlignment="Stretch">
                                            <Canvas x:Name="PART_CustomColorPickerCanvas" VerticalAlignment="Stretch" HorizontalAlignment="Stretch" Width="150" Height="150" Background="Transparent">
                                                <Image Stretch="None" Height="150" Width="150" Source="Images/customColorPickerImage.png" HorizontalAlignment="Left" local:CustomColorPicker.IsColorPickerImage="{Binding RelativeSource={RelativeSource Mode=TemplatedParent}}"/>
                                                    <Grid Height="15" Width="15" local:CustomColorPicker.IsColorPointer="{Binding RelativeSource={RelativeSource Mode=TemplatedParent}}">
                                                        <!-- cross hair with by drawing lines -->
                                                    </Grid>
                                                </Canvas>
                                            </Grid>
                           
                    </Border>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
    </Style>
```

well, if you click somewhere in the canvas, it does the "udpatePointer"

```
            Action<double, double> updatePointer = (x, y) =>
                {
                    Canvas.SetLeft(element, x - (element.ActualWidth/2.0));
                    Canvas.SetTop(element, y - (element.ActualHeight/2.0));
                    updatingPointer = false;
                };
```

and if you types in some values for RGB.. It does the "searchUpdatePointer"

```
            var redPropertyDescriptor = DependencyPropertyDescriptor.FromProperty(RedProperty, colorPicker.GetType());
            redPropertyDescriptor.AddValueChanged(colorPicker, (s, e) =>
            {
                if (updatingPointer) return;
                updatingPointer = true;
                element.Dispatcher.BeginInvoke(searchUpdatePointer, null);
            });
```


search does is to search through the Bitmap and find color with absolute differences on colors no greater than ...

## ListView to hide the Header.

How to hide the header of the listview, this is common when you want to show some ItemsControl data, but do not bother with the Headers things. 
Also, the other benefit offered by the ListView is that you can gain the feature of alignment built in in the ListView. 

the key to the hide the header is to use the HeaderContainer style to set the Visibility to Collapsed. here is the style definition.

```
	<Style TargetType="{x:Type GridViewColumnHeader}" x:Key="LiquidityHeaderContainerStyle">
		<Setter Property="Visibility" Value="Collapsed" />
	</Style>
```

## To drive vertical or horizontal lines in the listView

you can try to draw vertical or horizontal lines in the ListView to simulate something like the GridContorl in DevExpress or DataGrid in plain WPF.

To draw the Horizontal lines, you can overrride the ItemContainerStyle to draw an additional border when the Container for each element is generated.
the code snippet is shown as follow.


```
<ListView ...>
    <ListView.ItemContainerStyle>
        <Style TargetType="{x:Type ListViewItem}">
            <Setter Property="BorderBrush" Value="white" />            /// or listview color
            <Setter Property="BorderThickness" Value="0,0,0,0" />
        </Style>
    </ListView.ItemContainerStyle>
    <ListView.View>
        <GridView>
            <GridViewColumn ... />
        </GridView>
    </ListView.View>
```

However, to draw thevertical lines, it is a bit more complicated, but still possible to do. 

One of the non-intrusive way is to override the ArrangeOverride..   the code 

```
 protected override Size ArrangeOverride(Size arrangeSize)
    {
        var size = base.ArrangeOverride(arrangeSize);
        var children = Children.ToList();
        EnsureLines(children.Count);
        for (var i = 0; i < _lines.Count; i++)
        {
            var child = children[i];
            var x = child.TransformToAncestor(this).Transform(new Point(child.ActualWidth, 0)).X + child.Margin.Right;
            var rect = new Rect(x, -Margin.Top, 1, size.Height + Margin.Top + Margin.Bottom);
            var line = _lines[i];
            line.Measure(rect.Size);
            line.Arrange(rect);
        }
        return size;
    }
```

and to use it you can do the following. 

```
 <ListView.ItemContainerStyle>
            <Style TargetType="{x:Type ListViewItem}">
                <Setter Property="Margin" Value="2,0,0,0"/>
                <Setter Property="Padding" Value="0,2"/>
                <Setter Property="BorderBrush" Value="LightGray"/>
                <Setter Property="BorderThickness" Value="0,0,0,1"/>
                <Setter Property="HorizontalContentAlignment" Value="Stretch"/>
                <Setter Property="Template">
                    <Setter.Value>
                        <ControlTemplate TargetType="{x:Type ListViewItem}">
                            <Border BorderBrush="{TemplateBinding BorderBrush}" 
                                    BorderThickness="{TemplateBinding BorderThickness}" 
                                    Background="{TemplateBinding Background}">
                                <GridLines:GridViewRowPresenterWithGridLines 
                                    Columns="{TemplateBinding GridView.ColumnCollection}"
                                    Margin="{TemplateBinding Padding}" />
                            </Border>
                        </ControlTemplate>
                    </Setter.Value>
                </Setter>
                <Style.Triggers>
                    <Trigger Property="IsSelected" Value="True">
                        <Setter Property="Background" Value="{DynamicResource {x:Static SystemColors.ControlDarkBrushKey}}"/>
                    </Trigger>
                    <Trigger Property="IsEnabled" Value="False">
                        <Setter Property="Background" Value="{DynamicResource {x:Static SystemColors.ControlBrushKey}}"/>
                    </Trigger>
                </Style.Triggers>
            </Style>
        </ListView.ItemContainerStyle>
```

But I choose to implement in a slightly different way.

I especially create an grid line column template, like below. 

```
	<DataTemplate x:Key="LiquiditySeparatorCellTemplate">
		<Border
				Grid.Column="0"
				BorderThickness="1"
				Width="1"
				Height="28"
				BorderBrush="{DynamicResource DefaultBorderBrush}"/>
	</DataTemplate>
```

then from the ListView, you can add the extra border line as  you wish.

```
				<ListView
					Grid.Column="1"
					ItemsSource="{Binding FillUpdates}"
					ScrollViewer.VerticalScrollBarVisibility="Disabled"
					ScrollViewer.HorizontalScrollBarVisibility="Disabled">
					<ListView.View>
						<GridView ColumnHeaderContainerStyle="{StaticResource LiquidityHeaderContainerStyle}">
							<GridViewColumn CellTemplate="{StaticResource LiquiditySizeCellTemplate}" Width="64"/>
							<GridViewColumn CellTemplate="{StaticResource LiquiditySeparatorCellTemplate}"/>
							<GridViewColumn CellTemplate="{StaticResource LiquidityCounterPartyCellTemplate}" Width="Auto" />
							<GridViewColumn CellTemplate="{StaticResource LiquiditySeparatorCellTemplate}"/>
							<GridViewColumn CellTemplate="{StaticResource LiquidityMarketCellTemplate}" Width="80"/>
						</GridView>
					</ListView.View>
				</ListView>
```

references:
[Listview Horizontal vertical line visibitly WPF - Stack Overflow](http://stackoverflow.com/questions/17671417/listview-horizontal-vertical-line-visibitly-wpf)
[.net - Grid lines in WPF ListView - Stack Overflow](http://stackoverflow.com/questions/3138628/grid-lines-in-wpf-listview)


## Application.DoEvents() to solve an wierd UI race issue 
I recently encountered a very strange phenomenon that one Grid has wrong total summary belt when it is restored from some persisted state after the IsVisible is set to true.  While the same UI is fine if it is initially loaded and restored and bring into visible again. 

thus I kinda of suspect that this is due to the fact that the Visible is not processed before the restoration happens.  and thus I inserted the famouse Application.DoEvents() after the Visible=True and the code that does actually restore the code. 

things worked.

and that helped to verify that the theory:

"the ViewModel changes are not processed immediately and it won't show the affect until the UI message has been processed by the message loop. And if certain code that depends on the UI State (such as a UI element is literally visible - no 'visible' by the property 'Visible' is true) then there might exist certain race condtion"


To resolve the race condition, we have to first instruct the UI to process the messages.  To enable us to do that , we can rely on the Application.DoEvents().


```
using System.Windows.Threading;

namespace PushFrameDemo1.Threadings
{
    /// <summary>
    /// Refers to the Dispathcer.PushFrame method : http://msdn.microsoft.com/zh-cn/library/system.windows.threading.dispatcher.pushframe(v=vs.110).aspx
    /// </summary>
    public class Threading
    {
        public DispatcherOperationCallback FrameAction { get; set; }

        public void DoEvents()
        {
            DispatcherFrame frame = new DispatcherFrame();
            // this can simuate that we create some action that will be executed on a nexted loop
            // as according to [DispatcherFramer Class]: http://msdn.microsoft.com/zh-cn/library/system.windows.threading.dispatcherframe(v=vs.110).aspx
            // Dispatcher Frame represent "an execution loop in the Dispatcher".
            Dispatcher.CurrentDispatcher.BeginInvoke(
                //DispatcherPriority.Background, new DispatcherOperationCallback(ExitFrame), frame);
                DispatcherPriority.Background, new DispatcherOperationCallback(FrameAction), frame);
            Dispatcher.PushFrame(frame);
        }

        public object ExitFrame(object f)
        {
            // Exit from the Dispatcher frame indicated by the f
            ((DispatcherFrame)f).Continue = false;
            return null;
        }
    }
```



## Different types of Template
There are different type of template, to enumerate. they are 

1. ItemsTemplate
2. ControlTemplate
3. DataTemplate


## Control the height of the ListViewItem's height
you can control the height of the ListViewItem's height by using of hte ItemContainerStyle.

here is the code, you can first define a style like below.

```
	<Style x:Key="LiquidityItemContainerStyle" TargetType="{x:Type ListViewItem}">
		<Setter Property="Height" Value="26" />
	</Style>
```

and then from the ListView.

```

				<ListView
					Grid.Column="1"
					ItemsSource="{Binding FillUpdates}"
					ItemContainerStyle="{StaticResource LiquidityItemContainerStyle}">
					<ListView.View>
						<GridView ColumnHeaderContainerStyle="{StaticResource LiquidityHeaderContainerStyle}">
							<!-- ... -->
						</GridView>
					</ListView.View>
				</ListView>
```


## prefer to use VirtualizingStackPanel to StackPanel whenever possible
if you had a choice, prefer to use the VirtualizingStackPanel instead of plain StackPanel 

```
	<ItemsPanelTemplate x:Key="MarketItemsPanelTemplate">
		<VirtualizingStackPanel 
			Orientation="Horizontal"
			VerticalAlignment="Center"
			HorizontalAlignment="Right" 
			IsItemsHost="True"/>
	</ItemsPanelTemplate>
```


## Error "Can only base a style with target type tha tis base type 'IFrameworkInputElement"

I got an exception which has 

```
System.Windows.Markup.XamlParseException occurred
  HResult=-2146233087
  Message='Set property 'System.Windows.FrameworkElement.Style' threw an exception.' Line number '104' and line position '6'.
  Source=PresentationFramework
  LineNumber=104
  LinePosition=6
  StackTrace:
       at System.Windows.Markup.WpfXamlLoader.Load(XamlReader xamlReader, IXamlObjectWriterFactory writerFactory, Boolean skipJournaledProperties, Object rootObject, XamlObjectWriterSettings settings, Uri baseUri)
       at System.Windows.Markup.WpfXamlLoader.LoadBaml(XamlReader xamlReader, Boolean skipJournaledProperties, Object rootObject, XamlAccessLevel accessLevel, Uri baseUri)
       at System.Windows.Markup.XamlReader.LoadBaml(Stream stream, ParserContext parserContext, Object parent, Boolean closeStream)
       at System.Windows.Application.LoadComponent(Object component, Uri resourceLocator)
       at 
       ...
  InnerException: System.InvalidOperationException
       HResult=-2146233079
       Message=Can only base on a Style with target type that is base type 'IFrameworkInputElement'.
       Source=PresentationFramework
       StackTrace:
            at System.Windows.Style.Seal()
            at System.Windows.StyleHelper.UpdateStyleCache(FrameworkElement fe, FrameworkContentElement fce, Style oldStyle, Style newStyle, Style& styleCache)
            at System.Windows.FrameworkElement.OnStyleChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
            at System.Windows.DependencyObject.OnPropertyChanged(DependencyPropertyChangedEventArgs e)
            at System.Windows.FrameworkElement.OnPropertyChanged(DependencyPropertyChangedEventArgs e)
            at System.Windows.DependencyObject.NotifyPropertyChange(DependencyPropertyChangedEventArgs args)
            at System.Windows.DependencyObject.UpdateEffectiveValue(EntryIndex entryIndex, DependencyProperty dp, PropertyMetadata metadata, EffectiveValueEntry oldEntry, EffectiveValueEntry& newEntry, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType)
            at System.Windows.DependencyObject.SetValueCommon(DependencyProperty dp, Object value, PropertyMetadata metadata, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType, Boolean isInternal)
            at System.Windows.DependencyObject.SetValue(DependencyProperty dp, Object value)
            at System.Windows.Baml2006.WpfKnownMemberInvoker.SetValue(Object instance, Object value)
            at MS.Internal.Xaml.Runtime.ClrObjectRuntime.SetValue(XamlMember member, Object obj, Object value)
            at MS.Internal.Xaml.Runtime.ClrObjectRuntime.SetValue(Object inst, XamlMember property, Object value)
       InnerException: 
```

the reason is that I forget to add the "TargetType property when defining an style.

```
<Style x:Key="LiquidityListViewStyle" BasedOn="{StaticResource YourListViewStyle}"></Style>
```
Now that can be fixed by the following.

```
<Style x:Key="LiquidityListViewStyle" TargetType="{x:Type ListView}" BasedOn="{StaticResource YourListViewStyle}"></Style>
```


## ListView internal Presenters

when the ListView is a normal view (without the GridView), then the content presenter is just a normal content presenter, such as 

```
            <ContentPresenter VerticalAlignment="{TemplateBinding VerticalContentAlignment}"/>
```

while if the View is a GridView, then it should be the `GridViewRowPresenter`

```
        		<GridViewRowPresenter VerticalAlignment="{TemplateBinding VerticalContentAlignment}"/>
```


## ContentPresenter and ContentControl's special treating to the DataContext property

as you know that there is the ContentPresenter and the ContentControl which can be serves as the placeholder to hold other contents.


It is often used within another Usercontrol or template to render elements.

you might be attempted to set the DataContext of the presenter, and hope that will affect how it handles bindings for other properties such as "tooltip' or the "Visibility".

However, this is not workable.

see the following example.

```
			 <ContentPresenter
						DataContext="{Binding RelativeSource={RelativeSource Mode=FindAncestor, AncestorType=UserControl}, Path=DataContext}"
						ContentTemplate="{StaticResource ManyMarketLabelIndicator}"
						ToolTip="{Binding MarketIndicatorTooltip}"
						Visibility="{Binding ShowAllMarketsIndicators, Converter={StaticResource InvertedBooleanToVisibilityConverter}}"
						/> 
```

it turns out that the ToolTip and Visibility is still not getting bind to the parent (UserControl)'s Datacontext. To me, it is like that the DataContext is passed on the real content the ContentPresenter is trying to display... 

now, you can change the code to the following.

```
			 <ContentPresenter
						DataContext="{Binding RelativeSource={RelativeSource Mode=FindAncestor, AncestorType=UserControl}, Path=DataContext}"
						ContentTemplate="{StaticResource ManyMarketLabelIndicator}"
						ToolTip="{Binding RelativeSource={RelativeSource Mode=FindAncestor, AncestorType=UserControl}, Path=DataContext.MarketIndicatorTooltip}"
						Visibility="{Binding RelativeSource={RelativeSource Mode=FindAncestor, AncestorType=UserControl}, Path=DataContext.ShowAllMarketIndicators, Converter={StaticResource InvertedBooleanToVisibilityConverter}}"
						/> 
```

you can as well remove the "DataContext" settings as well.

```
			 <ContentPresenter
						ContentTemplate="{StaticResource ManyMarketLabelIndicator}"
						ToolTip="{Binding RelativeSource={RelativeSource Mode=FindAncestor, AncestorType=UserControl}, Path=DataContext.MarketIndicatorTooltip}"
						Visibility="{Binding RelativeSource={RelativeSource Mode=FindAncestor, AncestorType=UserControl}, Path=DataContext.ShowAllMarketIndicators, Converter={StaticResource InvertedBooleanToVisibilityConverter}}"
						/> 
```

because the DataTemplate 'ManyMarketLabelIndicator" do not use the Bindings.

```
	<DataTemplate
		x:Key="ManyMarketLabelIndicator">
		<Border
			x:Name="MarketLabelIndicator"
			Padding="3,0"
			MaxWidth="66"
			MinHeight="18"
			Margin="2,0,0,0">
			<Border.Background>
				<Binding RelativeSource="{RelativeSource Mode=FindAncestor, AncestorType=UserControl}" Path="DataContext.Status" Converter="{StaticResource AlertPopupBackgroundConverter}" ConverterParameter="{x:Static converters:AlertNotificationBackgroundConverter.MarketIndicatorParamName}" />
			</Border.Background>
			<TextBlock
				Text="MANY"
				VerticalAlignment="Center"
				HorizontalAlignment="Center"
				Margin="0,0,0,1"
				TextTrimming="WordEllipsis"/>
		</Border>
```

Another intreseting thing that I  have encountered is this:

```
	<Style TargetType="{x:Type ListBoxItem}" x:Key="LiquidityListBoxItemStyle">
		<Setter Property="Background" Value="Transparent"/>
		<Setter Property="HorizontalContentAlignment" Value="{Binding HorizontalContentAlignment, RelativeSource={RelativeSource AncestorType={x:Type ItemsControl}}}"/>
		<Setter Property="VerticalContentAlignment" Value="{Binding VerticalContentAlignment, RelativeSource={RelativeSource AncestorType={x:Type ItemsControl}}}"/>
		<Setter Property="Foreground" Value="{DynamicResource ForegroundBrush}"/>
		<Setter Property="SnapsToDevicePixels" Value="True"/>
		<Setter Property="UseLayoutRounding" Value="True"/>
		<Setter Property="MinHeight" Value="20"/>
		<Setter Property="Template">
			<Setter.Value>
				<ControlTemplate TargetType="{x:Type ListBoxItem}">
					<Grid x:Name="NotificationListItem">
						<Grid.ColumnDefinitions>
							<ColumnDefinition Width="57"/>
							<ColumnDefinition Width="*"/>
							<ColumnDefinition Width="70"/>
						</Grid.ColumnDefinitions>
						<Border x:Name="Bd" BorderThickness="1,0" SnapsToDevicePixels="true" Grid.ColumnSpan="1" Grid.Column="1" BorderBrush="{DynamicResource DefaultBorderBrush}"/>
						<TextBlock x:Name="Fill" TextWrapping="NoWrap" Text="{Binding Size}" VerticalAlignment="Center" HorizontalAlignment="Center"/>
						<TextBlock x:Name="FillProperties" TextWrapping="NoWrap" Text="" Grid.Column="1" VerticalAlignment="Center" Margin="4,0" HorizontalAlignment="Left"/>
						<!--<ContentControl ContentTemplate="{StaticResource LiquidityMarketLabelIndicator}" DataContext="{Binding Market}" Grid.Column="2" Margin="0,1,2,1"/>-->
						<ContentPresenter ContentTemplate="{StaticResource LiquidityMarketLabelIndicator}" DataContext="{Binding Market}" Grid.Column="2" Margin="0,1,2,1" />
					</Grid>
					<ControlTemplate.Triggers>
						<Trigger Property="IsSelected" Value="true"/>
						<Trigger Property="IsEnabled" Value="false"/>
					</ControlTemplate.Triggers>
				</ControlTemplate>
			</Setter.Value>
		</Setter>
	</Style>
```

then, we have the following template definition. "LiquidityMarketLabelIndicator"

```
	<DataTemplate
		x:Key="LiquidityMarketLabelIndicator">
		<Border
			x:Name="MarketLabelIndicator"
			Padding="3,0"
			MaxWidth="66"
			MinHeight="18"
			Margin="2,0,0,0">
			<Border.Background>
				<Binding RelativeSource="{RelativeSource Mode=FindAncestor, AncestorType=UserControl}" Path="DataContext.Status" Converter="{StaticResource AlertPopupBackgroundConverter}" ConverterParameter="{x:Static converters:AlertNotificationBackgroundConverter.MarketIndicatorParamName}" />
			</Border.Background>
			<TextBlock
				Text="{Binding Market}"
				VerticalAlignment="Center"
				HorizontalAlignment="Center"
				Margin="0,0,0,1"
				TextTrimming="WordEllipsis"/>
		</Border>
	</DataTemplate>
```

It looks like that the DataContext of inner defined resource has forcely reset the DataContext value and disregard the value of the DataContext value that I set 

```
DataContext="{Binding Market}"
```

and the ContentControl has slightly different handling to the ContentPresenter. if I change the code.

```
<ContentControl ContentTemplate="{StaticResource LiquidityMarketLabelIndicator}" DataContext="{Binding Market}" Grid.Column="2" Margin="0,1,2,1"/>
```

It just simply does not work...

## how does the margin affect the size of a control

Recently we have a simple UserControl which shows the Alerts. the problem is that the right side of the Alert seems to be cropped out. 

how does that happen, we find that if we change the Margin in the UserControl's settings then the Cropped border things has gone. 

the user control is something as below. 

```

<UserControl
	x:Class="Views.AlertNotification.AlertToastView"
	xmlns:toast="clr-namespace:Core.Toast;assembly=YourAssembly">

    <!-- .... -->
	<Grid x:Name="LayoutRoot" Width="320" MinHeight="105" Margin="0,0,2,2>
				<Rectangle x:Name="Hover" Grid.ColumnSpan="4" Fill="#19FFFFFF" Grid.RowSpan="4" Visibility="Collapsed" Stroke="{DynamicResource AccentBrush}"/>
```

it was because of the Minimum size of the ToastWindow is at least 321 size width. and when the margin is counted, we have to count the margin to the extern window (that is 320 + 2 to the right..)  

Also because of the Toast size is not changeable once it is displayed. It is like there is one pixel that has been cut out out by the Toast API.

and because of the border is initially collapsed, and when the window is shown, and by the trigger when the border is visible again, the border is just out side of the bound of the custom control.

So when you count on the size of a  control, thinks of the outside containers (such as the window) and taking into the account of the margin value.


## MediaPlayer does not play sounds keept as a resource file.

I have a application which plays sounds from a local file, the code is as such.

```
MediaPlayer player = new MediaPlayer();
player.Open(new Uri("Sounds/Chimes.wav"));
player.Play();
```

the Sounds/Chimes.wav file is set as follow

Build Action: "Content"
Copy to Directory: "Copy Always"

However, this does not help if I try to embeded a resource, such as 

```
MediaPlayer player = new MediaPlayer();
player.Open(new Uri("pack://application:,,,/MediaPlayerTest;component/Sounds/Chimes.wav"));
player.Play()
```

as per the reference shown below. 

> Actually you can not play the sound files keeping as resource files. This is cause for the media playback to not to start.

>You have to copy the resource sound files to the IsolatedStorage .

>and then you need to set the same files as source to the MediaElement to start the media playback.

References:

[Windows Phone Develoment – Multiple .mp3 files in media element and sound-effect not working - Stack Overflow](http://stackoverflow.com/questions/9308374/windows-phone-develoment-multiple-mp3-files-in-media-element-and-sound-effect)


## WPF application Resource, Content, and Data Files
while it is common that sometime you want to play sound or use a resource file in your application. there are few choices when you consider this. 

1. Resource (unlike the embedded resource )
2. Content files (Standalone data files )
3. Site of Origin Files: (has no association with an executable WPF assemblies)
4. Embedded Resource 

I will not talk about the Embedded Resource file in this matter. 

1. Resource file
to use the Resource file, there is a prerequisite that the file has to be configured to be Build action of "Resource" and there is no need to set "Copy" as local.

to show you a code that load the Resource file contents.

```
// Navigate to xaml page
Uri uri = new Uri("/PageResourceFile.xaml", UriKind.Relative);
StreamResourceInfo info = Application.GetResourceStream(uri);
System.Windows.Markup.XamlReader reader = new System.Windows.Markup.XamlReader();
Page page = (Page)reader.LoadAsync(info.Stream);
this.pageFrame.Content = page;
```

or sometimes, it is even easy just to set the Source , such as 

```
Uri pageUri = new Uri("/PageResourceFile.xaml", UriKind.Relative);
this.pageFrame.Source = pageUri;
```

you can do that via XAML , that is for sure.

2. Content file
Content file is just a loose file that alonside the executable assemblies.

to use the Content File, you first need to configure the "Build Action" to be "Content" and sometimes you need to set the "Copy to Directory" behavior to "Copy Always"


If you attempt to read the Content file, you can also use the programming code , such as 


```
// Navigate to xaml page
Uri uri = new Uri("/PageContentFile.xaml", UriKind.Relative);
StreamResourceInfo info = Application.GetContentStream(uri);
System.Windows.Markup.XamlReader reader = new System.Windows.Markup.XamlReader();
Page page = (Page)reader.LoadAsync(info.Stream);
this.pageFrame.Content = page;
```

3. The 3rd, the Site of Oring file.

You can erfer the Pack Uri to get more details about the Site of Origin files.

```
// Navigate to xaml page
Uri uri = new Uri("/SiteOfOriginFile.xaml", UriKind.Relative);
StreamResourceInfo info = Application.GetRemoteStream(uri);
System.Windows.Markup.XamlReader reader = new System.Windows.Markup.XamlReader();
Page page = (Page)reader.LoadAsync(info.Stream);
this.pageFrame.Content = page;
```

and a more appropriate example to show that how to get resource from a site of origin file is that you have to use the full Pack uri to refer to them..

```
Uri pageUri = new Uri("pack://siteoforigin:,,,/SiteOfOriginFile.xaml", UriKind.Absolute);
this.pageFrame.Source = pageUri;
```


4. the Embedded Resource file
this is a general way to store resource . however, difference is that the WPF resource is stored in an assembly called 

`AssemblyName.g.Resources ` files

while the embedded resources , the resources is stored in the 
`AssemblyName.Properties.Resources.resources`. while you can create more than one embedded resource file, that resouce files can be managed by `ResourceManager`

If you looked at the generated resource files, you will see 

```
[global::System.ComponentModel.EditorBrowsableAttribute(global::System.ComponentModel.EditorBrowsableState.Advanced)]
        internal static global::System.Resources.ResourceManager ResourceManager {
            get {
                if (object.ReferenceEquals(resourceMan, null)) {
                    global::System.Resources.ResourceManager temp = new global::System.Resources.ResourceManager("Properties.Resources", typeof(Resources).Assembly);
                    resourceMan = temp;
                }
                return resourceMan;
            }
        }
```
You can create the ResourceManager yourself.

References:
[WPF Application Resource, Content, and Data Files](http://msdn.microsoft.com/en-us/library/aa970494.aspx)


## Different ways to get Stream

it is different when you want to get a resource out of Embedded Resource or just a Resource. 

for an embedded resource, you can do this:  

```
            SoundPlayer soundPlayer = new SoundPlayer(MediaPlayerTest.Properties.Resources.chimes);
            soundPlayer.Stream = MediaPlayerTest.Properties.Resources.notify;
            soundPlayer.Stream = MediaPlayerTest.Properties.Resources.ResourceManager.GetStream("ploop");
```

while for an Resource, to get the Stream, you can do this:

```
            StreamResourceInfo sri = Application.GetResourceStream(new Uri("sounds/servicedown.wav", UriKind.Relative));
            if (sri != null)
            {
                soundPlayer.Stream = sri.Stream;
            }
```


## Play sound wit the SoundPlayer
the SoundPlayer is a limited capability class that enables you to play sounds. However, by saying that it is limited capability class we are meaning that it has one outstanding restriction that 

1. it can only play the PCM .wav file.


If you plan to play the RF64 format .wav file you might probably use the DX interaction, there are some libraries out there that you can readily use.


## A strange ComboBox issue together with DevExpress
I found a very strange issue that occurs when it is used together with DevExpress. 

The ComboBox 's xaml code is as such 
```
				<ComboBox
							x:Name="cmbx"
							Style="{DynamicResource AutoCompleteComboBox}" 
							Text="{Binding SearchText, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}"
							SelectedValue="{Bindng SearchText}"
							SelectedValuePath="Alias"
							DisplayMemberPath="InstrDisplay"  
							TextSearch.TextPath="Alias"
							IsTextSearchEnabled="False"
							IsEditable="True"
							>
```

and it has an attached behavior which is shown as below.

```
    public class InstrumentComboBehavior : Behavior<ComboBox>
    {
        private static readonly ILog Log = LogManager.GetLogger(MethodBase.GetCurrentMethod().DeclaringType);


        protected override void OnAttached()
        {
            AssociatedObject.Loaded += AssociatedObjectLoaded;
            AssociatedObject.IsKeyboardFocusedChanged += AssociatedObject_FocusChanged;
            AssociatedObject.DropDownOpened += AssociatedObject_DropDownOpened;
            AssociatedObject.KeyUp += AssociatedObject_KeyUp;
            AssociatedObject.AddHandler(TextBoxBase.TextChangedEvent, _textChangeHandler);
            base.OnAttached();
        }

        protected override void OnDetaching()
        {
            AssociatedObject.DropDownOpened -= AssociatedObject_DropDownOpened;
            AssociatedObject.IsKeyboardFocusedChanged -= AssociatedObject_FocusChanged;
            AssociatedObject.KeyUp -= AssociatedObject_KeyUp;

            if (_textChangeHandler != null)
            {
                AssociatedObject.RemoveHandler(TextBoxBase.TextChangedEvent, _textChangeHandler);
            }

            base.OnDetaching();
        }

        private void ComboBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            var combo = (ComboBox)sender;

            var viewModel = combo.DataContext as DepthViewerViewModel;

            if (viewModel != null && !viewModel.IsInstrumentComboValid)
            {
                viewModel.IsInstrumentComboValid = true;
            }

            if (combo.SelectedItem == null && combo.IsKeyboardFocusWithin)
            {
                var upperCase = combo.Text.ToUpper();

                if (0 != string.Compare(upperCase, combo.Text, StringComparison.InvariantCulture))
                {
                    // there's a chance that inner textbox is still initializing and 
                    // text is still in lower case, we need to make sure it shows up in upper case
                    combo.Text = upperCase;
                }

                SearchInstrument(combo, combo.Text);
            }
        }
```


the problem is that it seems that the GridControl is reusing a grid row like when it is delete a row in the middle. 

the solution is to remove the following contents from the ComboBox's definition 

`SelectedValue="{Binding SearchText}"`

Reason is because when one row is deleted from the GridControl, GridControl seems to reuse the GridRow and 					thus caused the Text and SelectedValue to be reevaluated. Each row has its own items source based on the text input. SelectedValue's change will change ComboBox.Text to string.Empty and thus the issue.

## MagnificationBehavior
Maginification Behavior is based on fact that the WPF engine has provided with a layout system, which can do translate or Scale transform or other type of transforms.
the Magnification system is based on the LayoutTransfroms. 
Let's first see how the MagnificationBehavior is implemented.

```
    /// <summary>
    /// MagnificationBehavior - a behavior class that enable to Magnifiy the element based on the Magnification coeffecient
    /// </summary>
    /// <remarks>
    /// The Magnification Behaivor's decorated element's first child (the child) will be magnified with the use of the ScaleTransform  - an layout transform which helps enlarge or enshrink .
    /// 
    /// When the parent (the behavior's directly decorated element's size changes, the Behavior is expected to receive event and fires that event to re-Scale the adorned elements.
    /// </remarks>
    public class MagnificationBehavior : Behavior<FrameworkElement>
    {
        #region Dependency Properties
        public double DisplayScaling
        {
            get { return (double)GetValue(DisplayScalingProperty); }
            set { SetValue(DisplayScalingProperty, value); }
        }

        // Using a DependencyProperty as the backing store for DisplayScaling.  This enables animation, styling, binding, etc...
        /* Do not use the UIPropertyMetadata , rather use the PropertyMetadata */
        public static readonly DependencyProperty DisplayScalingProperty =
            DependencyProperty.Register("DisplayScaling", typeof(double), typeof(MagnificationBehavior), new PropertyMetadata(1.0, OnDisplayChanged));
        #endregion


        #region Fields 
        private readonly ScaleTransform _scaleTransform = new ScaleTransform();
        #endregion

        #region Public Properties
        #endregion

        #region Private Proeprties
        private Transform ChildLayoutTransform
        {
            get
            {
                var child = FindVisualChildren<FrameworkElement>(AssociatedObject).FirstOrDefault();
                if (child != null)
                {
                    return child.LayoutTransform;
                }

                return null;
            }

            set
            {
                var child = FindVisualChildren<FrameworkElement>(AssociatedObject).FirstOrDefault();
                if (child != null)
                {
                    child.LayoutTransform = value;
                }
            }
        }
        #endregion

        #region Overrides Methods
        protected override void OnAttached()
        {
            AssociatedObject.SizeChanged += AssociatedObjectSizeChanged;
            base.OnAttached();
        }

        protected override void OnDetaching()
        {
            base.OnDetaching();
            AssociatedObject.SizeChanged -= AssociatedObjectSizeChanged;
        }
        #endregion


        #region Private Static Methods
        private static IEnumerable<T> FindVisualChildren<T>(DependencyObject depObj) where T : DependencyObject
        {
            if (depObj != null)
            {
                for (int i = 0; i < VisualTreeHelper.GetChildrenCount(depObj); i++)
                {
                    DependencyObject child = VisualTreeHelper.GetChild(depObj, i);
                    if (child != null && child is T)
                    {
                        yield return (T)child;
                    }

                    foreach (T childOfChild in FindVisualChildren<T>(child))
                    {
                        yield return childOfChild;
                    }
                }
            }
        }

        private static void OnDisplayChanged(DependencyObject depObj, DependencyPropertyChangedEventArgs e)
        {
            var magnificationBehavior = depObj as MagnificationBehavior;
            if (magnificationBehavior != null)
            {
                magnificationBehavior.CheckNewActualSize(magnificationBehavior.DisplayScaling);
            }
        }
        #endregion

        #region Private Methods 
        private void AssociatedObjectSizeChanged(object sender, SizeChangedEventArgs e)
        {
            CheckNewActualSize(DisplayScaling);
        }

        private void CheckNewActualSize(double scale)
        {
            _scaleTransform.ScaleX = scale;
            _scaleTransform.ScaleY = scale;

            if (!ReferenceEquals(_scaleTransform, ChildLayoutTransform))
            {
                ChildLayoutTransform = _scaleTransform;
            }
        }
        #endregion
    }

```

As in the comment section, the Behavior is able to change the transform factor once the depnedency property has changed. and the other is that when the parent' element's size has changed, the transform is also updated.

Let's see the View in action 
```
<Window x:Class="MagnificationBehaviorTest.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
				xmlns:behavior="clr-namespace:MagnificationBehaviorTest.Behaviors"
				xmlns:i="clr-namespace:System.Windows.Interactivity;assembly=System.Windows.Interactivity"
        Title="MainWindow" Height="350" Width="525">
    <Grid>
        <Grid.RowDefinitions>
					<RowDefinition />
					<RowDefinition />
					<RowDefinition />
				</Grid.RowDefinitions>

				<Grid
					Grid.Row="0">
					<TextBlock
							Text="Dummy Content">
					</TextBlock>
				<i:Interaction.Behaviors>
					<!-- you cannot just embedded the behavior directly to the elemnt's child content -->
					<behavior:MagnificationBehavior 
												DisplayScaling="{Binding DisplayScaling}"/>
				</i:Interaction.Behaviors>

				</Grid>
					

				<TextBox
					Grid.Row="1"
					Text="{Binding DisplayScaling, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}" />

					<Button
					Grid.Row="2"
						Content="Exit"
						ToolTip="Click this button to exit"
					></Button>
    </Grid>
</Window>

```


the viewmodel part is quit simple for what is worth, here is the code. 

```
    /// <summary>
    /// Defines a class to use as the View Models
    /// </summary>
    public class MainWindowViewmodel : INotifyPropertyChanged
    {
        #region Private Fields 

        private double _displayScaling = 1.0;
        #endregion

        #region public Properties
        public double DisplayScaling
        {
            get
            {
                return _displayScaling;
            }

            set
            {
                _displayScaling = value;
                OnPropertyChanged("DisplayScaling");
            }
        }
        #endregion

        #region INotifyPropertyChanged Implementation
        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(propertyName));
            }

        }
        #endregion 
    }
```

## An advanced topic - Multi-threaded UI decorator to show content

### Class introduction


* PresentationSource
* HostVisual

As a comparison, we will introduce the 
*Window
HwndHost 

classes


* _PresentationSource_
First let's see the PresentationSource class. the class hierarchy is as such.


>System.Object 
  System.Windows.Threading.DispatcherObject
    System.Windows.PresentationSource
      System.Windows.Interop.HwndSource

and the blurb of this class 

> Provides an abstract base for classes that present content from another technology as part of an interoperation scenario. In addition, this class provides static methods for working with these sources, as well as the basic visual-layer presentation architecture.

Mainly you would like to use this class if you want to host content from another technology such as a windows form contents, or Open GL Visual or etc...

In our case, we will use this Presentation source to show content generated from another thread.

* _HostVisual_
second, we are going to visit the *HostVisual* class.  the class hierarchy is 

> System.Object 
  System.Windows.Threading.DispatcherObject
    System.Windows.DependencyObject
      System.Windows.Media.Visual
        System.Windows.Media.ContainerVisual
          System.Windows.Media.HostVisual

this class fork from the Control class (Window, ListBox and others) since the DependencyObject, and it branches out the PresentationSource from the DispatcherObject.

as in its blurb. 

>Represents a Visual object that can be connected anywhere to a parent visual tree.


so that lays our foundation for the multi-thread UI hosted decorator type of contents.

As promised that I will introduce you some of related and most commonly used classs. first and foremost, the typical `Window` class. 

* *VisualTarget*

the class hiearchy

>System.Object 
  System.Windows.Threading.DispatcherObject
    System.Windows.Media.CompositionTarget
      System.Windows.Media.VisualTarget


Yet another class which decending from the DispatcherObject but do not follow the DependencyProperty one.

in its blurb.

> Provides functionality for connecting one visual tree to another visual tree across thread boundaries.

that is our *key*, its provides the link between thread boundaries. as for how that is beyond the scope of this discussion. but as we will shortly see that VisualTarget use another content as its target visual...

* *Decorator class*
the class hierarchy for the decorator clas is as below.

> Provides a base class for elements that apply effects onto or around a single child element, such as Border or Viewbox.

and its class hierarchy is as follow.

>System.Object 
  System.Windows.Threading.DispatcherObject
    System.Windows.DependencyObject
      System.Windows.Media.Visual
        System.Windows.UIElement
          System.Windows.FrameworkElement
            System.Windows.Controls.Decorator


* *Window*
> System.Object 
  System.Windows.Threading.DispatcherObject
    System.Windows.DependencyObject
      System.Windows.Media.Visual
        System.Windows.UIElement
          System.Windows.FrameworkElement
            System.Windows.Controls.Control
              System.Windows.Controls.ContentControl
                System.Windows.Window
                  System.Windows.Controls.Ribbon.RibbonWindow
                  System.Windows.Navigation.NavigationWindow


As you can see that the Window bisect from the HostVisual starting from the `Visual` class then followed by the `Visual` class there is the `UIElement` then `FrameworkElement`.


You may wonder there is a class called `HwndHost` that can host windows forms content, how that is possible.

* *HwndHost*

> System.Object 
  System.Windows.Threading.DispatcherObject
    System.Windows.DependencyObject
      System.Windows.Media.Visual
        System.Windows.UIElement
          System.Windows.FrameworkElement
            System.Windows.Interop.HwndHost
              System.Windows.Forms.Integration.WindowsFormsHost
              System.Windows.Interop.ActiveXHost

as you can see that it resides in the "System.Windows.Interop" namespace and is intended as a bridge between different technology.

Interesting enough that the HwndHost is also a UIElement, but it differs from the window like contorl , that it starts to fork from the `Control` level.


References So FAR:
[VisualTarget Class (System.Windows.Media)](http://msdn.microsoft.com/en-us/library/system.windows.media.visualtarget(v=vs.110).aspx)
[PresentationSource Class (System.Windows)](http://msdn.microsoft.com/en-us/library/system.windows.presentationsource(v=vs.110).aspx)
[HwndHost Class (System.Windows.Interop)](http://msdn.microsoft.com/en-us/library/system.windows.interop.hwndhost(v=vs.110).aspx)
[Window Class (System.Windows)](http://msdn.microsoft.com/en-us/library/system.windows.window%28v=vs.110%29.aspx)
[HostVisual Class (System.Windows.Media)](http://msdn.microsoft.com/en-us/library/system.windows.media.hostvisual(v=vs.110).aspx)

### BackgroundVisualHost (Custom class) as directly the child of the BusyDecorator

```
    public delegate Visual CreateContentFunction();

    /// <summary>
    /// The background visual host.
    /// </summary>
    public class BackgroundVisualHost : FrameworkElement
    {
        #region Private fields 

        private HostVisual _hostVisual;
        private ThreadVisualHelper _threadedHelper;
        #endregion

        #region Properties (dp)
        #endregion 

        #region Overrides 
        // Queried by the framework to return the count of Visual Child.
        protected override int VisualChildrenCount
        {
            get
            {
                return _hostVisual != null ? 1 : 0;
            }
        }

        // Getter to retrieve the nth visual child of the Visual elements.
        protected override System.Windows.Media.Visual GetVisualChild(int index)
        {
            if (_hostVisual != null && index == 0) return _hostVisual;
            throw new IndexOutOfRangeException("index");
        }

        // Queries by the framework to return the collection of Logical child.
        protected override System.Collections.IEnumerator LogicalChildren
        {
            get
            {
                if (_hostVisual != null) yield return _hostVisual;
            }
        }

        protected override Size MeasureOverride(Size availableSize)
        {
            if (_threadedHelper != null) return _threadedHelper.DesiredSize; // delegate to the lower bands.
            return base.MeasureOverride(availableSize);
        }

        #endregion

        #region Handlers (private)
        private void CreateContentHelper()
        {
            _threadedHelper = new ThreadVisualHelper(CreateContent, SafeInvalidateMeasure);
            _hostVisual = _threadedHelper.HostVisual; // though it is a simple assignment operation, but the source HostVisual is taken from a background thread helper.
        }

        private void SafeInvalidateMeasure()
        {
            Dispatcher.BeginInvoke(new Action(InvalidateMeasure), DispatcherPriority.Loaded); // this can be called by background thread to ensure that the invalide measure call happens on the ownner thread.
        }

        private void HideContentHelper()
        {
            if (_threadedHelper != null)
            {
                _threadedHelper.Exit(); // each time the Busy Indicator is shown or hide a new thread helper is created to handle that request.
                _threadedHelper = null;
                InvalidateMeasure(); // this is to re-render the contents?
            }
        }
        #endregion

        public bool IsContentShowing
        {
            get { return (bool)GetValue(IsContentShowingProperty); }
            set { SetValue(IsContentShowingProperty, value); }
        }

        // Using a DependencyProperty as the backing store for IsContentShowing.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty IsContentShowingProperty =
            DependencyProperty.Register("IsContentShowing", typeof(bool), typeof(BackgroundVisualHost), new FrameworkPropertyMetadata(false, OnIsContentShowingChanged));

        static void OnIsContentShowingChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var visualhost = (BackgroundVisualHost)d;
            if (visualhost.CreateContent != null)
            {
                if ((bool)e.NewValue)
                {
                    visualhost.CreateContentHelper();
                }
                else
                {
                    visualhost.HideContentHelper();
                }
            }
        }
        #region CreateContent Property

        /// <summary>
        /// Identifies the CreateContent dependency property.
        /// </summary>
        public CreateContentFunction CreateContent
        {
            get { return (CreateContentFunction)GetValue(CreateContentProperty); }
            set { SetValue(CreateContentProperty, value); }
        }

        // Using a DependencyProperty as the backing store for CreateContent.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty CreateContentProperty =
            DependencyProperty.Register("CreateContent", typeof(CreateContentFunction), typeof(BackgroundVisualHost), new FrameworkPropertyMetadata(OnCreateContentChanged));

        static void OnCreateContentChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var visualHost = (BackgroundVisualHost)d;
            if (visualHost.IsContentShowing)
            {
                visualHost.HideContentHelper();
                if (e.NewValue != null)
                {
                    visualHost.CreateContentHelper();
                }
            }
        }
        #endregion


        #region classes (private)
        private class ThreadVisualHelper
        {
            #region fields 

            private readonly HostVisual _hostVisual;
            private readonly AutoResetEvent _sync = new AutoResetEvent(false);
            private readonly CreateContentFunction _createContent;
            private readonly Action _invalidateMeasure;
            #endregion


            #region proeprties
            public HostVisual HostVisual { get { return _hostVisual; } }
            public Size DesiredSize { get; private set; }
            public Dispatcher Dispatcher { get; private set; }
            #endregion
            public ThreadVisualHelper(CreateContentFunction createContent, Action invalidateMeasure)
            {
                _hostVisual = new HostVisual();
                _createContent = createContent;
                _invalidateMeasure = invalidateMeasure;

                var backgroundUi = new Thread(CreateAndShowContent);
                backgroundUi.SetApartmentState(ApartmentState.STA);
                backgroundUi.Name = "BackgroundVisualHostTrehad";
                backgroundUi.IsBackground = true;
                backgroundUi.Start();

                _sync.WaitOne();
            }

            public void Exit()
            {
                Dispatcher.BeginInvokeShutdown(DispatcherPriority.Send);
            }

            #region Helpers (private) 
            private void CreateAndShowContent()
            {
                Dispatcher = Dispatcher.CurrentDispatcher;
                //Create the VisualTargetPresentationSource and then signal the
                //calling thread, so that it can continue without waiting for us.
                var source = new VisualTargetPresentationSource(_hostVisual);
                _sync.Set();

                // Create a media element and use it as the root visual for the Visual Target
                source.RootVisual = _createContent();
                DesiredSize = source.DesiredSize;
                _invalidateMeasure(); // - JOE: this method is required to invalidate the measure so that the HostVisual connected to the VisualTarget can properly resize its contents.

                // Run a dispatcher for this worker thread, this is the central processing loop for WPF 
                Dispatcher.Run();
                source.Dispose();
            }
            #endregion
        }
        #endregion
    }
```

the key above is the override of the `BackgroundVisualHost` override to the `FrameworkElement`'s override methods. the methods includes the following

* VisualChildrenCount
* GetVisualChild
* LogicalChildren
* MeasureOverride

the former 3 handles the BackgroundVisualHost's reference to the HostVisual as its direct child and the last one handles the situation of measure/arrange.

As in the inner class ThreadVisualHelper, which offers the helper methods for create/Exit the background threads.

as in the creation helper methods, it creates the PresentationSource for the HostVisual. (the host visual actually is created in the UI threads, while the PresentationSource is created in created in the background threads - it is the PresentationSource which handles the handling/operation to an UI element).

### PresenationSource to bridge the Visual Host and target

Now let's come to the PresentationSource override methods. It is the `VisualTargetPresentationSource` which inherits and implements the `PresentationSource` class.

```
    /// <summary>
    /// A Presentation Source as in its blurb. "provide an abstract base for clases that present content from another technology as part of the interopration scenario."
    /// </summary>
    /// <remarks>
    /// In my understanding, the PresentationSource gives the Core a way to query for interfaces/operations to the Visual Elements. it encapsulate operations/interactions to the 
    /// Visual that it represents.
    /// </remarks>
    public class VisualTargetPresentationSource : PresentationSource
    {
        #region fields 

        private readonly VisualTarget _visualTarget;
        private bool _isDisposed;
        #endregion

        #region Constructor(s)
        public VisualTargetPresentationSource(HostVisual hostVisual)
        {
            _visualTarget = new VisualTarget(hostVisual);
            AddSource(); // AddSource is one of the VisualTargetPresentationSource methods. As said by the PresentationSource documentation, that the PresentationSource class offers many visual helpers methods to help WPF.
        }

        #endregion

        #region Implementation (PresentationSource)
        protected override CompositionTarget GetCompositionTargetCore()
        {
            return _visualTarget;
        }

        public override Visual RootVisual
        {
            get
            {
                return _visualTarget.RootVisual;
            }
            set
            {
                var oldRoot = _visualTarget.RootVisual;

                // Set the root visual of the VisualTarget.  This visual will
                // now be used to visually compose the scene.
                _visualTarget.RootVisual = value;

                // Tell the PresentationSource that the root visual has
                // changed.  This kicks off a bunch of stuff like the
                // Loaded event.
                RootChanged(oldRoot, value); // JOE: why we need to call this is is a very intreseting questions.

                // Kickoff layout...
                var rootElement = value as UIElement;
                if (rootElement != null)
                {
                    rootElement.Measure(new Size(double.PositiveInfinity, double.PositiveInfinity));
                    rootElement.Arrange(new Rect(rootElement.DesiredSize));

                    DesiredSize = rootElement.DesiredSize;
                }
                else
                {
                    DesiredSize =new Size(0,0);
                }
            }
        }

        public override bool IsDisposed
        {
            get
            {
                return _isDisposed;
            }
        }
        #endregion

        #region Properties 
        public Size DesiredSize { get; private set; } // DesiredSize is a common properties that exists on many Controls, 
                                                      // why this we have to declare the DesiedSize in the VisualTargetPresentationSource explicilty?
        #endregion

        #region Dispose
        internal void Dispose()
        {
            RemoveSource();
            _isDisposed = true;
        }
        #endregion
    }

```

this class has three overrides to thte PresenationSource, they are

* GetCompositionTargetCore
* RootVisual
* IsDisposed

the first two operates on the VisualTarget. while as in the description of the VisualTarget, which provides the Cross thread connectivity between one visual tree to another visual tree.

as in the Constructor, the Host Visual (the same Visual created in the same UI thread) is created as a constructor parameter to the VisualTarget.

###  VisualTarget to connect VisualHost
this is omitted for space reason, some of its functionality has been mentioned in the above sections.


### the BusyDecorator to wire all up.

now comes to the BusyDecorator that connects all the dots.

```
    /// <summary>
    /// The BusyDecorator classes
    /// </summary>
    [StyleTypedProperty(Property = "BusyStyle", StyleTargetType = typeof(Control))] // - A Note on the StyleTypedProperty, in our example, it means that the Style applied to Control, 
                                                                                    // SHall also applies to the BusyDecorator classes.
    public class BusyDecorator : Decorator
    {
        private readonly BackgroundVisualHost _busyHost = new BackgroundVisualHost();

        private static double _busyStyleControlSize; // what is the use of this class?

        #region IsBusy Property

        /// <summary>
        /// Identifies the IsBusy dependency property.
        /// </summary>
        public static readonly DependencyProperty IsBusyProperty = DependencyProperty.Register(
            "IsBusy",
            typeof(bool),
            typeof(BusyDecorator),
            new FrameworkPropertyMetadata(
                false, FrameworkPropertyMetadataOptions.AffectsMeasure, OnIsBusyPropertyChanged));

        /// <summary>
        /// Gets or sets if the BusyDecorator is being shown.
        /// </summary>
        public bool IsBusy
        {
            get { return (bool)GetValue(IsBusyProperty); }
            set { SetValue(IsBusyProperty, value); }
        }

        private static void OnIsBusyPropertyChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) // once the IsBusy changed. change the child's enablement to false/true based.
        {
            var decorator = (BusyDecorator)d;
            if (decorator == null)
            {
                return;
            }

            if (decorator.Child == null)
            {
                return;
            }

            var childElement = decorator.Child;
            if ((bool)e.NewValue)
            {
                childElement.IsEnabled = false;
            }
            else
            {
                childElement.IsEnabled = true;
            }
        }
        #endregion

        #region BusyStyle


        public Style BusyStyle
        {
            get { return (Style)GetValue(BusyStyleProperty); }
            set { SetValue(BusyStyleProperty, value); }
        }

        // Using a DependencyProperty as the backing store for BusyStyle.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty BusyStyleProperty =
            DependencyProperty.Register("BusyStyle", typeof(Style), typeof(BusyDecorator), new FrameworkPropertyMetadata(OnBusyStyleChanged));

        private static void OnBusyStyleChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var decorator = (BusyDecorator)d;
            var newVal = (Style)e.NewValue; // pass a new createe contents methods in.
            decorator._busyHost.CreateContent =
                () => new Control() { Style = newVal, Width = _busyStyleControlSize, Height = _busyStyleControlSize };
        }
        #endregion



        public HorizontalAlignment BusyHorizontalAlignment
        {
            get { return (HorizontalAlignment)GetValue(BusyHorizontalAlignmentProperty); }
            set { SetValue(BusyHorizontalAlignmentProperty, value); }
        }

        // Using a DependencyProperty as the backing store for BusyHorizontalAlignment.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty BusyHorizontalAlignmentProperty =
            DependencyProperty.Register("BusyHorizontalAlignment", typeof(HorizontalAlignment), typeof(BusyDecorator), new FrameworkPropertyMetadata(HorizontalAlignment.Center));



        public VerticalAlignment BusyVerticalAlignment
        {
            get { return (VerticalAlignment)GetValue(BusyVerticalAlignmentProperty); }
            set { SetValue(BusyVerticalAlignmentProperty, value); }
        }

        // Using a DependencyProperty as the backing store for BusyVerticalAlignment.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty BusyVerticalAlignmentProperty =
            DependencyProperty.Register("BusyVerticalAlignment", typeof(VerticalAlignment), typeof(BusyDecorator), new FrameworkPropertyMetadata(VerticalAlignment.Center));




        public double DecoratorSize
        {
            get { return (double)GetValue(DecoratorSizeProperty); }
            set { SetValue(DecoratorSizeProperty, value); }
        }

        // Using a DependencyProperty as the backing store for DecoratorSize.  This enables animation, styling, binding, etc...
        public static readonly DependencyProperty DecoratorSizeProperty =
            DependencyProperty.Register("DecoratorSize", typeof(double), typeof(BusyDecorator), new FrameworkPropertyMetadata(40.0, FrameworkPropertyMetadataOptions.BindsTwoWayByDefault, OnDecoratorSizeChanged));


        private static void OnDecoratorSizeChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var decorator = (BusyDecorator)d;
            if (decorator == null) return;
            _busyStyleControlSize = (double)e.NewValue;
        }

        #region constructor(s)
        static BusyDecorator()
        {
            DefaultStyleKeyProperty.OverrideMetadata(typeof(BusyDecorator), new FrameworkPropertyMetadata(typeof(BusyDecorator)));
        }


        public BusyDecorator()
        {
            // @ constructor, add both the _busyHost as the Logical and Visual Child of the Current Busy Decorator class.
            AddLogicalChild(_busyHost);
            AddVisualChild(_busyHost);

            SetBinding(_busyHost, IsBusyProperty, BackgroundVisualHost.IsContentShowingProperty);
            SetBinding(_busyHost, BusyHorizontalAlignmentProperty, HorizontalAlignmentProperty);
            SetBinding(_busyHost, BusyVerticalAlignmentProperty, VerticalAlignmentProperty);

            if (DecoratorSize < 5) DecoratorSize = 5; // this is to ensure at least 5 is needed for the siz.e

            _busyStyleControlSize = DecoratorSize;

            // Register Unloaded Event Handlers
            Unloaded += (obj, e) =>
                {
                    var storyboard = FindResource("SpinAnimation") as Storyboard;
                    if (storyboard != null)
                    {
                        storyboard.Stop();
                    }
                };

        }
        #endregion


        #region Functional
        private void SetBinding(DependencyObject obj, DependencyProperty source, DependencyProperty target)
        {
            var binding = new Binding { Source = this, Path = new PropertyPath(source) }; // this is to set the Bindings from one Dependency Property to another depdency Property.
            BindingOperations.SetBinding(obj, target, binding);
        }

        protected override Size MeasureOverride(Size constraint)
        {
            // Measure the Busy host and itself to determine which one is the bigger one.
            var ret = new Size(0, 0);
            if (Child != null)
            {
                Child.Measure(constraint);
                ret = Child.DesiredSize;
            }

            _busyHost.Measure(constraint);

            return new Size(Math.Max(ret.Width, _busyHost.DesiredSize.Width),
                            Math.Max(ret.Height, _busyHost.DesiredSize.Height));
        }

        protected override Size ArrangeOverride(Size arrangeSize)
        {
            var ret = new Size(0, 0);
            if (Child != null)
            {
                Child.Arrange(new Rect(arrangeSize));
                ret = Child.RenderSize;
            }
            
            _busyHost.Arrange(new Rect(arrangeSize));

            return new Size(Math.Max(ret.Width, _busyHost.RenderSize.Width), Math.Max(ret.Height, _busyHost.RenderSize.Height));
        }
        #endregion

        #region Overrides
        protected override int VisualChildrenCount
        {
            get
            {
                return Child != null ? 2 : 1;
            }
        }

        protected override System.Collections.IEnumerator LogicalChildren
        {
            get
            {
                if (Child != null)
                {
                    yield return Child;
                }

                yield return _busyHost;
            }
        }

        protected override System.Windows.Media.Visual GetVisualChild(int index)
        {
            if (Child != null)
            {
                switch (index)
                {
                    case 0:
                        return Child;
                    case 1:
                        return _busyHost;
                }
            }
            else if (index == 0)
            {
                return _busyHost;
            }

            throw new IndexOutOfRangeException("index");
        }
        #endregion

    }
```

It create one `_busyHost` of type `BackgroundVisualHost` as its child, as in the constructor, it has the following code.

```
AddLogicalChild(_busyHost);
AddVisualChild(_busyHost);
```

Other  than this, there are a few Binding operations. Like binding the IsContentShowing to IsBusy, Horizontal and BusyHorizontalAlignment...

In one of the callback (OnIsContentShowing of BackgroundVisualHost), there will call CreateContentHelper or StopContentHelper.

that helpers manipulates the start/stop of background visual contents.

### the overall structure
the ovarall structure of the above classes in the terms of 
the Background Decorator is as follows.


```
PresentationSource --> VisualTarget --> HostVisual
                              ^
                              |
                      BackgroundVisualhost
```

the  `-->` in the above code means that the VisualTarget is a child of the PresentationSource of BackgroundVisualHost.


## TargetNullValue and Fallbackvalue


```
				<TextBox
					Width="30"
					Margin="2,0,0,0"
					VerticalAlignment="Center"
					Text="{Binding QuickClickQuantity, FallbackValue=0, TargetNullValue=0}" />
```


References:
[xaml - WPF Binding - Default value for empty string - Stack Overflow](http://stackoverflow.com/questions/15567588/wpf-binding-default-value-for-empty-string)


## Error border when binding failed

it could be that our style has changed how the binding error are dispplayed, normally the binding error wil be ignored but our style shows an error border.
and if you look at the output window you can see that :

```
System.Windows.Data Error: 7 : ConvertBack cannot convert value '' (type 'String'). BindingExpression:Path=QuickClickQuantity; DataItem='DepthViewerViewModel' (HashCode=23894041); target element is 'TextBox' (Name=''); target property is 'Text' (type 'String') FormatException:'System.FormatException: Input string was not in a correct format.
   at System.Number.StringToNumber(String str, NumberStyles options, NumberBuffer& number, NumberFormatInfo info, Boolean parseDecimal)
   at System.Number.ParseInt32(String s, NumberStyles style, NumberFormatInfo info)
   at System.String.System.IConvertible.ToInt32(IFormatProvider provider)
   at System.Convert.ChangeType(Object value, Type conversionType, IFormatProvider provider)
   at MS.Internal.Data.SystemConvertConverter.ConvertBack(Object o, Type type, Object parameter, CultureInfo culture)
   at System.Windows.Data.BindingExpression.ConvertBackHelper(IValueConverter converter, Object value, Type sourceType, Object parameter, CultureInfo culture)'
```

My solution is a EmptyStringIntConverter 

```
    /// <summary>
    /// Empty string Revrese converter converter
    /// </summary>
    /// <remarks>
    /// Empty string converter will convert a enmpty string to a value that specified by the 
    /// </remarks>
    public class EmptyStringIntConverter : IValueConverter
    {
        #region IValueConverter

        public object Convert(object value, System.Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            return value == null ? parameter : value.ToString();
        }

        public object ConvertBack(object value, System.Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            int intValue;
            return string.IsNullOrEmpty(value as string) || int.TryParse(value as string, out intValue)
                       ? parameter
                       : intValue;
        }

        #endregion
    }

```


## TransformGroup 

the transform group is a way that can let  you group several transform group together.

```
							<Path.LayoutTransform>
								<TransformGroup>
									<RotateTransform  Angle="180"/>
									<ScaleTransform ScaleX="0.8" ScaleY="0.8" />
								</TransformGroup>
							</Path.LayoutTransform>
```

While by default you can one transform into the Transform group . 

```
						<Path x:Name="DownArrow"                     
                          Fill="{DynamicResource ApplicationPrimaryGrayBrush }"
                            HorizontalAlignment="Center"
                          VerticalAlignment="Center"
                         Data="M 0 0 L 9 9 L 17 0 Z">
								<Path.LayoutTransform>
									<ScaleTransform ScaleX="0.8" ScaleY="0.8" />
								</Path.LayoutTransform>
						</Path>
```


## Change the ListBox the selection item's content template
It has been a very hot topic that we needs a way to change the background of the selected items' background, as per the stack overflow page, [wpf - Change background color for selected ListBox item - Stack Overflow][wpf - Change background color for selected ListBox item - Stack Overflow], it was suggested to change the ItemContainerStyle.  

and as per the Official MSDN page, You'd create a new `ItemContainerStyle`.   Which seems too overkill for me. 

I used a ItemTemplate to do the work, which looks like below. 
```
						<ListBox ItemsSource="{Binding SizeUnits}" SelectedItem="{Binding SizeUnit}">
							<ListBox.ItemsPanel>
								<ItemsPanelTemplate>
									<VirtualizingStackPanel Orientation="Horizontal" />
								</ItemsPanelTemplate>
							</ListBox.ItemsPanel>
							<!--<ListBox.ItemContainerStyle>
								<Style TargetType="{x:Type ListBoxItem}">
									<Setter Property="Content"></Setter>
								</Style>
							</ListBox.ItemContainerStyle>-->
							<ListBox.ItemTemplate>
								<DataTemplate>
									<Border x:Name="Bd" Background="{DynamicResource ApplicationDefaultBackgroundBrush}">
										<TextBlock Text="{Binding}" VerticalAlignment="Center" />
									</Border>
									<DataTemplate.Triggers>
										<Trigger Property="ListBoxItem.IsSelected" Value="True">
											<Setter Property="Background" TargetName="Bd" Value="{DynamicResource SelectionBrush}" />
										</Trigger>
									</DataTemplate.Triggers>
								</DataTemplate>
							</ListBox.ItemTemplate>
						</ListBox>
					</StackPanel>
```



References:
[wpf - Change background color for selected ListBox item - Stack Overflow][wpf - Change background color for selected ListBox item - Stack Overflow]
[wpf - Change background color for selected ListBox item - Stack Overflow]:http://stackoverflow.com/questions/2138200/change-background-color-for-selected-listbox-item
[ItemsControl.ItemContainerStyle Property (System.Windows.Controls)][ItemsControl.ItemContainerStyle Property (System.Windows.Controls)]
[ItemsControl.ItemContainerStyle Property (System.Windows.Controls)]:http://msdn.microsoft.com/en-us/library/system.windows.controls.itemscontrol.itemcontainerstyle.aspx

## Special use of '.' in the Binding 


```
							<ListBox.ItemTemplate>
								<DataTemplate>
									<Border x:Name="Bd" Background="{Binding Path=Background, RelativeSource={RelativeSource Mode=FindAncestor, AncestorType=ListBoxItem}}">
										<TextBlock Text="{Binding ., Mode=OneWay}" VerticalAlignment="Center" />
									</Border>
								</DataTemplate>
							</ListBox.ItemTemplate>
```


## When to choose the DataTrigger or Trigger

DataTrigger is more lenient in that it can accepts the Data Binding (the following may works)


```

<ContentControl 
    x:Name="designerContent"
    MinHeight="100"
    Margin="2,0,2,2"
    Content="{Binding Path=DesignerInstance}"
    Background="#FF999898">
    <ContentControl.Style>
        <Style TargetType="{x:Type ContentControl}">
            <Setter Property="Visibility" Value="Collapsed"/>
            <Style.Triggers>
                <DataTrigger
                        Binding="{Binding
                            RelativeSource={RelativeSource
                                Mode=FindAncestor,
                                AncestorType={x:Type ListBoxItem}},
                                Path=IsSelected}"
                        Value="True">
                    <Setter Property="Visibility" Value="Visible"/>
                </DataTrigger>
            </Style.Triggers>
        </Style>
    </ContentControl.Style>
</ContentControl>
```

While trigger as a general trigger does not allows bindings.  (the following has nothing)... (though the following is a Dependency Property, but perhaps that it is not a attached property)


```

								<DataTemplate>
									<Border x:Name="Bd">
										<TextBlock Text="{Binding}" VerticalAlignment="Center" />
									</Border>
									<DataTemplate.Triggers>
										<Trigger Property="ListBoxItem.IsSelected" Value="True">
											<Setter Property="Background" TargetName="Bd" Value="{DynamicResource SelectionBrush}" />
										</Trigger>
									</DataTemplate.Triggers>
								</DataTemplate>
```


References:
[WPF Trigger for IsSelected in a DataTemplate for ListBox items - Stack Overflow](http://stackoverflow.com/questions/248545/wpf-trigger-for-isselected-in-a-datatemplate-for-listbox-items)

## MultiValueConverter does not update once binding item value changes. 

I created one IMultiValueConverter implementation, and here is the code. 

```
    public class OrderBlotterSizeConverter : IMultiValueConverter
    {

        #region Implementation (IMultiValueConverter)
        /// <summary>
        /// Convert 
        /// </summary>
        /// <param name="values">the Inputs.</param>
        /// <param name="targetType">the Target type</param>
        /// <param name="parameter"></param>
        /// <param name="culture">the culture</param>
        /// <returns>the effective Size quantity</returns>
        public object Convert(object[] values, Type targetType, object parameter, CultureInfo culture)
        {
            if (values.Length != 2)
            {
                throw new ArgumentOutOfRangeException("values", "Expect two arguments input");
            }

            if (!(values[0] is int))
            {
                throw new ArgumentException("Expect first argument of type int");
            }

            if (!(values[1] is bool))
            {
                throw new ArgumentException("Expect second argument of type bool");
            }

            var size = (int)values[0];
            var minSize = (bool)values[1];

            return minSize ? 1 : size;
        }

        public object[] ConvertBack(object value, Type[] targetTypes, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
        #endregion
    }
```

and it is used by the following xaml code 

```
		<DataTemplate x:Key="OrderQuantityTemplate">
			<Grid>
				<TextBlock 
					Visibility="{Binding RowData.Row.AllowQuantityEdit, Converter={StaticResource invertedBooleanToVisibilityConverter}}"
					VerticalAlignment="Center" 
					HorizontalAlignment="Right" 
					Margin="5,0,0,0" 
					Text="{Binding RowData.Row.BlotterQty}" />
				<Grid Visibility="{Binding RowData.Row.AllowQuantityEdit, Converter={StaticResource BoolToVisibilityConverter}}">
					<controls:OrderBlotterQuantityControl 
						VerticalAlignment="Stretch" 
						HorizontalAlignment="Stretch" 
						FontSize="15" 
						InitValue="{Binding RowData.Row.BlotterEditQty, Mode=OneTime}"   
						Value="{Binding RowData.Row.BlotterEditQty, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}" >
						<controls:OrderBlotterQuantityControl.Increment>
							<MultiBinding Converter="{StaticResource OrderBlotterSizeConverter}">
									<Binding RelativeSource="{RelativeSource FindAncestor, AncestorType=UserControl}" Path="DataContext.LevelAndSizeSelectorViewModel.SizeUnit" Mode="OneWay" />
									<Binding RelativeSource="{RelativeSource FindAncestor, AncestorType=UserControl}" Path="DataContext.LevelAndSizeSelectorViewModel.MinSize" Mode="OneWay" />
							</MultiBinding>
						</controls:OrderBlotterQuantityControl.Increment>
						<controls:OrderBlotterQuantityControl.InputBindings>
							<KeyBinding Command="{Binding RowData.Row.CancelButton}"  Gesture="F4"/>
							<KeyBinding Command="{Binding RowData.Row.UpdateButton}"  Gesture="F2"/>
						</controls:OrderBlotterQuantityControl.InputBindings>
					</controls:OrderBlotterQuantityControl>
				</Grid>
			</Grid>
		</DataTemplate>
```

## RelativeSource limitation
I have data template which is used for rendering grid cells. (is DataTemplate itself the reason why the RetiveSource binding not working?)


```
					</controls:OrderBlotterPriceDecimalControl>
<!-- Increment="{Binding RelativeSource={RelativeSource AncestorType=UserControl}, Path=DataContext.LevelAndSizeSelectorViewModel.TickIncr, Mode=OneWay}"  -->
					<controls:OrderBlotterPriceTextControl 
						Visibility="{Binding RowData.Row.ShowTickFormat, Converter={StaticResource booleanToVisibilityConverter}}" 
						VerticalAlignment="Stretch"
						HorizontalAlignment="Stretch" 
						FontSize="15" 
						InitValue="{Binding RowData.Row.OrderPriceStr, Mode=OneTime}"  
						Value="{Binding RowData.Row.OrderPriceStr, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}" 
						ParsedValue="{Binding RowData.Row.Price, Mode=OneWay}"
						ValueType="{Binding RowData.Row.ValueType, Mode=TwoWay}" 
						UpdateCommand="{Binding RowData.Row.UpdateButton, Mode=OneWay}">
						<controls:OrderBlotterPriceTextControl.Increment>
							<MultiBinding Converter="{StaticResource OrderBlotterLevelAndSizeConverter}" ConverterParameter="{x:Static converters:OrderBlotterLevelAndSizeConverter.Level}" Mode="OneWay">
									<Binding Path="RowData.Row" />
									<Binding Path="DataContext.SelectedSize" RelativeSource="{RelativeSource Mode=FindAncestor, AncestorType=UserControl}"/>
							</MultiBinding>
							</controls:OrderBlotterPriceTextControl.Increment>
					</controls:OrderBlotterPriceTextControl>
```

If I change the multibinding to somethingas below. (Looks like that GridControl has provides a wrapping/proxy to the original DataContext).

```
<MultiBinding Converter="{StaticResource OrderBlotterLevelAndSizeConverter}" ConverterParameter="{x:Static converters:OrderBlotterLevelAndSizeConverter.Level}" Mode="OneWay">
									<Binding Path="RowData.Row" />
									<Binding Path="View.DataContext.SelectedSize" RelativeSource="{RelativeSource Mode=FindAncestor, AncestorType=dxg:GridControl}"/>
							</MultiBinding>
```

The converter may received the second parameter sometimes as "DependencyProperty.UnsetValue".

I also tried the following (replacing RelativeSource with Source). -- which later proves to be wrong.


```
<MultiBinding Converter="{StaticResource OrderBlotterLevelAndSizeConverter}" ConverterParameter="{x:Static converters:OrderBlotterLevelAndSizeConverter.Level}" Mode="OneWay">
									<Binding Path="RowData.Row" />
									<Binding Path="DataContext.SelectedDecimalLevel" Source="{RelativeSource Mode=FindAncestor, AncestorType=UserControl}"/>
							</MultiBinding>
```

Out of despair, I change it to the following (which does not use the RelativeSource at all) -- though not working, I am gonnna blow...


```
						<controls:OrderBlotterQuantityControl.Increment>
								<MultiBinding Converter="{StaticResource OrderBlotterLevelAndSizeConverter}" ConverterParameter="{x:Static converters:OrderBlotterLevelAndSizeConverter.Size}" Mode="OneWay">
									<Binding Path="RowData.Row" />
									<Binding Path="RowData.View.DataContext.SelectedSize" />
								</MultiBinding>
							</controls:OrderBlotterQuantityControl.Increment>
```
and last it is the ElementName binding.

As stated by others that RelativeSource may works well if using "ElementName" binding.  [wpf - Binding only works using ElementName, why? - Stack Overflow][wpf - Binding only works using ElementName, why? - Stack Overflow]

The code uses ElementName is 

```
<MultiBinding Converter="{StaticResource OrderBlotterLevelAndSizeConverter}" ConverterParameter="{x:Static converters:OrderBlotterLevelAndSizeConverter.Level}" Mode="OneWay">
									<Binding Path="RowData.Row" />
									<Binding Path="DataContext.SelectedSize" ElementName="orderBlotter"/>
							</MultiBinding>
```


Finally I found the reason, it was because the extra code here inside the `OrderBlotterQuantityControl`

```
        private static void OnIncrementPropertyChanged(DependencyObject sender, DependencyPropertyChangedEventArgs e)
        {
            var vm = (OrderBlotterQuantityControl)sender;
            vm.Increment = (int)e.NewValue;
        }
```

Once the callback is called, Increment is set with POC value and the Binding then is cleared. that is the reason why it does not work. After removing the code, the code works just fine. .....!!!!!!!!
     
References:

[wpf - Binding only works using ElementName, why? - Stack Overflow]: http://stackoverflow.com/questions/23298170/binding-only-works-using-elementname-why

## Validation Error
To enable the Data Validation, first, implements the IDataError.

then in the xaml , enable ValidatesOnDataErrors in data bindings.


```
					<TextBox
						Width="152"
						Text="{Binding QuickClickQuantityStr, UpdateSourceTrigger=PropertyChanged, ValidatesOnDataErrors=True, NotifyOnValidationError=True}"
						ToolTip="{Binding QuickClickQuantityErrorMessage}"
						FontSize="12px"
						gmp:TextBoxBehavior.SelectAllOnFocus="True"
						gmp:TextBoxBehavior.ClearTextOnEscape="True"
						gmp:TextBoxBehavior.Watermark="{StaticResource QuickClickQuantityWaterMark}"
						VerticalAlignment="Center" />
```

you can implements the Error tooltip in viewmodel, such as 
```
        private int? _quickClickQuantity;
        public int? QuickClickQuantity
        {
            get { return _quickClickQuantity; }
            set
            {
                if (value != _quickClickQuantity)
                {
                    _quickClickQuantity = value;
                    //TODO: Validation for the entered quantity. It has to be >0.
                    if (_quickClickQuantity.HasValue && _quickClickQuantity.Value > 0)
                    {
                        QuickClickQuantityStr = _quickClickQuantity.ToString();
                    }

                    RaisePropertyChanged(() => QuickClickQuantity);
                }
            }
        }

        private string _quickClickQuantityStr;
        public string QuickClickQuantityStr
        {
            get
            {
                return _quickClickQuantityStr;
            }

            set
            {
                if (value != _quickClickQuantityStr)
                {
                    _quickClickQuantityStr = value;
                    int quantity;
                    if (int.TryParse(_quickClickQuantityStr, out quantity))
                    {
                        QuickClickQuantity = quantity;
                        ClearError(() => QuickClickQuantityStr);
                        QuickClickQuantityErrorMessage = null;
                    }
                    else
                    {
                        QuickClickQuantity = null;
                        if (!string.IsNullOrEmpty(_quickClickQuantityStr))
                        {
                            QuickClickQuantityErrorMessage = string.Format("Invalid input: {0}", QuickClickQuantityStr);
                            SetError(() => QuickClickQuantityStr, QuickClickQuantityErrorMessage);
                        }
                        else
                        {
                            ClearError(() => QuickClickQuantityStr);
                            QuickClickQuantityErrorMessage = null;
                        }
                    }

                    RaisePropertyChanged(() => QuickClickQuantityStr);
                }
            }
        }

        private string _quickClickQuantityErrorMessage;
        public string QuickClickQuantityErrorMessage
        {
            get
            {
                return _quickClickQuantityErrorMessage;
            }

            set
            {

                _quickClickQuantityErrorMessage = value;
                RaisePropertyChanged(() => QuickClickQuantityErrorMessage);
            }
        }


```

quick some code, huh?? We can do this:


```
		<Style x:Key="QuickExecutionTextBoxStyle" BasedOn="{StaticResource ApplicationTextBoxStyle}" TargetType="{x:Type TextBox}">
			<Style.Triggers>
				<Trigger Property="Validation.HasError" Value="True">
					<Setter Property="ToolTip" Value="{Binding RelativeSource={RelativeSource Self}, Path=(Validation.Errors)[0].ErrorContent}" />
				</Trigger>
			</Style.Triggers>
		</Style>
```

and the textbox code now becomes.

```
					<TextBox
						Width="152"
						Text="{Binding QuickClickQuantityStr, UpdateSourceTrigger=PropertyChanged, ValidatesOnDataErrors=True, NotifyOnValidationError=True}"
						FontSize="12px"
						gmp:TextBoxBehavior.SelectAllOnFocus="True"
						gmp:TextBoxBehavior.ClearTextOnEscape="True"
						gmp:TextBoxBehavior.Watermark="{StaticResource QuickClickQuantityWaterMark}"
						VerticalAlignment="Center" 
						Style="{StaticResource QuickExecutionTextBoxStyle}"/>
```

you might wonder why the Validation.HasError and Validation.Errors (in parenthesis). they are attached properties, which when enclosed in the parenthesis will allow the Xaml editor to better resolve to the right attached properties.


References:
[validation - How to use IDataErrorInfo.Error in a WPF program? - Stack Overflow](http://stackoverflow.com/questions/14023552/how-to-use-idataerrorinfo-error-in-a-wpf-program)

## LostFocus and LostKeyboardFocus
Remember that Keyboard are global, but Focus (Logical ) are not... 

so that If you attached to the LostKeyboardFocus, once another window is activated, it is fired. But LostFocus happens only when you move focus out of the current focused element in the logical scope.

Choose wisely.

## GridControl is reusing the Grid rows, and this is causing unwantted results

the GridControl developed by the DevExpress has unwantted result that it reused for optimization purpose. this is causing the unwantted results.

let's review two examples.

1. the SelectedItem and the ItemsSource property.

```
				<!-- 
				GEMBOWUS-769:
					the following content is removed from the ComboBox below.

							SelectedValue="{Binding SearchText}"

					Reason is because when one row is deleted from the GridControl, GridControl seems to reuse the GridRow and 
					thus caused the Text and SelectedValue to be reevaluated. Each row has its own items source based on the text input.
					SelectedValue's change will change ComboBox.Text to string.Empty and thus the issue.
					-->
				<ComboBox
							x:Name="cmbx"
							Style="{DynamicResource AutoCompleteComboBox}" 
							Text="{Binding SearchText, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}"
							SelectedValuePath="Alias"
							DisplayMemberPath="InstrDisplay"  
							TextSearch.TextPath="Alias"
							IsTextSearchEnabled="False"
							IsEditable="True"							>
```

as explained in the comment, there was a "SelectedValue={Binding SearchText"}" property settings, now this has been removed.


2. OneTime binding ..
the one time binding was first introduced to optimize the performance, but this also introduced problems.

```
					<controls:OrderBlotterPriceTextControl 
						Visibility="{Binding RowData.Row.ShowTickFormat, Converter={StaticResource booleanToVisibilityConverter}}" 
						VerticalAlignment="Stretch"
						HorizontalAlignment="Stretch" 
						InitValue="{Binding RowData.Row.OrderPriceStr, Mode=OneTime}"  
						Value="{Binding RowData.Row.OrderPriceStr, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}" 
						ParsedValue="{Binding RowData.Row.Price, Mode=OneWay}"
						ValueType="{Binding RowData.Row.ValueType, Mode=TwoWay}"
						Increment="{Binding RowData.Row.PriceIncr}" 
						UpdateCommand="{Binding RowData.Row.UpdateButton, Mode=OneWay}">
					</controls:OrderBlotterPriceTextControl>
```

THere was used to be 

```
Increment="{Binding RowData.Row.PriceIncr, Mode=OneTime}"
```

however, as you know when this reusing the rows, one row may be using the PriceIncr from another row, and this is causing a lots of issues.

As shown in the following logs.

```
2014-12-11T10:41:13.683165 [WARN ] {Thread: UI} Unable to perform increasing SpinText Price, Expected value after increasing is 99.8371875, but formatted string is 99-266


```


## how can I pass a constant value for 1 binding in multi-binding

you can pass one binding for 1 binding in multi-bindings.


here you can leverage the Source property of the Binding element, here is an example of that in action.

```
<TextBlock>
  <TextBlock.Resources>
    <sys:Int32 x:Key="fixedValue">123</sys:Int32>
  </TextBlock.Resources>
  <TextBlock.Text>
    <MultiBinding Converter="{StaticResource myConverter}">
      <Binding Path="myFirst.Value" />
      <Binding Source="{StaticResource fixedValue}" />
    </MultiBinding>
  </TextBlock.Text>
</TextBlock>
```


Or you can use my tricks below, which leverage some x:Static tag, and here is the code. 

```
				<ContentPresenter
					Content="{StaticResource BidButton}">
					<ContentPresenter.Visibility>
						<MultiBinding Converter="{StaticResource OrderTicketButtonVisibilityConverter}" ConverterParameter="{x:Static converters:OrderTicketButtonVisibilityConverter.BidButton}">
							<Binding Path="InverseBuySell" Mode="OneWay" />
							<Binding Path="Show2Buttons" Mode="OneWay" />
							<Binding Source="{x:Static converters:OrderTicketButtonVisibilityConverter.RightSide}" />
						</MultiBinding>
					</ContentPresenter.Visibility>
				</ContentPresenter>
```

## KeyEventArgs.Key to char

the KeyEventArgs.Key is seomthing of System.Windows.Input.Key which is not readable for user to decipher.

we sometimes need to understand what what is really inside that Keyboard.Ke. so we can do the following (using of the P/Invoke) methods.

```
public static class KeyEventUtility
{
    // ReSharper disable InconsistentNaming
    public enum MapType : uint
    {
        MAPVK_VK_TO_VSC = 0x0,
        MAPVK_VSC_TO_VK = 0x1,
        MAPVK_VK_TO_CHAR = 0x2,
        MAPVK_VSC_TO_VK_EX = 0x3,
    }
    // ReSharper restore InconsistentNaming

    [DllImport( "user32.dll" )]
    public static extern int ToUnicode(
        uint wVirtKey,
        uint wScanCode,
        byte[] lpKeyState,
        [Out, MarshalAs( UnmanagedType.LPWStr, SizeParamIndex = 4 )] 
        StringBuilder pwszBuff,
        int cchBuff,
        uint wFlags );

    [DllImport( "user32.dll" )]
    public static extern bool GetKeyboardState( byte[] lpKeyState );

    [DllImport( "user32.dll" )]
    public static extern uint MapVirtualKey( uint uCode, MapType uMapType );

    public static char GetCharFromKey( Key key )
    {
        char ch = ' ';

        int virtualKey = KeyInterop.VirtualKeyFromKey( key );
        var keyboardState = new byte[256];
        GetKeyboardState( keyboardState );

        uint scanCode = MapVirtualKey( (uint)virtualKey, MapType.MAPVK_VK_TO_VSC );
        var stringBuilder = new StringBuilder( 2 );

        int result = ToUnicode( (uint)virtualKey, scanCode, keyboardState, stringBuilder, stringBuilder.Capacity, 0 );
        switch ( result )
        {
        case -1:
            break;
        case 0:
            break;
        case 1:
            {
                ch = stringBuilder[0];
                break;
            }
        default:
            {
                ch = stringBuilder[0];
                break;
            }
        }
        return ch;
    }
}
```

basically we get the Virtual Key adn the Scan code of the keyboard (KeyEventArgs.Key) and then with teh MapVirtualKey functiont o map it to a char.. (the real input which should be meant).

References:
[c# - KeyEventArgs.Key to char - Stack Overflow](http://stackoverflow.com/questions/15359336/keyeventargs-key-to-char)

## Behavior to help log the PreviewKeyDown event

Well, to apply what we have learnt so far (the KeyEventArgs.Key to char) we should apply that , here is an behavior which was meant to accomplish this sort of tasks.


```
    public class KeyEventBehavior : Behavior<FrameworkElement>
    {
        #region Logging
        private static readonly ILog Log = LogManager.GetLogger(MethodBase.GetCurrentMethod().DeclaringType);
        #endregion

        #region DP
        public static readonly DependencyProperty OriginProperty = DependencyProperty.Register("Origin", typeof(string), typeof(KeyEventBehavior), new PropertyMetadata(default(string)));

        public string Origin
        {
            get
            {
                return (string)GetValue(OriginProperty);
            }
            set
            {
                SetValue(OriginProperty, value);
            }
        }

        public static readonly DependencyProperty EventProperty = DependencyProperty.Register("Event", typeof(string), typeof(KeyEventBehavior), new PropertyMetadata(default(string)));

        public string Event
        {
            get
            {
                return (string)GetValue(EventProperty);
            }
            set
            {
                SetValue(EventProperty, value);
            }
        }
        #endregion


        #region Overrides

        protected override void OnAttached()
        {
            base.OnAttached();
            AssociatedObject.PreviewKeyDown += AssociatedObjectPreviewKeyDown;
        }

        protected override void OnDetaching()
        {
            base.OnDetaching();
            AssociatedObject.PreviewKeyDown -= AssociatedObjectPreviewKeyDown;
        }

        #endregion


        #region Handlers

        private void AssociatedObjectPreviewKeyDown(object sender, KeyEventArgs e)
        {
            Log.InfoFormat("(OrderTicket)<INTERACTION:Keyboard> key: {0}, key (in char) '{1}', modifiers: {2}. Focused: {3}", e.Key, KeyEventUtility.GetCharFromKey(e.Key), Keyboard.Modifiers, e.OriginalSource);
        }
        #endregion
    }
```

## Focus issues
There was an focusable issue. where moving by tab does not move to child element where we want the tab to move to next element in parent's control.


here is the fix

```
	<Setter Property="Focusable" Value="True"/>
		<Setter Property="IsTabStop" Value="False"/>
```

the key here is to use the combination of "Focusable" and "IstabStop".


## Alignment = Stretch and it use

when you have the requirement where you want to make a control to take the entire space when no other element exists. you can use the "Stretch" alignment..



```HorizontalAlignment="Stretch"```


## Topic - Multhreaded Collection bindings


the following keyword are highlighted,

* ICollectionViewFactory
* ICollectionView
* ReadWriteLockSlim
* Collection interface ....  IList&lt;T&gt;, IList, INotifyCollectionChanged, INotifyPropertyChanged.
* ListCollectionView and its general CollectionView and CollectionViewSource
* IWeakEventListener

So here are the highlight.

1. when bind a collection to the view, the View will (WPF) will create for each view biding a new CollectionVIew...
2. You can hijack the ViewCollection creation by the ICollectionViewFactory interface.
3. You can enhance the plain wpf collectoin implementation through the use of ReaderWriteLockSlim (which implements the read-write lock semantic).
4. WeakerEventListener with its ReceiveWeakEvent help eliminate the possibility of memory leak by use of strong reference.


First let see the implementation of the ReadWriteLockSlim enhanced CollectionVIew implemenation.

```
public class SynchronizedObservableCollection<T> : IList<T>, IList, INotifyCollectionChanged, INotifyPropertyChanged
    {
        #region Instance Fields

        private readonly List<T> _innerCollection;
        private readonly object _syncRoot;

        #endregion

        #region Constructors

        public SynchronizedObservableCollection(object syncRoot = null)
        {
            _syncRoot = syncRoot ?? new object();
            _innerCollection = new List<T>();
        }

        public SynchronizedObservableCollection(IEnumerable<T> source, object syncRoot = null)
        {
            _syncRoot = syncRoot ?? new object();
            _innerCollection = source.ToList();
        }

        #endregion

        #region Write

        /// <summary>
        /// Adds an item.
        /// </summary>
        /// <param name="item">The object to add to the <see cref="T:System.Collections.Generic.ICollection`1"/>.</param>
        public void Add(T item)
        {
            lock (_syncRoot)
            {
                var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Add, item, Count);
                _innerCollection.Add(item);
                OnCollectionChanged(args);
            }
        }


        /// <summary>
        /// Removes all items.
        /// </summary>
        public void Clear()
        {
            lock (_syncRoot)
            {
                _innerCollection.Clear();
                var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Reset);
                OnCollectionChanged(args);
            }
        }

        /// <summary>
        /// Removes the first occurrence of a specific object
        /// </summary>
        /// <returns>
        /// true if item was successfully removed; otherwise, false. This method also returns false if item is not found.
        /// </returns>
        /// <param name="item">The object to remove.</param>
        public bool Remove(T item)
        {
            lock (_syncRoot)
            {
                var idx = IndexOf(item);
                if (idx < 0)
                    return false;
                var ret = _innerCollection.Remove(item);
                var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Remove, item, idx);
                OnCollectionChanged(args);
                return ret;
            }
        }

        /// <summary>
        /// Inserts an item at the specified index.
        /// </summary>
        /// <param name="index">The zero-based index at which <paramref name="item"/> should be inserted.</param>
        /// <param name="item">The object to insert.</param>
        public void Insert(int index, T item)
        {
            lock (_syncRoot)
            {
                _innerCollection.Insert(index, item);
                var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Add, item, index);
                OnCollectionChanged(args);
            }
        }

        /// <summary>
        /// Removes the item at the specified index.
        /// </summary>
        /// <param name="index">The zero-based index of the item to remove.</param>
        public void RemoveAt(int index)
        {
            lock (_syncRoot)
            {
                var item = this[index];
                _innerCollection.RemoveAt(index);
                var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Remove, item, index);
                OnCollectionChanged(args);
            }
        }

        /// <summary>
        /// Gets or sets the element at the specified index.
        /// </summary>
        /// <returns>
        /// The element at the specified index.
        /// </returns>
        /// <param name="index">The zero-based index of the element to get or set.</param>
        public T this[int index]
        {
            get
            {
                lock (_syncRoot).
                {
                    return _innerCollection[index];
                }
            }
            set
            {
                lock (_syncRoot)
                {
                    var newItem = value;
                    var oldItem = _innerCollection[index];
                    _innerCollection[index] = newItem;
                    var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Replace, newItem, oldItem, index);
                    OnCollectionChanged(args);
                }
            }
        }
        
        /// <summary>
        /// Moves an item to the specified index.
        /// </summary>
        /// <param name="oldIndex">The index before moving</param>
        /// <param name="newIndex">The index after moving</param>
        public void Move(int oldIndex, int newIndex)
        {
            if(newIndex == oldIndex)
                return;
            lock (_syncRoot)
            {
                var item = _innerCollection[oldIndex];
                _innerCollection.RemoveAt(oldIndex);
                _innerCollection.Insert(newIndex, item);
                var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Move, item, newIndex, oldIndex);
                OnCollectionChanged(args);
            }
        }

        /// <summary>
        /// Inserts a collection of items at the specified index.
        /// </summary>
        /// <param name="index">The zero-based index at which items should be inserted.</param>
        /// <param name="items">The items to be inserted.</param>
        public void InsertRange(int index, IEnumerable<T> items)
        {
            lock (_syncRoot)
            {
                var tmp = items.ToList();
                _innerCollection.InsertRange(index, tmp);
                var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Add, tmp, index);
                OnCollectionChanged(args);
            }
        }

        /// <summary>
        /// Removes items at the specified index.
        /// </summary>
        /// <param name="index">The zero-based index of the item to remove.</param>
        /// <param name="count">the number of the items to be removed from the specified index</param>
        public void RemoveRange(int index, int count)
        {
            if(count <= 0)
                return;
            lock (_syncRoot)
            {
                var items = _innerCollection.Skip(index).Take(count).ToList();
                if(!items.Any())
                    return;
                _innerCollection.RemoveRange(index, count);
                var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Remove, items, index);
                OnCollectionChanged(args);
            }
        }

        #endregion

        #region Read

        /// <summary>
        /// Determines whether the collection contains a specific value.
        /// </summary>
        /// <returns>
        /// true if item is found; otherwise, false.
        /// </returns>
        /// <param name="item">The item to locate.</param>
        public bool Contains(T item)
        {
            lock (_syncRoot)
            {
                return _innerCollection.Contains(item);
            }
        }

        /// <summary>
        /// Copies the elements to an <see cref="T:System.Array"/>, starting at a particular <see cref="T:System.Array"/> index.
        /// </summary>
        /// <param name="array">The one-dimensional <see cref="T:System.Array"/> that is the destination of the elements. The <see cref="T:System.Array"/> must have zero-based indexing.</param><param name="arrayIndex">The zero-based index in <paramref name="array"/> at which copying begins.</param>
        public void CopyTo(T[] array, int arrayIndex)
        {
            lock (_syncRoot)
            {
                _innerCollection.CopyTo(array, arrayIndex);
            }
        }

        /// <summary>
        /// Gets the number of elements.
        /// </summary>
        /// <returns>
        /// The number of elements.
        /// </returns>
        public int Count
        {
            get { return _innerCollection.Count; }
        }

        /// <summary>
        /// Determines the index of a specific item.
        /// </summary>
        /// <returns>
        /// The index of item if found in the list; otherwise, -1.
        /// </returns>
        /// <param name="item">The object to locate.</param>
        public int IndexOf(T item)
        {
            lock (_syncRoot)
            {
                return _innerCollection.IndexOf(item);
            }
        }

        bool ICollection<T>.IsReadOnly
        {
            get { return ((ICollection<T>)_innerCollection).IsReadOnly; }
        }

        /// <summary>
        /// Returns an enumerator that iterates through the collection.
        /// </summary>
        /// <returns>
        /// A enumerator that can be used to iterate through the collection.
        /// </returns>
        /// <filterpriority>1</filterpriority>
        public IEnumerator<T> GetEnumerator()
        {
            lock (_syncRoot)
            {
                return _innerCollection.GetEnumerator(); 
            }
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }

        #endregion

        #region IList

        int IList.Add(object value)
        {
            var cnt = Count;
            Add((T)value);
            return cnt;
        }

        void IList.Insert(int index, object value)
        {
            Insert(index, (T)value);
        }

        void IList.Remove(object value)
        {
            Remove((T)value);
        }

        object IList.this[int index]
        {
            get { return this[index]; }
            set { this[index] = (T)value; }
        }

        bool IList.Contains(object value)
        {
            return Contains((T)value);
        }

        void ICollection.CopyTo(Array array, int index)
        {
            lock (_syncRoot)
            {
                ((IList)_innerCollection).CopyTo(array, index);
            }
        }

        /// <summary>
        /// The lock object for multi-thread access.
        /// </summary>
        public object SyncRoot
        {
            get { return _syncRoot; }
        }

        /// <summary>
        /// Gets a value indicating whether access to the <see cref="T:System.Collections.ICollection"/> is synchronized (thread safe).
        /// </summary>
        /// <returns>
        /// true if access to the <see cref="T:System.Collections.ICollection"/> is synchronized (thread safe); otherwise, false.
        /// </returns>
        /// <filterpriority>2</filterpriority>
        public bool IsSynchronized
        {
            get { return true; }
        }

        int IList.IndexOf(object value)
        {
            return IndexOf((T)value);
        }

        bool IList.IsReadOnly
        {
            get { return ((IList)_innerCollection).IsReadOnly; }
        }

        bool IList.IsFixedSize
        {
            get { return ((IList)_innerCollection).IsFixedSize; }
        }

        #endregion

        #region INotifyCollectionChanged

        public event NotifyCollectionChangedEventHandler CollectionChanged;

        protected virtual void OnCollectionChanged(NotifyCollectionChangedEventArgs e)
        {
            NotifyCollectionChangedEventHandler handler = CollectionChanged;
            if (handler != null) handler(this, e);
        }

        #endregion

        #region INotifyPropertyChanged

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(string propertyName)
        {
            var handler = PropertyChanged;
            if (handler != null) handler(this, new PropertyChangedEventArgs(propertyName));
        }

        #endregion

    }
```

Well, the above code does not have the ReadWriteLockSlim implementaion, but to replace the common lock with the ReadWriteLockSlim implementation, we should have done the following.

the following 
```
        public void Add(T item)
        {
            lock (_syncRoot)
            {
                var args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Add, item, Count);
                _innerCollection.Add(item);
                OnCollectionChanged(args);
            }
        }
```

should have been changed to the following.


```
	public void Add(T itme)
	{
		try 
		{
			_readWriteLockSlim.EnterWriteLock();
			_innerCollection.Add(item);
		}
		finally 
		{
			_readWriteLockSlim.ExitWriteLock();
		}
	}
```

Then followed by the BindableCollection&lt;T&gt;, the key to the `BindableCollection<T>` which implements the ICollectionViewFactory (whose sole methods is CreateView)

```
    public class BindableCollection<T> : SynchronizedObservableCollection<T>, ICollectionViewFactory
    {
        public BindableCollection()
        {
        }

        public BindableCollection(IEnumerable<T> collect) : base(collect)
        {
        }

        #region ICollectionViewFactory

        public ICollectionView CreateView()
        {
            return new ThreadSafeListCollectionView(this);
        }

        #endregion
    }

```


the IcollectionViewFactory does is to return a new CollectionView if requested. so that here introduced the new CollectionView implementation. (here becaue a CollectionView will be referenced by the Collection through a reference, we use a IWeakEventListener interface (the add event is hadnled by the WeakEventManager.AddListener and alike methods - actually CollectionChangedEventManager is a decendant class to the WeakeventManager). 


```
    /// <summary>
    /// CollectionView that supports changes from multiple threads, and uses weak event to listen to changes on source collection
    /// </summary>
    public class ThreadSafeListCollectionView : ListCollectionView, IWeakEventListener
    {
        private readonly object _syncRoot;
        private bool _isResetting = false;

        public ThreadSafeListCollectionView(IList list) : base(list)
        {
            _syncRoot = list.SyncRoot;
            var incc = list as INotifyCollectionChanged;
            if (incc != null)
            {
                incc.CollectionChanged -= this.OnCollectionChanged;
                CollectionChangedEventManager.AddListener(incc, this);
            }
        }

        public bool ReceiveWeakEvent(Type managerType, object sender, EventArgs e)
        {
            var args = e as NotifyCollectionChangedEventArgs;
            if (args == null)
                return false;

            if (!Dispatcher.CheckAccess())
            {
                _isResetting = true;
                Dispatcher.BeginInvoke(new Action(() =>
                    {
                        if (!_isResetting)
                            return;
                        lock (_syncRoot)
                        {
                            OnCollectionChanged(sender, new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Reset));
                        }
                        _isResetting = false;
                    }));
            }
            else
            {
                var newCnt = args.NewItems == null ? 0 : args.NewItems.Count;
                var oldCnt = args.OldItems == null ? 0 : args.OldItems.Count;
                if (newCnt > 1 || oldCnt > 1)
                {
                    _isResetting = true;
                    args = new NotifyCollectionChangedEventArgs(NotifyCollectionChangedAction.Reset);
                }

                lock (_syncRoot)
                {
                    Dispatcher.Invoke(new Action(() => OnCollectionChanged(sender, args)));
                }
                _isResetting = false;
            }
            return true;
        }
    }

```

<!--- This is not yet done. -->


And we have forget about one implementation on the IEnumerator where by Return an Iterator. IEnumerator interface also inherits from the IDisposable interface.

```
public  class ReadLockEnumerator  : IEnumerator
{
	public ReadLockEnumeartor(ReadWriteLockSlim readWriteLockSlim)
	{
		_readWriteLockSlim = readWriteLockSlim;
		_readWriteLockSlim.EnterReadLock();
	}

	public bool MoveNext() 
	{
		_inner.MoveNext();
	} 

	public object Current
	{
		return _innert.Current;
	}

	public void Dispose()
	{
		_readWriteLockSlim.ExitReadLock();
	}

	~ReadLockEnumerator()
	{
		Dispose(false);
	}
}
```

well, the above code just shows you how you can implements the Enumerator which can satisfy the following read lock when we do the foreach iteration.

```
for (var item in ienumerable) {
	.... // do something against the item.
}

// we want to lock the whole enumerator (- to say guard against unwantted write to the collection represented by the IEnumerable...)
```

About how to extend through the use of IcollectionViewFactory, please see this post:

References:
About WeakEventManager
[WeakEventManager Class (System.Windows)](https://msdn.microsoft.com/en-us/library/system.windows.weakeventmanager(v=vs.110).aspx)
About the Custom Collection View.
[Rat's Blog: How do I provide custom collection view for collection in WPF?](http://immortalratblog.blogspot.hk/2008/05/how-do-i-provide-custom-collection-view.html)
About the Memory leak regarding the "CollectionView".
[Collections, CollectionViews, and a WPF Binding Memory Leak | Pelebyte](http://pelebyte.net/blog/2009/10/01/collections-collectionviews-and-a-wpf-binding-memory-leak/)



## Popup and ToggleButtion interaction problem

well there are some interesting interaction problem between the ToggleButton and the Popup. 
basically we'd like to have the toggle button to control the display of an popup, and the popup shall not stay on top always. 

```
<ToggleButton Name="OptionsButton" Checked="{Binding IsOptionOpen}" />
<Popup Name="OptionsPopup" StaysOpen="False" IsOpen="{Binding IsOptionOpen, Mode=OneWay}" />
```
the problem is that when we click somewhere the Popup goes away, but the togglebutton still checked. We 'd like to change the One way binding to two way bindings.

```
<ToggleButton Name="OptionsButton" Checked="{Binding IsOptionOpen}" />
<Popup Name="OptionsPopup" StaysOpen="False" IsOpen="{Binding IsOptionOpen, Mode=TwoWay}" />
```

But that has problem that the popup cannot be closed by clicking on the ToggleButton again.

there are solution proposed here.

```
public class MyPopup : Popup {
    protected override void OnPreviewMouseLeftButtonDown(MouseButtonEventArgs e) {
        bool isOpen = this.IsOpen;
        base.OnPreviewMouseLeftButtonDown(e);

        if (isOpen)
            e.Handled = true;
    }
}
```

however, we would only want to filter the click event when we are directly click over the ToggleButton 

```
    // Subclass Popup to resolve Popup and Toggle button interaction issue 
    // http://stackoverflow.com/questions/5821709/popup-and-togglebutton-interaction-in-wpf/5821819#5821819
    public class PopupEx : Popup
    {
        // To solve the "can not click anywhere else" problem in answer comment.
        public static DependencyProperty ToggleButtonProperty = DependencyProperty.Register("ToggleButton", typeof(ToggleButton), typeof(PopupEx));

        public ToggleButton ToggleButton
        {
            get { return (ToggleButton)GetValue(ToggleButtonProperty); }
            set { SetValue(ToggleButtonProperty, value); }
        }

        protected override void OnPreviewMouseLeftButtonDown(MouseButtonEventArgs e)
        {
            bool isOpen = IsOpen;

            base.OnPreviewMouseLeftButtonDown(e);

            var toggle = ToggleButton;

            if (isOpen && !IsOpen && toggle != null && toggle.IsMouseOver)
            {
                e.Handled = true;
            }
        }
    }
```

References:
[binding - Popup and Togglebutton interaction in wpf - Stack Overflow](http://stackoverflow.com/questions/5821709/popup-and-togglebutton-interaction-in-wpf/5821819#5821819)


## Evenly distribute columns by Grid.Columns

I have one use case where the Columns should be evenly distributed among several controls. however, the number of controls varies, it can be 2 or it can be 3.

If we do this:

```
              <Grid x:Name="SpinnerGrid"
							  HorizontalAlignment="Center"
							  Grid.Row="0"
							  Margin="1">
                <Grid.ColumnDefinitions>
                  <ColumnDefinition Width="*"/>
                  <ColumnDefinition Width="*"/>
                  <ColumnDefinition Width="Auto" />
                </Grid.ColumnDefinitions>
			
			<Control Grid.Colummn="0" />
			<Control Grid.Colummn="1" />
			<Control Grid.Colummn="2" Visibility={Binding ShowControl3, Converter="{StaticResource BooleanToVisibilityConverter" />
```

the problem is that the 3rd button is not strictly the same width as the first two.


However, given my following solution.

```
			<gmp:BooleanMappingConverter x:Key="TotalColumnWidthConverter">
				<gmp:BooleanMappingConverter.FalseValue>
					<GridLength>Auto</GridLength>
				</gmp:BooleanMappingConverter.FalseValue>
				<gmp:BooleanMappingConverter.TrueValue>
					<GridLength>*</GridLength>
				</gmp:BooleanMappingConverter.TrueValue>
			</gmp:BooleanMappingConverter>
```

Please pay attention to how I create the above GridLength.

If you take a look at the Presentation at the System.Windows.GridLength class, it has the following attributes

```
    [TypeConverter(typeof(GridLengthConverter))]
    public struct GridLength : IEquatable<GridLength>
```

well, if used inside XAML, the XAML runtine can automatically apply the GridLengthConverter. so that you can directly construct the BooleanMappingConverter.

now come back to how the GridColumn.Width is defined.

```
              <Grid x:Name="SpinnerGrid"
							  HorizontalAlignment="Center"
							  Grid.Row="0"
							  Margin="1">
                <Grid.ColumnDefinitions>
                  <ColumnDefinition Width="*"/>
                  <ColumnDefinition Width="*"/>
                  <ColumnDefinition Width="{Binding IsIceBerg, Converter={StaticResource TotalColumnWidthConverter}}" />
                </Grid.ColumnDefinitions>
			
			<Control Grid.Colummn="0" />
			<Control Grid.Colummn="1" />
			<Control Grid.Colummn="2" Visibility={Binding ShowControl3, Converter="{StaticResource BooleanToVisibilityConverter" />
```

depending the value of Visibility of Control3, it can either be GridLength.Auto or GridLength.Start...

And I tested that, this can work pretty well.

## Percentage converter

sometimes you want to set the width/height relative to the one that higher in the hierarchy. you can first create the folowing converter.


```
public class PercentageConverter : IMultiValueConverter
    {
        public object Convert(object[] values, Type targetType, object parameter, CultureInfo culture)
        {
            double targetWidth = (double)values[0];
            double percentage = (double)values[1];
            double adjustment = 0.0;
            if (values.Length > 2)
            {
                adjustment = (double)values[2];
            }

            return targetWidth * percentage + adjustment;
        }

        public object[] ConvertBack(object value, Type[] targetTypes, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
```

Suppose that you have a grid which shall be relative*actual_width_of_parent + adjustment. you can do the following.


```
<Border x:name="TicketBorder">

              <Grid x:Name="SpinnerGrid"

							  HorizontalAlignment="Center"
							  Grid.Row="0"
							  Margin="1">
								<Grid.Width>
									<MultiBinding Converter="{StaticResource PercentageConverter}">
									<Binding ElementName="TicketBorder" Path="ActualWidth" />
									<Binding Source="{StaticResource SpinnerGridWidthPercentage}" />
								</MultiBinding>
	<!-- ... -->
</Border>
```

and you can declare the following static resource as below.

```
			<system:Double x:Key="SpinnerGridWidthPercentage">0.7381818181818182</system:Double>
			<system:Double x:Key="AggButtonPanelAdjustment">-60</system:Double>
```

## PreviewTextInput handler and gotchas

PreviewKeyInput has one benefit over the PreviewKeyDown in that it can gives back the text that are readable (translated rather than obscure Key.Tab event ). And it can also cope with the situation where the IME is involved.

however, it does not mean that PreviewTextInput does no have any drawbacks. 

For one, it does no thandle many caes. as shown in the following article. it does not handle the following KeyEvent.

* Spacebar
* Backspace
* Home/End/Delete/Insert keys
* Arrow keys
* Control key combinations, including Ctrl+V

Our code hooked with the TextBox.PreviewTextInput which does the text manipulation where there existing some Dpenedency Binding which render the TextBox.Text are unsynchronized with what is shown on the screen.

So a workaround is to escape the space operation, here is what I do :


TextBox.PreviewTextInput += TextBox_PreviewTextInput;
TextBox.PreviewKeydown += TextBox_PreviewKeydown;

```
private void TextBox_PreviewKeydown(object sender, KeyEventArgs e)
{
	if (e == Key.Space) { 
		e.handled = true;
	}
}
```

```
private void TextBox_PreviewTextInput(object sender, TextCompositionEventArgs e) {

TextBox _this = (sender as TextBox);
  var text = _this.Text;
  // do some operation to the Text and then then the text 
  // 
_this.Text = text;
_this.CaretIndex = caret;
_this.SelectionStart = caret;
_this.SelectiohnLength = selectionLength;
e.handled = true;
}
```

well, it worth a deal that you read through the code from the below example.

References 
[How to: Handle or Simulate User Input with the WPF WebControl](http://wiki.awesomium.net/wpf/user-input.html)
[#638 – PreviewTextInput Is Not Fired In Many Cases | 2,000 Things You Should Know About WPF](http://wpf.2000things.com/2012/09/03/638-previewtextinput-is-not-fired-in-many-cases/)


## x:Reference

well, when you are inside the DataGrid and you have DataGridXXXColumn, the element is not in the same visual tree so that you cannot do with an ElementName... 


you can find the following code snippet ... 

```
<DataGrid ItemsSource="{Binding GroupsCollection}">
    <DataGrid.Columns>
        <DataGridTextColumn Header="Col1"
                            IsReadOnly="{Binding IsChecked,
                                         Source={x:Reference DisableColumn1}}" >
        </DataGridTextColumn>

        <DataGridTextColumn Header="Col2"
                            IsReadOnly="{Binding IsChecked,
                                         Source={x:Reference DisableColumn2}}" >
        </DataGridTextColumn>
    </DataGrid.Columns>
</DataGrid>

<GroupBox>
    <StackPanel>
        <RadioButton x:Name="DisableColumn2"
                     Content="Col1 IsReadOnlyFalse, Col2 IsReadOnlyTrue"/>
        <RadioButton x:Name="DisableColumn1"
                     Content="Col1 IsReadOnlyTrue, Col2 IsReadOnlyFalse"/>
    </StackPanel>
</GroupBox>
```

here is the quote: 
> ataGridTextColumns doesn't lie in same Visual tree as that of DataGrid so simple binding with ElementName won't work here.
> In case you are using WPF 4.0 or higher you can use x:Reference to bind with radio buttons like this:
> Set x:Name on radio buttons and bind with it using x:Reference.

References: 
[x:Reference 标记扩展](https://msdn.microsoft.com/zh-cn/library/ee795380%28v=vs.110%29.aspx)
[c# - How to binding RadioButton with DataGridTextColumn? - Stack Overflow](http://stackoverflow.com/questions/24882905/how-to-binding-radiobutton-with-datagridtextcolumn)


## get a TaskScheduler from a Dispatcher

well, it is common that you would use the TaskSchuler to do the UI dispatching, well, in UI it is actually the Dispatcher which is doing the heavy lift...

then it raises the neccessity of an util which can does the conversion from Dispatcher to TaskScheduler.


here is what I searched from internet on Dispatcher to TaskScheduler.


```
 public static class ThreadingUtils 
    {
         public static TaskScheduler GetScheduler(Dispatcher dispatcher)
         {
             using (var waiter = new ManualResetEvent(false))
             {
                 TaskScheduler scheduler = null;
                 dispatcher.BeginInvoke(new Action(() =>
                 {
                     scheduler = 
                         TaskScheduler.FromCurrentSynchronizationContext();
                     waiter.Set();
                 }));
                 waiter.WaitOne();
                 return scheduler;
             }
         }
    }
```

References:
[.net - How can I get a TaskScheduler for a Dispatcher? - Stack Overflow](http://stackoverflow.com/questions/6368885/how-can-i-get-a-taskscheduler-for-a-dispatcher)

## Flashing with native wpf way

you can enable Flashing in native wpf way.
well. in the first post of "Making a wpf label or other element flash using animation", it shows someway that flashes the UI element.

```
<Label.Style>
    <Style TargetType="{x:Type Label}">
        <Style.Resources>
            <Storyboard x:Key="flashAnimation" >
                <DoubleAnimation Storyboard.TargetProperty="Opacity" From="1" To="0" AutoReverse="True" Duration="0:0:0.5" RepeatBehavior="Forever" />
            </Storyboard>
        </Style.Resources>

        <Setter Property="Visibility" Value="Hidden" />
        <Style.Triggers>
            <DataTrigger Binding="{Binding OptionInMoney}" Value="True">
                <Setter Property="Visibility" Value="Visible" />
                <DataTrigger.EnterActions>
                    <BeginStoryboard Name="flash" Storyboard="{StaticResource flashAnimation}" />
                </DataTrigger.EnterActions>
                <DataTrigger.ExitActions>
                    <StopStoryboard BeginStoryboardName="flash"/>
                </DataTrigger.ExitActions>
            </DataTrigger>

        </Style.Triggers>
    </Style>
</Label.Style>
```

In that blinking TextBox post, it shows some cool way that to flash the text box if it is enabled.

```
<TextBlock Name="txtBlockScannerText" Margin="10,0,0,0"  Text="WELCOME"> </TextBlock>
        <Button Content="Click Me" Height="23" HorizontalAlignment="Left" Margin="225,43,0,0" Name="button1" VerticalAlignment="Top" Width="75">
            <Button.Triggers>
                <EventTrigger RoutedEvent="Button.Click">
                    <EventTrigger.Actions>
                        <BeginStoryboard>
                            <Storyboard BeginTime="00:00:00" 
                                        RepeatBehavior="Forever" 
                                        Storyboard.TargetName="txtBlockScannerText" 
                                        Storyboard.TargetProperty="(Foreground).(SolidColorBrush.Color)">
                                 <ColorAnimation From="Black" To="Blue" Duration="0:0:1"/>
                            </Storyboard>
                        </BeginStoryboard>
                    </EventTrigger.Actions>
                </EventTrigger>
            </Button.Triggers>
        </Button>
```


References:

[Making a WPF Label (or other element) flash using animation - Stack Overflow](http://stackoverflow.com/questions/15822519/making-a-wpf-label-or-other-element-flash-using-animation)

[wpf - Blinking TextBlock - Stack Overflow](http://stackoverflow.com/questions/2652831/blinking-textblock#)

## UserControl.Trigger can only be EventTrigger

the UserControl.Trigger can only be event Trigger. so the folowing code will always fails

```

<UserControl>
	<UserControl.Triggers>
		<DataTrigger Binding="{Binding UserNoAction}" Value="True">
			<Setter Property="Border.Opacity" TargetName="TicketBorder" />
		</DataTrigger>
	</UserControl.Triggers>
</UserControl>

```

well, the rescue is to define a style to help .

as in this [post](http://stackoverflow.com/questions/7796297/wpf-usercontrols-triggers-and-changing-other-controls), it defines a default style for that user control. 

```

<UserControl x:Class="WpfUserControlSample.ToolbarButtonCombo"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" 
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008" 
             xmlns:local="clr-namespace:WpfUserControlSample"
             x:Name="Control"
             mc:Ignorable="d" 
             d:DesignHeight="30">    
    <UserControl.Resources>
        <Style TargetType="{x:Type local:ToolbarButtonCombo}">
            <Style.Triggers>
                <DataTrigger Binding="{Binding IsButtonMouseOver}" Value="True">
                    <Setter Property="ButtonStyle" Value="Black"/>
                    <Setter Property="ComboStyle" Value="Red"/>                    
                </DataTrigger>
                <!--
                <DataTrigger Binding="{Binding IsComboMouseOver}" Value="True">
                    <Setter Property="ButtonStyle" Value="Red"/>
                    <Setter Property="ComboStyle" Value="Black"/>
                </DataTrigger>
                -->
            </Style.Triggers>
        </Style>
    </UserControl.Resources>
    <StackPanel Orientation="Horizontal" Height="30">
        <Button Name="btn" Background="{Binding ButtonStyle,ElementName=Control,Mode=OneWay}">
            Test
        </Button>
        <ComboBox Name="cmb" Background="{Binding ComboStyle,ElementName=Control,Mode=OneWay}"></ComboBox>
    </StackPanel>
</UserControl>

```
References:

[c# - WPF UserControls; triggers and changing other controls - Stack Overflow](http://stackoverflow.com/questions/7796297/wpf-usercontrols-triggers-and-changing-other-controls)


## Storyboard in Style cannot specify a TargetName

well if you declare the Storyboard with EventTrigger it is perfectly ok that you can declare a TargetName, but if you uses DataTrigger which have to be defined into a Style, you cannot Specify a TargetName, otherwise, you will get the following exception.

```
A Storyboard tree in a Style cannot specify a TargetName. Remove TargetName 'TicketBorder'.
```

the code that has fault is as such 
```
			<Storyboard 
				x:Key="UserNoActionOpacityStoryboard"
				TargetName="TicketBorder"
				TargetProperty="Opacity"
				Duration="0:0:12"
				RepeatBehavior="Forever">
				<DoubleAnimation From="0" To="1" Duration="0:0:1" />
			</Storyboard>
```


while to use it 
```
		<Border 
				x:Name="TicketBorder"
				BorderBrush="Red"
				Opacity="0"
				BorderThickness="1">
			<Border.Style>
				<Style TargetType="Border"
					>
					<Style.Triggers>
						<DataTrigger Binding="{Binding UserNoAction}" Value="True">
							<DataTrigger.EnterActions>
								<BeginStoryboard Storyboard="{StaticResource UserNoActionOpacityStoryboard}" Name="flash" />
							</DataTrigger.EnterActions>
							<DataTrigger.ExitActions>
								<StopStoryboard BeginStoryboardName="flash" />
							</DataTrigger.ExitActions>
						</DataTrigger>
					</Style.Triggers>
				</Style>
			</Border.Style>
		</Border>
```


## Interactivity: event to command

the Interactivity namespace from the clr-namespace: 
`	xmlns:i="clr-namespace:System.Windows.Interactivity;assembly=System.Windows.Interactivity"`

has one  Interaction.Triggers which with the help of i:InvokeCommandAction tag can help raise events.

`<i:Interaction.Triggers>`

one example is as follow.

```
	<i:Interaction.Triggers>
		<i:EventTrigger EventName="PreviewMouseClick">
			<i:InvokeCommandAction Command="{Binding UserActionCommand}" CommandParameter="{x:Null}" />
		</i:EventTrigger>
		<i:EventTrigger EventName="PreviewKeydown">
			<i:InvokeCommandAction Command="{Binding UserActionCommand}" CommandParameter="{x:Null}" />
		</i:EventTrigger>
	</i:Interaction.Triggers>

```

## Stackoverflow with Grouped radio buttons bind to mutual exclusive boolean 

there are two radio buttons, 
```
<StackPanel 
									Orientation="Horizontal">
									<RadioButton 
										Content="Show 2 Buttons" 
										Margin="9,6,7,3" 
										IsChecked="{Binding Show2Buttons}"
										GroupName="ButtonConfig" />
									<RadioButton 
										Content="Show 4 Buttons" 
										Margin="9,6,7,3"
										IsChecked="{Binding Show4Buttons}"
										GroupName="ButtonConfig" />
```

which has the following code behind

```
        public bool Show2Buttons
        {
            get { return _show2Buttons; }

            set
            {
                if (value != _show2Buttons)
                {
                    _show2Buttons = value;
                    RaisePropertyChanged(() => Show2Buttons);
                    RaisePropertyChanged(() => Show4Buttons);
                    Logger.InfoFormat("(OrderTicket-NEW)<Action> Set Button Numbers : {0}", _show2Buttons ? "2" : "4");
                    WidgetTrackingService.NumberOfButtons = value ? 2 : 4;
                    WidgetTrackingService.SaveChanges(_layoutSettingOptionsViewModel.EnableAutoSave);
                }
            }
        }

        public bool Show4Buttons
        {
            get { return !_show2Buttons; }

            set
            {
                Show2Buttons = !value;
            }
        }
```

it will throw StackOverflow exception if you try to change from 2-button mode to 4 button and back..

the solution is to remove the "GroupName" property associated with the radio buttons.


## Interaction.Triggers cannot work if binding to command with default TwoWay binding

I have one command as follow.

`        public ICommand UserActivityCommand { get; set; }
`


and in the view, it is defined as follow.

```
	<i:Interaction.Triggers>

		<i:EventTrigger EventName="PreviewMouseDown">
			<i:InvokeCommandAction Command="{Binding UserActivityCommand}" />
		</i:EventTrigger>
		<i:EventTrigger EventName="PreviewKeyDown">
			<i:InvokeCommandAction Command="{Binding UserActivityCommand}" />
		</i:EventTrigger>
	</i:Interaction.Triggers>
	
```

and however, I clicked and press the key, it always does not trigger the action. 

and finally I found that it is because that I don't add the `OneWay` binding

```
	<i:Interaction.Triggers>

		<i:EventTrigger EventName="PreviewMouseDown">
			<i:InvokeCommandAction Command="{Binding UserActivityCommand, Mode=OneWay}" />
		</i:EventTrigger>
		<i:EventTrigger EventName="PreviewKeyDown">
			<i:InvokeCommandAction Command="{Binding UserActivityCommand, Mode=OneWay}" />
		</i:EventTrigger>
	</i:Interaction.Triggers>
```

it seems that the InvokeCommandAction has inadvently changed something.


## Readonly property back into viewmodel

this is a hot topic where you can channel some Readonly property back to viewmodel


this is how it is implemented via xaml file

```
<Canvas>
    <u:DataPiping.DataPipes>
         <u:DataPipeCollection>
             <u:DataPipe Source="{Binding RelativeSource={RelativeSource AncestorType={x:Type Canvas}}, Path=ActualWidth}"
                         Target="{Binding Path=ViewportWidth, Mode=OneWayToSource}"/>
             <u:DataPipe Source="{Binding RelativeSource={RelativeSource AncestorType={x:Type Canvas}}, Path=ActualHeight}"
                         Target="{Binding Path=ViewportHeight, Mode=OneWayToSource}"/>
          </u:DataPipeCollection>
     </u:DataPiping.DataPipes>
<Canvas>
```
well, and the code behind is as follow.

```
public class DataPiping
{
    #region DataPipes (Attached DependencyProperty)

    public static readonly DependencyProperty DataPipesProperty =
        DependencyProperty.RegisterAttached("DataPipes",
        typeof(DataPipeCollection),
        typeof(DataPiping),
        new UIPropertyMetadata(null));

    public static void SetDataPipes(DependencyObject o, DataPipeCollection value)
    {
        o.SetValue(DataPipesProperty, value);
    }

    public static DataPipeCollection GetDataPipes(DependencyObject o)
    {
        return (DataPipeCollection)o.GetValue(DataPipesProperty);
    }

    #endregion
}

public class DataPipeCollection : FreezableCollection<DataPipe>
{

}

public class DataPipe : Freezable
{
    #region Source (DependencyProperty)

    public object Source
    {
        get { return (object)GetValue(SourceProperty); }
        set { SetValue(SourceProperty, value); }
    }
    public static readonly DependencyProperty SourceProperty =
        DependencyProperty.Register("Source", typeof(object), typeof(DataPipe),
        new FrameworkPropertyMetadata(null, new PropertyChangedCallback(OnSourceChanged)));

    private static void OnSourceChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        ((DataPipe)d).OnSourceChanged(e);
    }

    protected virtual void OnSourceChanged(DependencyPropertyChangedEventArgs e)
    {
        Target = e.NewValue;
    }

    #endregion

    #region Target (DependencyProperty)

    public object Target
    {
        get { return (object)GetValue(TargetProperty); }
        set { SetValue(TargetProperty, value); }
    }
    public static readonly DependencyProperty TargetProperty =
        DependencyProperty.Register("Target", typeof(object), typeof(DataPipe),
        new FrameworkPropertyMetadata(null));

    #endregion

    protected override Freezable CreateInstanceCore()
    {
        return new DataPipe();
    }
}
```

well the reason is that the following won't work because the IsFocusedWithin is on the wrong side of the expression

```
UIElement.IsKeyboardFocusWithin="{Binding IsKeyboardFocusWithin}"
```

Wont' compile, and the following code throw exception at runtime.

```
            Binding isKeyboardFocusedWithinBinding = new Binding();
            isKeyboardFocusedWithinBinding.Path = new PropertyPath("IsKeyboardFocusWithin ");
            isKeyboardFocusedWithinBinding.Mode = BindingMode.OneWayToSource;
            BindingOperations.SetBinding(
                AssociatedObject,
                UIElement.IsKeyboardFocusWithinProperty,
                isKeyboardFocusedWithinBinding);
```

References:
[wpf - Pushing read-only GUI properties back into ViewModel - Stack Overflow](http://stackoverflow.com/questions/1083224/pushing-read-only-gui-properties-back-into-viewmodel)

## Keybinding stop bubbling of events
well, I Have one UI which defines a couple of Keybindings.

here is the code.

```
			<dxg:TableView.InputBindings>

					<KeyBinding 
						Key="Up" 
						Modifiers="Control" 
						Command= "{Binding CtrlUpCommand, ElementName=UserControl}"
						CommandParameter="{Binding ElementName=depthGrid}"/>
					<KeyBinding 
						Key="Down" 
						Modifiers="Control" 
						Command="{Binding CtrlDownCommand, ElementName=UserControl}" 
						CommandParameter="{Binding ElementName=depthGrid}"/>

			</dxg:TableView.InputBindings>
```


and i declared the following Keydown event 

```
<UserControl
	KeyDown="DepthGridKeyDown">

</UserControl>
```

and code behinde 

```
        private void DepthGridKeyDown(object sender, KeyEventArgs e)
        {
            OnKeyDown(e);
            switch (e.Key)
            {
                case Key.F1:
                case Key.F2:
                case Key.F3:
                case Key.F4:
                case Key.F5:
                case Key.F6:
                case Key.F7:
                case Key.F8:
                case Key.F9:
                case Key.F10:
                case Key.F11:
                case Key.F12:
                    e.Handled = true;
                    break;
            }
        }
```

well, if you pressed key in the keybinding collection, then the event will not be called.

It looks like that the Keybinding stop further bubbling of event

which means if you have both Keybinding on the child/parent controls. only the child's event handlers will be responded.


## MarkupExtension, FixupToken, IServiceProvider, IRootObjectProvider and etc...


well, I have one requirement to pass a UserControl instance back to ViewModel, however, the x:Reference tag , ideally if used this way, can suit my need

```

<GridControl
  x:Name="depthGrid">
  <!-- ... -->
<KeyBinding 
	Key="F1"
	Command="{Binding HotKeyCommand}">
	<KeyBinding.CommandParameter>
		<x:Array Type="sys:Object">
		   <x:Reference Name="depthGrid" />
		   <x:Static hotkey:HotKey.F1 />
		</x:Array>
	</KeyBinding.CommandParameter>
</KeyBinding>
<!-- ... -->
</GridControl>
```

well, the new feature is supported with a condition , see 

[WPF Tutorial | What's new in XAML in .NET 4.0](http://wpftutorial.net/XAML2009.html) and [x:Reference Markup Extension](https://msdn.microsoft.com/en-us/library/ee795380(v=vs.110).aspx)


So next I wrote up one MarkupExtension.

My first vesion is 

```
[MarkupExtensionReturnType(typeof(object))]
    public class ElementReferenceMarkupExtension : MarkupExtension
    {
        public ElementReferenceMarkupExtension(string name)
        {
            ElementName = name;
        }

        public ElementReferenceMarkupExtension() { }

        [ConstructorArgument("ElementName")]
        public string ElementName { get; set; }

        public override object ProvideValue(IServiceProvider serviceProvider)
        {

            if (serviceProvider == null) return null;
            if (ElementName == null) return null;

            IXamlNameResolver ixnr = (IXamlNameResolver)serviceProvider.GetService(typeof(IXamlNameResolver));
            object element = ixnr.Resolve(ElementName);
            return element;
            
        }
    }

```

well, Resolve does not always return an valid object, it may returns null and the reason is because XAML actually have several passes of parsing, at the first pass the name is not resolvable.

So after reading the article - [c# - How to create a XAML markup extension that returns a collection - St
ack Overflow](http://stackoverflow.com/questions/8302408/how-to-create-a-xaml-markup-extension-that-returns-a-collection)
. I decided to use `GetFixupToken` method.

```

using System;
using System.Windows;
using System.Windows.Markup;
using System.Xaml;

namespace Utils
{
    
        public override object ProvideValue(IServiceProvider serviceProvider)
        {
            if (serviceProvider == null) return null;
            if (ElementName == null) return null;

            IXamlNameResolver ixnr = (IXamlNameResolver)serviceProvider.GetService(typeof(IXamlNameResolver));
            object element = ixnr.Resolve(ElementName);
            if (element == null)
            {
                if (ixnr.IsFixupTokenAvailable)
                {
                    var fixup = ixnr.GetFixupToken(new[] { ElementName });
                    return fixup;
                }
                
            }
            return element;
    }
}

```

Basically when you return a FixupToken (Internal structure ), the Resolving will coming up again... (like the dispatcher pattern)

however, I am getting the

`MarkupExtension depends on another MarkupExtension` sort of message.

so I am thinking of that when debugging, i saw a `IXamlNameResolver.GetAllNamesAndValuesInScope` which returns a collection and that has name that I wantted. so I am thinking if we can directly Resolve the name with NameScope's help, so here is my solution.

```
        public override object ProvideValue(IServiceProvider serviceProvider)
        {
            var rootProvider = serviceProvider.GetService(typeof(IRootObjectProvider)) as IRootObjectProvider;
            var nameScope = NameScope.GetNameScope(rootProvider.RootObject as DependencyObject);
            return nameScope.FindName(ElementName);

        }
```
and the xaml file looks like below.

```
					<KeyBinding
							Key="F1"
							Command="{Binding HotKeyCommand}">
						<KeyBinding.CommandParameter>
							<x:Array Type="system:Object">
								<extensions:ElementReferenceMarkup ElementName="depthGrid" />
								<x:Static Member="hotkeys:HotKey.F1" />
							</x:Array>
						</KeyBinding.CommandParameter>
					</KeyBinding>
 
```

References:
[c# - How to create a XAML markup extension that returns a collection - St
ack Overflow](http://stackoverflow.com/questions/8302408/how-to-create-a-xaml-markup-extension-that-returns-a-collection)
[Markup extensions with state in WPF - Stack Overflow](http://stackoverflow.com/questions/16107103/markup-extensions-with-state-in-wpf)
[WPF Tutorial | What's new in XAML in .NET 4.0](http://wpftutorial.net/XAML2009.html)
[x:Reference Markup Extension](https://msdn.microsoft.com/en-us/library/ee795380(v=vs.110).aspx)
[Creating a Custom Markup Extension in WPF (and soon, Silverlight) - Pete Brown's 10rem.net](http://10rem.net/blog/2011/03/09/creating-a-custom-markup-extension-in-wpf-and-soon-silverlight)
[MarkupExtension revisited | My Memory](http://putridparrot.com/blog/markupextension-revisited/)
[binding - When is x:Reference in WPF resolved and why does XAML element order affect it? - Stack Overflow](http://stackoverflow.com/questions/14644924/when-is-xreference-in-wpf-resolved-and-why-does-xaml-element-order-affect-it)

## WPF XAML namescopes

You can register part of a visual tree to a Namescope and Style/Template/Resouces has their own XAML namespaces.

Check the references for more details regarding the WPF Xaml namescopes and thei Name-related APIs.

> FrameworkElement also has FindName, RegisterName and UnregisterName methods. If the element owns a name scope, the element methods simply call into the name scope's methods. Otherwise, WPF walks up the (logical) tree looking for the nearest namescope. 

References:
[WPF XAML 名称范围](https://msdn.microsoft.com/zh-cn/library/ms746659(v=vs.110).aspx)
[如何：定义名称范围](https://msdn.microsoft.com/zh-cn/library/ms746609(v=vs.110).aspx)
[What's a name scope? - Nick on Silverlight and WPF - Site Home - MSDN Blogs](http://blogs.msdn.com/b/nickkramer/archive/2006/06/06/618514.aspx)


## PropertyPath revisited

References:
[PropertyPath XAML 语法](https://msdn.microsoft.com/zh-cn/library/ms742451(v=vs.110).aspx)

[Markup Extensions for XAML Overview](https://msdn.microsoft.com/en-us/library/ee855815%28v=vs.110%29.aspx)

[XAML Namespace (x:) Language Features](https://msdn.microsoft.com/en-us/library/ms753327(v=vs.110).aspx)


## Failed to copy, CLIPBRD_E_CANT_OPEN

Recently I have encountered an user report that there is an exception when user  copy data from a clipboard.

```
        private void OrderGrid_OnCopyingToClipboard(object sender, CopyingToClipboardEventArgs e)
        {
            var grid = sender as GridControl;

            if (grid != null && grid.SelectedItems != null && grid.SelectedItems.Count <= 1)
            {
                var column = grid.CurrentColumn as GridColumn;
                if (column != null)
                {
                    //http://stackoverflow.com/questions/12769264/openclipboard-failed-when-copy-pasting-data-from-wpf-datagrid
                    Clipboard.SetText(grid.GetFocusedRowCellDisplayText(column));
                    e.Handled = true;
                }
            }
        }
```


while in xaml , the code is as follow.


```
					<dxg:GridControl 
						gmp:SnapSplitter.CollapseMode="RestrictCollapse"
						ItemsSource="{Binding Orders}"
						SelectedItem="{Binding SelectedItem}"
						CopyingToClipboard="OrderGrid_OnCopyingToClipboard"
						x:Name="orderGrid"
						MaxHeight="5000" 
						MaxWidth="5000"
						SelectionMode="Row"
						gmdx:GridControlScreenUpdateBehaviour.GridControlRowCount="{Binding Orders.Count}">
						<gmdx:GridControlScreenUpdateBehaviour.JumpToLatest>
							<MultiBinding Converter="{StaticResource AndConverter}">
								<Binding Path="EnableScrollToTop" Mode="OneWay" />
								<Binding Path="IsKeyboardFocusWithin" RelativeSource="{RelativeSource Mode=FindAncestor, AncestorType=orderBlotter:OrderBlotter}"  Mode="OneWay" Converter="{StaticResource BoleanInverterConverter}"/>
							</MultiBinding>
						</gmdx:GridControlScreenUpdateBehaviour.JumpToLatest>

					<dxg:GridControl.View>
							<dxg:TableView 
								UseLightweightTemplates="None"
								x:Name="fillView"
								ShowGroupPanel="False"
								ShowIndicator="True"
								AllowEditing="False"
								AlternationCount="2"
								ShowAutoFilterRow="True"
								AlternateRowBackground="{DynamicResource YourDataGridRowAlternateBackgroundBrush}"/>
						</dxg:GridControl.View>

						<i:Interaction.Behaviors>
							<gmdx:GridLayoutManagementBehavior 
								UseIndexerDataSource="False"
							GridDescriptor="{Binding OrderGridDescriptor}"/>
							<gmdx:ExportToExcelBehavior x:Name="ExportToExcelBehavior" />
							<behaviors:ExportBehavior
							ExportToExcelCommand="{Binding ElementName=ExportToExcelBehavior, Path=ExportAllCommand}"
							ViewModel="{Binding}" />
						</i:Interaction.Behaviors>
					</dxg:GridControl>

```

as according to [c# - OpenClipboard Failed when copy pasting data from wpf DataGrid - Stack Overflow](http://stackoverflow.com/questions/12769264/openclipboard-failed-when-copy-pasting-data-from-wpf-datagrid), there is a workaround that to use SetDataObject instead of SetText though no reason is given

I would guess that SetText will do Format conversion and data persisting (IDataObject so that even if application exit, the clipboard is not cleared), while SetDataObject only does the object passing, which has less conflicit with other application.

References:
[c# - OpenClipboard Failed when copy pasting data from wpf DataGrid - Stack Overflow](http://stackoverflow.com/questions/12769264/openclipboard-failed-when-copy-pasting-data-from-wpf-datagrid)
[CLIPBRD_E_CANT_OPEN error when setting the Clipboard from .NET - Stack Overflow](http://stackoverflow.com/questions/68666/clipbrd-e-cant-open-error-when-setting-the-clipboard-from-net)


## how can I exactly construct time stamp of actual time with milliseconds precision?
```
string timestamp = DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss.fff",
                                            CultureInfo.InvariantCulture);
```

References:
[c# - Get DateTime.Now with milliseconds precision - Stack Overflow](http://stackoverflow.com/questions/16032451/get-datetime-now-with-milliseconds-precision)

## DataTemplate  cannot have both DataType and x:Key

well, I defined a data template, and I thought it definitely works.

```
<DataTemplate x:Key="QuickOrderConfigDataTemplate" DataType="{quickorder:QuickOrderViewModel}">
	<!-- content omitted -->
</DataTemplate>
```


well, when I try to use it this way

```
<ContentPresenter Content="{Binding QuickOrderViewModel}" ContentTemplate="{StaticResource QuickOrderConfigDataTemplate}">
</ContentPresenter>

```

when run it, it throws exception.


```
  InnerException: 
       HResult=-2146233088
       Message=Cannot find resource named 'QuickOrderConfigDataTemplate'. Resource names are case sensitive.
       Source=PresentationFramework
       StackTrace:
            at System.Windows.StaticResourceExtension.ProvideValueInternal(IServiceProvider serviceProvider, Boolean allowDeferredReference)
            at System.Windows.StaticResourceExtension.ProvideValue(IServiceProvider serviceProvider)
            at MS.Internal.Xaml.Runtime.ClrObjectRuntime.CallProvideValue(MarkupExtension me, IServiceProvider serviceProvider)
       InnerException: 
```
the exception is rather misleading....

well , it works after I removed the DataType attributes from the DataTemplate configuration.

```
<DataTemplate x:Key="QuickOrderConfigDataTemplate" >
	<!-- content omitted -->
</DataTemplate>
```

## shell:WindowChrome.IsHitVisibleInChrome

well, when my colleague tries to modify the chrome tempate to add some buttons to the chrome. the button is not clickable, well, the reason being that the button does not have the right isHitTest enabled.

to enable it, you will need to add the following statements to the controls.

```
shell:WindowChrome.IsHitTestVisibleInChrome="True"
```



## MultiValueConverterChain

well, a MultiValueConverterChain can chain MultiValueConverters to forms a certain converter chain where first the multi binding can be convertered by the "MultiValueConverter" that it has. then it can further chain the value to the "ValueConverterChain"..

one usage of the MultiValueConverter can be written as follow.

```
<gmp:ValueConverterChain x:Key="BooleanToVisibilityConverterChain">
		        <BooleanToVisibilityConverter/>
	        </gmp:ValueConverterChain>
	        <gmp:MultiValueConverterChain x:Key="MultiAndToVisibilityConverter" MultiValueConverter="{StaticResource AndConverter}" ValueConverterChain="{StaticResource BooleanToVisibilityConverterChain}"/>
```

and then let's see how this is implemented.

```
	/// <summary>
	/// Converter chain which can combine MultiValueConverter and ValueConverterChain for reusability.
	/// </summary>
	public class MultiValueConverterChain : IMultiValueConverter
	{
		/// <summary>
		/// MultiValueConverter used for first convert, can be set in XAML.
		/// </summary>
		public IMultiValueConverter MultiValueConverter { get; set; }

		/// <summary>
		/// ValueConverterChain used for convert after MultiValueConverter, can be set in XAML.
		/// </summary>
		public ValueConverterChain ValueConverterChain { get; set; }

		/// <summary>
		/// Converts source values to a value for the binding target.
		/// MultiValueConverterChain will use the MultiValueConverter to do first convert and then let ValueConverterChain to convert it into final value.
		/// </summary>
		/// <returns>
		/// A converted value. If the method returns null, the valid null value is used.
		/// A return value of <see cref="T:System.Windows.DependencyProperty"/>.<see cref="F:System.Windows.DependencyProperty.UnsetValue"/> indicates that the converter did not produce a value, and that the binding will use the <see cref="P:System.Windows.Data.BindingBase.FallbackValue"/> if it is available, or else will use the default value.A return value of <see cref="T:System.Windows.Data.Binding"/>.<see cref="F:System.Windows.Data.Binding.DoNothing"/> indicates that the binding does not transfer the value or use the <see cref="P:System.Windows.Data.BindingBase.FallbackValue"/> or the default value.
		/// </returns>
		/// <param name="values">The array of values that the source bindings in the <see cref="T:System.Windows.Data.MultiBinding"/> produces. The value <see cref="F:System.Windows.DependencyProperty.UnsetValue"/> indicates that the source binding has no value to provide for conversion.</param>
		/// <param name="targetType">The type of the binding target property.</param>
		/// <param name="parameter">The converter parameter to use.</param>
		/// <param name="culture">The culture to use in the converter.</param>
		public object Convert(object[] values, Type targetType, object parameter, CultureInfo culture)
		{
			if (MultiValueConverter == null)
			{
				throw new InvalidOperationException("MultiValueConverter is not specified!");
			}

			if (ValueConverterChain == null || ValueConverterChain.Converters.Count == 0)
			{
				return MultiValueConverter.Convert(values, targetType, parameter, culture);
			}

			object temp = MultiValueConverter.Convert(values, null, parameter, culture);
			if (temp == Binding.DoNothing || temp == DependencyProperty.UnsetValue)
			{
				return temp;
			}

			return ValueConverterChain.Convert(temp, targetType, parameter, culture);
		}

		/// <summary>
		/// Converts back value to a values for the binding source.
		/// ValueConverterChain is used to convert back first and then MultiValueConverter.
		/// </summary>
		/// <returns>
		/// An array of values that have been converted from the target value back to the source values.
		/// </returns>
		/// <param name="value">The value that the binding target produces.</param>
		/// <param name="targetTypes">The array of types to convert to. The array length indicates the number and types of values that are suggested for the method to return.</param>
		/// <param name="parameter">The converter parameter to use.</param>
		/// <param name="culture">The culture to use in the converter.</param>
		public object[] ConvertBack(object value, Type[] targetTypes, object parameter, CultureInfo culture)
		{
			if (MultiValueConverter == null)
			{
				throw new InvalidOperationException("MultiValueConverter is not specified!");
			}

			if (ValueConverterChain == null || ValueConverterChain.Converters.Count == 0)
			{
				return MultiValueConverter.ConvertBack(value, targetTypes, parameter, culture);
			}

			object temp = ValueConverterChain.ConvertBack(value, null, parameter, culture);
			if (temp == Binding.DoNothing || temp == DependencyProperty.UnsetValue)
			{
				return null;
			}

			return MultiValueConverter.ConvertBack(temp, targetTypes, parameter, culture);
		}
	}

```



## ValueConverterChain

now we will introduce yet another Converter chain, this is now called ValueConverterChain.　First let 's see how this is implemented.

```
private readonly ObservableCollection<IValueConverter> _converters = new ObservableCollection<IValueConverter>();
		private readonly Dictionary<IValueConverter, ValueConversionAttribute> _cachedAttributes = new Dictionary<IValueConverter, ValueConversionAttribute>();

		/// <summary>
		/// Constructor
		/// </summary>
		public ValueConverterChain()
		{
			Converters.CollectionChanged += OnConvertersCollectionChanged;
		}

		/// <summary>
		/// Converters used for converting serially as a chain, can be set as content in XAML.
		/// </summary>
		public ObservableCollection<IValueConverter> Converters
		{
			get { return _converters; }
		}

		/// <summary>
		/// Converts source value to target value for the binding target.
		/// ValueConverterChain executes Convert method from Converters property serially from first to last.
		/// </summary>
		/// <returns>
		/// A converted value. If the method returns null, the valid null value is used.
		/// A return value of <see cref="T:System.Windows.DependencyProperty"/>.<see cref="F:System.Windows.DependencyProperty.UnsetValue"/> indicates that the converter did not produce a value, and that the binding will use the <see cref="P:System.Windows.Data.BindingBase.FallbackValue"/> if it is available, or else will use the default value.A return value of <see cref="T:System.Windows.Data.Binding"/>.<see cref="F:System.Windows.Data.Binding.DoNothing"/> indicates that the binding does not transfer the value or use the <see cref="P:System.Windows.Data.BindingBase.FallbackValue"/> or the default value.
		/// </returns>
		/// <param name="value">The value of the source binding</param>
		/// <param name="targetType">The type of the binding target property.</param>
		/// <param name="parameter">The converter parameter to use.</param>
		/// <param name="culture">The culture to use in the converter.</param>
		public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
		{
			object output = value;

			for (int i = 0; i < Converters.Count; ++i)
			{
				Type currentTargetType = GetTargetType(i, targetType, true);
				output = Converters[i].Convert(output, currentTargetType, parameter, culture);

				// If the converter returns Binding.DoNothing or DependencyProperty.UnsetValue then the binding operation should terminate.
				if (output == Binding.DoNothing || output == DependencyProperty.UnsetValue)
				{
					break;
				}
			}

			return output;
		}

		/// <summary>
		/// Converts back value to a values for the binding source.
		/// ValueConverterChain executes ConvertBack method from Converters property serially from last to first.
		/// </summary>
		/// <returns>
		/// An array of values that have been converted from the target value back to the source values.
		/// </returns>
		/// <param name="value">The value that the binding target produces.</param>
		/// <param name="targetType">The type of the binding source property.</param>
		/// <param name="parameter">The converter parameter to use.</param>
		/// <param name="culture">The culture to use in the converter.</param>
		public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
		{
			object output = value;

			for (int i = Converters.Count - 1; i > -1; --i)
			{
				Type currentTargetType = GetTargetType(i, targetType, false);
				output = Converters[i].ConvertBack(output, currentTargetType, parameter, culture);

				// When a converter returns Binding.DoNothing or DependencyProperty.UnsetValue the binding operation should terminate.
				if (output == Binding.DoNothing || output == DependencyProperty.UnsetValue)
				{
					break;
				}
			}

			return output;
		}

		/// <summary>
		/// Returns the target type for a conversion operation.
		/// </summary>
		/// <param name="converterIndex">The index of the current converter about to be executed.</param>
		/// <param name="finalTargetType">The 'targetType' argument passed into the conversion method.</param>
		/// <param name="convert">Pass true if calling from the Convert method, or false if calling from ConvertBack.</param>
		protected virtual Type GetTargetType(int converterIndex, Type finalTargetType, bool convert)
		{
			// If the current converter is not the last/first in the list, 
			// get a reference to the next/previous converter.
			IValueConverter nextConverter = null;
			if (convert)
			{
				if (converterIndex < Converters.Count - 1)
				{
					nextConverter = Converters[converterIndex + 1];
					if (nextConverter == null)
					{
						throw new InvalidOperationException("The Converters collection of the ValueConverterChain contains a null reference at index: " + (converterIndex + 1));
					}
				}
			}
			else
			{
				if (converterIndex > 0)
				{
					nextConverter = Converters[converterIndex - 1];
					if (nextConverter == null)
					{
						throw new InvalidOperationException("The Converters collection of the ValueConverterChain contains a null reference at index: " + (converterIndex - 1));
					}
				}
			}

			if (nextConverter != null)
			{
				if (_cachedAttributes.ContainsKey(nextConverter))
				{
					ValueConversionAttribute conversionAttribute = _cachedAttributes[nextConverter];

					// If the Convert method is going to be called, we need to use the SourceType of the next 
					// converter in the list.  If ConvertBack is called, use the TargetType.
					return convert ? conversionAttribute.SourceType : conversionAttribute.TargetType;
				}

				return null;
			}

			// If the current converter is the last one to be executed return the target type passed into the conversion method.
			return finalTargetType;
		}

		private void OnConvertersCollectionChanged(object sender, NotifyCollectionChangedEventArgs e)
		{
			// The 'Converters' collection has been modified, so validate that each value converter it now
			// contains is decorated with ValueConversionAttribute and then cache the attribute value.

			IList convertersToProcess = null;
			if (e.Action == NotifyCollectionChangedAction.Add ||
				e.Action == NotifyCollectionChangedAction.Replace)
			{
				convertersToProcess = e.NewItems;
			}
			else if (e.Action == NotifyCollectionChangedAction.Remove)
			{
				foreach (IValueConverter converter in e.OldItems)
				{
					_cachedAttributes.Remove(converter);
				}
			}
			else if (e.Action == NotifyCollectionChangedAction.Reset)
			{
				_cachedAttributes.Clear();
				convertersToProcess = Converters;
			}

			if (convertersToProcess != null && convertersToProcess.Count > 0)
			{
				foreach (IValueConverter converter in convertersToProcess)
				{
					object[] attributes = converter.GetType().GetCustomAttributes(typeof(ValueConversionAttribute), false);

					if (attributes.Length == 1)
					{
						_cachedAttributes.Add(converter, attributes[0] as ValueConversionAttribute);
					}
				}
			}
		}
	}
```


well, the use example would be 

```
            <gmp:ValueConverterChain x:Key="EqualityToVisibilityConverterChain">
                <converters:EqualityToBooleanConverter />
                <BooleanToVisibilityConverter />
            </gmp:ValueConverterChain>
```

this implementation uses of the `ValueConversionAttribute`. which contains the information about `Source`, `Target` type and etc.


## Threading and lock free

while lock is a good way to solve a bunch of issues, it has cost to pay, there is one alternatives that you can uses the dispatching to the same thread to avoid locking.

there are two ways to do the handle one is aggressive: using the Dispatcher and the other is to use _flag (which is passive), you can make one method as the entrent to many a contention code and you can use Flag(Message) to direct what next to go....
e.g.


```
public void CenterData()
{
	_isInitialize = false;
}


public void HandleUpdate(DepthLevelVm vm, DepthLevelDisplay d)
{

	if (_isInitialized) {
		// go to this branch - part I of the conflict
		return;
	}

	// go to this branch - part II of the conflict
}

```


## Traverse Visual tree by example - focus on next sibling

I wrote a Behavior which I hope can set focus to a next sibling. here are the coe

```
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Interactivity;
using System.Windows.Media;
using Utils;
using VisualTreeExtensions = Utils.VisualTreeExtensions;

namespace Behaviors
{
    public class ToolbarTrayFocusBehavior : Behavior<ToolBarTray>
    {

        #region Constructor()

        #endregion


        #region Fields
        #endregion

        #region Behavior 
        protected override void OnAttached()
        {
            base.OnAttached();
            AssociatedObject.KeyDown += AssociatedObjectOnKeyDown;
        }

        protected override void OnDetaching()
        {
            base.OnDetaching();
            AssociatedObject.KeyDown -= AssociatedObjectOnKeyDown;
        }
        #endregion 

        #region Focus (Tabbing)
        
        #region Handler
        private void AssociatedObjectOnKeyDown(object sender, KeyEventArgs e)
        {
            Key key = e.Key;

            if (key == Key.Tab)
            {
                SetNextFocusedItem(e);
            }
        }
        #endregion

        private void SetNextFocusedItem(KeyEventArgs e)
        {
            var eleFocused = Keyboard.FocusedElement as UIElement;
            var shiftDown = Keyboard.IsKeyDown(Key.LeftShift) || Keyboard.IsKeyDown(Key.RightShift);

            NavigateNextToolbar(eleFocused, e, shiftDown);
        }

        private bool NavigateNextToolbar(UIElement eleFocused, KeyEventArgs e, bool shiftDown)
        {
            //var prnt = eleFocused.FindAncestor<ToolBar>();
            if (eleFocused != AssociatedObject)
            {
                if (shiftDown)
                {
                    var prnt = eleFocused.GetParent() as UIElement;

                    UIElement tbr = eleFocused.GetPreviousSibling() as UIElement;
                    if (tbr != null)
                    {
                        if (tbr.IsTabStop() && tbr.Focusable)
                        {
                            return tbr.Focus();
                        }
                    }

                    if (!MoveFocusToLastFocusableChild(prnt))
                        return NavigateNextToolbar(prnt, e, shiftDown);
                }
                else
                {
                    var prnt = eleFocused.GetParent() as UIElement;

                    UIElement tbr = eleFocused.GetNextSibling() as UIElement;
                    while (tbr != null)
                    {
                        if (tbr.IsTabStop() && tbr.Focusable)
                        {
                            return tbr.Focus();
                        }

                        if (tbr.MoveFocusToFirstFocusableChild())
                            return true;
                        
                        tbr = tbr.GetNextSibling() as UIElement;
                    }

                    return NavigateNextToolbar(prnt, e, shiftDown);
                }
            }

            return false;

        }
        

        private UIElement DirectChildTo(UIElement parent, UIElement search)
        {
            var p = search;
            while (p != null)
            {
                p = search.GetParent() as UIElement;
                if (p == parent)
                    return search;
                search = p;
            }

            return null;
        }

        /// <summary>
        /// Move To last focusable child
        /// </summary>
        /// <param name="parent"></param>
        /// <returns></returns>
        public static bool MoveFocusToLastFocusableChild(UIElement parent)
        {
            if (VisualTreeExtensions.IsTabStop((DependencyObject)parent))
                return parent.Focus();
            int childrenCount = VisualTreeHelper.GetChildrenCount((DependencyObject)parent);
            for (int childIndex = childrenCount - 1; childIndex >= 0; --childIndex)
            {
                UIElement parent1 = VisualTreeHelper.GetChild((DependencyObject)parent, childIndex) as UIElement;
                if (parent1 != null && MoveFocusToLastFocusableChild(parent1))
                    return true;
            }
            return false;
        }
        #endregion
    }
}
```


It uses the VisualTreeExtensions, the code is as follow.


```
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Media3D;

usingExtensions;

namespace UI.Utils
{
    /// <summary>
    /// Extension methods container to work with visual elements
    /// </summary>
    public static class VisualTreeExtensions
    {
        /// <summary>
        /// GetParent method that traverses through content elements (as VisualTreeHelper.GetParent throws exception when called over FrameworkContentElement like Run )
        /// </summary>
        /// <param name="obj">target element</param>
        /// <returns>parent of target element</returns>
        public static DependencyObject GetParent(this DependencyObject obj)
        {
            if (obj == null)
            {
                return null;
            }

            var ce = obj as ContentElement;
            if (ce != null)
            {
                DependencyObject parent = ContentOperations.GetParent(ce);
                if (parent != null)
                {
                    return parent;
                }

                var fce = ce as FrameworkContentElement;
                return fce != null ? fce.Parent : null;
            }

            return VisualTreeHelper.GetParent(obj);
        }

        /// <summary>
        /// Finds the ancestor or self.
        /// </summary>
        /// <typeparam name="T">The type to find.</typeparam>
        /// <param name="obj">The dependency object.</param>
        /// <returns>The found type.</returns>
        public static T FindAncestor<T>(this DependencyObject obj) where T : DependencyObject
        {
            while (obj != null)
            {
                var source = obj as T;

                if (source != null)
                {
                    return source;
                }

                obj = GetParent(obj);
            }

            return null;
        }

        public static T FindAncestor<T>(this DependencyObject obj, out DependencyObject[] trace) where T : DependencyObject
        {
            var traceList = new List<DependencyObject>();
            while (obj != null)
            {
                var source = obj as T;

                if (source != null)
                {
                    trace = traceList.AsEnumerable().Reverse().ToArray();
                    return source;
                }

                traceList.Add(obj);
                obj = GetParent(obj);
            }

            trace = null;
            return null;
        }

        public static T FindAncestor<T>(this UIElement obj) where T : UIElement
        {
            return FindAncestor<T>((DependencyObject)obj);
        }

        /// <summary>
        /// Returns top-most parent for given element.
        /// Supports traversing through FrameworkContentElements
        /// </summary>
        /// <param name="obj">target element</param>
        /// <returns>top-most parent</returns>
        public static DependencyObject FindRoot(this DependencyObject obj)
        {
            DependencyObject parent = obj;
            while (parent != null)
            {
                parent = GetParent(obj);
                if (parent != null)
                {
                    obj = parent;
                }
            }

            return obj;
        }

        public static T FindChild<T>(this DependencyObject parent, string childName)
            where T : DependencyObject
        {
            // Confirm parent and childName are valid. 
            if (parent == null)
            {
                return null;
            }

            T foundChild = null;

            int childrenCount = VisualTreeHelper.GetChildrenCount(parent);
            for (var childIndex = 0; childIndex < childrenCount; childIndex++)
            {
                var child = VisualTreeHelper.GetChild(parent, childIndex);

                //// If the child is not of the request child type child
                var childType = child as T;
                if (childType == null)
                {
                    //// recursively drill down the tree
                    foundChild = FindChild<T>(child, childName);

                    //// If the child is found, break so we do not overwrite the found child. 
                    if (foundChild != null)
                    {
                        break;
                    }
                }
                else if (!string.IsNullOrEmpty(childName))
                {
                    var frameworkElement = child as FrameworkElement;

                    //// If the child's name is set for search
                    if (frameworkElement != null && frameworkElement.Name == childName)
                    {
                        //// if the child's name is of the request name
                        foundChild = (T)child;
                        break;
                    }
                }
                else
                {
                    //// child element found.
                    foundChild = (T)child;
                    break;
                }
            }

            return foundChild;
        }

        public static bool IsVisualChildOf(this DependencyObject obj, DependencyObject parent)
        {
            DependencyObject current = obj;
            while (current != parent && current != null)
            {
                current = GetParent(current);
            }

            return current == parent;
        }

        public static AdornerLayer GetAdornerLayer(Visual visual, int layerLevel = 0)
        {
            var adornerLayer = AdornerLayer.GetAdornerLayer(visual);

            if (adornerLayer == null || layerLevel == 0)
            {
                return adornerLayer;
            }

            AdornerLayer parentAdornerLayer;
            do
            {
                parentAdornerLayer = null;
                var layerContainer = adornerLayer.IfNotNull(l => VisualTreeHelper.GetParent(l) as Visual);
                if (layerContainer != null)
                {
                    parentAdornerLayer = AdornerLayer.GetAdornerLayer(layerContainer);
                }

                if (parentAdornerLayer != null)
                {
                    adornerLayer = parentAdornerLayer;
                }

                layerLevel--;
            }
            while (parentAdornerLayer != null && layerLevel != 0);

            return adornerLayer;
        }

        public static bool MoveFocusToFirstFocusableChild(this UIElement parent)
        {
            if (parent.IsTabStop())
            {
                return parent.Focus();
            }

            var childrenCount = VisualTreeHelper.GetChildrenCount(parent);

            for (var i = 0; i < childrenCount; i++)
            {
                var child = VisualTreeHelper.GetChild(parent, i) as UIElement;
                if (child != null && child.MoveFocusToFirstFocusableChild())
                {
                    return true;
                }
            }

            return false;
        }

        #region Code taken from sources of KeyboardNavigation class

        public static DependencyObject GetPreviousSibling(this DependencyObject e)
        {
            DependencyObject parent = e.GetParent();

            // If parent is IContentHost - get next from the enumerator
            var ich = parent as IContentHost;
            if (ich != null)
            {
                IInputElement previousElement = null;
                IEnumerator<IInputElement> enumerator = ich.HostedElements;
                while (enumerator.MoveNext())
                {
                    IInputElement current = enumerator.Current;
                    if (current == e)
                    {
                        return previousElement as DependencyObject;
                    }

                    if (current is UIElement || current is UIElement3D)
                    {
                        previousElement = current;
                    }
                    else
                    {
                        var ce = current as ContentElement;
                        if (ce != null && IsTabStop(ce))
                        {
                            previousElement = current;
                        }
                    }
                }

                return null;
            }
            else
            {
                // If parent is UIElement(3D) - return visual sibling
                DependencyObject parentAsUIElement = parent as UIElement ?? (DependencyObject)(parent as UIElement3D);

                DependencyObject elementAsVisual = e as Visual ?? (DependencyObject)(e as Visual3D);

                if (parentAsUIElement != null && elementAsVisual != null)
                {
                    int count = VisualTreeHelper.GetChildrenCount(parentAsUIElement);
                    DependencyObject prev = null;
                    for (int childIndex = 0; childIndex < count; childIndex++)
                    {
                        DependencyObject vchild = VisualTreeHelper.GetChild(parentAsUIElement, childIndex);
                        if (vchild == elementAsVisual)
                        {
                            break;
                        }

                        if (IsInNavigationTree(vchild))
                        {
                            prev = vchild;
                        }
                    }

                    return prev;
                }
            }

            return null;
        }

        public static DependencyObject GetNextSibling(this DependencyObject e)
        {
            DependencyObject parent = e.GetParent();

            // If parent is IContentHost - get next from the enumerator
            var ich = parent as IContentHost;
            if (ich != null)
            {
                IEnumerator<IInputElement> enumerator = ich.HostedElements;
                bool found = false;
                while (enumerator.MoveNext())
                {
                    IInputElement current = enumerator.Current;
                    if (found)
                    {
                        if (current is UIElement || current is UIElement3D)
                        {
                            return current as DependencyObject;
                        }

                        var ce = current as ContentElement;
                        if (ce != null && IsTabStop(ce))
                        {
                            return ce;
                        }
                    }
                    else if (current == e)
                    {
                        found = true;
                    }
                }
            }
            else
            {
                // If parent is UIElement(3D) - return visual sibling
                DependencyObject parentAsUIElement = parent as UIElement ?? (DependencyObject)(parent as UIElement3D);
                DependencyObject elementAsVisual = e as Visual ?? (DependencyObject)(e as Visual3D);

                if (parentAsUIElement != null && elementAsVisual != null)
                {
                    int count = VisualTreeHelper.GetChildrenCount(parentAsUIElement);
                    int i = 0;

                    // go till itself
                    for (; i < count; i++)
                    {
                        DependencyObject vchild = VisualTreeHelper.GetChild(parentAsUIElement, i);
                        if (vchild == elementAsVisual)
                        {
                            break;
                        }
                    }

                    i++;

                    // search ahead
                    for (; i < count; i++)
                    {
                        DependencyObject visual = VisualTreeHelper.GetChild(parentAsUIElement, i);
                        if (IsInNavigationTree(visual))
                        {
                            return visual;
                        }
                    }
                }
            }

            return null;
        }

        public static bool IsTabStop(this DependencyObject e)
        {
            var fe = e as FrameworkElement;
            if (fe != null)
            {
                return
                    (fe.Focusable
                    && (bool)fe.GetValue(KeyboardNavigation.IsTabStopProperty))
                    && fe.IsEnabled
                    && fe.IsVisible;
            }

            var fce = e as FrameworkContentElement;
            return
                fce != null
                && fce.Focusable
                && (bool)fce.GetValue(KeyboardNavigation.IsTabStopProperty)
                && fce.IsEnabled;
        }

        private static bool IsInNavigationTree(DependencyObject visual)
        {
            var uiElement = visual as UIElement;
            if (uiElement != null && uiElement.IsVisible)
            {
                return true;
            }

            if (visual is IContentHost/* && !(visual is MS.Internal.Documents.UIElementIsland)*/)
            {
                return true;
            }

            var uiElement3D = visual as UIElement3D;
            if (uiElement3D != null && uiElement3D.IsVisible)
            {
                return true;
            }

            return false;
        }

        #endregion
    }
}

```

## P/Invoke to translate mouse position (absolute to  system to application)


well if application does not have focus, it cannot get the mouse location, to get the mouse location (global state), there is a user 32 method but you have to use the p/Invoke to invoke it.



```
    public class MouseLocationProvider : IMouseLocationProvider
    {
        private static readonly ILog Logger = LogManager.GetLogger(MethodBase.GetCurrentMethod().DeclaringType);

        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        internal static extern bool GetCursorPos(ref Win32Point pt);

        [StructLayout(LayoutKind.Sequential)]
        internal struct Win32Point
        {
            public Int32 X;
            public Int32 Y;
        };

        public WindowPosition GetMousePosition()
        {
            try
            {
                var w32Mouse = new Win32Point();
                GetCursorPos(ref w32Mouse);
                var point = new Point(w32Mouse.X, w32Mouse.Y);
                return new WindowPosition(point.Y, point.X);
            }
            catch (Exception exception)
            {
                Logger.ErrorFormat("Failed to get mouse location with execption: {0}. Defaulting to empty", exception.Message);
                return WindowPosition.Empty;
            }
        }
    }
```


## get the default wpf control template in Visual studio 2012

well , you can reference this page :

[Getting the default WPF control templates in Visual Studio 2012 | David Rodrigues Blog](https://djfr.wordpress.com/2012/09/18/getting-the-default-wpf-control-templates-in-visual-studio-2012/)


When designing WPF control templates, one of the most common starting points is the ControlTemplate for that specific control that is shipped with the .Net Framework. By having a dump of that template we can easily start making changes as we go along.

In Visual Studio 2012, the way we get these templates dumped into a code file changed slightly, here’s a tutorial on how to do this.

1. Make a Copy of the control template

In the designer, right click what you want to template, in my example I’m using a Button control. Select Edit Template then select Edit Copy.


Next another windows appears, that let’s you select the name of the template and where exactly do you want to dump it into. In my example I want it on the code-behind file of the control that’s hosting my button (a Window).

2. Go to where you dumped it and start editing

This will assign the “ButtonStyle” template to your Button and will add the template to the Window.Resources tag.

....



## The Current SynchronizationContext may not be used as a TaskScheduler

well, when I try to use the following code 

```
_test_unityContainer.RegisterInstance<ITaskSchedulerService>(TaskSchedulerService.Instance);
```

well, it gives me the error;

```
The Current SynchronizationContext may not be used as a TaskScheduler
```

the key here is to use the following code

```
[SetUp]
protected void SetUp()
{
	SynchronizationContext.SetSynchronizationContext(new SynchronizationContext());
}
```


## Cached Window trick

well, we have an application which create a view but the view creation is heavy so here comes the idea to pre-create the view and make it hidden then on request, bring it back.

here is the code 

```
         // precreate view

        private void PoolCreateOrderTicketView()
        {
            // create an empty Order Ticket view to be used 
            // has to force its display once 
            // so that the UI Element are created 
            // once the Pooled ticket is used, recreate a new Ticket
            _dispatcher.BeginInvoke(DispatcherPriority.ApplicationIdle, new Action(() =>
            {
                var orderTicketViewModel = _container.Resolve<OrderTicketViewModel>();
                // ...


                _cachedRpmTicketWindow = CreateOrderTicketView(ViewSpecifiers.OrderTicket, Guid.NewGuid().ToString(), ViewSpecifiers.OrderTicket, ViewSpecifiers.OrderTicket, orderTicketViewModel, true) as Window;
                if (_cachedRpmTicketWindow !=  null)
                {
                    // ...
                    CachedOrderViews.Add(orderTicketViewModel, _cachedOrderTicketView);

                    _cachedRpmTicketWindow.ShowInTaskbar = false;
                    _cachedRpmTicketWindow.ResizeMode = ResizeMode.CanResizeWithGrip;
                    _cachedRpmTicketWindow.WindowState = WindowState.Minimized;
                    _cachedRpmTicketWindow.Show(); // we need to call show get it UI created.
                    _cachedRpmTicketWindow.Hide();
                    _log.Info("** Rpm - Pool created Order ticket view.");
                }
            }));  
        }
```

and the code that restore it on requested

```

 internal void LaunchRpmTicket(IExecutionTicketVm viewModel, ExecutionTicketLaunchParams launchParams)
        {
            if (_cachedOrderTicketView != null)
            {
                var widget = _cachedOrderTicketView.DataContext as OrderTicketViewModel;
                if (widget != null)
                {
                    // ...
                    if (CachedOrderViews.ContainsKey(widget))
                    {
                        _cachedOrderTicketView = null;

                        var window = _cachedRpmTicketWindow;
                        window.Title = widget.Product;
                        window.ShowInTaskbar = true;
                        //window.Topmost = true;
                        window.Show();
                        window.Activate();
                        window.WindowState = WindowState.Normal;
                        RepositionTicket(window);

                        _cachedRpmTicketWindow = null;
                        PoolCreateOrderTicketView();
                        // remove it 
                        CachedOrderViews.Remove(widget);
                    }
                }
            }
            else
            {
                // cached ticket not yet created
                // LaunchRpmTicketDirect(viewModel, launchParams);
            }
        }

```

##  Dock Panel to align controls in two groups

well, sometimes, you want to align your controls so that it one group at the left and the other group at the right, you can do 


```
<DockPanel LastChidlFill="True" >
	<!-- this is the first group -->
	<StackPanel DockPanel.Dock="Left">
	</StackPanel>

	<!-- now is the second group -->
	<DockPanel DockPanel.Dock="Right">
	</DockPanel>
</DockPanel>


```


## the compiler attributes called CallerMemberName

well, this is a Compiler service, it can cause the compiler to change the value of the parameter on the context of where the method is called within.

```
public event PropertyChangedEventHandler PropertyChanged;

protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null) { 

	PropertyChangedEventHandler handler = PropertyChanged;
	if (handler != null) { 
		handler(this, new PropertyChanged(propertyName);
	}
}

```

given that declaration, you can call by just this

```
private double _size;
public double Size 
{
   get { return _size; } 
   set { if (_size != value) { _size = value; OnPropertyChanged(); } }
}
```

the compiler will help figure out what value (e..g "Name" ) to fill for OnPropertyChanged();


## Style shared resource issues

well, I have a Style defined for Grid Row and the style has the following definition 

```
<Style x:Key="LockSizeButtonStyle" TargetType="ToggleButton" BasedOn="{StaticResource YourToggleButtonStyle}">
        <Style.Triggers>
            <Trigger Property="IsChecked" Value="True">
                <Setter Property="Content">
                    <Setter.Value>
                        <Path Width="13" Height="18" Stretch="Fill" Fill="White"
								      Data="M 752,435.999L 753.999,435.999L 754,432C 754,430.895 754.895,430 756,430L 761,430C 762.104,430 763,430.895 763,432L 762.999,435.999L 765,435.999L 765,447.999L 752,447.999L 752,435.999 Z M 756,438.999L 756,441.999L 758.001,442.001L 758,443.999L 756,443.999L 756,444.999L 761.001,445.001L 761,443.999L 759,443.999L 759,441.999L 761.001,442.001L 761.001,439L 756,438.999 Z M 757,432C 756.447,432 756,432.447 756,433L 756,435.999L 761,435.999L 761,433C 761,432.447 760.552,432 760,432L 757,432 Z " />
                    </Setter.Value>
                </Setter>
                <Setter Property="ToolTip" Value="Unlock Size when Calc Size" />
            </Trigger>
        </Style.Triggers>
        <Setter Property="Content">
            <Setter.Value>
                <StackPanel Orientation="Horizontal">
                    <Path Width="19" Height="18" Stretch="Fill" Fill="White"
							      Data="M 830,436L 830,438L 830,440L 830,448L 817,448L 817,436L 826,436L 826,432C 826,430.896 826.896,430 828,430L 834,430C 835.105,430 836,430.896 836,432L 836,438C 836,439.105 835.105,440 834,440L 833,440L 833,438C 833.552,438 834,437.553 834,437L 834,433C 834,432.448 833.552,432 833,432L 829,432C 828.448,432 828,432.448 828,433L 828,436L 830,436 Z M 821,439L 821,442L 823,442L 823,444L 821,444L 821,445L 826,445L 826,444L 824,444L 824,442L 826,442L 826,439L 821,439 Z " />                   
                </StackPanel>
            </Setter.Value>
        </Setter>
        <Setter Property="ToolTip" Value="Lock Size when Calc Size" />
    </Style>
```
once the style is dynamically applied to many a controls, then the shared state of the style could impact one another...

so the solution that we found is to change the style to the following (in-Style template)

```
	<Style x:Key="LockSizeButtonStyle" TargetType="{x:Type ToggleButton}">
		<Setter Property="FocusVisualStyle" Value="{DynamicResource YourFocusVisualStyle}"/>
		<Setter Property="Template">
			<Setter.Value>
				<ControlTemplate TargetType="{x:Type ToggleButton}">
					<Path 
						x:Name="LockPath" 
						StrokeThickness="0" 
						HorizontalAlignment="Center" 
						VerticalAlignment="Center" 
						SnapsToDevicePixels="True" 
						Data="M 830,436L 830,438L 830,440L 830,448L 817,448L 817,436L 826,436L 826,432C 826,430.896 826.896,430 828,430L 834,430C 835.105,430 836,430.896 836,432L 836,438C 836,439.105 835.105,440 834,440L 833,440L 833,438C 833.552,438 834,437.553 834,437L 834,433C 834,432.448 833.552,432 833,432L 829,432C 828.448,432 828,432.448 828,433L 828,436L 830,436 Z M 821,439L 821,442L 823,442L 823,444L 821,444L 821,445L 826,445L 826,444L 824,444L 824,442L 826,442L 826,439L 821,439 Z " 
						Width="15" 
						Height="15" 
						Stretch="Fill"
						ToolTip="Size unlocked. Click to lock."
						Fill="{DynamicResource IconColorBrush}"/>
					<ControlTemplate.Triggers>
						<Trigger Property="IsChecked" Value="true">
							<Setter Property="Data" TargetName="LockPath" Value="M 752,435.999L 753.999,435.999L 754,432C 754,430.895 754.895,430 756,430L 761,430C 762.104,430 763,430.895 763,432L 762.999,435.999L 765,435.999L 765,447.999L 752,447.999L 752,435.999 Z M 756,438.999L 756,441.999L 758.001,442.001L 758,443.999L 756,443.999L 756,444.999L 761.001,445.001L 761,443.999L 759,443.999L 759,441.999L 761.001,442.001L 761.001,439L 756,438.999 Z M 757,432C 756.447,432 756,432.447 756,433L 756,435.999L 761,435.999L 761,433C 761,432.447 760.552,432 760,432L 757,432 Z "/>
							<Setter Property="ToolTip" TargetName="LockPath" Value="Size locked. Click to unlock."/>
						</Trigger>
					</ControlTemplate.Triggers>
				</ControlTemplate>
			</Setter.Value>
		</Setter>
	</Style>
```


## Get Displayable row count and visible row count

this has been hot that we want to get the VisibleRowCount and Displayable Row Count (in a viewport). the GridControl.VisibleRowCount does not provide what we want.

to get the VisibleRowCount, as per the [E3138 - GridControl - How to get currently visible rows on the screen | DevExpress Support Center](https://www.devexpress.com/Support/Center/Example/Details/E3138), we can get a DataPresenter, and cast it the IScrollInfo object then we get the ViewportHeight, but how to get the DisplayableRowCount?

Here is what I do 

```
        private void SetVisibleRowCount(object sender, EventArgs e)
        {
            if (_dataPresenter != null)
            {
                //VisibleRowCount = AssociatedObject.VisibleRowCount;
                VisibleRowCount = (int)_dataPresenter.ViewportHeight;
                Log.DebugFormat(" -- RowCount = {0}", VisibleRowCount);

                if (VisibleRowCount != 0)
                {
                    // Get ViewportDisplayableRowCount by math
                    // https://www.devexpress.com/Support/Center/Question/Details/T117310
                    // https://www.devexpress.com/Support/Center/Example/Details/E3138
                    var firstVisibleRowHandle = AssociatedObject.GetRowHandleByVisibleIndex(Convert.ToInt32(_dataPresenter.VerticalOffset));
                    if (AssociatedObject.IsValidRowHandle(firstVisibleRowHandle))
                    {
                        var rowControl = AssociatedObject.View.GetRowElementByRowHandle(firstVisibleRowHandle);
                        var dataPresenterDisplayableRowCount = (int)Math.Floor(Convert.ToDouble(((DataPresenter)_dataPresenter).ActualHeight / rowControl.ActualHeight));
                        ViewportDisplayableRowCount = dataPresenterDisplayableRowCount == AssociatedObject.VisibleRowCount ? VisibleRowCount : dataPresenterDisplayableRowCount;
                    }
                }
            }
        }

```

the key here is that we get visible row handle by the (DataPresenter.VerticalOffset and GetRowHandleByVisibleIndex) method. then we can get its RowControl by (View.GetRowElementByRowHandle(rowHanlde)) method .

This being done, then we can do a match (DataPresenter.ActualHeight/RowControl.ActualHeight) to get how many rows the data presenter can display, But wait!!! we want the Viewport displayble row count, so we need to check if data presenter count  == all rows count if it equals, then that means the VisibleRow count is what we can display at most (all visible rows are now in viewport), otherwise, we can just use Data presenter row count.

## Glyph on ToggleButton is hard to click (smaller click area)

I had a Button, which it is declared as follow.

```
<Style x:Key="LockSizeButtonStyle" TargetType="{x:Type ToggleButton}">
		<Setter Property="FocusVisualStyle" Value="{DynamicResource YourFocusVisualStyle}"/>
		<Setter Property="Template">
			<Setter.Value>
				<ControlTemplate TargetType="{x:Type ToggleButton}">
					<Path 
						x:Name="LockPath" 
						StrokeThickness="0" 
						HorizontalAlignment="Center" 
						VerticalAlignment="Center" 
						SnapsToDevicePixels="True" 
						Data="M 830, ... ,439 Z " 
						Width="15" 
						Height="15" 
						Stretch="Fill"
						ToolTip="Size unlocked. Click to lock."
						Fill="{DynamicResource IconColorBrush}"/>
					<ControlTemplate.Triggers>
						<Trigger Property="IsChecked" Value="true">
							<Setter Property="Data" TargetName="LockPath" Value="M 752,..., 432 Z "/>
							<Setter Property="ToolTip" TargetName="LockPath" Value="Size locked. Click to unlock."/>
						</Trigger>
					</ControlTemplate.Triggers>
				</ControlTemplate>
			</Setter.Value>
		</Setter>
	</Style>
```


where the button is used as follow.


```
			<ToggleButton
					VerticalAlignment="Stretch"
					HorizontalAlignment="Stretch"
					Width="30"
					HorizontalContentAlignment="Center"
					IsChecked="{Binding RowData.Row.IsOrderSizeLocked}"
					Style="{StaticResource LockSizeButtonStyle}" />
```
the net result is that sometimes, the button is not clickable unless you place cursor around the path ...

As per the references [wpf - Image Button only responds when clicking on the image and not the area around inside the button - Stack Overflow](http://stackoverflow.com/questions/7541858/image-button-only-responds-when-clicking-on-the-image-and-not-the-area-around-in) , it seems that we need some `<Border>` or `<Grid>` `<StackPanel>` to extend the clickable area.


## Throttle implementation
There are many ways that a throttle can happen, this can happpen if 

1. Two message happens too soon - by checking timestamp
2. There is a burst of message, so by counting the received message, only after received a certain amount of messages, then do throttle
3. By time, this can be periodically timed or ..

Here is Simple solution which is periodically timed...

```
        private int _throttleInterval = 500; // in milliseconds
        private volatile bool _throttleStarted;
        //private DelayTask _throttleTask 
        private readonly CancellationTokenSource _throttleCancellationTokenSource =new CancellationTokenSource();
        private DateTime _lastAnalyticUpdateTimeStamp = DateTime.MinValue;

        private void TrottleUpdateAnalyticData()
        {
            if (!_throttleStarted)
            {
                _throttleStarted = true;
                new DelayTask(TimeSpan.FromMilliseconds(_throttleInterval), _delayTasks).Task.ContinueWith(
                    t => { UpdateAnalyticData(); _throttleStarted = false; },
                    _throttleCancellationTokenSource.Token,
                    TaskContinuationOptions.OnlyOnRanToCompletion, UITaskSchedulerService.Instance.GetUITaskScheduler()
                    ).LogTaskExceptionIfAny(Logger, "Failed on TrottleUpdateAnalyticData!");
            }
        }
```

and updated with Timestamp solution.

```
        private int _throttleInterval = 400; // in milliseconds
        private CancellationTokenSource _throttleCancellationTokenSource = new CancellationTokenSource();
        private DateTime _lastAnalyticUpdateTimeStamp = DateTime.MinValue;
        private TimeSpan _throttleFilterTimespan = TimeSpan.FromMilliseconds(200);
        private volatile bool _hasAnalyticUpdate;

        private void ThrottleUpdateAnalyticData()
        {
            var now = DateTime.Now;
            if (now - _lastAnalyticUpdateTimeStamp > _throttleFilterTimespan)
            {
                Interlocked.Exchange(ref _throttleCancellationTokenSource, new CancellationTokenSource()).Cancel();
                _hasAnalyticUpdate = false;
                UpdateAnalyticData();
            }
            else
            {
                if (!_hasAnalyticUpdate)
                {
                    // flag there is non-executed analyticUdpate pending.
                    _hasAnalyticUpdate = true;
                    // Fire and launch time-out thread
                    new DelayTask(TimeSpan.FromMilliseconds(_throttleInterval), _delayTasks).Task.ContinueWith(
                        t => { UpdateAnalyticData(); _hasAnalyticUpdate = false; },
                        _throttleCancellationTokenSource.Token,
                        TaskContinuationOptions.OnlyOnRanToCompletion,
                        UITaskSchedulerService.Instance.GetUITaskScheduler())
                        .LogTaskExceptionIfAny(Logger, "TrottleUpdateAnalyticData failed!");
                }
            }

            _lastAnalyticUpdateTimeStamp = now;
        }
```


## DeveExpress GridControl may swallow Key

there is one user control which in itself has one GridControl.


Structure is as follow

```
<UserControl>
	<xgrid:GridControl x:Name="TicketGrid">
	</xgrid:GridControl>
</UserControl>
```

now suppose that I want to to listen to the KeyDown/Up event to the TicketGrid, I wrote the followign code 


xaml has this:

```
	<xgrid:GridControl x:Name="TicketGrid" Loaded="DepthGrid_OnLoaded">
	</xgrid:GridControl>
```


```
	private void DepthGrid_OnLoaded(object sender, RoutedEventArgs e)
        {
            if (_viewModel == null)
            {
                return;
            }

            TicketDepth.KeyDown += TicketDepth_OnKeyDown;
            TicketDepth.KeyUp += TicketDepth_OnKeyUp;
        }

        private void TicketDepth_OnKeyDown(object sender, KeyEventArgs e)
        {
            if (_viewModel == null) return;

            if (e.Key == Key.LeftCtrl || e.Key == Key.RightCtrl)
            {
                if (!_isCtrlKeyDown)
                {
                    _viewModel.UpdateCursor();
                    _isCtrlKeyDown = true;
                }
            }
        }

        private void TicketDepth_OnKeyUp(object sender, KeyEventArgs e)
        {
            if (_viewModel == null) return;

            if (e.Key == Key.LeftCtrl || e.Key == Key.RightCtrl)
            {
                _viewModel.UpdateCursor();
                _isCtrlKeyDown = false;
            }
        } 
```

And I have to chagne to this (Added OnLoaded to the UserControl and listen event above there).

```
<UserControl x:Name="OrderTicket">
 ... 
</UserControl>
```

```
        private void OrderTicket_OnLoaded(object sender, RoutedEventArgs e)
        {
            var view = (OrderTicketView)sender;
            if (_viewModel == null)
            {
                _viewModel = (OrderTicketViewModel)view.DataContext;

                view.KeyDown += OrderTicket_OnKeyDown;
                view.KeyUp += OrderTicket_OnKeyUp;
            }
        }

        private void OrderTicket_OnKeyDown(object sender, KeyEventArgs e)
        {
            if (_viewModel == null) return;

            if (e.Key == Key.LeftCtrl || e.Key == Key.RightCtrl)
            {
                if (!_isCtrlKeyDown)
                {
                    _viewModel.UpdateCursor();
                    _isCtrlKeyDown = true;
                }
            }
        }

        private void OrderTicket_OnKeyUp(object sender, KeyEventArgs e)
        {
            if (_viewModel == null) return;

            if (e.Key == Key.LeftCtrl || e.Key == Key.RightCtrl)
            {
                _viewModel.UpdateCursor();
                _isCtrlKeyDown = false;
            }

        }
```

Reason being GridControl may have eaten the Ctrl key....