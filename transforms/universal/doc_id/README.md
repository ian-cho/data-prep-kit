# Document ID Python Annotator

The Document ID transforms adds a document identification (unique integers and content hashes), which later can be 
used in de-duplication operations, per the set of 
[transform project conventions](../../README.md#transform-project-conventions)
the following runtimes are available:

## Summary

This transform annotates documents with document "ids".
It supports the following transformations of the original data:
* Adding document hash: this enables the addition of a document hash-based id to the data.
  The hash is calculated with `hashlib.sha256(doc.encode("utf-8")).hexdigest()`.
  To enable this annotation, set `hash_column` to the name of the column,
  where you want to store it.
* Adding integer document id: this allows the addition of an integer document id to the data that
  is unique across all rows in all tables provided to the `transform()` method.
  To enable this annotation, set `int_id_column` to the name of the column, where you want
  to store it.

Document IDs are generally useful for tracking annotations to specific documents. Additionally
[fuzzy deduping](../fdedup) relies on integer IDs to be present. If your dataset does not have
document ID column(s), you can use this transform to create ones.


## Configuration and command line Options

The set of dictionary keys defined in [DocIDTransform](src/doc_id_transform_ray.py)
configuration for values are as follows:

* _doc_column_ - specifies name of the column containing the document (required for ID generation)
* _hash_column_ - specifies name of the column created to hold the string document id, if None, id is not generated
* _int_id_column_ - specifies name of the column created to hold the integer document id, if None, id is not generated
* _start_id_ - an id from which ID generator starts () 

At least one of _hash_column_ or _int_id_column_ must be specified.

## Running

### Launched Command Line Options 
When running the transform with the Ray launcher (i.e. TransformLauncher),
the following command line arguments are available in addition to 
[the options provided by the ray launcher](../../../../data-processing-lib/doc/ray-launcher-options.md).
```
  --doc_id_doc_column DOC_ID_DOC_COLUMN
                        doc column name
  --doc_id_hash_column DOC_ID_HASH_COLUMN
                        Compute document hash and place in the given named column
  --doc_id_int_column DOC_ID_INT_COLUMN
                        Compute unique integer id and place in the given named column
  --doc_id_start_id DOC_ID_START_ID
                        starting integer id
```
These correspond to the configuration keys described above.


To use the transform image to transform your data, please refer to the 
[running images quickstart](../../../../doc/quick-start/run-transform-image.md),
substituting the name of this transform image and runtime as appropriate.


### Running as spark-based application
```
(venv) cma:src$ python doc_id_local.py
18:32:13 INFO - data factory data_ is using local data access: input_folder - /home/cma/de/data-prep-kit/transforms/universal/doc_id/spark/test-data/input output_folder - /home/cma/de/data-prep-kit/transforms/universal/doc_id/spark/output at "/home/cma/de/data-prep-kit/data-processing-lib/ray/src/data_processing/data_access/data_access_factory.py:185"
18:32:13 INFO - data factory data_ max_files -1, n_sample -1 at "/home/cma/de/data-prep-kit/data-processing-lib/ray/src/data_processing/data_access/data_access_factory.py:201"
18:32:13 INFO - data factory data_ Not using data sets, checkpointing False, max files -1, random samples -1, files to use ['.parquet'] at "/home/cma/de/data-prep-kit/data-processing-lib/ray/src/data_processing/data_access/data_access_factory.py:214"
18:32:13 INFO - pipeline id pipeline_id at "/home/cma/de/data-prep-kit/data-processing-lib/ray/src/data_processing/runtime/execution_configuration.py:80"
18:32:13 INFO - code location {'github': 'github', 'commit_hash': '12345', 'path': 'path'} at "/home/cma/de/data-prep-kit/data-processing-lib/ray/src/data_processing/runtime/execution_configuration.py:83"
18:32:13 INFO - spark execution config : {'spark_local_config_filepath': '/home/cma/de/data-prep-kit/transforms/universal/doc_id/spark/config/spark_profile_local.yml', 'spark_kube_config_filepath': 'config/spark_profile_kube.yml'} at "/home/cma/de/data-prep-kit/data-processing-lib/spark/src/data_processing_spark/runtime/spark/spark_execution_config.py:42"
24/05/26 18:32:14 WARN Utils: Your hostname, li-7aed0a4c-2d51-11b2-a85c-dfad31db696b.ibm.com resolves to a loopback address: 127.0.0.1; using 192.168.1.223 instead (on interface wlp0s20f3)
24/05/26 18:32:14 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
24/05/26 18:32:15 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
18:32:17 INFO - files = ['/home/cma/de/data-prep-kit/transforms/universal/doc_id/spark/test-data/input/test_doc_id_1.parquet', '/home/cma/de/data-prep-kit/transforms/universal/doc_id/spark/test-data/input/test_doc_id_2.parquet'] at "/home/cma/de/data-prep-kit/data-processing-lib/spark/src/data_processing_spark/runtime/spark/spark_launcher.py:184"
24/05/26 18:32:23 WARN SparkStringUtils: Truncated the string representation of a plan since it was too large. This behavior can be adjusted by setting 'spark.sql.debug.maxToStringFields'.
```

### Doc ID Statistics
The metadata generated by the Spark `doc_id` transform contains the following statistics:
  * `total_docs_count`, `total_columns_count`: total number of documents (rows), and columns in the input table, before the `doc_id` transform ran    
  * `docs_after_doc_id`, `columns_after_doc_id`: total number of documents (rows), and columns in the output table, after the `doc_id` transform ran  

### Transforming data using the transform image

To use the transform image to transform your data, please refer to the 
[running images quickstart](../../../../doc/quick-start/run-transform-image.md),
substituting the name of this transform image and runtime as appropriate.

