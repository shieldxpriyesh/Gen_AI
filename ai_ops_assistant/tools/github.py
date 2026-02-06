import requests
from typing import Dict, Any
from .base import BaseTool

class GitHubTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="search_github_repos",
            description="Search for GitHub repositories."
        )

    def execute(self, query: str, sort: str = "stars", **kwargs) -> Dict[str, Any]:
        try:
            url = f"https://api.github.com/search/repositories?q={query}&sort={sort}&per_page=3"
            response = requests.get(url)
            
            if response.status_code != 200:
                return {"error": f"GitHub API failed with status {response.status_code}"}
            
            data = response.json()
            items = data.get("items", [])
            
            results = []
            for item in items:
                results.append({
                    "name": item.get("full_name"),
                    "description": item.get("description"),
                    "stars": item.get("stargazers_count"),
                    "url": item.get("html_url")
                })
            
            return {"repositories": results}
        except Exception as e:
            return {"error": str(e)}

    def to_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Keywords to search for repositories"
                        },
                        "sort": {
                            "type": "string",
                            "description": "Sort by stars, forks, or updated. Default is stars.",
                            "enum": ["stars", "forks", "updated"]
                        }
                    },
                    "required": ["query"]
                }
            }
        }
