"""Tests that filling out the database works as expected.
"""


import unittest
from manuscript_clusterer.api.database.fill_database import parse_manuscript


class TestFillDatabase(unittest.TestCase):
    """Tests that filling out the database works as expected.
    """

    def setUp(self):
        self.demo_XML = """<?xml version="1.0" encoding="utf-8"?>
          <?xml-stylesheet type="text/xsl" href="NTPapyri.xsl"?>
          <?xml-model href="TEI-NTMSS.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
          <TEI xmlns="http://www.tei-c.org/ns/1.0">
          <teiHeader>
              <fileDesc>
                <titleStmt>
                  <title type="document" n="01">01</title>
                </titleStmt>
                <publicationStmt>
                  <publisher><name type="org">The Institut für neutestamentliche Textforschung</name></publisher>
                  <availability><p>
          <![CDATA[
          (C) 2024 Institut für Neutestamentliche Textforschung.
          ]]>
          </p><p> <![CDATA[
          This work is licensed under a <a rel="license" target="_blank" href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 Unported License<br/><span style="float:right;"><img alt="Creative Commons License" style="border-width:0" src="https://licensebuttons.net/l/by/4.0/80x15.png" /></span></a>
          ]]>
          </p><p> <![CDATA[

          ]]>
          </p></availability>
                </publicationStmt>
          <sourceDesc>
                  <msDesc>
                          <msIdentifier>
                      <country>United Kingdom</country>
                      <settlement>London</settlement>
                      <repository>British Library</repository>
                      <idno>Add. 43725</idno>
                    </msIdentifier>
                  </msDesc>
                </sourceDesc>
          </fileDesc>
              <profileDesc>
                <langUsage>
                  <language ident="grc"></language>
                </langUsage>
                <handNotes>
                  <handNote>
                    <listWit>
                      <witness xml:id="firsthand"></witness>
          <witness xml:id="corrector1"></witness>
          </listWit>
                  </handNote>
                </handNotes>
              </profileDesc>
            </teiHeader>
          <text xml:lang="grc"><body>
          <div type="book" n="B03">
            <div type="chapter" n="B03K1">
              <ab n="B03K1V1" xml:id="Luke.1.1.P570.I1">
                <w>επειδηπερ</w> <w>πολλοι</w><lb/>
                <app>
                  <rdg type="orig" hand="firsthand">
                    <w>επεχειλησαν</w>
                  </rdg>
                  <rdg type="corr" hand="corrector1">
                    <w>επεχειρησαν</w>
                  </rdg>
                </app>
                <w>ανα<lb break="no"/>ταξασθαι</w> <w>διηγησιν</w><lb/>
                <w>περι</w> <w>των</w> <w>πεπλη<lb break="no"/>ροφορημενων</w><lb/>
                <w>εν</w> <w>ημιν</w> <w>πραγματων</w><lb/>
              </ab>
            </div>
          </div>
          </body>
          </text>
          </TEI>"""
        self.demo_XML_nominem_sacrum = """<?xml version="1.0" encoding="utf-8"?>
        <?xml-stylesheet type="text/xsl" href="NTPapyri.xsl"?>
        <?xml-model href="TEI-NTMSS.rng" type="application/xml" 
          schematypens="http://relaxng.org/ns/structure/1.0"?>
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
          <teiHeader>
            <fileDesc>
              <titleStmt>
                <title type="document" n="05">05</title>
              </titleStmt>
              <publicationStmt>
                <publisher>
                  <name type="org">The Institut für neutestamentliche Textforschung</name>
                </publisher>
                <availability>
                  <p><![CDATA[(C) 2024 Institut für Neutestamentliche Textforschung.]]></p>
                  <p><![CDATA[This work is licensed under a 
                    <a rel="license" target="_blank" 
                      href="https://creativecommons.org/licenses/by/4.0/">
                      Creative Commons Attribution 4.0 Unported License
                      <br/>
                      <span style="float:right;">
                        <img alt="Creative Commons License" style="border-width:0" 
                          src="https://licensebuttons.net/l/by/4.0/80x15.png" />
                      </span>
                    </a>
                  ]]></p>
                  <p><![CDATA[]]></p>
                </availability>
              </publicationStmt>
              <sourceDesc>
                <msDesc>
                  <msIdentifier>
                    <country>United Kingdom</country>
                    <settlement>Cambridge</settlement>
                    <repository>Cambridge University Library</repository>
                    <idno>Ms. Nn. 2.41</idno>
                  </msIdentifier>
                </msDesc>
              </sourceDesc>
            </fileDesc>
            <profileDesc>
              <langUsage>
                <language ident="g-l"></language>
              </langUsage>
              <handNotes>
                <handNote>
                  <listWit>
                    <witness xml:id="firsthand"></witness>
                  </listWit>
                </handNote>
              </handNotes>
            </profileDesc>
          </teiHeader>
          <text xml:lang="grc">
            <body>
              <div type="book" n="B02">
                <div type="chapter" n="B02K1">
                  <ab n="B02K1V1" xml:id="Mark.1.1.P5850.I1">
                    <w>αρχη</w> <w>του</w> <w>ευαγγελιου</w> 
                    <w><abbr type="nomSac"><hi rend="overline">ιηυ</hi></abbr></w> 
                    <w><abbr type="nomSac"><hi rend="overline">χρυ</hi></abbr></w> 
                    <w>υιου</w> 
                    <w><abbr type="nomSac"><hi rend="overline">θυ</hi></abbr></w><lb/>
                  </ab>
                </div>
              </div>
            </body>
          </text>
        </TEI>"""
        self.demo_XML_unclear = """<?xml version="1.0" encoding="utf-8"?>
          <?xml-stylesheet type="text/xsl" href="NTPapyri.xsl"?>
          <?xml-model href="TEI-NTMSS.rng" type="application/xml" 
            schematypens="http://relaxng.org/ns/structure/1.0"?>
          <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
              <fileDesc>
                <titleStmt>
                  <title type="document" n="05">05</title>
                </titleStmt>
                <publicationStmt>
                  <publisher>
                    <name type="org">The Institut für neutestamentliche Textforschung</name>
                  </publisher>
                  <availability>
                    <p><![CDATA[(C) 2024 Institut für Neutestamentliche Textforschung.]]></p>
                    <p><![CDATA[This work is licensed under a 
                      <a rel="license" target="_blank" 
                        href="https://creativecommons.org/licenses/by/4.0/">
                        Creative Commons Attribution 4.0 Unported License
                        <br/>
                        <span style="float:right;">
                          <img alt="Creative Commons License" style="border-width:0" 
                            src="https://licensebuttons.net/l/by/4.0/80x15.png" />
                        </span>
                      </a>
                    ]]></p>
                    <p><![CDATA[]]></p>
                  </availability>
                </publicationStmt>
                <sourceDesc>
                  <msDesc>
                    <msIdentifier>
                      <country>United Kingdom</country>
                      <settlement>Cambridge</settlement>
                      <repository>Cambridge University Library</repository>
                      <idno>Ms. Nn. 2.41</idno>
                    </msIdentifier>
                  </msDesc>
                </sourceDesc>
              </fileDesc>
              <profileDesc>
                <langUsage>
                  <language ident="g-l"></language>
                </langUsage>
                <handNotes>
                  <handNote>
                    <listWit>
                      <witness xml:id="firsthand"></witness>
                    </listWit>
                  </handNote>
                </handNotes>
              </profileDesc>
            </teiHeader>
            <text xml:lang="grc">
              <body>
                <div type="book" n="B04">
                  <div type="chapter" n="B04K1">
                    <ab n="B04K1V4" xml:id="John.1.4.P2100.I1">
                      <w>εν</w> <w>αυτω</w><lb/>
                      <w>ζωη</w> <w>εστ<unclear>ιν</unclear></w><pc>·</pc> 
                      <w>και</w> <w>η</w> <w>ζωη</w> <w>ην</w> <w>το</w> 
                      <w>φως</w> <w>των</w> <w>ανθρωπω<unclear>ν</unclear></w><lb/>
                    </ab>
                  </div>
                </div>
              </body>
            </text>
          </TEI>
          """

    def test_parse_manuscript_content(self):
        """Tests that filling out the database works as expected.
        """
        title, content = parse_manuscript(self.demo_XML,
                                          book_id="B03",
                                          use_reconstructed=True,
                                          variant="orig")
        self.assertEqual(
            title,
            "01")
        self.assertEqual(
            content,
            {'1': {'1': 'επειδηπερ πολλοι επεχειλησαν αναταξασθαι'
                   ' διηγησιν περι των πεπληροφορημενων εν ημιν πραγματων '}}
        )

    def test_parse_manuscript_nominem_sacrum(self):
        """Tests that parsing a manuscript with a nominem sacrum behaves as expected.
        """
        title, content = parse_manuscript(self.demo_XML_nominem_sacrum,
                                          book_id="B02",
                                          use_reconstructed=True,
                                          variant="orig")
        self.assertEqual(
            title,
            "05")
        self.assertEqual(
            content,
            {'1': {'1': "αρχη του ευαγγελιου ιηυ χρυ υιου θυ "}}
        )

    def test_parse_manuscript_unclear_reconstructed(self):
        """Tests that parsing a manuscript with an unclear tag and the reconstructed flag
        works as expected.
        """
        title, content = parse_manuscript(self.demo_XML_unclear,
                                          book_id="B04",
                                          use_reconstructed=True,
                                          variant="orig")
        self.assertEqual(
            title,
            "05")
        self.assertEqual(
            content,
            {'1': {'4': 'εν αυτω ζωη εστιν και η ζωη ην το φως των ανθρωπων '}}
        )

    def test_parse_manuscript_reconstructed(self):
        """Tests that parsing a manuscript with the reconstructed flag works as expected.
        """
        title, content = parse_manuscript(self.demo_XML_unclear,
                                          book_id="B04",
                                          use_reconstructed=False,
                                          variant="orig")
        self.assertEqual(
            title,
            "05")
        self.assertEqual(
            content,
            {'1': {'4': 'εν αυτω ζωη εστ και η ζωη ην το φως των ανθρωπω '}}
        )


if __name__ == "__main__":
    unittest.main()
