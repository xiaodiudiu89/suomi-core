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

import random
import string
import hashlib

from suomi_signing import create_context


CONTEXT = create_context('secp256k1')


def random_name(length=16):
    return ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(length))


def create_random_private_key():
    return CONTEXT.new_random_private_key()


def create_random_public_key():
    return CONTEXT.get_public_key(create_random_private_key())


def create_random_public_key_hash():
    public_key_bytes = create_random_public_key().as_hex().encode()
    return hashlib.sha256(public_key_bytes).hexdigest()
