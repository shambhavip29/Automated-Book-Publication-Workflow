from chroma_utils import save_to_chromadb, search_chromadb



with open("D:/Automated_book_pipeline/output/final_human_version.txt", "r", encoding="utf-8") as f:
    final_text = f.read()


save_to_chromadb(final_text, chapter_title="The Gates of Morning - Ch1")

search_chromadb("island", n_results=2)
