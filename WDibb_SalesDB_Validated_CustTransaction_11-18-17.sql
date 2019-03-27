/*
*********************************************************************************
Oracle 12c with SQL Developer
Relevant coding examples provided by Vicki Jonathan
Code independently written 2017-11-18 by Will Dibb

Transaction variables (CustID, OrderID, PartID, Qty) passed to program with vars
[&1, &2, &3, &4]. Sequential blocks to validate CustID, OrderID,
CustID:OrderID pairing, PartID, and nonzero Qty before calling the stored procedure.

Transaction commits only if input passes all validations

**********************************************************************************
*/

SET VERIFY OFF
SET SERVEROUTPUT ON FORMAT WRAPPED 

DECLARE   --Main program variables defined and available to all internal blocks


        -- Input parameters with substitution variables
        inCustID                     CUSTOMERS.CustID%TYPE;
        inOrderID                   ORDERS.OrderID%TYPE;
        inPartID                      INVENTORY.PartID%TYPE;
        inQty                          ORDERITEMS.Qty%TYPE;
        
        --Program constants
        vProgram                    VARCHAR2(20) := 'Lab 7';
        vProgrammer              VARCHAR2(20) := 'Will Dibb';
        
        --Program variables
        vCname                      CUSTOMERS.Cname%TYPE;   --CustID validation
        vSalesDate                  ORDERS.SalesDate%TYPE;     --OrderID validation
        vEmpID                      ORDERS.EmpID%TYPE;         --Cust ID/OrderID validation
        vDescription                INVENTORY.Description%TYPE; --PartID validation
        vOldStockQty               INVENTORY.StockQty%TYPE;    --pre-order stock quantity
        vValidQty                    CHAR(1);                               --Y/N quantity validation
        vDetail                        ORDERITEMS.Detail%TYPE;      -- for new line item
        vNewStockQty              INVENTORY.Stockqty%TYPE;    --post-order stock quantity for check
        vMsg                           VARCHAR2(512);                   --print line
        
        InvalidQty                          EXCEPTION;      --input quantity value error
        InsufficientStockQty             EXCEPTION;       --not enough stock error
        
