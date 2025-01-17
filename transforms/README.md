# Transforms

The transformation framework is designed to operate on arbitrary input data,
usually tabular data read from  
[parquet](https://arrow.apache.org/docs/python/parquet.html) files
as [pyarrow tables](https://arrow.apache.org/docs/python/index.html), but also any binary data.
For details on some of the key classes, listed here,
* AbstractBinaryTransform
* AbstractTableTransform
* TransformConfiguration
* DefaultTransformRuntime

please refer to 
[DPK core library documentation](../data-processing-lib/doc/overview.md).

## Importing Transforms 
These are generally binary transforms that take in one format and convert
to another usually, a parquet formatted PyArrow table.

## Annotating Transforms
Annotating transforms examine 1 or more columns of data, typically a _content_ column containing a document
to be annotated.  The content is often spoken/text or programming language, generally to build
a large language model (LLM).  Examples of annotation might include:

* Language identification - an additional string column is added to identify the language of the document content.
* Document quality - an additional float column is added to associated a quality score with the document.
* Block listing - an addtional boolean column is added that indicates if the content source url
  (in one of the columns) is from a blocked domain.

## Filtering Transforms
Filtering transforms modify the rows and/or columns, usually based on associated column values.  
For example,

* Language selection - remove rows that do not match the desired language
* Document quality threshold - remove rows that do not meet a minimum document quality value.
* Block listing - remove rows that have been flagged as having been sourced from undesirable domains.

# Transform Organization
This directory hierarchy of transforms is organized as follows:

* `universal` - transforms applicable across code and language model data include
* `language` - spoken language model specific transforms
* `code` - programming language specific transforms.

Each of the `universal`, `language` and `code`  directories contains a directory for a specific transform.
Each transform is expected to be a standalone entity that can be run locally on small data sets
or runs at scale to process terabytes of data. 
They each run in their own virtual environments.

## Transform Project Conventions

For transform projects it is encourraged to use a common set of conventions 
including code layout, build, documentation and IDE recommendations.  
For a transformed named `xyz`, it is expected to have its project located under one of

`transforms/code/xyz`   
`transforms/language/xyz`, OR   
`transforms/universal/xyz`.

Additional conventions follow.

### Makefile
The Makefile is the primary entry point for performing most CLI-based functions
for the build and management of a transform, including 
[git CI/CD workflows](../.github/workflows).
This includes 

* creating the virtual environment
* testing
* building docker images
* cleanup
 
Use `make help` in any directory with a Makefile to see the available targets.
Each Makefile generally requires the following macro definitions:

* REPOROOT - specifies a relative path to the local directory
that is the root of the repository.
* TRANSFORM_NAME - specifies the short name of the transform
that will be used in creating pypi artifacts and docker images.
This is set by default, for the examples above, `xyz` based on the directory name.

### File/Directory Organization

Transforms support one or more _runtimes_ (e.,g python, Ray, Spark, KFP, etc).
Each runtime implementation is placed in a sub-directory under the transform's
primary directory, for example:

A transform only need implement the python runtime, and the others generally build on this.

All runtime projects are structured as a _standard_ python project with the following:

* `dpk_xyz`  - directory contains all python implementation code (see below)
* `test` - directory contains test code (see below)
* `test-data` - directory containing data used in the tests
* `requirements-.txt` - defines requirements specific to the transform. 
* `Makefile`- runs most operations, try `make help` to see a list of targets.
* `Dockerfile.python` to build the transform and python runtime into a docker image 
* `Dockerfile.ray` to build the transform and ray runtime into a docker image 
* `Dockerfile.spark` to build the transform and spark runtime into a docker image 
* `output` - temporary directory capturing any test/local run output.  Ignored by .gitignore.
* `kfp_ray` - directory enabling the creation of a KFP pipeline that runs the transform.

Finally, the command `make conventions` run from within a runtime
directory will examine the runtime project structure and make recommendations.

#### dpk_\<xyz> Directory Organization
The `dpk_xyz` directory, for a transform named `xyz`, 
contains the core transform implementation and
its configuration, along with the code for the supported runtimes
in sub-modules named according to the runtime.
The following organization and  naming conventions are strongly recommended
and in some cases required for the Makefile to do its work.

* `transform.py` generally contains the core transform implementation: 
    * `XYZTransform` class implementing the transformation
    * `XYXTransformConfiguration` class that defines CLI configuration for the transform
* `transform_python.py` - runs the transform on input using the python runtime
    * `XYZPythonTransformConfiguration` class
  * main() to start the `PythonTransformLauncher` with the above.
* `ray` - contains code to enable the python transform in a Ray runtime.
   * `transform.py` - ray runtime artifacts to enable the transform in the DPK Ray runtime.
       * `XYZRayTransformConfiguration` class
       * main() to start the `RayTransformLauncher` with the above.
* `spark` - contains code to enable the python transform in a Spark runtime.
   * `transform.py` - spark runtime artifacts to enable the transform in the DPK Spark runtime.
       * `XYZSparkTransformConfiguration` class
       * main() to start the `SparkTransformLauncher` with the above. 
* Additional files can be added as necessary in support of the transform.

#### test Directory Organization

The `test` directory contains pytest test sources and is organized as follows:

* `test_xyz.py` - a standalone (non-ray launched) transform test.  This is best for initial debugging.
    * Inherits from an abstract test class so that to test one needs only to provide test data.
* `test_xyz_python.py` - defines the transform tests running in the Python launcher. 
    * Again, inherits from an abstract test class so that to test one needs only to provide test data.
* `test_xyz_ray.py` - defines the transform tests running in the Ray launcher. 
* `test_xyz_spark.py` - defines the transform tests running in the Spark launcher. 
         
Tests are expected to be run from anywhere and so need to use
`__file__` location to create absolute directory paths to the data in the `../test-data` directory.
From the command line, `make test` sets up the virtual environment and PYTHONPATH to include `dpk_xyz`
Do **not** add `sys.path.append(...)` in the test python code.
All test data should be referenced as `../test-data` relative
to `os.path.abspath(os.path.dirname(__file__))`.

### Configuration and command line options
A transform generally accepts a dictionary of configuration to
control its operation.  For example, the size of a table, the location
of a model, etc. These are set either explicitly in dictionaries
(e.g. during testing) or from the command line when run from a runtime launcher.

When specified on the command line, transform `xyz` should use an `xyz_` prefix with
`--xyz_` (dash dash) to define its command line options.
For example, `--xyz_some_cfg somevalue` sets
the value for the `xyz_some_cfg` configuration key value to `somevalue`.
To avoid potential collisions with options for the runtime launcher, 
Data Access Factory and others,
it is strongly encouraged to not use single dash options with a single
or small number of characters (e.g. -n).

### Docker Images
Generally, to build the docker images, one uses the Makefile with the following make targets

* `image-python` - uses `Dockerfile.python` to build the python runtime image for the transform.
* `image-ray` - uses `Dockerfile.ray` to build the python runtime image for the transform.
* `image-spark` - uses `Dockerfile.spark` to build the python runtime image for the transform.
* `image` - build all images.

Similarly, to test the docker images, 

* `test-image-python` - runs a simple --help run of the transform in the python image. 
* `test-image-ray` - runs a simple --help run of the transform in the Ray image. 
* `test-image-spark` - runs a simple --help run of the transform in the Spark image. 

### IDE Setup
When running in an IDE, such as PyCharm or VS Code, the following are generally required:

* From the command line, build the venv using `make venv`.
* In the IDE
    * Set your project/run configuration to use the venv/bin/python as your runtime virtual environment.
        * In PyCharm, this can be done through the PyCharm->Settings->Project...->Python Interpreter page
        * In VS Code, click on the current Python Interpreter in the bottom right corner and make sure that the Interpreter path is venv/bin/python
    * Mark the `dpk_xyz` directory as a _source root_ so that it is included in your PYTHONPATH when running .py files in the IDE
        * In Pycharm this can be done by selecting the `dpk_xyz` directory, and then selecting `Mark Directory as` -> `Sources Root`
 
