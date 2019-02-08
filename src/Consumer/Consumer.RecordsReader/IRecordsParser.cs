using System;

namespace Consumer.RecordsReader
{
    public interface IRecordsParser
    {
        void ParseHeader(ArraySegment<byte> header);
        Record ParseRecord(ArraySegment<byte> record);
    }
}