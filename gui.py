
"""
Graphical user interface for the CareerMatch Resume & Job Matching Tool.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


from analyzer import (
    extract_skills,
    compare_skills,
    calculate_match_score,
    calculate_text_similarity,
    calculate_overall_match,
    get_skill_gap_level,
    generate_recommendation
)

def read_file(file_path):
    """
    Reads text from either a TXT or PDF file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Text extracted from the file.
    """

    if file_path.lower().endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    

def browse_resume():
    """
    Opens a file browser for selecting a resume.
    """

    file_path = filedialog.askopenfilename(
        title="Select Resume",
        filetypes=[
            ("PDF files", "*.pdf"),
            ("Text files", "*.txt")
        ]
    )

    if file_path:
        resume_entry.delete(0, tk.END)
        resume_entry.insert(0, file_path)


def browse_job():
    """
    Opens a file browser for selecting a job description.
    """

    file_path = filedialog.askopenfilename(
        title="Select Job Description",
        filetypes=[
            ("PDF files", "*.pdf"),
            ("Text files", "*.txt")
        ]
    )

    if file_path:
        job_entry.delete(0, tk.END)
        job_entry.insert(0, file_path)


def clear_results():
    """
    Clears the selected files and analysis results.
    """

    resume_entry.delete(0, tk.END)
    job_entry.delete(0, tk.END)

    results_text.config(state=tk.NORMAL)
    results_text.delete("1.0", tk.END)
    results_text.insert(
        tk.END,
        "Select a resume and job description,\n"
        "then click ANALYZE to begin."
    )
    results_text.config(state=tk.DISABLED)

    score_label.config(text="--%")


def analyze_resume():
    """
    Analyzes the selected resume and job description.
    """

    resume_path = resume_entry.get()
    job_path = job_entry.get()

    if not resume_path or not job_path:
        messagebox.showerror(
            "Missing Files",
            "Please select both a resume and a job description."
        )
        return

    try:
        resume_text = read_file(resume_path)
        job_text = read_file(job_path)

    except Exception as error:
        messagebox.showerror(
            "File Error",
            f"Could not read the files:\n\n{error}"
        )
        return

    if not resume_text.strip() or not job_text.strip():
        messagebox.showerror(
            "Empty File",
            "One of the selected files does not contain readable text."
        )
        return

    # Extract skills.
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    # Compare skills.
    matched_skills, missing_skills = compare_skills(
        resume_skills,
        job_skills
    )

    # Calculate scores.
    skill_score = calculate_match_score(
        matched_skills,
        job_skills
    )

    text_similarity = calculate_text_similarity(
        resume_text,
        job_text
    )

    overall_match = calculate_overall_match(
        skill_score,
        text_similarity
    )

    # Generate recommendation.
    recommendation = generate_recommendation(
        missing_skills
    )

    # Determine skill gap.
    gap_level = get_skill_gap_level(
        missing_skills
    )

    # Update score at the top.
    score_label.config(
        text=f"{overall_match}%"
    )

    # Clear previous results.
    results_text.config(state=tk.NORMAL)
    results_text.delete("1.0", tk.END)

    # Header.
    results_text.insert(
        tk.END,
        "JOB MATCH SCORE\n",
        "section"
    )

    results_text.insert(
        tk.END,
        f"Skill Match:       {skill_score}%\n"
    )

    results_text.insert(
        tk.END,
        f"Text Similarity:   {text_similarity}%\n"
    )

    results_text.insert(
        tk.END,
        f"Overall Match:     {overall_match}%\n\n"
    )

    # Matched skills.
    results_text.insert(
        tk.END,
        "✓ MATCHED SKILLS\n",
        "section"
    )

    if matched_skills:
        for skill in matched_skills:
            results_text.insert(
                tk.END,
                f"✓ {skill.title()}\n",
                "matched"
            )
    else:
        results_text.insert(
            tk.END,
            "No matching skills found.\n"
        )

    # Skill gaps.
    results_text.insert(
        tk.END,
        "\n⚠ SKILL GAP ANALYSIS\n",
        "section"
    )

    if missing_skills:
        for skill in missing_skills:
            results_text.insert(
                tk.END,
                f"⚠ {skill.title()}\n",
                "missing"
            )
    else:
        results_text.insert(
            tk.END,
            "No recognized skill gaps found.\n"
        )

    results_text.insert(
        tk.END,
        f"\nSkill Gap Level: {gap_level}\n\n",
        "gap"
    )

    # Recommendation.
    results_text.insert(
        tk.END,
        "💡 RECOMMENDATION\n",
        "section"
    )

    results_text.insert(
        tk.END,
        recommendation + "\n"
    )

    results_text.config(state=tk.DISABLED)


# --------------------------------------------------
# Main Window
# --------------------------------------------------

window = tk.Tk()

window.title("CareerMatch - Resume & Job Match Analyzer")
window.geometry("760x760")
window.resizable(False, False)

window.configure(
    padx=20,
    pady=15
)


# --------------------------------------------------
# Header
# --------------------------------------------------

title_label = tk.Label(
    window,
    text="CAREERMATCH",
    font=("Arial", 25, "bold")
)

title_label.pack()

subtitle_label = tk.Label(
    window,
    text="Resume & Job Match Analyzer",
    font=("Arial", 12)
)

subtitle_label.pack(pady=(2, 15))


# --------------------------------------------------
# File Selection
# --------------------------------------------------

files_frame = tk.LabelFrame(
    window,
    text=" Select Files ",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=12
)

files_frame.pack(
    fill=tk.X,
    pady=(0, 15)
)


# Resume row.
tk.Label(
    files_frame,
    text="Resume:",
    font=("Arial", 11, "bold")
).grid(
    row=0,
    column=0,
    padx=(0, 8),
    pady=8
)

resume_entry = tk.Entry(
    files_frame,
    width=55,
    font=("Arial", 10)
)

resume_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=8
)

tk.Button(
    files_frame,
    text="Browse",
    command=browse_resume,
    width=9
).grid(
    row=0,
    column=2,
    padx=5
)


# Job row.
tk.Label(
    files_frame,
    text="Job:",
    font=("Arial", 11, "bold")
).grid(
    row=1,
    column=0,
    padx=(0, 8),
    pady=8
)

job_entry = tk.Entry(
    files_frame,
    width=55,
    font=("Arial", 10)
)

job_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=8
)

tk.Button(
    files_frame,
    text="Browse",
    command=browse_job,
    width=9
).grid(
    row=1,
    column=2,
    padx=5
)


# --------------------------------------------------
# Buttons
# --------------------------------------------------

button_frame = tk.Frame(window)

button_frame.pack(
    pady=(0, 15)
)

analyze_button = tk.Button(
    button_frame,
    text="ANALYZE RESUME",
    command=analyze_resume,
    font=("Arial", 12, "bold"),
    width=18,
    height=2
)

analyze_button.pack(
    side=tk.LEFT,
    padx=5
)

clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_results,
    font=("Arial", 11),
    width=10,
    height=2
)

clear_button.pack(
    side=tk.LEFT,
    padx=5
)


# --------------------------------------------------
# Overall Score
# --------------------------------------------------

score_frame = tk.LabelFrame(
    window,
    text=" Overall Match ",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=8
)

score_frame.pack(
    fill=tk.X,
    pady=(0, 15)
)

score_label = tk.Label(
    score_frame,
    text="--%",
    font=("Arial", 25, "bold")
)

score_label.pack()


# --------------------------------------------------
# Results
# --------------------------------------------------

results_frame = tk.LabelFrame(
    window,
    text=" Analysis Results ",
    font=("Arial", 11, "bold"),
    padx=8,
    pady=8
)

results_frame.pack(
    fill=tk.BOTH,
    expand=True
)

results_text = scrolledtext.ScrolledText(
    results_frame,
    width=80,
    height=25,
    font=("Arial", 11),
    wrap=tk.WORD,
    padx=10,
    pady=10
)

results_text.pack(
    fill=tk.BOTH,
    expand=True
)


# Text formatting.
results_text.tag_config(
    "section",
    font=("Arial", 12, "bold")
)

results_text.tag_config(
    "matched",
    font=("Arial", 11)
)

results_text.tag_config(
    "missing",
    font=("Arial", 11)
)

results_text.tag_config(
    "gap",
    font=("Arial", 11, "bold")
)


# Initial message.
results_text.insert(
    tk.END,
    "Select a resume and job description,\n"
    "then click ANALYZE to begin."
)

results_text.config(state=tk.DISABLED)


# Start the application.
window.mainloop()



