
## UI Automation Tree Overview

UI Automation tree has a root element [RootElement], where each child elemnts represent an applicatin windwo. 
UI Automation tree is not fixed.  The tree supports the UI automation tree by implementing navigation among items within a fragment (consists of root - hosted in a window) and a subtree.


## Views of the Automation Tree

the tree spports "scoping" and "filtering" 

* Scoping is defining the extent of the view, 
*  filtering by defining properties on elements

UI Automation provies three default views. these views are defined by thetype of filtering performed. 

they are 

* Raw view
* Control View
* Content View

### Raw view 

is the full tree of [AutomationElement]

### Control View

Control view simplifies technology products' task od describing to the end user adn helping that end  user interact with the application because it closely maps the UI structure perceived by the end user.

It is a sbuset of the Raw view, it consists of element that interactive or contributing to the logical structure of the control in the UI. 


### Content View

Content view is a subset of the Control view, and it only contains information in a user interface.  including UI items that can receive keyboard focus and some text that is not a label on a UI item. 


## reference

[UI Automation Tree Overvie](http://msdn.microsoft.com/en-us/library/ms741931(v=vs.110).aspx)
[UI_Automation_Tree]: http://msdn.microsoft.com/en-us/library/ms741931(v=vs.110).aspx 
[RootElement]: http://msdn.microsoft.com/en-us/library/ms741931(v=vs.110).aspx
[RootElement](http://msdn.microsoft.com/en-us/library/ms741931(v=vs.110).aspx)
[AutomationElement]:http://msdn.microsoft.com/en-us/library/system.windows.automation.automationelement(v=vs.110).aspx