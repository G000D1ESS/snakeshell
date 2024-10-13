# 🐍 SnakeShell: A Bash-like Unix Shell in Python

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

Welcome to **SnakeShell**! 🎉

This project aims to develop a Unix shell similar to Bash, written in Python and utilizing the PEG parser [TatSu](https://github.com/neogeny/TatSu). SnakeShell is designed to replicate core functionalities of traditional Unix shells while incorporating modern features.

## 📚 Table of Contents

- [Features](#-features)
- [Roadmap](#-roadmap)
  - [Development Stages](#development-stages)
- [Installation](#-installation)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Features

- **Process Management**: Forking, executing, and waiting for processes
- **File Redirection and Pipes**: Input/output redirection and command pipelines
- **Job Control**: Background processes and signal handling
- **Quoting and Expansion**: Variable expansion and globbing
- **Interactive Features**: Command history and auto-completion

## 📋 Roadmap

### Development Stages

#### Stage 1: Fork/Exec/Wait ✅

- Basics of Unix processes
- Implement the simplest possible shell
- Support built-in commands like `cd`, `exec`, etc.
- Search for commands in `PATH`
- Handle exit statuses and the `!` operator
- Support command lists using `;`, `&&`, and `||`
- Support subshells and line continuation

#### Stage 2: Files and Pipes ✅

- Implement file descriptor redirection (`<`, `>`, `>>`, `<>`)
- Support pipes between commands (`|`)
- Handle file descriptor duplication (`<&`, `>&`)
- Implement process and command substitution (`<(...)`, `$(...)`)
- Ensure proper handling of file descriptors and inheritance

#### Stage 3: Job Control and Signals 🚧

- Discuss signals and support for keyboard shortcuts like `Ctrl+C`, `Ctrl+\`, and `Ctrl+Z`
- Implement background processes and job control (`&`, `jobs`, `fg`, `bg`)
- Ensure proper handling of sessions and process groups

#### Stage 4: Quoting and Expansion ⏳

- Handle environments and variables
- Implement globbing (wildcard matching)
- Support quoting and character escaping
- Handle alias and function expansions

#### Stage 5: Interactivity ⏳

- Enhance the shell for interactive work
- Support command history
- Implement auto-completion
- Customize prompts and themes

## 🚀 Installation

To install **SnakeShell**, follow these steps:

1. **Clone the repository**

    ```bash
    git clone https://github.com/G000D1ESS/snakeshell.git
    ```

2. **Navigate to the project directory**

    ```bash
    cd snakeshell
    ```

3. **Run the installation**

    ```bash
    python3 -m pip install .
    ```

## 🎮 Usage

To use this Unix Shell, follow these steps:

1. **Start the shell by executing the command:**

    ```bash
    snake
    ```

2. **Enter commands in the interactive shell and press Enter to execute them.**

    Example commands:

    ```bash
    ls -l
    cd /path/to/directory
    mkdir new_directory
    ```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

Feel free to ⭐ star the repository if you find it interesting!
