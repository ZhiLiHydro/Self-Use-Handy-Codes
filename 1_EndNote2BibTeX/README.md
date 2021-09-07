## 1_EndNote to BibTeX

### To run:

```
python endnote2bibtex.py
```

This code/GUI is to repair the unusable BibTeX keys (RN+number) exported directly from EndNote (I'm using EndNote X9). 

The keys after repairs follow similar rules as the ones exported from Google Scholar (firstauthorlastname+year+titlefirstword). 

It also 

1. adds letter suffixes to repeated keys (e.g. peter1998researcha, peter1998researchb), 

2. adds curly brackets to preserve original title and journal names, and 

3. cleans DOI.

It only handles already-formatted BibTeX files exported directly from EndNote, and may report errors when trying to convert arbitrary BibTeX files.

### Example:

`My EndNote Library.txt` is the raw output exported from EndNote X9. It contains the search result in Web of Science Core Collection database with these criteria: (`year=2019` AND `journal=JFM` AND `title>=turbulence`) OR (`year=2018,2019` AND `journal=WRR` AND `title>=flood`))

`MyEndNoteLibrary.bib` is the repaired output.

### Before repair:

<img src="https://github.com/ZhiLiHydro/Self-Use-Handy-Codes/blob/master/1_EndNote2BibTeX/before.png">

### After repair:

<img src="https://github.com/ZhiLiHydro/Self-Use-Handy-Codes/blob/master/1_EndNote2BibTeX/after.png">
