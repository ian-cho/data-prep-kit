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

from data_processing.runtime.pure_python import PythonTransformLauncher
from data_processing.test_support.launch.transform_test import (
    AbstractTransformLauncherTest,
)
from dpk_tokenization2arrow.runtime import Tokenization2ArrowPythonConfiguration


tkn_params = {
    "tkn_tokenizer": "hf-internal-testing/llama-tokenizer",
    "tkn_doc_id_column": "document_id",
    "tkn_doc_content_column": "contents",
    "tkn_text_lang": "en",
    "tkn_chunk_size": 0,
}


class TestRayTokenization2ArrowTransform(AbstractTransformLauncherTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        basedir = "../test-data"
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), basedir))
        launcher = PythonTransformLauncher(Tokenization2ArrowPythonConfiguration())
        fixtures = [(launcher, tkn_params, basedir + "/ds01/input", basedir + "/ds01/expected")]
        return fixtures
