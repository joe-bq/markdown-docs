## Using UI Automation for Automated Testing
the commonly used automation is for automated testing, check the MSDN on page on the [UI Automationg for Automated Testing][Using_UI_Automation_for_Automated_Testing] 

UI Automation was developed as a successor to _Microsoft Active Accessibility_.

Both a provider and client are required to implement UI Automation for it to be useful as an automated test tool. 

### UI Automation in a Provider

For a UI to be automated, a developer of an application or control must look at what actions an end-user can perform on the UI object using standard keyboard and mouse interaction.

Once that has been identified, the correspondign UI automation control patterns should be implemented on the control. 

### Implementing UI Automation

this answers as why we need to implement the UI automation, that is because different technology involves, and you are required to know framework-specific information in order to expose properties and behaviors of the controls in that framework.

### UI Automation in a Client

The goal of many automated test tools and scenarios is the consistent and repeatable manipulation of the user interface. This can involve unit testing specific controls through to the recording and playback of test scripts that iterate through a series of generic actions on a group of controls.

the key is to provide the *Programmatic Acess*

#### Programmatic Acess

basically it is done with 

* UI Automation tree 
* UI Automation Control types 
* UI automation Properties
* UI Automation Control pattern 
* UI AUtomation Events

#### Key Properties for Test Automation

##### Automation ID

##### ControlType

##### NameProperty

### Implementing UI Automation in a Test Application
it is usually consists of hte following actions.

* Add the UI automation references
* Add the System.Windows.Automation namespace
* Add the System.Windows.Automation.Text namespace
* find controls of interest
* Obtain Control patterns
* Automate the UI 

 
## References

[Using UI Automation for Automated Testing](http://msdn.microsoft.com/en-us/library/aa348551(v=vs.110).aspx)
[Using_UI_Automation_for_Automated_Testing]:http://msdn.microsoft.com/en-us/library/aa348551(v=vs.110).aspx