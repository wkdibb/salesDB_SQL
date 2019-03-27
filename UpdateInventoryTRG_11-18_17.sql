/*
*********************************************************************************
Oracle 12c with SQL Developer
Relevant coding examples provided by Vicki Jonathan
Code independently written 2017-11-18 by Will Dibb

UpdateInventoryTRG evaluates StockQty for new line item and raises
EXCEPTION as needed. EXCEPTION from UPDATE trigger goes into 
InsertOrderItemsTRG, and from there into AddLineItemsSP (main stored 
procedure) where transaction is halted and ROLLBACK issued. 

____________________________________________________________________________________________________
CUSTOMERS 1:1 ------ 0:M ORDERS 0:M ------ 1:1 SALESPERSONS
                                           ORDERS 1:1 ------ 0:M ORDERITEMS 0:M ------ 1:1 INVENTORY
**********************************************************************************
*/

SET VERIFY OFF
SET SERVEROUTPUT ON

CREATE OR REPLACE TRIGGER UpdateInventoryTRG
BEFORE UPDATE ON INVENTORY
FOR EACH ROW

DECLARE
    
    InsufficientStockQty EXCEPTION;
    PRAGMA EXCEPTION_INIT(InsufficientStockQty, -20123);
    
BEGIN
    --This is where INVENTORY stock quantity is checked
    --Again, using NEW inventory stock quantity since we want 
    --to check order value difference
    IF :new.StockQty < 0 THEN
        RAISE InsufficientStockQty;
    --RAISE goes to EXCEPTION in main program
    END IF;


EXCEPTION

    WHEN InsufficientStockQty THEN
        DBMS_OUTPUT.PUT_LINE('UpdateInventoryTRG Error: Order Quantity is too large.');
        RAISE;
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('UpdateInventoryTRG OTHERS EXCEPTION. ' || SQLCODE || ' --- ' || SQLERRM);
        RAISE;

END;
