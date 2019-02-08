using System;
using System.Collections.Generic;
using System.Text;

namespace Consumer.RecordsReader
{
    public class RecordsParser : IRecordsParser
    {
        private ArraySegment<byte> _header;

        public void ParseHeader(ArraySegment<byte> header)
        {
            _header = header;
        }

        public Record ParseRecord(ArraySegment<byte> record)
        {
            return new Record(_header, record);
        }
    }
}
