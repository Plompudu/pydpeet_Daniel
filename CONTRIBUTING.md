# Contributions

Any contributions to our project are much appreciated! Feel free to open new issues if you have questions regarding the project, any problems using PyDPEET, or a feature request.

**Please double-check whether an issue already exists!**

## Non-Developer Contributions

### Test PyDPEET

Feel free to use our software on your own battery data and give us feedback on the general workflow or missing features (see below). This helps us to further improve PyDPEET which benefits the whole community.

Use this repo for a local "editable" installation with the latest changes or install a stable version from PyPI (see [installation guide](https://eet-tub.github.io/pydpeet/installation.html)).

### Report Issue

If you encounter an error or any unexpected behaviour, please open a new issue. Use our template to describe your problem in detail and -- if applicable -- point to its location in the code or suggest a solution/approach for fixing it.

### Feature Request

If you feel like there is any functionality missing in PyDPEET, don't hesitate to open a new issue as well. Make sure to describe your feature in detail and -- if applicable -- give an approach for implementing it (or open a pull request yourself; see below).

Since this is an open-source, volunteer-driven project, please understand that we won't always be able to implement features right away and that we might reject feature requests which are out of scope for our project.

## For Developers

If you want to support our project by directly contributing code, please follow this workflow.
1. Create a new issue if there is no fitting existing one
    - In case of bigger contributions: discuss your solution/approach with the maintainers first to avoid unnecessary work
    - Assign yourself to the issue
2. Create a fork of our project on GitHub
3. Create a work branch from the most recent 'main' branch
    - Do not directly push to your fork's 'main' branch!
    - PRs are only accepted when they are coming from a work branch
4. Implement your changes on the work branch
    - Keep the scope of your changes as small as possible
    - Don't change unrelated code lines or sneak in "quick fixes" for unrelated issues
    - Optional: Add yourself to the 'AUTHORS.md'
    - Add an entry to the 'CHANGELOG.md'
5. Test your changes locally before creating a pull request (PR)
    - Option 1: Trigger workflows locally on your device using docker (does not work for all workflows)
    - Option 2: Trigger workflows on your fork using 'workflow_dispatch'
6. Create a PR on our main repo
    - Use 'fix', 'fixes', or similar to connect your PR to the corresponding issue(s) (see [GitHub docs](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/using-keywords-in-issues-and-pull-requests))
    - Describe the code changes in the PRs description
    - Optional: Request a review from one of the maintainers
7. Wait...
    - ... for the CI to finish
    - ... for feedback from the maintainers or other contributors
    - ... for code review from any reviewers
8. Discuss feedback, adjust your code accordingly, and make sure to resolve all threads
9. Your PR is now ready to be merged!
10. Wait for a maintainer to merge your PR
11. Once the PR has been merged...
    - ... delete your source branch
    - ... all mentioned issues should be automatically closed (see above)