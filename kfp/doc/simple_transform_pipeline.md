# Simplest Transform pipeline tutorial

In this example, we implement a pipeline to automate execution of the simple 
[noop transform](../../data-processing-lib/doc/simplest-transform-tutorial.md)

In this tutorial, we will show the following:

* How to write the `noop` transform automation pipeline, leveraging [KFP components](../kfp_ray_components/README.md).
* How to compile a pipeline and deploy it to KFP
* How to execute pipeline and view execution results

Note: the project and the explanation below are based on [KFPv1](https://www.kubeflow.org/docs/components/pipelines/v1/)

Note: For details on using the HugginFace token in a pipeline for relevant transforms, 
please refer to the [HugginFace token](#hf) section.

## 📝 Table of Contents
- [Implementing pipeline](#implementing)
  - [Imports definition](#imports) 
  - [Components definition](#components)
  - [Input parameters definition](#inputs)
  - [Pipeline definition](#pipeline)
  - [Additional configuration](#add_config)
  - [Tolerations and node selector](#tolerations)
- [Compiling a pipeline](#compilation)
- [Deploying a pipeline](#deploying)
- [Executing pipeline and watching execution results](#execution)
- [Clean up the cluster](#cleanup")
  

## Implementing pipeline <a name = "implementing"></a> 

[Overall implementation](../../transforms/universal/noop/kfp_ray/v1/noop_wf.py) roughly contains 5 major sections:

* Imports
* Components definition - definition of the main steps of our pipeline
* Input parameters definition 
* Pipeline wiring - definition of the sequence of invocation (with parameter passing) of participating components
* Additional configuration

### Imports definition <a name = "imports"></a>

```python
import kfp.compiler as compiler
import kfp.components as comp
import kfp.dsl as dsl
import os
from kfp_support.workflow_support.runtime_utils import (
  DEFAULT_KFP_COMPONENT_SPEC_PATH,
  ONE_HOUR_SEC,
  ONE_WEEK_SEC,
  ComponentUtils,
)
from kubernetes import client as k8s_client
```

### Components definition <a name = "components"></a> 

Our pipeline includes 4 steps - compute execution parameters, create Ray cluster, submit and watch Ray job, clean up 
Ray cluster. For each step we have to define a component that will execute them:

```python
    # components
    base_kfp_image = "quay.io/dataprep1/data-prep-kit/kfp-data-processing:latest"
    component_spec_path = os.getenv("KFP_COMPONENT_SPEC_PATH", DEFAULT_KFP_COMPONENT_SPEC_PATH)
    # KFPv1 and KFP2 uses different methods to create a component from a function. KFPv1 uses the
    # `create_component_from_func` function, but it is deprecated by KFPv2 and so has a different import path.
    # KFPv2 recommends using the `@dsl.component` decorator, which doesn't exist in KFPv1. Therefore, here we use
    # this if/else statement and explicitly call the decorator.
    if os.getenv("KFPv2", "0") == "1":
      compute_exec_params_op = dsl.component_decorator.component(
                func=compute_exec_params_func, base_image=base_kfp_image
                )
    else:
      compute_exec_params_op = comp.create_component_from_func(func=compute_exec_params_func, base_image=base_kfp_image)
    # create Ray cluster
    create_ray_op = comp.load_component_from_file(component_spec_path + "createRayClusterComponent.yaml")
    # execute job
    execute_ray_jobs_op = comp.load_component_from_file(component_spec_path + "executeRayJobComponent.yaml")
    # clean up Ray
    cleanup_ray_op = comp.load_component_from_file(component_spec_path + "deleteRayClusterComponent.yaml")
    # Task name is part of the pipeline name, the ray cluster name and the job name in DMF.
    TASK_NAME: str = "noop"
```
Note: here we are using shared components described in this [document](../kfp_ray_components/README.md) for `create_ray_op`, 
`execute_ray_jobs_op` and `cleanup_ray_op`,  while `compute_exec_params_op` component is built inline, because it might
differ significantly. For "simple" pipeline cases we can use the 
[default implementation](../kfp_support_lib/src/kfp_support/workflow_support/runtime_utils/remote_jobs_utils.py),
while, for example for exact dedup, we are using a very [specialized one](../../transforms/universal/ededup/kfp_ray/v2/src/ededup_compute_execution_params.py).

### Input parameters definition <a name = "inputs"></a> 

The input parameters section defines all the parameters required for the pipeline execution:

```python
    # Ray cluster
    ray_name: str = "noop-kfp-ray",  # name of Ray cluster
    ray_run_id_KFPv2: str = "",
    ray_head_options: str = '{"cpu": 1, "memory": 4, \
                 "image": "' + task_image + '" }',
    ray_worker_options: str = '{"replicas": 2, "max_replicas": 2, "min_replicas": 2, "cpu": 2, "memory": 4, \
                "image": "' + task_image + '" }',
    server_url: str = "http://kuberay-apiserver-service.kuberay.svc.cluster.local:8888",
    # data access
    data_s3_config: str = "{'input_folder': 'test/noop/input/', 'output_folder': 'test/noop/output/'}",
    data_s3_access_secret: str = "s3-secret",
    data_max_files: int = -1,
    data_num_samples: int = -1,
    data_checkpointing: bool = False,
    # orchestrator
    actor_options: str = "{'num_cpus': 0.8}",
    pipeline_id: str = "pipeline_id",
    code_location: str = "{'github': 'github', 'commit_hash': '12345', 'path': 'path'}",
    # noop parameters
    noop_sleep_sec: int = 10,
    # additional parameters
    additional_params: str = '{"wait_interval": 2, "wait_cluster_ready_tmout": 400, "wait_cluster_up_tmout": 300, "wait_job_ready_tmout": 400, "wait_print_tmout": 30, "http_retries": 5, "delete_cluster_delay_minutes": 0}',
```

The parameters used here are as follows:

* ray_name: name of the Ray cluster
* ray_run_id_KFPv2: Ray cluster unique ID used only in KFP v2
* ray_head_options: head node options, containing the following:
  * cpu - number of cpus
  * memory - memory
  * image - image to use
  * image_pull_secret - image pull secret
  * tolerations - (optional) tolerations for the ray pods
* ray_worker_options: worker node options (we here are using only 1 worker pool), containing the following:
  * replicas - number of replicas to create
  * max_replicas - max number of replicas
  * min_replicas - min number of replicas
  * cpu - number of cpus
  * memory - memory
  * image - image to use
  * image_pull_secret - image pull secret
  * tolerations - (optional) tolerations for the ray pods
* server_url - server url
* additional_params: additional (support) parameters, containing the following:
  * wait_interval - wait interval for API server, sec
  * wait_cluster_ready_tmout - time to wait for cluster ready, sec
  * wait_cluster_up_tmout - time to wait for cluster up, sec
  * wait_job_ready_tmout - time to wait for job ready, sec
  * wait_print_tmout - time between prints, sec
  * http_retries - http retries for API server calls
* data_s3_access_secret - s3 access secret
* data_s3_config - s3 configuration
* data_max_files - max files to process
* data_num_samples - num samples to process
* actor_options - actor options
* pipeline_id - pipeline id
* code_location - code location
* noop_sleep_sec - noop sleep time

**Note** that here we are specifying initial values for all parameters that will be propagated to the workflow UI
(see below)

### Pipeline definition <a name = "pipeline"></a> 

Now, when all components and input parameters are defined, we can implement pipeline wiring defining sequence of 
component execution and parameters submitted to every component. 

```python
    # In KFPv2 dsl.RUN_ID_PLACEHOLDER is deprecated and cannot be used since SDK 2.5.0. On another hand we cannot create
    # a unique string in a component (at runtime) and pass it to the `clean_up_task` of `ExitHandler`, due to
    # https://github.com/kubeflow/pipelines/issues/10187. Therefore, meantime the user is requested to insert
    # a unique string created at run creation time.
    if os.getenv("KFPv2", "0") == "1":
        print("WARNING: the ray cluster name can be non-unique at runtime, please do not execute simultaneous Runs of the "
              "same version of the same pipeline !!!")
        run_id = ray_run_id_KFPv2
    else:
        run_id = dsl.RUN_ID_PLACEHOLDER
    # create clean_up task
    clean_up_task = cleanup_ray_op(ray_name=ray_name, run_id=run_id, server_url=server_url, additional_params=additional_params)
    ComponentUtils.add_settings_to_component(clean_up_task, ONE_HOUR_SEC * 2)
    # pipeline definition
    with dsl.ExitHandler(clean_up_task):
      # compute execution params
      compute_exec_params = compute_exec_params_op(
          worker_options=ray_worker_options,
          actor_options=runtime_actor_options,
          data_s3_config=data_s3_config,
          data_max_files=data_max_files,
          data_num_samples=data_num_samples,
          data_checkpointing=data_checkpointing,
          runtime_pipeline_id=runtime_pipeline_id,
          runtime_job_id=run_id,
          runtime_code_location=runtime_code_location,
          noop_sleep_sec=noop_sleep_sec,
      )
      ComponentUtils.add_settings_to_component(compute_exec_params, ONE_HOUR_SEC * 2)
      # start Ray cluster
      ray_cluster = create_ray_op(
        ray_name=ray_name,
        run_id=run_id,
        ray_head_options=ray_head_options,
        ray_worker_options=ray_worker_options,
        server_url=server_url,
        additional_params=additional_params,
      )
      ComponentUtils.add_settings_to_component(ray_cluster, ONE_HOUR_SEC * 2)
      ray_cluster.after(compute_exec_params)
      # Execute job
      execute_job = execute_ray_jobs_op(
        ray_name=ray_name,
        run_id=run_id,
        additional_params=additional_params,
        # note that the parameters below are specific for NOOP transform
        exec_params={
          "data_s3_config": data_s3_config,
          "data_max_files": data_max_files,
          "data_num_samples": data_num_samples,
          "num_workers": compute_exec_params.output,
          "worker_options": actor_options,
          "pipeline_id": pipeline_id,
          "job_id": run_id,
          "code_location": code_location,
          "noop_sleep_sec": noop_sleep_sec,
        },
        exec_script_name=EXEC_SCRIPT_NAME,
        server_url=server_url,
      )
      ComponentUtils.add_settings_to_component(execute_job, ONE_WEEK_SEC)
      ComponentUtils.set_s3_env_vars_to_component(execute_job, data_s3_access_secret)
      execute_job.after(ray_cluster)
```

Here we first create `cleanup_task` and the use it as an 
[exit handler](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ExitHandler) which will be 
invoked either the steps into it succeeded or failed.

Then we create each individual component passing it required parameters and specify execution sequence, for example
(`ray_cluster.after(compute_exec_params)`).

### Additional configuration <a name = "add_config"></a>

The final thing that we need to do is set some pipeline global configuration:

```python
    # Configure the pipeline level to one week (in seconds)
    dsl.get_pipeline_conf().set_timeout(ONE_WEEK_SEC)
```

### KFP pods Toleration and node selector (Optional)<a name = "tolerations"></a> 
To apply kuberenetes [Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) or [nodeSelector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) to KFP pods, you need to set `KFP_TOLERATIONS` or `KFP_NODE_SELECTOR` environment variables respectively before compiling the pipeline. Here's an example:

```bash
export KFP_TOLERATIONS='[{"key": "key","operator": "Equal", "value1": "value", "effect": "NoSchedule"}]'

export KFP_NODE_SELECTOR='{"label_key":"cloud.google.com/gke-accelerator","label_value":"nvidia-tesla-p4"}'

```
In KFP v1, setting `KFP_TOLERATIONS` will apply to the Ray pods, overriding any tolerations specified in the `ray_head_options` and `ray_worker_options` pipeline parameters if they are present.

## Compiling a pipeline <a name = "compilation"></a>

To compile pipeline execute `make workflow-build` command in the same directory where your pipeline is. 

## Deploying a pipeline <a name = "deploying"></a>

Prepare local Kind or external Kubernetes cluster as described in [Set Up a cluster](./setup.md)

Once the cluster is up, go to the kfp endpoint (`localhost:8080/kfp/` for Kind cluster, the end point of the external existing 
cluster depends on the KFP end-point configuration), which will bring up 
KFP UI, see below:

![KFP UI](kfp_ui.png)

Click on the `Upload pipeline` link and follow instructions on the screen to upload your file (`noop_wf.yaml`) and
name pipeline noop. Once this is done, you should see something as follows:

![noop pipeline](noop_pipeline.png)


## Executing pipeline and watching execution results <a name = "execution"></a>

Before we can run the pipeline we need to create required secrets (one for image loading in case of secured 
image registry and one for S3 access). As KFP is deployed in `kubeflow` namespace, workflow execution will happen
there as well, which means that secrets have to be created there as well.

When the MinIO Object Store, deployed as part of KFP, is used, its access secret is deployed as part of the cluster preparation, 
see [s3_secret.yaml](../../scripts/k8s-setup/s3_secret.yaml). 
Creation a secret to pull images from a private repository described [here](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
)

Once this is done we can execute the workflow. 

On the pipeline page (above) click on the `create run` button. You will see the list of the parameters, that you
can redefine or use the default values that we specified above. After that,
go to the bottom of the page and click the `start` button

This will start workflow execution. Once it completes you will see something similar to below 

![execution result](execution_result.png)

Note that the log (on the left) has the complete execution log.

Additionally, the log is saved to S3 (location is denoted but the last line in the log)

## Clean up the cluster <a name = "cleanup"></a>

The cluster clean up is described at [Clean up the cluster](./setup#cleanup)

## Using HugginFace token <a name = "hf"></a>

This section explains how to use the HugginFace token for transforms that require it.
To prevent exposing the token in the pipeline, it is assumed that the token is stored as a kubernetes secret in the namespace where the pipeline runs.
To support that, the transform pipeline should include the following code after the [Components definition](#components) section:

```bash
from python_apiserver_client.params import (
    EnvVarFrom,
    EnvironmentVariables,
    EnvVarSource,
)

# The name of the secret that holds the HugginFace token
HF_SECRET = "hf-secret"
# The secret key that holds the HugginFace token
HF_SECRET_KEY = "hf-token"
# HuggingFace token is exported as environment variables in Ray node pods.
env_v = EnvVarFrom(source=EnvVarSource.SECRET, name=HF_SECRET, key=HF_SECRET_KEY)
envs = EnvironmentVariables(from_ref={"HF_READ_ACCESS_TOKEN": env_v})
```

In addition, `"environment": envs.to_dict()` should be added to `ray_head_options`
and `ray_worker_options` in [Input parameters definition](#inputs) section. For
example, for `ray_head_options`:
```bash
ray_head_options: dict = {"cpu": 1, "memory": 4, "image": task_image, "environment": envs.to_dict()},
```

and for `ray_worker_options`:
```bash
ray_worker_options: dict = {
        "replicas": 2,
        "max_replicas": 2,
        "min_replicas": 2,
        "cpu": 2,
        "memory": 4,
        "image": task_image,
        "environment": envs.to_dict(),
    },
```

Before running the pipeline, create a secret named `hf-secret` as shown below, ensuring that the `HF_READ_ACCESS_TOKEN` environment variable is defined first, holding the HugginFace token.

```bash
export HF_READ_ACCESS_TOKEN=<HugginFace token>
```
```bash
apiVersion: v1
kind: Secret
metadata:
  name: hf-secret
  namespace: kubeflow
type: Opaque
stringData:
      hf-token: "${HF_READ_ACCESS_TOKEN}"
``` 
