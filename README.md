# Resume-Ranking

### About
This program basically ranks documents based on their textual similarities. The algorithm used are the BM25 families which include:
BM25Adpt
BM25okapi
BM25L
BM25Plus
BM25T

The file Production/Run.py, contains the calling code for processing the entire documents and storing them to pickle file for easy access. Each time any new document is added, this file should be run again.

The Play-Ground folder contains the jupyter Notebook for interacting freely and experimenting with the codes used for building the software.

The folder Data/Resumes contains the documents used. Feel free to add or remove from it.


### Packages to be installed
textract
tika
os
glob
pickle
shutil
bs4
re
nltk
sklearn
operator


### Usage
There are two ways to use this software.
You can rank the documents by specifying a document id, the software ranks all other documents based on their textual similarity to the document with the id chosen
You can rank the documents by typing in a search query, the software ranks all documents based on their textual similarity to the query specified in Search field.

There is an option to input the number of words of each document you want the software to display.

You can also specify the number of documents you want to be displayed.

