
## UI Automation Control Patterns Overview

* UI automation Control pattern Components
* UI Automation Providers and Clients
* Dynamic Control Patterns
* Control Pattern Classes and Interfaces
* Related Topics

## UI Automation Control Pattern Components

WHAT IS A CONTROL PATTERN?
> Control patterns support the methods, properties, events, and relationships needed to define a discrete piece of functionality available in a control.


the properties, events, can be defined in the use of the following categories.

*  relationship between UI automation element and its parent, childre n and sibling .. which describe the **STRUCTURE **
*  methods allow Automation Client to **MANIPULATE** the control
* the properties and events provide information aboutt the control patterns' functinoality as well as the **INFORMATION** about the **STATE** of the control.

> Control patterns relate to UI as interfaces relate to Component Object Model (COM) objects. 

### UI Automation Providers and Clients

what does the UI automation is supposed to do ?

UI Automation providers implement control patterns to expose the appropriate behavior for a specific piece of functionality supported by the control.

### Dynamic Control Patterns
Some controls do not always support the same set of control patterns. Control patterns are considered supported when they are available to a UI Automation client. e.g. For example, a multiline edit box enables vertical scrolling only when it contains more lines of text than can be displayed in its viewable area.

### Control Pattern clases adn Interfaces

Control pattern class | Provider Interface | Description 
----------------------|--------------------|---------------------------------
DockPattern | IDockProvider |Used for controls that can be docked in a docking container. For example, toolbars or tool palettes.
ExpandCollapsePattern |IExpandCollapseProvider | Used for controls that can be expanded or collapsed. For example, menu items in an application such as the File menu.
GridPattern | IGridProvider| Used for controls that support grid functionality such as sizing and moving to a specified cell. For example, the large icon view in Windows Explorer or simple tables without headers in Microsoft Word.
GridItemPattern | IGridItemProvider | Used for controls that have cells within grids. The individual cells should support the GridItem pattern. For example, each cell in Microsoft Windows Explorer detail view.
InvokePattern | IInvokeProvider | Used for controls that can be invoked, such as a button.
... | ... | ... 
## reference

[UI Automation Tree Overvie](http://msdn.microsoft.com/en-us/library/ms741931(v=vs.110).aspx)
[UI_Automation_Tree]: http://msdn.microsoft.com/en-us/library/ms741931(v=vs.110).aspx 
[RootElement]: http://msdn.microsoft.com/en-us/library/ms741931(v=vs.110).aspx
[RootElement](http://msdn.microsoft.com/en-us/library/ms741931(v=vs.110).aspx)
[AutomationElement]:http://msdn.microsoft.com/en-us/library/system.windows.automation.automationelement(v=vs.110).aspx