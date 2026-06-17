# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

#print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))
#print(pd.read_sql("""SELECT * FROM employees """, conn))
#print(pd.read_sql("""SELECT * FROM offices """, conn))
#print(pd.read_sql("""SELECT * FROM customers """, conn))
#print(pd.read_sql("""SELECT * FROM products """, conn))
#print(pd.read_sql("""SELECT * FROM orders """, conn))
#print(pd.read_sql("""SELECT * FROM payments """, conn))
#print(pd.read_sql("""SELECT * FROM orderdetails """, conn))

# STEP 1
df_boston = pd.read_sql("""
    SELECT firstName, lastName
    FROM employees
    INNER JOIN offices
        ON employees.officeCode = offices.officeCode
    WHERE city = 'Boston'
""", conn)

# STEP 2
df_zero_emp = pd.read_sql("""
    SELECT offices.officeCode, offices.city
    FROM offices
    LEFT JOIN employees
        ON employees.officeCode = offices.officeCode
    WHERE employees.employeeNumber IS NULL
""", conn)


# STEP 3
df_employee = pd.read_sql("""
    SELECT firstName, lastName, city, state
    FROM employees
    LEFT JOIN offices
        ON employees.officeCode = offices.officeCode
    ORDER BY firstName ASC, lastName ASC
""", conn)

# STEP 4
df_contacts = pd.read_sql("""
    SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
    FROM customers
    LEFT JOIN orders
        ON customers.customerNumber = orders.customerNumber
    WHERE orders.orderNumber IS NULL
    ORDER BY contactLastName ASC
""", conn)

# STEP 5
df_payment = pd.read_sql("""
    SELECT contactFirstName, contactLastName, amount, paymentDate
    FROM customers
    INNER JOIN payments
        ON customers.customerNumber = payments.customerNumber
    ORDER BY CAST(amount AS REAL) DESC, paymentDate DESC
""", conn)

# STEP 6
df_credit = pd.read_sql("""
    SELECT employees.employeeNumber,
           firstName,
           lastName,
           COUNT(customers.customerNumber) AS num_customers
    FROM employees
    INNER JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY employees.employeeNumber
    HAVING AVG(customers.creditLimit) > 90000
    ORDER BY num_customers DESC
""", conn)

# STEP 7
df_product_sold = pd.read_sql("""
    SELECT productName,
           COUNT(orderdetails.productCode) AS numorders,
           SUM(quantityOrdered) AS totalunits
    FROM products
    INNER JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    GROUP BY products.productCode
    ORDER BY totalunits DESC
""", conn)


# STEP 8
df_total_customers = pd.read_sql("""
    SELECT productName,
           products.productCode,
           COUNT(DISTINCT orders.customerNumber) AS numpurchasers
    FROM products
    INNER JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    INNER JOIN orders
        ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY products.productCode
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
df_customers = pd.read_sql("""
    SELECT COUNT(customerNumber) AS n_customers,
           offices.officeCode,
           offices.city
    FROM offices
    INNER JOIN employees
        ON offices.officeCode = employees.officeCode
    INNER JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY offices.officeCode
""", conn)

# STEP 10
df_under_20 = pd.read_sql("""
    SELECT DISTINCT employees.employeeNumber,
           firstName,
           lastName,
           offices.city,
           offices.officeCode
    FROM employees
    INNER JOIN offices
        ON employees.officeCode = offices.officeCode
    INNER JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    INNER JOIN orders
        ON customers.customerNumber = orders.customerNumber
    INNER JOIN orderdetails
        ON orders.orderNumber = orderdetails.orderNumber
    WHERE orderdetails.productCode IN (
        SELECT orderdetails.productCode
        FROM orderdetails
        INNER JOIN orders
            ON orderdetails.orderNumber = orders.orderNumber
        GROUP BY orderdetails.productCode
        HAVING COUNT(DISTINCT orders.customerNumber) < 20
    )
    ORDER BY firstName ASC
""", conn)





conn.close()