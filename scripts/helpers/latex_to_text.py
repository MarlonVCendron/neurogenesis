import os
import re
import sys

# Add project root to path to allow importing 'params'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from params.general import latex_dir


def latex_to_text(latex_content):
    # Remove comments
    text = re.sub(r"%.*?\n", "\n", latex_content)

    # Remove inline math between $...$
    text = re.sub(r"\$.*?\$", "", text, flags=re.DOTALL)

    # Remove multi-line environments like figure, table, equation
    text = re.sub(
        r"\\begin\{(figure|table|equation|tabular|center|tikzpicture)\*?\}.*?\\end\{\1\*?\}",
        "",
        text,
        flags=re.DOTALL,
    )

    # Remove commands with one argument, keeping the argument's content
    # e.g., \section{Title} -> Title
    text = re.sub(
        r"\\(section|subsection|subsubsection|chapter|paragraph|subparagraph|textbf|textit|texttt|emph|textit|textbf)\*?\{([^}]+)\}",
        r"\2",
        text,
    )

    # Remove commands with one argument, removing the command and the argument
    text = re.sub(r"\\(label|cite|citep|citet|ref|caption|path|footnote)\{[^}]+\}", "", text)

    # Remove commands without arguments
    text = re.sub(r"\\[a-zA-Z]+", "", text)

    # Remove remaining curly braces
    text = re.sub(r"\{|\}", "", text)

    # Clean up whitespace
    text = "\n".join(line.strip() for line in text.split("\n") if line.strip())

    return text


if __name__ == "__main__":
    for root, _, files in os.walk(latex_dir):
        for file in files:
            if file.endswith(".tex"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                plain_text = latex_to_text(content)
                print(plain_text)
