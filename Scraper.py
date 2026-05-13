import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

BASE = "https://www.nita.ac.in"

DEPT_IDS = {
    "caaqq": "Bio Engineering",
    "caaqs": "Chemical Engineering",
    "caaqm": "Civil Engineering",
    "caasa": "Computer Science and Engineering",
    "caasc": "Electrical Engineering",
    "caase": "Electronics and Communication Engineering",
    "caasg": "Electronics and Instrumentation Engineering",
    "caasi": "Mechanical Engineering",
    "caaqo": "Production Engineering",
    "caask": "MHSS",
    "caasm": "Physics",
    "caaso": "Chemistry",
    "caasq": "Mathematics"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def clean(x):
    return " ".join(x.replace("\xa0", " ").split())

def scrape_department(dept_id, dept_name):
    url = f"{BASE}/Department/Department_FacultyList.aspx?nDeptID={dept_id}"
    r = requests.get(url, headers=HEADERS, timeout=5)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    text = soup.get_text("\n", strip=True)

    lines = [clean(x) for x in text.split("\n") if clean(x)]

    rows = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.lower().startswith(("dr.", "prof.", "mr.", "mrs.", "ms.")):
            name = line
            title = lines[i+1] if i+1 < len(lines) else ""
            dept = lines[i+2] if i+2 < len(lines) else ""
            email = lines[i+3] if i+3 < len(lines) and "@" in lines[i+3] else ""

            rows.append({
                "Name": name,
                "Title": title,
                "Department": dept_name,
                "Email": email,
            })

            i += 4
        else:
            i += 1

    return rows


all_rows = []

for dept_id, dept_name in DEPT_IDS.items():
    try:
        print("Scraping:", dept_name)
        rows = scrape_department(dept_id, dept_name)
        print("Found:", len(rows))
        all_rows.extend(rows)
    except Exception as e:
        print("Failed:", dept_name, e)

df = pd.DataFrame(all_rows)
df.to_csv("Nita_Faculty.csv", index=False)
df.to_json("Nita_Faculty.json", orient="records", indent=2)

print("Saved", len(df), "faculty rows")
