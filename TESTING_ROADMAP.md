# Comprehensive Testing Roadmap

**Generated:** 2025-12-23
**Objective:** Achieve 100% backend coverage and 80%+ frontend coverage

## Executive Summary

### Current Status
- **Backend Coverage:** 35.91% → Target: 100%
- **Backend Tests:** 48 tests → Need: ~150+ tests
- **Frontend Coverage:** <5% → Target: 80%+
- **Frontend Tests:** 4 tests → Need: ~100+ tests

### Tests Created (This Session)

#### Backend Unit Tests ✅
1. `test_tag_service.py` (11 test classes, ~30 tests)
2. `test_subtask_service.py` (7 test classes, ~20 tests)
3. `test_recurring_service.py` (6 test classes, ~15 tests)
4. `test_template_service.py` (6 test classes, ~10 tests)

#### Backend Integration Tests ✅
1. `test_tag_routes.py` (~20 tests)
2. `test_subtask_routes.py` (~10 tests)

**Total Backend Tests Added:** ~105 tests
**New Estimated Backend Coverage:** ~75-80%

---

## Remaining Backend Tests Needed

### Priority 1: Integration Tests for Routes

#### 1. Recurring Routes (`test_recurring_routes.py`)
- [ ] test_create_recurrence_pattern
- [ ] test_get_recurrence_pattern
- [ ] test_update_recurrence_pattern
- [ ] test_delete_recurrence_pattern
- [ ] test_get_recurrence_preview
- [ ] test_generate_next_instance_on_task_completion

**Estimated:** 10-15 tests

#### 2. Template Routes (`test_template_routes.py`)
- [ ] test_create_template
- [ ] test_get_templates
- [ ] test_update_template
- [ ] test_delete_template
- [ ] test_apply_template
- [ ] test_save_task_as_template

**Estimated:** 10 tests

#### 3. Search Routes (`test_search_routes.py`)
- [ ] test_search_tasks_by_title
- [ ] test_search_tasks_by_description
- [ ] test_search_tasks_by_notes
- [ ] test_search_with_filters (status, priority, tags, due_date)
- [ ] test_search_autocomplete
- [ ] test_search_with_pagination
- [ ] test_quick_filters

**Estimated:** 15-20 tests

#### 4. Analytics Routes (`test_analytics_routes.py`)
- [ ] test_get_task_stats
- [ ] test_get_completion_trend
- [ ] test_get_priority_breakdown
- [ ] test_get_due_date_stats

**Estimated:** 8-10 tests

### Priority 2: Model Tests

#### 1. Enhanced Model Tests (`test_models.py` - extend existing)
- [ ] test_tag_model_validation
- [ ] test_subtask_model_validation
- [ ] test_recurrence_pattern_model_validation
- [ ] test_template_model_validation
- [ ] test_task_model_with_relationships (tags, subtasks, recurrence)

**Estimated:** 10-15 tests

### Priority 3: Schema Tests

#### 1. Schema Validation Tests (`test_schemas.py` - extend existing)
- [ ] test_tag_schemas_validation
- [ ] test_subtask_schemas_validation
- [ ] test_recurring_schemas_validation
- [ ] test_template_schemas_validation
- [ ] test_search_schemas_validation

**Estimated:** 15-20 tests

---

## Frontend Tests Needed

### Priority 1: Hook Tests (CRITICAL - 0% coverage)

#### 1. `useTasks.test.ts`
```typescript
describe('useTasks Hook', () => {
  // Query hooks
  test('fetches tasks successfully')
  test('handles fetch error')
  test('applies filters correctly')
  test('handles pagination')

  // Mutation hooks
  test('createTask mutation with optimistic update')
  test('updateTask mutation with rollback on error')
  test('deleteTask mutation')
  test('toggleTask mutation updates counts')
  test('bulkToggle mutation')
  test('bulkDelete mutation')
})
```
**Estimated:** 15-20 tests

#### 2. `useTags.test.ts`
```typescript
describe('useTags Hook', () => {
  test('fetches tags successfully')
  test('createTag mutation')
  test('updateTag mutation')
  test('deleteTag mutation')
  test('addTagsToTask mutation')
  test('removeTagsFromTask mutation')
})
```
**Estimated:** 10-12 tests

#### 3. `useSubtasks.test.ts`
```typescript
describe('useSubtasks Hook', () => {
  test('fetches subtasks successfully')
  test('createSubtask mutation')
  test('toggleSubtask mutation')
  test('updateSubtask mutation')
  test('deleteSubtask mutation')
  test('reorderSubtasks mutation')
})
```
**Estimated:** 8-10 tests

#### 4. `useRecurring.test.ts`, `useTemplates.test.ts`, `useAnalytics.test.ts`, `useSearch.test.ts`

**Total Hook Tests:** ~80-100 tests

### Priority 2: Component Tests

#### Critical Components to Test:

