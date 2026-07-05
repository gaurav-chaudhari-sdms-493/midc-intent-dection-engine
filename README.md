# MIDC Intent Detection Engine

## Development Workflow

Our development process follows a structured workflow to ensure code quality and collaboration.

1.  **Issue Creation**: Every new feature or bug fix starts with a GitHub Issue. This provides a clear description of the task and its acceptance criteria.

2.  **Branching**: Create a new feature branch from the `develop` branch. Name your branch descriptively (e.g., `feature/user-authentication`).

3.  **Implementation**: Write the code for the feature or bug fix in your feature branch.

4.  **Local Testing**: Thoroughly test your changes on your local machine to ensure they work as expected.

5.  **Committing**: Commit your changes with a clear and descriptive commit message, following our [Conventional Commits](CONTRIBUTING.md#commit-message-convention) standard.

6.  **Pushing**: Push your feature branch to the remote repository.

7.  **Pull Request**: Open a pull request from your feature branch to the `develop` branch. Fill out the pull request template, explaining what you changed and why.

8.  **Code Review**: At least one other developer must review and approve your pull request. This ensures code quality and knowledge sharing.

9.  **Merging**: Once approved, the pull request is merged into the `develop` branch.

10. **Sprint Testing**: At the end of each sprint, the `develop` branch is deployed to a staging environment for further testing.

11. **Release**: After successful sprint testing, the `develop` branch is merged into the `main` branch to be released to production.
