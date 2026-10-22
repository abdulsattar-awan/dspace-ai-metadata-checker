# DSpace AI Metadata Quality Checker

A Python tool that reads records from a DSpace repository through its REST API and uses Google Gemini as a "senior cataloger" to find metadata problems, then saves a CSV report for librarians.

Built by a librarian learning AI automation, to combine cataloguing rules with AI.

## Why

Institutional repositories often have inconsistent metadata: author names not in "Surname, Given name" form, mixed date formats, missing abstracts and subjects. Checking thousands of records by hand takes months. This tool does a first check automatically, and a librarian reviews the report.

## How it works

1. Searches the DSpace REST API (`/server/api/discover/search/objects`)
2. Extracts Dublin Core fields (title, author, date issued, abstract, subject)
3. Sends each record to Gemini with cataloguing rules
4. Writes the findings to `metadata_report.csv`

## Rules checked

- Author in "Surname, Given name" form
- Date issued as YYYY, YYYY-MM or YYYY-MM-DD
- Abstract and subject present
- Spelling in the title

## Example findings

| Record | Finding |
|---|---|
| Author "Dania Bilal" | Change to "Bilal, Dania" |
| Author "DUBE, Tinyiko Vivian" | Change to "Dube, Tinyiko Vivian" |
| Date "12/27/2021" | Change to "2021-12-27" |
| Abstract missing | Add an abstract |

## Reliability

- Missing fields are handled safely and reported as MISSING instead of crashing the program
- If Gemini returns a temporary error (503), the tool waits and retries up to 3 times
- Records that still fail are marked "AI check failed after 3 tries", so nothing is silently skipped

## Limitations

- Tested on the public DSpace 10 demo site (demo.dspace.org), not on a production repository
- Checks 5 search results at a time
- Only reports problems; it does not change any records. A librarian makes the corrections
- AI suggestions should always be reviewed by a person

## Next steps

- Check a whole collection with paging
- Add more rules (language codes, duplicate titles, controlled subject terms)
- Suggest corrections in a CSV format that DSpace can re-import

## Files

| File | Purpose |
|---|---|
| `metadata_checker.py` | Main tool: fetch, AI check, CSV report |
| `search_items.py` | Search DSpace and print metadata |
| `api_test.py` | First connection test to the DSpace API |
| `metadata_report.csv` | Sample report |

## Setup

```
pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_API_KEY=your_key_here
```

Run:

```
python metadata_checker.py
```

## Tech

Python, DSpace 10 REST API, Google Gemini (google-genai), requests, python-dotenv, csv