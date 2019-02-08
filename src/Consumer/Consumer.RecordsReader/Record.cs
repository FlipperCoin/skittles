using System;

namespace Consumer.RecordsReader
{
    public class Record
    {
        public ArraySegment<byte> Header { get; }
        public ArraySegment<byte> Bytes { get; }

        public Record(ArraySegment<byte> header, ArraySegment<byte> bytes)
        {
            Header = header;
            Bytes = bytes;
        }
    }
}