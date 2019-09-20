[![Build Status](https://travis-ci.org/rubys/feedvalidator.svg)](https://travis-ci.org/rubys/feedvalidator)

Some tests, and some functionality, will not be enabled unless a full set
of 32-bit character encodings are available through Python.

The package 'iconvcodec' provides the necessary codecs, if your underlying
operating system supports them. Its web page is at
<http://cjkpython.i18n.org/#iconvcodec>, and a range of packages are
provided.

Python 2.3.x is required, for its Unicode support.

To run with Docker:

```
docker build -t feedvalidator .
docker run -p 8080:80 feedvalidator
```