BEGIN   --Main program block

            --Initialize substitution variables
            inCustID    := &1;
            inOrderID  := &2;
            inPartID     := &3;
            inQty         := &4;
            
            --Main processing begins with header and print of input values
            DBMS_OUTPUT.PUT_LINE(vProgram ||  ' by ' || vProgrammer);
            DBMS_OUTPUT.PUT_LINE('INPUT values are: CustID = ' || inCustID || ', OrderID = ' || inOrderID || 
            ', PartID = ' || inPartID || ', and Quantity = ' || inQty);

            
            BEGIN  --Validate CustID by retrieving customer name
            
                vCname := '  ';  --initializes validation variable before query runs
                SELECT Cname
                INTO vCname   --table the data to program variable for valid entry
                FROM CUSTOMERS
                WHERE Custid = inCustID; --associate by PK customer ID
                
                --if input CustID is invalid, processing drops into EXCEPTION handler
                DBMS_OUTPUT.PUT_LINE('CustID ' || inCustID || ' is valid for customer ' || vCname);
                
            EXCEPTION
                
                WHEN NO_DATA_FOUND THEN
                        DBMS_OUTPUT.PUT_LINE('NO_DATA_FOUND for invalid CustID input ' || inCustID || '. Processing continues. ');
                WHEN OTHERS THEN
                        DBMS_OUTPUT.PUT_LINE (vProgram || ' OTHERS EXCEPTION for invalid CustID input. ' || 
                        SQLCODE || ' -- ' || SQLERRM);  --show error message
                        RAISE; --do not continue with unhandled validation error
            END;
            
            
            BEGIN
            
                vSalesDate := '01-JAN-1900'; -- initializes validation variable 
                SELECT SalesDate
                INTO vSalesDate
                FROM ORDERS
                WHERE OrderID = inOrderID;
                DBMS_OUTPUT.PUT_LINE('OrderID ' || inOrderID || ' for Sales Date ' || vSalesDate || ' is valid.');
                
            EXCEPTION
                
                WHEN NO_DATA_FOUND THEN
                        DBMS_OUTPUT.PUT_LINE('NO_DATA_FOUND for invalid OrderID input' || inOrderID || '. Processing continues.');
                WHEN OTHERS THEN
                        DBMS_OUTPUT.PUT_LINE (vProgram || ' OTHERS EXCEPTION for invalid OrderID input. ' || SQLCODE || ' -- ' || SQLERRM);  --show error message
                        RAISE; --do not continue with unhandled validation error
                        
            END;
            
            
            BEGIN  -- validate paired CustID/OrderID combination
            
                vEmpID := 0;  -- intializes validation variable
                SELECT EmpID
                INTO vEmpID
                FROM ORDERS
                WHERE OrderID = inOrderID
                AND CustID = inCustID;
                DBMS_OUTPUT.PUT_LINE('CustID/OrderID pairing is valid for Employee #' || vEmpID);
                
            EXCEPTION
                
                WHEN NO_DATA_FOUND THEN
                        DBMS_OUTPUT.PUT_LINE('NO_DATA_FOUND for invalid paired OrderID/CustID input. Processing continues.');
                WHEN OTHERS THEN
                        DBMS_OUTPUT.PUT_LINE (vProgram || ' OTHERS EXCEPTION for invalid paired OrderID/CustID input. ' || SQLCODE || ' -- ' || SQLERRM);  --show error message
                        RAISE; --do not continue with unhandled validation error
            
               END;     
            
            
                BEGIN  --validate PartID and retrieve description and stock quantity
                
                    vDescription := '  '; --initializes validation variable
                    vOldStockQty := 0;  --initializes original stock quantity variable
                    SELECT Description, StockQty
                    INTO vDescription, vOldStockQty
                    FROM INVENTORY
                    WHERE PartID = inPartID;
                    DBMS_OUTPUT.PUT_LINE('PartID #' || inPartID || ' is valid for ' || vDescription);
                    DBMS_OUTPUT.PUT_LINE('with ' || vOldStockQty || ' units in inventory.');
                    
                EXCEPTION
                
                WHEN NO_DATA_FOUND THEN
                        DBMS_OUTPUT.PUT_LINE('NO_DATA_FOUND for invalid PartID input. Processing continues.');
                WHEN OTHERS THEN
                        DBMS_OUTPUT.PUT_LINE (vProgram || ' OTHERS EXCEPTION for invalid PartID input. ' || SQLCODE || ' -- ' || SQLERRM);  --show error message
                        RAISE; --do not continue with unhandled validation error
            
               END;     
               
               
               BEGIN  --validate quantity input
               
                    IF inQty > 0 THEN
                        vValidQty := 'Y';
                        
                    ELSE
                        vValidQty := 'N';
                        RAISE InvalidQty;
                    END IF;
                
                EXCEPTION
                
                    WHEN InvalidQty THEN
                        DBMS_OUTPUT.PUT_LINE('Invalid quantity by user-defined exception. Processing continues.');
                        --exception not raised here to continue processing even with invalid quantity
                    WHEN OTHERS THEN
                        DBMS_OUTPUT.PUT_LINE(vProgram || ' OTHERS EXCEPTION quantity validation error.' || SQLCODE || ' -- ' || SQLERRM);
                        RAISE; --do not continue with unhandled validation error
                    
                END;
                
                
                BEGIN  -- block to process validated order transaction
                    
                    --did all input validate?
                    IF vCname > '  ' 
                    AND vSalesDate > '01-JAN-1900'
                    AND vEmpid > 0
                    AND vDescription > '  '
                    AND vValidQty = 'Y' THEN
                    
                        DBMS_OUTPUT.PUT_LINE('Input passed all validations. Transaction proceeding.');
                        
                        SAVEPOINT StartTransaction;
                        
                        AddLineItemSP (inOrderID, inPartID, inQty);
                        -- When AddLineItemSP returns correctly then COMMIT
                        --Otherwise exception goes to main program level EXCEPTION
                        DBMS_OUTPUT.PUT_LINE('Transaction successful for CustID = ' || inCustID || ', OrderID = ' || inOrderID || 
                         ', PartID = ' || inPartID || ', and Quantity = ' || inQty);
                        
                        COMMIT;
                    
                    ELSE
                        
                        DBMS_OUTPUT.PUT_LINE('Input did not pass all validations. Transaction does not proceed.');
                        
                    END IF; 
                    --EXCEPTION does not exist for this transaction block, errors here move to 
                    --main program EXCEPTION
                
                END;
                        
            DBMS_OUTPUT.PUT_LINE (vProgram || ' has completed.');       
                        
EXCEPTION --Main program exception handler
            
        WHEN InsufficientStockQty THEN
            DBMS_OUTPUT.PUT_LINE (vProgram || ' InsufficientStockQty EXCEPTION given ' || inQty || ' units of Part #' || inPartID || ' not in stock');
            DBMS_OUTPUT.PUT_LINE ('Transaction UNSUCCESSFUL with ROLLBACK');
            ROLLBACK TO StartTransaction;
            
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE (vProgram || ' OTHERS EXCEPTION. Transaction UNSUCCESSFUL with ROLLBACK.' || SQLCODE || ' -- ' || SQLERRM);
            ROLLBACK TO StartTransaction;
            
END;
/

                        
                        
                    
                    

    

            
                
                
            