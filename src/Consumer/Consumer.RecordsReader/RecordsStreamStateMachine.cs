using System;
using System.Collections.Generic;
using System.Text;

namespace Consumer.RecordsReader
{
    public class RecordsStreamStateMachine
    {
        public event Action<Record> OnNewRecord;

        private bool _isHeaderInitialized = false;
        private IRecordsParser _parser;

        public RecordsStreamStateMachine(IRecordsParser parser)
        {
            _parser = parser;
        }

        public RecordsStreamStateMachine() : this(new RecordsParser())
        {

        }

        public void HandleRecord(ArraySegment<byte> record)
        {
            if (!_isHeaderInitialized)
            {
                _parser.ParseHeader(record);
            }

            Record parsedRecord = _parser.ParseRecord(record);
        }
    }
}
