--SELECT * FROM customers;

SELECT t1.country, sum(t2.amount) from customers as t1 JOIN orders as t2 ON t1.id = t2.customer_id GROUP BY country;