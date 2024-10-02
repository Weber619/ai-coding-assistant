import git
import os
from typing import List

class GitIntegration:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)

    def commit_changes(self, files: List[str], commit_message: str) -> None:
        self.repo.index.add(files)
        self.repo.index.commit(commit_message)

    def create_branch(self, branch_name: str) -> None:
        self.repo.git.checkout('-b', branch_name)

    def switch_branch(self, branch_name: str) -> None:
        self.repo.git.checkout(branch_name)

    def push_changes(self, remote_name: str = 'origin', branch_name: str = None) -> None:
        if branch_name is None:
            branch_name = self.repo.active_branch.name
        self.repo.git.push(remote_name, branch_name)

    def pull_changes(self, remote_name: str = 'origin', branch_name: str = None) -> None:
        if branch_name is None:
            branch_name = self.repo.active_branch.name
        self.repo.git.pull(remote_name, branch_name)

async def commit_improved_code(repo_path: str, file_path: str, commit_message: str) -> None:
    git_integration = GitIntegration(repo_path)
    git_integration.commit_changes([file_path], commit_message)
    print(f"Changes committed: {commit_message}")

async def main():
    repo_path = input("Enter the path to your Git repository: ")
    file_path = input("Enter the path to the file you want to commit: ")
    commit_message = input("Enter a commit message: ")

    try:
        await commit_improved_code(repo_path, file_path, commit_message)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())