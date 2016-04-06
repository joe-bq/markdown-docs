## P/Invoke to simualate the Mouse/Keyboard movemenet 
it is allowed that you can control the move of the input device, such as the mouse, keyboard and other hardware devices. 

I will first present you a example case that moves the mouse 100 times eahc times by 10 pixels.

first let's see the WindowsApi code, it is basically the definition of the windows methods and necessary data structures. 

```
using System;
using System.Runtime.InteropServices;

namespace SendInputTest
{
    [StructLayout(LayoutKind.Sequential)]
    public struct MOUSEINPUT
    {
        public int dx;
        public int dy;
        public uint mouseData;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct KEYBDINPUT
    {
        public ushort wVk;
        public ushort wScan;
        public uint dwFlags;
        public uint time;
        public IntPtr dwExtraInfo;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct HARDWAREINPUT
    {
        public int uMsg;
        public short wParamL;
        public short wParamH;
    }

    [StructLayout(LayoutKind.Explicit)]
    public struct MouseKeybdHardwareInputUnion
    {
        [FieldOffset(0)]
        public MOUSEINPUT mi;

        [FieldOffset(0)]
        public KEYBDINPUT ki;

        [FieldOffset(0)]
        public HARDWAREINPUT hi;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct INPUT
    {
        public uint type;
        public MouseKeybdHardwareInputUnion mkhi;
    }

    [Flags]
    internal enum MOUSEEVENTF : uint
    {
        ABSOLUTE = 0x8000,
        HWHEEL = 0x01000,
        MOVE = 0x0001,
        MOVE_NOCOALESCE = 0x2000,
        LEFTDOWN = 0x0002,
        LEFTUP = 0x0004,
        RIGHTDOWN = 0x0008,
        RIGHTUP = 0x0010,
        MIDDLEDOWN = 0x0020,
        MIDDLEUP = 0x0040,
        VIRTUALDESK = 0x4000,
        WHEEL = 0x0800,
        XDOWN = 0x0080,
        XUP = 0x0100
    }

    /// <summary>
    /// TODO: Update summary.
    /// </summary>
    public static class WindowsApi
    {


        [DllImport("user32.dll", EntryPoint = "SendInput", SetLastError = true)]
        public static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

        [DllImport("user32.dll", EntryPoint = "GetMessageExtraInfo", SetLastError = true)]
        public static extern IntPtr GetMessageExtraInfo();

        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern Int32 GetLastError();

        // the version, the sample is built upon:
        [DllImport("Kernel32.dll", SetLastError = true)]
        public static extern uint FormatMessage(uint dwFlags, IntPtr lpSource,
           uint dwMessageId, uint dwLanguageId, ref IntPtr lpBuffer,
           uint nSize, IntPtr pArguments);

        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern IntPtr LocalFree(IntPtr hMem);
    }


    public static class WindowsConstants
    {
        // from header files
        public const uint FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100;
        public const uint FORMAT_MESSAGE_IGNORE_INSERTS = 0x00000200;
        public const uint FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000;
        public const uint FORMAT_MESSAGE_ARGUMENT_ARRAY = 0x00002000;
        public const uint FORMAT_MESSAGE_FROM_HMODULE = 0x00000800;
        public const uint FORMAT_MESSAGE_FROM_STRING = 0x00000400;

    }
}

```

and then the drive code, which is inside a windows forms. 

```
using System;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Windows.Forms;

namespace SendInputTest
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            var input = new INPUT();
            var mouseInput = new MOUSEINPUT();
            input.mkhi = new MouseKeybdHardwareInputUnion();


            for (int i = 0; i < 100; i++)
            {
                mouseInput.dx = 20;
                mouseInput.dy = 0;
                mouseInput.mouseData = 0;
                mouseInput.dwFlags = (uint)MOUSEEVENTF.MOVE;
                mouseInput.time = (uint)Environment.TickCount;
                mouseInput.dwExtraInfo = IntPtr.Zero;

                input.mkhi.mi = mouseInput;
                input.type = 0;
                if (Marshal.SizeOf(typeof(INPUT)) == Marshal.SizeOf(input))
                {
                    Console.WriteLine("the size of the two operations are equal!");
                }

                if (Marshal.SizeOf(typeof(uint)) == Marshal.SizeOf(typeof(int)))
                {
                    Console.WriteLine("the size of the two operations (uint) and (int) are equal!");
                }
                if (WindowsApi.SendInput(1, new INPUT[] { input }, Marshal.SizeOf(typeof(INPUT))) == 0) // size of input is the same as the Marshal.SizeOf(typeof(INPUT))
                {

                    int nLastError = WindowsApi.GetLastError();

                    IntPtr lpMsgBuf = IntPtr.Zero;
                    StringBuilder msgBuilder = new StringBuilder();
                    uint dwChars = WindowsApi.FormatMessage(
                        WindowsConstants.FORMAT_MESSAGE_ALLOCATE_BUFFER | WindowsConstants.FORMAT_MESSAGE_FROM_SYSTEM | WindowsConstants.FORMAT_MESSAGE_IGNORE_INSERTS,
                        IntPtr.Zero,
                        (uint)nLastError,
                        0, // Default language
                        ref lpMsgBuf,
                        0,
                        IntPtr.Zero);
                    if (dwChars == 0)
                    {
                        // handle the erro
                        int le = Marshal.GetLastWin32Error();
                        return;
                    }

                    string sRet = Marshal.PtrToStringAnsi(lpMsgBuf);

                    Console.WriteLine("Failed to execute SendInput, reason is {0}", sRet);

                    lpMsgBuf = WindowsApi.LocalFree(lpMsgBuf);

                    // must specify the FORMAT_MESSAGE_ARGUMENT_ARRAY flag when pass an array 

                }
                Thread.Sleep(20);
            }
        }
    }
}

```



