## RealtimeSource 

Introduction

this README file has the necessary informaiton about the RealtimeSource, which is a data collection which 
1. exonerated/relieve/relieve/pardon/exempt/absolved from the cross thread marshalling
2. can respond to large volume of data in short time (high throughput)

to use the RealTimeSource is quite straightforward, you just need to have create an instance of RealTimeSource and initialize its DataSource with an instance of IBindingList, INotifyCollectionChanged and/or PropertyChanged...

while I have roughly skim over the implementation code and I found that internally it basically has implemented some sort of throttling and I am not sure if it has embedded some heuristic algorithm inside. 

to demonstrate how to use it, here is sample code that guide you through.

First is the data model 

```
  public class Data : INotifyPropertyChanged
  {
    private int _id;

    private string _text;

    private double _progress;

    public event PropertyChangedEventHandler PropertyChanged;


    public int Id
    {
      get
      {
        return _id;
      }

      set
      {
        _id = value;
        NotifyPropertyChanged("Id");
      }
    }

    public string Text
    {
      get
      {
        return _text;
      }

      set
      {
        _text = value;
        NotifyPropertyChanged("Text");
      }
    }

    public double Progress
    {
      get
      {
        return _progress;
      }

      set
      {
        _progress = value;
        NotifyPropertyChanged("Progress");
      }
    }

    public void NotifyPropertyChanged(string name)
    {
      if (PropertyChanged != null)
      {
        PropertyChanged(this, new PropertyChangedEventArgs(name));
      }
    }
  }
  ```
then we build our ViewModel for the view to consume. 

```
  public class MainWindowViewModel : INotifyPropertyChanged
  {
    private ObservableCollection<Data> persons;

    public const int Count = 50;
    private Random Random = new Random();
    public ObservableCollection<Data> Persons
    {
      get
      {
        return persons;
      }
    }

    public MainWindowViewModel()
    {
      persons = new ObservableCollection<Data>();
      for (int i = 0; i < Count; i++)
      {
        persons.Add(new Data()
                      {
                        Id = i, 
                        Text = "Text" + i,
                        Progress =  GetNumber()
                      });
      }

      DispatcherTimer timer = new DispatcherTimer();
      timer.Interval = TimeSpan.FromMilliseconds(1); // fire each every milli-seconds 
      timer.Tick += Tick;
      timer.Start();
    }

    public event PropertyChangedEventHandler PropertyChanged;

    public void NotifyPropertyChanged(string name)
    {
      if (PropertyChanged == null)
      {
        PropertyChanged(this, new PropertyChangedEventArgs(name));
      }
    }

    private void Tick(object sender, EventArgs e)
    {
      int index = Random.Next(0, Count);
      Persons[index].Id = GetNumber();
      Persons[index].Text = "Text" + GetNumber();
      Persons[index].Progress = GetNumber();
    }

    private int GetNumber()
    {
      return Random.Next(0, Count);
    }
  }
  ```
then last we have views and the databinding that drives it works.

```
<Window x:Class="RealtimeSourceExample.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:dxg="http://schemas.devexpress.com/winfx/2008/xaml/grid" 
        xmlns:dxe="http://schemas.devexpress.com/winfx/2008/xaml/editors" 
        xmlns:dx="http://schemas.devexpress.com/winfx/2008/xaml/core" 
        Title="MainWindow" Height="350" Width="525">
    <Grid>
        <dxg:GridControl
          x:Name="grid"
          ItemsSource="{Binding Persons}">
          <dxg:GridControl.Columns>
            <dxg:GridColumn FieldName="Id" />
            <dxg:GridColumn FieldName="Text" />
            <dxg:GridColumn FieldName="Progress">
              <dxg:GridColumn.EditSettings>
                <dxe:ProgressBarEditSettings />
              </dxg:GridColumn.EditSettings>
            </dxg:GridColumn>
          </dxg:GridControl.Columns>
          
          <dxg:GridControl.View>
            <dxg:TableView 
              x:Name="view"
              AutoWidth="True" />
          </dxg:GridControl.View>
        </dxg:GridControl>
    </Grid>
</Window>
```

As you can see that the RealTimeSource is really handy to use.

--
References:

RealTimeSource Class: https://help.devexpress.com/#CoreLibraries/clsDevExpressDataRealTimeSourcetopic
DXGrid - How to use RealTimeSource: https://www.devexpress.com/Support/Center/Example/Details/E4748


##  DataControlBase.CurrentItem and DataControlBase.SelectedItem 

the difference between CurrentItem and SelectedItem are very trivial, below are documentations to the two property respectively. 

