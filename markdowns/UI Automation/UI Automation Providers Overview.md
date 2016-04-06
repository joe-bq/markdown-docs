
## UI Automation Providers Overview

UI Automation providers enable controls to communicate with UI Automation client applications. 

Client applications do not usually have to work directly with providers. Most of the standard controls in applications that use the Win32, Windows Forms, or Windows Presentation Foundation (WPF) frameworks are automatically exposed to the UI Automation system.  While, if you are working with custom control, then it is desirable to provide some UI Automation providers for those controls ( sot hat client application doe not have to take any special steps to gain access to them)

* Types of Poviders
* UI Automation Provider Concepts
* Related Topics

## Types of Providers

### Client-side Providers
> Because UI Automation providers for controls in Win32, Windows Forms, or WPF applications are supplied as part of the operating system, client applications seldom have to implement their own providers, a

### Server-side providers

> Server-side providers are implemented by custom controls or by applications that are based on a UI framework other than Win32, Windows Forms, or WPF.


## UI Automation Provider Concepts

### Elements

>UI Automation elements are pieces of user interface (UI) that are visible to UI Automation clients.

### Navigation

>UI Automation elements are exposed to clients as a UI Automation tree. UI Automation constructs the tree by navigating from one element to another.

### Views
a client can see the UI Automation tree in the three principle views, as shown in teh following table.

Views |  description
----|-------------------------
Raw View | Contains all Element
Control View | Contains elements that are controls
Content View | Contains elements that have contents

### Frameworks

> A framework is a component that manages child controls, hit-testing, and rendering in an area of the screen. For example, a Win32 window, often referred to as an HWND, can serve as a framework that contains multiple UI Automation elements such as a menu bar, a status bar, and buttons.


Win32 container controls such as list boxes and tree view are considered to be framework.

### Fragments

> A fragment is a complete subtree of elements from a particular framework. The element at the root node of the subtree is called a fragment root.

### Hosts

The root node of every fragment must be hosted in an elemnt, usually a Win32 window (HWND) ,... 

Well, the TOPIC Is too advanced, and I slacked not to copy full of them..


## References

[UI Automation Providers Overview](http://msdn.microsoft.com/en-us/library/ms750446(v=vs.110).aspx) 
[UI_Automation_Providers_Overview]:http://msdn.microsoft.com/en-us/library/ms750446(v=vs.110).aspx