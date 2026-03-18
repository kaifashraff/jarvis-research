---
name: colab-mcp
description: |
  Google Colab MCP Server integration for JARVIS. Allows creating, writing, and executing code in Google Colab notebooks. Perfect for heavy research, data analysis, and GPU-accelerated computing.
compatibility: Requires uv package manager and Google account authentication
metadata:
  author: JARVIS
  version: "1.0"
  requires:
    exec:
      - uv
      - python3
---

# Google Colab MCP Server

Access Google Colab's powerful compute environment directly from JARVIS.

## Features

- **Create Notebooks** — Generate new .ipynb files
- **Write Code** — Add Python cells with code
- **Execute Cells** — Run code in Colab environment
- **Add Markdown** — Document research with explanations
- **Install Dependencies** — `!pip install` packages
- **GPU Access** — Leverage Colab's GPU for heavy computation

## Prerequisites

1. **uv installed** — `pip install uv`
2. **Google Account** — For Colab authentication
3. **Colab MCP Server** — Auto-installed via uvx

## Usage

### Create Research Notebook
```python
# JARVIS will create a Colab notebook for research
# Example: "Create a notebook for Quran pattern analysis"
```

### Run Code in Colab
```python
# JARVIS will execute code in Colab
# Example: "Run this analysis in Colab with GPU"
```

### Data Analysis
```python
# JARVIS will process large datasets in Colab
# Example: "Analyze this CSV file in Colab"
```

## Integration with JARVIS

JARVIS uses Colab MCP for:
1. **Heavy Research** — GPU-accelerated computations
2. **Data Analysis** — Large dataset processing
3. **Model Training** — AI model fine-tuning
4. **Visualization** — Creating charts and graphs
5. **Mathematical Analysis** — Complex calculations

## Authentication

The Colab MCP server will prompt for Google authentication on first use. Follow the browser authentication flow.

## Example Commands

- "Create a Colab notebook for analyzing sales data"
- "Run this Python code in Colab with GPU"
- "Analyze this dataset in Colab and create visualizations"
- "Train a model on this data in Colab"

## Limitations

- **Session Time** — Colab has runtime limits
- **GPU Availability** — Not always available on free tier
- **File Storage** — Temporary storage only
- **Authentication** — Required for each session

## Security

- All code runs in Google's secure sandbox
- No local system access from Colab
- Authentication required for sensitive operations
- Data stays in Google's environment

---
*JARVIS Colab MCP Integration v1.0*
