# Working with Git Large File Storage (LFS)

When working with large CSV files in the PipMag project, we recommend using Git Large File Storage (LFS). Git LFS is an open-source Git extension that helps manage large files by replacing them with text pointers in your Git repository, while storing the actual file contents on a remote server. This results in a smaller repository size and faster operations.

This page provides a guide on how to install, setup, and use Git LFS for handling large CSV files.

## Installing Git LFS

To install Git LFS on macOS, you can use Homebrew:

```bash
brew install git-lfs
```

For Linux users, you can use conda/mamba:

```bash
mamba install -c conda-forge git-lfs
```

For other operating systems or methods, refer to the [official Git LFS installation instructions](https://git-lfs.github.com/).

## Setting Up Git LFS

After installing Git LFS, you need to set it up for your repository. Navigate to the root directory of your local clone of the Git repository and run:

```bash
git lfs install
```

This sets up Git LFS for your repository.

## Tracking Large Files with Git LFS

With Git LFS installed and set up, you can now start tracking large files. To track all CSV files with Git LFS, run:

```bash
git lfs track "*.csv"
```

This command tells Git LFS to track all CSV files in the repository. Adjust the "*.csv" pattern to match the specific files you want to track.

## Committing and Pushing Changes with Git LFS

After setting up Git LFS and specifying the files to track, you can commit and push your changes as usual:

```bash
git add .
git commit -m "Add large file"
git push
```

Git LFS will automatically handle the large files you specified and store them efficiently.

## Note

Remember, all users who interact with the large files will need to have Git LFS installed on their machines. Without Git LFS, users will only see the text pointers in their local repository instead of the actual file contents.

In the next section, we will guide you on how to maintain good commit practices in the [Commit Message Guidelines](./Commit-Message-Guidelines).

If you encounter any issues while working with Git LFS, feel free to raise an issue on the project's GitHub page. We are here to help!