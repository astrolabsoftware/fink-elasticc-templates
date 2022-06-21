# Fink Elasticc templates

This repo hosts necessary files to create and test a science module using Elasticc data. To start, useful links:

- DESC GitHub Elasticc repo: https://github.com/LSSTDESC/elasticc
- DESC Elasticc presentation & data: https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/

## Elasticc alert data

Elasticc alert data is different from the data used by the training. First, the schema is different (renamed fields, less available fields). You can inspect some of the difference [here](https://portal.nersc.gov/cfs/lsst/DESC_TD_PUBLIC/ELASTICC/TRAINING_SAMPLES/A_FORMAT.TXT), and you will find some of the alerts in the folder `data`.

## Processing alert data

For the sake of simplicity, we will abstract all the technical details of Fink (e.g. no use of Apache Spark), and keep only what is needed to add values to alerts. A science module in Fink is simply a Python routine that takes as input a set of alert fields, and output a new field based on the user logic.

In practice, the science module operates on batches of alerts, materialised as Pandas Series for each alert field. We provide a basic [example](mymodule) to familiarise with the structure of a science module. It contains two parts:
1. `processor.py`: includes the routine that is called by the broker.
2. `utils.py`: anything else required by the science module.

To test it, just run:

```python
python test_module.py
```

## Going further

This example is very simple, and in reality the processing can be quite complex. You can have a look at what is currently done in Fink with ZTF data on production: https://github.com/astrolabsoftware/fink-science.

## Difference with a full broker version

The broker is using Apache Spark to distribute the load on several machines, and process chunks in parallel. The syntax is very similar to the one described here, but the main difference is that machines do not have access to a shared local storage, hence any IO (configuration files if need be, trained models, ...) must be distributed beforehand.
