/*
***************************************************************************************************
Oracle SQL Developer 

Relevant coding examples provided by Vicki Jonathan
Code independently written 2017-11-18 by Will Dibb

Set variable inputs, exceptions, and parameters for a customer sales
database. Update inventories with order inputs. 

____________________________________________________________________________________________________
CUSTOMERS 1:1 ------ 0:M ORDERS 0:M ------ 1:1 SALESPERSONS
                                           ORDERS 1:1 ------ 0:M ORDERITEMS 0:M ------ 1:1 INVENTORY
***************************************************************************************************
*/

SET SERVEROUTPUT ON FORMAT WRAPPED

DECLARE
        --Declare assignments for manual entry of Customer ID, Order ID, Part ID, and Order Quantity
        --Declare variable for updated stock quantity
        --Declare variable for message header in print output
        v_newcustid     NUMBER(4,0)     := &1;
        v_neworderid   NUMBER(4,0)     := &2;
        v_newpartid     NUMBER(4,0)     := &3;
        v_newqty         NUMBER(6,0)     := &4;
        v_StockQty       INVENTORY.StockQty%TYPE; 
        vMsg               VARCHAR2(512) := 'SALESDB 11-2017';
        
        --Declare exceptions for non-existent Customer IDs, Order IDs, or Part IDs
        --Declare exception for Customers who do not have the corresponding Order ID
        --Declare exception for an invalid Order quantity
        --Declare exception for an Order quantity greater than Inventory stock
        FailedCustID EXCEPTION;
        FailedOrderID EXCEPTION;
        FailedCustOrderMatch EXCEPTION;
        FailedPartID EXCEPTION;
        FailedQty EXCEPTION;
        InsufficientStock EXCEPTION;

