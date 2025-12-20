/**
 * Tasks Page - Main page for task management.
 * Displays task list and provides task creation functionality.
 */

import { CreateTaskDialog } from "@/components/tasks/CreateTaskDialog";

export default function TasksPage() {
  return (
    <div className="container max-w-7xl mx-auto py-6 px-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">My Tasks</h1>
          <p className="text-muted-foreground mt-1">
            Manage your tasks and stay organized
          </p>
        </div>
        <CreateTaskDialog />
      </div>

      {/* Task list will be implemented in Feature 5 */}
      <div className="rounded-lg border border-dashed p-12 text-center">
        <p className="text-muted-foreground">
          Task list coming soon in Feature 5: View Tasks
        </p>
        <p className="text-sm text-muted-foreground mt-2">
          Create a task using the &quot;Add Task&quot; button above to get started
        </p>
      </div>
    </div>
  );
}
