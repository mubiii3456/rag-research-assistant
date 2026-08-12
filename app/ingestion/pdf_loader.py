from pypdf import PdfReader
 
 
def load_pdf(file_path: str) -> list[dict]:
    reader = PdfReader(file_path)
    pages_data = []
 
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
 
        if text:
            pages_data.append({
                "page_number": page_number,
                "text": text
            })
 
    return pages_data
 
 
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python pdf_loader.py <path_to_pdf>")
        sys.exit(1)
 
    pdf_path = sys.argv[1]
    pages = load_pdf(pdf_path)
 
    print(f"Extracted {len(pages)} pages with text.\n")
    if pages:
        print("--- Preview of Page 1 ---")
        print(pages[0]["text"][:500])
 