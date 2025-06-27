# Automated-Book-Publication-Workflow
Overview

The goal was to create a pipeline that:

Scrapes content from a book chapter online.

Uses AI models to rewrite and review the chapter.

Allows human editors to refine the AI output through a web interface.

Saves the final version in a vector database.

Supports intelligent search using a reinforcement learning-based method.

Technologies Used

Python: Main language for the project.

Playwright: For scraping the chapter and taking screenshots.

Ollama (LLM): Used to locally run the AI writer and reviewer.

Flask: Backend web app for editing and saving final content.

ChromaDB: Vector database for storing sentences and supporting semantic search.

Reinforcement Learning (epsilon-greedy): Used to balance between top match and exploration in search.
