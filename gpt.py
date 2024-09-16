from openai import OpenAI
from parse_profiles import get_profiles

API_SECRET = ""
client = OpenAI(
    api_key = API_SECRET
)

def search_consultants(search_terms: str) -> str:
    consultant_profiles = get_profiles()
    query = f"""You will act as an expert in matching consultant profiles with skills or areas of expertise. I will provide you with a set of consultant profiles, which may vary in format but include details such as skills, experience, and industry expertise. Along with that, I will specify a particular skill or area of expertise for which I need a recommendation.
        Your task is to:

        Analyze the profiles and identify the top 3 consultants who best fit the given skill or area of expertise.
        Rank the consultants by their suitability, providing a clear explanation for each ranking.
        Prioritize current expertise for all profiles except for Jr. or Associate Consultants, where upskilling potential can be weighed more heavily.
        If no explicit label is provided, infer that a consultant is Jr./Associate level if they have less than 3 years of experience.
        Make reasonable assumptions when certain details (such as industry expertise or experience level) are missing, and briefly mention these assumptions.
        If no strong match exists for a critical skill, consider candidates with strong secondary qualifications more heavily.
        Prioritize industry expertise equally across all profiles.
        Provide explanations using bullet points and short sentences to match my communication style.

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
            {"role": "system", "content": "You recommend consultants best suited for a project based on their provided profiles and a given set of skill search terms."},
            {
                "role": "user",
                "content": query
            }
        ]
    )

    print( completion.choices[0].message.content)

    return completion.choices[0].message.content