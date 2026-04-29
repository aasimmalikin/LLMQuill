# 🪶 LLMQuill

> An AI-powered multi-agent content pipeline that autonomously **writes** and **reviews** educational content — section by section, with full consistency tracking.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![CrewAI](https://img.shields.io/badge/CrewAI-1.14.3-blueviolet)
![LLM](https://img.shields.io/badge/LLM-GPT--4o--mini-green?logo=openai)
![Architecture](https://img.shields.io/badge/Architecture-Multi--Agent%20Flow-orange)


---

## 🧠 What is LLMQuill?

**LLMQuill** is a multi-agent LLM pipeline built on [CrewAI](https://crewai.com) that generates high-quality, structured educational content using a **write → review** agentic flow.

Two specialized AI agents collaborate on every section:

| Agent | Role | Responsibility |
|---|---|---|
| ✍️ **Content Writer** | Educational Content Writer | Drafts 500–800 word Markdown sections with examples, structure, and summaries |
| 🔍 **Content Reviewer** | Content Reviewer & Editor | Polishes drafts for grammar, clarity, accuracy, and cross-section consistency |

Each section is aware of **previously written content**, ensuring the final output reads as a cohesive, well-structured guide.

---

## 🔄 Agent Flow

```
Input: section_title + section_description
              │
              ▼
   ┌──────────────────────┐
   │   write_section_task  │  ←  Content Writer Agent
   │   (500–800 words,     │
   │    Markdown format)   │
   └──────────┬───────────┘
              │  draft_content
              ▼
   ┌──────────────────────┐
   │  review_section_task  │  ←  Content Reviewer Agent
   │  (polish, fix, refine)│
   │  context: write_task  │
   └──────────┬───────────┘
              │
              ▼
       ✅ Final Polished Section
            (saved to output/)
```

---

## 🤖 Agents

### ✍️ Content Writer

```yaml
role: Educational Content Writer
goal: >
  Create engaging, informative content that thoroughly explains
  the assigned topic and provides valuable insights to the reader
llm: openai/gpt-4o-mini
```

Specializes in breaking down complex concepts into accessible language. Each section includes:
- Brief topic introduction
- Key concepts with examples
- Practical applications or exercises
- Summary of key points

---

### 🔍 Content Reviewer

```yaml
role: Educational Content Reviewer and Editor
goal: >
  Ensure content is accurate, comprehensive, well-structured,
  and maintains consistency with previously written sections
llm: openai/gpt-4o-mini
```

Acts as a meticulous editor ensuring:
- Grammar and spelling corrections
- Improved clarity and readability
- Factual accuracy and completeness
- Consistency with prior sections
- Better structure and flow

---

## 🚀 Getting Started

### Prerequisites

- Python `>=3.13`
- [uv](https://docs.astral.sh/uv/) for dependency management

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/LLMQuill.git
cd LLMQuill
```

### 2. Install uv (if not already installed)

```bash
pip install uv
```

### 3. Install Dependencies

```bash
crewai install
```

Or directly with uv:

```bash
uv sync
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL=gpt-4o-mini
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Run the Flow

```bash
crewai run
```

The output will be saved to `output/post.md`.

---

## 📁 Project Structure

```
LLMQuill/
├── src/
│   └── creator_flow/
│       ├── config/
│       │   ├── agents.yaml        # Agent roles, goals & LLM config
│       │   └── tasks.yaml         # Task definitions & context wiring
│       ├── crew.py                # Crew assembly logic
│       └── main.py                # Entry points (kickoff, plot, etc.)
├── output/                        # Generated content saved here
├── .env                           # API keys (never commit)
├── .gitignore
├── .python-version                # Python 3.13
├── pyproject.toml                 # Project metadata & dependencies
├── uv.lock                        # Locked dependency versions
└── AGENTS.md                      # CrewAI reference for AI coding assistants
```

---

## 🛠️ Available Commands

| Command | Description |
|---|---|
| `crewai run` | Run the full content generation flow |
| `crewai flow kickoff` | Alternative flow execution |
| `crewai flow plot` | Visualize the agent flow as an HTML diagram |
| `crewai test` | Run crew tests (default: 2 iterations) |
| `crewai train -n 5` | Train the crew over N iterations |
| `crewai replay -t <id>` | Replay from a specific task |
| `crewai reset-memories -a` | Reset all agent memories |

---

## ⚙️ Configuration

### Customizing Agents

Edit `src/creator_flow/config/agents.yaml` to change agent roles, goals, backstories, or switch LLM models.

### Customizing Tasks

Edit `src/creator_flow/config/tasks.yaml` to change task descriptions, expected outputs, or context dependencies.

### Switching LLM Models

Update the `llm` field in `agents.yaml`:

```yaml
content_writer:
  llm: openai/gpt-4o        # Upgrade to GPT-4o
  # llm: anthropic/claude-3-5-sonnet  # Or use Claude
```

---

## 📦 Dependencies

```toml
requires-python = ">=3.13"
dependencies = [
    "crewai[tools]==1.14.3"
]
```

---

## 🏷️ Topics

`llm` `ai-agents` `multi-agent` `crewai` `content-generation` `gpt-4o-mini` `educational-content` `agentic-ai` `openai` `automation` `python`

---

## 🤝 Support & Resources

- 📘 [CrewAI Documentation](https://docs.crewai.com)
- 💬 [Join the CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)
- 🐛 [Report Issues](https://github.com/your-username/LLMQuill/issues)
- ⭐ If you find this useful, give it a star on GitHub!

---



---

> Built with ❤️ using [CrewAI](https://crewai.com) and OpenAI's GPT-4o-mini.
