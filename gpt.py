from openai import OpenAI
from parse_profiles import get_profiles

API_SECRET = ""
client = OpenAI(
    api_key = API_SECRET
)

def search_consultants(search_terms: str) -> str:
    consultant_profiles = get_profiles()
    query = f"""You are an expert in matching consultant profiles with specified skills or areas of expertise. Your task is to analyze a set of consultant profiles and identify the top 5 consultants who best fit the given skill or area of expertise.

    Instructions:
        1. Analyze Profiles:
          - Evaluate each consultant profile for relevance to the specified skills or expertise.
          - Consider details such as skills, experience, industry expertise, and location.

        2. Ranking Criteria:
          - Exact Skill Matches: Give the highest priority to consultants with exact matches to the required skills.
          - Current Expertise: Prioritize current expertise for all consultants except Jr. or Associate Consultants.
          - Upskilling Potential: For Jr. or Associate Consultants (those with less than 3 years of experience), weigh upskilling potential more heavily.
          - Industry Expertise: Consider industry expertise equally across all profiles.
          - Location: If the consultant's location is relevant to the area of expertise (e.g., location-specific requirements), consider it as a factor.
          - Secondary Qualifications: If no strong match exists for a critical skill, consider candidates with strong secondary qualifications more heavily.

        3. Assumptions:
          - Make reasonable assumptions when certain details are missing (e.g., industry expertise, experience level).
          - Briefly mention any assumptions made in your explanations.

        4. Output Format:
          - Present the rankings from 1 to 5, starting with the most suitable consultant.
          - For each consultant, provide a brief explanation of their suitability using bullet points and short sentences to match my communication style.

        5. Consistency:
          - Use a systematic approach in your analysis to ensure consistency across repeated searches.
          - Avoid any random elements in your evaluation.

    Skills or expertise to match against:
    \"\"\"
    {search_terms}
    \"\"\"

    Consultant Profiles:
    \"\"\"
    {consultant_profiles}
    \"\"\"
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You recommend consultants best suited for a project based on their provided profiles and a given set of skill search terms."},
            {
                "role": "user",
                "content": query
            }
        ]
    )

    return completion.choices[0].message.content