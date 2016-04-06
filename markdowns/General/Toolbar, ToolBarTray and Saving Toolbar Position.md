## Toolbar tray and toolbar

We have an design where that we want to have a toolbar in a toobar tray

the layout controls that we used includes the following


```
	QuickClickToolbarBorder
		ToolBarTray
			ToolBar
				OverflowGrid (it is just an Grid)...
			ToolBar
```


To remember the position of the ToolBar at ToolBarTray, you can save and load the


```
<ToolBar 
                    Margin="0,2" 
                    Height="32"
                    Band="{Binding QuantityToolBarBand, UpdateSourceTrigger=PropertyChanged, Mode=TwoWay}"
                    BandIndex="{Binding QuantityToolBarBandIndex, UpdateSourceTrigger=PropertyChanged, Mode=TwoWay}">
```

value.