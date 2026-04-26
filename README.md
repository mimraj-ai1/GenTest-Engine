# GenTest Engine

**GenTest Engine** is an AI-powered static analysis tool for C++ projects that automatically generates test scenarios and predicts code coverage — **without compiling or executing any code**.

> Built and extended by **SK Mimraj** · Inspired by open-source C++ analysis tooling
> Original concept: [aarabii/CppTestGenAI](https://github.com/aarabii/CppTestGenAI) (MIT-style, no license file)

---

## 🔍 What It Does

GenTest Engine analyzes your C++ codebase and:

- Scans all `.cpp`, `.cc`, and `.h` files in the `src/` directory
- Sends each file to a local AI model (via [Ollama](https://ollama.ai) using **Qwen2.5-Coder 1.5B**) for expert-level static analysis
- Predicts potential test cases and estimated code coverage — **no runtime execution needed**
- Stores and reuses analysis using a **file-based caching system**
- Generates detailed reports in **Markdown**, **YAML**, and **terminal** formats

No compilers. No linkers. No build steps. Just smart analysis.

---

## ✨ My Improvements Over the Original

| Feature | Original | This Version |
|---------|----------|--------------|
| Retry logic on API failure | ❌ | ✅ Up to 3 retries with exponential backoff |
| JSON validation before caching | ❌ | ✅ Invalid responses never saved |
| Auto-delete bad cache entries | ❌ | ✅ Corrupt cache auto-cleared on next run |
| Prompt JSON enforcement | Basic | ✅ Hardened with CRITICAL REMINDER footer |
| Request timeout | ❌ | ✅ 120s timeout per request |
| Sample C++ test file | ❌ | ✅ `calculator.cpp` included |
| Lightweight Model | ❌ (Used heavy 7B model) | ✅ `qwen2.5-coder:1.5b` for memory stability |

---

## 🧠 System Architecture

The tool follows a modular, build-free pipeline:

1. **Initialization** — Run `python -m app.main` to start
2. **Source Scanning** — Walks `src/` for `.cpp`, `.h`, `.cc` files
3. **Cache-First Workflow** — Reuses previous analysis if cached and valid
4. **AI Analysis** — LLM returns structured JSON with coverage predictions
5. **Reporting** — Markdown + YAML + terminal summary generated

---

## 📁 Project Structure

```
GenTest Engine/
├── app/
│   ├── main.py              # Orchestrates the pipeline
│   ├── config.py            # Paths, model name, endpoints
│   ├── llm_handler.py       # Ollama API calls with retry logic
│   └── report_generator.py  # Builds Markdown, YAML, terminal reports
├── prompt/
│   └── generate_report.yaml # AI prompt template (JSON-enforced)
├── src/                     # Put your C++ source files here
├── report/                  # Generated analysis reports
├── cache/                   # Per-file cached LLM responses
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Install Ollama & Pull the Model

Download from [ollama.ai](https://ollama.ai), then:

```bash
ollama pull qwen2.5-coder:1.5b
```

### 2. Install Python Requirements

```bash
pip install -r requirements.txt
```

### 3. Add Your C++ Source Files

Place `.cpp` / `.h` / `.cc` files into the `src/` folder.
A sample `calculator.cpp` is included for quick testing.

### 4. Run the Analyzer

```bash
python -m app.main
```

---

## ⚙️ Configuration

Edit `app/config.py` to change the model or paths:

```python
llmModelName = "qwen2.5-coder:1.5b"   # Change to any Ollama-supported model
```

---

## 📊 Sample Output

```
============================================================
              ESTIMATED CODE COVERAGE REPORT
============================================================
Component                      |   Estimated Coverage
------------------------------------------------------------
Service                        |              100.00%
------------------------------------------------------------
OVERALL ESTIMATED COVERAGE     |              100.00%
============================================================
```

---

## 📋 Features

- ⚡ **No Build Required** — Purely static analysis
- 🧠 **AI-Powered** — Qwen2.5-Coder 1.5B via local Ollama server (Lightweight & Fast)
- 🔁 **Retry Logic** — Auto-retries failed API calls with backoff
- 📁 **Validated Caching** — Only stores valid JSON responses
- 📊 **Multi-Format Reports** — Markdown, YAML, and terminal
- 🔧 **Configurable** — Easy model and path customization

---

## ⚠️ Limitations

- No actual test execution — static analysis only
- Output quality depends on the LLM used
- Large files may hit token limits

---

## 🧰 Troubleshooting

**Ollama not running?**
```bash
ollama serve
```

**Model not found?**
```bash
ollama pull qwen2.5-coder:1.5b
```

**`ollama` not recognized in terminal?**

Add to PATH (Windows PowerShell):
```powershell
$env:PATH += ";$env:LOCALAPPDATA\Programs\Ollama"
```

---

## 📜 License

No license was included in the original repository.
This customized version is published for portfolio and educational purposes with full credit to the original author.

---

## 🙏 Credits

- Original concept by [aarabii](https://github.com/aarabii/CppTestGenAI)
- Extended and improved by **SK Mimraj**
- Powered by [Ollama](https://ollama.ai) + [Qwen2.5-Coder](https://github.com/QwenLM/Qwen2.5-Coder) by Alibaba Cloud
