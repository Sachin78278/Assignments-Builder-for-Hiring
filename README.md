# Assignment Architect (PDF Edition)

A Streamlit app that generates role-specific assignment suites using Google Gemini and exports them as a downloadable PDF.

## What This App Does

- Lets you upload a `.csv` or `.xlsx` role list and pick a job role.
- Auto-suggests role-based skills from a built-in skills library.
- Generates assignment suites with configurable count and difficulty.
- Uses Gemini (`gemini-2.5-flash`) to create structured assignment content.
- Exports generated output as a PDF with one click.

## Tech Stack

- Python
- Streamlit
- Google GenAI SDK (`google-genai`)
- Pandas
- `python-dotenv`
- FPDF

## Project Structure

- `app.py` - Main Streamlit app (UI, generation logic, PDF export)
- `.env` - Local environment variables (not committed)

## Prerequisites

- Python 3.9+
- A valid Google Gemini API key

## Setup

1. Clone or open this project directory.
2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install streamlit pandas python-dotenv google-genai fpdf openpyxl
```

4. Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

## Run

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## Input File Format

When uploading role data:

- Supported formats: `.csv`, `.xlsx`
- The app reads the **first column** as role names.
- Example:

```csv
Role
AI Engineer Intern
Frontend Developer Intern
HR Intern
```

## How to Use

1. Upload a role directory file (optional).
2. Select a role from file or type a custom role.
3. Choose core skills from suggestions.
4. Add extra preferences.
5. Set assignment count (1-6) and difficulty.
6. Click **Generate Assignment Suite (PDF Ready)**.
7. Download the generated PDF.

## Notes

- If no file is uploaded, default role is `AI Engineer Intern`.
- You must select at least one skill to generate output.
- The PDF text is encoded as `latin-1`; unsupported characters may fail in edge cases.

## Troubleshooting

- **"API Key not found"**
  - Ensure `.env` exists in the same folder as `app.py`.
  - Ensure variable name is exactly `GEMINI_API_KEY`.

- **Excel upload errors**
  - Install `openpyxl` (`pip install openpyxl`).

- **Generation failed**
  - Check API key validity and quota.
  - Verify internet connectivity.

## Security

- Do not commit your `.env` file.
- Rotate API keys if exposed.

## License

Add your preferred license (MIT/Apache-2.0/etc.) in this repository.
