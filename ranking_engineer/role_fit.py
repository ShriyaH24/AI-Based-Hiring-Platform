import re
def extract_skills(skill_text):
    """
    Extract skills from the skills column.

    Example:

    ['Python' 'SQL' 'TensorFlow']

    becomes

    ['python','sql','tensorflow']
    """

    return [

        skill.lower().strip()

        for skill in re.findall(

            r"'([^']+)'",

            str(skill_text)

        )

    ]
def calculate_role_fit(

    jd_skills,

    candidate_skill_text

):

    candidate_skills = extract_skills(

        candidate_skill_text

    )

    jd_skills = [

        skill.lower().strip()

        for skill in jd_skills

    ]

    matched = list(

        set(candidate_skills)

        &

        set(jd_skills)

    )

    if len(jd_skills) == 0:

        return 0, matched

    score = len(matched) / len(jd_skills)

    return round(score,2), matched