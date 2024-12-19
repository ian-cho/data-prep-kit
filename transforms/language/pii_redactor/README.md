

# PII Redactor Transform

This transform redacts Personally Identifiable Information (PII) from the input data.

The transform leverages the [Microsoft Presidio SDK](https://microsoft.github.io/presidio/) for PII detection and uses the Flair recognizer for entity recognition.


## Contributors

- Sowmya.L.R (lrsowmya@gmail.com)


### Supported Entities

The transform detects the following PII entities by default:
- **PERSON**: Names of individuals
- **EMAIL_ADDRESS**: Email addresses
- **ORGANIZATION**: Names of organizations
- **DATE_TIME**: Dates and times
- **PHONE_NUMBER**: Phone number
- **CREDIT_CARD**: Credit card numbers

You can configure the entities to detect by passing the required entities as argument param ( **--pii_redactor_entities** ).
To know more about different entity types supported - [Entities](https://microsoft.github.io/presidio/supported_entities/)

### Redaction Techniques

Two redaction techniques are supported:
- **replace**: Replaces detected PII with a placeholder (default)
- **redact**: Removes the detected PII from the text

You can choose the redaction technique by passing it as an argument parameter (**--pii_redactor_operator**).

## Input and Output

### Input

The input data should be a `py.Table` with a column containing the text where PII detection and redaction will be applied. By default, this column is named `contents`.

**Example Input Table Structure:** Table 1: Sample input to the pii redactor transform

| contents            | doc_id |
|---------------------|--------|
| My name is John Doe | doc001 |
| I work at apple     | doc002 |


### Output

The output table will include the original columns plus an additional column `new_contents` which is configurable with redacted text and `detected_pii` 
column consisting the type of PII entities detected in that document for replace operator.

**Example Output Table Structure for replace operator:**

| contents            | doc_id | new_contents             | detected_pii     |
|---------------------|--------|--------------------------|------------------|
| My name is John Doe | doc001 | My name is `<PERSON>`    | `[PERSON]`       |
| I work at apple     | doc002 | I work at `<ORGANIZATION>` | `[ORGANIZATION]` |

When `redact` operator is chosen the output will look like below
 
**Example Output Table Structure for redact operator**

| contents            | doc_id | new_contents             | detected_pii     |
|---------------------|--------|--------------------------|------------------|
| My name is John Doe | doc001 | My name is  | `[PERSON]`       |
| I work at apple     | doc002 | I work at | `[ORGANIZATION]` |

## Running

### Launched Command Line Options 
The following command line arguments are available in addition to 
the options provided by 
the [python launcher](../../../../data-processing-lib/doc/python-launcher-options.md).

```
  --pii_redactor_entities PII_ENTITIES
                        list of PII entities to be captured for example: ["PERSON", "EMAIL"]
  --pii_redactor_operator REDACTOR_OPERATOR
                        Two redaction techniques are supported - replace(default), redact 
  --pii_redactor_transformed_contents PII_TRANSFORMED_CONTENT_COLUMN_NAME
                        Mention the column name in which transformed contents will be added. This is required argument. 
  --pii_redactor_score_threshold SCORE_THRESHOLD
                        The score_threshold is a parameter that sets the minimum confidence score required for an entity to be considered a match.
                        Provide a value above 0.6
```# PII Redactor Ray Transform 
Please see the set of
[transform project conventions](../../../README.md#transform-project-conventions)
for details on general project conventions, transform configuration,
testing and IDE set up.

## Summary 
This project wraps the [pii redactor transform](../python) with a Ray runtime.

## Configuration and command line Options

PII redactor configuration and command line options are the same as for the [base python](../python) transform and in additional it also supports other options refer [pii redactor transform](../python/README.md) . 

## Running

### Launched Command Line Options 
In addition to those available to the transform as defined in [here](../python/README.md),
the set of 
[ray launcher](../../../../data-processing-lib/doc/ray-launcher-options.md) are available.

### Running the samples
To run the samples, use the following `make` targets

* `run-cli-sample` - runs src/pii_redactor_transform.py using command line args
* `run-local-sample` - runs src/pii_redactor_local_ray.py
* `run-s3-sample` - runs src/pii_redactor_s3_ray.py
    * Requires prior installation of minio, depending on your platform (e.g., from [here](https://min.io/docs/minio/macos/index.html)
     and [here](https://min.io/docs/minio/linux/index.html) 
     and invocation of `make minio-start` to load data into local minio for S3 access.

These targets will activate the virtual environment and set up any configuration needed.
Use the `-n` option of `make` to see the detail of what is done to run the sample.

For example, 
```shell
make run-cli-sample
...
```
Then 
```shell
ls output
```
To see results of the transform.

### Transforming data using the transform image

To use the transform image to transform your data, please refer to the 
[running images quickstart](../../../../doc/quick-start/run-transform-image.md),
substituting the name of this transform image and runtime as appropriate.
