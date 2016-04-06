## Introduction 
this page will shows you a program that I wrote that can do the transformation of certain archived (any byte stream) into a png file.. 


# implementation
the main principle of the program is as such 
1. you can create an in-memory Bitmap object, which can save directly with png format, or you can just load a file which is compatible from a file.
2. we ignore the alpha channel
3. the first pixel (0, 0) stores the size of the orignal file
3. when gen PNG, we set pix by pix by converting each adjacent three bytes into RGB
4. when restore from PNG, we read file size and get each pixel's RGB and write 3 bytes (or less) to the output stream


First we have the MainWindow.xaml

```
<Window x:Class="PngGen.MainWindow"
				xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
				xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
				Title="MainWindow" Height="350" Width="525">
		<Grid>
		<Grid.RowDefinitions>
			<RowDefinition />
			<RowDefinition />
			<RowDefinition />
		</Grid.RowDefinitions>

		<Grid.ColumnDefinitions>
			<ColumnDefinition />
			<ColumnDefinition />
		</Grid.ColumnDefinitions>


		<Label x:Name="InputLabel" Content="Input:" Grid.Row="0" Grid.Column="0"/>
		<TextBox x:Name="Input" Text="{Binding Input}" Grid.Row="0" Grid.Column="1" />

		<Label x:Name="OutputLabel" Content="Output:" Grid.Row="1" Grid.Column="0"/>
		<TextBox x:Name="Output" Text="{Binding Output}" Grid.Row="1" Grid.Column="1" />


		<Button x:Name="Gen" Content="Generate" 
			Command="{Binding GenCommand}"
			Grid.Column="0"
			Grid.Row="2"
			/>

		<Button x:Name="Deflate" Content="Deflate" 
			Command="{Binding DeflateCommand}"
			Grid.Column="1"
			Grid.Row="2" />
		</Grid>
</Window>
```

then we define the MainViewModel

```
using System;
using System.ComponentModel;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.CompilerServices;
using System.Windows.Input;
using System.IO;

namespace PngGen
{
	public class MainViewModel : INotifyPropertyChanged
	{
		#region Fields 
		private string _input;
		private string _output;
		private ICommand _genCommand;
		private ICommand _deflateCommand;
		#endregion

		#region Properties
		public string Input
		{
			get
			{
				return _input;
			}

			set
			{
				if (_input != value)
				{
					_input = value;
					OnPropertyChanged();
					
				}
			}
		}

		public string Output
		{
			get
			{
				return _output;
			}

			set
			{
				if (_output != value)
				{
					_output = value;
					OnPropertyChanged();
				}
			}
		}

		public ICommand GenCommand
		{
			get
			{
				return _genCommand;
			}
		}

		public ICommand DeflateCommand
		{
			get
			{
				return _deflateCommand;
			}
		}
		#endregion

		#region Constructor(s)
		public MainViewModel()
		{
			_genCommand = new RoutedCommand();
			_deflateCommand = new RoutedCommand();
		}
		#endregion

		#region Public Method 
		public void Gen()
		{
			// More details on how to generate PNG file with C# - http://stackoverflow.com/questions/4585016/generate-a-png-file-with-c-sharp
			// first we need to judge if the Input and output are valid
			if (string.IsNullOrEmpty(Input))
			{
				return;
			}

			if (string.IsNullOrEmpty(Output))
			{
				return;
			}

			if (!File.Exists(Input))
			{
				return;
			}


			var inputInfo = new FileInfo(Input);
			var bytesInput = inputInfo.Length;


			var dots = (bytesInput + 2) / 3 + 1;
			var width = (int)Math.Ceiling(Math.Sqrt(dots));

			Bitmap bmp = new Bitmap(width, width);
			// Seems that Graphics does not offer the SetPixel methods
			//Graphics g = Graphics.FromImage(bmp);
			//g.
			
			// first dot (3 bytes to show the size)... 
			bmp.SetPixel(0, 0, FileLengthToColor((int)bytesInput));

			int xpos = 1;
			int ypos = 0;

			using (FileStream inputStream = File.OpenRead(Input))
			{
				byte[] b = new byte[3];
				int bytesRead = 0;
				while ((bytesRead = inputStream.Read(b, 0, b.Length)) > 0)
				{
					for (int j = bytesRead; j < 3; j++)
					{
						b[j] = 0;
					}
					
					bmp.SetPixel(xpos, ypos, Color.FromArgb(b[0], b[1], b[2]));
					if ((++xpos) >= width)
					{
						ypos++;
						xpos = 0;
					}
				}
			}

			bmp.Save(Output, ImageFormat.Png);

			// create Graphics
			//FileInfo fo = new FileInfo(Output);
			//FileStream fstr = fo.Create();
			//bmp.Save(fstr, ImageFormat.Png);
			//fstr.Close();
			
		}


		// the reverse of gen - method
		public void Deflate()
		{
			// first we need to judge if the Input and output are valid
			if (string.IsNullOrEmpty(Input))
			{
				return;
			}

			if (string.IsNullOrEmpty(Output))
			{
				return;
			}

			if (!File.Exists(Input))
			{
				return;
			}


			Bitmap bmp = new Bitmap(Input);
			Color color = bmp.GetPixel(0, 0);
			var fileLength = ColorToFileLength(color);
			var width = bmp.Width;

			int xpos = 1;
			int ypos = 0;

			long byteToWrite = fileLength;
			FileStream fo = File.Create(Output);
			byte[] b = new byte[3];
			while (byteToWrite > 0)
			{
				color = bmp.GetPixel(xpos, ypos);
				b[0] = color.R;
				b[1] = color.G;
				b[2] = color.B;
				fo.Write(b, 0, (int)Math.Min(3, byteToWrite));
				if ((++xpos) >= width)
				{
					ypos++;
					xpos = 0;
				}

				byteToWrite -= 3;
			}

			fo.Close();
		}

		private Color FileLengthToColor(int length)
		{
			//Color color = Color.FromArgb(length & ((~0 >> 16) & 0xFF), length & ((~0 >> 8) & 0xFF), length & 0xFF);
			Color color = Color.FromArgb((length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF);

			return color;
		}

		private long ColorToFileLength(Color color)
		{
			long length = (color.R << 16) | (color.G << 8) | color.B;
			return length;
		}


		#endregion

		public event PropertyChangedEventHandler PropertyChanged;

		protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
		{
			PropertyChangedEventHandler handler = PropertyChanged;
			if (handler != null)
			{
				handler(this, new PropertyChangedEventArgs(propertyName));
			}
		}
	}
}


```


in the code-behind file for MainWindow, we have the following

```
using System.Windows;
using System.Windows.Input;

namespace PngGen
{
	public partial class MainWindow : Window
	{
		public MainWindow()
		{
			InitializeComponent();

			var viewModel = new MainViewModel();
			DataContext = viewModel;
			CommandBindings.Add(new CommandBinding(viewModel.GenCommand, new ExecutedRoutedEventHandler((x, y) => viewModel.Gen())));
			CommandBindings.Add(new CommandBinding(viewModel.DeflateCommand, new ExecutedRoutedEventHandler((x, y) => viewModel.Deflate())));
		}

	}
}

```


References
[Generate a PNG file with C# - Stack Overflow](http://stackoverflow.com/questions/4585016/generate-a-png-file-with-c-sharp)
[c# - Reading a PNG image file in .Net 2.0 - Stack Overflow](http://stackoverflow.com/questions/100247/reading-a-png-image-file-in-net-2-0)