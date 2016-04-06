IN the GuiToolkit.DevExpress code base, there is a new change to use the ApplicationTheme theeme, the code is to load the RowStyle and CellStyle from the .xaml file with the ThemeManager way, here is the code inthe DxExtensions.cs file .


```
        internal static readonly ResourceDictionary ResourceDictionaryApplicationTheme
            = new ResourceDictionary { Source = new Uri("/GuiToolkit.DevExpress;component/Themes/ApplicationTheme/Resources.xaml", UriKind.Relative) };


        internal static Style RowStyle
        {
            get
            {
                if (ThemeManager.ApplicationThemeName == "ApplicationTheme")
                {
                    return (Style)ResourceDictionaryApplicationTheme["rowStyle"];
                }

                return (Style)ResourceDictionary["rowStyle"];
            }
        }
        
```

and inside the Resources. _/GuiToolkit.DevExpress;component/Themes/ApplicationTheme/Resources.xaml_ , the content is defined as such

```
    <Style x:Key="rowStyle"
      BasedOn="{StaticResource {dxgt:GridRowThemeKey ThemeName=ApplicationTheme, ResourceKey=RowStyle}}"
      TargetType="dxg:GridRowContent"/>

```

it has a special ThemeName property inside the "GridRowThemeKey" extension. So that it requires the explicit theme to be installed before the use of the theme. the code that does the install is as such .

```
using System;
using System.Linq;
using DevExpress.Xpf.Core;

namespace Desktop.Themes.ApplicationTheme.DevExpress
{
    public static class Installer
    {
        public static void Install()
        {
            if (Theme.Themes.FirstOrDefault(t => t.Name == "ApplicationTheme") == null)
            {
                var theme = new Theme("ApplicationTheme", "/DevExpress.Xpf.Themes.ApplicationTheme.v13.1;component/Themes/Generic.xaml") { FullName = "Application Theme", AssemblyName = "DevExpress.Xpf.Themes.ApplicationTheme.v13.1" };
                Theme.RegisterTheme(theme);
            }
            
            ThemeManager.ApplicationThemeName = "ApplicationTheme";
        }

        public static void UnInstall()
        {
            ThemeManager.ApplicationThemeName = Theme.Default.Name;
        }
    }
}
```

from the code above, it is create a theme by giving a name "ApplicationTheme" to the theme's by its main xaml file "/DevExpress.Xpf.Themes.ApplicationTheme.v13.1;component/Themes/Generic.xaml", be watchful to the special name of the URL that is provided to the ThemeManager.

From the Optic container code, it has those code that does the THeme installation. 

```
		public static void AddThemesDictionary(string themeName, string resourceName)
		{
			// If a theme was specified, load the resource dictionaries for it.
			if (String.IsNullOrWhiteSpace(themeName))
			{
				return;
			}

			try
			{
				//Call installer for ThemeManager install
                if (resourceName == ThemesHelper.MainResource || resourceName == ThemesHelper.SplashScreenResource)
				{
					string assemblyName = string.Format("Desktop.Themes.{0}.DevExpress", themeName);
					var assembly = AppDomain.CurrentDomain.GetAssemblies().FirstOrDefault(a => a.GetName().Name == assemblyName);
					if (assembly != null)
					{
						var type = assembly.GetType(assemblyName + ".Installer");
						if (type != null)
						{
							var method = type.GetMethod("Install");
							if (method != null && method.GetParameters().Length == 0)
							{
								method.Invoke(null, null);
							}
						}
					}
				}

				var themePath = String.Format("/Optic.Core;component/Themes/{0}/{1}", themeName, resourceName);

				var themeUri = new Uri(themePath, UriKind.RelativeOrAbsolute);

				var dictionary = new ResourceDictionary { Source = themeUri };
				Application.Current.Resources.MergedDictionaries.Add(dictionary);
			}
			// ReSharper disable EmptyGeneralCatchClause
			catch { /* for now, ignore any load issues */ }
			// ReSharper restore EmptyGeneralCatchClause
		}

```
basically it uses reflectionto find and call the .Install method we show above. Onething we should be watchful is when the Install method is called.

