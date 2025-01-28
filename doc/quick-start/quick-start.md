# Quick Start for Data Prep Kit 
Here we provided short examples of various uses of the Data Prep Kit. Most users who want to jump right in can use standard pip install to deploy the data-prep-kit and the python or ray transforms to their virtual python environment. 

When setting up a __virtual environment__ it is recommended to use __python3.11__ as in the example below using conda. 

## Create a Virtual Environment <a name = "conda"></a>
**setup a virtual environment using conda**

```shell
conda create -n data-prep-kit-1 -y python=3.11
```

**Linux system only: Install the gcc/g++ that is required while building fastext:**
If you are using a linux system, install gcc using the below commands, as it will be required to compile and install [fasttext](https://fasttext.cc/) currently used by some of the transforms.


```shell
conda install gcc_linux-64
conda install gxx_linux-64
```

**activate the new conda environment**

```shell
conda activate data-prep-kit-1
```

make sure env is switched to data-prep-kit-1 and Check python version.

```shell
python --version
The command above should say: 3.11
```

**install data prep toolkit**

```shell
pip3 install 'data-prep-toolkit-transforms[ray,all]'
```
the command above install the complete library with all the tansforms. In certain situations, it may be desirable to install a specific transform with or without the ray runtime. In that case, the command can specify the name of the transform in the \[extra\] value such as:

To install the lang_id transform, use the following command:

```shell
pip3 install 'data-prep-toolit-tranforms[lang_id]' 
```

to install the lang_id transform with the ray runtime, use the following command:

```shell
pip3 install 'data-prep-toolit-tranforms[ray,lang_id]' 
```



## Setting up Jupyter lab for local experimentation with transform notebooks <a name = "jupyter"></a>

```bash
pip install jupyterlab ipykernel ipywidgets
python -m ipykernel install --user --name=data-prep-kit --display-name "dataprepkit"
```



## Running transforms 

* Notebooks
    * There is a [simple notebook](../../examples/notebooks/Run_your_first_transform_colab.ipynb) for running a single transform that can be run from either Google Colab or the local environment by downloading the file.  
    * In most indidividual transform folders, we have included one (Python), two (Python and Ray), or three (Python, Ray and Spark) notebooks for running that transform. In order to run all these notebooks in the local environment, we clone the repo as: 
    ```bash
    git clone git@github.com:IBM/data-prep-kit.git 
    ```
    Then we go to an indvidual transformer folder, where we find the corresponding notebooks. As an example:

    ```bash
    cd data-prep-kit/transforms/universal/fdedup
    make venv
    source venv/bin/activate 
    pip install jupyterlab
    jupyter lab
    ```
    You can now run the [Python version](../../transforms/universal/fdedup/fdedup_python.ipynb), [Ray version](../../transforms/universal/fdedup/fdedup_ray.ipynb) or [Spark version](../../transforms/universal/fdedup/fdedup_spark.ipynb) of the three notebooks for this transform. 


* Command line  
    * [Using a docker image](run-transform-image.md) - runs a transform in a docker transform image 
    * [Using a virtual environment](run-transform-venv.md) - runs a transform on the local host 

## Running transforms on Windows

We have tested the latest release of Date Prep Kit  on Windows, which supports many of the transforms, but not all. To try DPK on Windows, clone the repo and use  the Anaconda Navigator to launch a Notebook Server on the local machine. Create a conda environment for testing and activate it. 
The runtime platform we have tested was as follows:

* Python 3.12.7
* Windows-11-10.0.22631-SP0
* 3.12.7 | packaged by Anaconda, Inc. | (main, Oct 4 2024, 13:17:27) [MSC v.1929 64 bit (AMD64)]

All transforms use `pip install` of their respective modules. For example,
when testing the `doc_chunk` transform with the python runtime, the following command is used:
```bash
pip install --user data-prep-toolkit-transforms[doc_chunck]
```
When testing the `doc_chunk` transform with the ray runtime, the following command is used:
```bash
pip install --user data-prep-tookit-transforms[ray,doc_chunk]
```

All tests use the Notebooks provided by the transform developers in the  corresponding transform folder. For example, for `doc_chunk`, we use this [Notebook](../../transforms/language/doc_chunk/doc_chunk-python.ipynb).

Notebooks for the following language/universal transforms have been tested and shown to work on Windows:

    doc_chunk
    doc_quality
    html2parqet
    pii_redactor
    text_encoder
    doc_id
    ededup
    filter
    hap
    profiler
    resize
    tokenization

If you want to try Notebooks that run many of the transforms in sequence, here is a sample [Notebook](../../transforms/transforms-1.0-lang-Windows.ipynb) for the python runtime and another sample [Notebook](../../transforms/transforms-1.0-lang-Windows.ipynb) for the ray runtime. 
    
## Creating transforms

* [Tutorial](contribute-your-own-transform.md) - shows how to use the library to add a new transform.

