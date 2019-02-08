using Consumer.RecordsReader;
using System;
using System.Net.Sockets;

namespace Consumer.Console
{
    class Program
    {
        private const string SERVER_HOST_NAME = "SERVER_HOST_NAME";
        private const string SERVER_PORT = "SERVER_PORT";

        private const string SERVER_HOST_NAME_DEFAULT = "records-loadbalancer";
        private const string SERVER_PORT_DEFAULT = "32000";

        static void Main(string[] args)
        {
            string serverHostName = getEnvVar(SERVER_HOST_NAME, SERVER_HOST_NAME_DEFAULT);
            int serverPort = int.Parse(getEnvVar(SERVER_PORT, SERVER_PORT_DEFAULT));

            var client = new TcpClient(serverHostName, serverPort);
            var sockStream = client.GetStream();
            
            var streamReaderWorker = new StreamReaderWorker(sockStream);
            var recordsStreamSplitter = new RecordsStreamSplitter();
            var recordsStreamStateMachine = new RecordsStreamStateMachine();

            recordsStreamStateMachine.OnNewRecord += HandleNewRecord;
            recordsStreamSplitter.OnNewSplit += recordsStreamStateMachine.HandleRecord;
            streamReaderWorker.OnNewData += recordsStreamSplitter.HandleData;

            streamReaderWorker.Run();
        }

        private static void HandleNewRecord(Record obj)
        {
            
        }

        private static string getEnvVar(string key, string defaultValue)
        {
            try
            {
                return Environment.GetEnvironmentVariable(key) ?? defaultValue;
            }
            catch (Exception e)
            {
                return defaultValue;
            }
        }
    }
}
