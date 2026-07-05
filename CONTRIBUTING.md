# Contributing

## Branching Strategy

- **main**: This branch is for production-ready code. Only release versions are merged into main.
- **develop**: This is the primary development branch. All feature branches are merged into develop.
- **feature/***: These are for new features. They are branched off of develop and merged back into develop.
- **bugfix/***: These are for fixing bugs. They are branched off of develop and merged back into develop.
- **hotfix/***: These are for critical production bugs. They are branched off of main and merged back into main and develop.

## Commit Message Convention

We use Conventional Commits.

| Prefix     | Use                                     |
| ---------- | --------------------------------------- |
| **feat:**  | New feature                             |
| **fix:**   | Bug fix                                 |
| **docs:**  | Documentation                           |
| **style:** | Formatting only                         |
| **refactor:**| Code improvement without changing behavior|
| **test:**  | Tests                                   |
| **chore:** | Setup, dependencies, configs            |
| **perf:**  | Performance improvements                |

**Examples:**

- `feat: implement JWT authentication`
- `feat: add inquiry status API`
- `fix: resolve duplicate routing issue`
- `docs: update system architecture`
- `refactor: simplify AI decision engine`
- `test: add authentication API tests`
- `chore: configure Docker Compose`

## Pull Request Rules

Every PR should answer:

**What changed?**

Example:
> Added JWT authentication module.

**Why?**

Example:
> Required for secure investor and officer login.

**Testing**
- [ ] Unit Tested
- [ ] API Tested
- [ ] No Breaking Changes

**Reviewer**

Assign one teammate.

## Merge Rules

```
feature/*
        │
        ▼
develop
        │
        ▼
Sprint Testing
        │
        ▼
main
```

Never merge directly: `feature` → `main`

## Issue Workflow

Every issue should contain:

- **Title**
- **Description**
- **Acceptance Criteria**
- **Assignee**
- **Sprint**
- **Labels**

**Example:**

**Title**
> Implement JWT Authentication

**Acceptance Criteria**
- [ ] Login API
- [ ] JWT Token
- [ ] Refresh Token
- [ ] Role Validation

## Code Ownership

| Area       | Primary Owner |
| ---------- | ------------- |
| Backend    | Member 1      |
| AI         | Member 2      |
| Frontend   | Member 3      |
| DevOps     | Member 4      |

Everyone can contribute elsewhere through PRs, but this clarifies responsibility.

## Coding Expectations

- Follow existing coding styles.
- Write clear and concise code.
- Add comments to explain complex logic.
- Write unit tests for new features.
- Ensure all tests pass before creating a pull request.
