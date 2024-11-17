REPOROOT=../../..
# Use make help, to see the available rules
include $(REPOROOT)/transforms/.make.cicd.targets

#
# This is intended to be included across the Makefiles provided within
# a given transform's directory tree,  so must use compatible syntax.
#
################################################################################
# This defines the name of the transform and is used to match against
# expected files and is used to define the transform's image name. 
TRANSFORM_NAME=$(shell basename `pwd`)

# Used as entry point: 
# python -m dpk_html2parquet.ray.transform --help
# or
# python -m dpk_html2parquet.transform_python --help
TRANSFORM_RUNTIME_SRC_FILE=-m dpk_$(TRANSFORM_NAME).ray.transform

################################################################################
# This defines the transforms' version number as would be used
# when publishing the wheel.  In general, only the micro version
# number should be advanced relative to the DPK_VERSION. 
#
# If you change the versions numbers, be sure to run "make set-versions" to 
# update version numbers across the transform (e.g., pyproject.toml).
#TRANSFORM_VERSION=$(DPK_VERSION)

test-image-default:: image .transforms.test-image-help .transforms.clean


.PHONY: workflow-vent
workflow-venv:
#	if [ -e kfp_ray ]; then                 \
#	    $(MAKE) -C kfp_ray workflow-venv;   \
#	fi

.PHONY: workflow-test
workflow-test:
#	if [ -e kfp_ray ]; then                 \
#	    $(MAKE) -C kfp_ray workflow-test;   \
#	fi

.PHONY: workflow-upload
workflow-upload:
#	if [ -e kfp_ray ]; then                 \
#	    $(MAKE) -C kfp_ray workflow-upload; \
#	fi

.PHONY: workflow-build
workflow-build:
#	if [ -e kfp_ray ]; then                 \
#	    $(MAKE) -C  kfp_ray workflow-build; \
#	fi


