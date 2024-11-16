from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import magic
import io

app = FastAPI()

# Initialize magic
magic_instance = magic.Magic()

# Root endpoint to serve the HTML form
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

# File upload and identification endpoint
@app.post("/identify", response_class=HTMLResponse)
async def identify_file(file: UploadFile = File(...)):
    try:
        # Read the file
        file_content = await file.read()

        # Identify the MIME type using libmagic
        mime_type = magic.from_buffer(file_content, mime=True)
        file_type = magic_instance.from_buffer(file_content)
        
        # Return result
        result = f"<h3>File Type: {file_type}</h3><p>MIME Type: {mime_type}</p>"
        return result
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"

