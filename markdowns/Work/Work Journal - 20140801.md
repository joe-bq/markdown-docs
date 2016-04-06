## the inplace (non-adorned element) ComboBox style 

```
<Style
                x:Key="NeedAttentionComboBoxStyle"
                TargetType="ComboBox">
                <Setter Property="SnapsToDevicePixels" Value="true" />
                <Setter Property="OverridesDefaultStyle" Value="true" />
                <Setter Property="ScrollViewer.HorizontalScrollBarVisibility" Value="Auto" />
                <Setter Property="ScrollViewer.VerticalScrollBarVisibility" Value="Auto" />
                <Setter Property="ScrollViewer.CanContentScroll" Value="true" />
                <!--Setter Property="MinWidth" Value="60" /-->
                <!--Setter Property="MinHeight" Value="22"/-->
                <Setter Property="BorderThickness" Value="1" />
                <Setter Property="Background" Value="{DynamicResource DefaultControlBackgroundBrush}"/>
                <Setter Property="Foreground" Value="{DynamicResource ForegroundBrush}"/>
                <Setter Property="FocusVisualStyle" Value="{DynamicResource YourOrganizationFocusVisualStyle}"/>

                <Setter Property="Template">
                    <Setter.Value>
                        <ControlTemplate TargetType="{x:Type ComboBox}">
                            <Grid>
                            <Grid Width="Auto">
                                <VisualStateManager.VisualStateGroups>
                                    <VisualStateGroup x:Name="CommonStates">
                                        <VisualState x:Name="Normal" />
                                        <VisualState x:Name="MouseOver" />
                                        <VisualState x:Name="Disabled"/>
                                    </VisualStateGroup>
                                    <VisualStateGroup x:Name="EditStates">
                                        <VisualState x:Name="Editable">
                                            <Storyboard>
                                                <ObjectAnimationUsingKeyFrames
                                                      Storyboard.TargetProperty="(UIElement.Visibility)"
                                                      Storyboard.TargetName="PART_EditableTextBox">
                                                    <DiscreteObjectKeyFrame
                                                        KeyTime="0"
                                                        Value="{x:Static Visibility.Visible}" />
                                                </ObjectAnimationUsingKeyFrames>
                                                <ObjectAnimationUsingKeyFrames
                                                      Storyboard.TargetProperty="(UIElement.Visibility)"
                                                      Storyboard.TargetName="ContentSite">
                                                    <DiscreteObjectKeyFrame
                                                        KeyTime="0"
                                                        Value="{x:Static Visibility.Hidden}" />
                                                </ObjectAnimationUsingKeyFrames>
                                            </Storyboard>
                                        </VisualState>
                                        <VisualState x:Name="Uneditable" />
                                    </VisualStateGroup>
                                </VisualStateManager.VisualStateGroups>
                                <ToggleButton
                                    x:Name="ToggleButton"
			                        BorderThickness="{TemplateBinding BorderThickness}"
			                        Background="{TemplateBinding Background}"
                                    Template="{StaticResource YourOrganizationComboBoxToggleButtonStyle}"
                                    Grid.Column="2"
                                    Focusable="false"
                                    ClickMode="Press"
                                    IsChecked="{Binding IsDropDownOpen, Mode=TwoWay, RelativeSource={RelativeSource TemplatedParent}}"/>
                                <ContentPresenter
                                  x:Name="ContentSite"
                                  IsHitTestVisible="False"
                                  Content="{TemplateBinding SelectionBoxItem}"
                                  ContentTemplate="{TemplateBinding SelectionBoxItemTemplate}"
                                  ContentTemplateSelector="{TemplateBinding ItemTemplateSelector}"
                                  Margin="5,4,23,3"
                                  VerticalAlignment="Stretch"
                                  HorizontalAlignment="Left"/>
                                <TextBox
                                  x:Name="PART_EditableTextBox"
                                  Style="{x:Null}"
                                  Template="{StaticResource YourOrganizationComboBoxTextBoxStyle}"
                                  HorizontalAlignment="Left"
                                  VerticalAlignment="Bottom"
                                  Margin="3,4,23,3"
                                  Focusable="True"
                                  Background="Transparent"
                                  Visibility="Hidden"
                                  IsReadOnly="{TemplateBinding IsReadOnly}"
                                  Foreground="{DynamicResource ForegroundBrush}"
                                  CaretBrush="{DynamicResource ForegroundBrush}"
                                  SelectionBrush="{DynamicResource SelectionBrush}" />
                                <Popup
                                  x:Name="Popup"
                                  Placement="Bottom"
                                  IsOpen="{TemplateBinding IsDropDownOpen}"
                                  AllowsTransparency="True"
                                  Focusable="False"
                                  PopupAnimation="Slide">
                                    <Grid
                                    x:Name="DropDown"
                                    SnapsToDevicePixels="True"
                                    MinWidth="{TemplateBinding ActualWidth}"
                                    MaxHeight="{TemplateBinding MaxDropDownHeight}"
                                    Margin="0,2,0,0">
                                        <Border
                                          x:Name="DropDownBorder"
                                          BorderThickness="1"
                                          Background="{DynamicResource DefaultControlBackgroundBrush}"
                                          BorderBrush="{DynamicResource DefaultBorderBrush}"/>
                                        <ScrollViewer
                                          SnapsToDevicePixels="True"
                                          Template="{DynamicResource YourOrganizationScrollViewerControlTemplate}"
                                          Margin="1,3,1,1">
                                            <StackPanel
                                                IsItemsHost="True"
                                                KeyboardNavigation.DirectionalNavigation="Contained" />
                                        </ScrollViewer>
                                    </Grid>
                                </Popup>
                            </Grid>
                                <Grid
                                    x:Name="InvalidBorderValidationGrid"
                                    Visibility="Collapsed">
                                    <Path x:Name="InvalidWhiteSlash" Width="12" Height="12" Stretch="Fill" Fill="#FFFFFFFF" Data="F1 M 12,12.0001L -2.11357e-005,0.00012207L 11.9988,0.00012207L 12,12.0001 Z " HorizontalAlignment="Right" VerticalAlignment="Top"/>
                                    <Path x:Name="InvalidRedCorner" Width="12" Height="12"  Stretch="Fill" Fill="{DynamicResource InvalidBorderBrush}" Data="M 12,12L -2.11357e-005,0L 11.9988,0L 12,12 Z M 9.99996,8.00012L 9.99996,5.00012L 6.99996,2.00012L 3.99997,2.00012L 9.99996,8.00012 Z " HorizontalAlignment="Right" VerticalAlignment="Top"/>
                                    <Rectangle HorizontalAlignment="Left" VerticalAlignment="Stretch" Width="1" Fill="{DynamicResource InvalidBorderBrush}"/>
                                    <Rectangle HorizontalAlignment="Right" VerticalAlignment="Stretch" Width="1" Fill="{DynamicResource InvalidBorderBrush}"/>
                                    <Rectangle VerticalAlignment="Top" HorizontalAlignment="Stretch" Height="1" Fill="{DynamicResource InvalidBorderBrush}"/>
                                    <Rectangle VerticalAlignment="Bottom" HorizontalAlignment="Stretch" Height="1" Fill="{DynamicResource InvalidBorderBrush}"/>
                                </Grid>
                            </Grid>
                            <ControlTemplate.Triggers>
                                <Trigger Property="HasItems" Value="False">
                                    <Setter TargetName="DropDownBorder" Property="MinHeight" Value="95" />
                                </Trigger>
                                <Trigger Property="IsGrouping" Value="true">
                                    <Setter Property="ScrollViewer.CanContentScroll" Value="false" />
                                </Trigger>
                                <Trigger SourceName="Popup" Property="AllowsTransparency" Value="true">
                                    <Setter TargetName="DropDownBorder" Property="Margin" Value="0,2,0,0" />
                                </Trigger>
                                <Trigger Property="IsEnabled" Value="false">
                                    <Setter Property="Foreground" Value="{DynamicResource DisabledForegroundBrush}"/>
                                    <Setter Property="Foreground" TargetName="PART_EditableTextBox" Value="{DynamicResource DisabledForegroundBrush}"/>
                                </Trigger>
                                <DataTrigger Binding="{Binding HasError}" Value="true">
                                    <Setter Property="Visibility" Value="Visible" TargetName="InvalidBorderValidationGrid" />
                                </DataTrigger>
                            </ControlTemplate.Triggers>
                        </ControlTemplate>
                    </Setter.Value>
                    </Setter>
                <Setter Property="UseLayoutRounding" Value="True"/>
            </Style>
```


