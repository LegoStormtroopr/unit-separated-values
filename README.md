USV - Unit Separated Variables

# Abstract

This specfication defines a control-code based format for storing text-based data files in an unambigious way using ASCII or Unicode Control Characters in a semantic way.

This exists as an alternative to other text data formats, such as Comma-Separated Variables (CSV) and Tab-Separated Variables that solves three main problems with
1. USV files don't require escaping of separator characters within data values
2. USV files can include metadata, without interupting the data
3. USV files can include multiple data tables of differing sizes

# Table of Contents

# Introduction

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

## Reserved ASCII/Unicode Characters

### Reserved characters

* Data Link Escape - DLE - Unicode U+0010 or ASCII Control Code 16
* End of Transmission Block - ETB - Unicode U+001F or ASCII Control Code 23
* Group Separator - GS - Unicode U+001D or ASCII Control Code 29
* Record separator - RS -  Unicode U+001E or ASCII Control Code 30
* Unit separator - US - Unicode U+001F or ASCII Control Code 31

### Reserved for future use
* Start of Header - SOH - Unicode U+0001 or ASCII Control Code 1
* Shift Out - SO - Unicode U+000E or ASCII Control Code 14
* Shift In - SI - Unicode U+000F or ASCII Control Code 15
* Escape - ESC - Unicode U+001B or ASCII Control Code 27
* File Separator - FS - Unicode U+001C ASCII Control Code 28 

# File format

USV files MUST be encoded as either UTF-8 or ASCII, however for interoperability UTF-8 is recommended.

## Escaping of characters

Any reserved character may be escaped using the **Data Link Escape** character, conforming software then must treat the single following character as data.

# Data table structure

## Groups

A table is a data structure that consists of collections of observations of data.
It is analogous to a table of that contains rows of cells.

### Opening a group

A data table is opened via the **Group Separator** character.
Software implementing the USV Specification MUST interpret an unescaped **Group Separator** as opening a table.

### Closing a group

A Group MUST be closed under one of the following three conditions:

1. End of File - During streaming, when the end of file is reached the table MUST be interpretted as completed, and the unit, record and group are all terminated.
2. New **Group Separator** - During streaming, when an unescaped **Group Separator** is encountered, the current group MUST be interpretted as completed, and the unit, record and group are all terminated, with a new Group started.
3. End of Transmission Block (ETB) character (U+0017 or ASCII Control Code 23) - During streaming, when an unescaped **Group Separator** is encountered, the current  group MUST be interpretted as completed, and the unit, record and group are all terminated, with a new Group started.

For data integrity, it is encouraged that the last group in a file SHOULD be terminated with an End of Transmission Block. Absence of an ETB at the end of file MUST not be interpreted as a truncated file, but data users should consider it work checking.

Software implementing the USV Specification MUST include a "safe close" option when writing USV files, that closes each group with an End of Transmission character. Software implementing the USV must include a "safe close check" option that verifies if the final group has been safely closed.

## Records

A record is a collection of data points that relate to an observation. It is analogous to a row within a table that contains data.

### Opening a record

A record is opened via the **Record Separator** character.
Software implementing the USV Specification MUST interpret an unescaped **Record Separator** as opening a record.

### Closing a record

A Record MUST be closed under one of the following two conditions:

1. New **Record Separator** - During streaming, when an unescaped **Reecord Separator** is encountered, the current record MUST be interpretted as completed, and the unit and record are all terminated, with a new Record started.
2. Any condition that closes a group

### Presentation

Each record SHOULD be presented on its own line within a user interface. For example a row within a spreadsheet or a line within a text editor.

## Unit

A unit a logical object that contains single data value (or datum). It is analogous to a cell within a row of a table that contains data.

A unit can contain any non-reserved character, or any escaped reserved character, including whitespace or new lines.

### Opening a unit

A unit is opened via the **Unit Separator** character.
Software implementing the USV Specification MUST interpret an unescaped **Unit Separator** as opening a table.

### Closing a unit

A Unit MUST be closed under one of the following two conditions:

1. New **Unit Separator** - During streaming, when an unescaped **Unit Separator** is encountered, the current unit MUST be interpretted as completed, and the unit is terminated, with a new Unit started.
2. Any condition that closes a record or a group

### Presentation

Each unit SHOULD be presented within a single line, with a fixed width within a user interface. For example a cell within a spreadsheet or a fixed-width within a text editor. If user interface folding is supported, cells longer than a configured value SHOULD be presented as truncated until unfolded.

# Formal grammar

The ABNF grammar [2] appears as follows:

    file = *(TEXTDATA / group)

    group = groupannotation groupdata [ groupterminators ]
    groupannotation = TEXTDATA
    groupdata = 1*(RS record)
    groupterminators = ETB

    record = 1*(US unit)
    unit = (TEXTDATA / eGS / eRS / eUS)

    eGS = DLE GS ; Escaped Group Separator
    eRS = DLE RS ; Escaped Record Separator
    eUS = DLE US ; Escaped Unit Separator

    TEXTDATA =  %x20-21 / %x23-2B / %x2D-7E

    SOH = %x01 ; Start of Header
    DLE = %x10 ; Data Link Escape
    ETB = %x1F ; End of Transmission
    GS  = %x1D ; Group Separator
    RS  = %x1E ; Record separator
    US  = %x1F ; Unit separator

ABNF Validated using: https://author-tools.ietf.org/abnf

# USV Metadata

* File
 Starting Positions: list 

* Groups
 Starting Position
 MD5 Hash
 Num Rows


## Examples



# References

## Normative References

* Crocker, D. and P. Overell, "Augmented BNF for Syntax Specifications: ABNF", RFC 2234, November 1997.


# Notes:

Python splits on groups, records, units
https://docs.python.org/3/library/stdtypes.html#str.splitlines
