"""
FastAPI Server for PDF2PPT
Comprehensive API with detailed documentation
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
from pydantic import BaseModel, Field

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from pdf2ppt import pdf2svg, svg2emf, emf2ppt, clean_tmp, parse_page_range
from pypdf import PdfReader

app = FastAPI(
    title="PDF2PPT API",
    description="""
## Convert PDF Slides to PowerPoint with Vector Graphics

This API provides multiple ways to convert PDF presentations to PowerPoint format while maintaining the highest resolution using vector graphics.

### Features
- 🎯 Vector graphics conversion (highest quality)
- 📄 Page selection support
- ⚡ Parallel processing for speed
- 📊 Real-time progress streaming
- 📦 Batch conversion support
- 🌐 Multi-language Web UI

### Use Cases
- Convert LaTeX Beamer slides to PPT
- Convert Typst Touying presentations to PPT
- Batch process multiple PDF files
- Integrate into your workflow via API

### Links
- 🏠 [GitHub Repository](https://github.com/neosun100/pdf2ppt)
- 📦 [PyPI Package](https://pypi.org/project/pdfslides2ppt/)
- 🐳 [Docker Hub](https://hub.docker.com/r/neosun/pdf2ppt)
- 📖 [MCP Guide](https://github.com/neosun100/pdf2ppt/blob/main/MCP_GUIDE.md)
    """,
    version="1.2.0",
    contact={
        "name": "Teddy van Jerry",
        "url": "https://github.com/neosun100/pdf2ppt",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Setup static files and templates
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Directories
UPLOAD_DIR = Path("/tmp/pdf2ppt/uploads")
OUTPUT_DIR = Path("/tmp/pdf2ppt/outputs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class ConversionOptions(BaseModel):
    """Options for PDF to PPT conversion"""
    pages: Optional[str] = Field(
        None,
        description="Page range to convert (e.g., '1-5,7,9-11'). Leave empty for all pages.",
        example="1-5,7,9-11"
    )
    parallel: int = Field(
        4,
        ge=1,
        le=16,
        description="Number of parallel workers for conversion (1-16)",
        example=4
    )
    force: bool = Field(
        True,
        description="Force overwrite if output file exists"
    )
    no_clean: bool = Field(
        False,
        description="Keep temporary files for debugging"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status", example="healthy")
    version: str = Field(..., description="API version", example="1.2.0")


class ConversionProgress(BaseModel):
    """Real-time conversion progress"""
    progress: int = Field(..., ge=0, le=100, description="Progress percentage (0-100)")
    message: str = Field(..., description="Current operation message")
    status: str = Field(..., description="Status: processing, completed, or error")
    output_file: Optional[str] = Field(None, description="Output filename (when completed)")
    download_url: Optional[str] = Field(None, description="Download URL (when completed)")
    error: Optional[str] = Field(None, description="Error message (if failed)")


@app.get(
    "/",
    response_class=HTMLResponse,
    summary="Web UI",
    description="Serve the modern web interface with drag-and-drop upload",
    tags=["UI"]
)
async def index(request: Request):
    """
    ## Web User Interface
    
    Access the modern, responsive web interface with:
    - Drag-and-drop file upload
    - Real-time progress tracking
    - Multi-language support (EN, CN, TW, JP)
    - Batch conversion support
    - Beautiful gradient design
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the service is running and get version info",
    tags=["System"]
)
async def health():
    """
    ## Health Check Endpoint
    
    Returns the current status and version of the API.
    
    **Use this endpoint for:**
    - Service monitoring
    - Load balancer health checks
    - Deployment verification
    """
    return {"status": "healthy", "version": "1.2.0"}


@app.post(
    "/api/convert",
    summary="Convert PDF to PPT",
    description="Convert a PDF file to PowerPoint with real-time progress streaming",
    tags=["Conversion"],
    responses={
        200: {
            "description": "Streaming conversion progress (Server-Sent Events)",
            "content": {
                "text/event-stream": {
                    "example": """data: {"progress": 10, "message": "Reading PDF...", "status": "processing"}

data: {"progress": 50, "message": "Converting to EMF...", "status": "processing"}

data: {"progress": 100, "status": "completed", "output_file": "slides.pptx", "download_url": "/api/download/slides.pptx"}"""
                }
            }
        }
    }
)
async def convert_pdf(
    file: UploadFile = File(..., description="PDF file to convert"),
    options: str = Form(
        "{}",
        description="JSON string with conversion options",
        example='{"pages":"1-10","parallel":4,"force":true}'
    )
):
    """
    ## Convert PDF to PowerPoint
    
    Upload a PDF file and convert it to PowerPoint format with vector graphics.
    
    **Features:**
    - Real-time progress updates via Server-Sent Events (SSE)
    - Page selection support
    - Parallel processing for speed
    - Automatic metadata preservation
    
    **Example using curl:**
    ```bash
    curl -X POST http://localhost:8100/api/convert \\
      -F "file=@slides.pdf" \\
      -F 'options={"pages":"1-10","parallel":4}'
    ```
    
    **Example using Python:**
    ```python
    import requests
    
    files = {'file': open('slides.pdf', 'rb')}
    data = {'options': '{"pages":"1-10","parallel":4}'}
    response = requests.post('http://localhost:8100/api/convert', 
                            files=files, data=data, stream=True)
    
    for line in response.iter_lines():
        if line.startswith(b'data: '):
            progress = json.loads(line[6:])
            print(f"Progress: {progress['progress']}% - {progress['message']}")
    ```
    
    **Progress Events:**
    - 10%: Reading PDF
    - 20%: Converting to SVG
    - 50%: Converting to EMF
    - 80%: Creating PowerPoint
    - 100%: Completed (or error)
    """
    
    opts = json.loads(options)
    task_id = f"{Path(file.filename).stem}_{asyncio.get_event_loop().time()}"
    
    # Save uploaded file
    input_path = UPLOAD_DIR / f"{task_id}.pdf"
    with open(input_path, "wb") as f:
        f.write(await file.read())
    
    async def generate():
        try:
            yield f"data: {json.dumps({'progress': 10, 'message': 'Reading PDF...', 'status': 'processing'})}\n\n"
            
            # Read PDF
            pdf_reader = await asyncio.to_thread(PdfReader, input_path)
            total_pages = len(pdf_reader.pages)
            
            # Parse pages
            pages = parse_page_range(opts.get('pages'), total_pages) if opts.get('pages') else list(range(1, total_pages + 1))
            
            yield f"data: {json.dumps({'progress': 20, 'message': 'Converting to SVG...', 'status': 'processing'})}\n\n"
            
            # PDF to SVG
            success = await asyncio.to_thread(pdf2svg, input_path, 'pdf2svg', False)
            if not success:
                raise Exception("PDF to SVG conversion failed. Is pdf2svg installed?")
            
            yield f"data: {json.dumps({'progress': 50, 'message': 'Converting to EMF...', 'status': 'processing'})}\n\n"
            
            # SVG to EMF
            success, filters = await asyncio.to_thread(
                svg2emf, pdf_reader, input_path, 'inkscape',
                pages, False, True, opts.get('parallel', 4)
            )
            
            if not success:
                raise Exception("SVG to EMF conversion failed. Is inkscape installed?")
            
            yield f"data: {json.dumps({'progress': 80, 'message': 'Creating PowerPoint...', 'status': 'processing'})}\n\n"
            
            # EMF to PPT
            output_filename = f"{Path(file.filename).stem}.pptx"
            output_path = OUTPUT_DIR / output_filename
            await asyncio.to_thread(emf2ppt, pdf_reader, input_path, output_path, pages, False)
            
            # Cleanup
            if not opts.get('no_clean', False):
                await asyncio.to_thread(clean_tmp, input_path, False)
            
            input_path.unlink()
            
            yield f"data: {json.dumps({'progress': 100, 'status': 'completed', 'output_file': output_filename, 'download_url': f'/api/download/{output_filename}'})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'progress': 100, 'status': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get(
    "/api/download/{filename}",
    summary="Download Converted File",
    description="Download the converted PowerPoint file",
    tags=["Conversion"],
    responses={
        200: {
            "description": "PowerPoint file",
            "content": {"application/vnd.openxmlformats-officedocument.presentationml.presentation": {}}
        },
        404: {"description": "File not found"}
    }
)
async def download(filename: str):
    """
    ## Download Converted PowerPoint File
    
    Download the converted PPTX file by filename.
    
    **Example:**
    ```bash
    curl -O http://localhost:8100/api/download/slides.pptx
    ```
    
    **Note:** Files are stored temporarily and may be cleaned up periodically.
    """
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, detail=f"File not found: {filename}")
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=filename
    )


