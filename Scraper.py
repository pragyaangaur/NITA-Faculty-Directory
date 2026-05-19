import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import re

BASE_URL = "https://www.nita.ac.in/Department/Department_FacultyList.aspx?nDeptID="

departments = {
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

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

all_faculty = []

for dept_id, dept_name in departments.items():
    url = BASE_URL + dept_id
    print(f"\nScraping: {dept_name}")
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        faculty_blocks = soup.find_all("div", class_="col-md-4")
        print(f"Faculty blocks found: {len(faculty_blocks)}")
        for block in faculty_blocks:
            image_url = ""
            img_tag = block.find("img")
            if img_tag and img_tag.get("src"):
                src = img_tag["src"].strip()
                image_url = urljoin(url, src)
            bad_urls = [
                "https://www.nita.ac.in/images/x-handle-white.png",
                "https://www.nita.ac.in/Images/system/noprofile.jpg"
            ]
            if image_url in bad_urls:
                continue

            full_text = block.get_text(" ", strip=True)
            full_text = re.sub(r"\s+", " ", full_text)

            email_match = re.search(
                r'[\w\.-]+@[\w\.-]+\.\w+',
                full_text
            )

            email = ""

            if email_match:
                email = email_match.group(0)
                full_text = full_text.replace(email, "").strip()

            full_text = full_text.replace(dept_name, "").strip()

            designation_patterns = [
                "HOD & Associate Professor",
                "Associate Professor",
                "Assistant Professor \\(Contractual\\)",
                "Assistant Professor",
                "Professor"
            ]

            name = ""
            title = ""

            for pattern in designation_patterns:
                match = re.search(pattern, full_text)
                if match:
                    title = match.group(0)
                    name = full_text[:match.start()].strip()
                    name = name.title()

                    break

            if not title:
                name = full_text.strip()
                title = ""

            if (
                not name
                or "department" in name.lower()
            ):
                continue

            all_faculty.append({
                "name": name,
                "title": title,
                "department": dept_name,
                "email": email,
                "photo_url": image_url
            })
            print(f"Found: {name}")

    except Exception as e:
        print(f"Error scraping {dept_name}: {e}")

df = pd.DataFrame(all_faculty)
df = df.drop_duplicates()
df = df.reset_index(drop=True)
df.to_csv("nit_agartala_faculty.csv", index=False)
df.to_json("Nita_Faculty.json", orient="records", indent=2)

print("\nCSV saved.")
print(f"Final faculty count: {len(df)}")
