# ColdMailBot 📧

[![Live Demo](https://img.shields.io/badge/Live-Demo-green?style=for-the-badge&logo=streamlit)](https://mailbot.streamlit.app)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dan10ish/coldmailbot)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Made with LangChain](https://img.shields.io/badge/🦜_LangChain-black?style=for-the-badge)](https://github.com/hwchase17/langchain)

An AI-powered cold email generator that creates personalized job application emails by analyzing job postings and your resume. Built with Streamlit and powered by LangChain + Groq LLM.

## Features

- **URL Analysis**: Automatically extracts job details from career page URLs
- **Resume Processing**: Analyzes your PDF resume
- **Smart Generation**: Creates tailored cold emails matching your profile to job requirements
- **Modern UI**: Clean, responsive interface with real-time processing

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/dan10ish/coldmailbot.git
cd coldmailbot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
GROQ_API_KEY=your_api_key_here
```

4. Run the application:

```bash
streamlit run main.py
```

## Tech Stack

- Streamlit
- LangChain
- Groq LLM
- Python 3.x

## Live Demo

Visit [ColdMailBot](https://mailbot.streamlit.app) to try it out!

## License

MIT

---

Made with ❤️ by [Danish](https://danish.bio)
