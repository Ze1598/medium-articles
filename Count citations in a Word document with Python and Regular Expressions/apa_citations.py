"""
Citation examples used in the sample text (random authors and titles with random dates)
(Sabbagh, 2009)
(Sabbagh, n.d.)
(Sabbagh, 2010a)
(Sabbagh, 2010b)
(Qianyi Gu & Sumner, 2006)
(Despotovic-Zrakic et al., 2012)
(Anonymous, 2010)
(Anonymous, n.d.)
(“Barcelona to Ban Burqa,” 2010)
"""
import docx2txt as docx
import re

# Open the document
text = docx.process("lorem_sample.docx")
# Specifiy a very large number so that each `replace()` call catches\
# all stylized double quotes
num_replaces = 100000000
# Replace stylized doubled quotes by the default double quotes
# https://www.w3schools.com/charsets/ref_utf_punctuation.asp
text = text.replace('“', '"', num_replaces).replace('”', '"', num_replaces).replace(
    '„', '"', num_replaces).replace('‟', '"', num_replaces)

# Text between double quotes: https://stackoverflow.com/a/378447/9263761
# Pattern to find all types of citations
pattern = r'\(([^"\)]*|\bAnonymous\b|"[^"\)]*")(, )([\d]+|n\.d\.|[\d]+[\w])\)'
"""
\( -> opening parentheses
([^"\)]*|\bAnonymous\b|"[^"\)]*") -> author (can be 1+ authors (single author, two authors or more, "et al."), an anonymous author (identified as Anonymous) or a post/article without author (only a quotation of the title))
(, ) -> comma and space that separate the author and the date
([\d]+|n\.d\.|[\d]+[\w]) -> date (can be a year, a missing date (n.d.) or a year with a letter (multiple publications of the same author in the same year))
\) -> closing parentheses
"""
# Try to find matches (returned as an iterator of matches)
results = re.finditer(pattern, text)

# Build a list with the citations found by looping through the matches
# Each match has the first and last indices of the match, relative to the original string
citations = [text[match.start(): match.end()] for match in results]
print("All citations found:", len(citations))
[print(i) for i in citations]
print()
print()

# Remove duplicate citations
unique_citations = list(set(citations))
print("Unique citations:", len(unique_citations))
[print(i) for i in unique_citations]
