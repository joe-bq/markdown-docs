## Visual studio code Productivity 

well there are some cases you want to create your own code snippet, here you can do that, but you have to understand how the code snippet files works. 

well, there are the basic code snippet 


```
<?xml version="1.0" encoding="utf-8"?>
<CodeSnippets
    xmlns="http://schemas.microsoft.com/VisualStudio/2005/CodeSnippet">
    <CodeSnippet Format="1.0.0">
        <Header>
            <Title></Title>
        </Header>
        <Snippet>
            <Code Language="">
                <![CDATA[]]>
            </Code>
        </Snippet>
    </CodeSnippet>
</CodeSnippets>
```

and a very basic one by live example 

```
<Code Language="VB">
    <![CDATA[Console.WriteLine("Hello, World!")]]>
</Code>
```

a code snippet can also require certain references to be added, here is code snippet that requires the assembly as well as the namespace to be imported.


```
<References>
    <Reference>
        <Assembly>System.Windows.Forms.dll</Assembly>
    </Reference>
</References>
```

and the namespace one

```
<Imports>
    <Import>
       <Namespace>System.Windows.Forms</Namespace>
    </Import>
</Imports>
```

well, the last one is the CDATA[] parts. 


```
<![CDATA[MessageBox.Show("Hello, World!")]]>
```




REFERENCES:
[workthrough_create_code_snippet]: http://msdn.microsoft.com/en-us/library/ms165394.aspx
[Walkthrough: Creating a Code Snippet][workthrough_create_code_snippet]


