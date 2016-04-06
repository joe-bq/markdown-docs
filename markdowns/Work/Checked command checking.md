first there is a command called "CheckedComand" 


which is from the *Common.Commands* namespace, and the command is as such 

```
using System;
using System.Windows.Input;

namespace Common.Commands
{
    public abstract class CheckedCommand : ICommand
    {
        protected CheckedCommand(Predicate<object> canExecute)
        {
            _canExecute = canExecute;
        }

        public virtual void Execute(object parameter)
        {}

        private readonly Predicate<object> _canExecute;

        // todo - use a method similar to that used in the Dispose pattern, so this gets called automatically
        public virtual bool CanExecute(object parameter)
        {
            return _canExecute == null || _canExecute(parameter);
        }

        public event EventHandler CanExecuteChanged
        {
            add { CommandManager.RequerySuggested += value; }
            remove { CommandManager.RequerySuggested -= value; }
        }
    }
}
```

the key here is the command that has the 
```
        public event EventHandler CanExecuteChanged
        {
            add { CommandManager.RequerySuggested += value; }
            remove { CommandManager.RequerySuggested -= value; }
        }
```

where it is a ICommand's member which is going to be implemented, 
while it detects if there need to check the "CanExecuteChanged".

the `CheckedCommand` is inherted by the commands 
`SimpleActionCommandBase` then by the comand called `MarkitWireTransferCommand` ... that is a lot of commands that shall be executed. 