First, when the splashscreen window, there are call to the _AddThemesDictionary_

```
        protected override void OnStartup(StartupEventArgs e)
        {
			// Let WPF do its thing first.
			base.OnStartup(e);

			// Name this thread.
			Thread.CurrentThread.Name = Resx.ThreadNameUI;

			// Parse the incoming arguments.
			var commandLineParser = new AeonCommandLineParser<OpticStartupParameters>(e.Args);

            ...
            
			//
        	var commandLine = ProcessCommandLine();
			if (commandLine == null)
			{
				Environment.Exit(1);
			}

			// Adjust the preferred culture if necessary. We need to do this before any visual
			// elements are shown (including the splash screen).
			//
        	SetCulture(commandLine.Culture);

			m_themeName = commandLine.Theme;
			ThemesHelper.AddThemesDictionary(m_themeName, ThemesHelper.SplashScreenResource);

			// If any preload XAML resources were specified, load them before launching
			// the splash screen.
			//
			if (!String.IsNullOrWhiteSpace(commandLine.PreloadResourcesUri))
			{
				try
				{
					var preloadUri = new Uri(commandLine.PreloadResourcesUri, UriKind.RelativeOrAbsolute);
					var dictionary = new ResourceDictionary { Source = preloadUri };
					Resources.MergedDictionaries.Add(dictionary);
				}
// ReSharper disable EmptyGeneralCatchClause
				catch { /* for now, ignore any load issues */ }
// ReSharper restore EmptyGeneralCatchClause
			}

            // Construct and display the splash screen.
            //
        	var title = commandLineParser.StartupParameters.Title;
        	var subtitle = commandLineParser.StartupParameters.Subtitle;
			if (String.IsNullOrWhiteSpace(subtitle))
				subtitle = String.Format("Framework Version {0}", Assembly.GetEntryAssembly().GetName().Version); 
			var splash = new GtkSplash.SplashScreen(title, subtitle);

			// Set up a handler for dispatcher exceptions.
			//
            Current.DispatcherUnhandledException += Current_DispatcherUnhandledException;

            // Tell MEF to find all the IBootstrap objects.
            splash.ProgressMessage = "Finding bootstraps ...";
            CompositionHost.Instance.ComposeParts(this);

            if (DomApplication.CommandLine.NoSplash != true)
            {
                splash.Show();
            }

            // Initialize DomApplication
            splash.ProgressMessage = "Initialising application ...";
            DomApplication.Initialise(this);
			if (DomApplication.RootAppContext == null)
			{
				splash.Close();
				Environment.Exit(1);
			}

			DispatcherHelper.DoEvents();

		    ...

            // Find packages specified in component definitions and request from ReCAP if necessary. 
            var packages = GetPackages();
            if (packages.Count() == 0 || commandLine.NoRecapMode.GetValueOrDefault())
            {
                ContinueStartup(splash, e);
            }
            else
            {
                UpdateRecapPackages(packages, splash, e);
            }
        }

```


There are call to the _AddThemesDictionary_ before the `splash.Show()` call, things looks all right, and then the code should goes to the `ContinueStartup(splash, e)`, which has 

