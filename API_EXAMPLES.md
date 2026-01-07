# API Usage Examples

Complete examples for using the PDF2PPT API in different programming languages.

## Table of Contents
- [Python Examples](#python-examples)
- [JavaScript Examples](#javascript-examples)
- [cURL Examples](#curl-examples)
- [Response Format](#response-format)

---

## Python Examples

### Basic Conversion

```python
import requests

# Upload and convert PDF
with open('slides.pdf', 'rb') as f:
    files = {'file': f}
    data = {'options': '{"parallel":4}'}
    
    response = requests.post(
        'http://localhost:8100/api/convert',
        files=files,
        data=data,
        stream=True
    )
    
    # Process streaming response
    for line in response.iter_lines():
        if line.startswith(b'data: '):
            progress = json.loads(line[6:])
            print(f"{progress['progress']}% - {progress['message']}")
            
            if progress['status'] == 'completed':
                print(f"✅ Done! Download: {progress['download_url']}")
```

### Convert Specific Pages

```python
import requests
import json

files = {'file': open('lecture.pdf', 'rb')}
options = {
    'pages': '1-10,15,20-25',  # Pages 1-10, 15, and 20-25
    'parallel': 8,              # Use 8 workers
    'force': True
}
data = {'options': json.dumps(options)}

response = requests.post(
    'http://localhost:8100/api/convert',
    files=files,
    data=data,
    stream=True
)

for line in response.iter_lines():
    if line.startswith(b'data: '):
        event = json.loads(line[6:])
        if event['status'] == 'completed':
            # Download the result
            download_url = f"http://localhost:8100{event['download_url']}"
            result = requests.get(download_url)
            with open('output.pptx', 'wb') as f:
                f.write(result.content)
            print("✅ Downloaded: output.pptx")
```

### Batch Conversion

```python
import requests

# Upload multiple files
files = [
    ('files', open('slide1.pdf', 'rb')),
    ('files', open('slide2.pdf', 'rb')),
    ('files', open('slide3.pdf', 'rb'))
]

response = requests.post(
    'http://localhost:8100/api/batch-convert',
    files=files
)

result = response.json()
print(f"Queued {len(result['task_ids'])} files")
print(f"Task IDs: {result['task_ids']}")
```

### Check API Health

```python
import requests

response = requests.get('http://localhost:8100/health')
health = response.json()

if health['status'] == 'healthy':
    print(f"✅ API is healthy (version {health['version']})")
else:
    print("❌ API is not healthy")
```

---

## JavaScript Examples

### Using Fetch API

```javascript
// Convert PDF with progress tracking
async function convertPDF(file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('options', JSON.stringify({
        pages: '1-10',
        parallel: 4
    }));
    
    const response = await fetch('http://localhost:8100/api/convert', {
        method: 'POST',
        body: formData
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
        const {done, value} = await reader.read();
        if (done) break;
        
        const text = decoder.decode(value);
        const lines = text.split('\n').filter(l => l.trim());
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = JSON.parse(line.slice(6));
                console.log(`${data.progress}% - ${data.message}`);
                
                if (data.status === 'completed') {
                    console.log(`✅ Download: ${data.download_url}`);
                }
            }
        }
    }
}

// Usage
const fileInput = document.getElementById('fileInput');
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    convertPDF(file);
});
```

### Using Axios

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function convertPDF() {
    const form = new FormData();
    form.append('file', fs.createReadStream('slides.pdf'));
    form.append('options', JSON.stringify({
        pages: '1-5',
        parallel: 4
    }));
    
    const response = await axios.post(
        'http://localhost:8100/api/convert',
        form,
        {
            headers: form.getHeaders(),
            responseType: 'stream'
        }
    );
    
    response.data.on('data', (chunk) => {
        const text = chunk.toString();
        if (text.startsWith('data: ')) {
            const data = JSON.parse(text.slice(6));
            console.log(`Progress: ${data.progress}%`);
        }
    });
}

convertPDF();
```

---

## cURL Examples

### Basic Conversion

```bash
curl -X POST http://localhost:8100/api/convert \
  -F "file=@slides.pdf" \
  -F 'options={"parallel":4}'
```

### Convert Specific Pages

```bash
curl -X POST http://localhost:8100/api/convert \
  -F "file=@lecture.pdf" \
  -F 'options={"pages":"1-10,15,20-25","parallel":8}'
```

### Download Result

```bash
# After conversion completes
curl -O http://localhost:8100/api/download/slides.pptx
```

### Batch Conversion

```bash
curl -X POST http://localhost:8100/api/batch-convert \
  -F "files=@slide1.pdf" \
  -F "files=@slide2.pdf" \
  -F "files=@slide3.pdf"
```

### Health Check

```bash
curl http://localhost:8100/health
```

### Get API Info

```bash
curl http://localhost:8100/api/info | jq
```

---

## Response Format

### Success Response (Streaming)

```
data: {"progress": 10, "message": "Reading PDF...", "status": "processing"}

data: {"progress": 20, "message": "Converting to SVG...", "status": "processing"}

data: {"progress": 50, "message": "Converting to EMF...", "status": "processing"}

data: {"progress": 80, "message": "Creating PowerPoint...", "status": "processing"}

data: {"progress": 100, "status": "completed", "output_file": "slides.pptx", "download_url": "/api/download/slides.pptx"}
```

### Error Response

```
data: {"progress": 100, "status": "error", "error": "Failed to convert PDF to SVG. Is pdf2svg installed?"}
```

### Health Check Response

```json
{
    "status": "healthy",
    "version": "1.2.0"
}
```

### API Info Response

```json
{
    "name": "PDF2PPT API",
    "version": "1.2.0",
    "features": [
        "Vector graphics conversion",
        "Page selection",
        "Parallel processing",
        "Batch conversion",
        "Real-time progress streaming"
    ],
    "endpoints": {
        "ui": "/",
        "health": "/health",
        "docs": "/docs",
        "convert": "/api/convert",
        "batch": "/api/batch-convert",
        "download": "/api/download/{filename}"
    }
}
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Input file not found" | File path incorrect | Check file path |
| "Failed to convert PDF to SVG" | pdf2svg not installed | `brew install pdf2svg` |
| "Failed to convert SVG to EMF" | inkscape not installed | `brew install inkscape` |
| "File not found" (download) | File was cleaned up | Convert again |
| Connection refused | Server not running | Start server first |

### Error Response Format

All errors follow this format:

```json
{
    "progress": 100,
    "status": "error",
    "error": "Detailed error message here"
}
```

---

## Best Practices

1. **Always check health first**
   ```bash
   curl http://localhost:8100/health
   ```

2. **Use appropriate parallel workers**
   - 1-2 workers: Low-end systems
   - 4-8 workers: Most systems (recommended)
   - 8-16 workers: High-end systems

3. **Handle streaming responses properly**
   - Use `stream=True` in requests
   - Process line by line
   - Check for 'completed' or 'error' status

4. **Clean up downloaded files**
   - Files in `/tmp/pdf2ppt/outputs` may be cleaned periodically
   - Download and save important results

5. **Use page selection for large PDFs**
   - Convert specific pages to save time
   - Example: `"pages": "1-10"` for first 10 pages

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider:
- Adding rate limiting middleware
- Implementing queue system for large batches
- Setting max file size limits

---

## Support

- 📖 Full Documentation: https://github.com/neosun100/pdf2ppt
- 🐛 Report Issues: https://github.com/neosun100/pdf2ppt/issues
- 💬 Discussions: https://github.com/neosun100/pdf2ppt/discussions
