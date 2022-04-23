import xml.etree.ElementTree as ET
import pathlib
from zipfile import ZipFile
import shutil
import json
import xmltodict

NSPS = {"opf": "{http://www.idpf.org/2007/opf}", "element": "{http://purl.org/dc/elements/1.1}"}


def read_xml(xml_file_path: str):
    with open(xml_file_path) as xml_file:
        data_dict = dict(xmltodict.parse(xml_file.read()))
    return data_dict


def pprint(arr):
    print(json.dumps([str(a) for a in arr], indent=2))


def main(args):
    epub_file = pathlib.Path(args[0]).resolve()
    if not epub_file.exists():
        print("!!!!! FILE COULD NOT BE FOUND")
        exit(1)

    epub_dump = pathlib.Path(args[0]+'.unzipped/')
    if epub_dump.resolve().exists():
        shutil.rmtree(epub_dump.absolute().__str__())

    #
    epub_dump.mkdir(parents=True, exist_ok=True)
    with ZipFile(epub_file.absolute().__str__(), 'r') as zip:
        zip.extractall(epub_dump.absolute().__str__())

    meta = list(epub_dump.glob("META-INF/container.xml"))[0]  # TODO: check, if not break
    meta_xml = read_xml(meta.absolute().__str__())
    print(json.dumps(meta_xml, indent=2))
    rootfile = (epub_dump / meta_xml["container"]["rootfiles"]["rootfile"]["@full-path"]).resolve()

    data_dict = read_xml(rootfile)


if __name__ == '__main__':
    from sys import argv
    main(argv[1:])
