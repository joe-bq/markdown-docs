
## UI Automation Overview
Microsoft UI Automation is the new accessibility framework for Microsoft Windows, available on all operating systems that support Windows Presentation Foundation (WPF).

## Joe's note on the UIAutomation
the UI automation can help in the unit test to simuate some user action while that can help to improve assertion on the correctness of the Controls that user wrote.

## Architecture 
according to the [UI Automation Overview][UI_Automation_Overview], the UI automation masks any difference in the frameworks that underlie various pieces of UI. 

an example is that, the Content property of a WPF button , the Caption property of Win32 button, the ALT property of an HTML image are all mapped to a single property, Name, in the UI automation view.


### Providers and Clients

it has four components, and the component are list below. 

Component | Description
----|-----
Provider API (UIAutomationProvider.dll and UIAutomationTypes.dll) | A set of interface definitions that are implemented by UI Automation providers, objects that provide information about UI elements and respond to programmatic input.
Client API (UIAutomationClient.dll and UIAutomationTypes.dll) | A set of types for managed code that enables UI Automation client applications to obtain information about the UI and to send input to controls.
UiAutomationCore.dll | The underlying code (sometimes called the UI Automation core) that handles communication between providers and clients.
UIAutomationClientsideProviders.dll | A set of UI Automation providers for standard legacy controls. (WPF controls have native support for UI Automation.) This support is automatically available to client applications.


#### To use the UI automation 

to ways 

* create supports for custom controls
* create application that use UI automation core to communicate with the UI elements. 


there are more to check on the matter of topics

Section | Matter
----|-----
[UI Automation Fundamentals](http://msdn.microsoft.com/en-us/library/ms753107(v=vs.110).aspx) | Broad overviews of the concepts.
[UI Automation Providers for Managed Code](http://msdn.microsoft.com/en-us/library/ms747229(v=vs.110).aspx) | Overviews and how-to topics to help you use the provider API.
[UI Automation Clients for Managed Code](http://msdn.microsoft.com/en-us/library/ms753326(v=vs.110).aspx) | Overviews and how-to topics to help you use the client API..
[UI Automation control Patterns](http://msdn.microsoft.com/en-us/library/ms743073(v=vs.110).aspx) | nformation about how control patterns should be implemented by providers, and what functionality is available to clients.
[UI Automation Text Pattern](http://msdn.microsoft.com/en-us/library/ms752280(v=vs.110).aspx) | Information about how the Text control pattern should be implemented by providers, and what functionality is available to clients.
[UI Automation Control types](hhttp://msdn.microsoft.com/en-us/library/ms743581(v=vs.110).aspx) | Information about the properties and control patterns supported by different control types.


### UI Automation Model 

UI Automation exposes every piece of the UI to client applications as an [AutomationElement]. Elements are contained in a tree structure, with the desktop as the root element. Clients can filter the raw view of the tree as a control view or a content view. Applications can also create custom views.

[[AutomationElement] expose common properties they represent.

#### control type and control patterns

control pattern example:  one control pattern to represent the ability to expand and collapse; another to represent the selectoin mechanism.

## References 
[UI_Automation_Overview]:http://msdn.microsoft.com/en-us/library/ms747327(v=vs.110).aspx
[UI Automation Overview](http://msdn.microsoft.com/en-us/library/ms747327(v=vs.110).aspx)
[AutomationElement]: http://msdn.microsoft.com/en-us/library/system.windows.automation.automationelement(v=vs.110).aspx
[AutomationElement](AutomationElement)
