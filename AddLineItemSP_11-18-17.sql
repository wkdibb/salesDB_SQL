
/*
*********************************************************************************
Oracle 12c with SQL Developer
Relevant coding examples provided by Vicki Jonathan
Code independently written 2017-11-18 by Will Dibb

Stored procedure (AddLineItemSP) will issue INSERT command that adds 
a new row to the ORDERITEMS table. When INSERT is issues trigger is fired.
Stored procedure will contain ROLLBACK or COMMIT statements contingent 
on raised EXCEPTIONs. 

____________________________________________________________________________________________________
CUSTOMERS 1:1 ------ 0:M ORDERS 0:M ------ 1:1 SALESPERSONS
                                           ORDERS 1:1 ------ 0:M ORDERITEMS 0:M ------ 1:1 INVENTORY
**********************************************************************************
*/

SET VERIFY OFF
SET SERVEROUTPUT ON

CREATE OR REPLACE PROCEDURE AddLineItemSP
    ( inOrderID     IN      NUMBER
    , inPartID        IN      NUMBER
    , inQty            IN      NUMBER)
    
AS

        InsufficientStockQty EXCEPTION;
        PRAGMA EXCEPTION_INIT(InsufficientStockQty, -20123);

BEGIN 

        INSERT INTO ORDERITEMS ( OrderID, PartID, Qty )
        VALUES (inOrderID, inPartID, inQty );
        --InsertOrderItemsTRG will complete INSERT function by completing Detail field
        
EXCEPTION
        --RAISE here sends EXCEPTION out to code that executed this procedure
        
        WHEN InsufficientStockQty THEN
            --Raised by InsertOrderItemsTRG
            DBMS_OUTPUT.PUT_LINE ('AddLineItemSP EXCEPTION for InsufficientStockQty');
            RAISE;
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE (SQLCODE || ' -- ' || SQLERRM);
            RAISE;

END;