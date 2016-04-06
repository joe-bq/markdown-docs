## introduction 

this page collects some common


http://stackoverflow.com/questions/2463822/threading-errors-with-application-loadcomponent-key-already-exists


threading errors with Application.LoadComponent (key aready exists problem)


The problem is that whenever Application.LoadComponent loads a "Part" from a "Package" it:

Checks its internal cache for the package to see if the part is already loaded & returns it if found
Loads the part from the file
Adds it to the internal cache
Returns it
You have two threads calling Application.LoadComponent to load the same part at the same time. The MSDN documentation says this is ok, but what is happening is:

Thread #1 checks the cache and starts loading from the file
Thread #2 checks the cache and starts loading from the file
Thread #1 finishes loading from the file and adds to the cache
Thread #2 finishes loading from the file and tries to add to the cache, resulting in a duplicate key exception