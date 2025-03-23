from fastapi import Response
import json

class APIResponse:
    @staticmethod
    def success(data=None, message="Success"):
        return Response(
            content=json.dumps({"status": "success", "message": message, "data": data}),
            media_type="application/json"
        )

    @staticmethod
    def error(message="Something went wrong", status_code=400):
        return Response(
            content=json.dumps({"status": "error", "message": message}),
            media_type="application/json",
            status_code=status_code
        )
