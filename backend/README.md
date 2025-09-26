# Basic FastAPI server

## How to run

1. Make sure you have FastAPI and Uvicorn installed (already handled by setup).
2. Start the server with:

```
uvicorn main:app --reload
```

- The server will be available at http://127.0.0.1:8000/
- The root endpoint `/` returns a JSON greeting.