```
        private void ContinueStartup(GtkSplash.SplashScreen splash, StartupEventArgs e)
        {
            // Fire off the bootstraps in priority order
            try
            {
                try
                {
                    if (Bootstraps != null)
                    {
                        splash.ProgressMessage = "Bootstrapping ...";

                        foreach (var b in Bootstraps.OrderBy(b => b.Metadata.BootstrapPriorityOrder))
                        {

                            var bootstrap = b.Value;

                            splash.ProgressMessage = "Bootstrapping " + bootstrap.Name + " ...";
                            var splash1 = splash;
                            bootstrap.BootstrapProgressUpdate +=
                                (s, a) => splash1.ProgressMessage = bootstrap.Name + ": " + a.Message;

                            if ((m_shuttingDown) || (Current == null))
                            {
                                // If we are shutting down or something has happened during startup to cause the application to have started a shutdown
                                return;
                            }

                            bootstrap.Bootstrap(this);
                        }
                    }
                }
                catch (ReflectionTypeLoadException ex)
                {
                   ...
                }
                catch (InvalidOperationException ex)
                {
                   ...
                }
            }
            catch (Exception ex)
            {
               ...
            }

			ThemesHelper.AddThemesDictionary(m_themeName, ThemesHelper.MainResource);

			// If any XAML resources were specified, load them before showing the shell.
			//
			if (!String.IsNullOrWhiteSpace(DomApplication.CommandLine.LoadResourcesUri))
			{
				try
				{
					var loadUri = new Uri(DomApplication.CommandLine.LoadResourcesUri, UriKind.RelativeOrAbsolute);
					var dictionary = new ResourceDictionary { Source = loadUri };
					Resources.MergedDictionaries.Add(dictionary);
				}
				// ReSharper disable EmptyGeneralCatchClause
				catch { /* for now, ignore any load issues */ }
				// ReSharper restore EmptyGeneralCatchClause
			}

			splash.ProgressMessage = "Opening main window ...";

            // Kick-off the main window
            if ((DomApplication.Workspace != null) && (DomApplication.Workspace.IsRibbonEnabled))            
            {
                IRibbonBasedMainWindow rbmw = RibbonBasedMainWindow.Value;

                if (rbmw == null)
                {
                    s_log.Error("Ribbon specified in workspace, but no suitable main window implementation available.");
                	MainWindow = CreateShell();
                }
                else
                {
                    MainWindow = rbmw.MainWindow;
                }
            }
            else
            {
                MainWindow = CreateShell();
            }

            MainWindow.Show();
        	m_mainWindowShown = true;

            splash.Close();
            base.OnStartup(e);
		}

```

as you can see before the Splash window is closed, there is a call to `ThemesHelper.AddThemesDictionary(m_themeName, ThemesHelper.MainResource);`
It all sounds reasonable, but it has thrown the exception as follow

```
  InnerException: 
       Message=Cannot find resource named 'GridRowThemeKeyExtension_RowStyle'. Resource names are case sensitive.
       Source=PresentationFramework
       StackTrace:
            at System.Windows.StaticResourceExtension.ProvideValueInternal(IServiceProvider serviceProvider, Boolean allowDeferredReference)
            at System.Windows.StaticResourceExtension.ProvideValue(IServiceProvider serviceProvider)
            at MS.Internal.Xaml.Runtime.ClrObjectRuntime.CallProvideValue(MarkupExtension me, IServiceProvider serviceProvider)
       InnerException: 
```

Please check the 
[CustomizingMissing DevExpress resource when loading the Grid][Missing_DevExpress_Resource_When_Loading_the_Grid]

> This problem appears because the theme defined in the ThemeManager.ApplicationThemeName property is not applied to any element until the Window is loaded, so the corresponding theme resources aren't loaded.

I guess the reason is that we need to install/set the theme before the application shown any UI element.

## References

[Missing DevExpress resource when loading the Grid](http://www.devexpress.com/Support/Center/Question/Details/Q521500)
[Customizing_TableView_RowStyle_With_Style_And_DevExthemes]:  http://devexpress.com/Support/Center/Question/Details/Q365533
[Customizing_TableView_RowStyle_With_Style_And_DevExthemes](http://devexpress.com/Support/Center/Question/Details/Q365533)
[Missing_DevExpress_Resource_When_Loading_the_Grid]: http://devexpress.com/Support/Center/Question/Details/B212124
[Missing DevExpress resource when loading the Grid](http://devexpress.com/Support/Center/Question/Details/B212124)