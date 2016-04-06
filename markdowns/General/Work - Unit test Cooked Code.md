## Setup AppContext to test


well, the key are 

* Store
* ConfigContext
* AppContext
* ConfigElement
* Codecs

check through the code below

```

var store = new InMemoryConfigStore();
            var ordrTemplConf = new ConfigElement();
            var ordTemplConfig = new OrderTicketGridTemplateConfig();
            ordTemplConfig.GridLayoutConfig = new GridDescriptorDefinition();
            ordTemplConfig.GridLayoutConfig.Layouts = new List<GridLayoutDefinition>(new [] {new GridLayoutDefinition() { Columns = new List<ColumnDescriptorDefinition>()}, });
            ordrTemplConf.Category = ordTemplConfig.Category;
            ordrTemplConf.Id = "default";
            ordrTemplConf.XmlConfigData = _test_codecs.Encode(ordTemplConfig).Root;

            store.Add(ordrTemplConf);

            var orderConfig = new OrderTicketConfig();
            var orderConfigElem = new ConfigElement();

            orderConfig.DepthGridDefinition = new GridDescriptorDefinition();
            orderConfig.DepthGridDefinition.Layouts = new List<GridLayoutDefinition>(new[] { new GridLayoutDefinition() {Columns = new List<ColumnDescriptorDefinition>()}, });

            orderConfigElem.Category = orderConfig.Category;
            orderConfigElem.Id = "default";
            orderConfigElem.XmlConfigData = _test_codecs.Encode(orderConfig).Root;
            store.Add(orderConfigElem);

            var accountConfig = new AccountsConfig();
            var accountConfigElem = new ConfigElement();
            accountConfig.DefaultAccount = new Account() { GMI = "NH36151", Name = "AGY NF" };
            accountConfig.AccountList = new List<Account>(new[] { accountConfig.DefaultAccount, new Account() { GMI = "NH36253", Name = "JV FLIES" }, new Account() { GMI = "NH36147", Name = "JV OIS" }, new Account() { GMI = "NH36254", Name = "PP OIS"}});
            accountConfigElem.Category = accountConfig.Category;
            accountConfigElem.Id = "default";
            accountConfigElem.XmlConfigData = _test_codecs.Encode(accountConfig).Root;
            
            store.Add(accountConfigElem);

            var basicConfigContext = new BasicConfigContext(store, null);
            basicConfigContext.Initialise();

            _test_appContext = new AppContext("test-dummy", "Test", AppEnvironment.Test, AppLocation.America, basicConfigContext);
```

Well, you can ignore the store parts and just add Item to the AppContext directly but the InMemoryStore does help you avoid issues such as saving back to network.


## initialize the appcontext from ConfigStore

AppContext can have a IConfigContext, with which you can read config off the config server. Well, the IConfigContext depends on the AppContext, this is a chick and egg issue... how to do the initialization?

```
      ManualResetEvent waitOne = new ManualResetEvent(false);
      AppContext appContext = new AppContext(null, "ecommerce", AppEnvironment.Staging, AppLocation.America, null);
      ConfigClient client = new ConfigClient(appContext);
      client.Ready += (o, args) => waitOne.Set();
          
      waitOne.WaitOne();
      appContext.RootContext.UserCredentials = new UserCredentials("user-name", null, new User("user-name")); 

      var bsCofigContext = new BasicConfigContext(new ServerConfigStore(client), new ServerConfigQuery() { Path = ConfigPath.Create("App-Execution")});
      bsCofigContext.Initialise();
```

here there are two places where needs your attention
1. ConfigClient has a Ready event, only after the ready event fires will the data loaded from the config server
2. BasicConfigContext does the talk to the Config server, how to enable that? after ConfigClient has properly initalized then you will be doing the BasicConfigContext.Initialise() methods


