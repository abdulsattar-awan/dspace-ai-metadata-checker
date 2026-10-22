import requests

# 1. DSpace API ko request bhejna (jaise browser karta hai)
url = "https://demo.dspace.org/server/api"
response = requests.get(url)

# 2. JSON ko Python dictionary mein badalna
data = response.json()

# 3. Dictionary se values nikalna
print("Status code:", response.status_code)
print("Repository:", data["dspaceName"])
print("Version:", data["dspaceVersion"])