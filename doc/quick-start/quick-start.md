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
pip3 'install data-prep-toolkit-transforms[ray,all]'
```
the command above install the complete library with all the tansforms. In certain situations, it may be desirable to install a specific transform with or without the ray runtime. In that case, the command can specify the name of the transform in the \[extra\] value such as:

To install the lang_id transform, use the following command:

```shell
pip3 install 'data-prep-toolit-tranforms[tng_id]' 
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

* Notebooks (to do- help from Shahrokh)
    * Links to the simple transform notebook in the example folder
    * Guide the users to the individual transforms notebook (explain how to get those using git clone)

* Command line  
    * [Using a docker image](run-transform-image.md) - runs a transform in a docker transform image 
    * [Using a virtual environment](run-transform-venv.md) - runs a transform on the local host 
    
## Creating transforms

* [Tutorial](xxxx.md) - shows how to use the library to add a new transform.

