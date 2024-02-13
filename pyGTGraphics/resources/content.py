import xml.etree.ElementTree as ET


class ContentTypes:
    def __init__(self):
        pass

    @staticmethod
    def to_xml():
        # <?xml version="1.0" encoding="utf-8"?>
        # <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
        #     <Default Extension="xml" ContentType="text/xml" />
        #     <Default Extension="png" ContentType="image/png" />
        # </Types>
        types = ET.Element(
            "Types",
            xmlns="http://schemas.openxmlformats.org/package/2006/content-types",
        )
        ET.SubElement(types, "Default", Extension="xml", ContentType="text/xml")
        ET.SubElement(types, "Default", Extension="png", ContentType="image/png")
        return ET.ElementTree(types)
