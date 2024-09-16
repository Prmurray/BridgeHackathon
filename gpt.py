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
