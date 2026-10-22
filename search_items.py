import requests

# Hifazati function: field ho to value do, na ho to "N/A"
def get_value(metadata, field):
    if field in metadata:
        return metadata[field][0]["value"]
    return "N/A"

url = "https://demo.dspace.org/server/api/discover/search/objects"
params = {"query": "library", "dsoType": "ITEM", "size": 5}
data = requests.get(url, params=params).json()
results = data["_embedded"]["searchResult"]["_embedded"]["objects"]

for result in results:
    item = result["_embedded"]["indexableObject"]
    md = item["metadata"]
    print("Title   :", get_value(md, "dc.title"))
    print("Author  :", get_value(md, "dc.contributor.author"))
    print("Year    :", get_value(md, "dc.date.issued"))
    print("Handle  :", item.get("handle", "N/A"))
    print("Abstract:", get_value(md, "dc.description.abstract")[:100])
    print("-" * 40)