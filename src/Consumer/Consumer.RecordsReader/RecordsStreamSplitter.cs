using System;
using System.Collections.Generic;
using System.Text;

namespace Consumer.RecordsReader
{
    public class RecordsStreamSplitter
    {
        public event Action<ArraySegment<byte>> OnNewSplit;

        private const byte DEFAULT_NEW_RECORD_DELIM = 0x0A;

        private byte _newRecordDelim;
        private ArraySegment<byte> _partialRecord;

        public RecordsStreamSplitter(byte newRecordDelim)
        {
            _newRecordDelim = DEFAULT_NEW_RECORD_DELIM;
        }

        public RecordsStreamSplitter() : this(DEFAULT_NEW_RECORD_DELIM)
        {

        }

        public void HandleData(byte[] data)
        {
            int startOfRecord = 0;

            if (_partialRecord != default)
            {
                var newData = new byte[_partialRecord.Count + data.Length];
                Array.Copy(_partialRecord.Array, _partialRecord.Offset, newData, 0, _partialRecord.Count);
                Array.Copy(data, 0, newData, _partialRecord.Count, data.Length);
                
                data = newData;
                _partialRecord = default;
            }

            for (int i = 0; i < data.Length; i++)
            {
               if (data[i] == _newRecordDelim)
                {
                    OnNewSplit?.Invoke(
                        new ArraySegment<byte>(data, startOfRecord, i - startOfRecord)
                    );
                    startOfRecord = i + 1;
                }
            }

            // There's a partial record at the end of the data
            if (startOfRecord < data.Length)
            {
                _partialRecord = new ArraySegment<byte>(data, startOfRecord, data.Length - startOfRecord);
            }
        }
    }
}
