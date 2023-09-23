# HandyScripts
Collection of convenient multi-purpose Python scripts

## Featuring

1. **repeating_words_finder.py**: Analyses text document (can be of `txt`, `pdf` or `docx` format) and produces output if repeated words if they exist with the number of times they occur.
- Usage:
```   
usage: repeating_words_finder.py [-h] [-l {1-100}] [-p] file_path

Extract content from files and display duplicate words.

positional arguments:
  file_path             Path to the input file (.txt, .pdf, .docx).

optional arguments:
  -h, --help            show this help message and exit
  -l {1-100}, --min_word_len {1-100}
                        Minimum word length to be considered (default is 1).
  -p, --print_content   Print the extracted content before showing repetitions.
```
- Sample invokation & output:
```
python3 repeating_words_finder.py ~/SampleDoc.pdf -l 5
```
```
Repetitions of min length 5:
{'users': 3, 'commerce': 2, 'digital': 2, 'design': 2, 'solutions': 2, 'experience': 2, 'technical': 2, 'increase': 2, 'functional': 2}
```
