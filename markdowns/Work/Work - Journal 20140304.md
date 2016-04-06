-- 

introduction, this is a monthly journal, which keeps track of the work and knowledge related stuff.  


## hijack the Build up way to do more smart kind of Build up 

UnityContainer.BuildUp() - Can I make it inject new instances into properties only if these are null? : http://stackoverflow.com/questions/7120476/unitycontainer-buildup-can-i-make-it-inject-new-instances-into-properties-on

## some issue regarding Singleton vs. Unity Container
not sure if this is related, but there is a bug found in regards with Singleton vs. Unity Container. 

Unity BuildUp fails for singleton: http://stackoverflow.com/questions/5990841/unity-buildup-fails-for-singleton


## introduction page on the resolving with Unity 
   3 - Dependency Injection with Unity: http://msdn.microsoft.com/en-us/library/dn178463(v=pandp.30).aspx

it talked about the 

1.  Hierarchical Lifetime Management
2. Lifetime Management


## ependency injetion and etc..
in this chapter the folloiwng has been discussed
  1)  
  2) Object Composition 
  3) type of construction: constructor injection and property setter injection 

References: 

  then follows the DependencyInjectionWithUnity 
  
2. - Dependency Injection - http://msdn.microsoft.com/en-us/library/dn178469(v=pandp.30).aspx
3. - Dependency Injection with Un http://msdn.microsoft.com/en-us/library/dn178463(v=pandp.30).aspx

there are other materials that you can find for the Unity related 

1. dependency injection 
2. Interception
3. Extending Unity and others .
4. IOC (inverse of control) 

## Annotating Objects for Constructor Injection

