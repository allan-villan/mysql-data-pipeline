# data-pipeline-test
The purpose of this repository is to create a data pipeline using Python to assist with the sale of tickets. It takes .csv data and saves it in a MySQL database.


## Getting started:
- All functionality is included in the main.py file
- After running the file, just follow the prompt displayed by the console
- Results are output to the console

### Prerequisites:
  You must have ***pandas*** and ***mysql-connector-python*** installed

### Installing:

> pip install pandas

> pip install mysql-connector-python

## Data Preview

### Ticket Sales Table Schema

| Column | Type |
---------| ------
| ticket_id | INT |
| trans_date | INT |
| event_id | INT |
| event_name | VARCHAR(50) |
| event_date | DATE |
| event_type | VARCHAR(10) |
| event_city | VARCHAR(20) |
| customer_id | INT |
| price | DECIMAL |
| num_tickets | INT |

### CSV Data
|ticket_id | trans_date|event_id|event_name                                |event_date|event_type|event_city   |customer_id|price|num_tickets|
|----------|-----------|--------|------------------------------------------|----------|----------|-------------|-----------|-----|-----------|
|1         |2020-08-01 |100     |The North American International Auto Show|2020-09-01|Exhibition|Michigan     |123        |35.00|3          |
|2         |2020-08-03 |101     |Carlisle Ford Nationals                   |2020-09-30|Exhibition|Carlisle     |151        |43.00|1          |
|3         |2020-08-03 |102     |Washington Spirits vs Sky Blue FC         |2020-08-30|Sports    |Washington DC|223        |59.34|5          |
|4         |2020-08-05 |103     |Christmas Spectacular                     |2020-10-05|Theater   |New York     |223        |89.95|2          |
|5         |2020-08-05 |100     |The North American International Auto Show|2020-09-01|Exhibition|Michigan     |126        |35.00|1          |
|6         |2020-08-05 |103     |Christmas Spectacular                     |2020-10-05|Theater   |New York     |1024       |89.95|3          |
