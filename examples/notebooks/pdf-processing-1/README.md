# PDF Processing with Data Prep Kit

Show cases Data Prep Kit capabilities of processing PDFs

## Running the code

The code can be run on either 

1.  Google colab: very easy to run; no local setup needed.
2.  On your local Python environment.  Here is a quick guide.  You can  find instructions for latest version [here](../../../README.md#-getting-started)

```bash
conda create -n data-prep-kit -y python=3.11
conda activate data-prep-kit

# install the following in 'data-prep-kit' environment
pip3 install  'data-prep-toolkit-transforms[ray,all]==1.0.0a4'
pip3 install jupyterlab   ipykernel  ipywidgets

## install custom kernel
## Important: Use this kernel when running example notebooks!
python -m ipykernel install --user --name=data-prep-kit --display-name "dataprepkit"

# start jupyter and run the notebooks with this jupyter
jupyter lab
```

## Intro

This notebook will demonstrate processing PDFs

`PDFs ---> text ---> compute hash ---> dedupe ---> document quality`

[python version](dpk_intro_1_python.ipynb)  &nbsp;   |   &nbsp;  [ray version](dpk_intro_1_ray.ipynb)


## Creating Input PDFs (Optional)

```bash
cd input/solar-system

pandoc earth.md  -o earth.pdf
pandoc earth2.md  -o earth2.pdf
pandoc mars.md  -o mars.pdf
pandoc spam.md  -o spam.pdf
pandoc lorem-ipsum.md  -o lorem-ipsum.pdf
```