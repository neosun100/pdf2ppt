# Docker Image Tags

## Available Tags

### Version + Architecture Tags (Recommended)

| Tag | Architecture | Platform | Description | Use Case |
|-----|--------------|----------|-------------|----------|
| `1.2.0-amd64` | x86_64 (Intel/AMD) | Linux servers, Intel Macs | Specific version for x86_64 | Production on Linux/Intel |
| `1.2.0-arm64` | ARM64 | Apple Silicon Macs, ARM servers | Specific version for ARM64 | Production on ARM |
| `latest-amd64` | x86_64 (Intel/AMD) | Linux servers, Intel Macs | Latest version for x86_64 | Always get newest x86_64 |
| `latest-arm64` | ARM64 | Apple Silicon Macs, ARM servers | Latest version for ARM64 | Always get newest ARM64 |

### Version Tags (Auto-detect architecture)

| Tag | Description | Use Case |
|-----|-------------|----------|
| `1.2.0` | Version 1.2.0 (multi-arch) | Pin to specific version |
| `latest` | Latest version (multi-arch) | Always get the newest version |

---

## Usage Examples

### For x86_64 / AMD64 Systems (Linux servers, Intel Macs)

```bash
# Recommended: Use architecture-specific tag
docker pull neosun/pdf2ppt:1.2.0-amd64
docker run -d -p 8100:8100 neosun/pdf2ppt:1.2.0-amd64

# Or use version tag (will pull amd64 automatically on x86_64 systems)
docker pull neosun/pdf2ppt:1.2.0
docker run -d -p 8100:8100 neosun/pdf2ppt:1.2.0

# Or use latest
docker pull neosun/pdf2ppt:latest
docker run -d -p 8100:8100 neosun/pdf2ppt:latest
```

### For ARM64 Systems (Apple Silicon Macs, ARM servers)

```bash
# Recommended: Use architecture-specific tag
docker pull neosun/pdf2ppt:1.2.0-arm64
docker run -d -p 8100:8100 neosun/pdf2ppt:1.2.0-arm64

# Or use version tag (will pull arm64 automatically on ARM systems)
docker pull neosun/pdf2ppt:1.2.0
docker run -d -p 8100:8100 neosun/pdf2ppt:1.2.0

# Or use latest
docker pull neosun/pdf2ppt:latest
docker run -d -p 8100:8100 neosun/pdf2ppt:latest
```

### Auto-detect Architecture (Easiest)

```bash
# Docker will automatically pull the correct architecture
docker run -d -p 8100:8100 neosun/pdf2ppt:latest
```

---

## Current Build Information

### Build Date
2026-01-07

### Available Architectures
- **linux/amd64 (x86_64)**: ✅ Available
- **linux/arm64 (ARM64)**: ✅ Available

### Image Details

#### AMD64 (x86_64)
- **Platform**: linux/amd64
- **Built on**: Linux x86_64 server
- **Base Image**: python:3.11-slim
- **Size**: ~611MB
- **Digest**: sha256:5079dd8ed1715b6887bf4689051ef557ba5c5a4f2e41384dcfd25e0417a309d6

#### ARM64
- **Platform**: linux/arm64
- **Built on**: macOS ARM64
- **Base Image**: python:3.11-slim
- **Size**: ~611MB
- **Digest**: sha256:aca6e4f8ef31500164af1943b7b402cba74de606183ce6e9e7f236d4150bc369

### Included Dependencies
- pdf2svg
- inkscape
- Python 3.11
- FastAPI + Uvicorn
- FastMCP
- All Python dependencies

---

## Tag Naming Convention

```
neosun/pdf2ppt:<version>-<arch>
```

**Components:**
- `<version>`: Semantic version (e.g., 1.2.0, 1.3.0)
- `<arch>`: Architecture (amd64, arm64)

**Examples:**
- `1.2.0-amd64` → Version 1.2.0 for x86_64
- `1.2.0-arm64` → Version 1.2.0 for ARM64 (future)
- `latest-amd64` → Latest version for x86_64
- `latest-arm64` → Latest version for ARM64 (future)

---

## Multi-Architecture Support (Future)

When ARM64 images are available, you can use:

```bash
# Docker will automatically pull the correct architecture
docker pull neosun/pdf2ppt:1.2.0
docker run -d -p 8100:8100 neosun/pdf2ppt:1.2.0
```

Or specify architecture explicitly:

```bash
# For x86_64
docker pull neosun/pdf2ppt:1.2.0-amd64

# For ARM64 (when available)
docker pull neosun/pdf2ppt:1.2.0-arm64
```

---

## Verification

### Check Image Architecture

```bash
docker image inspect neosun/pdf2ppt:1.2.0-amd64 | grep Architecture
# Output: "Architecture": "amd64"
```

### Check Image Details

```bash
docker image inspect neosun/pdf2ppt:1.2.0-amd64 --format '{{.Os}}/{{.Architecture}}'
# Output: linux/amd64
```

### List All Tags

```bash
docker images neosun/pdf2ppt
```

Expected output:
```
REPOSITORY          TAG              IMAGE ID       CREATED         SIZE
neosun/pdf2ppt      1.2.0-amd64     bacfcf7cdb53   2 minutes ago   500MB
neosun/pdf2ppt      latest-amd64    bacfcf7cdb53   2 minutes ago   500MB
neosun/pdf2ppt      1.2.0           bacfcf7cdb53   2 minutes ago   500MB
neosun/pdf2ppt      latest          bacfcf7cdb53   2 minutes ago   500MB
```

---

## Docker Hub Links

- **Repository**: https://hub.docker.com/r/neosun/pdf2ppt
- **Tags**: https://hub.docker.com/r/neosun/pdf2ppt/tags

---

## Recommended Usage

### For Production (Pin to specific version and architecture)
```bash
docker run -d -p 8100:8100 neosun/pdf2ppt:1.2.0-amd64
```

### For Development (Use latest)
```bash
docker run -d -p 8100:8100 neosun/pdf2ppt:latest-amd64
```

### For Testing (Use version without arch tag)
```bash
docker run -d -p 8100:8100 neosun/pdf2ppt:1.2.0
```

---

## Future Plans

- [ ] Build ARM64 images for Apple Silicon
- [ ] Create multi-arch manifest
- [ ] Automated builds via GitHub Actions
- [ ] Smaller Alpine-based images
