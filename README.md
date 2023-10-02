# basic_templates_AWS


[ERROR]	2023-09-12T18:47:41.651Z	4019b174-a5dd-4536-965c-fcacae31086f	Unable to retrieve secret: An error occurred (AccessDeniedException) when calling the GetSecretValue operation: User: arn:aws:sts::273488500123:assumed-role/ppdusrdevpricefileextrac/ppd-dev-get-pricefilesdetails is not authorized to perform: secretsmanager:GetSecretValue on resource: ppd-dev-pricefile-modernization because no identity-based policy allows the secretsmanager:GetSecretValue action

An error occurred: expected string or bytes-like object

Invalid bucket name "ppd.dev.paricefile.bucket/Custom/DSI": Bucket name must match the regex "^[a-zA-Z0-9.\-_]{1,255}$" or be an ARN matching the regex "^arn:(aws).*:(s3|s3-object-lambda):[a-z\-0-9]*:[0-9]{12}:accesspoint[/:][a-zA-Z0-9\-.]{1,63}$|^arn:(aws).*:s3-outposts:[a-z\-0-9]+:[0-9]{12}:outpost[/:][a-zA-Z0-9\-]{1,63}[/:]accesspoint[/:][a-zA-Z0-9\-]{1,63}$"

import json

def lambda_handler(event, context):
    # ... your code ...

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({"message": "Hello World"})
    }




SELECT 
    -- List the specific columns you need instead of *
    DD.someColumn,
    DC.anotherColumn,
    DM.yetAnotherColumn
FROM 
    PPDGLOBAL."DCPP0113C" DD 
JOIN 
    PPDGLOBAL."DCPP0115" DC ON DD."ITMID" = DC."ITMID"
JOIN 
    PPDGLOBAL."DEALER_MASTER" DM ON DC."CSTNO" = DM."DEALER_CODE"
WHERE 
    DM."DBS" = 'DSI';


vThe error you are getting indicates there is an issue with how memory is being accessed in your C program. Specifically:

- The error mentions an invalid space offset of X'FFFFFFFF' or X'0000000000000000'. This refers to trying to access memory at address 0xFFFFFFFF or 0x00000000, which are likely invalid addresses.

- It mentions this offset is outside the current limits for object ACV18_SD01ACPASI. This ACV18_SD01ACPASI seems to refer to some kind of memory region your program is trying to access.

Some things to check that could be causing this:

- Array/pointer out of bounds - accessing an array or pointer past its allocated memory, causing it to try to access invalid addresses. Check array indexes and pointer arithmetic.

- Uninitialized pointers - using uninitialized pointers that point to invalid addresses. Ensure all pointers are initialized before use.

- Stack/heap corruption - some other part of the code corrupted the stack or heap, causing the memory addresses to become invalid. Use memory debugging tools like valgrind or AddressSanitizer to check for issues.

- Stack overflow - if the stack grows too large it can collide with heap or other memory regions, causing invalid accesses. Check for infinite recursion or very large stack allocations. 

- Memory region issues - mismatch between how the program and linker map memory regions could cause invalid accesses. Ensure memory regions match.

Overall this indicates some invalid memory access. Carefully audit memory usage throughout the program - allocations, array accesses, pointer arithmetic, etc. A memory debugging tool can help pinpoint the line causing the invalid access.
