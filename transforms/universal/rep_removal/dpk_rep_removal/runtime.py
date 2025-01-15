# (C) Copyright IBM Corp. 2025.
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
from psutil import cpu_count
from dpk_rep_removal.transform import RepRemovalTransform
from data_processing.transform import TransformConfiguration
from data_processing.utils import ParamsUtils, CLIArgumentProvider, get_logger
from argparse import ArgumentParser, Namespace
from data_processing.runtime.pure_python import PythonTransformLauncher
from data_processing.runtime.pure_python.runtime_configuration import (
    PythonTransformRuntimeConfiguration,)

logger = get_logger(__name__)

short_name = "rep_removal"
cli_prefix = short_name + "_"

# configuration keys
contents_column_name_key = "contents_column_name"
""" Key holds the name of the column holding the document text."""
dedup_level_key = "dedup_level_name"
""" Key holds the type of file to process."""
length_thresh_key = "length_thresh"
""" Key holds the length threshold for processing"""
frequency_threshold_key = "frequency_threshold"
""" Key holds the frequency threshold for processing"""
retain_first_copy_key = "retain_first_copy"
""" Key holds boolean value for whether to retain first copy"""
tokenize_key = "tokenize"
""" Key holds boolean value for whether to tokenize"""
num_threads_key = "num_threads"
""" Key holds value for number of threads to use for processing"""
num_cpus_key = "num_cpus"
""" Key holds number of allocated cpus if Ray """

# CLI parameters corresponding to each config key
contents_column_name_cli_param = f"{cli_prefix}{contents_column_name_key}"
""" Name of the column holding the document text"""
dedup_level_cli_param = f"{cli_prefix}{dedup_level_key}"
""" Name of the type of file to process."""
length_thresh_cli_param = f"{cli_prefix}{length_thresh_key}"
""" Length threshold for processing"""
frequency_threshold_cli_param = f"{cli_prefix}{frequency_threshold_key}"
""" Frequency threshold for processing"""
retain_first_copy_cli_param = f"{cli_prefix}{retain_first_copy_key}"
""" Boolean value for whether to retain first copy"""
tokenize_cli_param = f"{cli_prefix}{tokenize_key}"
""" Boolean value for whether to tokenize"""
num_threads_cli_param = f"{cli_prefix}{num_threads_key}"
""" Value for number of threads to use for processing"""
num_cpus_cli_param = f"{cli_prefix}{num_cpus_key}"
""" Value of num cpus allocated for ray actor (if present)"""

# defaults - these are the values used
contents_column_name_default = "text"
dedup_level_default = "parquet"
length_thresh_default = str(50)
frequency_threshold_default = str(1)
retain_first_copy_default = True
tokenize_default = True
num_threads_default = str(4)
num_cpus_default = cpu_count(logical=False)


class RepRemovalTransformConfiguration(TransformConfiguration):
    def __init__(self):
        super().__init__(name='rep_removal', transform_class=RepRemovalTransform)

        self.daf = None

    def add_input_params(self, parser: ArgumentParser) -> None:
        """
        Add Transform-specific arguments to the given parser.
        This will be included in a dictionary used to initialize the BlockListTransform.
        By convention a common prefix should be used for all mutator-specific CLI args
        (e.g, noop_, pii_, etc.)
        """
        # The DataAccess created by the DataAccessFactory below will use this url
        parser.add_argument(
            f"--{contents_column_name_cli_param}",
            type=str,
            required=False,
            default=contents_column_name_default,
            help="Name of the column holding the document text",
        )
        parser.add_argument(
            f"--{dedup_level_cli_param}",
            type=str,
            required=False,
            default=dedup_level_default,
            help="Name of the type of file to process.",
        )
        parser.add_argument(
            f"--{length_thresh_cli_param}",
            type=str,
            required=False,
            default=length_thresh_default,
            help="Length threshold for processing",
        )
        parser.add_argument(
            f"--{frequency_threshold_cli_param}",
            type=str,
            required=False,
            default=frequency_threshold_default,
            help="Frequency threshold for processing.",
        )
        parser.add_argument(
            f"--{retain_first_copy_cli_param}",
            type=str,
            required=False,
            default=retain_first_copy_default,
            help="Boolean value for whether to retain first copy",
        )
        parser.add_argument(
            f"--{tokenize_cli_param}",
            type=str,
            required=False,
            default=tokenize_default,
            help="Boolean value for whether to tokenize",
        )
        parser.add_argument(
            f"--{num_threads_cli_param}",
            type=str,
            required=False,
            default=num_threads_default,
            help="Value for number of threads to use for processing",
        )
        parser.add_argument(
            f"--{num_cpus_cli_param}",
            type=str,
            required=False,
            default=num_cpus_default,
            help="Value for number of cpus allocated for processing",
        )

    def apply_input_params(self, args: Namespace) -> bool:
        """
        Validate and apply the arguments that have been parsed
        :param args: user defined arguments.
        :return: True, if validate pass or False otherwise
        """
        # Capture the args that are specific to this transform
        captured = CLIArgumentProvider.capture_parameters(args, cli_prefix, False)
        self.params = self.params | captured
        return True


class RepRemovalPythonTransformConfiguration(PythonTransformRuntimeConfiguration):

    def __init__(self):
        super().__init__(transform_config=RepRemovalTransformConfiguration())


class RepRemoval:
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
        sys.argv = ParamsUtils.dict_to_req(d=self.params)
        launcher = PythonTransformLauncher(RepRemovalPythonTransformConfiguration())
        return_code = launcher.launch()
        return return_code


if __name__ == "__main__":
    launcher = PythonTransformLauncher(RepRemovalPythonTransformConfiguration())
    launcher.launch()
