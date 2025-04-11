# ✈️ Incheon Airport Flight Counter

**A web-based automation project that collects and visualizes the number of departing flights from Incheon Airport's Terminal 2 in real time using Python and Streamlit.**
<p align="center">
  <img src="./assets/main.png" alt="Incheon Flight Counter Dashboard" width="750"/>
</p>
---

## 🧑‍💼 Motivation

> A friend working at the airport mentioned how time-consuming it is to manually count departing flights every day.  
> This project aims to solve that issue by building an automated system that fetches and visualizes departure data without any manual input.

---

## 🎯 Project Overview

- **Goal**: Automatically retrieve and display the number of departing flights from Incheon Airport Terminal 2 (current day)
- **Framework**: Python + Streamlit Web App
- **Tools Used**: `requests`, `BeautifulSoup`, `pandas`, `Streamlit`
- **Deployment**: Currently tested on local macOS; automation possible with `crontab`

---

## 🧠 Technical Summary

| Category           | Tools / Notes                                      |
|--------------------|----------------------------------------------------|
| Data Collection    | `requests.post`, `BeautifulSoup`, `selenium` (initial version) |
| Frontend           | `Streamlit`                                        |
| Data Format        | `.csv`                                             |
| Platform           | macOS (local)                                      |
| Automation         | Potential with `crontab` / Streamlit sharing       |

---

## 🔧 Development Steps

### ▶️ Step 1: Initial Approach using Selenium
- Attempted browser automation using `selenium`
- Encountered driver issues & non-compatibility with Streamlit Cloud

### ▶️ Step 2: Problem Analysis
- Target site loads flight data via JavaScript
- Traditional `requests.get()` couldn't retrieve dynamic content

### ▶️ Step 3: Final Solution
- Analyzed network activity, discovered internal POST endpoint:  
  `https://www.airport.kr/ap/ko/dep/flightOrgList.do`
- Used `requests.post()` to collect structured flight data
- **Selenium removed** — lightweight and deployable via `Streamlit`

---

## 🖼️ Final

<p align="center">
  <img src="./assets/main.png" alt="Incheon Flight Counter Dashboard" width="750"/>
</p>

---

## 🚀 Run the Code

```bash
git clone https://github.com/2eueu/incheon-flight-counter.git
cd incheon-flight-counter
pip install -r requirements.txt
streamlit run app.py
