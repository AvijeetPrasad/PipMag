# Contributing to PipMag

Thank you for your interest in contributing to PipMag! This document outlines the guidelines and best practices for contributing to this project.

## Getting Started

### Prerequisites

Make sure you have the following software installed on your local machine:

- Git
- Python (or the programming language your project uses)
- Any other necessary dependencies. See [PipMag installation](https://github.com/AvijeetPrasad/PipMag/blob/main/docs/Installation.md)

### Forking the Repository

1. Navigate to the [GitHub page of this repository](https://github.com/AvijeetPrasad/PipMag).
2. Click on the "Fork" button at the top-right corner.

### Setting Up Local Environment

1. Clone your forked repository to your local machine:

   ```bash
   git clone https://github.com/<Your-Username>/PipMag.git
   ```

2. Add the upstream repository:

   ```bash
   git remote add upstream https://github.com/AvijeetPrasad/PipMag.git
   ```

## Contributing Workflow

### Creating an Issue

Before you start coding, please [create an issue](https://github.com/AvijeetPrasad/PipMag/issues) in the GitHub repository. Make sure the issue does not already exist. This issue will serve as a discussion forum for the bug you found or the new feature you propose.

### Creating a Pull Request Linked to an Issue

1. Create a new branch for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:

   ```bash
   git add .
   git commit -m "Add some feature"
   ```

3. Push the changes to your forked repository:

   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a pull request from your forked repository to the original repository. Please link this pull request to the issue you initially created. This ensures that the pull request and issue are automatically connected, providing context and easier tracking.

## Style Guidelines

### Coding Style

Please adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python (or equivalent for other languages).

### Commit Messages

- See our [Commit Message Guidelines](https://github.com/AvijeetPrasad/PipMag/blob/main/docs/Commit-Message-Guidelines.md)

## Additional Resources

- [Git Documentation](https://git-scm.com/docs)
- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

Thank you for contributing to PipMag!
