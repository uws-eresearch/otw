from ImageConverterPlugin import ImageConverterPlugin
import sys
sys.path.append("..")
import dispatcher
import unittest
import logging
import re
import os
import shutil
import json

class TestImageConverter(unittest.TestCase):

    def setUp(self):
        self.converter = ImageConverterPlugin()
        self.config = dispatcher.get_config()
        self.logger = dispatcher.get_logger(self.config)
        self.converter.initialize(self.logger, self.config)    
        self.actions = dispatcher.FileActionStore()
        self.actions.addActions(self.converter.actions)    
       
        

    def test_rdfToDictbjects(self):
        self.converter.rdfToDict(rdfImage1)
        (_,subject) = self.converter.meta["Subject"]
        subjects = subject.split(", ")
        expectedSubjects = ["People/Florence", "Vinyl"]
        self.assertEqual(subjects.sort(),expectedSubjects.sort())
        
    def test_rdfToDict(self):
        self.converter.rdfToDict(rdfImage1)
        self.converter.dictToTable()
        self.assertEqual(self.converter.body.count("<tr>"),86)
        
    def test_exiftool(self):
        """
        Simple Smoke test to check that everything is actually happening
        """
        to_do = dispatcher.ActionableFile("ImageConverterPlugin_tests/image.png", self.logger, self.config, self.actions)
        try:
            shutil.rmtree(to_do.dirname)
        except:
            pass
        to_do.act()
        assert(os.path.exists(to_do.indexHTML))
        meta = json.load(open(to_do.metaJSON))
        self.assertEqual(meta["dc:title"], "image.png")
                 
        

