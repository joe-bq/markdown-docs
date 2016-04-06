## codec without Factory example

recently we have found a very strange encoding/decoding issue regarding the with the Encode System [ItemDecode][Encode_Decode_Item_Framework].

First we try to create some domain class, the class's definition is something like below.

```
namespace Showcase.DataAccess
{
    [Category(MyClassCateogryName)]
    public class ConfigServerComponentRepository : ItemBase
    {
        public const string MyClassCateogryName = "App:Data";
        public MyClass(string id, AppContext appContext)
            : base(id, appContext, new FunctionalContext("Application"))
        { }

        public string Components { get; set; }
    }
}
```

and the code that read from the config server to get the node is something as below.  

```
var item = m_appContext.GetItem(new ItemReference("App:Data", "Components"));
```


the config node for App:Data Components is something like below. 

```
<root type=".Showcase.DataAccess.ConfigServerComponentRepository" category="App:Data" id="Components" xmlns="http://www.app.com/your_org/core/1.1">
    <Components value="bulabula" type="string"/>
</root>
```

and we tried something as below. 

```
<root type=".DataAccess.ConfigServerComponentRepository" category="App:Data" id="Components" xmlns="http://www.app.com/your_org/core/1.1">
    <Components value="bulabula" type="string"/>
</root>
```
however, other combination on the name of the type does not work.. 

It seems that the decode is doing something like this to find the class name

* **&lt;Organization&gt;**{type}
* **{Assembly_Name}**{Type}

in our case, it either append **App**  to *Showcase.DataAccess.ConfigServerComponentRepository* as in case 1. or append **Showcase**  to the type *.DataAccess.ConfigServerComponentRepository*;

## violation when not starting from ContentProvider and not conforming naming convention
However, it does not explain the fact that  when I start an application without the ContentProvider, and my type does not begins with Organization... 

```
            m_appContext = Bootstrapper.ConstructRootContext("your_org-core", options, "Presentation-Showcase");

            var myClassObj = m_appContext.GetItem(new ItemReference("App:Data", "wangboqi"));
            if (myClassObj != null)
            {
                Console.WriteLine("success!");
                Console.WriteLine("!Component! = {0}", ((MyClass)myClassObj.Value).Components);
            }

```

I can violate the rules. e.g.

```
<root type="TableProviderClone.MyClass" category="App:Data" id="wangboqi" xmlns="http://www.app.com/your_org/core/1.1">
    <Components value="bulabula" type="string"/>
</root>
```

where my class is something like below. 
 
```
namespace TableProviderClone
{
    /// <summary>
    /// TODO: Update summary.
    /// </summary>
    [Category(MyClassCateogryName)]
    public class MyClass : ItemBase
    {
        public const string MyClassCateogryName = "App:Data";
        public MyClass(string id, AppContext appContext)
            : base(id, appContext, new FunctionalContext("Applicat"))
        { }

        public string Components { get; set; }
    }
}
```

It seems there are two separate set of logic when the Assembly is from the path or if the assembly is loading from ContentProvider.

I tried the following as well.

```
<root type=".MyClass" category="App:Data" id="wangboqi" xmlns="http://www.app.com/your_org/core/1.1">
    <Components value="bulabula" type="string"/>
</root>
```

which is conformant to the second notation.
