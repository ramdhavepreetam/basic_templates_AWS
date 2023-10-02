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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 1
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
100 /***********************************************/ 10/30/06
200 /* Header files needed to use the sockets API. */ 10/30/06
300 /* File contains Macro, Data Type and */ 10/30/06
400 /* Structure definitions along with Function */ 10/30/06
500 /* prototypes. */ 10/30/06
600 /***********************************************/ 10/30/06
700 /* in qcle/h file */ 10/30/06
800 #include <stdio.h> 10/30/06
900 #include <stdlib.h> 10/30/06
1000 #include <string.h> 10/30/06
1100 10/30/06
1200 /* in qsysinc library */ 10/30/06
1300 #include <sys/time.h> 10/30/06
1400 #include <sys/types.h> 10/30/06
1500 #include <sys/socket.h> 10/30/06
1600 #include <netinet/in.h> 10/30/06
1700 #include <netinet/tcp.h> 10/30/06
1800 #include <arpa/inet.h> 10/30/06
1900 #include <netdb.h> 10/30/06
2000 #include <netns/ns.h> 10/30/06
2100 #include <unistd.h> 10/30/06
2200 #include <errno.h> 10/30/06
2300 #include <mih/waittime.h> 10/30/06
2400 #include <xxcvt.h> 10/30/06
2500 10/30/06
2600 /* BufferLength is 30000 bytes */ 01/20/08
2700 #define BufferLength 30000 01/20/08
2800 #define WIDTHDATAQ 30000 01/20/08
2900 #define INITWAITFORDTAQ 3600 10/30/06
3000 #define DTAQKEYLEN 16 10/30/06
3100 10/30/06
3200 /* Host name of server system */ 10/30/06
3300 #define DFTSERVER "192.168.1.123" 10/30/06
3400 10/30/06
3500 /* Host name of server system */ 10/30/06
3600 #define DFTPAGE "/Testform.asp" 10/30/06
3700 10/30/06
3800 /* Default Key */ 10/30/06
3900 #define DFTKEY "001" 10/30/06
4000 10/30/06
4100 /* Server's port number */ 10/30/06
4200 #define SERVPORT 80 10/30/06
4300 10/30/06
4400 /* Data Queue Name to receive the commands */ 10/30/06
4500 #define INDTAQNAME "SGSHPDTAQO" 10/30/06
4600 10/30/06
4700 /* Data Queue Name to receive the commands */ 10/30/06
4800 #define OUTDTAQNAME "SGSHPDTAQI" 10/30/06
4900 10/30/06
5000 /* Data Queue Name to receive the commands */ 10/30/06
5100 #define DTAQLIBRARY "SCANGATE" 10/30/06
5200 10/30/06
5300 /* 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 2
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
5400 /********************************************************************/ 10/30/06
5500 10/30/06
5600 #pragma linkage(QRCVDTAQ,OS) 10/30/06
5700 /*set up OS linkage*/ 10/30/06
5800 /**************** function prototype ********************************/ 10/30/06
5900 extern void QRCVDTAQ(char *qname, char *qlib, 10/30/06
6000 unsigned char *fldlen, char *transaction,unsigned char *wait, 10/30/06
6100 char *keyorder, unsigned char *keylen, char *keydata, 10/30/06
6200 unsigned char *sndlen, char *sndid); 10/30/06
6300 /********************************************************************/ 10/30/06
6400 10/30/06
6500 #pragma linkage(QSNDDTAQ,OS) 10/30/06
6600 /*set up OS linkage*/ 10/30/06
6700 /**************** function prototype ********************************/ 10/30/06
6800 10/30/06
6900 extern void QSNDDTAQ(char *qname, char *qlib, 10/30/06
7000 unsigned char *fldlen, char *transaction, 10/30/06
7100 unsigned char *keylen, char *keydata); 10/30/06
7200 /* unsigned char *fldlen, char *transaction); */ 10/30/06
7300 /********************************************************************/ 10/30/06
7400 10/30/06
7500 #pragma linkage(QCMDEXC,OS) 10/30/06
7600 /*set up OS linkage*/ 10/30/06
7700 /**************** function prototype ********************************/ 10/30/06
7800 10/30/06
7900 extern void QCMDEXC(char *cmd, unsigned char *cmdlen); 10/30/06
8000 /********************************************************************/ 10/30/06
8100 10/30/06
8200 /* 10/30/06
8300 /********************************************************************/ 10/30/06
8400 10/30/06
8500 10/30/06
8600 /* AS400port - added tables for 819 <-> 500 (1100 <-> 0120) */ 10/30/06
8700 static unsigned char from_ebcdic[] = { 10/30/06
8800 /* FROM cp 500 TO iso8859_1 */ 10/30/06
8900 0x00, 0x01, 0x02, 0x03, 0x9c, 0x09, 0x86, 0x7f, /* 00 - 07 */ 10/30/06
9000 0x97, 0x8d, 0x8e, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, /* 08 - 0f */ 10/30/06
9100 0x10, 0x11, 0x12, 0x13, 0x9d, 0x0a, 0x08, 0x87, /* 10 - 17 */ 10/30/06
9200 0x18, 0x19, 0x92, 0x8f, 0x1c, 0x1d, 0x1e, 0x1f, /* 18 - 1f */ 10/30/06
9300 0x80, 0x81, 0x82, 0x83, 0x84, 0x0a, 0x17, 0x1b, /* 20 - 27 */ 10/30/06
9400 0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x05, 0x06, 0x07, /* 28 - 2f */ 10/30/06
9500 0x90, 0x91, 0x16, 0x93, 0x94, 0x95, 0x96, 0x04, /* 30 - 37 */ 10/30/06
9600 0x98, 0x99, 0x9a, 0x9b, 0x14, 0x15, 0x9e, 0x1a, /* 38 - 3f */ 10/30/06
9700 0x20, 0xa0, 0xe2, 0xe4, 0xe0, 0xe1, 0xe3, 0xe5, /* 40 - 47 */ 10/30/06
9800 0xe7, 0xf1, 0xac, 0x2e, 0x3c, 0x28, 0x2b, 0x7c, /* 48 - 4f */ 10/30/06
9900 0x26, 0xe9, 0xea, 0xeb, 0xe8, 0xed, 0xee, 0xef, /* 50 - 57 */ 10/30/06
10000 0xec, 0xdf, 0x21, 0x24, 0x2a, 0x29, 0x3b, 0x5e, /* 58 - 5f */ 10/30/06
10100 0x2d, 0x2f, 0xc2, 0xc4, 0xc0, 0xc1, 0xc3, 0xc5, /* 60 - 67 */ 10/30/06
10200 0xc7, 0xd1, 0x21, 0x2c, 0x25, 0x5f, 0x3e, 0x3f, /* 68 - 6f */ 10/30/06
10300 0xf8, 0xc9, 0xca, 0xcb, 0xc8, 0xcd, 0xce, 0xcf, /* 70 - 77 */ 10/30/06
10400 0xcc, 0x60, 0x3a, 0x23, 0x40, 0x27, 0x3d, 0x22, /* 78 - 7f */ 10/30/06
10500 0xd8, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, /* 80 - 87 */ 10/30/06
10600 0x68, 0x69, 0xab, 0xbb, 0xf0, 0xfd, 0xfe, 0xb1, /* 88 - 8f */ 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 3
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
10700 0xb0, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f, 0x70, /* 90 - 97 */ 10/30/06
10800 0x71, 0x72, 0xaa, 0xba, 0xe6, 0xb8, 0xc6, 0xa4, /* 98 - 9f */ 10/30/06
10900 0xb5, 0x7e, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, /* a0 - a7 */ 10/30/06
11000 0x79, 0x7a, 0xa1, 0xbf, 0xd0, 0xdd, 0xde, 0xae, /* a8 - af */ 10/30/06
11100 0xa2, 0xa3, 0xa5, 0xb7, 0xa9, 0xa7, 0xb6, 0xbc, /* b0 - b7 */ 10/30/06
11200 0xbd, 0xbe, 0x5b, 0x5d, 0xaf, 0xa8, 0xb4, 0xd7, /* b8 - bf */ 10/30/06
11300 0x7b, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, /* c0 - c7 */ 10/30/06
11400 0x48, 0x49, 0xad, 0xf4, 0xf6, 0xf2, 0xf3, 0xf5, /* c8 - cf */ 10/30/06
11500 0x7d, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f, 0x50, /* d0 - d7 */ 10/30/06
11600 0x51, 0x52, 0xb9, 0xfb, 0xfc, 0xf9, 0xfa, 0xff, /* d8 - df */ 10/30/06
11700 0x5c, 0xf7, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, /* e0 - e7 */ 10/30/06
11800 0x59, 0x5a, 0xb2, 0xd4, 0xd6, 0xd2, 0xd3, 0xd5, /* e8 - ef */ 10/30/06
11900 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, /* f0 - f7 */ 10/30/06
12000 0x38, 0x39, 0xb3, 0xdb, 0xdc, 0xd9, 0xda, 0x9f 10/30/06
12100 }; 10/30/06
12200 10/30/06
12300 static unsigned char from_ascii[] = 10/30/06
12400 { 10/30/06
12500 /* FROM iso8859_1 TO cp 500 */ 10/30/06
12600 0x00, 0x01, 0x02, 0x03, 0x37, 0x2d, 0x2e, 0x2f, /* 00 - 07 */ 10/30/06
12700 0x16, 0x05, 0x25, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, /* 08 - 0f */ 10/30/06
12800 0x10, 0x11, 0x12, 0x13, 0x3c, 0x3d, 0x32, 0x26, /* 10 - 17 */ 10/30/06
12900 0x18, 0x19, 0x3f, 0x27, 0x1c, 0x1d, 0x1e, 0x1f, /* 18 - 1f */ 10/30/06
13000 0x40, 0x5a, 0x7f, 0x7b, 0x5b, 0x6c, 0x50, 0x7d, /* 20 - 27 */ 10/30/06
13100 0x4d, 0x5d, 0x5c, 0x4e, 0x6b, 0x60, 0x4b, 0x61, /* 28 - 2f */ 10/30/06
13200 0xf0, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, /* 30 - 37 */ 10/30/06
13300 0xf8, 0xf9, 0x7a, 0x5e, 0x4c, 0x7e, 0x6e, 0x6f, /* 38 - 3f */ 10/30/06
13400 0x7c, 0xc1, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, /* 40 - 47 */ 10/30/06
13500 0xc8, 0xc9, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, /* 48 - 4f */ 10/30/06
13600 0xd7, 0xd8, 0xd9, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, /* 50 - 57 */ 10/30/06
13700 0xe7, 0xe8, 0xe9, 0xba, 0xe0, 0xbb, 0x5f, 0x6d, /* 58 - 5f */ 10/30/06
13800 0x79, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, /* 60 - 67 */ 10/30/06
13900 0x88, 0x89, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, /* 68 - 6f */ 10/30/06
14000 0x97, 0x98, 0x99, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, /* 70 - 77 */ 10/30/06
14100 0xa7, 0xa8, 0xa9, 0xc0, 0x4f, 0xd0, 0xa1, 0x07, /* 78 - 7f */ 10/30/06
14200 0x20, 0x21, 0x22, 0x23, 0x24, 0x15, 0x06, 0x17, /* 80 - 87 */ 10/30/06
14300 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x09, 0x0a, 0x1b, /* 88 - 8f */ 10/30/06
14400 0x30, 0x31, 0x1a, 0x33, 0x34, 0x35, 0x36, 0x08, /* 90 - 97 */ 10/30/06
14500 0x38, 0x39, 0x3a, 0x3b, 0x04, 0x14, 0x3e, 0xff, /* 98 - 9f */ 10/30/06
14600 0x41, 0xaa, 0xb0, 0xb1, 0x9f, 0xb2, 0x5a, 0xb5, /* a0 - a7 */ 10/30/06
14700 0xbd, 0xb4, 0x9a, 0x8a, 0x4a, 0xca, 0xaf, 0xbc, /* a8 - af */ 10/30/06
14800 0x90, 0x8f, 0xea, 0xfa, 0xbe, 0xa0, 0xb6, 0xb3, /* b0 - b7 */ 10/30/06
14900 0x9d, 0xda, 0x9b, 0x8b, 0xb7, 0xb8, 0xb9, 0xab, /* b8 - bf */ 10/30/06
15000 0x64, 0x65, 0x62, 0x66, 0x63, 0x67, 0x9e, 0x68, /* c0 - c7 */ 10/30/06
15100 0x74, 0x71, 0x72, 0x73, 0x78, 0x75, 0x76, 0x77, /* c8 - cf */ 10/30/06
15200 0xac, 0x69, 0xed, 0xee, 0xeb, 0xef, 0xec, 0xbf, /* d0 - d7 */ 10/30/06
15300 0x80, 0xfd, 0xfe, 0xfb, 0xfc, 0xad, 0xae, 0x59, /* d8 - df */ 10/30/06
15400 0x44, 0x45, 0x42, 0x46, 0x43, 0x47, 0x9c, 0x48, /* e0 - e7 */ 10/30/06
15500 0x54, 0x51, 0x52, 0x53, 0x58, 0x55, 0x56, 0x57, /* e8 - ef */ 10/30/06
15600 0x8c, 0x49, 0xcd, 0xce, 0xcb, 0xcf, 0xcc, 0xe1, /* f0 - f7 */ 10/30/06
15700 0x70, 0xdd, 0xde, 0xdb, 0xdc, 0x8d, 0x8e, 0xdf 10/30/06
15800 }; 10/30/06
15900 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 4
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
16000 #define TO_EBCDIC(buffer,len) \ 10/30/06
16100 { \ 10/30/06
16200 unsigned i; \ 10/30/06
16300 for (i=0;i<(len);i++) \ 10/30/06
16400 (buffer)[i] = from_ascii[(buffer)[i]];\ 10/30/06
16500 } 10/30/06
16600 #define TO_ASCII(buffer,len) \ 10/30/06
16700 { \ 10/30/06
16800 unsigned i; \ 10/30/06
16900 for (i=0;i<(len);i++) \ 10/30/06
17000 (buffer)[i] = from_ebcdic[(buffer)[i]];\ 10/30/06
17100 } 10/30/06
17200 10/30/06
17300 int ClearDtaq( char *rqname, char *qlib, char *DtaqKey, 10/30/06
17400 char *RetMessage); 10/30/06
17500 void RemoveBlanks(char *, int); 10/30/06
17600 void RemoveHexCommands(char *, int); 10/30/06
17700 int SendPost( char *, int ); 10/30/06
17800 int Reconnect( int , struct sockaddr* ); 10/30/06
17900 void GetHeader(int ,char *); 10/30/06
18000 void GetMessage(int ,char *, char *, char *, char *); 10/30/06
18100 10/30/06
18200 /* -------------------------------------*/ 10/30/06
18300 /* routines to convert: */ 10/30/06
18400 /* - from integer to ascii */ 10/30/06
18500 /* - ascii to integer */ 10/30/06
18600 /* - character to hex */ 10/30/06
18700 /* - hex to character */ 10/30/06
18800 /* -------------------------------------*/ 10/30/06
18900 void xitoa(int, char s[], int); 10/30/06
19000 int xatoi(char *, int); 10/30/06
19100 void ctoh(char *, int, char *); 10/30/06
19200 void htoc(char *, int, char *); 10/30/06
19300 10/30/06
19400 10/30/06
19500 /* Pass in 1 parameter which is either the */ 10/30/06
19600 /* address or host name of the server, or */ 10/30/06
19700 /* set the server name in the #define */ 10/30/06
19800 /* SERVER. */ 10/30/06
19900 void main(int argc, char *argv[]) 10/30/06
20000 { 10/30/06
20100 /****************************************/ 10/30/06
20200 /* Variable and structure definitions. */ 10/30/06
20300 /****************************************/ 10/30/06
20400 int sd, rc, length = sizeof(int); 10/30/06
20500 struct sockaddr_in serveraddr; 10/30/06
20600 char bufferOut[BufferLength]; 10/30/06
20700 char sPostPage[BufferLength]; 10/30/06
20800 char BufferIn[ BufferLength]; 11/01/06
20900 char BufferRet[ BufferLength]; 11/01/06
21000 char server[255]; 10/30/06
21100 char sRequestPage[512]; 10/30/06
21200 char sHostName[255]; 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 5
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
21300 char buffertst[BufferLength]; 10/30/06
21400 char transaction[WIDTHDATAQ]; 10/30/06
21500 char temp; 10/30/06
21600 char keyorder[2],keydata[DTAQKEYLEN]; 10/30/06
21700 char sndid[44]; 10/30/06
21800 unsigned char fldlen[5]; 10/30/06
21900 unsigned char keylen[3]; 10/30/06
22000 unsigned char wait[5]; 10/30/06
22100 unsigned char sndlen[3]; 10/30/06
22200 int Sckport; 10/30/06
22300 char DtaqKey[17]; 10/30/06
22400 char recvqlib[11]; 10/30/06
22500 char recvqname[11]; 10/30/06
22600 char sendqlib[11]; 10/30/06
22700 char sendqname[11]; 10/30/06
22800 char rqlib[11]; 10/30/06
22900 char rqname[11]; 10/30/06
23000 char sqlib[11]; 10/30/06
23100 char sqname[11]; 10/30/06
23200 char SocketPort[8]; 10/30/06
23300 struct timeval timeout; 10/30/06
23400 struct linger DiscLinger; 10/30/06
23500 int ret; 10/30/06
23600 int recvlen,len; 10/30/06
23700 int reccnt; 10/30/06
23800 int argumentLength; 10/30/06
23900 int connected; 10/30/06
24000 int attempts; 10/30/06
24100 int recordNbr; 10/30/06
24200 10/30/06
24300 int totalcnt = 0; 10/30/06
24400 int printcnt = 0; 10/30/06
24500 struct hostent *hostp; 10/30/06
24600 /* will send sample print command */ 10/30/06
24700 /******************************************/ 10/30/06
24800 /* The socket() function returns a socket */ 10/30/06
24900 /* descriptor representing an endpoint. */ 10/30/06
25000 /* The statement also identifies that the */ 10/30/06
25100 /* INET (Internet Protocol) address family */ 10/30/06
25200 /* with the TCP transport (SOCK_STREAM) */ 10/30/06
25300 /* will be used for this socket. */ 10/30/06
25400 /******************************************/ 10/30/06
25500 10/30/06
25600 10/30/06
25700 /* IP Address */ 10/30/06
25800 if (argc > 1) 10/30/06
25900 strcpy(server, argv[1]+1); 10/30/06
26000 else 10/30/06
26100 strcpy(server, DFTSERVER); 10/30/06
26200 10/30/06
26300 /* Key to Receive and Send DtaQ */ 10/30/06
26400 memset(DtaqKey,' ',16); 10/30/06
26500 if (argc > 2) 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 6
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
26600 { 10/30/06
26700 if (strlen(argv[2]) > 0) 10/30/06
26800 { 10/30/06
26900 argumentLength=16; 10/30/06
27000 if (strlen(argv[2]) < argumentLength) 10/30/06
27100 { 10/30/06
27200 argumentLength = strlen(argv[2]); 10/30/06
27300 } 10/30/06
27400 memmove(DtaqKey,argv[2],argumentLength); 10/30/06
27500 } 10/30/06
27600 } 10/30/06
27700 else 10/30/06
27800 { 10/30/06
27900 memmove(DtaqKey, DFTKEY,3); 10/30/06
28000 } 10/30/06
28100 10/30/06
28200 10/30/06
28300 /* Post Page */ 10/30/06
28400 memset(sRequestPage,0,512); 10/30/06
28500 if (argc > 3) 10/30/06
28600 { 10/30/06
28700 if (strlen(argv[3]) > 0) 10/30/06
28800 { 10/30/06
28900 argumentLength=512; 10/30/06
29000 if (strlen(argv[3]) < argumentLength) 10/30/06
29100 { 10/30/06
29200 argumentLength = strlen(argv[3]); 10/30/06
29300 } 10/30/06
29400 memmove(sRequestPage,argv[3],argumentLength); 10/30/06
29500 } 10/30/06
29600 } 10/30/06
29700 else 10/30/06
29800 { 10/30/06
29900 strcpy(sRequestPage,DFTPAGE); 10/30/06
30000 } 10/30/06
30100 10/30/06
30200 10/30/06
30300 /* Socket Port */ 10/30/06
30400 memset(SocketPort,0,8); 10/30/06
30500 if (argc > 4) 10/30/06
30600 { 10/30/06
30700 if (strlen(argv[4]) > 0) 10/30/06
30800 { 10/30/06
30900 argumentLength=8; 10/30/06
31000 if (strlen(argv[4]) < argumentLength) 10/30/06
31100 { 10/30/06
31200 argumentLength = strlen(argv[4]); 10/30/06
31300 } 10/30/06
31400 memmove(SocketPort,argv[4],argumentLength); 10/30/06
31500 } 10/30/06
31600 SocketPort[0] = '0'; 10/30/06
31700 } 10/30/06
31800 if (strlen(SocketPort) > 0 ) 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 7
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
31900 Sckport = xatoi(SocketPort,8); 10/30/06
32000 else 10/30/06
32100 Sckport = SERVPORT; 10/30/06
32200 10/30/06
32300 10/30/06
32400 /* Library */ 10/30/06
32500 memset(recvqlib,' ',10); 10/30/06
32600 memset(rqlib,0,11); 10/30/06
32700 if (argc > 5) 10/30/06
32800 { 10/30/06
32900 if (strlen(argv[5]) > 0) 10/30/06
33000 { 10/30/06
33100 argumentLength=10; 10/30/06
33200 if (strlen(argv[5]) < argumentLength) 10/30/06
33300 { 10/30/06
33400 argumentLength = strlen(argv[5]); 10/30/06
33500 } 10/30/06
33600 memmove(recvqlib,argv[5],argumentLength); 10/30/06
33700 memmove(rqlib,argv[5],argumentLength); 10/30/06
33800 } 10/30/06
33900 } 10/30/06
34000 else 10/30/06
34100 { 10/30/06
34200 strcpy(rqlib,DTAQLIBRARY); 10/30/06
34300 memmove(recvqlib,rqlib,strlen(rqlib)); 10/30/06
34400 } 10/30/06
34500 /* Receive from Dtaq Name */ 10/30/06
34600 memset(recvqname,' ',10); 10/30/06
34700 memset(rqname,0,11); 10/30/06
34800 if (argc > 6) 10/30/06
34900 { 10/30/06
35000 if (strlen(argv[6]) > 0) 10/30/06
35100 { 10/30/06
35200 argumentLength=10; 10/30/06
35300 if (strlen(argv[6]) < argumentLength) 10/30/06
35400 { 10/30/06
35500 argumentLength = strlen(argv[6]); 10/30/06
35600 } 10/30/06
35700 memmove(recvqname,argv[6],argumentLength); 10/30/06
35800 memmove(rqname,argv[6],argumentLength); 10/30/06
35900 } 10/30/06
36000 } 10/30/06
36100 else 10/30/06
36200 { 10/30/06
36300 strcpy(rqname,INDTAQNAME); 10/30/06
36400 memmove(recvqname,rqname,strlen(rqname)); 10/30/06
36500 } 10/30/06
36600 10/30/06
36700 /* Send To Dtaq Name */ 10/30/06
36800 memset(sendqname,' ',10); 10/30/06
36900 memset(sqname,0,11); 10/30/06
37000 if (argc > 7) 10/30/06
37100 { 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 8
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
37200 if (strlen(argv[7]) > 0) 10/30/06
37300 { 10/30/06
37400 argumentLength=10; 10/30/06
37500 if (strlen(argv[7]) < argumentLength) 10/30/06
37600 { 10/30/06
37700 argumentLength = strlen(argv[7]); 10/30/06
37800 } 10/30/06
37900 memmove(sendqname,argv[7],argumentLength); 10/30/06
38000 memmove(sqname,argv[7],argumentLength); 10/30/06
38100 } 10/30/06
38200 } 10/30/06
38300 else 10/30/06
38400 { 10/30/06
38500 strcpy(sqname,OUTDTAQNAME); 10/30/06
38600 memmove(sendqname,sqname,strlen(sqname)); 10/30/06
38700 } 10/30/06
38800 10/30/06
38900 10/30/06
39000 10/30/06
39100 strcpy(sHostName,server); 10/30/06
39200 memset(&serveraddr, 0x00, sizeof(struct sockaddr_in)); 10/30/06
39300 serveraddr.sin_family = AF_INET; 10/30/06
39400 serveraddr.sin_port = htons(Sckport); 10/30/06
39500 if ((serveraddr.sin_addr.s_addr = inet_addr(server)) 10/30/06
39600 == (unsigned long)INADDR_NONE) 10/30/06
39700 { 10/30/06
39800 /*************************************************/ 10/30/06
39900 /* When passing the host name of the server as a */ 10/30/06
40000 /* parameter to this program, use the gethostbyname() */ 10/30/06
40100 /* function to retrieve the address of the host server. */ 10/30/06
40200 /***************************************************/ 10/30/06
40300 /* get host address */ 10/30/06
40400 hostp = gethostbyname(server); 10/30/06
40500 if (hostp == (struct hostent *)NULL) 10/30/06
40600 { 10/30/06
40700 printf("server = %s\n",server); 10/30/06
40800 printf("HOST NOT FOUND --> "); 10/30/06
40900 /* h_errno is usually defined */ 10/30/06
41000 /* in netdb.h */ 10/30/06
41100 printf("h_errno = %d\n",h_errno); 10/30/06
41200 exit(-1); 10/30/06
41300 } 10/30/06
41400 memcpy(&serveraddr.sin_addr, 10/30/06
41500 hostp->h_addr, 10/30/06
41600 sizeof(serveraddr.sin_addr)); 10/30/06
41700 } 10/30/06
41800 10/30/06
41900 /***********************************************/ 10/30/06
42000 /* After the socket descriptor is received, the */ 10/30/06
42100 /* connect() function is used to establish a */ 10/30/06
42200 /* connection to the server. */ 10/30/06
42300 /***********************************************/ 10/30/06
42400 memmove(keyorder,"EQ",2); 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 9
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
42500 QXXITOP(sndlen,3,0,0); 10/30/06
42600 memset(sndid,' ',44); 10/30/06
42700 QXXITOP(fldlen,5,0,WIDTHDATAQ); 10/30/06
42800 QXXITOP(wait,5,0,INITWAITFORDTAQ); 10/30/06
42900 QXXITOP(keylen,3,0,DTAQKEYLEN); 10/30/06
43000 memcpy(keydata,DtaqKey,DTAQKEYLEN); 10/30/06
43100 reccnt = 0; 10/30/06
43200 10/30/06
43300 memset(BufferRet,0x00,BufferLength); 10/30/06
43400 rc = ClearDtaq( recvqname, recvqlib, DtaqKey, 10/30/06
43500 BufferRet ); 10/30/06
43600 ret = 0; 10/30/06
43700 connected = 0; 10/30/06
43800 for ( ; ; ) 10/30/06
43900 { 10/30/06
44000 memset(bufferOut,0x00,BufferLength); 10/30/06
44100 10/30/06
44200 strcpy(bufferOut,"HighwayMessageId=SPSBB&Synchronous=Yes"); 11/01/06
44300 strcat(bufferOut,"&HighwayMessage=Test Send Highway"); 10/30/06
44400 strcat(bufferOut," XML Message"); 10/30/06
44500 recvlen = strlen(bufferOut); 10/30/06
44600 10/30/06
44700 /* Temporarily send test 10/30/06
44800 */ 10/30/06
44900 10/30/06
45000 10/30/06
45100 QRCVDTAQ(recvqname, recvqlib, fldlen, bufferOut,wait, 10/30/06
45200 keyorder,keylen,keydata,sndlen,sndid); 10/30/06
45300 recvlen = QXXPTOI(fldlen,5,0); 10/30/06
45400 /* Temporarily send test 10/30/06
45500 */ 10/30/06
45600 10/30/06
45700 10/30/06
45800 10/30/06
45900 if (recvlen <= 0 ) 10/30/06
46000 { 10/30/06
46100 QXXITOP(wait,5,0,INITWAITFORDTAQ); 10/30/06
46200 } 10/30/06
46300 else 10/30/06
46400 { 10/30/06
46500 /* Check for BYE */ 10/30/06
46600 if (memcmp(bufferOut,"BYE",3) == 0 ) 10/30/06
46700 { 10/30/06
46800 ret = 1; 10/30/06
46900 break; 10/30/06
47000 } 10/30/06
47100 RemoveBlanks( bufferOut,sizeof(bufferOut)); 10/30/06
47200 /* RemoveHexCommands( bufferOut,sizeof(bufferOut)); */ 10/30/06
47300 reccnt++; 10/30/06
47400 /* Connect() to server. */ 10/30/06
47500 ret = 0; 10/30/06
47600 attempts= 0; 10/30/06
47700 if (connected == 0 ) 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 10
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
47800 { 10/30/06
47900 while ( connected == 0 ) 10/30/06
48000 { 10/30/06
48100 /* get a socket descriptor */ 10/30/06
48200 if ((sd = socket(AF_INET, SOCK_STREAM, 0)) < 0) 10/30/06
48300 { 10/30/06
48400 perror("socket() failed"); 10/30/06
48500 attempts++; 10/30/06
48600 if (attempts > 5 ) break; 10/30/06
48700 } 10/30/06
48800 else 10/30/06
48900 { 10/30/06
49000 if ((rc = connect(sd, 10/30/06
49100 (struct sockaddr *)&serveraddr, 10/30/06
49200 sizeof(serveraddr))) < 0) 10/30/06
49300 { 10/30/06
49400 perror("connect() failed"); 10/30/06
49500 ret = 1; 10/30/06
49600 close(sd); 10/30/06
49700 connected = 0; 10/30/06
49800 attempts++; 10/30/06
49900 if (attempts > 5 ) break; 10/30/06
50000 } 10/30/06
50100 else /* Connected to the Printer */ 10/30/06
50200 { 10/30/06
50300 connected = 1; 10/30/06
50400 } 10/30/06
50500 } /* end else on socket descriptor */ 10/30/06
50600 } /* end while( connected == 0) */ 10/30/06
50700 } 10/30/06
50800 /* Connected to the Shipping Server */ 10/30/06
50900 recordNbr = 0; 10/30/06
51000 attempts = 0; 10/30/06
51100 while (connected != 0 ) 10/30/06
51200 { 10/30/06
51300 10/30/06
51400 memset(sPostPage,0x00,BufferLength); 10/30/06
51500 switch(recordNbr) 10/30/06
51600 { 10/30/06
51700 case 0: 10/30/06
51800 strcpy(sPostPage,"POST "); 10/30/06
51900 strcat(sPostPage,sRequestPage); 10/30/06
52000 strcat(sPostPage," HTTP/1.0"); 10/30/06
52100 break; 10/30/06
52200 case 1: 10/30/06
52300 strcpy(sPostPage,"Accept: */*"); 10/30/06
52400 break; 10/30/06
52500 case 2: 10/30/06
52600 strcpy(sPostPage,"Accept-Language: en-us"); 10/30/06
52700 break; 10/30/06
52800 case 3: 10/30/06
52900 strcpy(sPostPage,"Accept-Encoding: gzip, deflate"); 10/30/06
53000 break; 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 11
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
53100 case 4: 10/30/06
53200 strcpy(sPostPage,"User-Agent: Mozilla/4.0"); 10/30/06
53300 break; 10/30/06
53400 case 5: 10/30/06
53500 sprintf(sPostPage,"Content-Length: %ld", 10/30/06
53600 strlen(bufferOut)); 10/30/06
53700 break; 10/30/06
53800 case 6: 10/30/06
53900 strcpy(sPostPage,"HOST: "); 10/30/06
54000 strcat(sPostPage,sHostName); 10/30/06
54100 break; 10/30/06
54200 case 7: 10/30/06
54300 strcpy(sPostPage,"Content-Type: application"); 10/30/06
54400 strcat(sPostPage,"/x-www-form-urlencoded"); 10/30/06
54500 break; 10/30/06
54600 case 8: 10/30/06
54700 /* Send only CR and LF */ 10/30/06
54800 break; 10/30/06
54900 case 9: 10/30/06
55000 /* Send HighwayMessageId= */ 10/30/06
55100 /* &Synchronous=YES */ 10/30/06
55200 /* &HighwayMessage= */ 10/30/06
55300 strcpy(sPostPage,bufferOut); 10/30/06
55400 10/30/06
55500 break; 10/30/06
55600 case 10: 10/30/06
55700 break; 10/30/06
55800 default: 10/30/06
55900 break; 10/30/06
56000 } 10/30/06
56100 10/30/06
56200 10/30/06
56300 printf("Send: %80.80s\n",sPostPage); 11/01/06
56400 10/30/06
56500 connected = SendPost(sPostPage,sd); 10/30/06
56600 if (connected == 0 ) 10/30/06
56700 { 10/30/06
56800 while (connected == 0 ) 10/30/06
56900 { 10/30/06
57000 connected = Reconnect(sd, 10/30/06
57100 (struct sockaddr *)&serveraddr); 10/30/06
57200 if (connected == 0 ) 10/30/06
57300 { 10/30/06
57400 attempts++; 10/30/06
57500 if (attempts > 5 ) break; 10/30/06
57600 } 10/30/06
57700 else 10/30/06
57800 { 10/30/06
57900 recordNbr = 0; 10/30/06
58000 attempts = 0; 10/30/06
58100 } 10/30/06
58200 } 10/30/06
58300 } 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 12
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
58400 else 10/30/06
58500 { 10/30/06
58600 recordNbr++; 10/30/06
58700 attempts = 0; 10/30/06
58800 if (recordNbr >= 10 ) 10/30/06
58900 { 10/30/06
59000 memset(BufferIn,0x00, BufferLength); 11/01/06
59100 memset(BufferRet,0x00, BufferLength); 11/01/06
59200 GetHeader(sd, BufferIn); 10/30/06
59300 /* */ 10/23/13
59400 printf("Header: len= %ld %80.80s \n",strlen(BufferIn),BufferIn); 10/30/06
59500 /* */ 10/23/13
59600 GetMessage(sd, BufferRet,sendqname,recvqlib, 10/30/06
59700 DtaqKey); 10/30/06
59800 /* 10/30/06
59900 printf("Reply: len= %ld %80.80s \n",strlen(BufferRet),BufferRet); 10/30/06
60000 len=strlen(BufferRet); 10/30/06
60100 memset(transaction,0x00,BufferLength); 10/30/06
60200 memcpy(transaction,BufferRet,len); 10/30/06
60300 QXXITOP(keylen,3,0,DTAQKEYLEN); 10/30/06
60400 QXXITOP(fldlen,5,0,WIDTHDATAQ); 10/30/06
60500 QSNDDTAQ(sendqname, recvqlib, fldlen, 10/30/06
60600 transaction,keylen,DtaqKey); 10/30/06
60700 printf("len: %ld %80.80s \n",len,transaction); 10/30/06
60800 printf("Key: %s %s %s %d \n",sendqname,recvqlib,DtaqKey, 10/30/06
60900 strlen(DtaqKey)); 10/30/06
61000 */ 10/30/06
61100 10/30/06
61200 break; 10/30/06
61300 } 10/30/06
61400 } 10/30/06
61500 } /* end while connected to the shipping server */ 10/30/06
61600 /****************************************/ 10/30/06
61700 /* When the data has been read, close() */ 10/30/06
61800 /* the socket descriptor. */ 10/30/06
61900 /****************************************/ 10/30/06
62000 /* Close socket descriptor from client side. */ 10/30/06
62100 if (connected != 0 ) 10/30/06
62200 { 10/30/06
62300 close(sd); 10/30/06
62400 connected = 0; 10/30/06
62500 } /* end if connected to the shipping server */ 10/30/06
62600 } /* end else recvlen > 0 */ 10/30/06
62700 10/30/06
62800 /* Temporarily end immediately */ 10/30/06
62900 /* break; */ 11/01/06
63000 10/30/06
63100 } /* End For loop */ 10/30/06
63200 /* Close socket descriptor from client side. */ 10/30/06
63300 if (connected != 0 ) 10/30/06
63400 { 10/30/06
63500 DiscLinger.l_onoff = 1; 10/30/06
63600 DiscLinger.l_linger = 0; 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 13
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
63700 if ((rc = setsockopt(sd, SOL_SOCKET, 10/30/06
63800 SO_LINGER, 10/30/06
63900 (char *)&DiscLinger, 10/30/06
64000 sizeof(DiscLinger))) < 0) 10/30/06
64100 { 10/30/06
64200 perror("setsockopt() failed"); 10/30/06
64300 } 10/30/06
64400 close(sd); 10/30/06
64500 } 10/30/06
64600 exit(0); 10/30/06
64700 } 10/30/06
64800 10/30/06
64900 10/30/06
65000 /* ------------------------------------------------------------------*/ 10/30/06
65100 /* Routine to Remove Blanks and make Message a C string */ 10/30/06
65200 /* ------------------------------------------------------------------*/ 10/30/06
65300 void RemoveBlanks(char *buff,int buffLen) 10/30/06
65400 { 10/30/06
65500 /* remove extra blanks at end */ 10/30/06
65600 int i; 10/30/06
65700 for (i=0;i<buffLen-2;i++) 10/30/06
65800 { 10/30/06
65900 if (buff[buffLen-i-1] <= ' ') 10/30/06
66000 { 10/30/06
66100 /* buff[buffLen-i-1] <= 0x00) { */ 10/30/06
66200 buff[buffLen-i-1] = 0x00; 10/30/06
66300 } 10/30/06
66400 else 10/30/06
66500 break; 10/30/06
66600 } 10/30/06
66700 } 10/30/06
66800 10/30/06
66900 /* ------------------------------------------------------------------*/ 10/30/06
67000 /* Routine to Remove Hex Commands and make Message a C string */ 10/30/06
67100 /* ------------------------------------------------------------------*/ 10/30/06
67200 void RemoveHexCommands(char *buff,int buffLen) 10/30/06
67300 { 10/30/06
67400 /* assume that buff is a null terminated string */ 10/30/06
67500 char *token; 10/30/06
67600 char *cbuff1; 10/30/06
67700 char *cbuff2; 10/30/06
67800 char buffcvt[3]; 10/30/06
67900 char buffval[3]; 10/30/06
68000 int istr; 10/30/06
68100 int len1, len2; 10/30/06
68200 cbuff1 = buff; 10/30/06
68300 do 10/30/06
68400 { 10/30/06
68500 token = strstr(buff,"="); 10/30/06
68600 if (token != NULL) 10/30/06
68700 { 10/30/06
68800 istr = strlen(buff) - strlen(token); 10/30/06
68900 if ( istr + 3 > strlen(buff) ) break; 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 14
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
69000 if (buffLen > istr + 3 ) 10/30/06
69100 { 10/30/06
69200 memset(buffcvt,0x00,3); 10/30/06
69300 memset(buffval,0x00,3); 10/30/06
69400 strncpy(buffcvt,buff + istr + 1,2); 10/30/06
69500 if (strncmp(buffcvt,"0D",2) == 0 ) 10/30/06
69600 { 10/30/06
69700 strcpy(buffval,"\r"); 10/30/06
69800 } 10/30/06
69900 else if (strncmp(buffcvt,"0A",2) == 0 ) 10/30/06
70000 { 10/30/06
70100 strcpy(buffval,"\n"); 10/30/06
70200 } 10/30/06
70300 else 10/30/06
70400 { 10/30/06
70500 ctoh(buffcvt, strlen(buffcvt), buffval); 10/30/06
70600 } 10/30/06
70700 cbuff2 = token + 3; 10/30/06
70800 buff[istr] = 0x00; 10/30/06
70900 buff[istr + 1] = 0x00; 10/30/06
71000 buff[istr + 2] = 0x00; 10/30/06
71100 10/30/06
71200 strcat(buff,buffval); 10/30/06
71300 strcat(buff,cbuff2); 10/30/06
71400 } 10/30/06
71500 } 10/30/06
71600 } while (token != NULL); 10/30/06
71700 } 10/30/06
71800 10/30/06
71900 /* ------------------------------------------------------------------*/ 10/30/06
72000 /* Routine to Clear all messages from the Data Queue */ 10/30/06
72100 /* ------------------------------------------------------------------*/ 10/30/06
72200 int ClearDtaq( char *rqname, char *qlib, char *DtaqKey, 10/30/06
72300 char *RetMessage) 10/30/06
72400 { 10/30/06
72500 10/30/06
72600 10/30/06
72700 char keyorder[2],keydata[DTAQKEYLEN]; 10/30/06
72800 char sndid[44]; 10/30/06
72900 unsigned char fldlen[5]; 10/30/06
73000 unsigned char wait[5]; 10/30/06
73100 unsigned char keylen[3]; 10/30/06
73200 unsigned char sndlen[3]; 10/30/06
73300 unsigned char CmdLen[15]; 10/30/06
73400 char BufferRet[BufferLength]; 10/30/06
73500 int length = sizeof(int); 10/30/06
73600 char temp; 10/30/06
73700 int recvlen; 10/30/06
73800 int totalcnt; 10/30/06
73900 int ret,rc; 10/30/06
74000 ret = 0; 10/30/06
74100 memmove(keyorder,"EQ",2); 10/30/06
74200 QXXITOP(sndlen,3,0,0); 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 15
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
74300 memset(sndid,' ',44); 10/30/06
74400 QXXITOP(fldlen,5,0,WIDTHDATAQ); 10/30/06
74500 QXXITOP(wait,5,0,0); 10/30/06
74600 QXXITOP(keylen,3,0,DTAQKEYLEN); 10/30/06
74700 memcpy(keydata,DtaqKey,DTAQKEYLEN); 10/30/06
74800 10/30/06
74900 for ( ; ; ) 10/30/06
75000 { 10/30/06
75100 memset(BufferRet,0x00,BufferLength); 10/30/06
75200 QRCVDTAQ(rqname, qlib, fldlen, BufferRet,wait, 10/30/06
75300 keyorder,keylen,keydata,sndlen,sndid); 10/30/06
75400 10/30/06
75500 recvlen = QXXPTOI(fldlen,5,0); 10/30/06
75600 10/30/06
75700 /* Clear all records in the data Queue */ 10/30/06
75800 if (recvlen > 0 ) { 10/30/06
75900 if (memcmp(BufferRet,"BYE",3) != 0 ) { 10/30/06
76000 RemoveBlanks( BufferRet,sizeof(BufferRet)); 10/30/06
76100 memset(RetMessage,0,BufferLength); 10/30/06
76200 memcpy(RetMessage,BufferRet,strlen(BufferRet)); 10/30/06
76300 } /* Check for BYE */ 10/30/06
76400 } /* recvlen > 0 */ 10/30/06
76500 else { 10/30/06
76600 break; 10/30/06
76700 } 10/30/06
76800 } 10/30/06
76900 return(ret); 10/30/06
77000 } 10/30/06
77100 10/30/06
77200 /* ------------------------------------------------------------------*/ 10/30/06
77300 /* Routine to Clear all messages from the Data Queue */ 10/30/06
77400 /* ------------------------------------------------------------------*/ 10/30/06
77500 int SendPost( char *bufferOut, int sd) 10/30/06
77600 { 10/30/06
77700 int length = sizeof(int); 10/30/06
77800 int rc,ret; 10/30/06
77900 int printcnt; 10/30/06
78000 char temp; 10/30/06
78100 ret = 1; 10/30/06
78200 /*********************************************/ 10/30/06
78300 /* Send bytes to the server using */ 10/30/06
78400 /* the write() function. */ 10/30/06
78500 /*********************************************/ 10/30/06
78600 /* Write() buffer to the server. */ 10/30/06
78700 strcat(bufferOut,"\r\n"); 10/30/06
78800 TO_ASCII((unsigned char *) bufferOut,strlen(bufferOut)); 10/30/06
78900 printcnt = 0; 10/30/06
79000 while(printcnt < 1) 10/30/06
79100 { 10/30/06
79200 /* rc = write(sd, bufferOut, strlen(bufferOut)); */ 10/30/06
79300 rc = send(sd, bufferOut, strlen(bufferOut),0); 10/30/06
79400 printcnt++; 10/30/06
79500 if (rc < 0) 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 16
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
79600 { 10/30/06
79700 ret = 0; 10/30/06
79800 perror("write() failed"); 10/30/06
79900 rc = getsockopt(sd, SOL_SOCKET, SO_ERROR, 10/30/06
80000 &temp, &length); 10/30/06
80100 if (rc == 0) 10/30/06
80200 { 10/30/06
80300 /* Print out the asynchronously */ 10/30/06
80400 /* received error. */ 10/30/06
80500 errno = temp; 10/30/06
80600 perror("SO_ERROR was"); 10/30/06
80700 } 10/30/06
80800 } 10/30/06
80900 } 10/30/06
81000 return(ret); 10/30/06
81100 } 10/30/06
81200 10/30/06
81300 /* ------------------------------------------------------------------*/ 10/30/06
81400 /* Routine to Clear all messages from the Data Queue */ 10/30/06
81500 /* ------------------------------------------------------------------*/ 10/30/06
81600 int Reconnect( int sd, struct sockaddr* serveraddr) 10/30/06
81700 { 10/30/06
81800 int connected; 10/30/06
81900 int attempts; 10/30/06
82000 int rc, ret; 10/30/06
82100 connected = 0; 10/30/06
82200 attempts = 0; 10/30/06
82300 close(sd); 10/30/06
82400 while ( connected == 0 ) 10/30/06
82500 { 10/30/06
82600 /* get a socket descriptor */ 10/30/06
82700 if ((sd = socket(AF_INET, SOCK_STREAM, 0)) < 0) 10/30/06
82800 { 10/30/06
82900 perror("socket() failed"); 10/30/06
83000 attempts++; 10/30/06
83100 if (attempts > 5 ) break; 10/30/06
83200 } 10/30/06
83300 else 10/30/06
83400 { 10/30/06
83500 if ((rc = connect(sd, 10/30/06
83600 (struct sockaddr *)&serveraddr, 10/30/06
83700 sizeof(serveraddr))) < 0) 10/30/06
83800 { 10/30/06
83900 perror("connect() failed"); 10/30/06
84000 ret = 1; 10/30/06
84100 close(sd); 10/30/06
84200 connected = 0; 10/30/06
84300 attempts++; 10/30/06
84400 if (attempts > 5 ) break; 10/30/06
84500 } 10/30/06
84600 else /* Connected to the Printer */ 10/30/06
84700 { 10/30/06
84800 connected = 1; 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 17
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
84900 break; 10/30/06
85000 } 10/30/06
85100 } 10/30/06
85200 } /* end while( connected == 0) */ 10/30/06
85300 ret = connected; 10/30/06
85400 return(ret); 10/30/06
85500 } 10/30/06
85600 10/30/06
85700 /* ------------------------------------------------------------------*/ 10/30/06
85800 /* Routine to Get Header message */ 10/30/06
85900 /* ------------------------------------------------------------------*/ 10/30/06
86000 void GetHeader(int sd ,char *buff) 10/30/06
86100 { 10/30/06
86200 int chars,done,l; 10/30/06
86300 char buffer[512]; 10/30/06
86400 char hexbuffer[512]; 10/30/06
86500 chars = 0; 10/30/06
86600 done = 0; 10/30/06
86700 10/30/06
86800 while(!done) 10/30/06
86900 { 10/30/06
87000 l = recv(sd,buffer,1,0); 10/30/06
87100 if(l<0) 10/30/06
87200 done=1; 10/30/06
87300 10/30/06
87400 switch(*buffer) 10/30/06
87500 { 10/30/06
87600 case 13: 10/30/06
87700 break; 10/30/06
87800 case 10: 10/30/06
87900 if(chars==0) 10/30/06
88000 done = 1; 10/30/06
88100 chars=0; 10/30/06
88200 break; 10/30/06
88300 default: 10/30/06
88400 chars++; 10/30/06
88500 if(chars >= ( BufferLength)-2) 11/01/06
88600 done = 1; 10/30/06
88700 break; 10/30/06
88800 } 10/30/06
88900 memcpy(buff+strlen(buff),buffer,l); 10/30/06
89000 } 10/30/06
89100 TO_EBCDIC(buff,strlen(buff)); 10/30/06
89200 10/30/06
89300 } 10/30/06
89400 /* ------------------------------------------------------------------*/ 10/30/06
89500 /* Routine to Get Header message */ 10/30/06
89600 /* ------------------------------------------------------------------*/ 10/30/06
89700 void GetMessage(int sd ,char *buff, char *sendqname, char *recvqlib, 10/30/06
89800 char *DtaqKey) 10/30/06
89900 { 10/30/06
90000 int l; 10/30/06
90100 int len; 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 18
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
90200 char buffer[ BufferLength]; 11/01/06
90300 char transaction[WIDTHDATAQ]; 10/30/06
90400 unsigned char fldlen[5]; 10/30/06
90500 unsigned char keylen[3]; 10/30/06
90600 10/30/06
90700 do 10/30/06
90800 { 10/30/06
90900 l = recv(sd,buffer,WIDTHDATAQ,0); 10/30/06
91000 if(l<0) 10/30/06
91100 break; 10/30/06
91200 if((strlen(buff) + l) > WIDTHDATAQ) 10/30/06
91300 { 10/30/06
91400 TO_EBCDIC(buff,strlen(buff)); 10/30/06
91500 printf("Reply: len= %ld %80.80s \n",strlen(buff),buff); 10/30/06
91600 len=strlen(buff); 10/30/06
91700 memset(transaction,0x00,BufferLength); 10/30/06
91800 memcpy(transaction,buff,len); 10/30/06
91900 QXXITOP(keylen,3,0,DTAQKEYLEN); 10/30/06
92000 QXXITOP(fldlen,5,0,WIDTHDATAQ); 10/30/06
92100 QSNDDTAQ(sendqname, recvqlib, fldlen, 10/30/06
92200 transaction,keylen,DtaqKey); 10/30/06
92300 memset(buff,0x00,BufferLength); 10/30/06
92400 } 10/30/06
92500 *(buffer+l)=0; 10/30/06
92600 memcpy(buff+strlen(buff),buffer,l); 10/30/06
92700 } while(l>0); 10/30/06
92800 10/30/06
92900 10/30/06
93000 if(strlen(buff) > 0) 10/30/06
93100 { 10/30/06
93200 TO_EBCDIC(buff,strlen(buff)); 10/30/06
93300 printf("Reply: len= %ld %80.80s \n",strlen(buff),buff); 10/30/06
93400 len=strlen(buff); 10/30/06
93500 memset(transaction,0x00,BufferLength); 10/30/06
93600 memcpy(transaction,buff,len); 10/30/06
93700 QXXITOP(keylen,3,0,DTAQKEYLEN); 10/30/06
93800 QXXITOP(fldlen,5,0,WIDTHDATAQ); 10/30/06
93900 QSNDDTAQ(sendqname, recvqlib, fldlen, 10/30/06
94000 transaction,keylen,DtaqKey); 10/30/06
94100 } 10/30/06
94200 10/30/06
94300 } 10/30/06
94400 10/30/06
94500 /* ------------------------------------------------------------------*/ 10/30/06
94600 /* xitoa - converts an integer to a string, padded w/blanks */ 10/30/06
94700 /* ------------------------------------------------------------------*/ 10/30/06
94800 void xitoa(int number, char s[], int slen) 10/30/06
94900 { 10/30/06
95000 10/30/06
95100 memset((void *)&s[0], 0x40, slen); 10/30/06
95200 10/30/06
95300 (void) sprintf((char *)&s[0],"%d\0", number); 10/30/06
95400 s[strlen(s)] = 0x40; 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 19
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
95500 s[strlen(s)+1]= 0x40; 10/30/06
95600 } 10/30/06
95700 10/30/06
95800 /* ------------------------------------------------------------------*/ 10/30/06
95900 /* xatoi - takes an input decimal string from the display, */ 10/30/06
96000 /* NULL terminates it, and then calls atoi() to */ 10/30/06
96100 /* convert it to an integer. */ 10/30/06
96200 /* ------------------------------------------------------------------*/ 10/30/06
96300 int xatoi(char *s, int slen) 10/30/06
96400 { 10/30/06
96500 char zonedbuf[300]; 10/30/06
96600 memset(zonedbuf, 0x40, sizeof(zonedbuf)); 10/30/06
96700 if (slen > 300) slen = 300; 10/30/06
96800 memcpy(zonedbuf, s, slen); 10/30/06
96900 return(atoi(zonedbuf)); 10/30/06
97000 } 10/30/06
97100 10/30/06
97200 10/30/06
97300 /* ------------------------------------------------------------------*/ 10/30/06
97400 /* Routine to convert characters that are treated as hex (i.e. */ 10/30/06
97500 /* a character string of FF is treated as 0xFF) to its hexadecimal */ 10/30/06
97600 /* representation. */ 10/30/06
97700 /* ------------------------------------------------------------------*/ 10/30/06
97800 static char lhexmask[] = { 10/30/06
97900 0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 10/30/06
98000 0x70, 0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0 10/30/06
98100 }; 10/30/06
98200 10/30/06
98300 static char rhexmask[] = { 10/30/06
98400 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 10/30/06
98500 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F 10/30/06
98600 }; 10/30/06
98700 10/30/06
98800 static char *hexchars[] = { 10/30/06
98900 "0", "1", "2", "3", "4", "5", "6", "7", "8", 10/30/06
99000 "9", "A", "B", "C", "D", "E", "F" 10/30/06
99100 }; 10/30/06
99200 10/30/06
99300 void ctoh(char *s1, int s1_len, char *hexstring) 10/30/06
99400 { 10/30/06
99500 int hexlen; 10/30/06
99600 int i, k; 10/30/06
99700 int index = 0; 10/30/06
99800 10/30/06
99900 if (s1_len < 1) return; 10/30/06
100000 10/30/06
100100 hexlen = s1_len/2; 10/30/06
100200 10/30/06
100300 for (i=0; i<hexlen; i++) { 10/30/06
100400 for (k=0; k<16; k++) 10/30/06
100500 if (s1[index] == *hexchars[k]) { 10/30/06
100600 hexstring[i] = lhexmask[k]; 10/30/06
100700 break; 10/30/06
5770WDS V7R3M0 160422 SEU SOURCE LISTING 09/20/23 07:54:33 S10A7350 PAGE 20
SOURCE FILE . . . . . . . MBENDER/QCSRC
MEMBER . . . . . . . . . HTTPPOST03
SEQNBR*...+... 1 ...+... 2 ...+... 3 ...+... 4 ...+... 5 ...+... 6 ...+... 7 ...+... 8 ...+... 9 ...+... 0
100800 } 10/30/06
100900 10/30/06
101000 for (k=0; k<16; k++) 10/30/06
101100 if (s1[index+1] == *hexchars[k]) { 10/30/06
101200 hexstring[i] = hexstring[i] | rhexmask[k]; 10/30/06
101300 break; 10/30/06
101400 } 10/30/06
101500 10/30/06
101600 index = index+2; 10/30/06
101700 } 10/30/06
101800 } 10/30/06
101900 /* ------------------------------------------------------------------*/ 10/30/06
102000 /* Routine to convert characters to its hexadecimal representation. */ 10/30/06
102100 /* ------------------------------------------------------------------*/ 10/30/06
102200 void htoc(char *s1, int s1_len, char *charstring) 10/30/06
102300 { 10/30/06
102400 int i, k; 10/30/06
102500 int index = 0; 10/30/06
102600 char rightnibble = 0x0F; 10/30/06
102700 char leftnibble = 0xF0; 10/30/06
102800 10/30/06
102900 if (s1_len < 1) return; 10/30/06
103000 10/30/06
103100 for (i=0; i< s1_len; i++) { 10/30/06
103200 for (k=0; k<16; k++) 10/30/06
103300 if ((s1[i] & leftnibble ) == lhexmask[k]) { 10/30/06
103400 charstring[index] = *hexchars[k]; 10/30/06
103500 break; 10/30/06
103600 } 10/30/06
103700 10/30/06
103800 for (k=0; k<16; k++) 10/30/06
103900 if ((s1[i] & rightnibble) == rhexmask[k]) { 10/30/06
104000 charstring[index+1] = *hexchars[k]; 10/30/06
104100 break; 10/30/06
104200 } 10/30/06
104300 10/30/06
104400 index = index + 2; 10/30/06
104500 } 10/30/06
104600 } 10/30/06
* * * * E N D O F S O U R C E * * * *
