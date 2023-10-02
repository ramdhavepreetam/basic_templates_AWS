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


Based on the additional context, here are some specific things I would look at to debug the invalid memory access error:

- Check the data queue access - the QRCVDTAQ and QSNDDTAQ functions are used to receive/send from the data queues. Make sure the queue names, keys, and buffer sizes are configured correctly.

- Validate ebcdic/ascii conversion - the TO_ASCII and TO_EBCDIC macros convert between ascii and ebcdic. Make sure the source buffers are large enough to hold the converted output.

- Analyze buffer sizes - many fixed size stack buffers are used, like bufferOut, BufferIn, BufferRet. Check that input data does not exceed these sizes.

- Review socket communication - the recv and send calls are used to communicate with the socket. Make sure the receive buffer is large enough and not overflowed.

- Use memory debugging tools - as mentioned previously, tools like valgrind and AddressSanitizer can help identify the line of code causing the invalid access.

- Add bounds checking - use asserts or other checks to validate array/buffer accesses are within bounds. This can quickly identify any issues.

- Simplify the problem - try to reduce the program to a small repro case that has the same error. This simplifies debugging.

Focus the investigation on the memory usage at the interfaces between components - the data queues, ebcdic/ascii conversion, socket communication, etc. The issue likely lies in one of those areas mishandling memory. Auditing and adding checks to the memory usage can help uncover any bugs.

Based on the additional context, here are some specific things I would look at to debug the invalid memory access error:

- Check the data queue access - the QRCVDTAQ and QSNDDTAQ functions are used to receive/send from the data queues. Make sure the queue names, keys, and buffer sizes are configured correctly.

- Validate ebcdic/ascii conversion - the TO_ASCII and TO_EBCDIC macros convert between ascii and ebcdic. Make sure the source buffers are large enough to hold the converted output.

- Analyze buffer sizes - many fixed size stack buffers are used, like bufferOut, BufferIn, BufferRet. Check that input data does not exceed these sizes.

- Review socket communication - the recv and send calls are used to communicate with the socket. Make sure the receive buffer is large enough and not overflowed.

- Use memory debugging tools - as mentioned previously, tools like valgrind and AddressSanitizer can help identify the line of code causing the invalid access.

- Add bounds checking - use asserts or other checks to validate array/buffer accesses are within bounds. This can quickly identify any issues.

- Simplify the problem - try to reduce the program to a small repro case that has the same error. This simplifies debugging.

Focus the investigation on the memory usage at the interfaces between components - the data queues, ebcdic/ascii conversion, socket communication, etc. The issue likely lies in one of those areas mishandling memory. Auditing and adding checks to the memory usage can help uncover any bugs.


Based on your suspicion that the ascii to ebcdic conversion of the reply message may be causing the issue, here are some things I would focus on:

- Carefully review the GetMessage() function that does the reply message conversion - look for any bugs in the logic or buffer handling.

- Print out the reply message length before and after conversion to validate the input/output sizes match expectations.

- Use a debugger or add additional logging to trace the execution and buffer sizes through the conversion step.

- Try simplifying by removing the ascii to ebcdic conversion entirely and just passing the ascii data through. Does the memory issue still happen?

- Make sure the reply buffer passed to GetMessage() is initialized and large enough to hold the converted output.

- Double check the logic in the TO_EBCDIC macro itself and verify it can handle the input length.

- Look for any cases where the input reply message could contain unexpected or invalid data that could trigger a bug.

- Try restructuring the logic to first convert into a temporary buffer, validate the size, then copy to the final output buffer.

- Consider switching from macros to functions to better encapsulate the conversion logic.

Isolating the reply message handling and conversion logic will help determine if that is the root cause. You can also use memory debugging tools to validate if any invalid accesses happen during the TO_EBCDIC call itself. A simplified test case focused just on the reply message handling may make the issue more apparent.