## System.windows.Forms.Sendkeys


#### Simulate with the System.Windows.Forms.SendKeys class

To simulate the windows form key event, there is the System.windows.Forms.SendKeys class, which has the following command

* SendWait
* Send

the former is to send the event and waiting it has been processed, while the second does not wait .

You can read the [SendKeys Command][SendKeys Command] for more details on how that can be useful. to handle the key combination, there are key modifiers, which exemplified as below. 

```
p = _snapSplitter.SplitterPosition;
            SendKeys.SendWait("^{RIGHT}");
		    Assert.IsTrue(_snapSplitter.SplitterPosition < p);

		    p = _snapSplitter.SplitterPosition;
            SendKeys.SendWait("^{LEFT}");
		    Assert.IsTrue(_snapSplitter.SplitterPosition > p);
```

#### Simulate the key without the windows form context
```
[DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, uint dwExtraInfo);
```

Check more details on the following page [How can I programmatically generate keypress events in C#?][Generate KeyPress event in CSharp]

#### in wpf, the RaiseEvent method 


well, you can try to simulate a single key stroke with the followign 

```
var key = Key.Insert;                    // Key to send
  var target = Keyboard.FocusedElement;    // Target element
  var routedEvent = Keyboard.KeyDownEvent; // Event to send

  target.RaiseEvent(
    new KeyEventArgs(
      Keyboard.PrimaryDevice,
      PresentationSource.FromVisual(target),
      0,
      key)
    { RoutedEvent=routedEvent }
  );
```

While, the RaiseEvent method is handy, there are some limitation associated with it.

> Using target.RaiseEvent(...) sends the event directly to the target without meta-processing such as accelerators, text composition and IME. This is normally what you want. On the other hand, if you really do what to simulate actual keyboard keys for some reason, you would use InputManager.ProcessInput() instead.
>  or you want to invoke accelerators for which you need InputManager.ProcessEvent. But normally you don't want to do this. 

the second quote means that the RaiseEvent method does not handle the Accelerators 

#### InputManager.ProcessInput

```
			//Cannot find a way to send Ctrl + Keys, so cannot test MoveCommand
		    p = _snapSplitter.SplitterPosition;
		    InputManager.Current.PrimaryKeyboardDevice.Modifiers = ModifierKeys.Control;
		    InputManager.Current.ProcessInput(
		        new InputEventArgs(Keyboard.PrimaryDevice, 0)
		            {
		                RoutedEvent = Keyboard.KeyDownEvent,
		                Source = PresentationSource.FromVisual(_snapSplitter),
		                Handled = false,
                        
		            });
```

While the KeyEventArgs and other are subclass to the InputEventArgs (KeyEventArgs -> KeyboardEventArgs -> InputEventArgs).

the real problem is there is no way to set the modifier keys.. 

there is a excellent post that teaches you a tip, which reads like this:  [How To Send Multiple Keystrokes From Code Behind][how_to_send_multiple_keystrokes_from_code_behind]

to use that code, you can to the following. 

```
 var modKey = ModifierKeys.Control;
        var device = new MYKeyboardDevice(InputManager.Current)
        {
            ModifierKeysImpl = modKey
        };
        var keyEventArgs = device.CreateKeyEventArgs(Key.Tab, modKey);
```
while the codethat the authro has shared is as follow. 

```
public sealed class MYKeyboardDevice : KeyboardDevice
    {
        private sealed class MYPresentationSource : PresentationSource
        {
            Visual _rootVisual;

            protected override CompositionTarget GetCompositionTargetCore()
            {
                throw new NotImplementedException();
            }

            public override bool IsDisposed
            {
                get { return false; }
            }

            public override Visual RootVisual
            {
                get { return _rootVisual; }
                set { _rootVisual = value; }
            }
        }

        private static RoutedEvent s_testEvent = EventManager.RegisterRoutedEvent(
                "Key Event",
                RoutingStrategy.Bubble,
                typeof(MYKeyboardDevice),
                typeof(MYKeyboardDevice));

        public ModifierKeys ModifierKeysImpl;

        public MYKeyboardDevice()
            : this(InputManager.Current)
        {

        }

        public MYKeyboardDevice(InputManager manager)
            : base(manager)
        {

        }

        protected override KeyStates GetKeyStatesFromSystem(Key key)
        {
            var hasMod = false;
            switch (key)
            {
                case Key.LeftAlt:
                case Key.RightAlt:
                    hasMod = HasModifierKey(ModifierKeys.Alt);
                    break;
                case Key.LeftCtrl:
                case Key.RightCtrl:
                    hasMod = HasModifierKey(ModifierKeys.Control);
                    break;
                case Key.LeftShift:
                case Key.RightShift:
                    hasMod = HasModifierKey(ModifierKeys.Shift);
                    break;
            }

            return hasMod ? KeyStates.Down : KeyStates.None;
        }

        public KeyEventArgs CreateKeyEventArgs(
            Key key,
            ModifierKeys modKeys = ModifierKeys.None)
        {
            var arg = new KeyEventArgs(
                this,
                new MYPresentationSource(),
                0,
                key);
            ModifierKeysImpl = modKeys;
            arg.RoutedEvent = s_testEvent;
            return arg;
        }

        private bool RaiseEvents(UIElement target, RoutedEventArgs e, params RoutedEvent[] routedEventArray)
        {
            foreach (var routedEvent in routedEventArray)
            {
                e.RoutedEvent = routedEvent;
                target.RaiseEvent(e);
                if (e.Handled)
                {
                    return true;
                }
            }

            return false;
        }

        private bool HasModifierKey(ModifierKeys modKey)
        {
            return 0 != (ModifierKeysImpl & modKey);
        }
    }
```

Here is my code, 

```
internal sealed class MyKeyboardDevice : KeyboardDevice
	    {
	        public MyKeyboardDevice(InputManager manager) : base(manager)
	        {
	        }

	        public ModifierKeys ModifierKeysImpl { get; set; }

	        protected override KeyStates GetKeyStatesFromSystem(Key key)
	        {
	            var hasMod = false;
	            switch (key)
	            {
	                case Key.LeftAlt:
                    case Key.RightAlt:
	                    hasMod = HasModifierKey(ModifierKeys.Alt);
	                    break;
                    case Key.LeftCtrl:
                    case Key.RightCtrl:
	                    hasMod = HasModifierKey(ModifierKeys.Control);
	                    break;
                    case Key.LeftShift:
                    case Key.RightShift:
	                    hasMod = HasModifierKey(ModifierKeys.Shift);
	                    break;
	            }

	            return hasMod ? KeyStates.Down : KeyStates.None;
	        }

	        private bool HasModifierKey(ModifierKeys modKey)
	        {
	            return 0 != (ModifierKeysImpl & modKey);
	        }
	    }

	}
```

and the test case is as follow. 

```
		    p = _snapSplitter.SplitterPosition;
		    var device = new MyKeyboardDevice(InputManager.Current) { ModifierKeysImpl = ModifierKeys.Control };

		    _snapSplitter.RaiseEvent(
		        new KeyEventArgs(device, PresentationSource.FromVisual(_snapSplitter), 0, Key.Right)
		            {
		                RoutedEvent = Keyboard.KeyDownEvent
		            });
		    device.ModifierKeysImpl = ModifierKeys.None;

		    Assert.IsTrue(_snapSplitter.SplitterPosition > p);
```


References
[SendKeys Command]: http://msdn.microsoft.com/en-us/library/8c6yea83(v=vs.84).aspx
[SendKeys Command][SendKeys Command]

[Generate KeyPress event in CSharp]: http://stackoverflow.com/questions/1645815/how-can-i-programmatically-generate-keypress-events-in-c
[How can I programmatically generate keypress events in C#?][Generate KeyPress event in CSharp]

[how_to_send_multiple_keystrokes_from_code_behind]: http://stackoverflow.com/questions/21899329/how-to-send-multiple-keystrokes-from-code-behind
[How To Send Multiple Keystrokes From Code Behind][how_to_send_multiple_keystrokes_from_code_behind]


## types sizes within P/Invoke

there are some common confusion when using the windows API. 

first uint and int are the same size, they are alias to the Int32 and UInt32 respectively 

but there are difference in terms of the pointer types, the IntPtr type is a system dependent reference type, which is 4 bytes long in 32 bit system, and 8 bytes long in 64 bites system. the UIntPtr is different, which is always 4 bytes long in all platforms (we don't consider the 16 bites systems).
