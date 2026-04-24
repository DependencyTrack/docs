#!/usr/bin/env python3

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

"""Generate configuration documentation from application.properties files."""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def parse_properties(path, include_hidden=False):
    """Parse an application.properties file and extract config property metadata."""
    lines = Path(path).read_text().splitlines()
    properties = []
    current = _new_property()

    line_index = 0
    while line_index < len(lines):
        line = lines[line_index].strip()

        if not line:
            if current != _new_property():
                print(
                    f"\033[33m[!] Detected empty line, discarding incomplete"
                    f" property: {current}\033[0m",
                    file=sys.stderr,
                )
                current = _new_property()
            line_index += 1
            continue

        if re.match(r"^#[\s\w]", line):
            line = line[1:].strip()
            if re.match(r"^@type:\s", line):
                current["type"] = line.split(":", 1)[1].strip().lower()
            elif re.match(r"^@category:\s", line):
                current["category"] = line.split(":", 1)[1].strip()
            elif re.match(r"^@default:\s", line):
                current["default_value"] = line.split(":", 1)[1].strip()
            elif re.match(r"^@example:\s", line):
                current["example"] = line.split(":", 1)[1].strip()
            elif re.match(r"^@valid-values:\s", line):
                current["valid_values"] = line.split(":", 1)[1].strip()
            elif re.match(r"^@hidden\s*$", line):
                current["hidden"] = True
            elif re.match(r"^@required\s*$", line):
                current["required"] = True
            elif re.match(r"^@deprecated:\s", line):
                current["deprecated"] = line.split(":", 1)[1].strip()
            elif re.match(r"^[\w.\-]+=", line):
                # Commented-out property definition.
                line_index = _finalize_property(
                    line, lines, line_index, current, properties, include_hidden
                )
                current = _new_property()
            else:
                if current["description"] is None:
                    current["description"] = line + "  "
                else:
                    current["description"] += line + "  "
        elif "=" in line:
            line_index = _finalize_property(
                line, lines, line_index, current, properties, include_hidden
            )
            current = _new_property()

        line_index += 1

    return properties


def _new_property():
    return {
        "name": None,
        "default_value": None,
        "type": None,
        "valid_values": None,
        "description": None,
        "example": None,
        "category": None,
        "required": False,
        "deprecated": None,
        "hidden": False,
    }


def _finalize_property(line, lines, line_index, current, properties, include_hidden):
    """Parse name=value from line, handle multi-line defaults, add to properties."""
    parts = line.split("=", 1)
    current["name"] = parts[0].strip()
    default_value = parts[1].strip() if len(parts) > 1 else ""

    # Handle multi-line defaults (trailing backslash).
    if default_value.endswith("\\"):
        default_value = default_value.rstrip("\\")
        next_index = line_index + 1
        while next_index < len(lines):
            next_line = lines[next_index]
            # Continuation lines are either comment-prefixed or whitespace-prefixed.
            if re.match(r"^#\s+", next_line):
                continuation = re.sub(r"^#", "", next_line).strip()
            elif re.match(r"^\s+", next_line):
                continuation = next_line.strip()
            else:
                break
            default_value += continuation
            if not default_value.endswith("\\"):
                break
            default_value = default_value.rstrip("\\")
            next_index += 1
        line_index = next_index

    # Skip profile-specific properties.
    if current["name"].startswith("%"):
        print(
            f"\033[33m[!] Skipping profile-specific property {current['name']}\033[0m",
            file=sys.stderr,
        )
        return line_index

    if not current["default_value"]:
        current["default_value"] = default_value
    elif default_value:
        print(
            f"\033[33m[!] {current['name']} has both a default value"
            f" ({default_value}) and a @default annotation"
            f" ({current['default_value']})\033[0m",
            file=sys.stderr,
        )

    if not current["hidden"] or include_hidden:
        properties.append(current)

    return line_index


def _anchor(name):
    return name.replace(".", "").replace('"', "").lower()


def _env(name):
    return name.replace(".", "_").replace("-", "_").replace('"', "_").upper()


def _validate_default(prop):
    """Validate that the default value matches the declared type."""
    default = prop["default_value"]
    prop_type = prop["type"]
    if not default or not prop_type or re.match(r"^\$\{[\w.]+}$", default):
        return
    try:
        if prop_type == "boolean" and default not in ("true", "false"):
            raise ValueError(f"{default} is not a valid boolean value")
        elif prop_type == "double":
            float(default)
        elif prop_type == "integer":
            int(default)
        elif prop_type == "duration":
            if not re.match(r"^P", default, re.IGNORECASE):
                raise ValueError(f"{default} is not a valid ISO 8601 duration")
    except (ValueError, TypeError) as e:
        print(
            f"\033[33m[!] Definition of property {prop['name']} appears to be"
            f" invalid: {e}\033[0m",
            file=sys.stderr,
        )


def post_process(properties):
    """Apply cross-referencing, validation, and env/anchor computation."""
    anchors_by_name = {p["name"]: _anchor(p["name"]) for p in properties}

    for prop in properties:
        _validate_default(prop)

        if not prop["default_value"] or not prop["default_value"].strip():
            prop["default_value"] = "null"

        if prop["type"] == "enum" and not prop.get("valid_values"):
            print(
                f"\033[33m[!] Property {prop['name']} is of type enum, but"
                f" does not define any valid values\033[0m",
                file=sys.stderr,
            )

        # Cross-reference property names in description and deprecated fields.
        for field in ("description", "deprecated"):
            if prop.get(field):
                for ref_name, ref_anchor in anchors_by_name.items():
                    prop[field] = re.sub(
                        r"\b" + re.escape(ref_name) + r"\b",
                        f"[`{ref_name}`](#{ref_anchor})",
                        prop[field],
                    )

        if prop["description"] is None:
            prop["description"] = ""

        prop["env"] = _env(prop["name"])
        prop["anchor"] = _anchor(prop["name"])

    # Group by category, sorted.
    by_category = defaultdict(list)
    for prop in properties:
        category = prop["category"] or "Other"
        by_category[category].append(prop)

    sorted_categories = dict(sorted(by_category.items()))
    for props in sorted_categories.values():
        props.sort(key=lambda p: p["name"])

    return sorted_categories


def render(properties_by_category, template_path, args):
    """Render properties using Jinja2 template."""
    template_dir = str(Path(template_path).parent)
    template_name = Path(template_path).name

    env = Environment(
        loader=FileSystemLoader(template_dir),
        keep_trailing_newline=True,
        trim_blocks=False,
        lstrip_blocks=False,
    )
    template = env.get_template(template_name)

    return template.render(
        properties_by_category=properties_by_category,
        generate_command=" ".join(args),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate configuration documentation from application.properties"
    )
    parser.add_argument("properties_file", help="Path to application.properties")
    parser.add_argument(
        "-t", "--template", required=True, help="Path to Jinja2 template"
    )
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    parser.add_argument(
        "--include-hidden", action="store_true", help="Include hidden properties"
    )
    args = parser.parse_args()

    properties = parse_properties(args.properties_file, args.include_hidden)
    properties_by_category = post_process(properties)
    output = render(properties_by_category, args.template, sys.argv[1:])

    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
