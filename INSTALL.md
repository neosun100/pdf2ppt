# 安装和使用指南

## 📦 从 PyPI 安装

使用 pipx 安装（推荐，隔离环境）：

```bash
pipx install pdfslides2ppt
```

或使用 pip 安装：

```bash
pip install pdfslides2ppt
```

## 🚀 快速使用

安装后，`pdf2ppt` 命令将全局可用：

```bash
# 基本用法
pdf2ppt input.pdf output.pptx

# 不指定输出文件名（自动生成 input.pptx）
pdf2ppt input.pdf

# 详细模式
pdf2ppt input.pdf output.pptx --verbose

# 保留临时文件（用于调试）
pdf2ppt input.pdf --no-clean
```

## 📋 依赖要求

确保系统中已安装：
- **pdf2svg** - 用于 PDF 转 SVG
- **inkscape** - 用于 SVG 转 EMF

### macOS 安装依赖

```bash
brew install pdf2svg inkscape
```

### Ubuntu/Debian 安装依赖

```bash
sudo apt-get install pdf2svg inkscape
```

## 🔗 PyPI 链接

https://pypi.org/project/pdfslides2ppt/

## 📝 更多信息

查看完整文档：[README.md](README.md)
