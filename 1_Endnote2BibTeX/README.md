### 1_Endnote to BibTeX

#### To run:

```
python endnote2bibtex.py
```

This code/GUI is to repair the unusable bibtex keys (RN+number) exported directly from Endnote. The keys after repairs follow similar rules as the ones exported from Google Scholar (firstauthorlastname+year+titlefirstword). It also adds letter suffixes to repeated keys (e.g. lee1998orangea, lee1998orangeb). It only handles already-formatted bibtex files exported directly from Endnote. It may report errors when trying to convert arbitrary bibtex files.

Example:

`My EndNote Library.txt` is the raw output exported from Endnote. It contains the search result in Web of Science Core Collection with these criterions: (`year=2019` AND `journal=JFM` AND `title>=turbulence`) OR (`year=2018,2019` AND `journal=WRR` AND `title>=flood`))

`MyEndNoteLibrary.bib` is the repaired output.
