## Introduction
This page will introduce you one home-made implementation of Home made Double buffer implementation.


## implementation

well, the key idea is in pre-load, it should load 2 * MaxBufferSize, and only when the file size > 2 * MaxSize then will it tries to read through the files circularly.


```

using System;
using System.Collections.Generic;
using System.IO;
using TIBCO.Rendezvous;

namespace FeedApp.Drivers
{
    public class DataInput : IDisposable
    {
        #region Logger
        //private Message[] _messages;
        private List<Message> _messages = new List<Message>();
        private string _input; // the full path to the Data input file
        private FileStream _inputFs;
        private StreamReader _inputSr;
        private int _curPos;
        private readonly TibcoMessageDecoder _decoder;

        private Message[] _foregroundBuffer;
        private Message[] _backgroundBuffer;

        private int _curBufPos;

        private const int MaxBufferSize = 1000;
        private int _foregroundBufferSize;
        private int _backgroundBufferSize;
        private int _prefetchedBufferPos;
        private int _prefetchedBufferSize;
        private int _backgroundBufferPos;
        #endregion

        #region Constructor(s)
        public DataInput()
        {
            _decoder = new TibcoMessageDecoder();
        }
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
                _input = value;
            }

        }

        #endregion

        #region Methods

        public void LoadAll()
        {
            Check();

            if (_inputSr == null)
            {
                _inputSr = new StreamReader(_inputFs);
            }

            if (_foregroundBufferSize == 0)
            {
                LoadNext();
            }

            while (!_inputSr.EndOfStream)
            {
                string line = _inputSr.ReadLine();
                if (line != null)
                {
                    line = line.TrimEnd();
                    Message msg = _decoder.Decode(line);
                    _messages.Add(msg);
                }
            }
        }

        private void Check()
        {
            if (string.IsNullOrEmpty(_input))
            {
                throw new ApplicationException("Input not set");
            }

            if (!File.Exists(BaseDir.Instance.GetFullPath(Input)))
            {
                throw new ApplicationException(string.Format("Input '{0}' not found!", _input));
            }
        }

        public void Initialize()
        {
            Check();
            if (_inputFs == null)
            {
                _inputFs = File.OpenRead(BaseDir.Instance.GetFullPath(_input));
            }

            if (_inputSr == null)
            {
                _inputSr = new StreamReader(_inputFs);
            }

            if (_foregroundBufferSize == 0)
            {
                LoadNext();
            }
        }

        public Message Next()
        {
            if (_curBufPos >= _foregroundBufferSize)
            {
                LoadNext();
                SwitchForeground();
            }

            if (_curBufPos < _foregroundBufferSize)
            {
                return _foregroundBuffer[_curBufPos++];
            }

            return null;
        }


        private void LoadNext() // load once at most 2 * BufferSize...
        {
            _prefetchedBufferSize = 0;
            _prefetchedBufferPos = 0;
            
            List<Message> messages = new List<Message>();

            int maxFetch = MaxBufferSize;
            if (_foregroundBufferSize == 0)
                maxFetch += MaxBufferSize;

            LoadBuffer(messages);

            int lastBackgroundBufferSize = _backgroundBufferSize;

            if (_inputSr.EndOfStream && _prefetchedBufferPos < maxFetch && lastBackgroundBufferSize == MaxBufferSize)
            {
                // we need to reset the Stream
                // how to reset a stream reader
                // http://stackoverflow.com/questions/831417/how-do-you-reset-a-c-sharp-net-textreader-cursor-back-to-the-start-point
                _inputSr.BaseStream.Position = 0;
                _inputSr.DiscardBufferedData();

                // Continue to read 
                LoadBuffer(messages);
            }


            if (_foregroundBufferSize == 0)
            {
                if (_foregroundBuffer == null)
                {
                    _foregroundBuffer = new Message[Math.Min(MaxBufferSize, _prefetchedBufferSize)];
                }

                for (_prefetchedBufferPos = 0; _prefetchedBufferPos < _prefetchedBufferSize && _prefetchedBufferPos < MaxBufferSize; ++_prefetchedBufferPos)
                {
                    _foregroundBuffer[_prefetchedBufferPos] = messages[_prefetchedBufferPos];
                }

                _foregroundBufferSize = _prefetchedBufferPos;
            }

            //int i = 0;
            _backgroundBufferPos = 0;
            if (_backgroundBuffer == null)
            {
                int expectedSize = Math.Min(_prefetchedBufferSize - _prefetchedBufferPos, MaxBufferSize);
                if (expectedSize > 0)
                {
                    _backgroundBuffer = new Message[expectedSize];
                }
            }
            for (; _prefetchedBufferPos < _prefetchedBufferSize && _backgroundBufferPos < MaxBufferSize; ++_prefetchedBufferPos, ++_backgroundBufferPos)
            {
                _backgroundBuffer[_backgroundBufferPos] = messages[_prefetchedBufferPos];
            }
            _backgroundBufferSize = _backgroundBufferPos;

        }

        private void LoadBuffer(List<Message> messages)
        {
            int maxFetch = _foregroundBufferSize == 0 ? 2 * MaxBufferSize : MaxBufferSize;
            while (!_inputSr.EndOfStream && _prefetchedBufferSize < 2 * maxFetch)
            {
                string line = _inputSr.ReadLine();
                if (line != null)
                {
                    line = line.TrimEnd();
                    Message msg = _decoder.Decode(line);
                    // only rest the stream
                    messages.Add(msg);
                    _prefetchedBufferSize++;
                }
            }
        }

        public void SwitchForeground()
        {
            if (_backgroundBufferSize != 0)
            {
                Message[] temp = _foregroundBuffer;
                _foregroundBuffer = _backgroundBuffer;
                _backgroundBuffer = temp;
                int tempSize = _foregroundBufferSize;
                _foregroundBufferSize = _backgroundBufferSize;
                _backgroundBufferSize = tempSize;

                _curBufPos = 0;
            }
            else
            {
                //. reset the foreground
                _curBufPos = 0;
            }
        }
        #endregion

        public void Dispose()
        {
            if (_inputSr != null)
            {
                _inputSr.Dispose();
                _inputSr = null;
            }
        }
    }
}

```