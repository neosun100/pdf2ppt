# Changelog

All notable changes to this project will be documented in this file.

## [1.3.1] - 2026-01-10

### Fixed
- 🐛 **Decompression Bomb Error**: Fixed PIL image size limit error when processing PDFs with large embedded images (>178M pixels)
  - Added `PIL.Image.MAX_IMAGE_PIXELS = None` to disable the security limit
  - Now supports PDFs with high-resolution scans and large images

### Changed
- Synchronized version numbers across all components (API, CLI, package)

## [1.3.0] - 2026-01-08

### 🌍 Major Release: 18 Languages Support

This release brings comprehensive internationalization with support for 18 languages.

### Added
- 🌍 **18 Languages Support**
  - English, 简体中文, 繁體中文, 日本語
  - 한국어 (Korean), Français (French), Deutsch (German), Español (Spanish)
  - Português (Portuguese), Italiano (Italian), Русский (Russian), العربية (Arabic)
  - हिन्दी (Hindi), ไทย (Thai), Tiếng Việt (Vietnamese), Nederlands (Dutch), Polski (Polish), Türkçe (Turkish)
- 📚 API Docs button in header with glassmorphism style
- ✍️ Author signature in footer: "Made with ❤️ by neosun100"
- 🔗 Docker Hub link in footer

### Changed
- Improved header layout with API Docs button alongside language selector
- Enhanced button styling with consistent glassmorphism effect
- Added cache-busting version parameters to static assets

### Fixed
- CDN cache issues with static files

## [1.2.2] - 2026-01-08

### Added
- 🌍 Extended i18n support to 18 languages
- 📚 Prominent API Docs (Swagger) button in footer
- 🔗 Docker Hub link in footer

### Changed
- Improved footer layout with button-style links
- Enhanced visual hierarchy for documentation access

## [1.2.1] - 2026-01-08

### Added
- 🎨 Ultra glassmorphism UI design
- 🌌 Dynamic mesh gradient background (5 colors)
- ✨ Shimmer animation on upload area
- 💫 Neon glow effects on all elements

### Changed
- Enhanced backdrop-filter to blur(40px) saturate(200%)
- Improved animation timing and easing

## [1.2.0] - 2026-01-07

### Added
- 🎨 Modern Web UI with drag-and-drop support
- 🌐 Multi-language support (EN, CN, TW, JP)
- 🚀 FastAPI server with async processing
- 📡 RESTful API with Swagger documentation
- 🔧 MCP (Model Context Protocol) tool server
- 🐳 Docker support with all-in-one image

## [1.1.0] - 2026-01-07

### Added
- Page selection with `--pages` option
- Parallel processing with `--parallel` option
- Beautiful CLI output using rich library

## [1.0.0] - 2023-12-01

### Added
- Initial release
- PDF to PPT conversion with vector graphics
- Metadata preservation
- Auto slide size detection
