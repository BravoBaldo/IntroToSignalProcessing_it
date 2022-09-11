# IntroToSignalProcessing_it

This is the first draft of the translation of the book "Pragmatic Introduction to Signal Processing" by prof. Tom O'Haver
(https://terpconnect.umd.edu/~toh/spectrum/TOC.html)
...With some experiments for .tex conversion.

## Tools used:
* [OmegaT v.4.3.2](https://omegat.org) - (but with [Okapi Filters For OmegaT-1.7-1.39](https://okapiframework.org/wiki/index.php/Okapi_Filters_Plugin_for_OmegaT)).
* [Notepad++](https://notepad-plus-plus.org).
* [Dillinger](https://dillinger.io) - an online Markdown editor/viewer.
* [tagwipe](http://185.13.37.79/?q=node/35) - cleaner for Word documents
* [docx2tex](https://github.com/transpect/docx2tex/releases) - Convert .docx to .tex
* [gif2apng](http://gif2apng.sourceforge.net/) - Convert .gif in something else

## Conversion Process

### Download org files (English):
Download the whole site: [Spectrum zip](https://terpconnect.umd.edu/~toh/spectrum/SPECTRUM.zip) - contains almost all required images
[English version](https://terpconnect.umd.edu/~toh/spectrum/IntroToSignalProcessing2021.docx) - Usually more updated than the one in Spectrum.zip
    [English .docx](https://terpconnect.umd.edu/~toh/spectrum/IntroToSignalProcessing2021.docx)
    (https://terpconnect.umd.edu/~toh/spectrum/SPECTRUM.zip)
    Unzip it in a directory
    
### Modifications of the English .docx:
* Centre the title!
* Remove dropcaps (there is a word-macro for this) they will be restored after...
* Replace all "^s" with " "		Unbrekable spaces to normal spaces
* Replace all "^l" with "^p"			Manual row breaks
* Replace all "^m" with ""			Manual page breaks
* Replace all "^u8208" with "-"      Some strange Armenian minus
* Replace all "^u8203" with ""       A few strange null characters

### Cleaning English .docx
(tagwipe:	http://185.13.37.79/?q=node/35)

### Translate it
(OmegaT)

### Conversion to Tex ()
...\docx2tex\d2t IntroToSignalProcessing2021.docx ..\..\IntroToSignalProcessing2021.csv .\Out

### Images conversions
Tex does not handle .gif images
Convert all .gif in .png in Spectrum directory and in docx2tex conversion directory (usually ...\IntroToSignalProcessing2021.docx.tmp\word\media)
for %f in (*.gif) do gif2apng %f %~nxf.png
This was already done in the directory "GifPngImages"

### Manual pre-processing
.tex Modifications
Replace first part (until '\tableofcontents') with contents of IntroToSignalProcessing_Head.tex
Replace last part (from row after "\chapter{References" to the end before "\end{document}") with "\input{../../IntroToSignalProcessing_Tail.tex}"
Adjust in .tex file paths in "\graphicspath{..."

### Adjust Pyton Script
(In ...\CBookSignalProcessing\Python\Apitsp\PreProcessing.py)
change path for Spectrum directory
Change path of .tex converted file
Change path of LatexBook

### Automatic pre-processing with Pyton Script
Execute Python script, a ..._AUTO.tex will be produced; we will work on it

### Pdf generation
"pdflatex -halt-on-error FileName_AUTO.TEX"

## ToDo
* At least a first revision of the Italian text!
* In the Italian version images and pages are not well formatted
* Translation maintenance.
* Conversion in Tex and/or pdf
