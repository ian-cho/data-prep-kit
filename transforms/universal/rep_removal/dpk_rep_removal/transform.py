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

import subprocess
import os
import tempfile
import pyarrow as pa
import pandas as pd
from dpk_rep_removal.dedup_pq_level import load_pq_docs_once_avoidIO, extract_dup_per_doc_avoidIO_further, save_deduped_pq_once
from dpk_rep_removal.dedup_Rust_scripts import find_repeated_substrings, collect_duplicates_avoidIO
from typing import Any
from psutil import cpu_count
from dpk_rep_removal.make_suffix_array import make_suffix_array
from data_processing.transform import AbstractTableTransform


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


# defaults - these are the values used
contents_column_name_default = "text"
dedup_level_default = "parquet"
length_thresh_default = str(50)
frequency_threshold_default = str(1)
retain_first_copy_default = True
tokenize_default = True
num_threads_default = str(4)
num_cpus_default = cpu_count(logical=False)


class RepRemovalTransform(AbstractTableTransform):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)

        self.contents_column_name = config.get(contents_column_name_key, contents_column_name_default)
        self.dedup_level = config.get(dedup_level_key, dedup_level_default)
        self.length_thresh = config.get(length_thresh_key, length_thresh_default)
        self.frequency_threshold = config.get(frequency_threshold_key, frequency_threshold_default)
        self.retain_first_copy = config.get(retain_first_copy_key, retain_first_copy_default)
        self.tokenize = config.get(tokenize_key, tokenize_default)
        self.num_threads = config.get(num_threads_key, num_threads_default)
        self.num_cpus = config.get(num_cpus_key, num_cpus_default)

    def transform(self, table: pa.Table, file_name: str = None) -> tuple[list[pa.Table], dict[str, Any]]:
        """ """
        pq_df = table.to_pandas()
        try:
            with tempfile.TemporaryDirectory() as td:
                save_dir = os.path.join(td, 'save_dir')
                encoded_pq = os.path.join(save_dir, self.dedup_level)

                load_pq_docs_once_avoidIO(pq_df, self.contents_column_name, save_dir, self.dedup_level,
                                          self.tokenize, int(self.num_threads))

                cache_dir = os.path.join(td, 'cache')
                temp_dir = os.path.join(td, 'tmp')
                os.makedirs(cache_dir)
                os.makedirs(temp_dir)

                make_suffix_array(encoded_pq, temp_dir, self.dedup_level, int(self.num_threads), int(self.num_cpus))
                find_repeated_substrings(encoded_pq, self.length_thresh, cache_dir, self.num_threads,
                                         self.frequency_threshold, self.retain_first_copy)

                repeated_pairs = collect_duplicates_avoidIO(encoded_pq, self.length_thresh, cache_dir)
                extract_dup_per_doc_avoidIO_further(repeated_pairs)

                output_pq = os.path.join(td, 'output.parquet')
                pre_content_col_size, deduped_content_col_size = save_deduped_pq_once(pq_df, output_pq,
                                                                                      self.contents_column_name,
                                                                                      self.num_threads,
                                                                                      self.tokenize)

                metadata = {
                    "pre_content col size": pre_content_col_size,
                    "rep_removed_content col size": deduped_content_col_size
                }

            # add deduped to res table
                deduped_table = pd.read_parquet(output_pq)
                res_table = pa.Table.from_pandas(deduped_table)

                return [res_table], metadata

        except subprocess.TimeoutExpired:
            print("subprocess timed out. skipping file")
            return [], {}

        except subprocess.CalledProcessError:
            print("error during subprocess call. skipping file")
            return [], {}
