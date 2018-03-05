# Copyright 2017 Suomi Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import collections
import logging
import os

import toml

from suomi_sdk.processor.exceptions import LocalConfigurationError

LOGGER = logging.getLogger(__name__)


def load_default_block_info_config():
    """
    Returns the default BlockInfoConfig
    """
    return BlockInfoConfig(
        connect='tcp://localhost:4004',
    )


def load_toml_block_info_config(filename):
    """Returns a BlockInfoConfig created by loading a TOML file from the
    filesystem.

    Args:
        filename (string): The name of the file to load the config from

    Returns:
        config (BlockInfoConfig): The BlockInfoConfig created from the stored
            toml file.

    Raises:
        LocalConfigurationError
    """
    if not os.path.exists(filename):
        LOGGER.info(
            "Skipping transaction proccesor config loading from non-existent"
            " config file: %s", filename)
        return BlockInfoConfig()

    LOGGER.info("Loading transaction processor information from config: %s",
                filename)

    try:
        with open(filename) as fd:
            raw_config = fd.read()
    except IOError as e:
        raise LocalConfigurationError(
            "Unable to load transaction processor configuration file:"
            " {}".format(str(e)))

    toml_config = toml.loads(raw_config)
    invalid_keys = set(toml_config.keys()).difference(
        ['connect'])
    if invalid_keys:
        raise LocalConfigurationError(
            "Invalid keys in transaction processor config: "
            "{}".format(", ".join(sorted(list(invalid_keys)))))

    config = BlockInfoConfig(
        connect=toml_config.get("connect", None)
    )

    return config


def merge_block_info_config(configs):
    """
    Given a list of BlockInfoConfig object, merges them into a single
    BlockInfoConfig, giving priority in the order of the configs
    (first has highest priority).

    Args:
        config (list of BlockInfoConfigs): The list of block_info configs that
            must be merged together

    Returns:
        config (BlockInfoConfig): One BlockInfoConfig that combines all of the
            passed in configs.
    """
    connect = None

    for config in reversed(configs):
        if config.connect is not None:
            connect = config.connect

    return BlockInfoConfig(
        connect=connect
    )


class BlockInfoConfig:
    def __init__(self, connect=None):
        self._connect = connect

    @property
    def connect(self):
        return self._connect

    def __repr__(self):
        # not including  password for opentsdb
        return \
            "{}(connect={})".format(
                self.__class__.__name__,
                repr(self._connect),
            )

    def to_dict(self):
        return collections.OrderedDict([
            ('connect', self._connect),
        ])

    def to_toml_string(self):
        return str(toml.dumps(self.to_dict())).strip().split('\n')
