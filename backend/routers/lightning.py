from fastapi import APIRouter
import requests
import os

router = APIRouter(prefix="/api", tags=["lightning"])

@router.get("/test-graphql")
async def test_lightning_graphql():
    """Test Lightning.ai GraphQL API."""
    LIGHTNING_API_KEY = os.getenv("LIGHTNING_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {LIGHTNING_API_KEY}",
        "Content-Type": "application/json"
    }
    
    introspection_query = {
        "query": """
        query IntrospectionQuery {
            __schema {
                types {
                    name
                    kind
                }
            }
        }
        """
    }
    
    try:
        response = requests.post("https://lightning.ai/graphql", headers=headers, json=introspection_query)
        return {
            "status": response.status_code,
            "response": response.text[:500]
        }
    except Exception as e:
        return {"error": str(e)}