**Predictor search** is a small tool for exploring statistical relations between two datasets.
For example, precipitation and sea surface temperature. First, **Predictor search** calculates
correlations between all possible pairs of points (grid nodes) from the datasets and store the results
into the db. Second, the **Predictor search** provides the tools to query this database and
explore the relationships.

## Install
Clone repository to your computer. No other actions is needed.

## Dependencies

This programms have been tested to work with Python 3.5

* sqlalchemy 1.1.5
* numpy 1.11
* netCDF4 1.2.7, h5py 2.6 (used to read input data)
* scipy 0.18.1 (only scipy.stats.spearmanr)

## Tutorial

1. Open `settings.py` and following the example provided set the `x_config` and `y_config` to point
to your datafiles.

2. Set the database connection in `settings.py` if needed. By default the sqlite will be used.
Default db location is `./db/main.sqlite`

3. Run `create_db.py` to execute

`>>> create_db()`

`>>> add_meta()`

This will create the db, tables and fill the list of points existing in the datafile

4. To add data run `add_data(yMin, yMax, month)` from `create_db.py`. This can take a long time depending on a size
of your dataset.

5. Use functions from `queries.py` to extract results from db
