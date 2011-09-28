Walkthrough
===========

Site Structure Mapping
----------------------

The first step in automated testing is to identify all the content types and
how they can be structured.

Metadata about all types known to atapi are captured.

The root type (generally 'Plone Site') is visited first. Then all types allowed
in 'Plone Site' are visited. A depth first search is performed with some basic
loop detectiion (so no Folder -> Folder -> Folder -> infinity).

For each type that is visited information about the fields it has are collected.

Structure Building
------------------

The map generated in the previous step is used to create test content.

Each piece of content is created by looping over each field and 'fuzzing' its
contents. There are fuzzers registered for various types and for handling
various restrictions including solving regular expressions. Each piece of
content is validated against this schema (normally programmatic content
creation could bypass that) and then the content is created.

Content verification
--------------------

Each piece of content created by the structure building step is visited and checked
for obvious errors.

