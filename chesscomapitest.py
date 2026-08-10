import requests
import json

headers = {
    "User-Agent": "RookSacCheckerTool/1.0 (kavijasaluwadana@gmail.com)"
}

username = "ShaunChess123"
url = f"https://api.chess.com/pub/player/{username}/games/archives"
response = requests.get(url, headers = headers)

if (response.status_code >= 200) and (response.status_code <= 299):
    results = response.json()
    archives = results["archives"]
    
    with open("archives.json", "w", encoding = "utf-8") as file:
        json.dump(results, file, ensure_ascii = False, indent = 4)

    allMonths = []
    for index in range(0, len(archives)):
        response = requests.get(archives[index], headers= headers)

        if (response.status_code >= 200) and (response.status_code <= 299):
            monthlyResults = response.json()
            allMonths.append(monthlyResults)
        else:
            print(response.status_code)

    with open("monthlyArchives.json", "w", encoding = "utf-8") as file:
        json.dump(allMonths, file, ensure_ascii = False, indent = 4)
else:
    print(response.status_code)