[CurrentItem Property - Online Documentation - Developer Express Inc.](https://documentation.devexpress.com/#XAML/DevExpressUIXamlGridDataControlBase_CurrentItemtopic)
[SelectedItem Property - Online Documentation - Developer Express Inc.](https://documentation.devexpress.com/#XAML/DevExpressUIXamlGridDataControlBase_SelectedItemtopic)

Well, from the comment, it has the following. 

> When record multi-selection is disabled, both the CurrentItem and SelectedItem properties refer to the focused record.

> When multi-selection mode is enabled, the CurrentItem property refers to the last selected object (focused record), while the SelectedItem property refers to the first selected object (the first item in the SelectedItems collection).

there is a property called `IsSynchronizedWithCurrentItem` however, this property may not be used by SelectedItem synchronization between the CurrentItem. 

## DevExpress GridControl selection mode

with DevExpress GridControl you can choose different kind of selection mode. among the selection, there are the fews

* Cell
* Row
* None

with Cell or Row selected, you can select multiple Cells or Rows, but Cells has finer grains. 

If you choose None, which means you cannot do multi-selection.


## change the appearance of Selected Rows 

It was recommended by the DevExpress on how to change the appearance of a style. 

```
<Window x:Class="DXGrid_ChangeRowAppearance.Window1" xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" xmlns:dxg="http://schemas.devexpress.com/winfx/2008/xaml/grid" Title="Window1" Height="300" Width="505">
    <Window.Resources>
        <Style x:Key="SelectedRowStyle" TargetType="{x:Type dxg:RowControl}">
            <Style.Triggers>
                <DataTrigger Binding="{Binding Path=IsSelected}" Value="True">
                    <Setter Property="Background" Value="Gray" />
                    <Setter Property="Foreground" Value="White" />
                </DataTrigger>
                <Trigger Property="dxg:GridViewBase.IsFocusedRow" Value="True">
                    <Setter Property="Background" Value="Red" />
                    <Setter Property="Foreground" Value="White" />
                </Trigger>
            </Style.Triggers>
        </Style>
    </Window.Resources>
    <Grid>
        <dxg:GridControl x:Name="grid" AutoGenerateColumns="AddNew" SelectionMode="Row">
            <dxg:GridControl.View>
                <dxg:TableView AutoWidth="True" ShowGroupPanel="False" AllowGrouping="False" RowStyle="{StaticResource SelectedRowStyle}"/>
            </dxg:GridControl.View>
        </dxg:GridControl>
    </Grid>
</Window>
```

while in my code, I only need to change the Focused style to make it something like the Selected Row. Here is my code that does simlar things.

```
		<Style x:Key="RowStyle" TargetType="{x:Type dxg:RowControl}">
			<Setter Property="Foreground" Value="{DynamicResource ForegroundBrush}"/>
			<Setter Property="BorderBrush">
				<Setter.Value>
					<MultiBinding Converter="{StaticResource DepthRowBorderConverter}">
						<Binding ElementName="depthGrid" Path="DataContext" Mode="OneWay"/>
						<Binding Path="RowHandle.Value" Mode="OneWay"/>
					</MultiBinding>
				</Setter.Value>
			</Setter>
      <Style.Triggers>
        <Trigger Property="dxg:GridViewBase.IsFocusedRow" Value="True">
          <Setter Property="Background" Value="{DynamicResource {dxgt:GridRowThemeKey ThemeName=Project_Code, ResourceKey=BorderSelectedBrush}}" />
        </Trigger>
      </Style.Triggers>
		</Style>
    </UserControl.Resources>
```



References:
[How to: Change the Appearance of Selected Rows - Online Documentation - Developer Express Inc.](https://documentation.devexpress.com/#wpf/customdocument7553)


## A freeze issue looking at general the resources...


It has been found that there is  one exception that happens on a very rare conditions. 

the exception is as follow. 

```
Message: 	This Freezable cannot be frozen.
Exception Type: 	System.InvalidOperationException
	
Source Assembly: 	WindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35
Source Type: 	System.Windows.Freezable
Source Method: 	Freeze
	
Application Name: 	Your-App
Command Line: 	"C:\Program Files (x86)\App\Desktop\Installs\your\apps.exe" -Application=Your-App -System=Your:System -Suite=YourSuite -Environment=Development -Instance default -theme YourTHeme -recycle -nomonitor -supportemail=group@app.com

Environment: 	Development
Location: 	Asia.Shanghai
Internal?: 	True
User Credentials: 	credential
	
Aeon Version: 	4.5.1.1

________________________________________
Stack Trace:
at System.Windows.Freezable.Freeze() 
at System.Windows.SystemResources.Freeze(Object resource) 
at System.Windows.SystemResources.FindDictionaryResource(Object key, Type typeKey, ResourceKey resourceKey, Boolean isTraceEnabled, Boolean allowDeferredResourceReference, Boolean mustReturnDeferredResourceReference, Boolean& canCache) 
at System.Windows.SystemResources.FindResourceInternal(Object key, Boolean allowDeferredResourceReference, Boolean mustReturnDeferredResourceReference) 
at System.Windows.FrameworkElement.FindResourceInternal(FrameworkElement fe, FrameworkContentElement fce, DependencyProperty dp, Object resourceKey, Object unlinkedParent, Boolean allowDeferredResourceReference, Boolean mustReturnDeferredResourceReference, DependencyObject boundaryElement, Boolean isImplicitStyleLookup, Object& source) 
at System.Windows.StyleHelper.GetChildValueHelper(UncommonField`1 dataField, ItemStructList`1& valueLookupList, DependencyProperty dp, DependencyObject container, FrameworkObject child, Int32 childIndex, Boolean styleLookup, EffectiveValueEntry& entry, ValueLookupType& sourceType, FrameworkElementFactory templateRoot) 
at System.Windows.StyleHelper.GetChildValue(UncommonField`1 dataField, DependencyObject container, Int32 childIndex, FrameworkObject child, DependencyProperty dp, FrugalStructList`1& childRecordFromChildIndex, EffectiveValueEntry& entry, ValueLookupType& sourceType, FrameworkElementFactory templateRoot) 
at System.Windows.StyleHelper.GetValueFromStyleOrTemplate(FrameworkObject fo, DependencyProperty dp, EffectiveValueEntry& entry) 
at System.Windows.FrameworkElement.GetRawValue(DependencyProperty dp, PropertyMetadata metadata, EffectiveValueEntry& entry) 
at System.Windows.FrameworkElement.EvaluateBaseValueCore(DependencyProperty dp, PropertyMetadata metadata, EffectiveValueEntry& newEntry) 
at System.Windows.DependencyObject.EvaluateEffectiveValue(EntryIndex entryIndex, DependencyProperty dp, PropertyMetadata metadata, EffectiveValueEntry oldEntry, EffectiveValueEntry newEntry, OperationType operationType) 
at System.Windows.DependencyObject.UpdateEffectiveValue(EntryIndex entryIndex, DependencyProperty dp, PropertyMetadata metadata, EffectiveValueEntry oldEntry, EffectiveValueEntry& newEntry, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType) 
at System.Windows.DependencyObject.InvalidateProperty(DependencyProperty dp) 
at System.Windows.StyleHelper.InvalidateResourceDependents(DependencyObject container, ResourcesChangeInfo info, FrugalStructList`1& resourceDependents, Boolean invalidateVisualTreeToo) 
at System.Windows.TreeWalkHelper.InvalidateStyleAndReferences(DependencyObject d, ResourcesChangeInfo info, Boolean containsTypeOfKey) 
at System.Windows.TreeWalkHelper.OnResourcesChanged(DependencyObject d, ResourcesChangeInfo info, Boolean raiseResourceChangedEvent) 
at System.Windows.FrameworkElement.OnAncestorChangedInternal(TreeChangeInfo parentTreeState) 
at System.Windows.TreeWalkHelper.OnAncestorChanged(DependencyObject d, TreeChangeInfo info) 
at System.Windows.DescendentsWalker`1._VisitNode(DependencyObject d) 
at MS.Internal.PrePostDescendentsWalker`1._VisitNode(DependencyObject d) 
at System.Windows.DescendentsWalker`1.VisitNode(FrameworkElement fe) 
at System.Windows.DescendentsWalker`1.VisitNode(DependencyObject d) 
at System.Windows.DescendentsWalker`1.WalkFrameworkElementLogicalThenVisualChildren(FrameworkElement feParent, Boolean hasLogicalChildren) 
at System.Windows.DescendentsWalker`1.IterateChildren(DependencyObject d) 
at System.Windows.DescendentsWalker`1.StartWalk(DependencyObject startNode, Boolean skipStartNode) 
at MS.Internal.PrePostDescendentsWalker`1.StartWalk(DependencyObject startNode, Boolean skipStartNode) 
at System.Windows.TreeWalkHelper.InvalidateOnTreeChange(FrameworkElement fe, FrameworkContentElement fce, DependencyObject parent, Boolean isAddOperation) 
at System.Windows.FrameworkElement.OnVisualParentChanged(DependencyObject oldParent) 
at System.Windows.Media.Visual.FireOnVisualParentChanged(DependencyObject oldParent) 
at System.Windows.Media.Visual.RemoveVisualChild(Visual child) 
at System.Windows.FrameworkElement.set_TemplateChild(UIElement value) 
at System.Windows.StyleHelper.ClearGeneratedSubTree(HybridDictionary[] instanceData, FrameworkElement feContainer, FrameworkContentElement fceContainer, FrameworkTemplate oldFrameworkTemplate) 
at System.Windows.StyleHelper.DoTemplateInvalidations(FrameworkElement feContainer, FrameworkTemplate oldFrameworkTemplate) 
at System.Windows.Controls.ContentPresenter.OnTemplateChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) 
at System.Windows.DependencyObject.OnPropertyChanged(DependencyPropertyChangedEventArgs e) 
at System.Windows.FrameworkElement.OnPropertyChanged(DependencyPropertyChangedEventArgs e) 
at System.Windows.DependencyObject.NotifyPropertyChange(DependencyPropertyChangedEventArgs args) 
at System.Windows.DependencyObject.UpdateEffectiveValue(EntryIndex entryIndex, DependencyProperty dp, PropertyMetadata metadata, EffectiveValueEntry oldEntry, EffectiveValueEntry& newEntry, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType) 
at System.Windows.DependencyObject.SetValueCommon(DependencyProperty dp, Object value, PropertyMetadata metadata, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType, Boolean isInternal) 
at System.Windows.Controls.ContentPresenter.OnContentTemplateChanged(DataTemplate oldContentTemplate, DataTemplate newContentTemplate) 
at System.Windows.Controls.ContentPresenter.OnContentTemplateChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) 
at System.Windows.DependencyObject.OnPropertyChanged(DependencyPropertyChangedEventArgs e) 
at System.Windows.FrameworkElement.OnPropertyChanged(DependencyPropertyChangedEventArgs e) 
at System.Windows.DependencyObject.NotifyPropertyChange(DependencyPropertyChangedEventArgs args) 
at System.Windows.DependencyObject.UpdateEffectiveValue(EntryIndex entryIndex, DependencyProperty dp, PropertyMetadata metadata, EffectiveValueEntry oldEntry, EffectiveValueEntry& newEntry, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType) 
at System.Windows.DependencyObject.SetValueCommon(DependencyProperty dp, Object value, PropertyMetadata metadata, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType, Boolean isInternal) 
at System.Windows.DependencyObject.SetValue(DependencyProperty dp, Object value) 
at DevExpress.Xpf.Docking.VisualElements.BasePanePresenter`2.ChangeTemplate(TLogical item) 
at DevExpress.Xpf.Docking.VisualElements.BasePanePresenter`2.OnContentChanged(Object content, Object oldContent) 
at DevExpress.Xpf.Docking.VisualElements.psvContentPresenter.<.cctor>b__0(DependencyObject dObj, DependencyPropertyChangedEventArgs e) 
at System.Windows.DependencyObject.OnPropertyChanged(DependencyPropertyChangedEventArgs e) 
at System.Windows.FrameworkElement.OnPropertyChanged(DependencyPropertyChangedEventArgs e) 
at System.Windows.DependencyObject.NotifyPropertyChange(DependencyPropertyChangedEventArgs args) 
at System.Windows.DependencyObject.UpdateEffectiveValue(EntryIndex entryIndex, DependencyProperty dp, PropertyMetadata metadata, EffectiveValueEntry oldEntry, EffectiveValueEntry& newEntry, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType) 
at System.Windows.DependencyObject.ClearValueCommon(EntryIndex entryIndex, DependencyProperty dp, PropertyMetadata metadata) 
at System.Windows.DependencyObject.ClearValue(DependencyProperty dp) 
at DevExpress.Xpf.Docking.VisualElements.psvContentPresenter.Dispose() 
at DevExpress.Xpf.Docking.VisualElements.GroupPane.OnDispose() 
at DevExpress.Xpf.Docking.VisualElements.psvContentControl.Dispose() 
at DevExpress.Xpf.Docking.VisualElements.MultiTemplateControl.OnLayoutItemChanged(BaseLayoutItem item) 
at DevExpress.Xpf.Docking.VisualElements.MultiTemplateControl.<.cctor>b__0(DependencyObject dObj, DependencyPropertyChangedEventArgs e) 
at System.Windows.DependencyObject.OnPropertyChanged(DependencyPropertyChangedEventArgs e) 
at System.Windows.FrameworkElement.OnPropertyChanged(DependencyPropertyChangedEventArgs e) 
at System.Windows.DependencyObject.NotifyPropertyChange(DependencyPropertyChangedEventArgs args) 
at System.Windows.DependencyObject.UpdateEffectiveValue(EntryIndex entryIndex, DependencyProperty dp, PropertyMetadata metadata, EffectiveValueEntry oldEntry, EffectiveValueEntry& newEntry, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType) 
at System.Windows.DependencyObject.SetValueCommon(DependencyProperty dp, Object value, PropertyMetadata metadata, Boolean coerceWithDeferredReference, Boolean coerceWithCurrentValue, OperationType operationType, Boolean isInternal) 
at System.Windows.DependencyObject.SetValue(DependencyProperty dp, Object value) 
at DevExpress.Xpf.Docking.BaseLayoutItem.ClearTemplate() 
at DevExpress.Xpf.Docking.DockLayoutManager.DisposeLayoutLayer() 
at DevExpress.Xpf.Docking.DockLayoutManager.OnDispose() 
at DevExpress.Xpf.Docking.VisualElements.psvControl.Dispose() 
at DevExpress.Xpf.Docking.DockLayoutManager.OwnerWindowClosed(Object sender) 
at DevExpress.Xpf.Docking.DockLayoutManager.System.Windows.IWeakEventListener.ReceiveWeakEvent(Type managerType, Object sender, EventArgs e) 
at System.Windows.WeakEventManager.DeliverEventToList(Object sender, EventArgs args, ListenerList list) 
at System.Windows.WeakEventManager.DeliverEvent(Object sender, EventArgs args) 
at System.EventHandler.Invoke(Object sender, EventArgs e) 
at System.Windows.Window.OnClosed(EventArgs e) 
at System.Windows.Window.WmDestroy() 
at System.Windows.Window.WindowFilterMessage(IntPtr hwnd, Int32 msg, IntPtr wParam, IntPtr lParam, Boolean& handled) 
at System.Windows.Interop.HwndSource.PublicHooksFilterMessage(IntPtr hwnd, Int32 msg, IntPtr wParam, IntPtr lParam, Boolean& handled) 
at MS.Win32.HwndWrapper.WndProc(IntPtr hwnd, Int32 msg, IntPtr wParam, IntPtr lParam, Boolean& handled) 
at MS.Win32.HwndSubclass.DispatcherCallbackOperation(Object o) 
at System.Windows.Threading.ExceptionWrapper.InternalRealCall(Delegate callback, Object args, Int32 numArgs) 
at MS.Internal.Threading.ExceptionFilterHelper.TryCatchWhen(Object source, Delegate method, Object args, Int32 numArgs, Delegate catchHandler) 

