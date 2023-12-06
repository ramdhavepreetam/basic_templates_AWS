"Gather  (cost=114307.16..849307.58 rows=1980917 width=148)"
"  Workers Planned: 1"
"  ->  Parallel Hash Left Join  (cost=113307.16..650215.88 rows=1165245 width=148)"
"        Hash Cond: (((""DCPP0113U"".""ITMID"")::text = (d.""ITMID"")::text) AND ((c.""GLFINENT"")::text = (d.""GLFINENT"")::text))"
"        ->  Parallel Hash Left Join  (cost=106653.96..578039.42 rows=1129788 width=138)"
"              Hash Cond: ((""DCPP0113U"".""ITMID"")::text = (e.""ITMID"")::text)"
"              ->  Nested Loop  (cost=4.49..415872.26 rows=1129788 width=137)"
"                    ->  Hash Left Join  (cost=3.92..7200.96 rows=58138 width=32)"
"                          Hash Cond: (((b.""CSTNO"")::text = (c.""CSTNO"")::text) AND ((b.""CSTSFX"")::text = (c.""CSTSFX"")::text))"
"                          ->  Parallel Index Scan using idx_custom_dcpp0115_cstno on ""DCPP0115"" b  (cost=0.57..6742.87 rows=58138 width=28)"
"                                Index Cond: ((""CSTNO"")::text = 'A300'::text)"
"                          ->  Hash  (cost=3.32..3.32 rows=2 width=12)"
"                                ->  Index Scan using ""DOPCMST0_DOPCMST0"" on ""DOPCMST0"" c  (cost=0.29..3.32 rows=2 width=12)"
"                                      Index Cond: ((""CSTNO"")::text = 'A300'::text)"
"                    ->  Append  (cost=0.56..6.99 rows=4 width=127)"
"                          ->  Index Scan using idx_custom_dcpp0113u_priceid on ""DCPP0113U""  (cost=0.56..2.33 rows=1 width=127)"
"                                Index Cond: ((""PRICEID"")::text = (b.""PRICEID"")::text)"
"                          ->  Index Scan using idx_custom_dcpp0113c_priceid on ""DCPP0113C""  (cost=0.56..2.07 rows=1 width=127)"
"                                Index Cond: ((""PRICEID"")::text = (b.""PRICEID"")::text)"
"                          ->  Index Scan using idx_custom_dcpp0113m_priceid on ""DCPP0113M""  (cost=0.43..1.38 rows=1 width=128)"
"                                Index Cond: ((""PRICEID"")::text = (b.""PRICEID"")::text)"
"                          ->  Index Scan using idx_custom_dcpp0113p_priceid on ""DCPP0113P""  (cost=0.43..1.19 rows=1 width=119)"
"                                Index Cond: ((""PRICEID"")::text = (b.""PRICEID"")::text)"
"              ->  Parallel Hash  (cost=84535.54..84535.54 rows=1272154 width=12)"
"                    ->  Parallel Seq Scan on ""DCPP0124"" e  (cost=0.00..84535.54 rows=1272154 width=12)"
"        ->  Parallel Hash  (cost=3360.68..3360.68 rows=150768 width=27)"
"              ->  Parallel Seq Scan on ""DCPP0111"" d  (cost=0.00..3360.68 rows=150768 width=27)"





	Explain	WITH PRICING_DATA AS (
                SELECT  a."PRICEID", b."CSTNO", b."CSTSFX", a."ITMID", a."EFFDATE", a."PDCFRZ", a."DSPFRZ",
                    a."CHANNEL", a."CLIST", a."RESALE", a."STDDLRNET", a."BESTCODE", a."QTYBREAK", a."QTYDISC",
                    a."QTYPRICE", a."QTYFNL", a."QTBRKEND", a."PROMO", a."PROMOPCT", a."SANBR", a."PHASE",
                    a."SALINE", a."BASEQTY", a."SABSTNET", a."SAEFFDATE", a."SAEXPDATE", a."FNLNET",
                    c."GLFINENT", d."CORFLG", d."CORPRC", d."CORGRP", d."CORCLS",e."GRPCDE"
                FROM (
                    SELECT * FROM ppdglobal."DCPP0113U"
                    UNION ALL
                    SELECT * FROM ppdglobal."DCPP0113C"
                    UNION ALL
                    SELECT * FROM ppdglobal."DCPP0113M"
                    UNION ALL
                    SELECT * FROM ppdglobal."DCPP0113P"
                ) AS a
                JOIN ppdglobal."DCPP0115" AS b ON a."PRICEID" = b."PRICEID"
                LEFT JOIN ppdglobal."DOPCMST0" AS c ON c."CSTNO" = b."CSTNO" AND c."CSTSFX" = b."CSTSFX"
                LEFT JOIN ppdglobal."DCPP0111" AS d ON a."ITMID" = d."ITMID" AND c."GLFINENT" = d."GLFINENT"
                LEFT JOIN ppdglobal."DCPP0124" AS e ON a."ITMID" = e."ITMID"
            )
            SELECT * FROM PRICING_DATA WHERE "CSTNO" = 'A300' 
