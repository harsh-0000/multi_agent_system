# 🔬 Multi-Agent Research System

A fully automated AI research pipeline that takes a topic and returns a structured, critiqued report — powered by a chain of specialized agents.

---

## What it does

You give it a topic. It does the rest.

1. **Search Agent** — Queries the web for recent, reliable information on the topic
2. **Reader Agent** — Extracts URLs from search results, scrapes each page, and summarizes the content
3. **Writer Chain** — Synthesizes the scraped content into a well-structured research report
4. **Critic Chain** — Reviews the generated report and provides actionable critique

The Streamlit UI shows live step-by-step progress as each agent completes its task.

---

## Project Structure

```
MULTI_AGENT_SYSTEM/
├── agents.py          # Agent definitions (search_agent, reader_agent, writer_chain, critic_chain)
├── pipeline.py        # Core orchestration logic — runs all 4 agents in sequence
├── app.py             # Streamlit UI
├── tool.py            # Tool definitions used by agents (web search, scraper, etc.)
├── requirements.txt   # Python dependencies
└── .env               # API keys (not committed)
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/multi-agent-system.git
cd multi-agent-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here   # or whichever search API you're using
```

### 5. Run the app

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## Running without the UI

You can also run the pipeline directly from the terminal:

```bash
python pipeline.py
```

It will prompt you to enter a research topic and print each stage's output to stdout.

---

## Dependencies

Key packages used (see `requirements.txt` for full list):

| Package | Purpose |
|---|---|
| `streamlit` | Web UI |
| `langchain` | Agent and chain orchestration |
| `langchain-openai` | LLM backend |
| `tavily-python` | Web search tool |
| `beautifulsoup4` | Web scraping |
| `python-dotenv` | Environment variable loading |

---

## How the Pipeline Works

```
topic (str)
    │
    ▼
┌─────────────┐
│ Search Agent │  ← LangChain agent with web search tool
└──────┬──────┘
       │ search_results
       ▼
┌─────────────┐
│ Reader Agent │  ← Scrapes URLs, summarizes page content
└──────┬──────┘
       │ scraped_content
       ▼
┌──────────────┐
│ Writer Chain  │  ← LLM chain: topic + content → structured report
└──────┬───────┘
       │ report
       ▼
┌──────────────┐
│ Critic Chain  │  ← Reviews report quality, flags gaps or errors
└──────┬───────┘
       │ critique
       ▼
   state dict  →  returned to UI / printed to stdout
```

## License

MIT — feel free to use, modify, and build on this.
