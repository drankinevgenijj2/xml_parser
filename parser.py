from lxml import etree

class XMLParser:
    def __init__(self, params: list):
        self.__paths = {}

        for param in params:
            self.__paths.update({param.get('alias'): param.get('path')})

    def parse(self, xml: str, src_attrs: list) -> dict:
        result = []
        root = etree.fromstring(xml)

        for attr in src_attrs:
            path = None

            splitted = attr.lower().split('.')

            if len(splitted) > 1:
                alias = splitted[0]
                attr = splitted[1]
                path = self.__paths.get(alias).lower()

                if self._has_root_tag(root.tag, path):
                    path = self._remove_root_tag(root.tag, path)

            xpath = path + '/' + attr if path else attr

            if xpath[:2]!='./':
                xpath='./'+xpath
            
            if not root.findall(xpath):
                xpath='./'+xpath[xpath[3:].find('/')+3:]
                print(xpath)

            i=0
            for el in root.findall(xpath):
                value = el.text
                if len(result)<i+1:
                    result.append(dict())
                result[i].update({attr: value})
                i+=1


        return result

    def _has_root_tag(self, root: str, template: str) -> bool:
        return template[:len(root)] == root

    def _remove_root_tag(self, root: str, template: str):
        return template[len(root)+1:]


conditions = [{'alias': 'st1', 'path': '/appointment'},{'alias':'st2','path':'zAppointments/appointment'},{'alias':'st3','path':''}]
xml = open('/content/tree.xml', 'r').read()

pars = XMLParser(conditions)

attrs = ['st1.begin','st1.duration','st3.zAppointments']
# try:
result = pars.parse(xml, attrs)
print(result)
# except AttributeError:
#   print('pzdc')