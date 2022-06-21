# Fink Elasticc templates

This repo hosts necessary files to create and test a science module using Elasticc data. To start, useful links:

- DESC GitHub Elasticc repo: https://github.com/LSSTDESC/elasticc
- DESC Elasticc presentation & data: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/

## Elasticc alert data

Elasticc alert data is different from the data used by the training. First, the schema is different (renamed fields, less available fields). You can inspect some of the difference [here](https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/TRAINING_SAMPLES/A_FORMAT.TXT). Second, the format is different (training = full lightcurves format, alert = chunked lightcurves).

For the sake of this exercise, we exported data in the form required by the broker. We internally use Apache Parquet (we receive Apache Avro, and convert straight). Each file contains a table, whose rows are individual alerts, and columns are alert fields. You will find two exports in the folder `data`.

### `data/elasticc_test0.parquet`

This is a basic export of the test data given by DESC before the challenge (https://github.com/LSSTDESC/plasticc_alerts/tree/main/tests/test01). It contains 5,693 alerts. The alerts have usually long history.

### `data/elasticc_test1.parquet`

Export of the first 27,993 alerts from the challenge.

### Inputing directly alerts from the training set

TBD

## Fink science module

For the sake of simplicity, we will abstract all the technical details of Fink (e.g. no use of Apache Spark), and keep only what is needed to add values to alerts. A science module in Fink is simply a Python routine that takes as input a set of alert fields, and output a new field based on the user logic.

In practice, the science module operates on batches of alerts, materialised as Pandas Series for each alert field. We provide a basic [example](mymodule) to familiarise with the structure of the science module. It contains two parts:
1. `processor.py`: entry point for the broker.
2. `utils.py`: anything else required by the science module.

## Running

### Requirements

This example has been tested on Python 3.7 & 3.9. Higher versions might work. Other dependencies:
- numpy>=1.19.5
- scipy>=1.7.3
- pandas==1.3.5

In case you do not want to mess up your environment (and work in the environment of the broker), you can pull one of the Fink docker images (dev or prod) at https://hub.docker.com/r/julienpeloton/fink-ci/tags, and clone the repo inside.

### Test files

This example takes alerts, constructs lightcurves (concatenating the current measurement with the alert history), and for those with at least 2 measurements in the g band, extract the slope in the g band. To test it, just run:

```python
python test_module.py
```

Note the example has not been optimised! The goal is to learn how to construct a module.

## Going further

Although in practice the logic is always the same as described in this example, some examples can be more complicated than others. You can have a look at what is currently done in Fink with ZTF data on production: https://github.com/astrolabsoftware/fink-science.

### FAQ

#### Can the science module output more than one new field?

Yes, but the syntax becomes slightly different between Pandas and Spark. If you need, do it as usual in Pandas, and we will translate in Spark later on.

#### Why are there `null` fields?

Elasticc is the first of its kind, and simulations are still limited. Some of the fields have not been simulated.

#### Why the schemas between elasticc_test0.parquet and elasticc_test1.parquet are slightly different?

The Elasticc schema is still evolving as we provide feedback. From time to time, you will see a schema migration.

## Difference with a full broker version

The broker is using Apache Spark to distribute the load on several machines, and process chunks of alerts in parallel. The syntax is very similar to the one described here. One of the main difference is that machines do not have access to a shared local storage, hence any IO to be read/written (configuration files if need be, trained models, ...) must be minimised or distributed beforehand.
