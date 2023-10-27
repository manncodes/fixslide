# library to make banger cli tools
import os
import sys
from pathlib import Path

import fitz
import typer
from tqdm import tqdm
from typing_extensions import Annotated


# ---- Utility functions ----
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def block_print():
    sys.stdout = open(os.devnull, "w")


def enable_print():
    sys.stdout = sys.__stdout__


# ---- End of Utility functions ----


# ---- Main function ----
def main(
    pdf_path: Path = typer.Argument(..., help="Path to the pdf file"),
    save_name: Annotated[Path, "o"] = typer.Option(
        None, help="Name of the output file"
    ),
):
    print(f"Opening {bcolors.OKCYAN} {pdf_path} {bcolors.ENDC} ...")
    pdf_document = fitz.open(pdf_path)

    print(
        f"{bcolors.OKCYAN} {pdf_path} {bcolors.ENDC} has {bcolors.OKGREEN} {len(pdf_document)} {bcolors.ENDC} pages"
    )
    page_map = {}
    for current_page in range(len(pdf_document)):
        page = pdf_document[current_page]
        text = page.get_text()
        x = text.split("\n")[-2].replace(" ", "").split("/")[0]
        page_map[x] = page_map.get(x, []) + [current_page]

    print(f"Found {bcolors.OKGREEN} {len(page_map)} {bcolors.ENDC} unique pages")
    full_pages = [max(v) for k, v in page_map.items()]

    output = fitz.open()
    block_print()
    for page in tqdm(full_pages):
        output.insert_pdf(pdf_document, from_page=page, to_page=page)
    enable_print()

    if save_name is None:
        save_name = pdf_path.stem + "-fixed.pdf"

    output.save(save_name)
    output.close()
    pdf_document.close()
    print(f"New file saved as {bcolors.OKGREEN} {save_name} {bcolors.ENDC}")


# ---- End of Main function ----

if __name__ == "__main__":
    typer.run(main)
