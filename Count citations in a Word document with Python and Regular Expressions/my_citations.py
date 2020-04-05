"""
Citation examples:
("Learning Analytics - Definitions, Processes and Potential", p. 2)
("Wanted: A road map for understanding Integrated Learning Systems")
"""
import docx2txt as docx
import re

# Open the document
text = docx.process("my_lorem_sample.docx")
# Specifiy a very large number so that each `replace()` call catches\
# all stylized double quotes
num_replaces = 100000000
# Replace stylized doubled quotes by the default double quotes
# https://www.w3schools.com/charsets/ref_utf_punctuation.asp
text = text.replace('“', '"', num_replaces).replace('”', '"', num_replaces).replace(
    '„', '"', num_replaces).replace('‟', '"', num_replaces)

# Text between double quotes: https://stackoverflow.com/a/378447/9263761
# Pattern to find all cited titles (i.e., only looks up document titles\
# enclosed in double quotes with an opening parentheses before the first\
# quote)
pattern = r'\("[^"]*"'
"""
\( -> opening parentheses
"[^"]*" -> document title (title is enclosed by double quotes, and the title itself can't have double quotes)
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
