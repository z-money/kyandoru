# kyanodoru
Configurable searcher of stock data.

The database is not included because it's too large for github.

You can build the database yourself if you want, but it takes a long time and generates a lot of CSV files and a pretty big database.
run:
```
python3 save_stock_names.py
python3 get_yahoo_stock_data.py
python3 save_yahoo_stock_data.py
```
This takes quite a while since it needs to download lots of CSVs.  You can make this faster by using a smaller company list in the data folder.
If get_yahoo_stock_data.py dies before finishing, you can restart it and it will pick up where it left off.

An example is provided in scripts/run.py.  You can run it (once you have a database) using:
```
python3 run.py ../sample_constraints/test_constraints_no_slope.json
```
This can take a little while to run as well.