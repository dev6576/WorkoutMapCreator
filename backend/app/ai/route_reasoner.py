from typing import List
from app.cv.models import RouteComponent

class RouteReasoner:
    def __init__(self, llm_client):
        self.llm = llm_client

    def choose_primary(self, components: List[RouteComponent]) -> int | None:
        if not self.llm or not self.llm.enabled():
            return None

        # Minimal structured prompt
        summary = [
            {
                "id": c.id,
                "length": c.pixel_length,
                "endpoints": len(c.endpoints),
                "loops": c.loops
            }
            for c in components
        ]

        prompt = f"""
        Given route components metadata, select the most likely race route.
        {summary}
        """

        response = self.llm.complete(prompt)
        return int(response.strip())
