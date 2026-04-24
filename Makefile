# This file is part of Dependency-Track.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

build: dev-image
	docker run --rm \
	  -v "$(shell pwd)":/docs \
	  "dependency-track-docs-dev" \
	  build --strict
.PHONY: build

clean:
	rm -rf site/
.PHONY: clean

lint: lint-markdown lint-yaml lint-prose
.PHONY: lint

lint-markdown:
	docker run --rm \
	  -v "$(shell pwd)":/workdir \
	  davidanson/markdownlint-cli2:v0.18.1 \
	  "docs/**/*.md" "context/**/*.md"
.PHONY: lint-markdown

lint-yaml:
	docker run --rm \
	  -v "$(shell pwd)":/workdir \
	  -w /workdir \
	  pipelinecomponents/yamllint:0.35.1 \
	  yamllint .
.PHONY: lint-yaml

lint-prose:
	docker run --rm \
	  -v "$(shell pwd)":/workdir \
	  -w /workdir \
	  jdkato/vale:v3.14.1 \
	  sync && \
	docker run --rm \
	  -v "$(shell pwd)":/workdir \
	  -w /workdir \
	  jdkato/vale:v3.14.1 \
	  docs/
.PHONY: lint-prose

serve: dev-image
	docker run --rm -it \
	  -p 8000:8000 \
	  -v "$(shell pwd)":/docs \
	  "dependency-track-docs-dev" \
	  serve --livereload -a '0.0.0.0:8000'
.PHONY: serve

dev-image:
	docker build -t "dependency-track-docs-dev" .
.PHONY: dev-image

lock:
	docker run --rm \
	  -v "$(shell pwd)":/work \
	  -w /work \
	  python:3.14-slim \
	  sh -c "pip install -q pip-tools && pip-compile --generate-hashes --strip-extras --output-file=requirements.txt requirements.in"
.PHONY: lock
