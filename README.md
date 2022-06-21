# Fink Elasticc templates

This repo hosts necessary files to create and test a science module using Elasticc data. To start, useful links:

- DESC GitHub Elasticc repo: https://github.com/LSSTDESC/elasticc
- DESC Elasticc presentation & data: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/

## Elasticc alert data

Elasticc alert data is different from the data used by the training. First, the schema is different (renamed fields, less available fields). You can inspect some of the difference [here](https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/TRAINING_SAMPLES/A_FORMAT.TXT).

For the sake of this exercise, we exported data in the form required by the broker. We internally use parquet. Each file contains a table, whose rows are individual alerts, and columns are alert fields. You will find two exports in the folder `data`.

### `data/elasticc_test0.parquet`

This is a basic export of the test data given by DESC before the challenge (https://github.com/LSSTDESC/plasticc_alerts/tree/main/tests/test01). It contains 5,693 alerts. The alerts have usually long history.

### `data/elasticc_test1.parquet`

Export of the first 27,993 alerts from the challenge.

### Inputing directly alerts from the training set

TBD

## Processing alert data

For the sake of simplicity, we will abstract all the technical details of Fink (e.g. no use of Apache Spark), and keep only what is needed to add values to alerts. A science module in Fink is simply a Python routine that takes as input a set of alert fields, and output a new field based on the user logic.

In practice, the science module operates on batches of alerts, materialised as Pandas Series for each alert field. We provide a basic [example](mymodule) to familiarise with the structure of the science module. It contains two parts:
1. `processor.py`: entry point for the broker.
2. `utils.py`: anything else required by the science module.

This example takes alerts, constructs lightcurves (concatenating the current measurement with the alert history), and for those with at least 2 measurements in the g band, extract the slope in the g band. To test it, just run:

```python
python test_module.py
```

Note the example has not been optimised! The goal is to learn how to construct a module.

## Going further

Although in practice the logic is always the same as described in this example, some examples can be more complicated than others. You can have a look at what is currently done in Fink with ZTF data on production: https://github.com/astrolabsoftware/fink-science.

## Difference with a full broker version

The broker is using Apache Spark to distribute the load on several machines, and process chunks of alerts in parallel. The syntax is very similar to the one described here. One of the main difference is that machines do not have access to a shared local storage, hence any IO to be read/written (configuration files if need be, trained models, ...) must be minimised or distributed beforehand.
