## UI Automation of a WPF control Custom control
Microsoft UI Automation provides a single, generalized interface that automation clients can use to examine or operate the user interfaces of a variety of platforms and frameworks. 

WPF's way to automation is to provide the AutomationPeer class.  

## Automation Peer Classes

WPF controls supports UI Automation through a tree of peer classes that derive from AutomationPeer. 

e..g ButtonAutomationPeer is the peer class for the Button contorl classes

## Built-in Automation Peer classes

> Elements implement an automation peer class if they accept interface activity from the user, or if they contain information needed by users of screen-reader applications.


## Peer navaition

**in-process** code can navigate through the peer tree by calling the object's **GetChildren** and **GetParent** methods.  

## Customization in Derived Peer

>All classes that derive from UIElement and ContentElement contain the protected virtual method OnCreateAutomationPeer. WPF calls OnCreateAutomationPeer to get the automation peer object for each control. 


## Override OnCreateAutomationPeer

You can create the your own AutomationPeer and override the custom control so that it returns its own AutomationPeer.

## Override GetPattern

as the OnCreateAutoamtionPeer, the OverideGetPattern shall be implemnted by the custom control implementer.

```
public override object GetPattern(PatternInterface patternInterface)
{
    if (patternInterface == PatternInterface.RangeValue)
    {
        return this;
    }
    return base.GetPattern(patternInterface);
}
```

and other type of implementaion are omiited.


## Override "Core" methods 

Automation code gets information about your contorl by calling public methos of hte peer clases, to provide information about your control, override ach method whose name ends with "Core" when your control implementation is differes from that provided by the base automation peer class.

```
protected override string GetClassNameCore()
{
    return "NumericUpDown";
}

protected override AutomationControlType GetAutomationControlTypeCore()
{
    return AutomationControlType.Spinner;
}
```

Your automation peer should provide approviate default values for your contro, Note the XAML that referenced your control can override your peer implementation by including the AutomationProperties attributes, e.g.
```
<Button AutomationProperties.Name = "Special" AutomationProperties.HelpText="This is a special button" />
```

## Implementing Pattern Providers

The interfaces implemented by a custom provider are explicitly declared if the owning element derives directly from Control. For example, the following code declares a peer for a Control that implements a range value.



```
public class RangePeer1 : FrameworkElementAutomationPeer, IRangeValueProvider { }
```

If the owning control derives from a specific type of control such as RangeBase, the peer can be derived from an equivalent derived peer class.

```
public class RangePeer2 : RangeBaseAutomationPeer { }
```


## Raise Events 

Automation clients can subscribe to automation events, Custom control must report changes to control state by callingthe RaiesAutomationEvent method. , when a property value changes, report RaisePropertyChangedEvent method. 

```
if (AutomationPeer.ListenerExists(AutomationEvents.PropertyChanged))
{
    NumericUpDownAutomationPeer peer = 
        UIElementAutomationPeer.FromElement(nudCtrl) as NumericUpDownAutomationPeer;

    if (peer != null)
    {
        peer.RaisePropertyChangedEvent(
            RangeValuePatternIdentifiers.ValueProperty,
            (double)oldValue,
            (double)newValue);
    }
}
```

## references

[UI Automation of a WPF Custom Control](http://msdn.microsoft.com/en-us/library/cc165614(v=vs.110).aspx)
[UI_Automation_of_a_WPF_Custom Control]:http://msdn.microsoft.com/en-us/library/cc165614(v=vs.110).aspx
[AutomationPeer](http://msdn.microsoft.com/en-us/library/system.windows.automation.peers.automationpeer(v=vs.110).aspx)
[AutomationPeer]: http://msdn.microsoft.com/en-us/library/system.windows.automation.peers.automationpeer(v=vs.110).aspx