from fastapi import Response
import json

class APIResponse:
    @staticmethod
    def success(data=None, message="Success"):
        return Response(
            content=json.dumps({"status": "success", "message": message, "data": data}),
            media_type="application/json"
        )