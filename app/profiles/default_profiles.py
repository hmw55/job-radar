# ============================================================
# Default Job Radar Search Profile
# ============================================================
#
# NEW USERS START HERE
#
# This file contains the default search profile used by Job Radar.
#
# For most users, this is the first file to customize after
# installing the project.
#
# Job Radar compares every discovered job against this profile
# and assigns a match score. Higher scores indicate stronger
# alignment with the user's preferences.
#
# Most users should start by updating:
#
# 1. job_titles
# 2. keywords
# 3. allowed_locations
#
# These sections have the largest impact on match quality.
#
# ============================================================

from app.profiles.search_profile import SearchProfile


default_profile = SearchProfile(
    # Human-readable profile name.
    #
    # You can update this to describe your job search.
    #
    # Examples:
    # - "Default Tech Profile"
    # - "Hospitality Profile"
    # - "Data Entry Profile"
    # - "My Job Search Profile"
    name="Default Tech Profile",

    # ========================================================
    # Target Job Titles
    # ========================================================
    #
    # Job titles that should be treated as target roles.
    #
    # A title match is one of the strongest signals in the
    # matching engine. If a discovered job contains one of
    # these titles, it receives a significant score increase.
    #
    # If you are not receiving enough opportunities, expand
    # this list with more role titles.
    job_titles=[
        "application engineer",
        "applications engineer",
        "software engineer",
        "software engineer i",
        "software engineer 1",
        "associate software engineer",
        "junior software engineer",
        "entry level software engineer",
        "new grad software engineer",
        "graduate software engineer",
        "early career software engineer",
        "software developer",
        "software developer i",
        "software developer 1",
        "associate software developer",
        "junior software developer",
        "frontend developer",
        "frontend engineer",
        "frontend software engineer",
        "backend developer",
        "backend software engineer",
        "backend engineer",
        "full stack developer",
        "full stack engineer",
        "web developer",
        "web application developer",
        "application developer",
        "technical support engineer",
        "support engineer",
        "product support engineer",
        "product engineer",
        "solutions engineer",
        "implementation engineer",
        "integration engineer",
        "technical consultant",
        "customer engineer",
        "platform support engineer",
        "site reliability engineer",
        "sre",
        "platform engineer",
        "devops engineer",
        "forward deployed engineer",
        "react developer",
        "javascript developer",
        "typescript developer",
        "java developer",
        "python developer",
        "api developer",
        "cloud engineer",
        "infrastructure engineer",
        "developer support engineer",
        "technical product support engineer",
        "technical customer support engineer",
        "customer support engineer",
        "implementation specialist",
        "integration specialist",
        "solutions consultant",
        "technical solutions consultant",
        "technical account manager",
        "developer advocate",
        "developer relations engineer",
        "devrel engineer",
        "associate devops engineer",
        "junior devops engineer",
        "cloud support engineer",
        "technical success engineer",
        "customer success engineer",
        "implementation consultant",
        "application support engineer",
        "production support engineer",
        "site reliability engineer i",
        "platform engineer i",
    ],

    # ========================================================
    # Keywords
    # ========================================================
    #
    # Keywords commonly associated with desired jobs.
    #
    # These are searched within job descriptions and contribute
    # to the overall match score.
    #
    # Good keywords include:
    # - Skills
    # - Tools
    # - Technologies
    # - Certifications
    # - Industry terms
    #
    # Examples:
    # - "python"
    # - "customer service"
    # - "data entry"
    # - "hospitality"
    keywords=[
        "react",
        "typescript",
        "python",
        "fastapi",
        "spring boot",
        "java",
        "postgresql",
        "sql",
        "api",
        "saas",
        "linux",
        "integration",
        "automation",
        "support",
        "customer-facing",
        "javascript",
        "next.js",
        "nextjs",
        "node",
        "node.js",
        "html",
        "css",
        "tailwind",
        "supabase",
        "postgres",
        "mysql",
        "sqlite",
        "docker",
        "github",
        "git",
        "rest",
        "graphql",
        "oauth",
        "auth",
        "cloudflare",
        "vercel",
        "render",
        "troubleshooting",
        "debugging",
        "developer support",
        "technical support",
        "customer support",
    ],

    # ========================================================
    # Preferred Locations
    # ========================================================
    #
    # Preferred locations are used for scoring and match
    # explanations.
    #
    # Include countries, states, cities, regions, and "remote"
    # if remote work is acceptable.
    locations=[
        "remote",
        "united states",
        "usa",
        "colorado",
        "denver",
    ],

    # ========================================================
    # Experience Levels
    # ========================================================
    #
    # Experience indicators that increase match confidence.
    #
    # These terms are searched within job descriptions and
    # titles. They help prioritize opportunities intended for
    # early-career, junior, associate, and new-graduate
    # candidates.
    #
    # If you have more experience, consider replacing these
    # values with terms such as:
    # - "mid-level"
    # - "senior"
    # - "staff"
    experience_levels=[
        "junior",
        "associate",
        "entry level",
        "new grad",
        "0-3 years",
        "early career",
    ],

    # ========================================================
    # Excluded Titles
    # ========================================================
    #
    # Titles that should never be matched.
    #
    # This is useful for filtering out leadership roles,
    # recruiting positions, sales positions, legal roles, and
    # other opportunities outside your target career path.
    #
    # If Job Radar sends noisy or irrelevant roles, this is one
    # of the first sections to update.
    excluded_titles=[
        "senior",
        "staff",
        "principal",
        "manager",
        "director",
        "lead",
        "vp",
        "vice president",
        "head of",
        "recruiter",
        "recruiting",
        "talent",
        "account executive",
        "sales",
        "marketing",
        "counsel",
        "attorney",
        "hr",
        "people",
    ],

    # Companies that should never generate matches.
    #
    # Example:
    # excluded_companies=[
    #     "Example Company",
    # ]
    excluded_companies=[
        "Amazon",
    ],

    # If True, Job Radar should only consider remote roles.
    #
    # Note:
    # ATS providers format remote jobs differently, so remote
    # detection depends on the location metadata provided by
    # each ATS.
    remote_only=False,

    # ========================================================
    # Allowed Locations
    # ========================================================
    #
    # Locations that are explicitly permitted.
    #
    # Jobs outside these locations are rejected before scoring.
    #
    # Multiple variations are included because ATS providers
    # format locations differently.
    #
    # Examples:
    # - "United States"
    # - "USA"
    # - "US"
    # - "Remote - US"
    allowed_locations=[
        "remote",
        "remote - us",
        "united states",
        "usa",
        "us",
        "u.s.",
        "u.s.a",
        "americas",
        "north america",
        "colorado",
        "denver",
    ],

    # ========================================================
    # Excluded Locations
    # ========================================================
    #
    # Locations that should always be rejected.
    #
    # These are checked before scoring and help eliminate
    # opportunities that are not geographically compatible.
    excluded_locations=[
        "india",
        "china",
        "singapore",
        "ireland",
        "united kingdom",
        "london",
        "europe",
        "european union",
        "europe timezone",
    ],
)