from openai import OpenAI
from sqlalchemy import create_engine, Table, MetaData, select
from config import get_db_connection_string, API_Secret  # Import configuration for DB connection

API_SECRET = API_Secret
client = OpenAI(
    api_key=API_SECRET
)

# Set up Azure SQL connection using SQLAlchemy
DATABASE_URL = get_db_connection_string()
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the consultants table (should match the table structure in load_profiles.py)
consultants_table = Table(
    'consultants', metadata,
    autoload_with=engine
)

def get_profiles_from_database():
    """
    Fetch consultant profiles from the Azure SQL database.
    """
    with engine.connect() as connection:
        # Corrected select statement
        query = select(consultants_table)  # Use the table directly in select
        result = connection.execute(query).mappings().all()  # Fetch as mappings to get dict-like rows
        profiles = []
        for row in result:
            profiles.append(f"name: {row['name']}\n profile_text: {row['profile_text']}\n")
        return "\n\n".join(profiles)

def search_consultants(search_terms: str) -> str:
    """
    Search for consultants based on given search terms by querying the GPT model with profiles from the database.
    """
    # Fetch consultant profiles from the database
    consultant_profiles = get_profiles_from_database()
    
    # Construct the prompt for GPT
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

    # Call OpenAI API with the constructed prompt
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

    print(completion.choices[0].message.content)

    return completion.choices[0].message.content
