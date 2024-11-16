import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import magic
import io

app = FastAPI()

# Initialize magic
magic_instance = magic.Magic()

@app.get("/", response_class=HTMLResponse)
async def main():
    html_content = """
    <html>
        <body>
            <h2>Select a file to identify its format:</h2>
            <form action="/identify" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <input type="submit">
            </form>
        </body>
    </html>
    """
    return html_content

@app.post("/identify", response_class=HTMLResponse)
async def identify_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        mime_type = magic.from_buffer(file_content, mime=True)
        file_type = magic_instance.from_buffer(file_content)
        result = f"<h3>File Type: {file_type}</h3><p>MIME Type: {mime_type}</p>"
        return result
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
