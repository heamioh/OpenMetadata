#  Copyright 2025 Collate
#  Licensed under the Collate Community License, Version 1.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  https://github.com/open-metadata/OpenMetadata/blob/main/ingestion/LICENSE
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Test GitHub Reader
"""
from unittest import TestCase

from metadata.generated.schema.security.credentials.gitlabCredentials import (
    GitlabCredentials,
)
from metadata.ingestion.source.dashboard.looker.models import Includes, ViewName
from metadata.ingestion.source.dashboard.looker.parser import LkmlParser
from metadata.readers.file.gitlab import GitlabReader


class TestLookMLGitlabReader(TestCase):
    """
    Validate the github reader against the OM repo
    """

    creds = GitlabCredentials(
        # An accessible LookML Gitlab Repository is required to run this Test
        repositoryName="test-group/test-repo",
        repositoryOwner="test-owner",
        token="token",
    )

    reader = GitlabReader(creds)
    parser = LkmlParser(reader)

    def x_test_lookml_read_and_parse(self):
        """
        To test the Gitlab reader, update these files with files in your test LookML repository and enable the test
        """

        explore_file = "test_explore.model.lkml"
        self.parser.parse_file(Includes(explore_file))

        contents = self.parser.parsed_files.get(Includes(explore_file))

        # Check file contents
        self.assertIn("explore: test-explore", contents)

        view = self.parser.find_view(
            view_name=ViewName("test-view"), path=Includes(explore_file)
        )

        # We can get views that are resolved even if the include does not contain `.lkml`
        self.assertIsNotNone(view)
        self.assertEqual(view.name, "test-view")