```

while, the first study shows that when the exception is throwing, the windows is responding to the following windows messages.

•	WM_DEVICECHANGE
•	WM_DISPLAYCHANGE
•	WM_POWERBROADCAST
•	WM_THEMECHANGED
•	WM_SYSCOLORCHANGE
•	WM_SETTINGCHANGE
•	WM_TABLET_ADDED
•	WM_TABLET_DELETED
•	WM_DWMNCRENDERINGCHANGED
•	WM_DWMCOMPOSITIONCHANGED
•	WM_DWMCOLORIZATIONCOLORCHANGED


the message from Leaf Garland is as follow. 


> I cannot recreate the issue on a Win 7 PC yet, I can when remoting into XP and changing the Windows theme (remoting into Win 7 may also trigger the issue, as we have seen it from some IT staff who were WFH).

> I have been able to recreate using the Project_Code-DX theme harness test app, but not using the Project_Code theme showcase app – this suggests that there is something in the resources of the Project_Code-DX theme that triggers the problem. Using the same harness app but without applying our Project_Code-DX theme (i.e, using DX own themes) does not throw the exception.

> The stack trace suggests that this only happens when WPF responds to certain Windows messages:
•	WM_DEVICECHANGE
•	WM_DISPLAYCHANGE
•	WM_POWERBROADCAST
•	WM_THEMECHANGED
•	WM_SYSCOLORCHANGE
•	WM_SETTINGCHANGE
•	WM_TABLET_ADDED
•	WM_TABLET_DELETED
•	WM_DWMNCRENDERINGCHANGED
•	WM_DWMCOMPOSITIONCHANGED
•	WM_DWMCOLORIZATIONCOLORCHANGED

> At which point WPF re-loads all resources and attempts to Freeze them, this is when the exception is thrown.

> This happens in the main thread event loop, outside of any calls into our code so we cannot ‘handle’ the exception directly – and even if we did use an unhandled exception catcher, the resources are in an unknown state so there is not much hope of continuing without restarting the System.Windows.Application. I guess it would be simpler to save any unsaved state and signal a restart via the desktop organizer/coordinator.

> I will continue to see if I can identify what in the Project_Code-DX theme is triggering this.

Later he did more study this is related to the DevExpress or some other code condition combination (RemoteDesk , Windows XP or the DevExpress Thenem loading.


here is the reply that he found and shared with us..

>I narrowed down the parts of the Project_Code-DX theme that seemed to be causing the problems to brushes that were using DynamicResource , e.g.:

> <SolidColorBrush x:Key="{dxnt:CommonElementsThemeKey ResourceKey=GroupForegroundBrush}" Color="{DynamicResource ForegroundColor}" cs:Name="SolidColorBrush_0001" />

> I found this by replacing all the DynamicResources in brushes like the above with DeepPink and made a build of YourApp using this custom theme. I was able to change theme on a remote session into XP without a crash. This suggests that fixing the themes to ensure that all Freezable resources can be frozen (see the WPF docs for what can prevent freezing) will stop the issue. 

>The issue only seems to occur in fairly specific situations – some combination of DevExpress theme loading, XP and/or remote sessions. I suspect it is ultimately a bug in WPF (I can see from the source that it freezes resources without first checking if they can be frozen) but I cannot recreate it with anything smaller than DX components and our DX theme. 

>Note, you might know that WPF will freeze all freezable resources in styles and templates but this is not the same code path. That freezing of resources does check if the resources can be frozen first.

>If we are willing to change the Project_CodeDX themes to prevent this issue then we would need to look at changing all the SolidColorBrush resources that use DynamicResource to set their color property. I have found ~150 SolidColorBrushes that use a DynamicResource. 

>We could replace these with a StaticResource:

><SolidColorBrush x:Key="{dxnt:CommonElementsThemeKey ResourceKey=GroupForegroundBrush}" Color="{StaticResource ForegroundColor}" cs:Name="SolidColorBrush_0001" />

>Or we remove the brush resources and change the references to use a theme brush directly. This has the added benefit of reducing the number of resources in our themes/apps as currently we have many brush resources that are essentially duplicates of theme brushes such as ForegroundBrush.

>Instead of:
<Setter Property="Foreground" Value="{DynamicResource {dxnt:CommonElementsThemeKey ResourceKey=GroupForegroundBrush}}" />

>We could use:
<Setter Property="Foreground" Value="{DynamicResource ForegroundBrush}" />

>People more familiar with the themes would be better placed to decide which option to use.

## DevExpress GridControl handle key events

the background is to handle the cell navigation through simply keyboard actions, such as moving with the Up/Down key to send messsage to coordinating views such as the Quck trade tickets. 

However, GridControl already has its own keyboard handling, which menas you cannot just listen to its OnKeyDown or OnKeyUp, OnPreviewKeyDown event to do your own processing.

actually before I present my solution, it is useful to show you some possible solutions. 

1. sublcass the GridControl or the GridView to handle the key press event manually
2. listen to PreviewKeyDown event and does the processing ourselve.
3. CurrentItemChanged event --- Last selected item 
the problem with 1 is that they are too heavy. 

the problem with 2 is that we don't know what to do with the preview key down event and it is intricate invovles complex handling of the grid controls.

the problem with 3 is that the CurrentItemChanged is fired not on cells? but instead on row handle??? --- haven't verify that...

last I choose the following implementation, I hijack the keyboard event handling on KeyboardKey.Up and KeyboardKey.Down. and I simulate the cell moving with code. 

here is the code. 

to declare to handle the Up/Down event from the xaml code


```
            <KeyBinding
              Key="Down"
              Command="{Binding DownCommand}"
              CommandParameter="{Binding ElementName=depthGrid}"/>
            <KeyBinding
              Key="Up"
              Command="{Binding UpCommand}"
              CommandParameter="{Binding ElementName=depthGrid}" />
