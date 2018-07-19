import xml.etree.ElementTree as ET
from lxml import etree

if __name__ == '__main__':
    for i in range(1,21):
        print(i)
        tree = ET.parse("hbase_param_file/hbase-site"+str(i)+".xml")
