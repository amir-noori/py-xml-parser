
from Parser import XmlParser

xml_string = """
<Root>
    <ChildA>
    </ChildA>
    <ChildA>
        <ChildB>
            <ChildCa>
            </ChildCa>
            <ChildCb>
                <a>
                    <b>
                        <ca>
                        </ca>
                        <cb>
                        </cb>
                    </b>
                </a>
            </ChildCb>
        </ChildB>
    </ChildA>
    
</Root>
"""

if __name__ == "__main__":
    parser = XmlParser(xml_string)
    parser.parse().show()