BEGIN

        DBMS_OUTPUT.PUT_LINE (vMsg);
        
        BEGIN
            --Define customer ID input
            SELECT CustID
            INTO    v_newcustid
            FROM CUSTOMERS 
            WHERE CustID = v_newcustid;
        
        --Print confirmation of valid Customer ID input    
        DBMS_OUTPUT.PUT_LINE (v_newcustid || ' is a valid Customer ID.');
        
        --Define exception parameter for non-existent Customer ID and raise exception
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
            RAISE FailedCustID;
        
        END;
        
        BEGIN
            --Define Order ID input
            SELECT OrderID
            INTO v_neworderid
            FROM ORDERS
            WHERE OrderID = v_neworderid;
        
        --Print confirmation of valid Order ID input
        DBMS_OUTPUT.PUT_LINE (v_neworderid || ' is a valid Order ID.');
        
        --Define exception parameter for non-existent Order ID and raise exception    
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
            RAISE FailedOrderID;
    
        END;
        
        BEGIN
            --Define Order ID and Customer ID input and relationship
            SELECT CUSTOMERS.CustID
             ,           ORDERS.OrderID
            INTO v_newcustid
             ,        v_neworderid
            FROM CUSTOMERS JOIN ORDERS ON
                  CUSTOMERS.CustID = ORDERS.CustID 
            WHERE ORDERS.CustID = v_newcustid
            AND ORDERS.OrderID = v_neworderid;
            
       --Print confirmation of correlating Order ID with existing Customer ID
       DBMS_OUTPUT.PUT_LINE ('Customer ID ' || v_newcustid || ' has placed Order ID ' || v_neworderid || '.');
        
        --Define exception parameter for no correlation between Order ID and Customer ID inputs
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
            RAISE FailedCustOrderMatch;
        
        END;
        
        BEGIN
             --Define Part ID input
             SELECT PartID
             INTO v_newpartid
             FROM INVENTORY
             WHERE PartID = v_newpartid;
        
        --Print confirmation of valid Part ID input
        DBMS_OUTPUT.PUT_LINE(v_newpartid || ' is a valid Part ID.');
        
        --Define exception parameter for non-existent Part ID and raise exception
        EXCEPTION
             WHEN NO_DATA_FOUND THEN
             RAISE FailedPartID;
        
        END;
        
        BEGIN
        
        --Validate positive integer input for Order quantity
        IF v_newqty < 1 THEN
        RAISE FailedQty;
        ELSE   DBMS_OUTPUT.PUT_LINE(v_newqty || ' is a valid Quantity.');
        END IF;
        
        END;
        
        BEGIN
            --Insert Order line item with input Order ID, Part ID, and order quantity variables and define unique detail
            INSERT INTO ORDERITEMS (OrderID
            , Detail
            , PartID
            , Qty)
            VALUES (v_neworderid
            ,  (SELECT DISTINCT NVL(MAX(Detail) + 1,0)
               FROM ORDERITEMS)
            , v_newpartid
            , v_newqty);
          
        --Define exception for missing fields           
        EXCEPTION
             WHEN NO_DATA_FOUND THEN
             DBMS_OUTPUT.PUT_LINE('Field Error: One or more INSERT fields is not valid.');
            
        END;

        BEGIN
            
            --Update Inventory stock quantity based on order quantity
            UPDATE INVENTORY 
            SET StockQty = StockQty - v_newqty
            WHERE INVENTORY.PartID = v_newpartid;
            
            --Define Stock Quantity input
            SELECT StockQty
            INTO v_StockQty
            FROM INVENTORY
            WHERE INVENTORY.PartID = v_newpartid;
            
            --Validate available stock quantity available with respect to order quantity and raise exception for a greater order quantity
            IF v_StockQty < 0 THEN
                RAISE InsufficientStock;
            END IF; 
            
            --Print confirmation of transaction including both line item addition and inventory stock quantity change
            DBMS_OUTPUT.PUT_LINE('Transaction complete. Line item added for Order ID ' || v_neworderid || ' for ' || v_newqty || ' units of Part ID ' || v_newpartid || '.');
            DBMS_OUTPUT.PUT_LINE('Inventory has been updated to ' || v_StockQty || ' units of Part ' || v_newpartid || '.');
        
        --Define exception for missing fields in update
        EXCEPTION
             WHEN NO_DATA_FOUND THEN
             DBMS_OUTPUT.PUT_LINE('Update field is not valid.');
                
        END;
            
EXCEPTION
        
        --Define raised exceptions for invalid customer ID, Order ID, Part ID, or order quantity input and print specific error results
        --Define raised exceptions for no correlation between customer ID and Order ID input and print specific error result
        --Define raised exception for order quantities greater than available inventory stock and print specific error result
        --Roll back program and transaction if entries are invalid
        --Define other error print result
        WHEN FailedCustID THEN 
            DBMS_OUTPUT.PUT_LINE('Customer ID #: ' || v_newcustid || ' does not exist.');
            ROLLBACK;
        WHEN FailedOrderID THEN
            DBMS_OUTPUT.PUT_LINE('Order ID #: ' || v_neworderid || ' does not exist.');
            ROLLBACK;
        WHEN FailedCustOrderMatch THEN
            DBMS_OUTPUT.PUT_LINE('The Customer ID #: ' || v_newcustid || ' does not match the respective Order ID #: ' || v_neworderid);
            ROLLBACK;
        WHEN FailedPartID THEN
            DBMS_OUTPUT.PUT_LINE('The Part ID #: ' || v_newpartid || ' does not exist.');
            ROLLBACK;
        WHEN FailedQty THEN
            DBMS_OUTPUT.PUT_LINE('The quantity ' || v_newqty || ' is not a valid order quantity.');
            ROLLBACK;
        WHEN InsufficientStock THEN
            DBMS_OUTPUT.PUT_LINE('Transaction Error: There is insufficient stock quantity for an order of ' || v_newqty || ' units of Part ID ' || v_newpartid || '.');
            ROLLBACK;
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE(SQLERRM);
     
    --Commit to valid entries for order line item insert and updated inventory stock quantity       
    COMMIT;
        
END;
/



