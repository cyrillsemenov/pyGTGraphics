import xml.etree.ElementTree as ET


class Resources:
    def __init__(self):
        pass

    @staticmethod
    def to_xml():
        return ET.ElementTree(ET.Element("resources"))
