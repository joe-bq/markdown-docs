## Windows Debugger tools to download 

where the AdPlus and others are availabe through the windows SDK or WDK (Windows Driver Kit) , you can download from the links in the references parts. 

Reference: 
[Debugging Tools for Windows (WinDbg, KD, CDB, NTSD)](http://msdn.microsoft.com/en-us/library/windows/hardware/ff551063(v=vs.85).aspx) 
[Windows Driver Kit Version 7.1.0](http://www.microsoft.com/en-us/download/confirmation.aspx?id=11800) 
[Microsoft Windows SDK for Windows 7 and .NET Framework 4](http://www.microsoft.com/en-us/download/confirmation.aspx?id=8279) 



## Windows SDK Fails to install with Return code 5100

then Windows SDK will fail to install and return return code 5100 on the Windows SDK... 

the errors are 

>C:\Program Files\Microsoft SDKs\Windows\v7.1\Setup\SFX\vcredist_x86.exe installation failed with return code 5100

OR

>C:\Program Files\Microsoft SDKs\Windows\v7.1\Setup\SFX\vcredist_x64.exe installation failed with return code 5100

cause 

    This issue occurs when you install the Windows 7 SDK on a computer that has a newer version of the Visual C++ 2010 Redistributable installed.  The Windows 7 SDK installs version 10.0.30319 of the Visual C++ 2010 Redistributable. 
    
resolution

1. remove the Visual C++ 2010 X86 Redistributable
2. install Windows 7 SDKs
3. Reinstall the visual C++ 2010 x86 Redistributable

Check the references 


References
[windows_sdk_failes_return_51000]: http://support.microsoft.com/kb/2717426
[Windows SDK Fails to Install with Return Code 5100 Print Print Email Email][windows_sdk_failes_return_51000]
[wdk_and_windbg_downloads]: http://msdn.microsoft.com/en-us/windows/hardware/hh852365.aspx
[WDK and WinDbg downloads][wdk_and_windbg_downloads]



## install the Windows Debugging tools
while after installation, I did not find the debugging tools under the 

    C:\Program Files\Microsoft SDKs\Windows\v7.1\bin

However, I found them under the following location (for debuggint tools)

    C:\Program Files\Debugging Tools for Windows (x86)

and under this for the Performance Suite 

    C:\Program Files\Microsoft Windows Performance Toolkit\WPF Performance Suite
    
and indeed, when you have install the Windows SDK, you can find the redist directory under the Windows SDKs root folder. e.g. 

    C:\Program Files\Microsoft SDKs\Windows\v7.1\Redist\Debugging Tools for Windows\dbg_x86.msi
    
Double click to install.

Reference: 
[Debugging Tools for Windows (WinDbg, KD, CDB, NTSD)](http://msdn.microsoft.com/en-us/library/windows/hardware/ff551063(v=vs.85).aspx) 
[Windows Driver Kit Version 7.1.0](http://www.microsoft.com/en-us/download/confirmation.aspx?id=11800) 
[Microsoft Windows SDK for Windows 7 and .NET Framework 4](http://www.microsoft.com/en-us/download/confirmation.aspx?id=8279) 


## with adplus to collect dump information. 

the command line that I used to create dump is as such 

    cscript "c:\Program Files\Debugging Tools for Windows (x86)\adplus_old.vbs" -crash -o C:\Temp\YourApp-Dump -sc "C:\Program Files\Path\to\Your\Application.exe -Application=Your-App -System=Your:App -Environment=Development.Staging -theme ApplicationTheme -norecap -scanfolder -nomonitor -debugView YourViewer"
    
while there is a flash and there is nothing that I can do about it. I guess that is because of the space in the file's path. 

so changing to the attach mode 

    cscript "c:\Program Files\Debugging Tools for Windows (x86)\adplus_old.vbs" -crash -p 10308 -o C:\Temp\YourApp-Dump
    
to use it in the hang mode, do this 

    cscript "c:\Program Files\Debugging Tools for Windows (x86)\adplus_old.vbs" -hang -p 6008 -o C:\Temp\YourApp-Dump

Reference:

[How to use ADPlus (AutoDump+) to create a memory dump file for troubleshooting issues with Symantec Products and other third party applications](http://www.symantec.com/business/support/index?page=content&id=TECH38846) 
[如何使用 ADPlus.vbs 来解决"挂起"和"崩溃"](http://support.microsoft.com/kb/286350/zh-cn)

## How do I use a dump file to diagnose a memory leak?

> I'm assuming you're using .NET4 given you can open the dump in Visual Studio. Here's a very quick guide to help you work with your dmp file:

>1) Run WinDbg, set symbols path (File -> Symbol Search Path) to
SRV*c:\symbols*http://msdl.microsoft.com/download/symbols

>2) Open Crash dump or drag your .DMP file onto WinDbg.

>3)type this into the command window
.loadby sos clr
(FYI, for .NET 2, the command should be .loadby sos mscorwks)

>4) then type this
!dumpheap -stat
which lists the type of objects and their count. looks something like this:

also, there is also this 

> To troubleshoot this you need to inspect the managed heap. WinDbg + SOS (or PSSCOR) will let you do this. The !dumpheap -stat command lists the entire managed heap.

>You need to have an idea of the number of instances of each type to expect on the heap. Once you find something that looks odd you can use the !dumpheap -mt <METHOD TABLE> command to list all instances of a given type.

>The next step is to analyze the root of these instances. Pick one at random and do a !gcroot on that. That will show how that particular instance is rooted. Look for event handlers and pinned objects (usually represent static references). If you see the finalizer queue in there you need to examine what the finalizer thread is doing. Use the !threads and !clrstack commands for that.

>If everything looks fine for that instance you move on to another instance. If that doesn't yield anything you may need to go back to look at the heap again and repeat from there.

>Other sources of leaks include: Assemblies that are not unloaded and fragmentation of the Large Object Heap. SOS/PSSCOR can help you locate these as well, but I'll skip the details for now.


to fix the symbol, I can run 

    .symfix c:\localsymbols

try search 
> .symfix or Microsoft Public Symbols

in 
>.hh

References
[How do I use a dump file to diagnose a memory leak?](http://stackoverflow.com/questions/9514401/how-do-i-use-a-dump-file-to-diagnose-a-memory-leak)
[Debugging Memory Problems](http://msdn.microsoft.com/en-us/library/ee817660.aspx)
[Investigating issues with Unmanaged Memory. First steps.](http://kate-butenko.blogspot.hk/2012/07/investigating-issues-with-unmanaged.html)

## Some windbg help commands

* .cls
you can do the 

    .cls
to clear the screen


* .reload
do a reload when you fixed the symbols path

## SQL priviledged account and sysadmin account


> It's the same issue. You won't be able to set passwords because your account didn't have the necessary permissions in your SQL instance. If you don't know the login details if an account with sysadmin privileges (or certain other more specialized privileges that are very unlikely in your situation) then you will need to get it from someone who does.

> If you specifically provisioned your account during SQL Server setup (it asks you for accounts to be added to the sysadmin group) then yes. It does not automatically add you to the sysadmin group, nor will it automatically add anything except sa. It should have asked you to set the sa password during setup. Do you remember doing that? 

the problem might be related to login, you can try "fantastic step-by-step guide on getting control of your SQLExpress instance if you don't have your sa password.".. [Resetting SA Password for SQL Server Express 2008 R2](http://prognuggets.blogspot.hk/2011/05/resetting-sa-password-for-sql-server.html)


while the key points is 
1. -m; to the SQLExpress to start the SQLServer on a single use mode 
2. login to the box with administrators 
3. Management studio login to the local .\SQlExpress and change password
4. enable both "SQL Server and Windows Authentication mode"


Reference:
[SQL Server 2008 R2 Express permissions — cannot create database or modify users](http://stackoverflow.com/questions/9185142/sql-server-2008-r2-express-permissions-cannot-create-database-or-modify-users)
[Resetting SA Password for SQL Server Express 2008 R2](http://prognuggets.blogspot.hk/2011/05/resetting-sa-password-for-sql-server.html) 


## Install of SQl Server 2008 Sample Databases
there are certain prerequisite that has to be met before you can install the sample database. , check [install_prerequisite_for_the_sql_server_2008].

while in short, the following has to be installed. 

* Full-Text Search must be installed.
* The SQL Full-text Filter Daemon Launcher service must be running.
* FILESTREAM must be enabled.

on my case, the following shall be installed.

AdventureWorks OLTP 2008
AdventureWorks Data Warehouse 2008
AdventureWorks LT 2008
AdventureWorks OLAP Standard 2008           Manually deploy via BIDS after install
AdventureWorks OLAP Enterprise 2008         Manually deploy via BIDS after install
AdventureWorks OLTP
AdventureWorks Data Warehouse
AdventureWorks LT
AdventureWorks OLAP Standard               Manually deploy via BIDS after install
AdventureWorks OLAP Enterprise             Manually deploy via BIDS after install


check 
[SQL Server 2008 SR4][sqls_server_2008_sr4]

References
[installation Prerequisites for the SQL Server 2008 Sample Databases][install_prerequisite_for_the_sql_server_2008]
[install_prerequisite_for_the_sql_server_2008]: http://msftdbprodsamples.codeplex.com/wikipage?title=Database%20Prerequisites
[sqls_server_2008_sr4]: http://msftdbprodsamples.codeplex.com/releases/view/37109
[SQL Server 2008 SR4][sqls_server_2008_sr4]

## Add logins and Server Roles on a particular User 

you can add a login to the SQlExpress with the Sql Server Managerment Studio 

1. First connect to the SQLExpression locally with an admin account (with SQL authentication), haven't tried the windows authentication 
2. Goes to Security | Logins 
3. Right click "New Login"
4. in the Login Name, fill in ASIAPAC\wangboqi, or similar
5. in General tab, Select "Windows Authentication"
6. in Server Roles tab, check "public" and "sysadmin"
7. in user mapping, tick "master", "model", "msdb", "tempdb" (all of them) 
8. Click save
9. Back to the Management Studio main page, find the node "sysadmin" under  "Server Roles", open "properties"
10. Click Add, and input ASIAPAC\wangboqi that you created at step 4.
11. done.

check the [Installing Sample Databases][instaling_sample_database] for more details.

You can do this for a group of users. ... 
References:
[instaling_sample_database]: http://msftdbprodsamples.codeplex.com/wikipage?title=Installing%20Databases&referringTitle=AWDW2008Details
[Installing Sample Databases][instaling_sample_database]

## Install SQL Server Express 2008 with Advanced Features (such as FullText Search support) 

on my box, it was the SQL Server Express 2008 R2 (with Service Pack 1) that was installed, the problem with this is it does not have some of the advanced features enabled. such as the "FullText Search support" which is necessary to install the "Adventure Works for Online Service the sample database".

the steps that I followed in order to get it installed

1. remove the old Microsoft SQl Server 2008 
2. Install the new Microsoft SQl Server 2008 with Advanced features ([microsoft_sql_server_2008_express_with_advanced_services])
3. install the [SQL Server 2008 SR4][sqls_server_2008_sr4]

In step 2, you will have to close all the windows, otherwise, you will get the BeginInvoke errors. the reference link is missing, so I shall not repeat it here.  

Another parts that you may be watchful is that you may need to add your window login to the sysadmin group from within in the Sql Management studio.

Theree is such an "prerequisite" web, which you should have refers to [Installation Prerequisites for the SQL Server 2008 Sample Databases][installation_prerequisites_for_sql_server_2008_sample_database]

things (service) that you need to enable or start
1. Install Full-Text Search
2. nabling the SQL Full-text Filter Daemon Launcher Service
3. Enabling FILESTREAM


References:
[microsoft_sql_server_2008_express_with_advanced_services]: http://www.microsoft.com/en-us/download/details.aspx?id=1842
[Microsoft® SQL Server® 2008 Express with Advanced Services][microsoft_sql_server_2008_express_with_advanced_services]
[howto_install_adventure_works_sql_dw_and_analysis_services]: http://www.ssas-info.com/analysis-services-faq/29-mgmt/242-how-install-adventure-works-dw-database-analysis-services-2005-sample-database
[How to install Adventure Works SQL DW and Analysis Services 2005/2008 sample database and project][howto_install_adventure_works_sql_dw_and_analysis_services]
[sqls_server_2008_sr4]: http://msftdbprodsamples.codeplex.com/releases/view/37109
[SQL Server 2008 SR4][sqls_server_2008_sr4]
[installation_prerequisites_for_sql_server_2008_sample_database]: http://msftdbprodsamples.codeplex.com/wikipage?title=Database%20Prerequisites
[Installation Prerequisites for the SQL Server 2008 Sample Databases][installation_prerequisites_for_sql_server_2008_sample_database]


## Connection to localhost\MSSQlSERVER failed 

After I installed the new SQl Server Express 2008 with Advanced Features, I tried to connect to localhost\MSSQlSERER, I failed w ith the following message 

```
TITLE: Connect to Server
------------------------------

Cannot connect to localhost\MSSQLSERVER.

------------------------------
ADDITIONAL INFORMATION:

A network-related or instance-specific error occurred while establishing a connection to SQL Server. The server was not found or was not accessible. Verify that the instance name is correct and that SQL Server is configured to allow remote connections. (provider: SQL Network Interfaces, error: 25 - Connection string is not valid) (Microsoft SQL Server, Error: 87)

For help, click: http://go.microsoft.com/fwlink?ProdName=Microsoft+SQL+Server&EvtSrc=MSSQLServer&EvtID=87&LinkId=20476

------------------------------
BUTTONS:

OK
------------------------------
```

well, you can check list the servers, by the sqlcmd command.  List shows 

```
localhost
localhost\SQLEXPRESS
```

then I figured out that there might not be a service in the location localhost\MSSQlSERVER, then I tried localhost directly and then it worked.

References

[Connect to Server :A network-related or instance-specific error [closed]](http://stackoverflow.com/questions/9185142/sql-server-2008-r2-express-permissions-cannot-create-database-or-modify-users)

## Installing the "analysis service" 

while to support deploy adn runnig the "analysis service", you have to install it, this is not something that you can get for free for the SQL Server 2008 version.  But you might be able to get from the "SQL Server 2008 version 2008 R2" version.

[Install Analysis Services in Tabular Mode][install_analysis_services_in_tabulr_mode], and [Install Analysis Services in Multidimensional and Data Mining Mode][install_analysis_services_in_multidimensional_and_data_minding_mode]

tools that might be required. 

* SQL Server Data Tools (SSDT), used to create and view Analysis Services data structures and data mining models.
* Client tools connectivity components, used for communication between clients and servers, including network libraries for DB-Library, ODBC, and OLE DB.
* Integration Services, a set of graphical and programmable objects for moving, copying, and transforming data.
* Management tools, including SQL Server Configuration Manager, SQL Server Management Studio, SQL Server Profiler, and Replication Monitor.

Referenfes:
[install_analysis_services_in_tabulr_mode]: http://msdn.microsoft.com/en-us/library/hh231722(v=sql.110).aspx
[Install Analysis Services in Tabular Mode][install_analysis_services_in_tabulr_mode]
[install_analysis_services_in_multidimensional_and_data_minding_mode]: http://msdn.microsoft.com/en-us/library/ms143708.aspx
[Install Analysis Services in Multidimensional and Data Mining Mode][install_analysis_services_in_multidimensional_and_data_minding_mode]



## Launch Windows Powershell

Click Start, type PowerShell, and then click Windows PowerShell.
From the Start menu, click Start, click All Programs, click Accessories, click the Windows PowerShell folder, and then click Windows PowerShell.


References:
[Starting Windows PowerShell](http://technet.microsoft.com/en-us/library/hh857343.aspx)
[Tip: More Powerful Ways to Launch Windows PowerShell](http://technet.microsoft.com/en-us/magazine/ff629472.aspx)

## Fusion Logs Viewer

you can use the fusion logs Viewer to debug obscure loader errors. 

[Back to Basics: Using Fusion Log Viewer to Debug Obscure Loader Errors][back_to_basic_using_fusion_log_viewer]


References
[back_to_basic_using_fusion_log_viewer]: http://www.hanselman.com/blog/BackToBasicsUsingFusionLogViewerToDebugObscureLoaderErrors.aspx
[Back to Basics: Using Fusion Log Viewer to Debug Obscure Loader Errors][back_to_basic_using_fusion_log_viewer]


## Enumerable.SequenceEqual

the Enumerable.SequenceEqual method is used to compare two sequence to see if they are equal elements by elements. A quick teset case can show you how they looks like. 

```
    class Program
    {
        private static void Main(string[] args)
        {
            var arr1 = new string[] {"hello", "world"};
            var arr2 = new string[] {"world", "hello"};

            var sequenceEqual = arr1.SequenceEqual(arr2);
            Console.WriteLine("The arr1 and arr2 SequenceEqual == {0}", sequenceEqual);
        }
    }
```


## Outlook TODO and flagged emails management

Once you got a hell lots of emails, then you would like to handle them only when you can turn around. Here is what you might do with the flagged emails. 

Flagged email is not the same as the "categoried" emails. 

1. Adda  "For Follow Up" Search folder. 


* you can add a "For Follow Up" search email by Right Click on the "Search Folder", 
* from the context menu, select "Mail Flagged for Follow up"
* Click OK

then you will find the For Follow up in the list. 


2. To quickly index those flagged email from one folder 

   1. in multiline view, click Arranged by, and then click Flag: start data or Flag: Due Date
   2. in single-line view, click the flag status colmn header


3. Find response to flagged email that you sent
   * Open the original message in the Sent item folder
   * Open the flagged sent messsage in the TO-DO bar
   * Open any e-mail message that is a response to the original message, click the Info bar, and click Open Original Flagged messages 
   
or you can 
   * Click the InfoBar, adn then click Find Related Messages.
   
References:

[Find flagged messages]: http://office.microsoft.com/en-us/outlook-help/find-flagged-messages-HA010062180.aspx
[Find flagged messages][Find flagged messages]