class XmlTestCase(TestCase):
    def xml_compare(self, xml_true, xml_expected, excludes=[], parent='/'):
        if xml_true.tag != xml_expected.tag:
            xml_true.text
            raise AssertionError(
                'Tags do not match: <%s>%s != <%s>%s' % (parent, xml_true.tag, parent, xml_expected.tag))
        for name, value in xml_true.attrib.items():
            if not name in excludes:
                if xml_expected.attrib.get(name) != value:
                    raise AssertionError('Attributes do not match: <%s><%s %s=%r ..> != <%s><%s %s=%r ..>'
                                         % ( parent, xml_true.tag, name, value, parent,
                                             xml_expected.tag, name, xml_expected.attrib.get(name)))
        for name in xml_expected.attrib.keys():
            if not name in excludes:
                if name not in xml_true.attrib:
                    raise AssertionError('x2 has an attribute x1 is missing: %s' % name)
        if not self.text_compare(xml_true.text, xml_expected.text):
            raise AssertionError('text: %r != %r' % (xml_true.text, xml_expected.text))
        if not self.text_compare(xml_true.tail, xml_expected.tail):
            raise AssertionError('tail: %r != %r' % (xml_true.tail, xml_expected.tail))
        cl1 = xml_true.getchildren()
        cl2 = xml_expected.getchildren()

        i = 0
        for c1, c2 in zip(cl1, cl2):
            i += 1
            if not self.xml_compare(c1, c2, excludes, parent=xml_true.tag):
                raise AssertionError('children %i do not match: %s'
                                     % (i, c1.tag))
        return True

    def text_compare(self, t1, t2):
        if not t1 and not t2:
            return True
        if t1 == '*' or t2 == '*':
            return True
        return (t1 or '').strip() == (t2 or '').strip()
