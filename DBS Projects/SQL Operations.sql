-- ***********************
-- Name: Harnoor Kaur Dran
-- Date: 15-10-2023
-- ***********************

--Q1 SOLUTION--
SELECT 
e.employeenumber,
e.lastname || ', ' || e.firstname AS "Employee Name",
o.phone,
e.extension,
o.city,
e.reportsto AS "Manager ID"


FROM
   employees e 
   JOIN
      offices o USING (officecode) 
WHERE 
e.reportsto IS NULL

ORDER BY
   o.city,
   e.employeenumber;
   
--Q2 SOLUTION--
SELECT 
e.employeenumber,
e.firstname || ' ' || e.lastname AS "Employee Name",
o.phone,
e.extension,
o.city
 FROM
 employees e
 JOIN offices o USING (officecode)
 WHERE
 UPPER(o.city) = 'NYC'
 OR UPPER(o.city) = 'TOKYO'
 OR UPPER(o.city)= 'PARIS'
 ORDER BY
 o.city,
 e.employeenumber;
 
 --Q3 SOLUTION--
 SELECT 
 e.employeenumber,
 e.lastname || ', ' ||e.firstname AS "Employee Name",
 o.phone,
 e.extension,
 o.city,
 e.reportsto AS "Manager ID",
 m.firstname || ' ' ||m.lastname AS "Manager Name"

 FROM
 employees e
 JOIN
 offices o USING (officecode),
 employees m
 WHERE
 (
 UPPER(o.city) = 'NYC'
OR  UPPER(o.city) = 'TOKYO'
OR  UPPER(o.city) = 'PARIS'
 )
 AND e.reportsto = m.employeenumber
 ORDER BY
 o.city,
 e.employeenumber;
 

 
 --Q6 SOLUTION--
 --Part a--
 SELECT DISTINCT c.customernumber, c.customername
FROM orders o1
JOIN orders o2 ON o1.customernumber = o2.customernumber AND o1.ordernumber <> o2.ordernumber
JOIN customers c ON o1.customernumber = c.customernumber
ORDER BY c.customernumber;
 
--Part b--
 SELECT c.customernumber, c.customername
FROM orders o1
LEFT JOIN orders o2 ON o1.customernumber = o2.customernumber AND o1.ordernumber <> o2.ordernumber
JOIN customers c ON o1.customernumber = c.customernumber
WHERE o2.customernumber IS NULL
ORDER BY c.customernumber, c.customername;

 