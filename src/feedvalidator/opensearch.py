from validators import *
from logging import *
import re

class OpenSearchDescription(validatorBase):
  def validate(self):
    name=self.name.replace("opensearch_",'')
    if not "ShortName" in self.children:
      self.log(MissingElement({"parent":name, "element":"ShortName"}))
    if not "Description" in self.children:
      self.log(MissingElement({"parent":name, "element":"Description"}))
    if not "Url" in self.children:
      self.log(MissingElement({"parent":name, "element":"Url"}))

  def do_ShortName(self):
    return lengthLimitedText(16), noduplicates()
  def do_Description(self):
    return lengthLimitedText(1024), noduplicates()
  def do_Url(self):
    return Url()
  def do_Contact(self):
    return addr_spec()
  def do_Tags(self):
    return lengthLimitedText(256)
  def do_LongName(self):
    return lengthLimitedText(48)
  def do_Image(self):
    return Image()
  def do_Query(self):
    return Query()
  def do_Developer(self):
    return lengthLimitedText(64)
  def do_Attribution(self):
    return lengthLimitedText(256)
  def do_SyndicationRight(self):
    return SyndicationRight()
  def do_AdultContent(self):
    return AdultContent()
  def do_Language(self):
    return iso639()
  def do_InputEncoding(self):
    return Charset()
  def do_OutputEncoding(self):
    return Charset()

class Url(validatorBase):
  def getExpectedAttrNames(self):
    return [(None,attr) for attr in ['template', 'type', 'indexOffset',
      'pageOffset']]
  def prevalidate(self):
    self.validate_required_attribute((None,'template'), Template)
    self.validate_required_attribute((None,'type'), MimeType)
    self.validate_optional_attribute((None,'indexOffset'), Integer)
    self.validate_optional_attribute((None,'pageOffset'), Integer)

class Template(rfc2396_full):
  def validate(self):
    self.value = re.sub("{(\w+:?\w*\??)}",r'\1',self.value)
    rfc2396_full.validate(self)

class Image(text):
  def getExpectedAttrNames(self):
    return [(None,attr) for attr in ['height', 'width', 'type']]

class Query(validatorBase):
  def getExpectedAttrNames(self):
    return [(None,attr) for attr in ['role', 'title', 'totalResults',
      'searchTerms', 'count', 'startIndex', 'startPage', 'language',
      'inputEncoding', 'xutputEncoding', 'parameter']]

  def prevalidate(self):
    self.validate_required_attribute((None,'role'), QueryRole)
    self.validate_optional_attribute((None,'title'), lengthLimitedText(256))
    self.validate_optional_attribute((None,'title'), nonhtml)
    self.validate_optional_attribute((None,'totalResults'), nonNegativeInteger)
    self.validate_optional_attribute((None,'searchTerms'), UrlEncoded)
    self.validate_optional_attribute((None,'count'), nonNegativeInteger)
    self.validate_optional_attribute((None,'startIndex'), Integer)
    self.validate_optional_attribute((None,'startPage'), Integer)
    self.validate_optional_attribute((None,'language'), iso639)
    self.validate_optional_attribute((None,'inputEncoding'), Charset)
    self.validate_optional_attribute((None,'outputEncoding'), Charset)

class QueryRole(enumeration):
  error = InvalidLocalRole
  valuelist = ['request', 'example', 'related', 'correction', 'subset',
    'superset']
  def validate(self):
    if self.value.find(':')<0:
      enumeration.validate(self)
    else:
      pass # TBD: check for role extension

class UrlEncoded(validatorBase):
  def validate(self):
    from urllib import quote, unquote
    import re
    for value in self.value.split():
      value = re.sub('%\w\w', lambda x: x.group(0).lower(), value)
      if value != quote(unquote(value)):
        self.log(NotURLEncoded({}))
        break

class SyndicationRight(enumeration):
  error = InvalidValue
  valuelist = ['open','limited','private','closed']

class AdultContent(enumeration):
  error = InvalidValue
  valuelist = ['false', 'FALSE', '0', 'no', 'NO', 'true', 'TRUE', '1', 'yes', 'YES']