[Annotating Objects for Constructor Injection](http://msdn.microsoft.com/en-us/library/ff660875(v=pandp.20).aspx)

>Constructor Injection with Existing Objects
>
>If you use configuration or the RegisterInstance method to register an existing object, constructor injection does not take place on that object because  it has already been created outside of the influence of the Unity container. Even if you call the BuildUp method of the container and pass it the existing object, 
constructor injection will never take place because the constructor will not execute.

## Casle Proxy 

below are just some logs 

base {Connect.Contract.ServiceContractBase} = {Unity:UTP:BrokerPosition: Environment=Development;Connectivity=Intranet (768d347d-0d84-4e3f-8e8b-947eb5e11505)}

[Castle.Proxies.IBrokerPositionServiceProxy] = {Castle.Proxies.IBrokerPositionServiceProxy}

http://www.castleproject.org/projects/dynamicproxy/
>   Castle DynamicProxy is a library for generating lightweight .NET proxies on the fly at runtime. Proxy objects allow calls to members of an object to be intercepted without modifying the code of the class.



## Different between OnlyOnRranToCompletion and NotOnFaulted?

References:
[Different between OnlyOnRranToCompletion and NotOnFaulted?](http://stackoverflow.com/questions/7622909/difference-between-onlyonrantocompletion-and-notonfaulted)

it turnes out that  

```
NotOnRanToCompletion | NotOnFaulted == OnlyOnCancelled
NotOnCanceled        | NotOnFaulted == OnlyOnRanToCompletion
NotOnRanToCompletion | NotOnCanceld == OnlyOnFaulted
```

and the quote is here 

> `OnlyOnFaulted` means that the continuation will run if the antecedent task throws an exception that is not handled by the task itself, unless the task was canceled.

> `NotOnRanToCompletio` means that the continuation will not run if the task ran to completion, that is to say it will run if the task threw an exception, or if it was canceled.

> So to summarize, if you want your continuation to run if the task is canceled or threw an exception, use `NotOnRanToCompletion`. If you want it to run only if it threw an exception but not if it is canceled, use OnlyOnFaulted.


## OQL fields is null predicate
you know how to compare empty fileds, but how do you compare those null fields?

the oql clause that you can use to compare if a field is null is by using something like below. 

```
where t.getValue.get('TradeId') != ''  and t.getValue.get('UpfrontFee') = null
```
or more complex one would be like below. 

```
where t.getValue.get('TradeId') != ''  and ( t.getValue.get('Totoro.PremiumAmount') = null  and t.getValue.get('Totoro.Premium') = null)
```

## Difference between LIB and LIBPATH

> LIB is for the linker, helps it find import and static libraries.

> LIBPATH is for the compiler, helps it find metadata files. Like type libraries, .NET assemblies, WinRT .winmd files.

references:

[What is the difference between the LIB and LIBPATH environment variables for MS Visual


 C/C++?](http://stackoverflow.com/questions/20483619/what-is-the-difference-between-the-lib-and-libpath-environment-variables-for-ms)

## How to build/compile Ruby with openssl and zlib

### Compile zlib

first, you will need to downoad the latest sources of the zlib;

second, if you are running for x86, just do the following 

```
cd zlib-work-directory
nmake -f win32/Makefile.msc
```

if you are running for x64, you will need to do 

```
cd contrib\masmx64
bld_ml32.bat
cd ..\vstudio\vc10
msbuid /p:Configuration=Release /p:Platform=x64
```

1. the debug version of the output is **libwapid.** rather than **libwapi** that is required by the ruby compilation
2. you won't like to define the constants */DZLIB_WINAPI* or similar because that will gives you the **__stdcall** calling convention, and that you won't be able to correctly compile the sources. 

#### Compile openssl
first, you will need to download the files of openssl

SECOND, you will need to download the ActivePerl and install it

second, if you are running a dynamic libraries, do the following 

```
perl Configure VC-WIN32 --prefix=C:\Build-OpenSSL-VC-32
ms\do_ms
nmake -f ms\ntdll.mak 
nmake -f ms\ntdll.mak install
```
[Building OpenSSL for Visual Studio](http://developer.covenanteyes.com/building-openssl-for-visual-studio/)


### Compile the Ruby-2.1.1 itself
you will first set the following variables

1. LIBPATH=%LIBPATH%;path_to_openssl_lib;path_to_zlib_lib;
2. LIB=%LIB%;path_to_openssl_lib;path_to_zlib_lib;
3. INCLUDE=%INCLUDE%;path_to_openssl_topheader;path_to_zlib_headers
4. PATH=%PATH%;path_to_openssl_dll;path_to_zlib_dll;

## Calling conventions and Windows API calling convention

differente compiler may have different name decoration/mangling schema that is in place, like the Visual Studio they treat the VC/C/decl/stdcall/fastcall and etc...

ONE spcial notes : **x64 symbols don't have the leading underscore since x64 doesn't have any calling conventions.**

so that when you compile the same funciton, such as *func*, you will get back *_func* if you compile with x86 with *_cdec_*, but you will always get back *func* just when you are compiling with x64 compiler.

the **WINAPI** calling convention default to use the **_stdcall** calling convention.

you can find from the reference section about the Decorated names, where the table is as follow

|Calling convention|Decoration|
|------------------|----------|
|__cdecl (the default)| Leading underscore(_)|
|__stdcall|Leading underscore (_) and a trailing at sign (@) followed by a number representing the number of bytes in the parameter list|
|__fastcall|Same as __stdcall, but prepended by an at sign instead of an underscore|

while the decorated names for the C++ program is much more complex, check [Format of a C++ Decorated Name](http://msdn.microsoft.com/en-us/library/2ax8kbk1.aspx)


Reference:
[Using win32 Calling Convention](http://unixwiz.net/techtips/win32-callconv.html)
[/Gd,/Gr,/Gv,/Gz (Calling Convention)](http://msdn.microsoft.com/en-us/library/46t77ak2.aspx)
[MS VC linker (link.exe): Why no warning for 32/64 bit CPU architecture mismatch?](http://stackoverflow.com/questions/7938936/ms-vc-linker-link-exe-why-no-warning-for-32-64-bit-cpu-architecture-mismatch) 
[Decorated names](http://msdn.microsoft.com/en-us/library/56h2zst2.aspx) 
[Argument Passing and Naming Conventions](http://msdn.microsoft.com/en-us/library/984x0h58.aspx)


## Exporting from a DLL Using DEF Files

Basically this can give you the ability to explicitly state which symbosl that you want to export.

the .exp file menas the import files that the library will import. 

[Exporting from a DLL Using DEF Files](http://msdn.microsoft.com/en-us/library/d91k01sh%28v=VS.100%29.aspx)
[.def file EXPORTS](http://msdn.microsoft.com/en-us/library/hyx1zcd3(v=vs.100).aspx)

## Compiler generated pdb and the Linker generated pdb files

during the build of the VC projects, there are two steps that can generate the pdb files. 

* the compiler generated 
* the linker generated

it is created in different steps which is supposed to give different program debug dabatase if the compiler output/linked output are used differently.

you can set the pdb for the compiler via 

* /Fd option in the CL compiler
* Project Properties | Configuration Properites | C/C++ | Output Files, find "Program Database File name", changing it from *$(IntDir)vc$(PlatformToolsetVersion).pdb* to something like *$(TargetDir)$(TargetName).pdb* - be careful not to do so 

the same you can control the pdb file generated by the linker

* /PDB option from the linker command 
* Project Properties | Configuration Properites | Linker | Debugging | Generate Program Database file. normally the value the field is *$(TargetDir)$(TargetName).pdb*



