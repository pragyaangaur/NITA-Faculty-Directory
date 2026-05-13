## NITA Faculty Directory

An extraction and visualization system for publicly available faculty data from the NIT Agartala website.

The system is split into two layers: a Python-based data extraction pipeline and a static frontend for real-time display which can be seen <a href="https://pragyaangaur.github.io/NITA-Faculty-Directory/">here</a>.

---

## Core Systems

### 1. Data Extraction Pipeline

What it does:  
Scrapes faculty listings across multiple engineering and science departments from the NITA website and converts them into structured records.

Core Idea:  
Transforming semi-structured HTML text into normalized tabular data using deterministic parsing rules.

Approach:

- Iterates over department-specific endpoint IDs
- Parses raw HTML into cleaned text lines
- Identifies faculty entries using title-based heuristics (Dr., Prof., etc.)
- Extracts structured fields: Name, Title, Department, Email
- Aggregates results into a unified dataset

How it Works:  
Each department page is fetched via HTTP request and flattened into raw text. The parser scans sequential lines, grouping them into logical faculty entries based on predictable ordering patterns. Extracted entries are normalized and appended into a global dataset, which is later exported as both CSV and JSON for downstream use.

Stack: Python (requests, BeautifulSoup, pandas)

---

### 2. Web-Based Directory Interface

What it does:  
Provides an interactive browser-based interface to search, filter, and browse faculty records.

Core Idea:  
Client-side rendering of a static dataset with instant filtering over a flattened memory model.

Approach:

- Loads precomputed JSON dataset
- Builds dynamic department filter options
- Performs real-time substring matching over all fields
- Renders faculty entries as responsive UI cards

How it Works:  
The dataset is loaded into memory on page initialization. A search function continuously filters entries based on user input, matching against concatenated field strings. Department filtering is implemented as a categorical constraint layered over the same search pipeline. The UI re-renders the visible subset on every input event, enabling instant feedback without server calls.

Stack: HTML, CSS, JavaScript

---

## Key Result

A fully client-side searchable academic directory built from scraped institutional data, requiring no backend infrastructure after dataset generation.
