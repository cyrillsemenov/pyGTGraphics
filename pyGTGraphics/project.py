import os.path
import tempfile
import xml.etree.ElementTree as ET
import zipfile

from pyGTGraphics.objects import Layer, Root
from pyGTGraphics.content import ContentTypes
from pyGTGraphics.resources import Resources
from pyGTGraphics.xml_utils import write_xml


class Project:
    """
    Represents a project for creating and managing GT graphics layouts.

    Attributes:
        document (Root): The root object of the project containing layout elements.
        resources (Resources): The resources manager for the project.
        types (ContentTypes): Manager for content types used in the project.
        filename (str): The name of the file to save the project to.
    """
    def __init__(self, width: int, height: int, filename=None) -> None:
        """
        Initialize a new Project instance.

        Args:
            width (int): The width of the project canvas.
            height (int): The height of the project canvas.
            filename (str, optional): The default filename to save the project to.
        """
        self._dir = tempfile.TemporaryDirectory()

        self.document = Root(width, height)
        self.resources = Resources()
        self.types = ContentTypes()
        self.filename = filename

    def create_layer(self, name: str, x: int = None, y: int = None, width: int = None, height: int = None) -> Layer:
        return self.document.create_layer(name, x, y, width, height)

    def save(self, filename=None) -> None:
        """
        Save the project to a file.

        Args:
            filename (str, optional): The filename to save the project to. If not
                                      provided, the instance's filename is used.

        Raises:
            ValueError: If no filename is provided and the instance's filename is None.
        """
        tree = self.document.to_xml()
        # document.xml
        ET.indent(tree, "  ")
        write_xml(
            tree,
            os.path.join(self._dir.name, "document.xml"),
            declared_encoding="utf-16", xml_declaration=True
        )
        # resources.xml
        resources = Resources()
        write_xml(
            resources.to_xml(),
            os.path.join(self._dir.name, "resources.xml"),
            xml_declaration=False
        )
        # [Content_Types].xml
        types = ContentTypes()
        write_xml(
            types.to_xml(),
            os.path.join(self._dir.name, "[Content_Types].xml"),
            xml_declaration=True
        )
        # thumbnail.png
        # TODO: generate thumbnail

        output_file = filename or self.filename
        if not output_file:
            raise ValueError("Filename must be provided.")

        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_STORED, allowZip64=False) as zf:
            print(zf.filename)
            for filename in os.listdir(self._dir.name):
                f = os.path.join(self._dir.name, filename)
                f = os.path.normpath(f)
                if os.path.isfile(f):
                    zf.write(f, filename)

    def __del__(self) -> None:
        self._dir.cleanup()

    def __enter__(self) -> 'Project':
        """
        Support usage of the class as a context manager.
        Ensure that a filename is set for the project before entering the context.

        Returns:
            Project: The instance itself.

        Raises:
            ValueError: If the filename has not been provided.
        """
        if not self.filename:
            raise ValueError("A filename must be provided for the project before entering the context manager.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Finalize the project and clean up resources when exiting the context.
        If an exception occurred, handle it gracefully.

        Args:
            exc_type: The exception type if an exception has been raised in the context.
            exc_val: The exception value if an exception has been raised.
            exc_tb: The traceback if an exception has been raised.

        Returns:
            bool: True if the exception was handled here, False otherwise.
        """

        try:
            if not exc_type:
                self.save()
        finally:
            self._dir.cleanup()

        return False

