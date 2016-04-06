
## Linux Shell variable related

there is a wonderful primer on the shell variable related article here: 

https://developer.apple.com/library/mac/documentation/opensource/conceptual/shellscripting/shell_scripts/shell_scripts.htmlf


where in a summary, in a Bourne shell, you will need to do the following 

1. overriding a variable starting a child process 
   VARIABLE=VALUE command
2. set variable
   VARIABLE=VALUE
3. export the variable
   export VARIABLE=VALUE # the =VARIABLE part can be omitted


while if you are workingw with a CShell, here is what you might need to do

1. overriding a variable in a child process 
   env VARIABLE-VALUE command
2. set an variable
   set VARIABLE=VALUE
3. export the variable
   setenv VARIABLE

## Lists goals/targets in Makefile

It is usually required to know which targets/goals are available in the Makefile, then you may try the following 

1. make -pn (meaning make --print-data-base --dry-run)
2. make help (if the Makefile itself has provides some way to print the online documentation)

check the references here for details: 
   
http://stackoverflow.com/questions/3063507/list-goals-targets-in-gnu-make


also, if you are interested in what `standard targets' are available in the autoconf, automake, there are available in the documentation 

http://www.gnu.org/software/automake/manual/html_node/Standard-Targets.html

where quote:

Here is a list of the most useful targets that the GNU Coding Standards specify.

>make all
Build programs, libraries, documentation, etc. (same as make).

>make install
    Install what needs to be installed, copying the files from the package’s tree to system-wide directories.
    
>make install-strip
    Same as make install, then strip debugging symbols. Some users like to trade space for useful bug reports...
    
>make uninstall
    The opposite of make install: erase the installed files. (This needs to be run from the same build tree that was installed.)
    
>make clean
    Erase from the build tree the files built by make all.
    
>make distclean
    Additionally erase anything ./configure created.
    
>make check
Run the test suite, if any.

>make installcheck
Check the installed programs or libraries, if supported.

>make dist
Recreate package-version.tar.gz from all the source files.


## Understanding the pkg-config use and etc.

http://www.chenjunlu.com/2011/03/understanding-pkg-config-tool/

please check out the link above, it turns out to be quite useful. 

## resolve the conflicting types for `int8_t`

while compiling the nasm to the mingw system, I found that there is a conflict types to the int8_t types. 


the offending file is 

1. inttypes.h 
typedef signed char int8_t;


2. while in the sys/types.h
typedef char int8_t;

to resolve this I have to explicitly change the typedef in the inttypes.h files in order to make them in sync.