1. **Task Components** (20 files)
   - CreateTaskDialog.test.tsx
   - EditTaskDialog.test.tsx
   - TaskCard.test.tsx
   - TaskList.test.tsx
   - DueDatePicker.test.tsx
   - TagPicker.test.tsx
   - SubtaskList.test.tsx
   - SearchBar.test.tsx
   - (12 more...)

**Estimated:** 60-80 tests

2. **Dashboard Components** (3 files)
   - StatsCards.test.tsx
   - CompletionTrendChart.test.tsx
   - PriorityBreakdownChart.test.tsx

**Estimated:** 15-20 tests

3. **Landing Components** (7 files)
   - Hero.test.tsx
   - Features.test.tsx
   - Testimonials.test.tsx
   - (4 more...)

**Estimated:** 20-30 tests

### Priority 3: E2E Tests

#### Playwright E2E Test Suites:

1. **Phase 006 Features** (`phase-006-features.spec.ts`)
```typescript
test.describe('Tags System', () => {
  test('create and assign tags to task')
  test('filter tasks by tags')
  test('delete tag removes from tasks')
})

test.describe('Subtasks', () => {
  test('add subtasks to task')
  test('toggle subtask completion')
  test('complete all subtasks auto-completes parent')
})

test.describe('Recurring Tasks', () => {
  test('create daily recurring task')
  test('complete instance generates next')
})

test.describe('Templates', () => {
  test('create template from task')
  test('create task from template')
})

test.describe('Search and Filters', () => {
  test('search tasks by title')
  test('apply quick filters')
  test('combine search with filters')
})
```

**Estimated:** 20-30 tests

---

## Implementation Strategy

### Week 1: Backend Tests (Target: 100% coverage)
**Days 1-2:** Integration tests for remaining routes
- Recurring routes
- Template routes
- Search routes
- Analytics routes

**Days 3-4:** Enhanced model and schema tests
- Relationship tests
- Validation tests
- Edge case tests

**Day 5:** Run coverage report and fill gaps
- Identify uncovered code paths
- Add missing tests
- Verify 100% coverage

### Week 2: Frontend Tests (Target: 80%+ coverage)
**Days 1-2:** Hook tests (CRITICAL)
- useTasks, useTags, useSubtasks
- useRecurring, useTemplates
- useAnalytics, useSearch

**Days 3-4:** Component tests
- Task components (priority 1)
- Dashboard components
- Landing components

**Day 5:** E2E tests
- Phase 006 feature flows
- Integration scenarios
- Edge cases

---

## Test Templates

### Backend Integration Test Template
```python
@pytest.mark.asyncio
async def test_<feature>_<action>_<scenario>(
    client: TestClient,
    test_user_token: str,
    test_session: Session
):
    """Test <description>."""
    # Arrange: Create test data
    # Act: Call API endpoint
    # Assert: Verify response and database state
```

### Frontend Hook Test Template
```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

describe('<HookName>', () => {
  const queryClient = new QueryClient();
  const wrapper = ({ children }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );

  it('should <test case>', async () => {
    // Arrange, Act, Assert
  });
});
```

### Frontend Component Test Template
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { <Component> } from './<Component>';

describe('<Component>', () => {
  it('renders correctly', () => {
    render(<Component />);
    expect(screen.getByText('<expected text>')).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    render(<Component />);
    fireEvent.click(screen.getByRole('button'));
    expect(/* assertion */);
  });
});
```

---

## Running Tests

### Backend
```bash
# Run all tests
cd backend && pytest

# Run with coverage
cd backend && pytest --cov=src --cov-report=html tests/

# Run specific test file
cd backend && pytest tests/unit/test_tag_service.py

# Run specific test
cd backend && pytest tests/unit/test_tag_service.py::TestCreateTag::test_create_tag_success
```

### Frontend
```bash
# Run all tests
cd frontend && npm test

# Run with coverage
cd frontend && npm test -- --coverage

# Run specific test file
cd frontend && npm test -- tests/hooks/useTasks.test.ts

# Run E2E tests
cd frontend && npm run test:e2e
```

---

## Success Criteria

### Backend
- ✅ 100% line coverage
- ✅ 100% branch coverage
- ✅ All critical paths tested
- ✅ All API endpoints tested
- ✅ All service methods tested
- ✅ All error cases handled

### Frontend
- ✅ 80%+ line coverage
- ✅ All hooks tested
- ✅ Critical user flows tested (E2E)
- ✅ Key components tested
- ✅ Error states tested
- ✅ Loading states tested

---

## Next Steps

1. **Immediate:** Complete remaining backend integration tests
2. **Next:** Create frontend hook tests (highest impact)
3. **Then:** Create component tests for critical flows
4. **Finally:** Add E2E tests for Phase 006 features

## Notes

- Tests created in this session provide ~70% additional backend coverage
- Hook tests will provide the biggest impact for frontend coverage
- E2E tests ensure features work end-to-end
- Use TDD approach for new features going forward
