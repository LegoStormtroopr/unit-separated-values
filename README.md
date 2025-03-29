USV - Unit Separated Variables

# Abstract

This specfication defines a control-code based format for storing text-based data files in an unambigious way using ASCII or Unicode Control Characters in a semantic way.

This exists as an alternative to other text data formats, such as Comma-Separated Variables (CSV) and Tab-Separated Variables that solves three main problems with
1. USV files don't require escaping of separator characters within data values
2. USV files can include metadata, without interupting the data
3. USV files can include multiple data tables of differing sizes

# Table of Contents

# Introduction

## Purpose

Delimited text-based tabular-data formats, such as comma-separated values (CSV) or tab-separated values (TSV), or other structures such as JSON-Lines (JSON-L) are ubiquitous for sharing of structured, tabular data. Text-based formats have many advantages over spreadsheet formats or binary formats, in that they do not require specialised tools to view, are easy to read in text editors and terminal environments, and are (relatively) easy to parse programatically.

However, formats that used hierarchical data structures (eg. JSON) may not be suitable for tabular data or may not be easy for humans to read (eg. XML). Additionally, the use of common characters for delimiters causes issues with escaping, especially in instances where there is no formal specification for quoting or escaping. This is especially difficult with CSVs, where there are no formal rules for treating quotes or commas, and different processors may parse these differently. 

For data to make sense, it is also required that data has annotations that provide context to the data, this can include descriptive metadata that talks about what data is, how it was collected and how it can be used, or structural metadata about data types and codes used with the data.

Simple text formats, such as CSVs or TSVs also do not include a way to annotate a data file without breaking the tablular structure, and common conventions are for a single cell entry in first lines, last lines. Similarly JSON files do not include the ability to add comments, so metadata keys may be used in some instances but again these require schema files to describe the structure of the data.

Alternative common methods for annotating data may be supplementary files, either send along side or archived (zipped) with the data. However, the risk again is that as data is send between systems metadata data information may not be attached and important human context about the data is lost.

Finally, existing text-based tabular data formats, such as CSV or TSV cannot include multiple data tables within a single file. With again means that data that should be interpretted together may be lost during processing.

## Proposal

The ASCII character set has for a long time included data delimiters for structuring data, but as these are in the non-printable range, users are not familar with these.

## Requirements

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
   document are to be interpreted as described in RFC 2119 [https://datatracker.ietf.org/doc/html/rfc2119].

   An implementation is not compliant if it fails to satisfy one or more
   of the MUST or REQUIRED level requirements for the protocols it
   implements. An implementation that satisfies all the MUST or REQUIRED
   level and all the SHOULD level requirements for its protocols is said
   to be "unconditionally compliant"; one that satisfies all the MUST
   level requirements but not all the SHOULD level requirements for its
   protocols is said to be "conditionally compliant."

### Terminology

* annotations - details about data
* Group separator - Unicode U+001D or ASCII Control Code 29
* Record separator - Unicode U+001E or ASCII Control Code 30
* Unit separator - Unicode U+001F or ASCII Control Code 31

# Logical structure

File has heading
File can have tables
tables have rows
rows have cells

# File format

USV files MUST be encoded as either UTF-8 or ASCII, however for interoperability UTF-8 is preferred.

# File annotations

# Data table structure

## Tables (Groups)

### Starting a table

### Ending a table

A Table MUST be closed under one of the following three conditions
1. End of File - when a file is terminated the table is interpretted as ended, and the unit, record and group are al terminated.
2. New Group Separator 
3. U+0017	

### Presentation

## Records

### Starting a row

### Ending a row

### Presentation

## Unit

### Starting a record

### Ending a record

### Presentation

# Embedded USVs


## Examples


# Reserved Characters

* File Separator - Unicode U+001C ASCII Control Code 28 
* 

# Notes:

Python splits on groups, records, units
https://docs.python.org/3/library/stdtypes.html#str.splitlines
