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

MARKDOWNLINT_IMAGE := davidanson/markdownlint-cli2:v0.18.1
PROTOC_GEN_DOC_IMAGE := pseudomuto/protoc-gen-doc:1.5
VALE_IMAGE := jdkato/vale:v3.14.1
VALE_SYNC_STAMP := .vale/styles/.synced
YAMLLINT_IMAGE := pipelinecomponents/yamllint:0.35.1

build:
	uv run mkdocs build --strict
.PHONY: build

clean:
	rm -rf site/
.PHONY: clean

lint: lint-markdown lint-yaml lint-prose lint-python
.PHONY: lint

lint-markdown:
	docker run --rm \
	  -v "$(shell pwd)":/workdir \
	  "$(MARKDOWNLINT_IMAGE)" \
	  "context/**/*.md" \
	  "docs/**/*.md"
.PHONY: lint-markdown

lint-yaml:
	docker run --rm \
	  -v "$(shell pwd)":/workdir \
	  -w /workdir \
	  "$(YAMLLINT_IMAGE)" \
	  yamllint .
.PHONY: lint-yaml

lint-python:
	uvx ruff check scripts/
	uvx ruff format --check scripts/
.PHONY: lint-python

# Only sync vale when .vale.ini has changed since last sync.
# https://www.technovelty.org/tips/the-stamp-idiom-with-make.html
$(VALE_SYNC_STAMP): .vale.ini
	docker run --rm \
	  -v "$(shell pwd)":/workdir \
	  -w /workdir \
	  "$(VALE_IMAGE)" \
	  sync
	@mkdir -p $(dir $@) && touch $@

lint-prose: $(VALE_SYNC_STAMP)
	docker run --rm \
	  -v "$(shell pwd)":/workdir \
	  -w /workdir \
	  "$(VALE_IMAGE)" \
	  --output=line \
	  docs/
.PHONY: lint-prose

generate-config-docs:
	uv run --only-group generate scripts/generate_config_docs.py \
	  --template scripts/templates/config-docs.md.j2 \
	  --output docs/reference/configuration/properties.md \
	  $(APISERVER_PROPERTIES)
.PHONY: generate-config-docs

generate-proto-docs:
	docker run -i --rm -u "$$(id -u):$$(id -g)" \
	  -v "$$(pwd)/docs/reference/schemas:/out" \
	  -v "$$(pwd)/$(APISERVER_DIR)/notification/api/src/main/proto/org/dependencytrack/notification/v1:/protos" \
	  "$(PROTOC_GEN_DOC_IMAGE)" \
	  --doc_opt=/out/notification.md.tmpl,notification.md
	docker run -i --rm -u "$$(id -u):$$(id -g)" \
	  -v "$$(pwd)/docs/reference/schemas:/out" \
	  -v "$$(pwd)/$(APISERVER_DIR)/proto/src/main/proto/org/dependencytrack/policy/v1:/protos" \
	  "$(PROTOC_GEN_DOC_IMAGE)" \
	  --doc_opt=/out/policy.md.tmpl,policy.md
.PHONY: generate-proto-docs

serve:
	uv run mkdocs serve --livereload
.PHONY: serve
