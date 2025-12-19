---
description: "Task breakdown for Project Setup & Architecture feature"
---

# Tasks: Project Setup & Architecture

**Input**: Design documents from `/specs/002-project-setup/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create monorepo structure and initialize projects

- [X] T001 Create monorepo directory structure (backend/, frontend/, docker-compose.yml at root)
- [X] T002 [P] Initialize backend Python project with pyproject.toml
- [X] T003 [P] Initialize frontend Next.js project with package.json
- [X] T004 [P] Create root-level .gitignore (exclude .env, node_modules, __pycache__, .venv, .next)
- [X] T005 [P] Create backend/.gitignore (exclude .env, __pycache__, .pytest_cache, .venv)
- [X] T006 [P] Create frontend/.gitignore (exclude .env.local, .next, node_modules)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Backend Configuration

- [X] T007 [P] Create backend/requirements.txt with FastAPI, SQLModel, Alembic, asyncpg, uvicorn, pydantic-settings
- [X] T008 [P] Create backend/pyproject.toml with ruff, black, mypy, pytest configuration
- [X] T009 [P] Create backend/.env.example with DATABASE_URL, SECRET_KEY, CORS_ORIGINS, LOG_LEVEL
- [X] T010 Create backend/src/__init__.py (empty init file)
- [X] T011 Create backend/src/config.py with Pydantic Settings class for environment variables
- [X] T012 Create backend/src/database.py with async SQLModel engine, session factory, and get_session dependency

### Backend Database Models

- [X] T013 [P] Create backend/src/models/__init__.py
- [X] T014 [P] Create backend/src/models/user.py with User, UserBase, UserCreate, UserResponse models
- [X] T015 [P] Create backend/src/models/task.py with Task, TaskBase, TaskCreate, TaskUpdate, TaskResponse models

### Backend API Schemas

- [X] T016 [P] Create backend/src/schemas/__init__.py
- [X] T017 [P] Create backend/src/schemas/responses.py with StandardizedResponse, ErrorResponse, PaginationMeta models

### Backend Infrastructure

- [X] T018 [P] Create backend/src/services/__init__.py (empty for now)
- [X] T019 [P] Create backend/src/validators/__init__.py (empty for now)
- [X] T020 [P] Create backend/src/api/__init__.py

### Frontend Configuration

- [ ] T021 [P] Create frontend/package.json with Next.js 15, React 19, TypeScript, Tailwind, TanStack Query, Axios
- [ ] T022 [P] Create frontend/tsconfig.json with strict mode and path aliases (@/* for src/)
- [ ] T023 [P] Create frontend/next.config.ts with basic Next.js configuration
- [ ] T024 [P] Create frontend/tailwind.config.ts with Shadcn/ui integration
- [ ] T025 [P] Create frontend/.env.example with NEXT_PUBLIC_API_URL, NODE_ENV
- [ ] T026 Create frontend/app/layout.tsx with root layout and Providers wrapper
- [ ] T027 Create frontend/app/globals.css with Tailwind imports and Shadcn/ui CSS variables

### Frontend Components

- [X] T028 [P] Create frontend/components/providers.tsx with TanStack Query provider
- [X] T029 [P] Create frontend/lib/utils.ts with cn() utility function
- [X] T030 [P] Create frontend/lib/api.ts with Axios client and request/response interceptors
- [X] T031 [P] Create frontend/lib/validations.ts (empty for now)

### Initialize Shadcn/ui

- [X] T032 Run npx shadcn@latest init in frontend/ directory to initialize Shadcn/ui
- [X] T033 [P] Install Shadcn/ui button component in frontend/components/ui/button.tsx
- [X] T034 [P] Install Shadcn/ui card component in frontend/components/ui/card.tsx
- [X] T035 [P] Install Shadcn/ui toast component in frontend/components/ui/toast.tsx

### Database Migrations

- [ ] T036 Initialize Alembic in backend/ directory (alembic init alembic)
- [ ] T037 Configure backend/alembic/env.py for async engine and SQLModel metadata
- [ ] T038 Create backend/alembic.ini with database URL configuration
- [ ] T039 Create backend/alembic/versions/001_initial_schema.py migration (users and tasks tables with indexes)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Developer Environment Setup (Priority: P1)

**Goal**: Enable developers to clone repository and run full development environment with single command

**Independent Test**: New developer clones repo, runs docker-compose up, sees frontend at localhost:3000 and backend at localhost:8000

### Tests for User Story 1



> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**



- [X] T040 [P] [US1] Create backend/tests/__init__.py

- [X] T041 [P] [US1] Create backend/tests/conftest.py with test database fixtures and test client

- [X] T042 [P] [US1] Create backend/tests/unit/__init__.py

- [X] T043 [P] [US1] Create backend/tests/integration/__init__.py

- [X] T044 [US1] Create backend/tests/integration/test_health.py with smoke test for GET /health endpoint

- [X] T045 [P] [US1] Create frontend/tests/setup.ts with Vitest global setup and @testing-library/jest-dom

- [X] T046 [US1] Create frontend/tests/components/button.test.tsx with basic component test



### Backend Implementation for User Story 1



- [X] T047 [US1] Create backend/src/main.py with FastAPI app, CORS middleware, and route registration

- [X] T048 [US1] Create backend/src/api/health.py with GET /health endpoint (returns service status and database connectivity)

- [ ] T049 [US1] Test health endpoint manually with curl http://localhost:8000/health



### Frontend Implementation for User Story 1



- [X] T050 [US1] Create frontend/app/page.tsx with Hello World page displaying app name and description

- [X] T051 [US1] Create frontend/app/api/health/route.ts with frontend health check endpoint

- [ ] T052 [US1] Test Hello World page manually in browser at localhost:3000



### Docker Configuration for User Story 1



- [X] T053 [P] [US1] Create backend/Dockerfile.dev with Python 3.13, hot reload, volume mounts

- [X] T054 [P] [US1] Create backend/Dockerfile with production-optimized multi-stage build

- [X] T055 [P] [US1] Create frontend/Dockerfile.dev with Node 22, hot reload, volume mounts

- [X] T056 [P] [US1] Create frontend/Dockerfile with production-optimized multi-stage build

- [X] T057 [US1] Create docker-compose.yml with backend, frontend services, health checks, volume mounts, and port mappings



### Documentation for User Story 1



- [ ] T058 [P] [US1] Create backend/README.md with backend setup instructions and commands

- [ ] T059 [P] [US1] Create frontend/README.md with frontend setup instructions and commands

- [ ] T060 [US1] Create root README.md with project overview, quick start guide, and links to backend/frontend READMEs



### Verification for User Story 1



- [ ] T061 [US1] Run docker-compose up and verify both services start successfully

- [ ] T062 [US1] Verify frontend accessible at localhost:3000 and displays Hello World page

- [ ] T063 [US1] Verify backend health endpoint responds at localhost:8000/health

- [ ] T064 [US1] Verify hot reload works (edit frontend/app/page.tsx, see changes without restart)

- [ ] T065 [US1] Verify hot reload works (edit backend/src/api/health.py, see changes without restart)

- [ ] T066 [US1] Run backend tests with pytest backend/tests/

- [ ] T067 [US1] Run frontend tests with npm test in frontend/



**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently



---



## Phase 4: User Story 2 - Database Connectivity Verification (Priority: P2)



**Goal**: Verify application can successfully connect to Neon PostgreSQL database and run migrations



**Independent Test**: Health endpoint reports database connection status, migrations run successfully



### Tests for User Story 2



- [ ] T068 [US2] Update backend/tests/integration/test_health.py to verify database_connected field in health response

- [ ] T069 [US2] Create backend/tests/integration/test_database.py with test for database session creation

- [ ] T070 [US2] Create backend/tests/integration/test_migrations.py with test for migration success



### Implementation for User Story 2



- [ ] T071 [US2] Update backend/src/database.py to add database connectivity check function

- [ ] T072 [US2] Update backend/src/api/health.py to include database connectivity status in response

- [ ] T073 [US2] Create backend/.env file with actual Neon DATABASE_URL (developer must provide credentials)

- [ ] T074 [US2] Run alembic upgrade head to apply initial migration to Neon database

- [ ] T075 [US2] Verify tables created in Neon console (users, tasks tables exist)

- [ ] T076 [US2] Update backend/src/main.py to add startup event for database connection verification



### Error Handling for User Story 2



- [ ] T077 [US2] Add error handling for invalid database credentials in backend/src/database.py

- [ ] T078 [US2] Add logging for database connection success/failure in backend/src/main.py

- [ ] T079 [US2] Update backend health endpoint to return 503 status if database unreachable



### Documentation for User Story 2



- [ ] T080 [US2] Update specs/002-project-setup/quickstart.md with Neon database setup instructions

- [ ] T081 [US2] Update backend/README.md with migration commands and troubleshooting



### Verification for User Story 2



- [ ] T082 [US2] Run docker-compose up and verify backend connects to Neon database successfully

- [ ] T083 [US2] Query health endpoint and verify database_connected: true in response

- [ ] T084 [US2] Run alembic current and verify migration version matches HEAD

- [ ] T085 [US2] Test with invalid database URL and verify clear error messages in logs

- [ ] T086 [US2] Run backend tests with pytest backend/tests/ and verify all tests pass



**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently



---



## Phase 5: User Story 3 - Code Quality Tools Integration (Priority: P3)



**Goal**: Integrate automated code quality checks into workflow for consistent code standards



**Independent Test**: Write code with violations, run linters, verify violations are detected and reported



### Backend Code Quality Setup



- [ ] T087 [P] [US3] Configure ruff in backend/pyproject.toml with rules (line-length: 100, select: E, F, I, N, W)

- [ ] T088 [P] [US3] Configure black in backend/pyproject.toml with line-length: 100

- [ ] T089 [P] [US3] Configure mypy in backend/pyproject.toml with strict mode enabled

- [ ] T090 [US3] Add scripts to backend/pyproject.toml (lint, format, type-check)



### Frontend Code Quality Setup



- [ ] T091 [P] [US3] Create frontend/.eslintrc.json with TypeScript and Next.js rules

- [ ] T092 [P] [US3] Create frontend/.prettierrc with formatting rules (semi: true, singleQuote: true, tabWidth: 2)

- [ ] T093 [US3] Add lint, format, type-check scripts to frontend/package.json



### Tests for User Story 3



- [ ] T094 [US3] Create backend/tests/unit/test_code_quality.py to verify code passes linting

- [ ] T095 [US3] Test ruff check passes on backend/src/ with no violations

- [ ] T096 [US3] Test black --check passes on backend/src/ with no violations

- [ ] T097 [US3] Test mypy passes on backend/src/ with no type errors

- [ ] T098 [US3] Test ESLint passes on frontend with no violations

- [ ] T099 [US3] Test Prettier --check passes on frontend with no formatting issues

- [ ] T100 [US3] Test TypeScript compilation (tsc --noEmit) passes with no errors



### Implementation for User Story 3



- [ ] T101 [P] [US3] Run ruff format backend/src/ to format all backend code

- [ ] T102 [P] [US3] Run black backend/src/ to format all backend code

- [ ] T103 [P] [US3] Run prettier --write frontend/ to format all frontend code

- [ ] T104 [US3] Fix any remaining linting issues identified by ruff check

- [ ] T105 [US3] Fix any remaining linting issues identified by ESLint

- [ ] T106 [US3] Fix any type errors identified by mypy and TypeScript compiler



### Documentation for User Story 3



- [ ] T107 [US3] Update backend/README.md with code quality commands (lint, format, type-check)

- [ ] T108 [US3] Update frontend/README.md with code quality commands (lint, format, type-check)

- [ ] T109 [US3] Update root README.md with code quality section and pre-commit recommendations



### Verification for User Story 3



- [ ] T110 [US3] Run ruff check backend/src/ and verify zero violations

- [ ] T111 [US3] Run black --check backend/src/ and verify all files formatted correctly

- [ ] T112 [US3] Run mypy backend/src/ and verify no type errors

- [ ] T113 [US3] Run npm run lint in frontend/ and verify zero violations

- [ ] T114 [US3] Run npm run format:check in frontend/ and verify all files formatted correctly

- [ ] T115 [US3] Run npm run type-check in frontend/ and verify no type errors

- [ ] T116 [US3] Verify all code quality checks pass before committing



**Checkpoint**: All code quality tools are integrated and passing



---



## Phase 6: User Story 4 - Testing Infrastructure Ready (Priority: P3)



**Goal**: Set up testing frameworks for both frontend and backend with basic smoke tests



**Independent Test**: Write simple test, run test command, verify test executes and results are reported



### Backend Testing Setup



- [X] T117 [P] [US4] Add pytest, pytest-asyncio, pytest-cov, httpx to backend/requirements.txt

- [X] T118 [P] [US4] Configure pytest in backend/pyproject.toml (testpaths, asyncio_mode, coverage)

- [X] T119 [US4] Update backend/tests/conftest.py with comprehensive fixtures (async_client, test_db_session, mock_user, mock_task)



### Frontend Testing Setup



- [X] T120 [P] [US4] Add vitest, @testing-library/react, @testing-library/jest-dom, jsdom to frontend/package.json

- [X] T121 [P] [US4] Create frontend/vitest.config.ts with jsdom environment and coverage configuration

- [X] T122 [US4] Update frontend/tests/setup.ts with testing library matchers



### Backend Smoke Tests



- [ ] T123 [P] [US4] Create backend/tests/integration/test_api_smoke.py with test for app startup

- [ ] T124 [P] [US4] Create backend/tests/unit/test_config.py with test for environment variable loading

- [ ] T125 [P] [US4] Create backend/tests/unit/test_models.py with test for User and Task model creation



### Frontend Smoke Tests



- [X] T126 [P] [US4] Update frontend/tests/components/button.test.tsx with rendering and click tests

- [ ] T127 [P] [US4] Create frontend/tests/app/page.test.tsx with test for Hello World page rendering

- [ ] T128 [P] [US4] Create frontend/tests/lib/utils.test.ts with test for cn() utility function



### Test Coverage Configuration



- [ ] T129 [US4] Configure coverage reporting in backend/pyproject.toml (exclude tests, alembic, __init__)

- [ ] T130 [US4] Configure coverage reporting in frontend/vitest.config.ts (threshold: 70%)

- [X] T131 [US4] Add test:coverage scripts to backend/pyproject.toml and frontend/package.json



### Documentation for User Story 4



- [ ] T132 [US4] Update backend/README.md with testing commands (test, test:coverage, test:watch)

- [ ] T133 [US4] Update frontend/README.md with testing commands (test, test:coverage, test:watch)

- [ ] T134 [US4] Update root README.md with testing section and test pyramid explanation



### Verification for User Story 4



- [X] T135 [US4] Run pytest backend/tests/ and verify all backend tests pass (100% passing)

- [ ] T136 [US4] Run pytest --cov backend/tests/ and verify coverage report generated

- [X] T137 [US4] Run npm test in frontend/ and verify all frontend tests pass (100% passing)

- [ ] T138 [US4] Run npm run test:coverage in frontend/ and verify coverage report generated

- [ ] T139 [US4] Verify test failure detection by intentionally breaking a test and confirming it fails

- [ ] T140 [US4] 

 

 Verify all smoke tests are independent and can run in isolation

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, documentation, and validation

### Documentation

- [ ] T141 [P] Verify specs/002-project-setup/quickstart.md is complete and accurate
- [ ] T142 [P] Verify all README files are up-to-date with correct commands and links
- [ ] T143 [P] Create root-level CONTRIBUTING.md with development workflow guidelines
- [ ] T144 Update root README.md with architecture diagram and technology stack overview

### Final Validation

- [ ] T145 Fresh clone test: Clone repository to new directory, follow quickstart.md, verify setup completes within 10 minutes
- [ ] T146 Verify docker-compose up starts both services with health checks passing within 30 seconds
- [ ] T147 Verify all environment variables documented in .env.example files
- [ ] T148 Verify all success criteria from spec.md are met (SC-001 through SC-010)

### Code Quality Final Check

- [ ] T149 Run all backend code quality checks (ruff, black, mypy) and verify zero violations
- [ ] T150 Run all frontend code quality checks (ESLint, Prettier, TypeScript) and verify zero violations
- [ ] T151 Run all backend tests and verify 100% passing
- [ ] T152 Run all frontend tests and verify 100% passing

### Security & Best Practices

- [ ] T153 Verify all .env files are in .gitignore (backend/.env, frontend/.env.local)
- [ ] T154 Verify all .env.example files use placeholder values (no real credentials)
- [ ] T155 Verify CORS is configured with explicit origins (no wildcard in production config)
- [ ] T156 Verify all Docker images use specific version tags (no :latest)

### Performance Verification

- [ ] T157 Verify hot reload works within 2 seconds for both frontend and backend
- [ ] T158 Verify Docker build times are reasonable (<5 minutes for first build)
- [ ] T159 Verify health check endpoints respond within 100ms

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion AND User Story 1 completion (needs Docker environment)
- **User Story 3 (Phase 5)**: Depends on Foundational phase completion AND User Story 1 completion (needs code to lint)
- **User Story 4 (Phase 6)**: Depends on Foundational phase completion AND User Story 1 completion (needs code to test)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Requires User Story 1 (needs Docker environment running to test database connectivity)
- **User Story 3 (P3)**: Requires User Story 1 (needs codebase to run quality checks on)
- **User Story 4 (P3)**: Requires User Story 1 (needs test infrastructure and code to test)

### Within Each User Story

- Tests (if included) should be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- Within Phase 1 (Setup): All tasks marked [P] can run in parallel
- Within Phase 2 (Foundational): All tasks marked [P] can run in parallel within each subsection
- Within User Story tests: All test creation tasks marked [P] can run in parallel
- Within User Story implementation: Tasks marked [P] working on different files can run in parallel
- User Stories 3 and 4 can run in parallel after User Story 1 is complete

---

## Implementation Strategy

### MVP First (Critical Path)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Developer Environment Setup)
4. **STOP and VALIDATE**: Test that docker-compose up works end-to-end
5. Complete Phase 4: User Story 2 (Database Connectivity)
6. **STOP and VALIDATE**: Test database connection and migrations
7. Complete Phase 5: User Story 3 (Code Quality) in parallel with Phase 6: User Story 4 (Testing)
8. Complete Phase 7: Polish

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP environment running
3. Add User Story 2 → Test independently → Database integrated
4. Add User Stories 3 & 4 in parallel → Test independently → Full development workflow ready
5. Polish → Production-ready development environment

### Time Estimates

- **Phase 1 (Setup)**: 30 minutes
- **Phase 2 (Foundational)**: 2-3 hours
- **Phase 3 (User Story 1)**: 3-4 hours
- **Phase 4 (User Story 2)**: 1-2 hours
- **Phase 5 (User Story 3)**: 1-2 hours
- **Phase 6 (User Story 4)**: 1-2 hours
- **Phase 7 (Polish)**: 1 hour
- **Total**: 10-15 hours for complete implementation

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability (US1, US2, US3, US4)
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD discipline)
- Commit after each task or logical group (use Conventional Commits format)
- Stop at any checkpoint to validate story independently
- Docker Compose is the primary development environment - all manual testing should be done via Docker
- Neon PostgreSQL is required - no local PostgreSQL needed (simplifies setup)
- Follow ADR-0004 standardized API response format for all endpoints
- Use UUID primary keys for all database entities (security best practice)
- All paths are absolute from repository root
- Hot reload must work for both frontend and backend during development
- Code quality checks must pass before committing (enforce with pre-commit hooks in future)
- Test coverage targets: Backend 80%, Frontend 70% (enforced in future features, not this setup)
