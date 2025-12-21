# Tasks: Landing Page and UI Enhancement Suite

**Input**: Design documents from `/specs/006-landing-page-ui/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Tests are OPTIONAL in this specification - tasks focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/` (Next.js App Router structure)
- Backend: `backend/src/models/`, `backend/src/services/`, `backend/src/api/routes/`, `backend/src/schemas/`
- Frontend: `frontend/app/`, `frontend/components/`, `frontend/hooks/`, `frontend/lib/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure project for new features

- [X] T001 [P] Install frontend dependencies: framer-motion, recharts, @dnd-kit/core, @dnd-kit/sortable, @use-gesture/react, cmdk, date-fns, zustand
- [X] T002 [P] Verify backend dependencies are current: fastapi>=0.100, sqlmodel, alembic, pydantic>=2.0
- [X] T003 [P] Add Shadcn/ui components: command, badge, calendar, tooltip, popover, select
- [X] T004 [P] Create frontend/lib/animations.ts with Framer Motion animation variants
- [X] T005 [P] Create frontend/lib/theme-store.ts Zustand store for theme preferences
- [X] T006 [P] Configure Tailwind CSS for custom animation keyframes in frontend/tailwind.config.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create Alembic migration: Add due_date TIMESTAMPTZ to tasks table in backend/alembic/versions/
- [X] T008 [P] Create Alembic migration: Add notes TEXT and manual_order INTEGER to tasks table in backend/alembic/versions/
- [X] T009 [P] Extend Task model in backend/src/models/task.py with due_date, notes, manual_order, template_id, recurrence_pattern_id fields
- [X] T010 [P] Create backend/src/schemas/task_schemas.py with extended TaskResponse, TaskCreate, TaskUpdate schemas including new fields
- [X] T011 Run alembic upgrade head to apply foundational migrations
- [X] T012 [P] Update frontend/types/task.ts to include due_date, notes, manual_order, tags, subtasks, recurrence_pattern fields
- [X] T013 [P] Extend useTasks hook in frontend/hooks/useTasks.ts to support filtering parameters (status, priority, tags, due_date_range, search)
- [X] T014 [P] Create frontend/lib/date-utils.ts with due date formatting and color coding logic (overdue=red, due_soon=orange, upcoming=blue)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - First-Time Visitor Landing Experience (Priority: P1) 🎯 MVP

**Goal**: Create professional landing page that converts visitors to users with animated hero, features showcase, interactive demos, testimonials, and pricing

**Independent Test**: Navigate to root URL (/), verify all landing page sections load with smooth scroll-triggered animations, CTA buttons are functional and link to signup flow, page achieves 90+ Lighthouse score

### Implementation for User Story 1

- [X] T015 [P] [US1] Create frontend/app/page.tsx as landing page with Server Component structure
- [X] T016 [P] [US1] Create frontend/components/landing/Hero.tsx with animated gradient background, headline, subheadline, floating task cards with parallax
- [X] T017 [P] [US1] Create frontend/components/landing/Features.tsx grid with 6+ feature cards showing icons, titles, descriptions, hover effects
- [X] T018 [P] [US1] Create frontend/components/landing/Demo.tsx with tabbed navigation (List/Kanban/Calendar/Dashboard) and animated previews
- [X] T019 [P] [US1] Create frontend/components/landing/Testimonials.tsx with rotating quotes and avatar images
- [X] T020 [P] [US1] Create frontend/components/landing/Pricing.tsx section with Free/Premium tier comparison
- [X] T021 [P] [US1] Create frontend/components/landing/CTA.tsx final call-to-action section with gradient background
- [X] T022 [P] [US1] Create frontend/components/landing/Footer.tsx with navigation links, social icons, copyright
- [X] T023 [US1] Implement scroll-triggered animations in landing page using Framer Motion useInView hook
- [X] T024 [US1] Add responsive breakpoints for mobile (320px-767px), tablet (768px-1024px), desktop (1920px+) in all landing components
- [X] T025 [US1] Optimize landing page images and implement lazy loading for below-the-fold sections
- [X] T026 [US1] Configure landing page metadata in frontend/app/page.tsx for SEO (title, description, Open Graph tags)

**Checkpoint**: At this point, User Story 1 should be fully functional - landing page loads, animations play, CTAs link to signup

---

## Phase 4: User Story 2 - Task Management with Due Dates (Priority: P1)

**Goal**: Enable users to assign due dates to tasks with visual indicators (red=overdue, orange=soon, blue=upcoming) and filter by date ranges

**Independent Test**: Create tasks with various due dates (today, tomorrow, next week, past date), verify color-coded badges appear, apply "Today"/"This Week"/"Overdue" filters work correctly, celebration animation plays on completion

### Implementation for User Story 2

- [X] T027 [P] [US2] Add GET /api/v1/tasks/due endpoint in backend/src/api/routes/tasks.py with filter parameter (overdue/today/tomorrow/this_week/next_week/no_due_date)
- [X] T028 [P] [US2] Add PATCH /api/v1/tasks/{task_id}/due-date endpoint in backend/src/api/routes/tasks.py to set/update/remove due dates
- [X] T029 [P] [US2] Add GET /api/v1/tasks/due/stats endpoint in backend/src/api/routes/tasks.py returning counts for overdue/today/this_week/no_due_date
- [X] T030 [US2] Implement due date filtering logic in backend/src/services/task_service.py with timezone handling
- [X] T031 [US2] Add due_date_status calculation (overdue/due_soon/upcoming/none) in backend/src/services/task_service.py
- [X] T032 [P] [US2] Create frontend/components/tasks/DueDatePicker.tsx with date selection and timezone display
- [X] T033 [P] [US2] Create frontend/components/tasks/DueDateBadge.tsx with color-coded styling based on due date status
- [X] T034 [P] [US2] Create frontend/components/tasks/DueDateFilters.tsx with quick filter chips (Today/This Week/Overdue/No Due Date)
- [X] T035 [US2] Add due date field to CreateTaskDialog.tsx and EditTaskDialog.tsx in frontend/components/tasks/
- [X] T036 [US2] Update TaskCard.tsx in frontend/components/tasks/ to display DueDateBadge component
- [X] T037 [US2] Implement celebration animation (confetti) on task completion when due date is met using frontend/lib/animations.ts
- [X] T038 [US2] Add relative time display ("Due tomorrow", "3 days overdue") in DueDateBadge.tsx using date-fns

**Checkpoint**: At this point, User Story 2 should be fully functional - due dates can be set, visual indicators appear, filters work independently

---

## Phase 5: User Story 3 - Task Organization with Tags (Priority: P1)

**Goal**: Allow users to create color-coded tags, assign multiple tags to tasks, and filter task list by tags

**Independent Test**: Create tags with custom colors, assign multiple tags to a single task, filter by tag and verify only tagged tasks appear, edit tag name/color and verify changes reflect across all tasks

### Implementation for User Story 3

- [ ] T039 [P] [US3] Create Alembic migration: Create tags table (id, user_id, name, color, timestamps) in backend/alembic/versions/
- [ ] T040 [P] [US3] Create Alembic migration: Create task_tags join table (task_id, tag_id, created_at) in backend/alembic/versions/
- [ ] T041 [P] [US3] Run alembic upgrade head to apply tag migrations
- [ ] T042 [P] [US3] Create backend/src/models/tag.py with Tag model (id, user_id, name VARCHAR(50), color VARCHAR(7), timestamps)
- [ ] T043 [P] [US3] Create backend/src/models/task_tag.py with TaskTag join model (task_id, tag_id, created_at)
- [ ] T044 [P] [US3] Create backend/src/schemas/tag_schemas.py with TagCreate, TagUpdate, TagResponse schemas including validation
- [ ] T045 [US3] Create backend/src/services/tag_service.py with CRUD operations (create_tag, get_tags, update_tag, delete_tag)
- [ ] T046 [US3] Implement tag assignment logic in backend/src/services/task_service.py (add_tags_to_task, remove_tags_from_task)
- [ ] T047 [P] [US3] Add GET /api/v1/tags endpoint in backend/src/api/routes/tags.py for listing user's tags
- [ ] T048 [P] [US3] Add POST /api/v1/tags endpoint in backend/src/api/routes/tags.py for creating new tag
- [ ] T049 [P] [US3] Add PATCH /api/v1/tags/{tag_id} endpoint in backend/src/api/routes/tags.py for updating tag
- [ ] T050 [P] [US3] Add DELETE /api/v1/tags/{tag_id} endpoint in backend/src/api/routes/tags.py for deleting tag
- [ ] T051 [P] [US3] Add POST /api/v1/tasks/{task_id}/tags endpoint in backend/src/api/routes/tasks.py for assigning tags
- [ ] T052 [P] [US3] Add DELETE /api/v1/tasks/{task_id}/tags endpoint in backend/src/api/routes/tasks.py for removing tags
- [ ] T053 [P] [US3] Create frontend/hooks/useTags.ts with useQuery for fetching tags, useMutation for CRUD operations
- [ ] T054 [P] [US3] Create frontend/components/tasks/TagPicker.tsx with existing tag selection and new tag creation with color picker
- [ ] T055 [P] [US3] Create frontend/components/tasks/TagBadge.tsx displaying tag name with assigned color background
- [ ] T056 [P] [US3] Create frontend/components/tasks/TagFilters.tsx with filter chips for each tag
- [ ] T057 [P] [US3] Create frontend/components/tasks/TagManagement.tsx dialog for managing user's tags (edit/delete)
- [ ] T058 [US3] Add tag picker to CreateTaskDialog.tsx and EditTaskDialog.tsx in frontend/components/tasks/
- [ ] T059 [US3] Update TaskCard.tsx in frontend/components/tasks/ to display TagBadge components
- [ ] T060 [US3] Extend useTasks hook in frontend/hooks/useTasks.ts to support tag filtering (tags query parameter)
- [ ] T061 [US3] Update backend/src/services/task_service.py to load tasks with tags relationship using selectinload

**Checkpoint**: At this point, User Story 3 should be fully functional - tags can be created/managed, tasks can be tagged, tag filtering works independently

---

## Phase 6: User Story 4 - Beautiful Visual Experience with Animations (Priority: P2)

**Goal**: Add smooth animations for task completion, card hover effects, view transitions, drag interactions, and dialog appearances

**Independent Test**: Mark task complete and verify checkmark + confetti animation plays, hover over task card and verify elevation effect, toggle between list/grid views and verify smooth layout transition, drag task and verify smooth follow with drop zone highlights

### Implementation for User Story 4

- [ ] T062 [P] [US4] Define animation variants in frontend/lib/animations.ts: fadeIn, slideIn, scaleIn, confetti, cardHover, cardExit
- [ ] T063 [P] [US4] Wrap TaskCard.tsx in frontend/components/tasks/ with motion.div and add initial/animate/exit props
- [ ] T064 [P] [US4] Implement confetti animation component in frontend/components/ui/confetti.tsx using canvas-confetti library
- [ ] T065 [US4] Add confetti trigger to task toggle mutation onSuccess callback in frontend/hooks/useTasks.ts
- [ ] T066 [US4] Add hover elevation effect to TaskCard.tsx using Framer Motion whileHover prop
- [ ] T067 [US4] Implement stagger animation for task list in TaskList.tsx using Framer Motion staggerChildren
- [ ] T068 [US4] Add exit animation to deleted tasks in TaskList.tsx with AnimatePresence wrapper
- [ ] T069 [US4] Implement view transition animation between list/grid layouts in frontend/app/tasks/page.tsx
- [ ] T070 [US4] Add scale + fade animation to dialog/modal components in frontend/components/ui/dialog.tsx
- [ ] T071 [US4] Add backdrop blur effect to dialog overlays in frontend/components/ui/dialog.tsx
- [ ] T072 [US4] Respect prefers-reduced-motion media query by conditionally disabling animations in frontend/lib/animations.ts

**Checkpoint**: At this point, User Story 4 should be fully functional - all animations play smoothly at 60fps, respecting user motion preferences

---

## Phase 7: User Story 5 - Global Search and Quick Filters (Priority: P2)

**Goal**: Enable instant search across task titles, descriptions, notes and provide quick filter chips for common views (Today/High Priority/This Week)

**Independent Test**: Type in search bar and verify instant filtering with highlighted matches, click quick filter chip and verify only matching tasks appear, combine search + filters and verify AND logic works, clear search and verify all tasks reappear

### Implementation for User Story 5

- [ ] T073 [P] [US5] Add GET /api/v1/tasks/search endpoint in backend/src/api/routes/search.py with query parameters (q, status, priority, tags, due_date_from, due_date_to, has_due_date, has_notes)
- [ ] T074 [P] [US5] Add GET /api/v1/tasks/autocomplete endpoint in backend/src/api/routes/search.py for search suggestions
- [ ] T075 [P] [US5] Add GET /api/v1/tasks/quick-filters endpoint in backend/src/api/routes/search.py returning filter options with counts
- [ ] T076 [US5] Implement search logic in backend/src/services/task_service.py with ILIKE queries for title/description/notes
- [ ] T077 [US5] Implement combined filter logic in backend/src/services/task_service.py with AND conditions for multiple filters
- [ ] T078 [P] [US5] Create frontend/components/tasks/SearchBar.tsx with debounced input (300ms delay) and clear button
- [ ] T079 [P] [US5] Create frontend/components/tasks/QuickFilters.tsx with chips for Today/This Week/High Priority/Overdue
- [ ] T080 [P] [US5] Create frontend/hooks/useSearch.ts with debounced search query and filter state management
- [ ] T081 [US5] Update TaskList.tsx to highlight search terms in yellow within task cards
- [ ] T082 [US5] Add search bar and quick filters to frontend/app/tasks/page.tsx above task list
- [ ] T083 [US5] Implement filter chip active state styling in QuickFilters.tsx (highlighted when active)
- [ ] T084 [US5] Add filter combination logic in useSearch.ts to build query parameters for useTasks hook
- [ ] T085 [US5] Display "No results found" empty state in TaskList.tsx when search/filters return no matches

**Checkpoint**: At this point, User Story 5 should be fully functional - search is instant with highlighting, quick filters work, combinations apply AND logic

---

## Phase 8: User Story 6 - Dashboard Overview with Statistics (Priority: P2)

**Goal**: Provide dashboard with stat cards (pending/completed/overdue counts), 7-day completion trend chart, and priority breakdown chart

**Independent Test**: Navigate to /tasks/dashboard, verify stat cards show correct counts, verify 7-day line chart renders with accurate data, verify priority pie chart displays correct proportions, click stat card and navigate to filtered view

### Implementation for User Story 6

- [ ] T086 [P] [US6] Add GET /api/v1/tasks/analytics/stats endpoint in backend/src/api/routes/tasks.py returning pending_count, completed_today_count, overdue_count
- [ ] T087 [P] [US6] Add GET /api/v1/tasks/analytics/completion-trend endpoint in backend/src/api/routes/tasks.py with days parameter (default 7)
- [ ] T088 [P] [US6] Add GET /api/v1/tasks/analytics/priority-breakdown endpoint in backend/src/api/routes/tasks.py returning counts by priority
- [ ] T089 [US6] Implement analytics calculations in backend/src/services/task_service.py with date range queries
- [ ] T090 [P] [US6] Create frontend/app/tasks/dashboard/page.tsx as dashboard route
- [ ] T091 [P] [US6] Create frontend/components/dashboard/StatsCards.tsx with three cards (pending, completed today, overdue) clickable to filter
- [ ] T092 [P] [US6] Create frontend/components/dashboard/CompletionTrendChart.tsx using Recharts LineChart for 7-day completion data
- [ ] T093 [P] [US6] Create frontend/components/dashboard/PriorityBreakdownChart.tsx using Recharts PieChart for priority distribution
- [ ] T094 [P] [US6] Create frontend/hooks/useAnalytics.ts with queries for stats, completion trend, priority breakdown
- [ ] T095 [US6] Add empty state illustration to dashboard when user has no tasks
- [ ] T096 [US6] Implement click handlers on stat cards to navigate to filtered task list views
- [ ] T097 [US6] Add loading skeletons to dashboard components while data fetches

**Checkpoint**: At this point, User Story 6 should be fully functional - dashboard displays analytics, charts render correctly, empty states handle zero data

---

## Phase 9: User Story 7 - Kanban Board View (Priority: P2)

**Goal**: Provide kanban board with three columns (To Do, In Progress, Done) and drag-and-drop between columns to update task status

**Independent Test**: Navigate to /tasks/kanban, verify tasks appear in columns by status, drag task from To Do to In Progress and verify status updates automatically, verify column headers show task counts

### Implementation for User Story 7

- [ ] T098 [P] [US7] Create frontend/app/tasks/kanban/page.tsx as kanban board route
- [ ] T099 [P] [US7] Create frontend/components/kanban/KanbanBoard.tsx with DndContext from @dnd-kit/core
- [ ] T100 [P] [US7] Create frontend/components/kanban/KanbanColumn.tsx with useDroppable from @dnd-kit/core showing column header and task count
- [ ] T101 [P] [US7] Create frontend/components/kanban/DraggableTaskCard.tsx with useDraggable and useSortable from @dnd-kit
- [ ] T102 [US7] Implement drag handlers in KanbanBoard.tsx to update task status via API on drop
- [ ] T103 [US7] Add optimistic UI update to kanban drag operation using TanStack Query setQueryData
- [ ] T104 [US7] Add drop zone highlighting in KanbanColumn.tsx when dragging over column
- [ ] T105 [US7] Implement "Add Task" button in each column header that opens CreateTaskDialog with appropriate status pre-filled
- [ ] T106 [US7] Add filter support to kanban view (filtered tasks appear in their respective columns)
- [ ] T107 [US7] Add drag overlay animation with semi-transparent task card following cursor

**Checkpoint**: At this point, User Story 7 should be fully functional - kanban board displays tasks by status, drag-and-drop updates status, counts update

---

## Phase 10: User Story 8 - Calendar View with Due Date Visualization (Priority: P2)

**Goal**: Display tasks on a monthly calendar organized by due date with drag-to-reschedule functionality

**Independent Test**: Navigate to /tasks/calendar, verify tasks appear on their due dates as colored badges, drag task to different date and verify due date updates, click calendar day and verify task list for that date appears

### Implementation for User Story 8

- [ ] T108 [P] [US8] Create frontend/app/tasks/calendar/page.tsx as calendar view route
- [ ] T109 [P] [US8] Create frontend/components/calendar/CalendarView.tsx with custom monthly calendar grid implementation
- [ ] T110 [P] [US8] Create frontend/components/calendar/CalendarDayCell.tsx displaying date and tasks as colored badges
- [ ] T111 [P] [US8] Create frontend/components/calendar/CalendarTaskCard.tsx compact task card for calendar display
- [ ] T112 [P] [US8] Create frontend/components/calendar/DayTasksPanel.tsx sidebar showing all tasks for selected date
- [ ] T113 [US8] Implement month navigation (previous/next month buttons) in CalendarView.tsx with ±12 month constraint
- [ ] T114 [US8] Implement drag-to-reschedule using @use-gesture/react in CalendarDayCell.tsx
- [ ] T115 [US8] Update task due_date via API when dropped on new calendar date
- [ ] T116 [US8] Add click handler to calendar day to open DayTasksPanel with filtered tasks
- [ ] T117 [US8] Implement "Create Task" button in DayTasksPanel that pre-fills selected date
- [ ] T118 [US8] Add color coding to calendar task badges based on priority (red=high, yellow=medium, blue=low)
- [ ] T119 [US8] Handle overflow when calendar day has more tasks than fit (show "+N more" badge)

**Checkpoint**: At this point, User Story 8 should be fully functional - calendar displays tasks by due date, drag-to-reschedule works, day panel shows task details

---

## Phase 11: User Story 9 - Keyboard Shortcuts and Command Palette (Priority: P3)

**Goal**: Enable power users to perform actions via keyboard shortcuts (N=new, E=edit, Delete=delete) and access command palette (Cmd/Ctrl+K) for action search

**Independent Test**: Press Cmd/Ctrl+K and verify command palette opens, type action name and verify filtering works, press N and verify new task dialog opens, hover over buttons and verify shortcut tooltips appear

### Implementation for User Story 9

- [ ] T120 [P] [US9] Create frontend/components/ui/command-palette.tsx using cmdk library with search and action list
- [ ] T121 [P] [US9] Create frontend/hooks/useKeyboardShortcuts.ts with keyboard event handlers (N, E, Delete, Cmd/Ctrl+K)
- [ ] T122 [US9] Register keyboard shortcuts in frontend/app/layout.tsx using useKeyboardShortcuts hook
- [ ] T123 [US9] Define command actions in command-palette.tsx (New Task, Search Tasks, Toggle View, Filter by Priority, etc.)
- [ ] T124 [US9] Implement command execution handlers in command-palette.tsx (open dialogs, navigate routes, apply filters)
- [ ] T125 [US9] Add Cmd/Ctrl+K detection to open command palette globally
- [ ] T126 [US9] Add "N" key handler to open CreateTaskDialog when no input is focused
- [ ] T127 [US9] Add "E" key handler to open EditTaskDialog for selected task
- [ ] T128 [US9] Add "Delete" key handler to trigger delete confirmation for selected task
- [ ] T129 [US9] Implement task selection state in TaskList.tsx (highlight selected task with border)
- [ ] T130 [US9] Add keyboard navigation (arrow up/down) to move selection between tasks in TaskList.tsx
- [ ] T131 [US9] Add tooltip to all action buttons showing keyboard shortcut (e.g., "New Task (N)")
- [ ] T132 [US9] Prevent shortcuts from firing when user is typing in input/textarea fields

**Checkpoint**: At this point, User Story 9 should be fully functional - keyboard shortcuts work globally, command palette searches actions, tooltips show shortcuts

---

## Phase 12: User Story 10 - Subtasks and Checklists (Priority: P3)

**Goal**: Allow users to break down tasks into subtasks with progress indicators and auto-complete parent when all subtasks done

**Independent Test**: Create task with 3 subtasks, check off 2 subtasks and verify progress shows "2/3 completed", check final subtask and verify parent task auto-completes

### Implementation for User Story 10

- [ ] T133 [P] [US10] Create Alembic migration: Create subtasks table (id, task_id, description VARCHAR(200), is_completed BOOLEAN, order_index INTEGER, timestamps) in backend/alembic/versions/
- [ ] T134 [P] [US10] Run alembic upgrade head to apply subtask migration
- [ ] T135 [P] [US10] Create backend/src/models/subtask.py with Subtask model (id, task_id FK, description, is_completed, order_index, timestamps)
- [ ] T136 [P] [US10] Create backend/src/schemas/subtask_schemas.py with SubtaskCreate, SubtaskUpdate, SubtaskResponse schemas
- [ ] T137 [US10] Create backend/src/services/subtask_service.py with CRUD operations and auto-completion logic
- [ ] T138 [P] [US10] Add GET /api/v1/tasks/{task_id}/subtasks endpoint in backend/src/api/routes/subtasks.py
- [ ] T139 [P] [US10] Add POST /api/v1/tasks/{task_id}/subtasks endpoint in backend/src/api/routes/subtasks.py for creating subtask
- [ ] T140 [P] [US10] Add PATCH /api/v1/subtasks/{subtask_id} endpoint in backend/src/api/routes/subtasks.py for updating subtask
- [ ] T141 [P] [US10] Add PATCH /api/v1/subtasks/{subtask_id}/toggle endpoint in backend/src/api/routes/subtasks.py for toggling completion
- [ ] T142 [P] [US10] Add DELETE /api/v1/subtasks/{subtask_id} endpoint in backend/src/api/routes/subtasks.py
- [ ] T143 [P] [US10] Add PATCH /api/v1/tasks/{task_id}/subtasks/reorder endpoint in backend/src/api/routes/subtasks.py
- [ ] T144 [US10] Implement auto-complete parent task logic in backend/src/services/subtask_service.py when all subtasks completed
- [ ] T145 [P] [US10] Create frontend/hooks/useSubtasks.ts with queries and mutations for subtask operations
- [ ] T146 [P] [US10] Create frontend/components/tasks/SubtaskList.tsx displaying checklist with toggle and delete buttons
- [ ] T147 [P] [US10] Create frontend/components/tasks/SubtaskProgress.tsx showing "X/Y completed" badge with percentage
- [ ] T148 [US10] Add subtask list to EditTaskDialog.tsx and TaskCard expanded view in frontend/components/tasks/
- [ ] T149 [US10] Add "Add Subtask" input field to SubtaskList.tsx with auto-focus on Enter key
- [ ] T150 [US10] Implement drag-to-reorder for subtasks in SubtaskList.tsx using @dnd-kit
- [ ] T151 [US10] Update TaskCard.tsx to display SubtaskProgress badge when subtasks exist
- [ ] T152 [US10] Update backend/src/services/task_service.py to load subtasks relationship using selectinload

**Checkpoint**: At this point, User Story 10 should be fully functional - subtasks can be added/toggled/reordered, progress displays, parent auto-completes

---

## Phase 13: User Story 11 - Task Notes and Expandable Details (Priority: P3)

**Goal**: Allow users to add detailed notes to tasks with expand/collapse toggle and notes search integration

**Independent Test**: Add notes to task, verify notes section collapses/expands with toggle, verify note icon indicator appears on task card, search for text in notes and verify task appears in results

### Implementation for User Story 11

- [ ] T153 [P] [US11] Add notes textarea field to EditTaskDialog.tsx in frontend/components/tasks/
- [ ] T154 [P] [US11] Create frontend/components/tasks/NotesSection.tsx with expand/collapse toggle and formatted text display
- [ ] T155 [P] [US11] Add NotesSection to TaskCard expanded view with collapsed state by default
- [ ] T156 [US11] Add note icon indicator to TaskCard.tsx when task.notes is not null
- [ ] T157 [US11] Update backend search logic in backend/src/services/task_service.py to include notes field in ILIKE query
- [ ] T158 [US11] Add character count display (X/500 characters) to notes textarea in EditTaskDialog.tsx
- [ ] T159 [US11] Add last updated timestamp display in NotesSection.tsx showing task.updated_at
- [ ] T160 [US11] Implement markdown formatting support in NotesSection.tsx for basic styles (bold, italic, lists)

**Checkpoint**: At this point, User Story 11 should be fully functional - notes can be added/edited, expand/collapse works, search includes notes

---

## Phase 14: User Story 12 - Recurring Tasks (Priority: P3)

**Goal**: Enable users to create tasks that automatically recur on schedule (daily/weekly/monthly) with new instances generated on completion

**Independent Test**: Create recurring task with weekly schedule, complete instance and verify new instance appears with next due date, edit recurring task and verify options to update this instance or all future instances

### Implementation for User Story 12

- [ ] T161 [P] [US12] Create Alembic migration: Create recurrence_patterns table (id, task_id FK UNIQUE, frequency VARCHAR(50), interval INTEGER, days_of_week JSON, day_of_month INTEGER, end_date TIMESTAMPTZ, next_occurrence_date TIMESTAMPTZ, timestamps) in backend/alembic/versions/
- [ ] T162 [P] [US12] Run alembic upgrade head to apply recurrence migration
- [ ] T163 [P] [US12] Create backend/src/models/recurrence_pattern.py with RecurrencePattern model (id, task_id, frequency, interval, days_of_week, day_of_month, end_date, next_occurrence_date, timestamps)
- [ ] T164 [P] [US12] Create backend/src/schemas/recurring_schemas.py with RecurrencePatternCreate, RecurrencePatternUpdate, RecurrencePatternResponse schemas
- [ ] T165 [US12] Create backend/src/services/recurring_service.py with recurrence creation, next occurrence calculation, and instance generation logic
- [ ] T166 [P] [US12] Add GET /api/v1/tasks/{task_id}/recurrence endpoint in backend/src/api/routes/recurring.py
- [ ] T167 [P] [US12] Add POST /api/v1/tasks/{task_id}/recurrence endpoint in backend/src/api/routes/recurring.py for setting recurrence pattern
- [ ] T168 [P] [US12] Add PATCH /api/v1/tasks/{task_id}/recurrence endpoint in backend/src/api/routes/recurring.py for updating pattern
- [ ] T169 [P] [US12] Add DELETE /api/v1/tasks/{task_id}/recurrence endpoint in backend/src/api/routes/recurring.py for stopping recurrence
- [ ] T170 [P] [US12] Add GET /api/v1/tasks/{task_id}/recurrence/preview endpoint in backend/src/api/routes/recurring.py showing next N occurrences
- [ ] T171 [US12] Implement next occurrence date calculation in backend/src/services/recurring_service.py (daily/weekly/monthly logic)
- [ ] T172 [US12] Add hook to task completion in backend/src/services/task_service.py to generate next recurring instance
- [ ] T173 [P] [US12] Create frontend/components/tasks/RecurringDialog.tsx with frequency selector (daily/weekly/monthly), interval input, days of week checkboxes, end date picker
- [ ] T174 [P] [US12] Create frontend/hooks/useRecurring.ts with queries and mutations for recurrence operations
- [ ] T175 [US12] Add recurring toggle button to CreateTaskDialog.tsx and EditTaskDialog.tsx opening RecurringDialog
- [ ] T176 [US12] Add repeat icon indicator to TaskCard.tsx when task has recurrence pattern
- [ ] T177 [US12] Display recurrence pattern summary in TaskCard.tsx (e.g., "Repeats every Monday")
- [ ] T178 [US12] Add confirmation dialog when deleting recurring task: "Delete this instance" or "Stop all recurrences"
- [ ] T179 [US12] Add confirmation dialog when editing recurring task: "Update this instance" or "Update all future instances"

**Checkpoint**: At this point, User Story 12 should be fully functional - recurring tasks can be created with schedules, instances generate on completion, edit/delete options work

---

## Phase 15: User Story 13 - Task Templates (Priority: P3)

**Goal**: Allow users to save task structures as reusable templates and create new tasks from templates

**Independent Test**: Create task with title, description, tags, subtasks, save as template, create new task from template and verify all fields populate correctly, manage templates (edit/delete)

### Implementation for User Story 13

- [ ] T180 [P] [US13] Create Alembic migration: Create task_templates table (id, user_id FK, name VARCHAR(100), title VARCHAR(100), description TEXT, priority VARCHAR(20), subtasks_template JSON, timestamps) in backend/alembic/versions/
- [ ] T181 [P] [US13] Create Alembic migration: Create template_tags join table (template_id, tag_id, created_at) in backend/alembic/versions/
- [ ] T182 [P] [US13] Run alembic upgrade head to apply template migrations
- [ ] T183 [P] [US13] Create backend/src/models/task_template.py with TaskTemplate model (id, user_id, name, title, description, priority, subtasks_template, timestamps)
- [ ] T184 [P] [US13] Create backend/src/models/template_tag.py with TemplateTag join model (template_id, tag_id, created_at)
- [ ] T185 [P] [US13] Create backend/src/schemas/template_schemas.py with TemplateCreate, TemplateUpdate, TemplateResponse schemas
- [ ] T186 [US13] Create backend/src/services/template_service.py with CRUD operations and apply_template logic
- [ ] T187 [P] [US13] Add GET /api/v1/templates endpoint in backend/src/api/routes/templates.py for listing user's templates
- [ ] T188 [P] [US13] Add POST /api/v1/templates endpoint in backend/src/api/routes/templates.py for creating template
- [ ] T189 [P] [US13] Add PATCH /api/v1/templates/{template_id} endpoint in backend/src/api/routes/templates.py
- [ ] T190 [P] [US13] Add DELETE /api/v1/templates/{template_id} endpoint in backend/src/api/routes/templates.py
- [ ] T191 [P] [US13] Add POST /api/v1/templates/{template_id}/apply endpoint in backend/src/api/routes/templates.py for creating task from template
- [ ] T192 [P] [US13] Add POST /api/v1/tasks/{task_id}/save-as-template endpoint in backend/src/api/routes/templates.py
- [ ] T193 [P] [US13] Create frontend/components/tasks/TemplateDialog.tsx with template list and apply button
- [ ] T194 [P] [US13] Create frontend/components/tasks/SaveTemplateDialog.tsx with template name input and options (include subtasks, include tags)
- [ ] T195 [P] [US13] Create frontend/hooks/useTemplates.ts with queries and mutations for template operations
- [ ] T196 [US13] Add "Use Template" button to CreateTaskDialog.tsx opening TemplateDialog
- [ ] T197 [US13] Add "Save as Template" button to EditTaskDialog.tsx opening SaveTemplateDialog
- [ ] T198 [US13] Implement template application logic in frontend: populate form fields from selected template
- [ ] T199 [US13] Add template management section to settings page for editing/deleting templates

**Checkpoint**: At this point, User Story 13 should be fully functional - templates can be saved from tasks, new tasks can be created from templates, template management works

---

## Phase 16: User Story 14 - Drag and Drop Reordering (Priority: P3)

**Goal**: Enable manual task reordering by dragging tasks to different positions with persistence

**Independent Test**: Drag task from position 3 to position 1, verify tasks shift to accommodate, refresh page and verify order persists, attempt drag with active filter and verify drag handles are disabled

### Implementation for User Story 14

- [ ] T200 [P] [US14] Update TaskCard.tsx in frontend/components/tasks/ to be draggable using @dnd-kit useSortable
- [ ] T201 [P] [US14] Wrap TaskList.tsx with DndContext and SortableContext from @dnd-kit
- [ ] T202 [US14] Implement drag handlers in TaskList.tsx to update manual_order field via API on drop
- [ ] T203 [US14] Add PATCH /api/v1/tasks/reorder endpoint in backend/src/api/routes/tasks.py accepting array of task IDs in new order
- [ ] T204 [US14] Implement manual reorder logic in backend/src/services/task_service.py updating manual_order field for affected tasks
- [ ] T205 [US14] Add optimistic UI update to drag operation using TanStack Query setQueryData in TaskList.tsx
- [ ] T206 [US14] Disable drag handles in TaskCard.tsx when active filters or sorting is applied (show disabled state with tooltip)
- [ ] T207 [US14] Add subtle animation on drop to confirm new position in TaskList.tsx
- [ ] T208 [US14] Update backend queries in backend/src/services/task_service.py to order by manual_order when no explicit sort specified
- [ ] T209 [US14] Implement long-press to activate drag mode on mobile in TaskCard.tsx using @use-gesture/react

**Checkpoint**: At this point, User Story 14 should be fully functional - tasks can be manually reordered by dragging, order persists, mobile long-press works

---

## Phase 17: User Story 15 - Mobile Optimizations with Swipe Gestures (Priority: P3)

**Goal**: Add mobile-specific UI (bottom nav, FAB) and swipe gestures (left=delete, right=complete) for touch devices

**Independent Test**: On mobile device, swipe task card left and verify delete action reveals, swipe right and verify task toggles completion, verify bottom navigation bar fixed at bottom, tap FAB and verify new task dialog opens

### Implementation for User Story 15

- [ ] T210 [P] [US15] Create frontend/components/tasks/SwipeableTaskCard.tsx wrapping TaskCard with useSwipe from @use-gesture/react
- [ ] T211 [US15] Implement swipe left gesture to reveal delete button in SwipeableTaskCard.tsx
- [ ] T212 [US15] Implement swipe right gesture to toggle task completion in SwipeableTaskCard.tsx
- [ ] T213 [P] [US15] Create frontend/components/mobile/BottomNav.tsx with icons for Tasks/Dashboard/Calendar/Settings
- [ ] T214 [P] [US15] Create frontend/components/mobile/FloatingActionButton.tsx fixed bottom-right opening CreateTaskDialog
- [ ] T215 [US15] Add mobile detection in frontend/app/layout.tsx to conditionally render BottomNav
- [ ] T216 [US15] Replace TaskCard with SwipeableTaskCard in TaskList.tsx for mobile viewports
- [ ] T217 [US15] Ensure all tap targets are minimum 44x44 pixels in mobile components
- [ ] T218 [US15] Add haptic feedback on swipe actions for iOS/Android devices
- [ ] T219 [US15] Prevent swipe gesture conflicts with horizontal scrolling in kanban/calendar views
- [ ] T220 [US15] Add visual swipe indicator (colored background) during swipe in SwipeableTaskCard.tsx

**Checkpoint**: At this point, User Story 15 should be fully functional - mobile swipe gestures work, bottom nav appears on mobile, FAB creates tasks, tap targets meet accessibility

---

## Phase 18: User Story 16 - Theme Picker and Personalization (Priority: P3)

**Goal**: Allow users to choose from multiple theme palettes (Ocean, Sunset, Forest, Monochrome) and custom accent colors with persistence

**Independent Test**: Open theme picker, select different theme and verify all UI updates, choose custom accent color and verify primary buttons use new color, refresh and verify theme persists

### Implementation for User Story 16

- [ ] T221 [P] [US16] Create Alembic migration: Create user_preferences table (id, user_id FK UNIQUE, theme VARCHAR(50), accent_color VARCHAR(7), default_view VARCHAR(50), default_sort VARCHAR(50), show_completed_tasks BOOLEAN, enable_animations BOOLEAN, onboarding_completed BOOLEAN, timestamps) in backend/alembic/versions/
- [ ] T222 [P] [US16] Run alembic upgrade head to apply preferences migration
- [ ] T223 [P] [US16] Create backend/src/models/user_preferences.py with UserPreferences model (id, user_id, theme, accent_color, default_view, default_sort, show_completed_tasks, enable_animations, onboarding_completed, timestamps)
- [ ] T224 [P] [US16] Create backend/src/schemas/preferences_schemas.py with PreferencesUpdate, PreferencesResponse schemas
- [ ] T225 [US16] Create backend/src/services/preferences_service.py with get/update operations and default creation on user signup
- [ ] T226 [P] [US16] Add GET /api/v1/preferences endpoint in backend/src/api/routes/preferences.py
- [ ] T227 [P] [US16] Add PATCH /api/v1/preferences endpoint in backend/src/api/routes/preferences.py
- [ ] T228 [P] [US16] Add PATCH /api/v1/preferences/theme endpoint in backend/src/api/routes/preferences.py for theme-only updates
- [ ] T229 [P] [US16] Create frontend/components/settings/ThemePicker.tsx with theme preview cards (Ocean, Sunset, Forest, Monochrome, System)
- [ ] T230 [P] [US16] Create frontend/components/settings/AccentColorPicker.tsx with color swatches and custom color input
- [ ] T231 [P] [US16] Create frontend/hooks/usePreferences.ts with queries and mutations for user preferences
- [ ] T232 [US16] Update frontend/lib/theme-store.ts Zustand store to sync with backend preferences
- [ ] T233 [US16] Define CSS custom properties for each theme in frontend/app/globals.css
- [ ] T234 [US16] Implement theme switching logic in frontend/app/layout.tsx applying theme class to root element
- [ ] T235 [US16] Add dark mode variants for each theme in frontend/app/globals.css
- [ ] T236 [US16] Persist theme preference to localStorage and backend in usePreferences mutations
- [ ] T237 [US16] Create settings page in frontend/app/settings/page.tsx with ThemePicker and AccentColorPicker

**Checkpoint**: At this point, User Story 16 should be fully functional - themes can be selected and persist, accent colors customize UI, dark mode works per theme

---

## Phase 19: User Story 17 - Enhanced Empty States with Illustrations (Priority: P3)

**Goal**: Display beautiful illustrated empty states with helpful messages for zero tasks, no search results, empty trash, no data scenarios

**Independent Test**: Clear all tasks and verify illustrated empty state with "Create your first task" CTA, apply filter with no matches and verify "No tasks match" message, view trash when empty and verify empty trash illustration

### Implementation for User Story 17

- [ ] T238 [P] [US17] Create frontend/components/ui/empty-state.tsx reusable component with illustration, heading, description, action button props
- [ ] T239 [P] [US17] Add empty state SVG illustrations to frontend/public/illustrations/ (no-tasks.svg, no-results.svg, empty-trash.svg, no-data.svg)
- [ ] T240 [P] [US17] Update TaskList.tsx to show EmptyState when tasks array is empty (no active filters)
- [ ] T241 [P] [US17] Update TaskList.tsx to show EmptyState with "No tasks match" when filtered list is empty
- [ ] T242 [P] [US17] Update TrashView.tsx in frontend/app/tasks/trash/page.tsx to show EmptyState when trash is empty
- [ ] T243 [P] [US17] Update SearchBar results to show EmptyState with search term when no search matches
- [ ] T244 [P] [US17] Update DashboardStatsCards.tsx to show "0" with empty state message when no tasks exist
- [ ] T245 [P] [US17] Update charts in dashboard to show empty state placeholders when no data available
- [ ] T246 [US17] Add contextual CTAs to each empty state (e.g., "Create Task" button in no-tasks state, "Clear Filters" in no-results state)

**Checkpoint**: At this point, User Story 17 should be fully functional - empty states appear in all relevant scenarios with illustrations and helpful CTAs

---

## Phase 20: User Story 18 - Onboarding Tour for New Users (Priority: P3)

**Goal**: Show guided tour to first-time users after signup highlighting key features (create task, filters, views) with spotlight overlays

**Independent Test**: Create new test account, verify onboarding overlay appears on first login, step through tour and verify spotlight highlights each feature in sequence, skip tour and verify tour doesn't re-trigger unless manually restarted

### Implementation for User Story 18

- [ ] T247 [P] [US18] Create frontend/components/onboarding/OnboardingTour.tsx with step state management and spotlight overlay
- [ ] T248 [P] [US18] Create frontend/components/onboarding/TourStep.tsx with tooltip positioning and next/prev/skip buttons
- [ ] T249 [P] [US18] Define tour steps in frontend/lib/onboarding-steps.ts (welcome → create task → filters → views → completion)
- [ ] T250 [US18] Implement spotlight effect in OnboardingTour.tsx with overlay and highlight cutout
- [ ] T251 [US18] Add onboarding_completed check in frontend/app/layout.tsx to trigger tour for new users
- [ ] T252 [US18] Add smooth transitions between tour steps with scroll-into-view for highlighted elements
- [ ] T253 [US18] Implement "Skip Tour" button updating onboarding_completed preference via API
- [ ] T254 [US18] Implement "Start Tour" button in user menu dropdown for manually restarting tour
- [ ] T255 [US18] Add confetti animation on tour completion using frontend/lib/animations.ts
- [ ] T256 [US18] Update backend/src/services/preferences_service.py to set onboarding_completed=false for new users
- [ ] T257 [US18] Add PATCH /api/v1/preferences/onboarding endpoint to mark tour complete

**Checkpoint**: At this point, User Story 18 should be fully functional - onboarding tour appears for new users, spotlight highlights features, tour can be skipped/restarted

---

## Phase 21: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality assurance

- [ ] T258 [P] Update all API endpoints in backend to include proper error handling and logging
- [ ] T259 [P] Add composite database indexes for performance: (user_id, deleted_at), (user_id, due_date), (user_id, status)
- [ ] T260 [P] Run backend test suite and ensure ≥80% coverage: pytest --cov=src tests/
- [ ] T261 [P] Run frontend type checking and fix any type errors: npm run type-check
- [ ] T262 [P] Run Lighthouse audit on landing page and optimize for 90+ score (performance, accessibility, SEO)
- [ ] T263 [P] Add loading skeletons to all components that fetch data
- [ ] T264 [P] Implement error boundaries in frontend/app/error.tsx and frontend/app/tasks/error.tsx
- [ ] T265 [P] Add rate limiting to search endpoint (300 requests per minute per user)
- [ ] T266 [P] Optimize bundle size: analyze frontend build and lazy load heavy components
- [ ] T267 [P] Add API response caching headers for static data (tags, templates, preferences)
- [ ] T268 [P] Update frontend/README.md with feature documentation and setup instructions
- [ ] T269 [P] Update backend/README.md with new API endpoint documentation
- [ ] T270 [P] Run E2E test suite with Playwright covering all critical user flows
- [ ] T271 [P] Perform security audit: check for SQL injection, XSS, CSRF vulnerabilities
- [ ] T272 [P] Verify WCAG 2.1 AA compliance: run axe-core accessibility tests
- [ ] T273 [P] Test application on multiple browsers (Chrome, Safari, Firefox, Edge)
- [ ] T274 [P] Test responsive design on mobile devices (iOS Safari, Android Chrome)
- [ ] T275 [P] Implement prefers-reduced-motion CSS queries for all animations
- [ ] T276 Run quickstart.md validation: follow all instructions and verify completeness

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-20)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if team capacity allows)
  - Or sequentially in priority order (P1 → P2 → P3)
  - **P1 Stories (US1-US3)**: Critical for MVP - complete these first
  - **P2 Stories (US4-US8)**: Enhanced functionality - complete after P1
  - **P3 Stories (US9-US18)**: Advanced features - complete after P2
- **Polish (Phase 21)**: Depends on all desired user stories being complete

### User Story Dependencies

**P1 Stories (MVP - Complete First)**:
- **User Story 1 (Landing Page)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (Due Dates)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (Tags)**: Can start after Foundational - No dependencies on other stories

**P2 Stories (Enhanced Features)**:
- **User Story 4 (Animations)**: Can start after Foundational - Integrates with US1-US3 components
- **User Story 5 (Search)**: Can start after Foundational - Works better with US2 (due dates) and US3 (tags) but independently testable
- **User Story 6 (Dashboard)**: Can start after Foundational - Works better with US2/US3 data but independently testable
- **User Story 7 (Kanban)**: Can start after Foundational - No dependencies on other stories
- **User Story 8 (Calendar)**: Depends on US2 (due dates) for visualization

**P3 Stories (Advanced Features)**:
- **User Story 9 (Keyboard Shortcuts)**: Can start after Foundational - Integrates with existing UI
- **User Story 10 (Subtasks)**: Can start after Foundational - No dependencies on other stories
- **User Story 11 (Notes)**: Can start after Foundational - Integrates with US5 (search)
- **User Story 12 (Recurring)**: Depends on US2 (due dates) for scheduling
- **User Story 13 (Templates)**: Depends on US3 (tags) and US10 (subtasks) for full template functionality
- **User Story 14 (Drag Reorder)**: Can start after Foundational - No dependencies on other stories
- **User Story 15 (Mobile)**: Can start after Foundational - Integrates with existing UI
- **User Story 16 (Themes)**: Can start after Foundational - Affects all UI components
- **User Story 17 (Empty States)**: Can start after Foundational - Integrates with all views
- **User Story 18 (Onboarding)**: Depends on US16 (preferences) for completion tracking

### Within Each User Story

- Backend migrations → Backend models → Backend schemas → Backend services → API endpoints
- Frontend hooks/types → Frontend components → Frontend integration
- Parallel tasks marked [P] can run simultaneously within a story
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup (Phase 1)**: All 6 tasks marked [P] can run in parallel
- **Foundational (Phase 2)**: Tasks T007-T014 can run in parallel after migrations complete
- **Once Foundational completes**: Multiple user stories can be worked on in parallel by different team members
- **Within User Stories**: All tasks marked [P] can run in parallel (e.g., all API endpoints, all frontend components)
- **P1 Stories**: US1, US2, US3 can be developed in parallel by 3 developers
- **P2 Stories**: US4-US8 can be developed in parallel after P1 complete
- **P3 Stories**: US9-US18 can be developed in parallel after P2 complete

---

## Parallel Example: User Story 3 (Tags)

```bash
# Launch backend migrations together:
Task T039: Create tags table migration
Task T040: Create task_tags join table migration

