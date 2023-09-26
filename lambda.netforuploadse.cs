using Amazon.Lambda.Core;
using Amazon.SecretsManager;
using Amazon.SecretsManager.Model;
using Amazon.S3;
using Npgsql;
using Newtonsoft.Json.Linq;
using System;
using System.Data;
using System.IO;
using System.Text;

[assembly: LambdaSerializer(typeof(Amazon.Lambda.Serialization.SystemTextJson.DefaultLambdaJsonSerializer))]

public class Function
{
    private const string SecretId = "ppd-dev-pricefile-modernization";

    public JObject GetSecrets()
    {
        using var client = new AmazonSecretsManagerClient();
        var response = client.GetSecretValue(new GetSecretValueRequest { SecretId = SecretId });
        return JObject.Parse(response.SecretString);
    }

    public string GetConnectionString(JObject secrets)
    {
        return $"Host={secrets["host"]};Username={secrets["user"]};Password={secrets["password"]};Database={secrets["dbname"]};Port={secrets["port"]}";
    }

    public void CreateS3Folder(DataTable allData, string dealerID, string bucketName)
    {
        var output = new StringBuilder();
        foreach (DataRow row in allData.Rows)
        {
            for (var i = 0; i < allData.Columns.Count; i++)
            {
                output.Append(row[i].ToString() + ",");
            }
            output.Length--; // Remove the last comma
            output.AppendLine();
        }

        using var client = new AmazonS3Client();
        var folderName = $"{dealerID}_{DateTime.Now:yyyy_MM_dd}";
        var s3Key = $"{folderName}/ITEM.csv";

        var putRequest = new Amazon.S3.Model.PutObjectRequest
        {
            BucketName = bucketName,
            Key = s3Key,
            ContentBody = output.ToString()
        };
        client.PutObject(putRequest);
    }

    public object LambdaHandler(ILambdaContext context)
    {
        var secrets = GetSecrets();
        var connectionString = GetConnectionString(secrets);

        using var conn = new NpgsqlConnection(connectionString);
        conn.Open();
        
        var cmd = new NpgsqlCommand("SELECT distinct \"DEALER_CODE\" FROM ppdglobal.\"DEALER_MASTER\"", conn);
        var adapter = new NpgsqlDataAdapter(cmd);
        
        var initialData = new DataTable();
        adapter.Fill(initialData);

        foreach (DataRow row in initialData.Rows)
        {
            var dealerCode = row[0].ToString().Replace(" ", string.Empty);
            var secondaryQuery = $"SELECT * FROM PPDGLOBAL.\"DCPP0113C\" DD WHERE DD.\"ITMID\" IN ((SELECT DC.\"ITMID\" FROM PPDGLOBAL.\"DCPP0115\" DC WHERE  DC.\"CSTNO\" = '{dealerCode}'))";
            var secondaryCmd = new NpgsqlCommand(secondaryQuery, conn);
            var secondaryAdapter = new NpgsqlDataAdapter(secondaryCmd);
            
            var secondaryData = new DataTable();
            secondaryAdapter.Fill(secondaryData);

            CreateS3Folder(secondaryData, dealerCode, secrets["BucketName"].ToString());
        }

        conn.Close();

        return new 
        {
            statusCode = 200,
            body = "Data successfully uploaded to S3!"
        };
    }
}
