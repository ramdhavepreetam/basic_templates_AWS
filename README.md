# basic_templates_AWS


[ERROR]	2023-09-12T18:47:41.651Z	4019b174-a5dd-4536-965c-fcacae31086f	Unable to retrieve secret: An error occurred (AccessDeniedException) when calling the GetSecretValue operation: User: arn:aws:sts::273488500123:assumed-role/ppdusrdevpricefileextrac/ppd-dev-get-pricefilesdetails is not authorized to perform: secretsmanager:GetSecretValue on resource: ppd-dev-pricefile-modernization because no identity-based policy allows the secretsmanager:GetSecretValue action

An error occurred: expected string or bytes-like object

Invalid bucket name "ppd.dev.paricefile.bucket/Custom/DSI": Bucket name must match the regex "^[a-zA-Z0-9.\-_]{1,255}$" or be an ARN matching the regex "^arn:(aws).*:(s3|s3-object-lambda):[a-z\-0-9]*:[0-9]{12}:accesspoint[/:][a-zA-Z0-9\-.]{1,63}$|^arn:(aws).*:s3-outposts:[a-z\-0-9]+:[0-9]{12}:outpost[/:][a-zA-Z0-9\-]{1,63}[/:]accesspoint[/:][a-zA-Z0-9\-]{1,63}$"


Mon Sep 18 20:02:14 UTC 2023 : Sending request to https://lambda.us-west-2.amazonaws.com/2015-03-31/functions/arn:aws:lambda:us-west-2:273488500123:function:ppd-d-GetAllPficeFiles/invocations
Mon Sep 18 20:02:14 UTC 2023 : Received response. Status: 200, Integration latency: 449 ms
Mon Sep 18 20:02:14 UTC 2023 : Endpoint response headers: {Date=Mon, 18 Sep 2023 20:02:14 GMT, Content-Type=application/json, Content-Length=1217, Connection=keep-alive, x-amzn-RequestId=772e7fab-c608-43fc-b627-7420d5860fd1, x-amzn-Remapped-Content-Length=0, X-Amz-Executed-Version=$LATEST, X-Amzn-Trace-Id=root=1-6508acc6-56cad85c314479e284bbf023;sampled=0;lineage=852b76c4:0}
Mon Sep 18 20:02:14 UTC 2023 : Endpoint response body before transformations: {"Urls": [{"Fileurl": "https://s3.us-west-2.amazonaws.com/ppd.dev.paricefile.bucket/Custom/DSI/test.csv?AWSAccessKeyId=ASIAT7LJPKWN45YLQTW4&Signature=omi8uwVQEJXBNXfBlaMQZbVo5bY%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEMT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCICow9wEfcFXXvu3aSG6r6nazCTeq9b5JGR%2B%2FSuKELYC%2FAiAJ12%2FshxQZ4sFtSep9eOi3o829AkMRrTUzR57%2BQS7NdiqJAwit%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAMaDDI3MzQ4ODUwMDEyMyIMHb3fgIIAOyBT9r5nKt0Cnw9BJ7QbNuiDAnfywwAzxciVB4Xmzeb6In9S8FQC7y4j43zSCPLN1o35%2FtElGUkxLPshBtC7q9WBr73EU16v4IvRPwviUstWyXwpyxwEEnSkShxjMdQCtx9ZxlP2BIbFNw5olPlkXPVuA7GceR2VXVM5saev82GU11sNHUxEWLVoO1XD7YQwKCDU6J2nZ3B5hhWIR59nKDNZmkAApMztiszJKbNo8S9W%2BfU%2FThSxmFRSG4O6bi062CuLIxnySUKs9a81M6GmunONnbg%2FRriIUFdFigMFBh4eHSMCWbU5fg%2FAdfAKWXU1iQJeoYjPGQV4mH5Tl5jdyYIlWHMS3mucRY32vJdx5hAexBnk11N3MEgaYAut2g4Rs6sjOOyl2c1Q8GpoE%2FfX%2FsnKl8DBLQuB%2B%2BZqokdZtU15zK%2Fi%2F9FA0DxI7XEd0z5TEXQoBUwgTpf23HGDOdRkZzSwWVZPojCU2KKoBjqfAegkkZ9BlB6IHDllvgLYlRA [TRUNCATED]
Mon Sep 18 20:02:14 UTC 2023 : Execution failed due to configuration error: Output mapping refers to an invalid method response: 200
Mon Sep 18 20:02:14 UTC 2023 : Method completed with status: 500
