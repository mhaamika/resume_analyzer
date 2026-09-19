
"""
Analyzes internship job-market data using Pandas.
"""

import pandas as pd


def load_job_market_data(file_path):
    """
    Loads internship data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        DataFrame: Job-market data.
    """

    return pd.read_csv(file_path)


def calculate_skill_demand(data):
    """
    Calculates how frequently each skill appears
    in the internship dataset.

    Args:
        data (DataFrame): Internship job-market data.

    Returns:
        Series: Skill demand percentages.
    """

    skill_columns = [
        "python",
        "java",
        "sql",
        "git",
        "aws",
        "docker",
        "pandas",
        "machine_learning"
    ]

    skill_demand = data[skill_columns].mean() * 100

    return skill_demand.sort_values(ascending=False)


def display_skill_demand(skill_demand):
    """
    Displays the most requested technical skills.

    Args:
        skill_demand (Series): Skill demand percentages.
    """

    print("\n" + "=" * 55)
    print("              INTERNSHIP SKILL DEMAND")
    print("=" * 55)

    for skill, percentage in skill_demand.items():

        skill_name = skill.replace("_", " ").title()

        print(
            f"{skill_name:<20} {percentage:.1f}%"
        )

    print("=" * 55)


def prioritize_missing_skills(missing_skills, skill_demand):
    """
    Ranks missing skills based on how frequently they
    appear in the internship job-market dataset.

    Args:
        missing_skills (list): Skills missing from the resume.
        skill_demand (Series): Skill demand percentages.

    Returns:
        list: Missing skills sorted by market demand.
    """

    skill_priorities = []

    for skill in missing_skills:

        # Convert skill names to match CSV column names.
        skill_key = skill.lower().replace(" ", "_")

        demand = skill_demand.get(
            skill_key,
            0
        )

        skill_priorities.append(
            (skill, demand)
        )

    skill_priorities.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return skill_priorities


def display_market_priorities(missing_skills, skill_demand):
    """
    Displays missing skills ranked by internship
    job-market demand.

    Args:
        missing_skills (list): Skills missing from the resume.
        skill_demand (Series): Skill demand percentages.
    """

    priorities = prioritize_missing_skills(
        missing_skills,
        skill_demand
    )

    print("\n📈 MARKET-BASED SKILL PRIORITY")
    print("-" * 35)

    if not priorities:
        print("  No skill gaps to prioritize.")
        return

    for number, (skill, demand) in enumerate(
        priorities,
        start=1
    ):

        if demand > 0:

            print(
                f"  {number}. {skill.title()} "
                f"({demand:.1f}% of analyzed internships)"
            )

        else:

            print(
                f"  {number}. {skill.title()} "
                "(No market data available)"
            )

    print("-" * 35)


