## Introduction 
this page is about the core technology such as the Coordinator, Organizer and ContentProvider.


## Launch a view

you can try to open the Launch mode, by ctrl+alt+O to bring up the Organizer window. then you can type the following to the stk://address field 


stk://launcher

then from the launcher address you can type the following. 

stk://Staging.Your-App.default/YourTheme

or you can try the following by changing the launch special.

change from the following 
`$AppEnvironment openwindow stk://$AppEnvironment.Your-App.default/YourTheme`

to the following. 

`$AppEnvironment launch stk://$AppEnvironment.Your-App.default/YourTheme`


## GuiToolkit's Watermark margin issue

it seems that the WaterMark margin is affectecd by the TextBox' alignmnet.



the code is as below

```

gtk:TextBoxBehavior.WaterMarkText="Set focus on the text"

```

well, the Text box control that has the attached property is  as follow.


```
<TextBox
   gtk:TextBoxBehavior.WaterMarkText="Set focus on the text" margin="5" />

```

it shows the text which aligns to the bottom of the Control, the fix is to remove the margin settings.

```
<TextBox
  gtk:TextBehavior.WaterMarkText="SetFocus on the text" />
```