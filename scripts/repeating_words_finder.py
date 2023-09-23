import os
import re
import sys
import argparse
import PyPDF2
from docx import Document

# Constants
DEFAULT_MIN_WORD_LEN = 1

# CustomRangeAction
class CustomRangeAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        # Dynamically generate a concise metavar from choices
        if kwargs.get('choices') is not None:
            first, last = kwargs['choices'][0], kwargs['choices'][-1]
            kwargs['metavar'] = f"{{{first}-{last}}}"
        super(CustomRangeAction, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        # This is the core method for the action. We're just using the default behavior here.
        setattr(namespace, self.dest, values)

class FileExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        raise NotImplementedError("Subclasses must implement this method")

class PDFExtractor(FileExtractor):
    def extract(self):
        content = ""
        with open(self.file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                content += page.extract_text()
        return content

class TXTExtractor(FileExtractor):
    def extract(self):
        with open(self.file_path, 'r') as file:
            return file.read()

class DOCXExtractor(FileExtractor):
    def extract(self):
        doc = Document(self.file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

class DuplicateFinder:
    @staticmethod
    def find_repetitions(content, min_word_len=DEFAULT_MIN_WORD_LEN):
        # Tokenize content into words
        words = re.findall(r'\b\w+\b', content)
        # Convert to lowercase and filter based on the minimum word length
        words = [word.lower() for word in words if len(word) >= min_word_len]
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        repetitions = { word: count for word, count in sorted(word_count.items(), key=lambda item: item[1], reverse=True) if count > 1 }
        return repetitions

class MainScript:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Extract content from files and display duplicate words.")
        self.setup_arguments()

    def setup_arguments(self):
        self.parser.add_argument("file_path", help="Path to the input file (.txt, .pdf, .docx).")
        self.parser.add_argument("-l", "--min_word_len", type=int, choices=range(1, 101), default=DEFAULT_MIN_WORD_LEN, 
                                 help="Minimum word length to be considered (default is 1).", action=CustomRangeAction)
        self.parser.add_argument("-p", "--print_content", action="store_true", 
                                 help="Print the extracted content before showing repetitions.")

    def run(self):
        args = self.parser.parse_args()

        content = self._extract_content_from_file(args.file_path)

        # Print the content if needed
        if args.print_content:
            print("\nExtracted Content:\n", "-"*50, "\n", content, "\n", "-"*50, "\n")

        repetitions = DuplicateFinder.find_repetitions(content, args.min_word_len)
        self._display_results(repetitions, args.min_word_len)

    def _extract_content_from_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist.")
            sys.exit(1)

        file_extension = os.path.splitext(file_path)[1].lower()

        if os.path.splitext(file_path)[1].lower() == ".pdf":
            extractor = PDFExtractor(file_path)
        elif os.path.splitext(file_path)[1].lower() == ".txt":
            extractor = TXTExtractor(file_path)
        elif os.path.splitext(file_path)[1].lower() == ".docx":
            extractor = DOCXExtractor(file_path)
        else:
            print(f"Unsupported file type: {file_extension}")
            sys.exit(1)

        content = extractor.extract()
        return content

    def _display_results(self, repetitions, min_word_len):
        title_prefix = "" if min_word_len == DEFAULT_MIN_WORD_LEN else f"of min length {min_word_len}"
        print(f"Repetitions {title_prefix}:\n{repetitions}" if repetitions else "No repetitions found.")

if __name__ == "__main__":
    script = MainScript()
    script.run()