```

and the code that does the handling.
```
        public ICommand UpCommand
        {
            get
            {
                return _upCommand;
            }
        }

        public ICommand DownCommand
        {
            get
            {
                return _downCommand;
            }
        }

        private void HandleUp(GridControl grid)
        {
            HandleKeyboardMove(grid, KeyboardKey.Up);
        }

        private void HandleDown(GridControl grid)
        {
            HandleKeyboardMove(grid, KeyboardKey.Down);
        }

        private void HandleKeyboardMove(GridControl grid, KeyboardKey key)
        {
            var tableView = grid.View as TableView;
            if (tableView != null)
            {
                var column = grid.CurrentColumn as GridColumn;
                grid.UnselectAll();
                switch (key)
                {
                    case KeyboardKey.Down:
                        tableView.MoveNextRow();
                        break;
                    case KeyboardKey.Up:
                        tableView.MovePrevRow();
                        break;
                }

                if (column != null)
                {
                    tableView.SelectCell(FocusedDataSourceIndex, column);
                }
            }

            if (UpdateSelectedSingleCell(grid))
            {
                _eventAggregator.GetEvent<DepthKeyPressedEvent>().Publish(new DepthKeyPressedEventArgs
                {
                    KeyboardKey = key,
                    DepthViewerViewModel = this,
                    GridControl = grid
                });
            }
        }

