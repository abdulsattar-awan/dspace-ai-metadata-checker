import os
import csv
import time
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_value(metadata, field):
    if field in metadata:
        return metadata[field][0]["value"]
    return "MISSING"

def ask_gemini(prompt, tries=3):
    for attempt in range(1, tries + 1):
        try:
            response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
            return response.text
        except Exception as e:
            print(f"   (koshish {attempt} fail, 10 second baad dobara...)")
            time.sleep(10)
    return "AI check failed after 3 tries."

# 1. DSpace se records lana
url = "https://demo.dspace.org/server/api/discover/search/objects"
params = {"query": "library", "dsoType": "ITEM", "size": 5}
data = requests.get(url, params=params).json()
results = data["_embedded"]["searchResult"]["_embedded"]["objects"]

# 2. Report ki file kholna
with open("metadata_report.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Handle", "Title", "Author", "Date issued", "AI findings"])

    # 3. Har record check kar ke file mein likhna
    for result in results:
        item = result["_embedded"]["indexableObject"]
        md = item["metadata"]
        record = f"""Title: {get_value(md, "dc.title")}
Author: {get_value(md, "dc.contributor.author")}
Date issued: {get_value(md, "dc.date.issued")}
Abstract: {get_value(md, "dc.description.abstract")}
Subject: {get_value(md, "dc.subject")}"""

        prompt = f"""You are a senior library cataloger checking DSpace metadata.
Rules:
- Author must be "Surname, Given name" (e.g. "Malik, Usman").
- Date issued must be YYYY, YYYY-MM or YYYY-MM-DD.
- Abstract and Subject should not be MISSING.
- Check the title for spelling mistakes.
List only the problems, one short line each, with the suggested fix.
If there are no problems, reply "OK".

Record:
{record}"""

        print("📄 Checking:", item.get("handle"))
        findings = ask_gemini(prompt)
        writer.writerow([
            item.get("handle"),
            get_value(md, "dc.title"),
            get_value(md, "dc.contributor.author"),
            get_value(md, "dc.date.issued"),
            findings
        ])
        time.sleep(5)

print("✅ Report saved: metadata_report.csv")