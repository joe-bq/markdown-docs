# Overview 
what we will be covered in this chapter in this page will include: 

* JQL (Jira Query Language) 
* Text formating Notaion Help in Jira 

Where in the jira, you can input a hand-written query for jiras matches that condition. 

the query language is called "jql", Jira Query Language .

Where you can search the source of JQL syntax from the official site, which is available from the atlassian confluence page, which is hard to open, there is a recap page on the JQL , from [IRA Query Language (JQL) Recap][jira_query_language_recap], or the most official one [JQL: The most flexible way to search JIRA][jql_most_flexible_way_to_search_jira] .

## how to use the JQL

the JQL is quite intuitive to use, where there is intelligence to guide you through when you types. 

e.g.

```
"Epic Link" = JIRA_CODE-3225
```

where when you type "Epic Link", it prompts the "Epic Link -cf[12050]"; then you hit space, it will prompt you the operators list, where you can select '=', and others.  you select the "=" then "TC: JPY S" where it prompts with "TC: JPY Swaps Day 1 - (JIRA_CODE-3225)", you can as well type in "JIRA_CODE-3225" to directly input the jira number 


## Text Formating Notation Help 
the notation is much like the formatting language used in the markdown world.

First **Headings**
here are some excerpt with some highlights. 

`h1. Biggest heading`
`h2. Bigger heading`

Second **Text Effects**

* strong text
`*strong*`

* quote text 
```
{quote}
  here is quotable
  content to be quoted 
{quote}
```

* colored text
```
{color:red}
  look ma, red text!
{color}
```

Third, **Text breaks**

* Text Breaks
`{empty line}`

* ruler 
`----` 
crate a horizontal ruler 

Fourth, **Links**

* anchor
`{anchor:anchorname}`

* link to anchor 
`[#anchor]` : link to internal anchor
`[^attachment.ext]`: link to the attachment

* user name
`[~username]`

Fifth, **lists**

* bulleted list 
```
* some
* bullet
** indented
** bullets
* points
```

* numbered list 
```
# a
# numbered

# list
```

Sixth, **Images**

* insert a image into the page 
```
!http://www.host.com/image.gif!
or
!attached-image.gif
```

* insert image thumbnails
`!image.jpg|thumbnail!`

Seventh, **Attachements**
OMITTED

Eighth, **Tables**

```
||heading 1||heading 2||heading 3||
|col A1|col A2|col A3|
|col B1|col B2|col B3|
```

Nineth, **Advanced Formatting**

* no format
```
{noformat}
preformatted piece of text
 so *no* further _formatting_ is done here
{noformat}
```

* customized panel

```
{panel:title=My Title|borderStyle=dashed|borderColor=#ccc|titleBGColor=#F7D6C1|bgColor=#FFFFCE}
a block of text surrounded with a *panel*
yet _another_ line
{panel}
```

* preformatted block of code with syntax highlighting 

```
{code:title=Bar.java|borderStyle=solid}
// Some comments here
public String getFoo()
{
    return foo;
}
{code}
```

and

```
{code:xml}
    <test>
        <another tag="attribute"/>
    </test>
{code}
```

Tenth, **Misc**

