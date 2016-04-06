## UI Automation Events Overview

### Types of Events
UI Automation events fall intot he following categories

Event | Description   
----|------------------------
Property change | Raised when a property on an UI Automation element or control pattern changes. 
Element Action| Raised when a change in the UI results from end user or programmatic activity; for e.g. button is clicked invoke through InvokePattern or clicked.
strucure change | Raised when the structure of the UI Automation tree changes. , when eleemnt become visible, hidden or removed on the desktop
global desktop change | Raised when action of global interest to the client occurs, such as when focus shift from one to another, or window to window, or window close. 


Beside the folloiwng may raise without the state of the UI change. 

* AutomationPropertyChangedEvent (depending on the property that has changed)
* ElementSelectedEvent
* InvalidatedEvent
* TextChangedEvent


As the proerties identifiers, there are UI automation event identifiers

### UI Automation Event identifiers



Client Identifier | Provider identifier
------------------|-----------------------------
AutomationElement.AsyncContentLoadedEvent | AutomationElementIdentifiers.AsyncContentLoadedEvent
AutomationElement.AutomationFocusChangedEvent | AutomationElementIdentifiers.AutomationFocusChangedEvent
...|...


And the UI automation Event arguments
the following classes encapsulate event argumetns.

Client Identifier | Provider identifier
------------------|-----------------------------
AsyncContentLoadedEventArgs | Contains information about the asynchronous loading of content, including the percentage of loading completed.
AutomationEventArgs | Contains information about a simple event that requires no extra data.
...|...


## References

[UI Automation Events Overview](http://msdn.microsoft.com/en-us/library/ms748252(v=vs.110).asp)
[UI_Automation_Event_Overview]:http://msdn.microsoft.com/en-us/library/ms748252(v=vs.110).aspx