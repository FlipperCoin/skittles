using System;
using System.IO;
using System.Threading.Tasks;

namespace Consumer.RecordsReader
{
    public class StreamReaderWorker : IDisposable
    {
        public event Action<byte[]> OnNewData;

        private const int DEFUALT_BUFFER_SIZE = 8192;

        private int _bufferSize;
        private Stream _dataStream;

        public StreamReaderWorker(Stream dataStream, int bufferSize)
        {
            _dataStream = dataStream;
        }

        public StreamReaderWorker(Stream dataStream) : this(dataStream, DEFUALT_BUFFER_SIZE) { }

        public void Run()
        {
            Task.Run(() => ReadWorker());
        }

        private void ReadWorker()
        {
            var buffer = new byte[_bufferSize];

            while (true)
            {
                int actualRead;
                try
                {
                    actualRead = _dataStream.Read(buffer, 0, _bufferSize);
                }
                catch (Exception e)
                {
                    // log, crash, whatever
                    continue;
                }

                var dataCopy = new byte[actualRead];
                Array.Copy(buffer, dataCopy, actualRead);
                OnNewData?.Invoke(dataCopy);
            }
        }

        public void Dispose()
        {
            _dataStream.Dispose();
        }
    }
}