```
the reason the above code to use the GridControl.FocusedColumn is that TableView.GetSelectedCells does not remember which is the last focused one (it returns a list of columns in the coordinate orders). TableView.MovePrevRow() and TableView.MoveNextRow() best describe the handling inside the TableView just with keyboard navigation.  MoveNextRow() and MovePrevRow update the FocusedRowHandle which is bound by the FocusdedDataSourceIndex.

we first clear the selection and then reselect the cell under the FocusedColumn.


References:
[CurrentItem Property - Online Documentation - Developer Express Inc.](https://documentation.devexpress.com/#WPF/DevExpressXpfGridDataControlBase_CurrentItemtopic)
[Getting the Focused Row, Column and Cell in Developer Express XtraGrid](http://support.smartbear.com/viewarticle/63237/)


## DevExpress BeginDataUpdate and EndDataUpdate.


there are two methods (methods pairs) that should be called in sequence in order to flag the being and end of visual update ( to prevent unnecessary visual update during manipulate of data from code behind)

it is like the flood gate which stop first the visual ripples by the data changes and then it open the gate then the data changes flood to the visual to reflect thet changes. 


References:
[BeginDataUpdate Method - Online Documentation - Developer Express Inc.](https://documentation.devexpress.com/#windowsforms/DevExpressXtraGridViewsBaseColumnView_BeginDataUpdatetopic)
[Q93456 - Differences of BeginUpdate/EndUpdate for Grid, GridView and dataset | DevExpress Support Center](https://www.devexpress.com/Support/Center/Question/Details/Q93456)


##  Clear the GridControl's focused row.
You can clear the GridControl's focused row by the following sample code. 

```
 _gridControl.UnselectAll();

                    var count = ((ICollection)((RealTimeSource)_gridControl.ItemsSource).DataSource).Count;

                    for (int i = 0; i < count; i++)
                    {
                        var row = _tableView.GetRowElementByRowHandle(i) as RowControl;
                        if (row != null)
                        {
                            row.SetValue(DataViewBase.IsFocusedRowProperty, false);
                        }
                    }

                    _tableView.FocusedRowHandle = -1;
