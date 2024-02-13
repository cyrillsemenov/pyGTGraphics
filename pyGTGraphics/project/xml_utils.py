"""
Description: This module extends standard xml.etree library capabilities.
Author: Cyrill Semenov
Date Created: 2023/11/09
Date Modified: 2023/11/09
Version: 1.0
License: MIT License
"""

import xml.etree.ElementTree as ET
from typing import Optional


def write_xml(
    element_tree: ET.ElementTree,
    filename: str,
    encoding: Optional[str] = None,
    declared_encoding: Optional[str] = None,
    xml_declaration: Optional[bool] = None,
) -> None:
    """
    Write an ElementTree object to a file as XML, allowing for different file encoding
    and declared encoding within the XML declaration.

    Parameters:
    - element_tree (ElementTree): An XML ElementTree to write.
    - filename (str): The path to the output file.
    - encoding (str, optional): The encoding of the output file. Defaults to 'utf-8'.
    - declared_encoding (str, optional): The encoding declared in the XML header.
      If not provided, it defaults to the same value as `encoding`.
    - xml_declaration (bool, optional): Whether to add an XML declaration at the start of the file.
      If not provided, the declaration is not added.

    Returns:
    - None
    """
    _encoding = encoding or "utf-8"
    _declared_encoding = declared_encoding or _encoding
    with open(
        filename, "w", encoding=_encoding.lower(), errors="xmlcharrefreplace"
    ) as file:
        if xml_declaration:
            file.write("<?xml version='1.0' encoding='%s'?>\n" % (_declared_encoding,))
        # TODO: The following operations are internal to ElementTree and should be replaced
        #   with public API calls if possible, as direct access to these functions may not
        #   be compatible with all versions of Python's standard library.
        # noinspection All
        qnames, namespaces = ET._namespaces(element_tree._root, None)
        # noinspection All
        ET._serialize_xml(
            file.write,
            element_tree._root,
            qnames,
            namespaces,
            short_empty_elements=True,
        )
