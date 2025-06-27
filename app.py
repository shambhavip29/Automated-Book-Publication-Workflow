
import os
import sys
from flask import Flask, render_template, request, make_response
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


from scraper.scrape_chapter import scrape_content
from vector_score.chroma_utils import save_to_chromadb, collection
from vector_score.rl_search import epsilon_greedy_search
from ai_writer.ai_writer import ai_writer  
from ai_writer.ai_reviewer import ai_reviewer

app = Flask(__name__)

RAW_PATH = r"scraper/output/raw_text.txt"
SPUN_PATH = r"output/spun_by_ai.txt"
REVIEWED_PATH = r"output/reviewed_by_ai.txt"


@app.route("/", methods=["GET", "POST"])
def editor():
    if not os.path.exists(REVIEWED_PATH):
        print("Running full pipeline...")

        if not os.path.exists(RAW_PATH):
            return " No scraped text available. Please add 'raw_text.txt' manually before proceeding."

        with open(RAW_PATH, "r", encoding="utf-8") as f:
            raw_text = f.read()

        spun = ai_writer(raw_text)
        os.makedirs(os.path.dirname(SPUN_PATH), exist_ok=True)
        with open(SPUN_PATH, "w", encoding="utf-8") as f:
            f.write(spun)

        reviewed = ai_reviewer(spun)
        os.makedirs(os.path.dirname(REVIEWED_PATH), exist_ok=True)
        with open(REVIEWED_PATH, "w", encoding="utf-8") as f:
            f.write(reviewed)


  
    if request.method == "POST":
        edited_text = request.form["editedText"]
        save_to_chromadb(edited_text, chapter_title="The Gates of Morning - Ch1")
        print(f"Total documents in ChromaDB now: {collection.count()}")

        response = make_response(edited_text)
        response.headers["Content-Disposition"] = "attachment; filename=final_human_version.txt"
        response.mimetype = "text/plain"
        return response

    with open(REVIEWED_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    return render_template("editor.html", content=content)


@app.route("/search", methods=["POST"])
def search():
    query = request.form["query"]
    result = epsilon_greedy_search(query)
    return render_template("editor.html", content=open(REVIEWED_PATH).read(), result=result)



if __name__ == "__main__":
    app.run(debug=True)
