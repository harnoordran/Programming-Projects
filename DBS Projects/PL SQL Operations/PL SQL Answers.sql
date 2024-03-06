-- *********************** 
-- Name: Harnoor Kaur Dran
-- ID: 145433223 
-- Date: 16-02-2024 
-- Purpose: Lab 5 DBS311 
-- ***********************

SET SERVEROUTPUT ON;
-- Question 1 : To get an integer number and check if it is even or odd
-- ANSWER 1
CREATE OR REPLACE PROCEDURE even_odd(
num IN NUMBER
) AS
BEGIN 
    IF MOD(num,2) = 0 THEN
        DBMS_OUTPUT.PUT_LINE('The number is even.');
    ELSE 
        DBMS_OUTPUT.PUT_LINE('The number is odd.');
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error!');
END even_odd;

-- Question 2 : To get employee information from the employee number
-- ANSWER 2
CREATE OR REPLACE PROCEDURE find_employee(
    emp_id IN NUMBER
) AS
    v_first_name employees.first_name%TYPE;
    v_last_name employees.last_name%TYPE;
    v_email employees.email%TYPE;
    v_phone employees.phone%TYPE;
    v_hire_date employees.hire_date%TYPE;
    v_job_title employees.employee_id%TYPE;
BEGIN
    SELECT first_name, last_name, email, phone, hire_date, employee_id
    INTO v_first_name, v_last_name, v_email, v_phone, v_hire_date, v_job_title
    FROM employees
    WHERE employee_id = emp_id;

    DBMS_OUTPUT.PUT_LINE('First name: ' || v_first_name);
    DBMS_OUTPUT.PUT_LINE('Last name: ' || v_last_name);
    DBMS_OUTPUT.PUT_LINE('Email: ' || v_email);
    DBMS_OUTPUT.PUT_LINE('Phone: ' || v_phone);
    DBMS_OUTPUT.PUT_LINE('Hire date: ' || TO_CHAR(v_hire_date, 'DD-MON-YY'));
    DBMS_OUTPUT.PUT_LINE('Job title: ' || v_job_title);
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Employee not found.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error!');
END find_employee;

-- Question 3 : Update the price of all products in a given category
-- ANSWER 3
CREATE OR REPLACE PROCEDURE update_price_by_cat(
    category_id IN products.category_id%TYPE,
    amount IN NUMBER
) AS
    rows_updated NUMBER;
BEGIN
    -- Update price of products in the specified category by the given amount
    UPDATE products
    SET list_price = list_price + amount
    WHERE category_id = update_price_by_cat.category_id
    AND list_price > 0;

    -- Get the number of rows updated
    rows_updated := SQL%ROWCOUNT;

    -- Display the number of updated rows
    DBMS_OUTPUT.PUT_LINE('Number of updated rows: ' || rows_updated);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error updating prices.');
END update_price_by_cat;

-- Question 4 : Find the average price of all the products and store in a variable
-- same type.
-- ANSWER 4
CREATE OR REPLACE PROCEDURE update_price_under_avg AS
    avg_price NUMBER(9,2);
    rows_updated NUMBER;
BEGIN
    -- Calculate average price of all products
    SELECT AVG(list_price) INTO avg_price FROM products;

    -- Update price based on average price condition
    IF avg_price <= 1000 THEN
        -- If average price is less than or equal to $1000, increase price by 2%
        UPDATE products
        SET list_price = list_price * 1.02
        WHERE list_price < avg_price;
    ELSE
        -- If average price is greater than $1000, increase price by 1%
        UPDATE products
        SET list_price = list_price * 1.01
        WHERE list_price < avg_price;
    END IF;

    -- Get the number of rows updated
    rows_updated := SQL%ROWCOUNT;
    
    -- Display the number of updated rows
    DBMS_OUTPUT.PUT_LINE('Number of updated rows: ' || rows_updated);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error updating prices.');
END update_price_under_avg;

-- Question 5 : Show the number of products in each price category.
-- ANSWER 5
CREATE OR REPLACE PROCEDURE product_price_report AS
    avg_price NUMBER(9,2);
    min_price NUMBER(9,2);
    max_price NUMBER(9,2);
    cheap_count NUMBER := 0;
    fair_count NUMBER := 0;
    exp_count NUMBER := 0;
BEGIN
    -- Find average, minimum, and maximum prices
    SELECT AVG(list_price), MIN(list_price), MAX(list_price)
    INTO avg_price, min_price, max_price
    FROM products;

    -- Calculate price thresholds
    DECLARE
        cheap_threshold NUMBER := (avg_price - min_price) / 2;
        exp_threshold NUMBER := (max_price - avg_price) / 2;
    BEGIN
        -- Iterate through products and categorize them
        FOR product IN (SELECT list_price FROM products) LOOP
            IF product.list_price < cheap_threshold THEN
                cheap_count := cheap_count + 1;
            ELSIF product.list_price > exp_threshold THEN
                exp_count := exp_count + 1;
            ELSE
                fair_count := fair_count + 1;
            END IF;
        END LOOP;
    END;

    -- Display the counts for each category
    DBMS_OUTPUT.PUT_LINE('Cheap: ' || cheap_count);
    DBMS_OUTPUT.PUT_LINE('Fair: ' || fair_count);
    DBMS_OUTPUT.PUT_LINE('Expensive: ' || exp_count);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error generating product price report.');
END product_price_report;





























































































    