* escape 
`\X` : meaning escape character X, (i.e. {)
* emotic
`:)`



# References
[JIRA Query Language (JQL) Recap][jira_query_language_recap]
[JQL: The most flexible way to search JIRA][jql_most_flexible_way_to_search_jira]
[Text Formating Notation Help - All][text_formating_notation_help_all]

[jira_query_language_recap]: (http://blogs.atlassian.com/2013/03/jql-recap/)
[jql_most_flexible_way_to_search_jira]: http://blogs.atlassian.com/2013/01/jql-the-most-flexible-way-to-search-jira-14/ 
[text_formating_notation_help_all]: http://your.jira.com/secure/WikiRendererHelpAction.jspa?section=all

## order of lib imports in gcc/lib are importants
the order of lib imports in gcc/lib are importants.

I used to have this command line, the code is as follow.
```
rm -f ../../.ext/i386-mingw32/openssl.so
gcc -shared  -o ../../.ext/i386-mingw32/openssl.so openssl_missing.o ossl.o ossl_asn1.o ossl_bio.o ossl_bn.o ossl_cipher.o ossl_config.o ossl_digest.o ossl_engine.o ossl_hmac.o ossl_ns_spki.o ossl_ocsp.o ossl_pkcs12.o ossl_pkcs5.o ossl_pkcs7.o ossl_pkey.o ossl_pkey_dh.o ossl_pkey_dsa.o ossl_pkey_ec.o ossl_pkey_rsa.o ossl_rand.o ossl_ssl.o ossl_ssl_session.o ossl_x509.o ossl_x509attr.o ossl_x509cert.o ossl_x509crl.o ossl_x509ext.o ossl_x509name.o ossl_x509req.o ossl_x509revoked.o ossl_x509store.o -L. -L../.. -L/mingw:/local32/lib -L. -L/local32/lib -mthreads -L/mingw/lib -L/local32/lib -LC:/MinGW/local32/lib -Wl,--enable-auto-image-base,--enable-auto-import -L/mingw/lib -L/local32/lib openssl-i386-mingw32.def  -lmsvcrt-ruby210 -lcrypto -lgdi32  -lws2_32 -lwsock32  -lssl  -lgmp -lshell32 -liphlpapi -limagehlp -lshlwapi 

```

while it has error complaining that undefined referenced to `CreateDAC@16` and etc.. 

then I changed the order of -l{libs}, where the 

from 
`-lcrypto -lgdi32  -lws2_32 -lwsock32  -lssl`

to 

`-lssl -lcrypto -lws2_32  -lgdi32  -lwsock32 `

so basically I have moved -lssl, and -lcrypto in front of their dependent libraries, then the compiles just worked fine. 

References:
[ITS#5603) Linking OpenSSL on Windows requires libgdi32 and libws2_32 after libcrypto] (http://www.openldap.org/lists/openldap-bugs/200807/msg00050.html)


## pkg-config, the libs.private

you might find that the following lines in the pkg-config's config files.

```
Libs: -L${libdir} -lssl -lcrypto
Libs.private: -lws2_32 -lgdi32 -lcrypt32
```

that means, if static linked, the `-lws2_32 -lgdi32 -lcrypt32` are required, though they are not parts of libraries that are exposed by this package. 

[http://linux.die.net/man/1/pkg-conf](http://linux.die.net/man/1/pkg-conf)


## --with-opt-dir
the `--with-opt-dir` if present tells the build system where to find necessary additional library and header files. 

e.g.

```
wget-chttp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p125.tar.gz
tar zvxf ruby-1.9.3-p125.tar.gz
cd ruby-1.9.3-p125
./configure--prefix=/usr/local--enable-shared--disable-install-doc--with-opt-dir=/usr/local/lib
make&&install
```

where mine is 

```
PATH_SEPARATOR=":" ./configure --prefix=${LOCALDESTDIR} --enable-shared --disable-install-doc --with-opt-dir=/mingw/lib:${LOCALDESTDIR} && \
make && \
make install
```

References:
[ruby安装出现没有libyaml-devel的包](http://blog.csdn.net/qishiba/article/details/8175371) 


## Compiling libyaml on Windows

References:

[Compiling libyaml on Windows](http://stackoverflow.com/questions/9072178/compiling-libyaml-on-windows)
[Compile error while compiling libyaml under windows 7](http://stackoverflow.com/questions/3273486/compile-error-while-compiling-libyaml-under-windows-7)

the key is to modify the code 

```
#lif defined _WIN32
#   if defined(YAML_DECLARE_STATIC)
#       define  YAML_DECLARE(type)  type
#   elif defined(YAML_DECLARE_EXPORT)
#       define  YAML_DECLARE(type)  __declspec(dllexport) type
#   else
#       define  YAML_DECLARE(type)  __declspec(dllimport) type
#   endif                                                    
#else                                                        
#   define  YAML_DECLARE(type)  type                         
#endif
```

to 

```
#if defined(__MINGW32__)
#   define  YAML_DECLARE(type) type
#elif defined _WIN32
#   if defined(YAML_DECLARE_STATIC)
#       define  YAML_DECLARE(type)  type
#   elif defined(YAML_DECLARE_EXPORT)
#       define  YAML_DECLARE(type)  __declspec(dllexport) type
#   else
#       define  YAML_DECLARE(type)  __declspec(dllimport) type
#   endif                                                    
#else                                                        
#   define  YAML_DECLARE(type)  type                         
#endif
```


