# Documentation Index

Welcome to the Qdrant MCP Server documentation. This folder contains comprehensive guides for using, configuring, and troubleshooting the server.

---

## Quick Links

| Document | Purpose | Audience |
|----------|---------|----------|
| [CONFIG.md](CONFIG.md) | Server configuration guide | All users |
| [QUICK_START_CN.md](QUICK_START_CN.md) | Chinese quick start guide | Chinese users |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions | All users |
| [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md) | Docker and container issues | All users |
| [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md) | Detailed debugging process | Developers |

---

## Documentation Overview

### For Users

#### [CONFIG.md](CONFIG.md)
**Purpose**: Configuration guide for the Qdrant MCP server.

**Contents**:
- Environment variables reference
- Embedding provider configuration
- OpenAI-compatible service setup
- Collection name configuration
- Common configuration examples

**When to use**:
- Setting up the server for the first time
- Switching embedding providers
- Connecting to different Qdrant instances
- Configuring custom collections

---

#### [QUICK_START_CN.md](QUICK_START_CN.md)
**Purpose**: 中文快速开始指南 (Chinese quick start guide).

**内容**:
- 配置说明
- 环境变量设置
- 嵌入模型配置
- 常见配置示例

**适用于**: 中文用户快速上手

---

#### [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
**Purpose**: Solutions to common problems.

**Contents**:
- "No Results Found" issue resolution
- Cursor MCP tool errors
- Vector type mismatch problems
- Server startup issues
- Embedding model problems
- Search result quality issues
- Common error messages and fixes

**When to use**:
- When something isn't working
- Before filing a bug report
- After configuration changes
- When upgrading or migrating

**Quick diagnostic checklist included**: Step-by-step troubleshooting process.

---

#### [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md)
**Purpose**: Docker and Qdrant container specific issues.

**Contents**:
- Container won't start (Exit code 101)
- Data corruption detection and recovery
- Port conflict resolution
- Filesystem compatibility issues
- Interactive batch file usage
- Container management best practices
- Emergency recovery procedures

**When to use**:
- Qdrant container fails to start
- "Exited (101)" or similar errors
- Port 6333 conflicts
- Data corruption warnings
- Docker-related errors

**Key feature**: Interactive prompts in improved `start_mcp_server.bat`

---

### For Developers

#### [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md)
**Purpose**: Comprehensive debugging methodology and technical details.

**Contents**:
- Detailed debugging steps for "No Results Found" issue
- Environment variable propagation analysis
- Testing strategy (4 layers of testing)
- Common pitfalls and how to avoid them
- Quick diagnostic script
- Resolution patterns
- Prevention best practices

**When to use**:
- Deep diving into issues
- Understanding server internals
- Contributing to the project
- Writing tests or debugging tools

**Key sections**:
- **Critical Configuration Points**: How settings are resolved
- **Testing Strategy**: Layer-by-layer testing approach
- **Common Pitfalls**: What to watch out for
- **Quick Diagnostic Script**: Ready-to-use debugging tool

---

## Documentation by Topic

### Configuration

| Topic | Document | Section |
|-------|----------|---------|
| Environment Variables | [CONFIG.md](CONFIG.md) | Configuration Section |
| Embedding Providers | [CONFIG.md](CONFIG.md) | Embedding Model Configuration |
| OpenAI-Compatible APIs | [CONFIG.md](CONFIG.md) | OpenAI Compatible Service Config |
| Collection Names | [CONFIG.md](CONFIG.md) | Qdrant Server Configuration |

### Troubleshooting

| Problem | Document | Section |
|---------|----------|---------|
| No Search Results | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | "No Results Found" Issue |
| Cursor Errors | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Cursor MCP Tool Error |
| Vector Mismatches | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Vector Type Mismatch |
| Server Won't Start | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Server Won't Start |
| Slow Downloads | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Embedding Model Download Slow |
| Bad Results | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Search Returns Irrelevant Results |