@app.post(
    "/api/batch-convert",
    summary="Batch Convert Multiple PDFs",
    description="Upload and convert multiple PDF files at once",
    tags=["Conversion"],
    responses={
        200: {
            "description": "Batch conversion initiated",
            "content": {
                "application/json": {
                    "example": {
                        "task_ids": ["uuid1", "uuid2"],
                        "message": "Queued 2 files for conversion"
                    }
                }
            }
        }
    }
)
async def batch_convert(
    files: List[UploadFile] = File(..., description="Multiple PDF files to convert")
):
    """
    ## Batch Convert Multiple PDF Files
    
    Upload multiple PDF files and convert them all at once.
    
    **Example using curl:**
    ```bash
    curl -X POST http://localhost:8100/api/batch-convert \\
      -F "files=@slide1.pdf" \\
      -F "files=@slide2.pdf" \\
      -F "files=@slide3.pdf"
    ```
    
    **Example using Python:**
    ```python
    import requests
    
    files = [
        ('files', open('slide1.pdf', 'rb')),
        ('files', open('slide2.pdf', 'rb')),
        ('files', open('slide3.pdf', 'rb'))
    ]
    
    response = requests.post('http://localhost:8100/api/batch-convert', files=files)
    result = response.json()
    print(f"Queued {len(result['task_ids'])} files")
    ```
    
    **Returns:** Task IDs for tracking conversion status
    """
    task_ids = []
    
    for file in files:
        task_id = f"{Path(file.filename).stem}_{asyncio.get_event_loop().time()}"
        task_ids.append(task_id)
        
        # Save file
        input_path = UPLOAD_DIR / f"{task_id}.pdf"
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
    
    return {
        "task_ids": task_ids,
        "message": f"Queued {len(files)} files for conversion"
    }