## Readonly Collection 

this can be used in place where the readonly string array should be used. 

        public static readonly ReadOnlyCollection<string> Instances = new ReadOnlyCollection<string>(
            new []
            {
                DefaultInstance, "Asia", "America"
            });
            
            
            
this is better than this 
```
public string[] Instances = {
                DefaultInstance, "Asia", "America"
            };
            
```

because this you can still do the following .


```
Instances[0] = "Hello";
```

Or better, youc can do the following



```
    private static readonly IList<string> myArrayReadOnly = Array.AsReadOnly(myArray);

```

## IDataErrorInfo and the INotifyDataErrorInfo and ValidationRule

One is that the IDataInfo does synchronouse validation error, while with the INotifyDataErrorINfo, you can do even further with the Asynchronous Data validation.


There is a validation rule class, which does the validation on the binding on a separate class, which is ideal in case where you want to make a common validation logics.


## tools - Responsive  XAML editor

you can enable responsive XAML editor, by the the followig two was

1. Set Source Code (Text) Editor Default
![Set_Default](http://blog.lebosquain.net/wp-content/uploads/2012/08/VsOpenWithSetAsDefault.png)

2. Editing Faster

change `HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\VisualStudio\10.0\Languages\Language Services\XAML  ` the value `CodeSenhse` from `1` to `0`

References:
[Responsive XAML editing with ReSharper](http://blog.lebosquain.net/2012/08/responsive-xaml-editing-with-resharper/)

## Window on top

within C#, you can make a window on top with the following proeprty 


```
Window.TopMost = true;
```



## Template binding binding with relative source.

TemplateParent is a relatively lightweight binding on the properties. You can replace TemplateBinding with Binding (a derived class to BindingBase). 

I have a use case which uses Binding vs. Template binding which you might be interested to find out details.

I have a ViewModel named "GlobalFilterSummaryViewModel", and I have one data template directing how to render it . 

here is the code. 

```
    <DataTemplate
        DataType="{x:Type viewModels:GlobalFilterSummaryViewModel}">
        <Grid>
            <Grid
                ClipToBounds="False"
                x:Name="filterGrid">
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="*" />
                    <ColumnDefinition Width="Auto" MinWidth="24" />
                </Grid.ColumnDefinitions>
                <TextBlock
                  Grid.Column="0"
                  Margin="2,0,0,0"
                  Style="{StaticResource TextBlockStyle}"
                  Text="{Binding Filter}"
                  TextTrimming="CharacterEllipsis"
                  TextWrapping="NoWrap"
                  VerticalAlignment="Center">
                </TextBlock>
                <ToggleButton
                   Grid.Column="1"
                   x:Name="more" 
                   Visibility="Visible"
                   Opacity="0"
                   Command="{Binding ShowOrHideDetailCommand}"
                   Style="{StaticResource GlobalFilterGlyphButtonStyle}"/>
            </Grid>
            <Popup
                x:Name="popup"
                IsOpen="{Binding IsOpen}"
                HorizontalOffset="{TemplateBinding ActualWidth, Converter={StaticResource AddConverter}, ConverterParameter={StaticResource OffSetValue}"
                Placement="Left"
                MinHeight="300"
                MaxHeight="600"
                MinWidth="500"
                MaxWidth="500">
                <Border 
                   <!-- ... -->
                </Border>
                            </Grid>
                        </Grid>
                    </Border>
                </Border>
            </Popup>
        </Grid>
        <DataTemplate.Triggers>
            <!-- ... -->
        </DataTemplate.Triggers>
    </DataTemplate>
```

As you can see there is a converter inside the `Popup` tag. And that binds to the outside `DataTemplate` . you might be tempted to do this 

```
<Popup
                x:Name="popup"
                IsOpen="{Binding IsOpen}"
                VerticalOffset="{TemplateBinding ActualWidth, Converter={StaticResource AddConverter}, ConverterParameter={StaticResource OffSetValue}"
                Placement="Left"
                MinHeight="300"
                MaxHeight="600"
                MinWidth="500"
                MaxWidth="500">
                <Popup
                x:Name="popup"
                IsOpen="{Binding IsOpen}"
                HorizontalOffset="{TemplateBinding ActualWidth, Converter={StaticResource AddConverter}, ConverterParameter={StaticResource OffSetValue}"
                Placement="Left"
                MinHeight="300"
                MaxHeight="600"
                MinWidth="500"
                MaxWidth="500">
                <Popup.HorizontalOffset>
                    <MultiBinding Converter="{StaticResource MultAddConverter}">
                        <TemplateBindingExtension Property="ActualWidth" />
                        <Binding Path="{x:Static OffsetValue}" />
                    </MultiBinding>
                </Popup>
</Popup>                
```

There is a compilation error because the TemplateBindingExtension is not a instance of the `BindingBase`.

Then you might be changing to this:

```
<Popup
                x:Name="popup"
                IsOpen="{Binding IsOpen}"
                VerticalOffset="{TemplateBinding ActualWidth, Converter={StaticResource AddConverter}, ConverterParameter={StaticResource OffSetValue}"
                Placement="Left"
                MinHeight="300"
                MaxHeight="600"
                MinWidth="500"
                MaxWidth="500">
                <Popup
                x:Name="popup"
                IsOpen="{Binding IsOpen}"
                HorizontalOffset="{TemplateBinding ActualWidth, Converter={StaticResource AddConverter}, ConverterParameter={StaticResource OffSetValue}"
                Placement="Left"
                MinHeight="300"
                MaxHeight="600"
                MinWidth="500"
                MaxWidth="500">
                <Popup.HorizontalOffset>
                    <MultiBinding Converter="{StaticResource MultAddConverter}">
                        <Binding RelativeSource={RelativeSource Mode=FindAcestor, Level=2, AncestorType=Control}" Path="ActualWidth" />
                        <Binding Path="{x:Static OffsetValue}" />
                    </MultiBinding>
                </Popup>
</Popup>      

```
 you can see that it complains that `GlobalFilterSummaryViewModel` do not have the `ActualWidth` property.


this uses an example to show you the difference bewteen using a TemplateBinding and the Binding (general)

## DependencyProperty.UnsetValue 
the UnsetValue is a value when 

1. binding fail to find the appropriate source property
2. binding error?
3. just UnsetValue - default value ..


## default Event handler / value 

it is common that you use the invoke pattern
```
public event EventHandler SampleEvent;

var sampleEvent = SampleEvent;
if (sampleEvent != null)
{
    sampleEvent(this, EventArgs.Empty);
}
```

while that is tedious, what you can is to give it an default value such as the following. 


```
public event EventHandler SampleEvent = (o, e) => {};

// now it becomes easiler just to do the following. 
SampleEvent(this, EventArgs.Empty);
```

A special note is that the owner of the event should guarantee that this event never get nullified.

## Code snippet to consolidate the layout report
there is a code nsippet that to deal with the layout report. 

```
        public IEnumerable<LayoutReportItem> GetLayoutReports()
        {
            var reports = _layoutReportsProvider.Single();

            var layoutNames = GetNames();
            var reportCollection = reports != null ? reports.Items.ToList() : new List<LayoutReportItem>();
            var reportsNames = reportCollection.Select(x => x.Name).ToArray();
            reportCollection.RemoveAll(x => !layoutNames.Contains(x.Name));

            reportCollection.AddRange(
                layoutNames.Except(reportsNames)
                    .Select(
                        name =>
                        new LayoutReportItem()
                            {
                                Name = name,
                                UseCount = 0,
                                LastAccessTime = DateTimeExtensions.Epoch,
                                CreateTime = DateTimeExtensions.Epoch
                            }));

            return reportCollection;
        }
```