### Development

| Topic | Document | Section |
|-------|----------|---------|
| Debugging Methodology | [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md) | Key Debugging Steps |
| Testing Strategy | [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md) | Testing Strategy |
| Environment Variable Flow | [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md) | Environment Variables Priority |
| Common Mistakes | [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md) | Common Pitfalls |

---

## Getting Started

### First Time Setup

1. **Read**: [CONFIG.md](CONFIG.md) - Understand configuration options
2. **Configure**: Set environment variables for your setup
3. **Start**: Use startup script with your configuration
4. **Verify**: Run `verify_fix.py` to confirm it works

### If Something Breaks

1. **Check**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Quick diagnostic checklist
2. **Diagnose**: Follow the relevant troubleshooting section
3. **Deep Dive**: If needed, refer to [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md)
4. **Ask**: If still stuck, check logs and existing issues

---

## Related Documentation

### Project Documentation
- **Main README**: `../README.md` - Project overview and general usage
- **License**: `../LICENSE` - Apache License 2.0

### Test Documentation
- **Test Suite**: `../tests/README.md` - Test documentation and examples

### Configuration Files
- **PyProject**: `../pyproject.toml` - Python project configuration
- **UV Lock**: `../uv.lock` - Dependency lock file

---

## Documentation Standards

### Writing Style
- **Clear and concise**: Get to the point quickly
- **Examples included**: Show, don't just tell
- **Step-by-step**: Break down complex processes
- **Cross-referenced**: Link to related sections

### Code Examples
- **Complete**: Can be copy-pasted and run
- **Commented**: Explain what's happening
- **Tested**: All examples are verified to work

### Organization
- **By audience**: User docs vs developer docs
- **By topic**: Configuration, troubleshooting, debugging
- **By frequency**: Common issues first

---

## Contributing to Documentation

### When to Update

- **Code changes**: Update relevant documentation
- **New features**: Add configuration and usage docs
- **Bug fixes**: Add to troubleshooting guide
- **Common questions**: Document in FAQ/troubleshooting

### Documentation Checklist

- [ ] Clear title and purpose
- [ ] Table of contents for long docs
- [ ] Code examples included
- [ ] Cross-references added
- [ ] Tested all examples
- [ ] Updated index (this file)

---

## Version History

| Date | Change | Documents Affected |
|------|--------|-------------------|
| 2024-10-21 | Created comprehensive debugging and troubleshooting guides | DEBUGGING_GUIDE.md, TROUBLESHOOTING.md |
| 2024-10-21 | Consolidated historical fix documents | All obsolete fix docs deleted |
| 2024-10-21 | Organized documentation structure | Created docs/ folder and index |

---

## Questions?

If you can't find what you're looking for:

1. **Search**: Use Ctrl+F to search within documents
2. **Check Index**: Review this README for relevant sections
3. **Read Tests**: `../tests/README.md` has integration examples
4. **Check Issues**: GitHub issues may have answers
5. **Ask**: Create a new issue with your question

---

## Quick Reference

### Most Common Tasks

| Task | Command | Document |
|------|---------|----------|
| **Configure server** | Edit env vars | [CONFIG.md](CONFIG.md) |
| **Start server** | `powershell -File start_server_correct_config.ps1` | [CONFIG.md](CONFIG.md) |
| **Verify server** | `uv run python verify_fix.py` | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| **Debug issues** | Follow diagnostic checklist | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| **Run tests** | `uv run pytest tests/` | `../tests/README.md` |

### Most Common Issues

1. **"No Results Found"** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md#issue-no-results-found-from-qdrant-find-tool)
2. **Cursor MCP Error** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md#issue-cursor-mcp-tool-error)
3. **Server Won't Start** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md#issue-server-wont-start)
4. **Wrong Collection** → [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md#environment-variables-priority)

---

**Last Updated**: October 21, 2024

