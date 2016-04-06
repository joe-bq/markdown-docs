## Introduction

this page will show you how to use the Sublime more accurately


## Tools-tip: how to do Column Selection in Sublime text

it is called [Column Selection][column_selection]

also, welcome to check out the various [Useful shortcuts][submlime_useful_shortcut]

References:
[column_selection]: https://www.sublimetext.com/docs/2/column_selection.html
[submlime_useful_shortcut]: https://gist.github.com/lucasfais/1207002


## SublimeCodeIntel configuration
well you can configure the SublimeCodeIntel 's configuartion on the code completion.
here is the skeleton for you to configure the code completion. 

to locate the configuration file path, it is ~/.codeintel/config 


```

{
        "PHP": {
            "php": '/usr/bin/php',
            "phpExtraPaths": [],
            "phpConfigFile": 'php.ini'
        },
        "JavaScript": {
            "javascriptExtraPaths": []
        },
        "Perl": {
            "perl": "/usr/bin/perl",
            "perlExtraPaths": []
        },
        "Ruby": {
            "ruby": "/usr/bin/ruby",
            "rubyExtraPaths": []
        },
        "Python": {
            "python": '/usr/bin/python',
            "pythonExtraPaths": []
        },
        "Python3": {
            "python": '/usr/bin/python3',
            "pythonExtraPaths": []
        }
    }
    
```

and an live example would be mine like this: 

```
{
  "Python": {
    "python":"C:/Python27/python.exe",
    "pythonExtraPaths": [
       "C:/Python27",
       "C:/Python27/Lib",
       "C:/Python27/DLLs",
       "C:/Python27/libs",
       "C:/Python27/Scripts"
       "C:/Python27/Lib/site-packages"
  ]},
  "Ruby": {
    "ruby":"c:/ProgramFiles/JRuby/jruby-1.7.12/jruby.exe",
    "rubyExtraPaths": [
        "C:/ProgramFiles/JRuby/jruby-1.7.12/lib/ruby/1.9/site_ruby", 
        "C:/ProgramFiles/JRuby/jruby-1.7.12/lib/ruby/shared",
        "C:/ProgramFiles/JRuby/jruby-1.7.12/lib/ruby/1.9"
    ]
  }
}
```
well, this is not entirely true,  I hvae modified the config which is in-effective 

```
{
    "Python":  {
        "python": "C:/Python27/python.exe",
        "pythonExtraPaths": ["C:/Python27", "C:/Python27/Lib", "C:/Python27/DLLs", "C:/Python27/libs", "C:/Python27/Lib/site-packages"]
    },
    "Ruby":  {
        "ruby": "C:/ProgramFiles/JRuby/jruby-1.7.12/bin/jruby.exe",
        "rubyExtraPaths": ["C:/ProgramFiles/JRuby/jruby-1.7.12/lib/ruby/1.9/site_ruby", "C:/ProgramFiles/JRuby/jruby-1.7.12/lib/ruby/shared", "C:/ProgramFiles/JRuby/jruby-1.7.12/lib/ruby/1.9"]
    }
}
```

Please be noticed that you won't be able to get Auto completion if you are not opening a project by opening a folder. 


Reference:

[sublime_codeinte_auto_completion]: http://www.thefourtheye.in/2013/05/sublime-configuring-codeintel.html
[Sublime Configuring CodeIntel Auto Completion][sublime_codeinte_auto_completion]
[rubyextrapaths_not_giving_completion]: https://github.com/SublimeCodeIntel/SublimeCodeIntel/issues/248
[RubyExtraPaths not giving completion][rubyextrapaths_not_giving_completion]