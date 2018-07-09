from lxml import etree
import random  as r
import properties as p

def generate_random_parameters(value):
    if type(value[0]) == float:
        tmp = round(r.uniform(value[0],value[1]),2)
    elif type(value[0]) == int:
        tmp = int(round(r.uniform(value[0],value[1]),0))
    elif type(value[0]) == bool:
        tmp = r.choice(value)

    return tmp


def xml_parser(i):
    P = p.Parameters
    v = []

    conf = etree.Element("configuration")
    for key,value in P.items():
        tmp = generate_random_parameters(value)
        prop = etree.SubElement(conf, "property")
        name = etree.SubElement(prop, "name")
        value = etree.SubElement(prop, "value")
        name.text = key
        value.text = str(tmp)
        v.append(tmp)

    et = etree.ElementTree(conf)
    et.write(("hbase-site.xml"+str(i)), pretty_print=True)
    return v





if __name__ == '__main__':
    for i in range(0,3):
        v = xml_parser(i)
        print(v)








#soit utiliser  In [21]: text_type_determine("2016.23")
#               Out[21]: 'double'
# OU bien creer encore un autre dict et y mettre les doubles... cela revient au meme...
