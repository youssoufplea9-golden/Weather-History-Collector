# 🌤️ Weather History Collector

**Basically it is a simple Python application for collecting, storing, and analyzing weather data.**

> **Developed by:**
>
>   * **Youssouf Plea**
>   * **Humam Tahseen Abdullah Al-Mohammed**
>   * **Othman Murtala Abubakar**

-----

## 🚀 Project Overview

This project is a console-based tool designed to help you managing weather data. It allows you to fetch real-time weather, download historical data for the past month, store everything in a database, and generate detailed reports.

It was built to demonstrate advanced software engineering skills, including web scraping, database management, and object-oriented programming.

-----

## 🏆 Key Achievements (Bonus Points: 40/45)

We implemented several advanced features to meet high technical standards:

**Web Scraping (+10 Points):** We used the **Scrapy framework** to perform advanced data extraction.
**Database (+15 Points):** Full integration with **MongoDB** to save, search, and manage weather records reliably.
  **Professional Code Structure (+15 Points):**
      * Use of **Abstract Base Classes** and Protocols.
      * Strict **Type Checking** using Python Dataclasses.
      * Clean separation between business logic and the user interface.

-----

## ✨ Features

When you run the program, you can access the following tools via the main menu:

1.  **🌡️ Fetch Current Weather:** Get live weather updates for any city (e.g., London, Tokyo,Istanbul).
2.  **📅 Fetch Historical Weather:** Download weather history for the last 1–30 days.
3.  **🔍 Search Records:** Filter your saved data by location or temperature (e.g., "Find days above 25°C").
4.  **📊 Generate Reports:** Create summaries or detailed location-specific reports.
5.  **📈 View Statistics:** See average temperatures, trends, and records.
6.  **🌍 Compare Locations:** Compare the weather of two different cities side-by-side.
7.  **💾 Data Persistence:** All data is saved automatically to MongoDB.

-----

## 🛠️ Installation Guide

Follow these simple steps to set up the project on your machine.

### 1\. Prerequisites

Make sure you have the following installed:

  * **Python 3.8+**
  * **MongoDB** (Must be running to save data)

### 2\. Clone the Repository

```bash
git clone https://github.com/youssoufplea9-golden/Weather-History-Collector
cd Weather-History-Collector
```

### 3\. Install Dependencies

Install the required libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4\. Run the Application

Launch the main program:

```bash
python main.py
```

-----

## 📂 Project Structure

The code is organized logically to separate different responsibilities:

```text
weather_history_collector/
│
├── main.py                      # The entry point of the application
├── requirements.txt             # List of project dependencies
│
├── database/                    # Database management
│   └── mongodb_client.py        # Handles MongoDB connections and queries
│
├── scrapers/                    # Data collection
│   ├── api_weather_fetcher.py   # Fetches data from APIs
│   └── scrapy_weather_scraper.py # Advanced Scrapy implementation
│
├── models/                      # Data structures
│   └── weather_models.py        # Type-safe data classes
│
└── business_logic/              # Core logic
    └── weather_analyzer.py      # Calculates stats and generates reports
```

-----

## ℹ️ Notes

  ***Offline Mode:** If MongoDB is not running, the app will still work in "Offline Mode," but your data will not be saved.
  ***APIs:** This project uses the Open-Meteo API (free, no key required) for standard data fetching.
  ***Type Safety:** The entire codebase is strictly typed and checked with `mypy`.

-----