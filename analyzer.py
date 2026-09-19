"""
Provides functions for analyzing resumes and job descriptions.
"""

import re

from skills import TECHNICAL_SKILLS

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_skills(text):
    """
    Finds technical skills mentioned in a piece of text.

    Text is normalized before searching so that differences
    in capitalization, punctuation, and whitespace do not
    prevent skills from being detected.

    Args:
        text (str): Resume or job description text.

    Returns:
        list: Technical skills found in the text.
    """

    text = text.lower()

    # Normalize hyphens and slashes.
    text = text.replace("-", " ")
    text = text.replace("/", " ")

    # Replace multiple spaces and line breaks with one space.
    text = " ".join(text.split())

    found_skills = []

    for skill in TECHNICAL_SKILLS:

        normalized_skill = skill.lower()
        normalized_skill = normalized_skill.replace("-", " ")
        normalized_skill = normalized_skill.replace("/", " ")
        normalized_skill = " ".join(normalized_skill.split())

        # Handle REST API / REST APIs.
        if normalized_skill == "rest api":
            if re.search(r"\brest\s+apis?\b", text):
                found_skills.append(skill)

        # Handle Machine Learning / ML.
        elif normalized_skill == "machine learning":
            if re.search(r"\bmachine\s+learning\b", text):
                found_skills.append(skill)

        # Use word boundaries for normal skills.
        else:
            pattern = r"\b" + re.escape(normalized_skill) + r"\b"

            if re.search(pattern, text):
                found_skills.append(skill)

    return found_skills


def compare_skills(resume_skills, job_skills):
    """
    Compares resume skills with the skills required
    by a job description.

    Args:
        resume_skills (list): Skills found in the resume.
        job_skills (list): Skills found in the job description.

    Returns:
        tuple: Matched skills and missing skills.
    """

    matched_skills = []
    missing_skills = []

    for skill in job_skills:

        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return matched_skills, missing_skills


def calculate_match_score(matched_skills, job_skills):
    """
    Calculates the percentage of required job skills
    that are present in the resume.

    Args:
        matched_skills (list): Skills found in both documents.
        job_skills (list): Skills required by the job.

    Returns:
        float: Skill match percentage.
    """

    if len(job_skills) == 0:
        return 0

    score = (len(matched_skills) / len(job_skills)) * 100

    return round(score, 1)


def calculate_text_similarity(resume_text, job_text):
    """
    Calculates the similarity between a resume and job
    description using TF-IDF and cosine similarity.

    Args:
        resume_text (str): Text from the resume.
        job_text (str): Text from the job description.

    Returns:
        float: Text similarity percentage.
    """

    documents = [resume_text, job_text]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 1)


def calculate_overall_match(skill_score, text_similarity):
    """
    Calculates the overall resume-job match score.

    Skill matching accounts for 60% of the score,
    while text similarity accounts for 40%.

    Args:
        skill_score (float): Technical skill match percentage.
        text_similarity (float): Resume-job text similarity percentage.

    Returns:
        float: Overall match percentage.
    """

    overall_score = (
        skill_score * 0.60
        + text_similarity * 0.40
    )

    return round(overall_score, 1)


def get_skill_gap_level(missing_skills):
    """
    Determines the size of the candidate's skill gap.

    Args:
        missing_skills (list): Skills required by the job
            but not found in the resume.

    Returns:
        str: Skill gap level.
    """

    if len(missing_skills) == 0:
        return "Excellent"

    if len(missing_skills) <= 2:
        return "Small"

    if len(missing_skills) <= 5:
        return "Moderate"

    return "Large"


def generate_recommendation(missing_skills):
    """
    Generates a recommendation based on missing skills.

    Args:
        missing_skills (list): Skills required by the job
            but not found in the resume.

    Returns:
        str: Recommendation message.
    """

    if len(missing_skills) == 0:
        return (
            "Your resume contains all recognized technical "
            "skills found in this job description."
        )

    if len(missing_skills) <= 2:
        return (
            "You have a strong technical match. "
            "Consider developing experience with: "
            + ", ".join(missing_skills)
            + "."
        )

    return (
        "You have several technical skill gaps. "
        "Consider prioritizing: "
        + ", ".join(missing_skills)
        + "."
    )