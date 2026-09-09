# Libraries to import to create our MCP server and handle data loading
from fastmcp import FastMCP
from pathlib import Path
import json



# Initializing our MCP server instance
mcp = FastMCP("Connoisseur-Server")



# Data Paths
DATA_DIR = Path(__file__).parent
CULINARY_MAP_PATH = DATA_DIR / "California-Culinary-Map.txt"
RESTAURANT_DATA_PATH = DATA_DIR / "structured-restaurant-data.json"
REVIEW_DATA_PATH = DATA_DIR / "augmented-user-review.json"



# Helper Functions
def load_restaurant_data() -> list[dict]:
    """Load the structured restaurant data produced in Module 1."""
    with open(RESTAURANT_DATA_PATH, "r") as f:
        return json.load(f)


def load_review_data() -> list[dict]:
    """Load the augmented user reviews produced in Module 1."""
    with open(REVIEW_DATA_PATH, "r") as f:
        return json.load(f)



# MCP Resource - Exposing the Raw Culinary Map data
@mcp.resource("culinary-map://california")
def get_culinary_map() -> str:
    """The full raw California Culinary Map text from Module 1.
    Contains detailed descriptions of 100+ restaurants across California
    including their vibes, cuisines, ratings, and price ranges."""
    return CULINARY_MAP_PATH.read_text()



# TOOL 1 — Get Restaurant Info (Structured Search)
@mcp.tool()
def get_restaurant_info(restaurant_name: str) -> str:
    """Search for a restaurant by name and return its structured details
    including cuisine, rating, price range, and signature dish."""
    restaurants = load_restaurant_data()
    query = restaurant_name.lower().strip()

    # Finding restuarants that match the query in the structured JSON data
    matches = []
    for restaurant in restaurants:
        name = restaurant["name"].lower()
        if query in name or name in query:
            matches.append(restaurant)

    # Return a not found message if no matches are found
    if not matches:
        return json.dumps(
            {
                "status": "not_found",
                "message": f"No restaurant found matching '{restaurant_name}'.",
                "suggestion": "Try a partial name like 'Iron' or 'Sakura'.",
            },
            indent=2,
        )

    return json.dumps(
        {"status": "found", "count": len(matches), "results": matches},
        indent=2,
    )



# TOOL 2 — Recommend by Vibe (Semantic Search)
@mcp.tool()
def recommend_by_vibe(vibe: str) -> str:
    """Find restaurants that match a given vibe or atmosphere keyword.
    Searches both structured vibe tags and raw text descriptions.
    Examples of vibe keywords: "moody", "sun-drenched", "romantic", etc."""
    restaurants = load_restaurant_data()
    vibe_lower = vibe.lower().strip()

    # Pass 1: Search structured vibe tags in JSON
    structured_matches = []
    for restaurant in restaurants:
        vibes_list = [v.lower() for v in restaurant.get("vibes", [])]
        description = restaurant.get("description", "").lower()

        if any(vibe_lower in v for v in vibes_list) or vibe_lower in description:
            structured_matches.append(
                {
                    "name": restaurant["name"],
                    "neighborhood": restaurant["neighborhood"],
                    "cuisine": restaurant["cuisine"],
                    "rating": restaurant["rating"],
                    "vibes": restaurant["vibes"],
                    "price_range": restaurant["price_range"],
                }
            )

    # Pass 2: Search the raw text for additional matches 
    raw_text = CULINARY_MAP_PATH.read_text()
    paragraphs = raw_text.split("\n\n")
    text_excerpts = []
    for para in paragraphs:
        if vibe_lower in para.lower() and para.strip():
            text_excerpts.append(para.strip()[:300])

    return json.dumps(
        {
            "vibe_searched": vibe,
            "structured_matches": structured_matches,
            "raw_text_excerpts": text_excerpts[:5],
        },
        indent=2,
    )



# TOOL 3 — Get Review (Returns Review Data for Lab 2 Demonstration)
@mcp.tool()
def get_review(restaurant_name: str) -> str:
    """Retrieve the full review for a restaurant."""
    reviews = load_review_data()
    query = restaurant_name.lower().strip()

    # Find the matching review
    matching_review = None
    for review in reviews:
        if query in review["restaurant_name"].lower():
            matching_review = review
            break
    
    # Return a not found message if no review matches the query
    if not matching_review:
        return json.dumps(
            {
                "status": "not_found",
                "message": f"No review found for '{restaurant_name}'.",
            },
            indent=2,
        )

    return json.dumps(
        {
            "status": "found",
            "restaurant": matching_review["restaurant_name"],
            "reviewer": matching_review["reviewer"],
            "rating": matching_review["rating"],
            "review_text": matching_review["review_text"],
            "image_description": matching_review.get("image_description", "N/A"),
            "visit_date": matching_review.get("visit_date", "N/A"),
        },
        indent=2,
    )



# Run the Server
if __name__ == "__main__":
    mcp.run()