rdfImage1 = """<?xml version='1.0' encoding='UTF-8'?>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>

<rdf:Description rdf:about='/home/pt/Documents/PC300326.JPG'
  xmlns:et='http://ns.exiftool.ca/1.0/' et:toolkit='Image::ExifTool 8.60'
  xmlns:ExifTool='http://ns.exiftool.ca/ExifTool/1.0/'
  xmlns:System='http://ns.exiftool.ca/File/System/1.0/'
  xmlns:File='http://ns.exiftool.ca/File/1.0/'
  xmlns:JFIF='http://ns.exiftool.ca/JFIF/JFIF/1.0/'
  xmlns:IFD0='http://ns.exiftool.ca/EXIF/IFD0/1.0/'
  xmlns:ExifIFD='http://ns.exiftool.ca/EXIF/ExifIFD/1.0/'
  xmlns:Olympus='http://ns.exiftool.ca/MakerNotes/Olympus/1.0/'
  xmlns:InteropIFD='http://ns.exiftool.ca/EXIF/InteropIFD/1.0/'
  xmlns:PrintIM='http://ns.exiftool.ca/PrintIM/PrintIM/1.0/'
  xmlns:IFD1='http://ns.exiftool.ca/EXIF/IFD1/1.0/'
  xmlns:XMP-x='http://ns.exiftool.ca/XMP/XMP-x/1.0/'
  xmlns:XMP-xmp='http://ns.exiftool.ca/XMP/XMP-xmp/1.0/'
  xmlns:XMP-dc='http://ns.exiftool.ca/XMP/XMP-dc/1.0/'
  xmlns:IPTC='http://ns.exiftool.ca/IPTC/IPTC/1.0/'
  xmlns:Photoshop='http://ns.exiftool.ca/Photoshop/Photoshop/1.0/'
  xmlns:Composite='http://ns.exiftool.ca/Composite/1.0/'>
 <ExifTool:ExifToolVersion>8.60</ExifTool:ExifToolVersion>
 <System:FileName>PC300326.JPG</System:FileName>
 <System:Directory>/home/pt/Documents</System:Directory>
 <System:FileSize>463 kB</System:FileSize>
 <System:FileModifyDate>2014:01:09 07:56:10+11:00</System:FileModifyDate>
 <System:FilePermissions>rw-r--r--</System:FilePermissions>
 <File:FileType>JPEG</File:FileType>
 <File:MIMEType>image/jpeg</File:MIMEType>
 <File:ExifByteOrder>Little-endian (Intel, II)</File:ExifByteOrder>
 <File:CurrentIPTCDigest>4543d1375ecee103ceeb7db3770bf688</File:CurrentIPTCDigest>
 <File:ImageWidth>768</File:ImageWidth>
 <File:ImageHeight>1024</File:ImageHeight>
 <File:EncodingProcess>Baseline DCT, Huffman coding</File:EncodingProcess>
 <File:BitsPerSample>8</File:BitsPerSample>
 <File:ColorComponents>3</File:ColorComponents>
 <File:YCbCrSubSampling>YCbCr4:4:0 (1 2)</File:YCbCrSubSampling>
 <JFIF:JFIFVersion>1.01</JFIF:JFIFVersion>
 <JFIF:ResolutionUnit>None</JFIF:ResolutionUnit>
 <JFIF:XResolution>1</JFIF:XResolution>
 <JFIF:YResolution>1</JFIF:YResolution>
 <IFD0:ImageDescription>OLYMPUS DIGITAL CAMERA         </IFD0:ImageDescription>
 <IFD0:Make>OLYMPUS IMAGING CORP.</IFD0:Make>
 <IFD0:Model>E-M5</IFD0:Model>
 <IFD0:XResolution>350</IFD0:XResolution>
 <IFD0:YResolution>350</IFD0:YResolution>
 <IFD0:ResolutionUnit>inches</IFD0:ResolutionUnit>
 <IFD0:Software>Version 1.6</IFD0:Software>
 <IFD0:ModifyDate>2014:01:09 08:00:59</IFD0:ModifyDate>
 <IFD0:Artist>Picasa</IFD0:Artist>
 <IFD0:YCbCrPositioning>Co-sited</IFD0:YCbCrPositioning>
 <IFD0:Copyright></IFD0:Copyright>
 <ExifIFD:ExposureTime>1/80</ExifIFD:ExposureTime>
 <ExifIFD:FNumber>10.0</ExifIFD:FNumber>
 <ExifIFD:ExposureProgram>Aperture-priority AE</ExifIFD:ExposureProgram>
 <ExifIFD:ISO>1000</ExifIFD:ISO>
 <ExifIFD:SensitivityType>Standard Output Sensitivity</ExifIFD:SensitivityType>
 <ExifIFD:ExifVersion>0230</ExifIFD:ExifVersion>
 <ExifIFD:DateTimeOriginal>2013:12:30 16:31:54</ExifIFD:DateTimeOriginal>
 <ExifIFD:CreateDate>2013:12:30 16:31:54</ExifIFD:CreateDate>
 <ExifIFD:ComponentsConfiguration>Y, Cb, Cr, -</ExifIFD:ComponentsConfiguration>
 <ExifIFD:ExposureCompensation>0</ExifIFD:ExposureCompensation>
 <ExifIFD:MaxApertureValue>1.7</ExifIFD:MaxApertureValue>
 <ExifIFD:MeteringMode>Multi-segment</ExifIFD:MeteringMode>
 <ExifIFD:LightSource>Unknown</ExifIFD:LightSource>
 <ExifIFD:Flash>Auto, Did not fire</ExifIFD:Flash>
 <ExifIFD:FocalLength>20.0 mm</ExifIFD:FocalLength>
 <ExifIFD:UserComment></ExifIFD:UserComment>
 <ExifIFD:FlashpixVersion>0100</ExifIFD:FlashpixVersion>
 <ExifIFD:ColorSpace>sRGB</ExifIFD:ColorSpace>
 <ExifIFD:ExifImageWidth>768</ExifIFD:ExifImageWidth>
 <ExifIFD:ExifImageHeight>1024</ExifIFD:ExifImageHeight>
 <ExifIFD:FileSource>Digital Camera</ExifIFD:FileSource>
 <ExifIFD:CustomRendered>Normal</ExifIFD:CustomRendered>
 <ExifIFD:ExposureMode>Auto</ExifIFD:ExposureMode>
 <ExifIFD:WhiteBalance>Auto</ExifIFD:WhiteBalance>
 <ExifIFD:DigitalZoomRatio>1</ExifIFD:DigitalZoomRatio>
 <ExifIFD:SceneCaptureType>Standard</ExifIFD:SceneCaptureType>
 <ExifIFD:GainControl>High gain up</ExifIFD:GainControl>
 <ExifIFD:Contrast>Normal</ExifIFD:Contrast>
 <ExifIFD:Saturation>Normal</ExifIFD:Saturation>
 <ExifIFD:Sharpness>Normal</ExifIFD:Sharpness>
 <ExifIFD:ImageUniqueID>f32ac9ce66259d64321abe602559599d</ExifIFD:ImageUniqueID>
 <ExifIFD:LensInfo>20mm f/1.7</ExifIFD:LensInfo>
 <ExifIFD:LensModel>LUMIX G 20/F1.7</ExifIFD:LensModel>
 <Olympus:SpecialMode>Normal, Sequence: 0, Panorama: (none)</Olympus:SpecialMode>
 <Olympus:CameraID>OLYMPUS DIGITAL CAMERA         </Olympus:CameraID>
 <InteropIFD:InteropIndex>R98 - DCF basic file (sRGB)</InteropIFD:InteropIndex>
 <InteropIFD:InteropVersion>0100</InteropIFD:InteropVersion>
 <InteropIFD:RelatedImageWidth>4608</InteropIFD:RelatedImageWidth>
 <InteropIFD:RelatedImageHeight>3456</InteropIFD:RelatedImageHeight>
 <PrintIM:PrintIMVersion>0300</PrintIM:PrintIMVersion>
 <IFD1:Compression>JPEG (old-style)</IFD1:Compression>
 <IFD1:XResolution>72</IFD1:XResolution>
 <IFD1:YResolution>72</IFD1:YResolution>
 <IFD1:ResolutionUnit>inches</IFD1:ResolutionUnit>
 <IFD1:ThumbnailOffset>1910</IFD1:ThumbnailOffset>
 <IFD1:ThumbnailLength>8310</IFD1:ThumbnailLength>
 <XMP-x:XMPToolkit>XMP Core 5.1.2</XMP-x:XMPToolkit>
 <XMP-xmp:ModifyDate>2014:01:09 08:00:59+11:00</XMP-xmp:ModifyDate>
 <XMP-dc:Creator>Picasa</XMP-dc:Creator>
 <XMP-dc:Subject>
  <rdf:Bag>
   <rdf:li>People/Florence</rdf:li>
   <rdf:li>Vinyl</rdf:li>
  </rdf:Bag>
 </XMP-dc:Subject>
 <IPTC:EnvelopeRecordVersion>4</IPTC:EnvelopeRecordVersion>
 <IPTC:CodedCharacterSet>UTF8</IPTC:CodedCharacterSet>
 <IPTC:ApplicationRecordVersion>4</IPTC:ApplicationRecordVersion>
 <IPTC:Keywords>
  <rdf:Bag>
   <rdf:li>People/Florence</rdf:li>
   <rdf:li>Vinyl</rdf:li>
  </rdf:Bag>
 </IPTC:Keywords>
 <Photoshop:IPTCDigest>4543d1375ecee103ceeb7db3770bf688</Photoshop:IPTCDigest>
 <Composite:Aperture>10.0</Composite:Aperture>
 <Composite:ImageSize>768x1024</Composite:ImageSize>
 <Composite:ShutterSpeed>1/80</Composite:ShutterSpeed>
 <Composite:ThumbnailImage>(Binary data 8310 bytes, use -b option to extract)</Composite:ThumbnailImage>
 <Composite:FocalLength35efl>20.0 mm</Composite:FocalLength35efl>
 <Composite:LightValue>9.6</Composite:LightValue>
</rdf:Description>
</rdf:RDF>

"""

if __name__ == '__main__':
    unittest.main()
