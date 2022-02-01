# Parsing Course Info for NIT Kurukshetra

## Overview

This repository houses code for a small Python script to convert the course info found [here](https://nitkkr.ac.in/sub_courses.php?id=283&id3=92) into a JSON file suitable for usage anywhere it's needed (provided all the PDFs are converted to text firsthand)

The code is fairly messy and does need to be cleaned up, and the output itself is unreliable as the PDF to text conversion is not perfect. The source material is also fairly inconsistent when it comes to key words used, sometimes using synonyms (instead of writing "reference books", they sometimes write "suggested books").

Hence care should be used while using the tool, and it is strongly recommended to go through the output once.

The tool can automatically detect certain unnecessary lines in the input (lines with just a newline character, ones with just ---, etc.) but it's not perfect.

## Requirements

No external modules are used; the standard packages are enough

## Usage

```bash
python savetojson.py path/to/txtfile.txt
```
