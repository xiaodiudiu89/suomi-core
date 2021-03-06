/*
 Copyright 2017 Suomi Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
------------------------------------------------------------------------------
*/

#pragma once

#include <string>

// This is meant to be platform-independent services that are used by libpoet

namespace suomi {
    namespace poet {
        extern const size_t MAXIMUM_PATH_LENGTH;
        extern const std::string PATH_SEPARATOR;

        std::string GetDataDirectory();
        void Sleep(size_t milliseconds);
    } // namespace poet
} // namespace suomi
