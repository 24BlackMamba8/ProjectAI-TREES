# ProjectAI-TREES

## Overview
ProjectAI-TREES is a Python-based project designed to automate the collection, cleaning, organization, and consolidation of tree logging data and appeal reports. The system processes multiple Excel sheets from the Ministry of Agriculture and forestry officials into a unified dataset that can be easily loaded and visualized in Power BI.

## Features
- Automatic collection of Excel files from official sources.
- Data cleaning and normalization, including dates, numbers, location codes, and tree species.
- Integration and logical processing of appeal reports.
- Use of OpenAI GPT for processing free-text fields into structured categories.
- Generation of a consolidated dataset suitable for BI analysis.
- Output visualization ready for Power BI.

## Technologies
- Python (Pandas, OpenPyXL, Requests)
- OpenAI GPT API
- Power BI for data visualization
- Git/GitHub for version control

## Usage
1. Clone the repository:
```bash
git clone https://github.com/yourusername/ProjectAI-TREES.git
Navigate to the excel-merge-tool folder:

cd ProjectAI-TREES/TREES/excel-merge-tool

Install dependencies:

pip install -r requirements.txt

Run the main script to process the data:

python main.py

The output will be saved in the output/ directory as a consolidated Excel/CSV file ready for Power BI.

Project Structure
TREES/
│
├─ excel-merge-tool/         # Main Python module for processing Excel files
│   ├─ input_files/          # Raw Excel input files
│   ├─ output/               # Processed and consolidated output files
│   ├─ static/               # Static resources (e.g., images, CSS, JS)
│   ├─ utils/                # Helper Python modules
│   ├─ venv/                 # Virtual environment for dependencies
│   ├─ app.py                # Optional Flask app or interface
│   └─ main.py               # Main execution script for data processing
│
├─ hs_err_pid7752.log        # Error log file
├─ replay_pid7752.log        # Replay log file
├─ T1.java                   # Optional Java file (testing/prototype)
└─ README.md                 # Project documentation
Screenshots / Example Output

(Place screenshots of the output files, Power BI dashboards, or processing results here.)



Project Status

✅ Automatic data collection implemented

✅ Data cleaning and normalization implemented

✅ Appeal report processing implemented

⚡ Ready for Power BI integration

Contributing

Contributions are welcome! Please fork the repository and submit a pull request with improvements or bug fixes.

License

This project is licensed under the MIT License.