# Launch backend models together:
Task T042: Create Tag model
Task T043: Create TaskTag model

# Launch API endpoints together (after service complete):
Task T047: GET /api/v1/tags
Task T048: POST /api/v1/tags
Task T049: PATCH /api/v1/tags/{tag_id}
Task T050: DELETE /api/v1/tags/{tag_id}
Task T051: POST /api/v1/tasks/{task_id}/tags
Task T052: DELETE /api/v1/tasks/{task_id}/tags

# Launch frontend components together (after hooks complete):
Task T054: TagPicker component
Task T055: TagBadge component
Task T056: TagFilters component
Task T057: TagManagement component
```

---

## Implementation Strategy

### MVP First (P1 Stories Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Landing Page)
4. Complete Phase 4: User Story 2 (Due Dates)
5. Complete Phase 5: User Story 3 (Tags)
6. **STOP and VALIDATE**: Test all P1 stories independently
7. Deploy/demo MVP (landing page + core task features)

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready
2. Add P1 Stories (US1-US3) → Test independently → Deploy/Demo (MVP!)
3. Add P2 Stories (US4-US8) → Test independently → Deploy/Demo (Enhanced version)
4. Add P3 Stories (US9-US18) → Test independently → Deploy/Demo (Full-featured version)
5. Complete Polish phase → Final quality assurance → Production release

### Parallel Team Strategy

With 3 developers for MVP:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Landing Page)
   - Developer B: User Story 2 (Due Dates)
   - Developer C: User Story 3 (Tags)
3. Stories complete and integrate independently
4. Team validates MVP together

With 5 developers for enhanced version:

1. Complete Setup + Foundational + MVP (US1-US3)
2. Assign P2 stories in parallel:
   - Developer A: User Story 4 (Animations)
   - Developer B: User Story 5 (Search)
   - Developer C: User Story 6 (Dashboard)
   - Developer D: User Story 7 (Kanban)
   - Developer E: User Story 8 (Calendar)

---

## Summary

- **Total Tasks**: 276 tasks
- **P1 Tasks (MVP)**: 62 tasks (US1: 12, US2: 12, US3: 23, Setup: 6, Foundational: 9)
- **P2 Tasks (Enhanced)**: 88 tasks (US4: 11, US5: 13, US6: 12, US7: 10, US8: 12)
- **P3 Tasks (Advanced)**: 108 tasks (US9: 13, US10: 20, US11: 8, US12: 19, US13: 20, US14: 10, US15: 11, US16: 17, US17: 9, US18: 11)
- **Polish Tasks**: 19 tasks (cross-cutting concerns)
- **Parallel Opportunities**: 180+ tasks marked [P] can run in parallel within their phase
- **Independent Stories**: Each user story can be tested and deployed independently
- **MVP Scope**: Phase 1-5 (Setup + Foundational + US1-US3) = 62 tasks for minimum viable product

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability (US1-US18)
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All tasks include exact file paths for immediate implementation
- Tests are NOT included per specification (implementation-focused)
- Follow TDD approach: implement with validation at each checkpoint
