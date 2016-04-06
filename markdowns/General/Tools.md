
# Introduction

this page will contains some information about the commonly used tools such as PHP,... and their configuration usage and etc...



## php interactive mode 
well if you are running from the widows, you are screwed, because there is no support of the readline libraries, which means you cannot run line by line interactive. 

however, you still types in some thing and send an end-of-file signal to the windows, and let the interpreter to execute the input once.

here is what you do 

```php -a ```

then types in 
```
<?php 

interactive mode enabled

<?php
echo "hello world!";
?>

^Z
hello world!
```

References:
[PHP: Interactive shell - Manual](http://php.net/manual/en/features.commandline.interactive.php)


## Visual Studio to do Regular expression replace

I have the following text

```
SecurityName 
PriceLevel 
DisplayBid 
DisplayAsk 
IsHighValue 
IsLowValue 
FlashMe 
FlashOthers 
BetweenHighAndLow 
DepthLevelVm 
BidSizeDisplay 
BidMarketDetails 
AskMarketDetails 
BidTrader 
AskTrader 
BidDetails 
AskDetails 
IsBidTake 
IsAskHit 
```

and I want to replace to the following

```
SecurityName = Display.SecurityName, 
PriceLevel = Display.PriceLevel, 
DisplayBid = Display.DisplayBid, 
DisplayAsk = Display.DisplayAsk, 
IsHighValue = Display.IsHighValue, 
IsLowValue = Display.IsLowValue, 
FlashMe = Display.FlashMe, 
FlashOthers = Display.FlashOthers, 
BetweenHighAndLow = Display.BetweenHighAndLow, 
DepthLevelVm = Display.DepthLevelVm,
BidSizeDisplay = Display.BidSizeDisplay, 
BidMarketDetails = Display.BidMarketDetails, 
AskMarketDetails = Display.AskMarketDetails, 
BidTrader = Display.BidTrader, 
AskTrader = Display.AskTrader, 
BidDetails = Display.BidDetails, 
AskDetails = Display.AskDetails, 
IsBidTake = Display.IsBidTake, 
IsAskHit = Display.IsAskHit, 
```


I searched with the following keyword "visual studio replace regular expression backreference", and this [regex - Search and replace in Visual Studio - Stack Overflow](http://stackoverflow.com/questions/7848329/search-and-replace-in-visual-studio)

tells some how. 

the regular expression that I wrote . Search `^([^\s]*)`, replace with `$1 = Display.$1`