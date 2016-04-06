## UI Automation Properties Overview

check the original page available [here][UI Automation Properties Overview]

* Property Identifiers
* Properties by Category
* Localization
* Properties and Events
* Related Topics

## Property Identifies
Every Properties is identified by a number and a name, the names  of properties are used only for debugging and diagnostics. the provider and the client is getting property  names from a different assembly.


kind of properties | Client gets ID from | Providers get IDs from 
----------------------|---------------------|------------------------
Properties common to all elements (see following tables) | AutomationElement | AutomationElementIdentifiers
Position of a docking window | DockPattern |DockPatternIdentifiers
State of an element that can expand and collapse | ExpandCollapsePattern | ExpandCollapsePatternIdentifiers
Properties of an item in a grid | GridItemPattern | GridItemPatternIdentifiers
Properties of a grid | GridPattern |GridPatternIdentifiers
... | ... |...

## Properties by Category 

the following tables categorize the properties whose IDs are fond in AutomationElemnet and AutomationElementIdenfiers. 

Properites are likely to be static for the lifetime of the provider application , most dynamic properties are associated with control patterns.

* Display Characteristics
| Property identifier  | Property acccess|
|----------------------|-----------------|
| BoundingRectangleProperty|BoudingRectangle|
|CultureProperty | n/a|
|HelpTextProperty | HepText |
| ... | ... |

* Element type

| Property identifier  | Property acccess|
|----------------------|-----------------|
| ControlTypeProperty|ControlType|
|IsContentElementProperty |IsContentElement |
|IsControlElementProperty | IsControlElement |
| ... | ... |

## Loalization

UI automation providers should present following proerites in teh language of hte operating system:

which is left out because it is not yet too relevant to this discussion

## Properties and Events

Closely tied in with the properties in UI Automation is the concept of property-changed events. For dynamic properties, the client application needs a way to know that a property value has changed, so that it can update its cache of information or react to the new information in some other way.

as A general rule that the provider raise events when something in the UI changes. 


## reference

[UI Automation Properties Overview](http://msdn.microsoft.com/en-us/library/ms752056(v=vs.110).aspx)
[UI Automation Properties Overview]: http://msdn.microsoft.com/en-us/library/ms741931(v=vs.110).aspx 
