/*
*********************************************************************************
Oracle 12c with SQL Developer
Relevant coding examples provided by Vicki Jonathan
Code independently written 2017-11-18 by Will Dibb

INSERT trigger (InsertOrderitemsTRG) assigns new Detail column value and UPDATE command
reduces StockQty in INVENTORY table given line item amount. UPDATE trigger then fires, if
there is UPDATE trigger exception then INSERT trigger will RAISE exception causing AddLineItemSP 
to ROLLBACK.

____________________________________________________________________________________________________
CUSTOMERS 1:1 ------ 0:M ORDERS 0:M ------ 1:1 SALESPERSONS
                                           ORDERS 1:1 ------ 0:M ORDERITEMS 0:M ------ 1:1 INVENTORY
**********************************************************************************
*/

SET VERIFY OFF
SET SERVEROUTPUT ON

CREATE OR REPLACE TRIGGER InsertOrderItemsTRG
BEFORE INSERT ON ORDERITEMS
FOR EACH ROW

DECLARE 

        InsufficientStockQty EXCEPTION;
        PRAGMA EXCEPTION_INIT(InsufficientStockQty, -20123);
        
BEGIN

        --Add detail value for INSERT in AddLineItem stored procedure
        --Retrieve maximum value of Detail for OrderID and add one for new Detail
         --':new' here references NEW value, since UPDATE will have both old and new row
        
        SELECT NVL(MAX(Detail),0) + 1
        INTO :new.Detail
        FROM ORDERITEMS
        WHERE OrderID = :new.OrderID;
        
        --Update inventory quantity by subtracting quantity in new order
        UPDATE INVENTORY
        SET StockQty = (StockQty - :new.Qty)
        WHERE PartID = :new.PartID;     --This will cause UpdateInventoryTRG to fire.
        
EXCEPTION
        --RAISE here sends EXCEPTION to the procedure that caused this trigger function to fire
        WHEN InsufficientStockQty THEN
        -- RAISED by UpdateInventoryTRG
             DBMS_OUTPUT.PUT_LINE ('InsertOrderItemsTRG EXCEPTION for InsufficientStockQty');
            RAISE;
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE (SQLCODE || ' -- ' || SQLERRM);
            RAISE;
            
END;
            
        
        
        
            
                
                
            