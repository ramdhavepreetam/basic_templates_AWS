Here is one way to convert the Python code to C# for .NET Core:

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Amazon.SecretsManager;
using Amazon.SecretsManager.Model;
using Amazon.S3;
using Amazon.S3.Model;
using Npgsql;

public class Function 
{
  private static IAmazonSecretsManager secretsClient;
  private static IAmazonS3 s3Client;
  
  public async Task<string> FunctionHandler(SNSEvent evnt, ILambdaContext context)
  {
    try 
    {
      var secrets = await GetSecrets("secretID");
      
      var dbParams = new NpgsqlConnectionStringBuilder{
        Host = secrets["host"],
        Port = int.Parse(secrets["port"]),
        Username = secrets["user"],
        Password = secrets["password"],
        Database = secrets["dbname"]
      };

      using(var conn = new NpgsqlConnection(dbParams.ConnectionString)) {
        conn.Open();
      
        var initialData = await FetchData(conn, "SELECT DISTINCT dealer_code FROM dealer_master");
        
        foreach(var row in initialData) {
          var dealerCode = row[0];
          
          var query = $"SELECT * FROM dcpp0113c dd WHERE dd.itmid IN (SELECT dc.itmid FROM dcpp0115 dc WHERE dc.cstno = '{dealerCode}')";
          
          var data = await FetchData(conn, query);
          
          await CreateS3File(data, dealerCode, secrets["bucketName"]);
        }
      }

      return "Done!";
      
    } catch(Exception ex) {
      return ex.Message; 
    }
  }

  private async Task<Dictionary<string, string>> GetSecrets(string secretId)
  {
    var response = await secretsClient.GetSecretValueAsync(new GetSecretValueRequest 
    {
      SecretId = secretId
    });

    return JsonConvert.DeserializeObject<Dictionary<string, string>>(response.SecretString);
  }

  private async Task<List<string[]>> FetchData(NpgsqlConnection conn, string query)
  {
    using(var cmd = new NpgsqlCommand(query, conn))
    using(var reader = await cmd.ExecuteReaderAsync()) {
      var results = new List<string[]>();
      while(await reader.ReadAsync()) {
        var values = new string[reader.FieldCount];
        reader.GetValues(values);
        results.Add(values);
      }
      return results;
    }
  }

//...

private async Task CreateS3File(List<string[]> data, string dealerId, string bucketName)  
{
  var folderName = $"{dealerId}_{DateTime.UtcNow:yyyy_MM_dd}";
  var key = $"{folderName}/data.csv";

  using (var writer = new StringWriter())
  {
    using (var csv = new CsvWriter(writer, System.Globalization.CultureInfo.InvariantCulture))
    {
      foreach (var row in data)
      {
        csv.WriteField(row);
        csv.NextRecord();
      }
    }

    var contents = writer.ToString();

    // upload to S3
  }
}

}
```

The key differences:

- Use C# async/await for async operations instead of Python's async framework
- Convert Python libraries to .NET equivalents (Npgsql instead of psycopg2, AWSSDK instead of boto3, System.IO instead of io, etc.)
- Dictionary instead of Python dict for secrets 
- String interpolation with $ for queries instead of f-strings
- Use C# CSV helper instead of Python CSV module
- Handle exceptions differently since no try/except blocks in C# async methods

Let me know if any part needs more explanation!
