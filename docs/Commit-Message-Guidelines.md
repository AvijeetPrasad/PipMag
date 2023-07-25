# Commit Message Guidelines

Maintaining clear and concise commit messages is an essential part of collaborating on a project. It helps to keep track of the changes made and understand the history of the project. 

In PipMag, we recommend using specific tags at the start of each commit message to easily identify the nature of the change. Here are the tags and what they represent:

| Tag | Description |
| --- | --- |
| `[DEV]` | Code development (including additions and deletions) |
| `[ADD]` | Adding new features |
| `[DEL]` | Removing files or routines |
| `[FIX]` | Fixes that occur during development, but which have essentially no impact on previous work |
| `[BUG]` | Bug with significant impact on previous work |
| `[OPT]` | Optimization |
| `[DBG]` | Debugging |
| `[ORG]` | Organizational changes, no changes to functionality |
| `[SYN]` | Typos and misspellings (including simple syntax error fixes) |
| `[DOC]` | Documentation only |
| `[REP]` | Repository related changes (e.g., changes in the ignore list, remove files) |
| `[UTL]` | Changes in utilities |

When making a commit, prepend your commit message with the appropriate tag. For example, if you're adding a new feature, your commit message might look like this:

```bash
git commit -m "[ADD] New feature for ..."
```

By adhering to these guidelines, we can maintain a clear and useful commit history that will benefit all collaborators.

In the next section, we will guide you on understanding the structure of the PipMag repository in the [Repository Structure](./Repository-structure.md).

If you have any questions or suggestions about these guidelines, feel free to raise an issue on the project's GitHub page. We are here to help!
