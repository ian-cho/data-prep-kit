# NOOP Transform 
Please see the set of
[transform project conventions](../../README.md#transform-project-conventions)
for details on general project conventions, transform configuration,
testing and IDE set up.

## Summary 
This transform serves as a template for transform writers as it does
not perform any transformations on the input (i.e., a no-operation transform).
As such, it simply copies the input parquet files to the output directory.
It shows the basics of creating a simple 1:1 table transform.
It also implements a single configuration value to show how configuration
of the transform is implemented.

## Output Format
The noop transform simply copies the input, so the output format is the same as the input.

| Output column name | Data type | Description |
|--------------------|-|-|
| same as input      | same as input |same as input |
| ...        | ... | ... | 

## Configuration and command line Options
The transform can be initialized with the following parameters
found in [NOOPTransform](dpk_noop/transform.py) 

| Parameter        | Default | Description                                                                                                                                                 |
|------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `noop_sleep_sec` | 1       | Number of seconds to sleep while inside the transform() method.  This may be useful to simulate transform timeings and as a way to limit I/O bandwidth use. | 
| `noop_pwd`       | None    | specifies a dummy password not included in metadata. Provided as an example of metadata that we want to not include in logging. | 

The set of dictionary keys can be found in [NOOPTransform](dpk_noop/transform.py).

## Usage

### Launched Command Line Options 
When invoking the CLI, the parameters are set using the parameter names from the above table.  
For example, 
```shell
python -m dpk_noop/transform_python --noop_sleep_sec 10 ...
```

### Running the samples
To run the samples, use the following `make` targets

* `run-cli-sample` - runs dpk_noop/transform_python.py using command line args

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
[running images quickstart](../../../doc/quick-start/run-transform-image.md),
substituting the name of this transform image and runtime as appropriate.
