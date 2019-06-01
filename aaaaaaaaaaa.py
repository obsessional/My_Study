# -*- coding:utf-8 -*-
#!/usr/bin/python3
import xml.sax

myxml = """
<?xml version="1.0" encoding="utf-8"?>
<collection shelf="New Arrivals">
<movie title="Enemy Behind">
  <type>love中国</type>
  <format>DVD</format>
  <year>2003</year>
  <rating>PG</rating>
  <stars>10</stars>
  <description>Talk about a US-Japan war</description>
</movie>
<movie title="Transformers">
  <type>Anime, Science Fiction</type>
  <format>DVD</format>
  <year>1989</year>
  <rating>R</rating>
  <stars>8</stars>
  <description>A schientific fiction</description>
</movie>
</collection>
"""

class MovieHandler( xml.sax.ContentHandler ):
  def __init__(self):
    self.CurrentData = ""
    self.type = ""
    self.format = ""
    self.year = ""
    self.rating = ""
    self.stars = ""
    self.description = ""
  # 元素开始调用
  def startElement(self, tag, attributes):
    self.CurrentData = tag
    if tag == "movie":
      print ("*****Movie*****")
      title = attributes["title"]
      print ("Title:", title)
  # 元素结束调用
  def endElement(self, tag):
    if self.CurrentData == "type":
      print ("Type:", self.type)
    elif self.CurrentData == "format":
      print ("Format:", self.format)
    elif self.CurrentData == "year":
      print ("Year:", self.year)
    elif self.CurrentData == "rating":
      print ("Rating:", self.rating)
    elif self.CurrentData == "stars":
      print ("Stars:", self.stars)
    elif self.CurrentData == "description":
      print ("Description:", self.description)
    self.CurrentData = ""
  # 读取字符时调用
  def characters(self, content):
    if self.CurrentData == "type":
      self.type = content
    elif self.CurrentData == "format":
      self.format = content
    elif self.CurrentData == "year":
      self.year = content
    elif self.CurrentData == "rating":
      self.rating = content
    elif self.CurrentData == "stars":
      self.stars = content
    elif self.CurrentData == "description":
      self.description = content
if ( __name__ == "__main__"):
  # 创建一个 XMLReader
  parser = xml.sax.make_parser()
  # turn off namepsaces
  parser.setFeature(xml.sax.handler.feature_namespaces, 0)
  # 重写 ContextHandler
  Handler = MovieHandler()
  parser.setContentHandler( Handler )
  parser.parse("myxml")
