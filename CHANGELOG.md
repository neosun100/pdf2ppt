# Changelog

All notable changes to this project will be documented in this file.

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
  - English, 简体中文, 繁體中文, 日本語
  - 한국어, Français, Deutsch, Español
  - Português, Italiano, Русский, العربية
  - हिन्दी, ไทย, Tiếng Việt, Nederlands, Polski, Türkçe
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
- 🔮 Rotating conic gradient halo
- ⚡ Button ripple animation
- 🌈 Flowing 4-color gradient progress bar
- 💎 Glass highlight reflections
- 🌟 Enhanced 3D depth shadows

### Changed
- Enhanced backdrop-filter to blur(40px) saturate(200%)
- Improved animation timing and easing
- Better hover interactions with glow effects
- Star banner moved to bottom with golden glow
- Upgraded visual hierarchy with multiple shadow layers

### Technical
- Grid overlay pattern (50px x 50px)
- Floating particle effects
- Multi-layer box-shadow with inset glow
- Cubic-bezier easing for smooth animations
- Fallback support for older browsers

## [1.2.0] - 2026-01-07

### Added
- 🎨 Modern Web UI with drag-and-drop support
- 🌐 Multi-language support (EN, CN, TW, JP)
- 🚀 FastAPI server with async processing
- 📡 RESTful API with Swagger documentation
- 🔧 MCP (Model Context Protocol) tool server
- 🐳 Docker support with all-in-one image
- 📦 Batch conversion support
- 📊 Real-time progress tracking
- 🎯 Streaming response for long-running tasks

### Changed
- Improved error handling and user feedback
- Better dependency checking
- Enhanced documentation

## [1.1.0] - 2026-01-07

### Added
- Page selection with `--pages` option
- Parallel processing with `--parallel` option
- Beautiful CLI output using rich library
- Automatic dependency check
- Force overwrite with `--force` option

### Changed
- Replaced tqdm with rich for progress display
- Improved error messages

## [1.0.0] - 2023-12-01

### Added
- Initial release
- PDF to PPT conversion with vector graphics
- Metadata preservation
- Auto slide size detection
- Command line interface

[1.2.0]: https://github.com/neosun100/pdf2ppt/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/neosun100/pdf2ppt/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/neosun100/pdf2ppt/releases/tag/v1.0.0
