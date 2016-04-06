## Best general SVN Ignore Pattern?

This is a note page on the tools - [SVN how to create a SVN Ignore pattern][Best_General_SVN_Ignore_Pattern], and [How do you include/exclude a certain type of files under Subversion?](http://stackoverflow.com/questions/122313/how-do-you-include-exclude-a-certain-type-of-files-under-subversion)

### the issues

I am working with Dotnet applications, and I wantted to precluded the AssemblyInfo.cs and the AssemblyInfoMaven.cs file from being considered again and again when the I do  a MVN update. 

### the solution
it turns out that you can modify the global settings for SVN , the location to the SVN config is availabel here 

> "%APPDATA%\Subversion\config"

or 

> ~/.subversion/config 

Where you can open the section on

> global-ignores = ...


you can edit it to make it something similar to the following. 

> global-ignores = AssemblyInfo.cs AssemblyInfoMaven.cs




[Best_General_SVN_Ignore_Pattern]: http://stackoverflow.com/questions/85353/best-general-svn-ignore-pattern 
[How_do_you_include_exclude_a]: http://stackoverflow.com/questions/122313/how-do-you-include-exclude-a-certain-type-of-files-under-subversion

## References

[Best general SVN Ignore Pattern?](http://stackoverflow.com/questions/85353/best-general-svn-ignore-pattern)
[How do you include/exclude a certain type of files under Subversion?](http://stackoverflow.com/questions/122313/how-do-you-include-exclude-a-certain-type-of-files-under-subversion)
