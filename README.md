# resume_analyzer

This is a Python-based resume and job description analysis tool that helps users identify relevant skills, understand skill gaps, and measure how closely a resume matches a target job description.

The application combines rule-based skill matching with natural language processing techniques to provide a simple, data-driven overview of a candidate's job fit.

## Features

* **Resume Analysis**
  Upload and analyze resume files in `.txt` or `.pdf` format.

* **Skill Matching**
  Identifies technical skills found in both the resume and job description.

* **Skill Match Percentage**
  Calculates the percentage of relevant skills found in the resume.

* **Text Similarity Analysis**
  Uses TF-IDF and cosine similarity to compare the content of a resume with a job description.

* **Overall Match Score**
  Combines skill matching and text similarity into an overall job match score.

* **Skill Gap Analysis**
  Identifies skills that appear in the job description but are missing from the resume.

* **Recommendations**
  Provides feedback based on the identified skill gap.

* **Job Market Analysis**
  Analyzes a dataset of internship skill requirements to identify commonly requested technical skills.

* **Graphical User Interface**
  Provides a desktop interface built with Tkinter.

## Technologies Used
* Python
* Pandas
* scikit-learn
* Natural Language Processing (NLP)
* Tkinter
* pypdf
* TF-IDF
* Cosine Similarity

## How It Works

This follows several steps to analyze a resume against a job description:

```text
Resume + Job Description
          ↓
     Text Extraction
          ↓
      Skill Matching
          ↓
   TF-IDF Text Analysis
          ↓
   Cosine Similarity
          ↓
     Match Calculation
          ↓
   Skill Gap Analysis
          ↓
      Recommendations
```

The application also uses a job-market dataset to identify technical skills that frequently appear in internship job descriptions.

## Screenshots

1. Main interface

<img width="754" height="793" alt="Screenshot 2026-09-19 at 5 22 33 PM" src="https://github.com/user-attachments/assets/9c7fe957-eff0-4f86-a19a-473561d6fa3a" />

2. Analyze feature

<img width="780" height="788" alt="Screenshot 2026-09-19 at 5 23 35 PM" src="https://github.com/user-attachments/assets/db58627e-b9bd-419d-93d4-d9a601188e9a" />

 <img width="750" height="786" alt="Screenshot 2026-09-19 at 5 29 46 PM" src="https://github.com/user-attachments/assets/c92b1276-3432-499d-99c1-10bd178eaaa8" />


## Project Structure

```text
CareerMatch/
│
├── gui.py
├── analyzer.py
├── skills.py
├── market_analysis.py
├── job_market.csv
│
├── sample_data/
│   ├── sample_resume.txt
│   └── sample_job.txt
│
├── README.md
├── requirements.txt
└── .gitignore
```

### File Descriptions

| File                 | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| `gui.py`             | Runs the CareerMatch graphical user interface                |
| `analyzer.py`        | Performs resume and job description analysis                 |
| `skills.py`          | Contains the technical skill definitions used for matching   |
| `market_analysis.py` | Analyzes technical skill demand using the job-market dataset |
| `job_market.csv`     | Dataset containing internship skill requirements             |
| `sample_data/`       | Fictional resume and job description files for testing       |

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/CareerMatch.git
```

### 2. Navigate to the project

```bash
cd CareerMatch
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python gui.py
```

## Example

This compares a resume with a target job description and produces results such as:

```text
Skill Match: 77.8%
Text Similarity: 23.9%
Overall Match: 56.2%

Skill Gap: Small

Missing Skills:
- Docker
- AWS
- Algorithms
```

The exact results depend on the resume and job description being analyzed.

## Sample Data

The `sample_data` folder contains fictional files that can be used to test the application:

* `sample_resume.txt`
* `sample_job.txt`

These files are provided so users can test CareerMatch without uploading personal information.

## Future Improvements

Potential future improvements include:

* Expanding the technical skill database
* Adding support for additional resume formats
* Improving natural language processing
* Connecting the application to real-time job postings
* Adding visual charts for skill-demand trends
* Improving resume recommendations based on target roles

