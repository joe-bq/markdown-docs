## Vertical depth and some implementation thoughts

thought that we have an implementation on the Vertical depths.

ASize | Ask | Bid | BSize
--------- | ----- | ----- | ----------
30 | 98-24 | 97-12 | 29 
31| 98-24+| 97-11+| 28
32| 98-25| 97-11| 27
33| 98-25+| 97-10+| 26
34 | 98-26| 97-10| 25

well, we want to display the values in to a vertical detphs


which shows as follow



ASize | Prices| BSize
--------- | ----- | ----- 
30  | 98-26|
31 | 98-25+|
32 | 98-25| 
33 | 98-24+|
34  | 98-24|
 .  | ... | .
 .  | 97-12 | 29
 .  | 97-11+| 28
 .  | 97-11| 27
 .  | 97-10+| 26
 . | 97-10| 25


well, given the above graph, we now that for level 0 (TopStack) we have two price levels 98-24 and 98-12 separately to display the ask size and  bid size.

there are few implications to the horizontal depth to Vertical depth conversion. 

1. triple update that affect opposite side 
the triple update meaning an update that affects three prices.
suppose that we have a update which change Ask Price from 98-26 to 98-25+, while the bid prices doesn't change.

well, this means we will need to 
1) clear the Ask size display at 98-26
2) show the Ask size display at 98-25+
3) do not change 98-12 (bid size)

well, if we update both Bid/Ask side when we do an update to a vertical depths: then it will happens as such.

1) clear the Ask size display at 98-26
2) show the Ask size display at 98-25+
3) do not change 98-12 (bid size)
4) 98-11+ (98-25+'s bid side) will be updated to get 98-26 (old)'s bid size and this can cause phantom error

2. Market move update
suppose that we have an market move, where Ask prices 98-25+ moves to 98-26, and at that moment, the udpate comes in at the same time, which can cause a transit state where there are two 98-25+ prices.

Suppose that when such update comes we do 

1) clear the Ask size display at 98-25+
2) show the Ask size display at 98-26
3) do not change 98-11+ (bid size)

the problems is that vertical despth is not consistent with the horizontal depth in that 98-25+ now shows empty and there is only one showing 98-26 (which is inevitable), but it is one side of inconsistency


now suppose there comes a second message, which update 98-26 to 98-26+.. we do this 

1) clear the Ask size display at 98-26
2) show the Ask size display at 98-26+
3) do not change 98-12 (bid size)

combines the two together, we ends up showing no 98-26.... well at horizontal we still shows one 98-26.... 

to correct way is 

1) clear the Ask size display at 98-26 ( as we found there is still depth level piont to 98-26)..
2) show the Ask size display at 98-26+
3) do not change 98-12 (bid size)