```

well, this can be simplified to just this code. 

```
_gridControl.UnselectAll();
_tableView.FocusedRowHandle = -1;
```


## AllowCascadeUpdate

AllowCascadeUpdate is a method that allows the cascading update to the TableView. 

the use of Cascading update is that it can move some computation to the background thread, such as when the Grid is doing scrolling, and when the scrolling is happening, there is no need to display the content of the intermediate rows. only when the scrolling is over, then you will like to see the rows coming up. 

From the documentation below. 

> When an end-user scrolls group rows, group summaries can be asynchronously calculated, one after another, in a background thread. To enable asynchronous calculation of group summaries, set the TableView.AllowGroupSummaryCascadeUpdate property to true.

well, you can control what kind of feedback that you can ask the TableView to give back to you.

1. Animation Effect
2. Animation Duration

References:
[Q394723 - TableView.AllowCascadeUpdate | DevExpress Support Center](https://www.devexpress.com/Support/Center/Question/Details/Q394723)
[Cascading Data Updates - Online Documentation - Developer Express Inc.](https://documentation.devexpress.com/#wpf/CustomDocument9787)

## Some tips on improve the performance of GridControl

1 . stop using the type-safe versin of RaisePropertyChanged and use the original RaisePropertyChanged 


you may be Tempted to use the type-safe version of the RaisePropertyChanged event. however, this has some penalty to pay.

the type-safe version of the RaisePropertyChanged handler has to 

	1. compile the lambda expression to Method declaration 
	2. go through the body of the Expression in order to get the name of the property 

So instead of using 
```RaisePropertyChanged(() => PropertyA);```

then we can do 

```RaisePropertyChanged("PropertyA");```

2 . stoping using complicated method accessor and instead by doing that through first doing calculation up-front and 

if the property is read-only once, then we do no have too much improvement, however, if we are looking for extreme high corner improment, we'd better do that..

let's take this for example. 

```

