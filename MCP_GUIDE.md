# MCP Tool Server Guide

## What is MCP?

Model Context Protocol (MCP) is an open protocol that enables AI assistants to interact with external tools and services. The PDF2PPT MCP server provides programmatic access to PDF conversion functionality.

## Available Tools

### 1. `convert_pdf_to_ppt`

Convert a single PDF file to PowerPoint presentation.

**Parameters:**
- `input_pdf` (required): Path to input PDF file
- `output_ppt` (optional): Path to output PPTX file
- `pages` (optional): Page range (e.g., "1-5,7,9-11")
- `parallel` (optional): Number of parallel workers (default: 4)
- `force` (optional): Force overwrite (default: True)
- `no_clean` (optional): Keep temporary files (default: False)

**Example:**
```python
result = await mcp_client.call_tool(
    "convert_pdf_to_ppt",
    {
        "input_pdf": "/path/to/slides.pdf",
        "pages": "1-10",
        "parallel": 8
    }
)
```

**Response:**
```json
{
    "status": "success",
    "output": "/path/to/slides.pptx",
    "pages_converted": 10,
    "total_pages": 20
}
```

### 2. `batch_convert_pdfs`

Batch convert multiple PDF files in a directory.

**Parameters:**
- `input_dir` (required): Directory containing PDF files
- `output_dir` (optional): Output directory for PPTX files
- `pattern` (optional): File pattern to match (default: "*.pdf")
- `parallel` (optional): Number of parallel workers per file (default: 4)

**Example:**
```python
result = await mcp_client.call_tool(
    "batch_convert_pdfs",
    {
        "input_dir": "./lectures",
        "pattern": "lecture*.pdf",
        "parallel": 4
    }
)
```

**Response:**
```json
{
    "status": "success",
    "converted": 5,
    "failed": 0,
    "total": 5,
    "files": [
        {"file": "lecture1.pdf", "status": "success", "output": "lecture1.pptx"},
        ...
    ]
}
```

### 3. `check_dependencies`

Check if required dependencies (pdf2svg, inkscape) are installed.

**Parameters:** None

**Example:**
```python
result = await mcp_client.call_tool("check_dependencies", {})
```

**Response:**
```json
{
    "pdf2svg": true,
    "inkscape": true,
    "all_installed": true
}
```

## MCP Server Configuration

Add this to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "pdf2ppt": {
      "command": "python",
      "args": ["/path/to/pdf2ppt/mcp/server.py"],
      "env": {}
    }
  }
}
```

Or using `uvx`:

```json
{
  "mcpServers": {
    "pdf2ppt": {
      "command": "uvx",
      "args": ["--from", "pdfslides2ppt[mcp]", "python", "-m", "mcp.server"]
    }
  }
}
```

## Running the MCP Server

### Method 1: Direct Python

```bash
cd /path/to/pdf2ppt
python mcp/server.py
```

### Method 2: Using pipx

```bash
pipx install "pdfslides2ppt[mcp]"
python -m mcp.server
```

### Method 3: Docker

```bash
docker run -v /path/to/pdfs:/data neosun/pdf2ppt:latest python mcp/server.py
```

## Differences from API

| Feature | MCP Tools | REST API |
|---------|-----------|----------|
| Access Method | Programmatic (AI assistants) | HTTP requests |
| Authentication | None (local) | Optional |
| Streaming | No | Yes (progress updates) |
| Batch Processing | Built-in | Manual |
| Use Case | AI automation | Web applications |

## Error Handling

All tools return a consistent error format:

```json
{
    "status": "error",
    "error": "Error message here"
}
```

Common errors:
- File not found
- Missing dependencies (pdf2svg, inkscape)
- Invalid page range
- Permission denied

## Best Practices

1. **Check dependencies first**: Always call `check_dependencies()` before conversion
2. **Use page ranges**: For large PDFs, convert specific pages to save time
3. **Parallel processing**: Adjust `parallel` parameter based on your CPU cores
4. **Batch operations**: Use `batch_convert_pdfs` for multiple files instead of looping
5. **Error handling**: Always check the `status` field in responses

## Examples

### Convert specific pages from a PDF

```python
# Convert only slides 1-10 from a lecture
result = await mcp_client.call_tool(
    "convert_pdf_to_ppt",
    {
        "input_pdf": "lecture.pdf",
        "pages": "1-10",
        "parallel": 8
    }
)

if result["status"] == "success":
    print(f"Converted {result['pages_converted']} pages to {result['output']}")
```

### Batch convert all PDFs in a directory

```python
# Convert all lecture PDFs
result = await mcp_client.call_tool(
    "batch_convert_pdfs",
    {
        "input_dir": "./lectures",
        "output_dir": "./pptx",
        "pattern": "*.pdf"
    }
)

print(f"Converted {result['converted']} files, {result['failed']} failed")
```

### Check if dependencies are installed

```python
# Check before conversion
deps = await mcp_client.call_tool("check_dependencies", {})

if not deps["all_installed"]:
    print("Missing dependencies:")
    if not deps["pdf2svg"]:
        print("  - pdf2svg")
    if not deps["inkscape"]:
        print("  - inkscape")
    print(f"\nInstall with: {deps['install_instructions']['macos']}")
```

## Troubleshooting

### MCP server not starting

1. Check Python version (>= 3.9)
2. Install dependencies: `pip install fastmcp`
3. Verify file paths in configuration

### Conversion fails

1. Run `check_dependencies()` to verify pdf2svg and inkscape are installed
2. Check file permissions
3. Verify input file is a valid PDF

### Slow conversion

1. Increase `parallel` parameter (try 8 or 16)
2. Convert specific pages instead of entire PDF
3. Use batch conversion for multiple files

## Support

- GitHub Issues: https://github.com/neosun100/pdf2ppt/issues
- Documentation: https://github.com/neosun100/pdf2ppt#readme
