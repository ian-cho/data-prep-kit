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

import os

from data_processing.test_support.launch.transform_test import (
    AbstractTransformLauncherTest,
)
from data_processing_ray.runtime.ray import RayTransformLauncher
from dpk_rep_removal.ray.runtime import RepRemovalRayTransformConfiguration


class TestRayRepRemovalTransform(AbstractTransformLauncherTest):

    def get_test_transform_fixtures(self) -> list[tuple]:
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               "../test-data"))
        fixtures = []
        transform_config = {
            "run_locally": True,
            "rep_removal_contents_column_name": 'text',
            "rep_removal_num_threads":  '1',

        }
        launcher = RayTransformLauncher(RepRemovalRayTransformConfiguration())
        fixtures.append((launcher, transform_config,
                         basedir + "/input",
                         basedir + "/expected"))
        return fixtures
