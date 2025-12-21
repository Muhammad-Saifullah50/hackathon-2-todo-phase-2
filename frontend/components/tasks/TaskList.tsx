"use client";

/**
 * TaskList Component - Main list/grid view with filters and pagination.
 * Client Component because it manages filter state and uses React Query.
 */

import { useState } from "react";
import { useTasks, useBulkToggle, useBulkDelete } from "@/hooks/useTasks";
import { TaskCard } from "./TaskCard";
import { TaskFilters } from "./TaskFilters";
import { Pagination } from "./Pagination";
import { BulkActions } from "./BulkActions";
import { TaskStatus } from "@/lib/types/task";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { LayoutGrid, LayoutList } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { TaskListSkeleton } from "./TaskListSkeleton";

export function TaskList() {
  // Filter and pagination state
  const [status, setStatus] = useState<TaskStatus | "all">("all");
  const [sortBy, setSortBy] = useState("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");
  const [page, setPage] = useState(1);
  const [layout, setLayout] = useState<"list" | "grid">("list");

  // Bulk selection state
  const [selectedTaskIds, setSelectedTaskIds] = useState<Set<string>>(new Set());
  const { mutate: bulkToggle } = useBulkToggle();
  const { mutate: bulkDelete } = useBulkDelete();

  // Fetch tasks with React Query
  const { data, isLoading, isError, error } = useTasks({
    page,
    limit: 20,
    status: status === "all" ? null : status,
    sort_by: sortBy,
    sort_order: sortOrder,
  });

  // Loading state
  if (isLoading) {
    return <TaskListSkeleton count={5} variant={layout} />;
  }

  // Error state
  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>
          Failed to load tasks: {error instanceof Error ? error.message : "Unknown error"}
        </AlertDescription>
      </Alert>
    );
  }

  const tasks = data?.data?.tasks || [];
  const metadata = data?.data?.metadata;
  const pagination = data?.data?.pagination;

  // Bulk selection handlers
  const toggleTaskSelection = (taskId: string) => {
    setSelectedTaskIds((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(taskId)) {
        newSet.delete(taskId);
      } else {
        newSet.add(taskId);
      }
      return newSet;
    });
  };

  const toggleSelectAll = () => {
    if (selectedTaskIds.size === tasks.length) {
      setSelectedTaskIds(new Set());
    } else {
      setSelectedTaskIds(new Set(tasks.map((t) => t.id)));
    }
  };

  const handleBulkToggle = (targetStatus: TaskStatus) => {
    bulkToggle(
      { taskIds: Array.from(selectedTaskIds), targetStatus },
      {
        onSuccess: () => {
          setSelectedTaskIds(new Set());
        },
      }
    );
  };

  const handleBulkDelete = () => {
    bulkDelete(Array.from(selectedTaskIds), {
      onSuccess: () => {
        setSelectedTaskIds(new Set());
      },
    });
  };

  const clearSelection = () => {
    setSelectedTaskIds(new Set());
  };

  const allSelected = tasks.length > 0 && selectedTaskIds.size === tasks.length;

  // Empty state
  if (tasks.length === 0) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <TaskFilters
            status={status}
            sortBy={sortBy}
            sortOrder={sortOrder}
            onStatusChange={(value) => {
              setStatus(value);
              setPage(1); // Reset to first page on filter change
            }}
            onSortByChange={(value) => {
              setSortBy(value);
              setPage(1);
            }}
            onSortOrderChange={(value) => {
              setSortOrder(value);
              setPage(1);
            }}
          />

          {/* Layout Toggle */}
          <div className="flex gap-1">
            <Button
              variant={layout === "list" ? "default" : "outline"}
              size="icon"
              onClick={() => setLayout("list")}
            >
              <LayoutList className="h-4 w-4" />
            </Button>
            <Button
              variant={layout === "grid" ? "default" : "outline"}
              size="icon"
              onClick={() => setLayout("grid")}
            >
              <LayoutGrid className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="rounded-lg border border-dashed p-12 text-center">
          <p className="text-muted-foreground">
            {status === "all"
              ? "No tasks found. Create your first task to get started!"
              : `No ${status} tasks found.`}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Screen reader announcements */}
      <div className="sr-only" aria-live="polite" aria-atomic="true">
        {metadata && `${metadata.total_pending} pending tasks, ${metadata.total_completed} completed tasks`}
      </div>

      {/* Filters and Layout Toggle */}
      <div className="flex items-center justify-between gap-4">
        <TaskFilters
          status={status}
          sortBy={sortBy}
          sortOrder={sortOrder}
          onStatusChange={(value) => {
            setStatus(value);
            setPage(1);
          }}
          onSortByChange={(value) => {
            setSortBy(value);
            setPage(1);
          }}
          onSortOrderChange={(value) => {
            setSortOrder(value);
            setPage(1);
          }}
        />

        {/* Layout Toggle */}
        <div className="flex gap-1">
          <Button
            variant={layout === "list" ? "default" : "outline"}
            size="icon"
            onClick={() => setLayout("list")}
            aria-label="List view"
          >
            <LayoutList className="h-4 w-4" />
          </Button>
          <Button
            variant={layout === "grid" ? "default" : "outline"}
            size="icon"
            onClick={() => setLayout("grid")}
            aria-label="Grid view"
          >
            <LayoutGrid className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Task Count Badges and Select All */}
      <div className="flex items-center justify-between">
        {metadata && (
          <div className="flex gap-4 text-sm">
            <div className="flex items-center gap-2">
              <span className="text-muted-foreground">Pending:</span>
              <span className="font-medium">{metadata.total_pending}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-muted-foreground">Completed:</span>
              <span className="font-medium">{metadata.total_completed}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-muted-foreground">Total:</span>
              <span className="font-medium">{metadata.total_active}</span>
            </div>
          </div>
        )}

        {/* Select All Checkbox */}
        {tasks.length > 0 && (
          <div className="flex items-center gap-2">
            <Checkbox
              id="select-all"
              checked={allSelected}
              onCheckedChange={toggleSelectAll}
            />
            <label
              htmlFor="select-all"
              className="text-sm font-medium cursor-pointer"
            >
              Select All
            </label>
          </div>
        )}
      </div>

      {/* Task Grid/List */}
      <div
        className={
          layout === "grid"
            ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
            : "space-y-3"
        }
      >
        {tasks.map((task) => (
          <div key={task.id} className="flex items-start gap-2">
            {/* Bulk Selection Checkbox */}
            <Checkbox
              checked={selectedTaskIds.has(task.id)}
              onCheckedChange={() => toggleTaskSelection(task.id)}
              className="mt-4"
              aria-label={`Select ${task.title}`}
            />
            <div className="flex-1">
              <TaskCard task={task} variant={layout} />
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
      {pagination && pagination.total_pages > 1 && (
        <Pagination pagination={pagination} onPageChange={setPage} />
      )}

      {/* Bulk Actions Toolbar */}
      <BulkActions
        selectedCount={selectedTaskIds.size}
        onMarkAsCompleted={() => handleBulkToggle('completed')}
        onMarkAsPending={() => handleBulkToggle('pending')}
        onBulkDelete={handleBulkDelete}
        onClearSelection={clearSelection}
      />
    </div>
  );
}
