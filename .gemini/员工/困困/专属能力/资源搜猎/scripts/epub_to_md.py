import sys
import os
import ebooklib # type: ignore
from ebooklib import epub # type: ignore
from bs4 import BeautifulSoup # type: ignore
import warnings

# Suppress annoying XML warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def epub_to_md(epub_path, output_dir=None):
    if not os.path.exists(epub_path):
        print(f"呜... 找不到文件: {epub_path}")
        return

    print(f"汪！正在咀嚼: {os.path.basename(epub_path)} (这可能需要一点时间，因为它很大...)")
    
    try:
        book = epub.read_epub(epub_path)
    except Exception as e:
        print(f"呜... 咬不动 (Read Failed): {e}")
        return

    if output_dir is None:
        output_dir = os.path.dirname(epub_path)
        
    base_name = os.path.splitext(os.path.basename(epub_path))[0]
    md_file = os.path.join(output_dir, base_name + ".md")

    try:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {base_name}\n\n")
            
            # Iterate through items
            # spine gives order
            for item_id in book.spine:
                # item_id is usually a tuple (id, linear) or just item
                if isinstance(item_id, tuple): 
                     item = book.get_item_with_id(item_id[0])
                else:
                     item = item_id # Depending on library version logic, could be different

                if not item: continue

                if item.get_type() == ebooklib.ITEM_DOCUMENT: # type: ignore
                    soup = BeautifulSoup(item.get_content(), 'lxml') # type: ignore
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.extract()    

                    # Get text
                    text = soup.get_text(separator='\n\n')
                    
                    # Simple cleanup
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)

                    f.write(text)
                    f.write("\n\n---\n\n")
                    
        print(f"汪！嚼完了！吐在: {md_file}")
    except Exception as e:
        print(f"呜... 消化不良 (Write Failed): {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        # If directory passed, find first epub
        if os.path.isdir(target):
            files = [f for f in os.listdir(target) if f.lower().endswith('.epub')]
            if files:
                epub_to_md(os.path.join(target, files[0]))
            else:
                print("呜... 没闻到 EPUB 味儿。")
        else:
            epub_to_md(target)
    else:
        print("Usage: python epub_to_md.py <path_to_epub_or_dir>")
