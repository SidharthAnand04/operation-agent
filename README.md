# Code Weaver

A natural language programming system that allows experienced programmers to express their intent in natural language/pseudocode and have it converted to python code.

## Overview

Vibes Coding is an AI-powered code generation system that transforms natural language descriptions into functional code. It uses a multi-agent architecture to ensure high-quality, well-structured code output.

### Key Features

- Natural language to code conversion
- Multi-agent architecture for quality control
- Support for multiple project types:
  - Flask web applications
  - CLI tools
  - Python libraries
- Automated project structure generation
- Dependency management
- Quality assurance through multiple evaluation phases

## System Architecture

The system uses multiple specialized agents:

1. **Planning & Outline Agent**: Creates structured plans from natural language input
2. **Plan Evaluator**: Judges plan quality and provides improvement feedback
3. **Code Generation Agent**: Converts approved plans into actual code
4. **Code Evaluator**: Ensures code quality and adherence to best practices
5. **Input/Output Guardrails**: Validates inputs and outputs
6. **Context Manager**: Maintains project context and ensures proper integration

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Required environment variables:
  - `AGENTOPS_API_KEY`: Your AgentOps API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vibes-coding
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Usage

1. Create a text file with your project description (e.g., `project.txt`)

2. Run the Vibes Coding system:
```bash
python vibes_coding.py
```

3. When prompted, enter the path to your input file

4. The system will:
   - Generate a project plan
   - Evaluate and refine the plan
   - Generate code based on the approved plan
   - Evaluate and refine the code
   - Create a complete project structure

### Input File Format

Your input file should contain a clear description of the project you want to create. Example:

```text
Create a CLI tool that converts markdown files to HTML.
The tool should support basic markdown syntax and output formatted HTML files.
Include support for headers, lists, links, and code blocks.
```

## Project Types

### Flask Applications
- Full web application structure
- Routes, models, and templates
- Static file handling
- Configuration management

### CLI Tools
- Single-file or structured CLI applications
- Command-line argument parsing
- Input/output handling
- Error management

### Libraries
- Organized package structure
- Documentation
- Example code
- Test framework

## Development

### Adding New Project Types

To add support for new project types:

1. Update the `ProjectStructure` class
2. Modify the `create_project_structure` function
3. Update the planning agent's instructions
4. Add appropriate code generation templates

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with AgentOps
- Powered by advanced language models
- Inspired by natural language programming concepts

## Support

For issues and feature requests, please create an issue in the repository.
