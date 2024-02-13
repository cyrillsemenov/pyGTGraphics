"""
find . -type f -name 'document.xml' -exec sh -c '
  for file do
    sed "1d" "$file" | xmlstarlet sel -t -m "//Composition/*" -v "name()" -n
  done
' sh {} + | sort -u

find . -type f -name 'document.xml' | python pyGTGraphics/pyGTGraphics/_parser.py | sort -u

"""

import os
import sys

# trunk-ignore(bandit/B405)
import xml.etree.ElementTree as ET
from collections import defaultdict


def parse_xml_skip_first_line(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        # Skip the first line
        next(file)
        # Read the rest of the file
        xml_content = file.read()
    # Parse the XML content from the string
    # trunk-ignore(bandit/B314)
    root = ET.fromstring(xml_content)
    return root


def process_node(node, node_info):
    for child in node:
        # Include direct attributes
        node_info[child.tag].update(child.attrib.keys())

        # Special handling for child nodes treated as attributes
        if "." in child.tag:
            _, attribute_name = child.tag.rsplit(".", 1)
            node_info[child.tag.split(".", 1)[0]].add(attribute_name)

        # Recurse into children
        process_node(child, node_info)


def process_file(filename, global_node_info):
    root = parse_xml_skip_first_line(filename)
    process_node(root, global_node_info)


def print_global_info(global_node_info):
    for node, attributes in global_node_info.items():
        attrs = ", ".join(sorted(attributes))
        print(f"'{node}': {attrs}")


if __name__ == "__main__":
    global_node_info = defaultdict(set)
    if not sys.stdin.isatty():
        input_stream = sys.stdin
    else:
        input_stream = sys.argv[1:]

    for line in input_stream:
        line = os.path.abspath(line.strip())
        process_file(line, global_node_info)
    print_global_info(global_node_info)