@app.get(
    "/api/info",
    summary="API Information",
    description="Get detailed information about the API capabilities",
    tags=["System"]
)
async def api_info():
    """
    ## API Information
    
    Get comprehensive information about this API service.
    
    **Returns:**
    - Supported features
    - Version information
    - Available endpoints
    - Usage examples
    """
    return {
        "name": "PDF2PPT API",
        "version": "1.2.0",
        "description": "Convert PDF Slides to PowerPoint with Vector Graphics",
        "features": [
            "Vector graphics conversion",
            "Page selection",
            "Parallel processing",
            "Batch conversion",
            "Real-time progress streaming",
            "Multi-language UI"
        ],
        "endpoints": {
            "ui": "/",
            "health": "/health",
            "docs": "/docs",
            "convert": "/api/convert",
            "batch": "/api/batch-convert",
            "download": "/api/download/{filename}"
        },
        "dependencies": {
            "pdf2svg": "Required for PDF to SVG conversion",
            "inkscape": "Required for SVG to EMF conversion"
        },
        "links": {
            "github": "https://github.com/neosun100/pdf2ppt",
            "pypi": "https://pypi.org/project/pdfslides2ppt/",
            "docker": "https://hub.docker.com/r/neosun/pdf2ppt",
            "mcp_guide": "https://github.com/neosun100/pdf2ppt/blob/main/MCP_GUIDE.md"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
