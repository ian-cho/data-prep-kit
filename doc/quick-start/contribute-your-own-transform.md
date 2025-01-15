<h1 align="center">Data Prep Kit</h1>

<div align="center"> 

<?  [![Status](https://img.shields.io/badge/status-active-success.svg)]() ?>
<?  [![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/IBM/data-prep-kit/issues) ?>
<?  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/IBM/data-prep-kit/pulls) ?>
</div> 

In this tutorial we take the developers through the steps for contributing a new transform to the DPK. We will cover the steps for cloning the repo, writing the code and using the capabilities offered by the framework to accelerate development and testing. [Part 2 of the tutorial](tutorial-part-2) is found [here](tutorial-part-2) and covers how to enable Ray and KFP


[This part of the tutorial](#part1) covers:
1. How to clone the repo and setup the file structure for the transform
1. Write the code by implementing the transform specific functionality 
1. Use the framework capabilities to accelerate development, testing and deployment

For this tutorial, we will follow a suggested flow. Developers are welcome to explore on their own to achieve the same results. Except for the transform name and module name, developers have a lot of freedom on how they choose their class name, file names and file structure. that said, following the convention listed below would make it easier for the community to chime-in to help with debugging and maintaining the code base.

The new transform will annotate each document in the data set with a digest value that is calculated using a SHA256, SHA512 or MD5 hash function. The objective is to show how we can use a user defined function to build a transform and how developers can specify the configuration parameters for the transform. 

- For the purpose of this tutorial, our transform will be called **digest** and the python named module is **dpk_digest**. Developers have some freedom in how they name their modules to the extent that the choosen name does not collide with an existing transform name.

- The user defined function for is tutorial is a simple annotator that uses the python hashlib package: 
 ```  
      hash = hashlib.new(self.algorithm)
      digest=hash.update(elt.encode('utf-8'))
```
- The transform defines a single configuration parameter **digest_algortihm** that specifies the name of the digest algorithm to use and selected from a predefined list that includes **\['SHA256', 'SHA512' or 'MD5'\]**


## 📝 List of Steps to follow in this tutorial

1. [Create folder structure](#setup)
1. [Implement DigestTransform](#DigestTransform)- core functionality for annotating documents
1. [Implement DigestConfiguration](#DigestConfiguration) - Configure and validate transform parameters
1. [Implement DigestRuntime](#DigestRuntime) - wires the transform to the runtime so it is correctly invoked
1. [Integrate with CI/CD](#cicd) - automate testing, integration and packaging
1. [Develop Unit Test](#UnitTest) - get test data and write Unit Test

## Step 1: Create folder structure <a name=setup></a>

**fork and clone the repo locally**

This can be done from the github web browser or using the gh CLI as below:

Example using CLI (https://github.com/cli/cli)

```shell
gh auth login --skip-ssh-key
gh repo fork git@github.com:IBM/data-prep-kit.git --default-branch-only 
```

ASSUMPTION: We assume that the developer had already installed git cli and setup her/his public key as part of the developer’s profile.  https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account



**Create placeholder for new transform**

The DPK transforms are currently organized in three categories for Code (Transforms that are used specifically for programming languages), 
Language(Transforms that are used specifically for natural languages) and Universal (Transforms that are used for both language and code). it is safe to assume that our transform can be used for calculating the hash for natural languages text and programming languages alike and we will add it to the universal subfolder. We will also create the python module and a skeleton of the code including a notebook and readme.md file. A typical implementation would have the following file structure.

```
data-prep-kit
│
└───transforms
│   |
│   └───universal
│       │
│       └───digest
│            |
│            └───dpk_digest
│            |      │
│            |      │ __init__.py
│            |      │ transform.py
│            |      | runtime.py
│            │
│            └───test
│            │    |
│            │    |test_digest.py
│            │
│            └───test-data
│            │     |
│            |     └───input
│            |     |     │
│            |     |     │ testfile.parquet
│            |     |     
│            |     └───expected
│            |          │
│            |          │ testfile.parquet
│            |          │ markdown.json
│            | 
│            | digest.ipynb
│            | README.md
│            | Makefile
```

## Step 2: Implemnt DigestTransform <a name="DigestTransform></a>

**dpk_digest/transform.py** 

This file implements the key logic for the transform. It receives a pyarrow table with a list of documents in the data set and append a new column with a digest value. We will described the contents of the file in 2 sections:

- The first portion of the file includes the language for the license used to distribute and use the code and a set of import statements for the library modules that will be needed for invoking this transfroms


```python
# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

from typing import Any

import pyarrow as pa
import hashlib
from data_processing.transform import AbstractTableTransform
from data_processing.utils import  TransformUtils
```

**AbstractTableTransform** defines a template for the APIs that will be invoked by the runtime to trigger the transform.

**TransformUtils** provides a number of shortcuts commonly used by transfdorms for data conversions, table manipulations, etc.



- The remaining section of the file implements the Transform method that will be called by the framework when new data is available for annotation. 


```python
class DigestTransform(AbstractTableTransform):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)

        ## If the algorithm is not specified, use sha256
        self.algorithm = config.get('digest_algorithm', "sha256")

    def transform(self, 
                  table: pa.Table, 
                  file_name: str = None) -> tuple[list[pa.Table], dict[str, Any]]:
            
        ## calculate digest for the content column
        tf_digest = []
        for elt in table['contents'].to_pylist():
            h = hashlib.new(self.algorithm)
            h.update(elt.encode('utf-8'))
            tf_digest.append(h.hexdigest())

        ## digest as a new column to the existing table
        table = TransformUtils.add_column(table=table, 
                                           name='digest', 
                                           content=tf_digest)
        
        metadata = {"nrows": len(table)}
        return [table], metadata
```

**\__init__()** receives a dictionary that represents the different configuration parameters specified by the user. In our case, the only parameter that we use is the string value representing the name of digest. if the user does not specify a digest, we will use default value fo "sha256"

**transform()** The transform method implements the callback that the runtime uses when it identifies new data to be processed by this transform. it
Receives a pyarrow table, calculate the digest for each row in the table and append the digest as a new column to the same table


**dpk_digest/__init__.py**

```python
# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################
from .transform import *
```

## Step 3: Implement DigestConfiguration <a name="DigestConfiguration"></a>

**dpk_digest/runtime.py** 

This file implements a serie of user defined validation steps that must be executed prior to invoking the transform. 

- The first portion of the file includes the language for the license used to distribute and use the code and a set of import statements for the library modules that will be needed to run validation


```python
# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
import sys
from dpk_digest.transform import DigestTransform
from data_processing.transform import TransformConfiguration
from data_processing.utils import ParamsUtils, CLIArgumentProvider, get_logger
from argparse import ArgumentParser, Namespace
from data_processing.runtime.pure_python import PythonTransformLauncher
from data_processing.runtime.pure_python.runtime_configuration import (
    PythonTransformRuntimeConfiguration,)

logger = get_logger(__name__)
```

- Some of the key classes indetified in this import list include:
* **TransformConfiguration** Defines a template for the method that the DigestConfiguration implements
* **ParamsUtils, CLIArgumentProvider** Utilities method provided by the framework for parsing the transform configuration as defined by the user of the transform
* **ArgumentParser, Namespace** Standard python methods for parsing command line arguments and standard argument types
* **PythonTransformLauncher, PythonTransformRuntimeConfiguration** Implemented by the framework for orchestration the execution of the transform



- The next section of the file defines the implementation of the DigestConfiguration that will provide guidance to the user on how to configure the transform and also validate the associated configuration value

```Python
logger = get_logger(__name__)

class DigestConfiguration(TransformConfiguration):
    def __init__(self):
        ## Identify the transform implementation that this configuration relates to
        super().__init__(name='digest', transform_class=DigestTransform,)

    def add_input_params(self, parser: ArgumentParser) -> None:
        ## Define how varius configuration parameters should be parsed
        parser.add_argument(
            "--digest_algorithm",
            type=str,
            help="Specify the hash algorithm to use for calculating the digest value.",
        )

    def apply_input_params(self, args: Namespace) -> bool:
        ## Validate each of the configuration parameters received from the user
        captured = CLIArgumentProvider.capture_parameters(args, 'digest', True)
        self.params = self.params | captured
        if captured.get('digest_algorithm') not in ['sha256','SHA512', 'MD5']:
            logger.error(f"Parameter digest_algorithm cannot be other than ['sha256','SHA512', 'MD5']. You specified {args.digest_algorithm}")
            return False
        return True
```

## Step 4: Implement DigestRuntime <a name="DigestRuntime"></a>

**dpk_digest/runtime.py** 

- The next section of the file wires the transform into the the python orchestrator and allows the framework to instantiate, configure and invoke the transfrom

```Python
class DigestRuntime(PythonTransformRuntimeConfiguration):

    def __init__(self):
        super().__init__(transform_config=DigestConfiguration())

if __name__ == "__main__":
    launcher = PythonTransformLauncher(DigestRuntime())
    launcher.launch()
```



- The last section of the file defines a wrapper that simplifies how the transform is invoked and hides some of the complexity that is inherit to the runtime orchestrator

```Python
class Digest:
    def __init__(self, **kwargs):
        self.params = {}
        for key in kwargs:
            self.params[key] = kwargs[key]
        # if input_folder and output_folder are specified, then assume it is represent data_local_config
        try:
            local_conf = {k: self.params[k] for k in ("input_folder", "output_folder")}
            self.params["data_local_config"] = ParamsUtils.convert_to_ast(local_conf)
            del self.params["input_folder"]
            del self.params["output_folder"]
        except:
            pass

    def transform(self):
        sys.argv = ParamsUtils.dict_to_req(d=(self.params))
        launcher = PythonTransformLauncher(DigestRuntime())
        return_code = launcher.launch()
        return return_code
```


## Step 5: Develop Unit Test <a name="UnitTest"></a>

- For our testing, we will need some initial data as input to our transform. We will copy it from another transform test folder.

```shell
cd data-prep-kit/transforms/universal/digest
mkdir -p test-data/input
cp ../../language/doc_chunk/test-data/expected/*.parquet test-data/input
```


- Create a virtual environment and run the transform against the input data to produce the expected output data. This will be used by the CI/CD to verify that the logic of the transform always produces the same output for a give input.

```shell
cd data-prep-kit/transforms/universal/digest
python -m venv venv && source venv/bin/activate
pip intall data-prep-toolkit
rm -fr test-data/expected/*
python -m dpk_digest.runtime --digest_algorithm sha256 --data_local_config "{ 'input_folder' : 'test-data/input', 'output_folder' : 'expected’}” 
```
If the test code runs properly, we should see 2 new files creted in the test-data/expected folder:
test-data/expected/test1.parquet
test-data/expected/metadata.json

- Developers have some freedom in designing their unit tests. in this section we should how developers can use the test fixture defined in the framework to rapidly create unit tests

**test/test_digest.py

```python
# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import os

from data_processing.test_support.launch.transform_test import (
    AbstractTransformLauncherTest,
)
from data_processing.runtime import PythonTransformLauncher
from dpk_digest.runtime import DigestRuntime


class TestDigestTransform(AbstractTransformLauncherTest):

    def get_test_transform_fixtures(self) -> list[tuple]:
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                               "../test-data"))
        fixtures = []
        transform_config = {
            "run_locally": True,
            "digest_algorithm": "sha256", 
        }
        launcher = TransformLauncher(DigestRuntime())
        fixtures.append((launcher, transform_config, 
                         basedir + "/input", 
                         basedir + "/expected"))
        return fixtures
```

## Step 5: Integrate with CI/CD <a name="cicd"></a>

- The repo implements a rich set of functionality for setting up the environment, running unit tests, publish the transforms to pypi, building the transforms as part of a docker image and running it with Kubeflow. For the prupose of this section, we will explore only a portion of the capabilities for support this initial phase of the implementation

we will first copy the Makefile template from the parent folder
```shell
cd data-prep-kit/transforms/universal/digest
cp ../../Makefile.transform.template Makefile
```