public void MessageUpdate(Message message) {
	_originalProperty = message.getProperty("Original");	
	RaisePropertyChanged("OriginalProperty");
	RaisePropertyChanged("CalculatedProperty");

}
public int CalculatedProperty {
{
get{
  _caculatedProperty = OriginalProperty * factory;
  }
}

public int OringalProperty { 
get { return _originalProperty; } 
}


```

now if we change to that...


```

public void MessageUpdate(Message message) {
	_originalProperty = message.getProperty("Original");	
	_calculatedProperty = _originalProperty * factor;
	RaisePropertyChanged("OriginalProperty");
	RaisePropertyChanged("CalculatedProperty");

}
public int CalculatedProperty {
{
get{
	return _calculatedProperty;
  }
}

public int OringalProperty { 
get { return _originalProperty; } 
}

```

It is not a huge time savier, but if you takes into account if there are many properties, then the savier can be great.

## CopyToClipboard support for the GridControl

You can find there is a CopyToClipboard command that is available from the GridControl .


You can attach some event handlers to that event. Here shows you how you can do that....



```


					<dxg:GridControl 
						gmp:SnapSplitter.CollapseMode="RestrictCollapse"
						ItemsSource="{Binding Orders}"
						CopyingToClipboard="OrderGrid_OnCopyingToClipboard"
						x:Name="orderGrid"
						MaxHeight="5000" 
						MaxWidth="5000"
						SelectionMode="Row">
				</dxg:GridControl>
```

while the implementation of the OrderGird_OnCopyingToClipboard can be implemented as below.

```
private void OrderGRid_OnCopyingToClipboard(object sender, CopyingToClipboardEventArgs e) {

   var grid = sender as GridControl;
   if (grid != null) {

       var column = grid.CurrentColumn as GridColumn;
       if (column != nuoll) 
       {
           Clipboard.SetText(grid.GetFocusedRowCellDisplayText(column));
  	       e.Handled = true;
       }
   }
}
```


## ILayoutAdapter and the use of it.

The ILayoutAdapter is useful when you are constructing the MVVM mode to drive the DockManaqger from DevExpress. 

>  MVVMHelper.LayoutAdapter attached property. This attached property accepts an instance of the ILayoutAdapter interface. ILayoutAdapter contains only one method - Resolve. This method is called for each item in the ItemsSource, and returns the parent group. 


Basically the resolve methods will tell the item in ItemSource which LayoutGroupd the Items should goes to... So it allows delegation to the view level.

Well, here we will present you with one simple implemenation of the ILayoutAdapter. 

    /// <summary>
    /// Adapter for the DevExpress document management control because it doesn't support MVVM pattern very well,
    /// </summary>
    public class DocManagerLayoutAdapter : ILayoutAdapter
    {
        public string DefaultGroupName { get; set; }

        string ILayoutAdapter.Resolve(DockLayoutManager owner, object item)
        {
            return DefaultGroupName;
        }
    }

it basically return the one and the only one - the root panel's name, and from the Xaml, you may find the definition of the Group name as such...

```
  <dxd:DockLayoutManager
       x:Name="dockManager"
       FloatingMode="Desktop"
       IsSynchronizedWithCurrentItem="True"
       ItemsSource="{Binding Documents}"
       Visibility="{Binding IsVisible, Converter={StaticResource BooleanToVisibilityConverter}}">
    <i:Interaction.Behaviors>
      <behaviors:DockLayoutManagerBehaviour
                        Layout="{Binding LayoutXml, Mode=TwoWay}"
                        SelectedDocument="{Binding SelectedDocument, Mode=TwoWay}"
                        LayoutName="{Binding Name}"
                        LayoutLoadComplete="{Binding LoadComplete}"/>
    </i:Interaction.Behaviors>

    <dxd:MVVMHelper.LayoutAdapter>
      <adapters:DocManagerLayoutAdapter DefaultGroupName="PanelHost"/>
    </dxd:MVVMHelper.LayoutAdapter>
    <dxd:LayoutGroup Name="PanelHost"
                     DestroyContentOnTabSwitching="False"
                     DestroyOnClosingChildren="False"/>
  </dxd:DockLayoutManager>
```

well, we can take the step further, by create the LayoutGroup panel if it does not exit, so that we don't need to declare such `<dxd:LayoutGroup Name="PanelHost"... ` any more. here is the code


```
    public class DocManagerLayoutAdapter : ILayoutAdapter
    {
        public string Resolve(DockLayoutManager owner, object item)
        {
            BaseLayoutItem panelHost = owner.GetItem("PanelHost");

            if (panelHost == null)
            {
                panelHost = new LayoutGroup
                {
                    Name = "PanelHost",
                    DestroyOnClosingChildren = true
                };
                owner.LayoutRoot.Add(panelHost);
            }

            return "PanelHost";
        }
    }
```

and from the Xaml, i tis much clearer.

```
    <dxd:DockLayoutManager
        Grid.Row="2"
        FloatingMode="Desktop"
        IsSynchronizedWithCurrentItem="True"
        ItemsSource="{Binding Widgets}"
        Visibility="{Binding IsVisible, Converter={StaticResource BooleanToVisibilityConverter}}">
		<i:Interaction.Behaviors>
            <behaviors:DockLayoutManagerBehavior x:Name="DockManagerBehavior"
                Layout="{Binding LayoutXml, Mode=TwoWay}"
                SelectedWidget="{Binding SelectedWidget, Mode=TwoWay}"
                LayoutName="{Binding Name}"
                AllowChanges="{Binding AllowChanges}"
                LayoutLoadComplete="{Binding LoadComplete}"/>
		</i:Interaction.Behaviors>
		<dxd:MVVMHelper.LayoutAdapter>
            <adapters:DocManagerLayoutAdapter />
		</dxd:MVVMHelper.LayoutAdapter>
		<!-- this is no longer required <dxd:LayoutGroup>
		</dxd:LayoutGroup> -->
	</dxd:DockLayoutManager>
```

References

[Q289940 - Is there an alternative for the IMVVMDockingProperties interface? | DevExpress Support Center](https://www.devexpress.com/Support/Center/Question/Details/Q289940)
[Q523472 - DockLayoutManager ItemsSource MVVM | DevExpress Support Center](https://www.devexpress.com/Support/Center/Question/Details/Q523472)

## LayoutGroup.DestroyOnClosingChilren

Recent there is a vague/obsur/mysterious/esoteric/enigma e bug that when all children are removed, no group driven by MVVM pattern can be added back.


It turns out that the code 

```
    public class DocManagerLayoutAdapter : ILayoutAdapter
    {
        public string Resolve(DockLayoutManager owner, object item)
        {
            BaseLayoutItem panelHost = owner.GetItem("PanelHost");

            if (panelHost == null )
            {
                panelHost = new LayoutGroup
                {
                    Name = "PanelHost",
                    DestroyOnClosingChildren = true
                };
                owner.LayoutRoot.Add(panelHost);
            }


            return "PanelHost";
        }
    }
```

has this "DestroyOnClosingChilren" is set to true. And according to the [DestroyOnClosingChildren Property - Online Documentation - Developer Express Inc.](https://documentation.devexpress.com/#WPF/DevExpressXpfDockingLayoutGroup_DestroyOnClosingChildrentopic)
> Gets or sets whether the current group is destroyed when removing all its children. This is a dependency property.

it means that the LayoutGroup may be destroyed when all the children are removed.  the solution to this problem is to 

```
DestroyOnClosingChildren = false;
``` 

references:
[T137992 - DX DockingManager Serialization Problem | DevExpress Support Center](https://www.devexpress.com/Support/Center/Question/Details/T137992)
[DestroyOnClosingChildren Property - Online Documentation - Developer Express Inc.](https://documentation.devexpress.com/#WPF/DevExpressXpfDockingLayoutGroup_DestroyOnClosingChildrentopic)