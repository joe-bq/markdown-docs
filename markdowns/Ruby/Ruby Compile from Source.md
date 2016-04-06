


## Install Ruby gems locally
you will first need to download the gem files with a computer that has the gem..

[Installing gems with no network](http://help.rubygems.org/kb/rubygems/installing-gems-with-no-network)

Normally it will involves the necessary steps as follow 

```
$ gem install rails -i repo --no-rdoc --no-ri
```

and copy it somewhere that you can take away 
```
$ cp -r repo/cache /path/to/USB_drive/gems
```
then install the gems on teh destination machine from the local files.

```
$ cd /path/to/USB_drive/gems
$ gem install --force --local *.gem
```

you might need to deal with the platform, here is how you can get information about the platforms.

```
$ gem env
```

then when you install, you can do this with the `--platform` option.

```
$ gem install nokogiri --platform x86-mswin32-60 -i repo --no-rdoc --no-ri
```
my real example would be something like below. 

```
gem install railties-4.0.4.gem --platform x86-mswin32-100 --no-rdoc --no-ri --local --force
```

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

while you have to be careful that 

1. the debug version of the output is **libwapid.** rather than **libwapi** that is required by the ruby compilation
2. you won't like to define the constants */DZLIB_WINAPI* or similar because that will gives you the **__stdcall** calling convention, and that you won't be able to correctly compile the sources. 

one spcial notes 

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


## Installing the Sqlite

### preparation

what you will need is 

1. the sqlite C source code (amalgation)
2. the sqlite compiled windows dll files. (to extract the def files) 
3. the sqlite3-1.3.9.gem files to install native gems
4. sqlite3-ruby gem files


### 1 unzip the Sqlite C header file

to prepare for the header, you can unzip it to somewhere controlled by **--with-sqlite3-dir** , which shall have a **lib** and a **include** directory to contains the libraries and the header respectively. 

also, there is a default include directory, *c:/ProgramFiles/Ruby193/include/ruby-1.9.1*, you can put the header there.

for your reference, you can guess from the output 

C:\ProgramFiles\Ruby193\lib\ruby\gems\1.9.1\gems\sqlite3-1.3.9\ext\sqlite3\mkmf.log

```
"cl -nologo -Ic:/ProgramFiles/Ruby193/include/ruby-1.9.1/i386-mswin32_100 -Ic:/ProgramFiles/Ruby193/include/ruby-1.9.1/ruby/backward -Ic:/ProgramFiles/Ruby193/include/ruby-1.9.1 -I. -Ic:/ProgramFiles/Ruby193/include/sqlite-3.8.4    -MD -Zi -W2 -wd4996 -we4028 -we4142 -O2sy-  -Zm600 -W3   -c conftest.c"
```

### 2. extract the .def file

we need the .def file to build the .lib file

you can extract the .def file from a .dll ,the command to execute is 

```dumpbin /exports sqlite3.dl```

then modify the output to get some thing like 

```
EXPORTS
symbol1
symbol2
; ... this is a comment

```

### 3 . create an empty VC project to build

you will add the .c files and the .h files to the project, and you will need to add the *sqlite3.def* file as the input, do this via *Linker -> Input -> Module definition file* 


you will first need to download the source files and the binaries files of the sqlite.

better download the amalgation one, which has only four files, compile faster, and run faster.

you may need to define those two constants

* THREADSAFE
* SQLITE_ENABLE_COLUMN_METADATA

### 4. install the gems

```
C:\Temp\repo\cache\gems>gem install --platform x86-mswin32-100 --no-rdoc --no-ri
 sqlite3-1.3.9.gem -- --with-sqlite3lib=c:/ProgramFiles/Ruby193/lib/ruby/site_ru
by/1.9.1/i386-msvcr100/sqlite3 --with-sqlite3-include=c:/ProgramFiles/Ruby193/in
clude/sqlite-3.8.4
```

reference

[Compiling SQLite on Windows](http://eli.thegreenplace.net/2009/09/23/compiling-sqlite-on-windows/)

## Compile the Ruby-2.1.1 itself
you will first set the following variables

1. LIBPATH=%LIBPATH%;path_to_openssl_lib;path_to_zlib_lib;
2. LIB=%LIB%;path_to_openssl_lib;path_to_zlib_lib;
3. INCLUDE=%INCLUDE%;path_to_openssl_topheader;path_to_zlib_headers
4. PATH=%PATH%;path_to_openssl_dll;path_to_zlib_dll;

## install rails

if you are behind some firewall which prevent you from downloading gems from within the corporate environmnets, still you have an option, the options is to download the gem files one by one locally and store it somewhere. 

the gem files list that I have installed is as follow 

```
actionmailer (4.0.4)
actionpack (4.0.4)
activemodel (4.0.4)
activerecord (4.0.4)
activerecord-deprecated_finders (1.0.2)
activesupport (4.0.4)
arel (4.0.0)
atomic (1.1.16)
bigdecimal (1.1.0)
builder (3.1.4)
bundler (1.5.3)
coffee-rails (4.0.0)
coffee-script (2.2.0)
coffee-script-source (1.7.0)
erubis (2.7.0)
execjs (2.0.2)
hike (1.2.3)
i18n (0.6.9)
io-console (0.3)
jbuilder (1.2.0)
jquery-rails (3.1.0)
json (1.8.1, 1.5.5)
mail (2.5.4)
mime-types (1.16)
minitest (4.2.0, 2.5.1)
multi_json (1.9.2)
polyglot (0.3.1)
rack (1.5.2)
rack-test (0.6.2)
rails (4.0.4)
railties (4.0.4)
rake (0.9.2.2)
rdoc (4.0.1, 3.9.5)
sass (3.2.0)
sass-rails (4.0.2)
sdoc (0.4.0)
sprockets (2.8.0)
sprockets-rails (2.0.0)
sqlite3 (1.3.9)
thor (0.19.1)
thread_safe (0.1.3)
tilt (1.1)
treetop (1.4.8)
turbolinks (2.2.1)
tzinfo (0.3.37)
uglifier (1.3.0)
```

while, downloading this does not mean the job is done.  you will have to test if you can launch the rails server. 

you will first need to create a new rails application, by issuing one of the following commands.  

```
work> rails new demo
```

then you can enter the application's base directory and start the new rails server. with the following commands.

```
work> cd demo
demo> rails server
```

if everything starts up correctly, you can type the following to the browser's address 

```
http://localhost:3000
```

however, if everything just go such smoothly then there would be no doubt that we don't bother to create such a page to dedicate such set up 

### undefined method `default_mime_type=' for Sprockets::JstProcessor:Class (NoMethodError)

this happens when I have the sprocket-2.8.0. it turns out the reason for the fail is that there missing one methods declaration. 

It was first discussed here on this mail thread [Starting rails server](https://groups.google.com/forum/#!msg/rubyonrails-talk/3TWXtLd4P-0/G47W4WREfzsJ), then followed that thread, we can traced down to this thread, which is a github fix commit, which has the following. [sstephenson / sprockets](https://github.com/sstephenson/sprockets/commit/743c1b1a6433195e440e2d863e5d4767cc41271a)

the key is to remove the line such as 

```
- self.default_mime_type = 'application/javascript'
```

and add this one

```
   def self.default_mime_type
     'application/javascript'
   end
```


### TZInfo/TZInfo-data error

you may have the tzinfo or the tzinfo-data error, something like that the

```
 No timezone data source could be found. To resolve this, either install TZInfo::Data (e.g. by running
```


to resolve the issue, we can do the following

1. add the gem entry for tzinfo-data to the Gemfile (work/demo/Gemfile)
```
# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem 'tzinfo-data', '~> 1.2014.2'

# https://github.com/rails/rails/issues/13553 
gem 'tzinfo', '~> 1.1.0'
```

2. add the require statements to the Environment.rb file

```
require 'tzinfo'
require 'tzinfo/data'
```


### references:

[Windows: No timezone data source could be found](https://github.com/middleman/middleman/issues/1097) [# Uninitialized Constant TZInfo::InvalidTimezoneIdentifier (NameError) - Rails ](http://stackoverflow.com/questions/20713472/uninitialized-constant-tzinfoinvalidtimezoneidentifier-nameerror-rails-4)



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

## install MySql

you can install MySql through the zip file or through the MSI installer. 


### Install the MySQL services

after you have added the mysqld in the service through the following commands,

    c:\ProgramFiles\mysql-5.6.17\bin\mysqld --install
    
then you can find MySQL appears in the `services.msc` control panel

Admmonition: you can add the path to MySQL to the environmental variables.

    set MYSQL_HOME=c:\ProgramFiles\mysql-5.6.17
    set PATH=%PATH%;%MYSQL_HOME%\bin


after the installation of the MySQL service, you an now start the service with 

    net start MySQL

### Remove the service manually 

First you can stop the MySQL services, here is what you can do 

    net stop MySQL

after that you can remove the services.

    c:\ProgramFiles\mysql-5.6.17\bin\mysqld --remove 

REMEMBER, do run the above commands when you are in the directory of the mysql binaries.

### references

[Installing MySQL on Microsoft Windows Using a noinstall Zip Archive](http://dev.mysql.com/doc/refman/5.7/en/windows-install-archive.html)

## JRuby and Rails

where from the references page, you can do the following to create the rails server. 

    jruby -S rails new testapp -d mysql -m http://jruby.org/rails3.rb 

You might need to do that via the windows bash shell. (not sure why we need to do thatt..)

after the install is complete, you will need to do the following. 

    open config\database.yml 

### References
[安装jruby和rails，创建 application](http://wj196.iteye.com/blog/980490)

## JDBC adapter cannot work with mysql

while from the referenced page, there is a post 

    development:
    adapter: jdbc
    driver: com.mysql.jdbc.Driver
    username: [username]
    password: [password]
    url: jdbc:mysql://localhost:3306/[db_name]

Reference:
[cannot load Java class com.mysql.jdbc.Driver](https://github.com/jruby/activerecord-jdbc-adapter/issues/302)

while I have added the following to the 'Gemfile'

    gem 'jdbc-msyql', '5.1.30'
    
## JCE (Java Cryptography Extensions) 

as stated in  
    Deploying With JRUby

there is a warning that 

    OpenSSL::Cipher::CipherError: Illegal key size: possibly you need to install Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files for your JRE

> If you see this error it means you need to install the unrestricted policy files for the JVM. You can find these at the Oracle Website. Download the zip file, and extract the two important files it contains: local_policy.jar and US_export_policy.jar. Move these files into your $JAVA_HOME/jre/lib/security directory, and replace the existing files of the same name.  On Mac OS X they are probably located here:

References:
[Deploying with JRuby](http://deployingjruby.blogspot.hk/2013/05/how-to-run-rails-400rc1-on-jruby.html)
[Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files 7 Download](http://www.oracle.com/technetwork/java/javase/downloads/jce-7-download-432124.html)
