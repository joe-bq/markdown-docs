## Excel tips

introduction, this page will contains some useful tips on how to use the excel very effectively to be more productive in day to day basis.

## Making Sense of dollar signs in Excel

> We’ve noticed some of you searching for help using “$” – a dollar sign. In Excel, a dollar sign can denote a currency format, but it has another common use: indicating absolute cell references in formulas. Let’s consider both uses of the dollar sign in Excel.

what is the meaning, the Dollar signs indicating absolute references. 

There are three types of Cell references

* Abosolute Cell references
* Relative cell references
* Mixed call references

where the _$A$1_ means that the reference is always cell A1, wherever the fomula is copied or moved, it is always refers to cell A1.

while relative one like A1, when it is moved down, it becomes A2, and move right, then it becomes B2.

while the mixed call references, such as _A$1_, when it is moved, the row adjusts, but the column do not adjusts, so it is possbile to become _B$1_ but never become _A$2_;

## the use of fomula

where the first cell E18, it has this formular 
`=(1-SUM($E$18:E18)*C19)/(1+C19)`

and the cell E19, it depends on the sum value of E18:E18, so you can write as follow 

`=(1-SUM($E$18:E18)*C19)/(1+C19)`

and the E20 is 
`=(1-SUM($E$18:E19)*C20)/(1+C20)`
so on and so fource. 

hence you will get the net result the value of Cell E19 uses the sum from E18 to E18, and Cell E20 uses the sum from E18 to E19...

if you otherwise not apply the dollar sign notation, you will always have the sum 

`=(1-SUM(E19:E19)*C20)/(1+C20)`

on the Cell E20.


references: 

[Making sense of dollar signs in Excel](http://blogs.office.com/2011/08/17/making-sense-of-dollar-signs-in-excel/)