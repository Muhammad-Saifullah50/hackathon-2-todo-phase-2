"use client";

/**
 * TaskCard Component - Displays a single task with interactive elements.
 * Client Component because it needs onClick handlers and state for hover effects.
 * Enhanced with Framer Motion animations for smooth interactions.
 */

import { useState } from "react";
import { motion } from "framer-motion";
import { Task } from "@/lib/types/task";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Circle, Clock, Edit, Trash2, RotateCcw } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import { EditTaskDialog } from "./EditTaskDialog";
import { DeleteConfirmDialog } from "./DeleteConfirmDialog";
import { DueDateBadge } from "./DueDateBadge";
import { TagBadgeList } from "./TagBadge";
import { HighlightedText } from "./SearchBar";
import { useCelebration } from "./CelebrationAnimation";
import { useToggleTask, useDeleteTask, useRestoreTask, usePermanentDelete } from "@/hooks/useTasks";
import { listItem, cardHover, useReducedMotion } from "@/lib/animations";

interface TaskCardProps {
  task: Task;
  variant?: "list" | "grid";
  isTrashView?: boolean;
  searchQuery?: string;
}

export function TaskCard({ task, variant: _variant = "list", isTrashView = false, searchQuery = "" }: TaskCardProps) {
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [isPermanentDeleteDialogOpen, setIsPermanentDeleteDialogOpen] = useState(false);

  const { mutate: toggleTask } = useToggleTask();
  const { mutate: deleteTask } = useDeleteTask();
  const { mutate: restoreTask } = useRestoreTask();
  const { mutate: permanentDelete } = usePermanentDelete();
  const { triggerCelebration, CelebrationComponent } = useCelebration();
  const prefersReducedMotion = useReducedMotion();
  const isCompleted = task.status === "completed";

  const StatusIcon = isCompleted ? CheckCircle2 : Circle;
  const statusColor = isCompleted
    ? "text-green-600 dark:text-green-400"
    : "text-gray-400 dark:text-gray-500";

  const priorityColors = {
    low: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
    medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
    high: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
  };

  const handleToggleStatus = () => {
    // Trigger celebration if marking as completed
    if (!isCompleted) {
      triggerCelebration();
    }
    toggleTask(task.id);
  };

  const handleDelete = () => {
    deleteTask(task.id);
    setIsDeleteDialogOpen(false);
  };

  const handleRestore = () => {
    restoreTask(task.id);
  };

  const handlePermanentDelete = () => {
    permanentDelete(task.id);
    setIsPermanentDeleteDialogOpen(false);
  };

  return (
    <>
      {/* Celebration Animation */}
      <CelebrationComponent />

      <motion.div
        variants={listItem}
        initial="hidden"
        animate="visible"
        exit="exit"
        whileHover={prefersReducedMotion ? undefined : cardHover.hover}
        whileTap={prefersReducedMotion ? undefined : cardHover.tap}
        layout={!prefersReducedMotion}
      >
        <Card className="hover:shadow-md transition-shadow" role="article" aria-label={`Task: ${task.title}`}>
          <CardContent className="p-4">
          <div className="flex items-start gap-3">
            {/* Status Checkbox */}
            <button
              className="mt-0.5 hover:scale-110 transition-transform"
              onClick={handleToggleStatus}
              aria-label={isCompleted ? "Mark as pending" : "Mark as completed"}
              aria-pressed={isCompleted}
            >
              <StatusIcon className={`h-5 w-5 ${statusColor}`} />
            </button>

            {/* Task Content */}
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-2">
                <h3
                  className={`font-medium text-sm leading-tight ${
                    isCompleted
                      ? "line-through text-muted-foreground"
                      : "text-foreground"
                  }`}
                >
                  <HighlightedText text={task.title} query={searchQuery} />
                </h3>

                <div className="flex items-center gap-1 shrink-0">
                  {/* Due Date Badge */}
                  {task.due_date && (
                    <DueDateBadge dueDate={task.due_date} />
                  )}

                  {/* Priority Badge */}
                  <Badge
                    variant="secondary"
                    className={`${priorityColors[task.priority]} text-xs`}
                  >
                    {task.priority}
                  </Badge>

                  {isTrashView ? (
                    <>
                      {/* Restore Button */}
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={handleRestore}
                        aria-label="Restore task"
                      >
                        <RotateCcw className="h-3.5 w-3.5" />
                      </Button>

                      {/* Permanent Delete Button */}
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 text-destructive hover:text-destructive"
                        onClick={() => setIsPermanentDeleteDialogOpen(true)}
                        aria-label="Delete permanently"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </Button>
                    </>
                  ) : (
                    <>
                      {/* Edit Button */}
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => setIsEditDialogOpen(true)}
                        aria-label="Edit task"
                      >
                        <Edit className="h-3.5 w-3.5" />
                      </Button>

                      {/* Delete Button */}
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 text-destructive hover:text-destructive"
                        onClick={() => setIsDeleteDialogOpen(true)}
                        aria-label="Delete task"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </Button>
                    </>
                  )}
                </div>
              </div>

            {/* Description */}
            {task.description && (
              <p
                className={`text-sm mt-1.5 ${
                  isCompleted
                    ? "line-through text-muted-foreground/70"
                    : "text-muted-foreground"
                }`}
              >
                <HighlightedText text={task.description} query={searchQuery} />
              </p>
            )}

            {/* Tags */}
            {task.tags && task.tags.length > 0 && (
              <div className="mt-2">
                <TagBadgeList
                  tags={task.tags}
                  maxVisible={3}
                  size="sm"
                />
              </div>
            )}

            {/* Timestamps */}
            <div className="flex items-center gap-3 mt-2 text-xs text-muted-foreground">
              <div className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                <span>
                  {formatDistanceToNow(new Date(task.created_at), {
                    addSuffix: true,
                  })}
                </span>
              </div>

              {isCompleted && task.completed_at && (
                <div className="flex items-center gap-1">
                  <CheckCircle2 className="h-3 w-3 text-green-600" />
                  <span>
                    Completed{" "}
                    {formatDistanceToNow(new Date(task.completed_at), {
                      addSuffix: true,
                    })}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
        </CardContent>
      </Card>
      </motion.div>

      {/* Edit Dialog */}
    {!isTrashView && (
      <EditTaskDialog
        task={task}
        open={isEditDialogOpen}
        onOpenChange={setIsEditDialogOpen}
      />
    )}

    {/* Delete Confirmation Dialog */}
    <DeleteConfirmDialog
      open={isDeleteDialogOpen}
      onOpenChange={setIsDeleteDialogOpen}
      onConfirm={handleDelete}
      taskTitle={task.title}
      isPermanent={false}
    />

    {/* Permanent Delete Confirmation Dialog */}
    <DeleteConfirmDialog
      open={isPermanentDeleteDialogOpen}
      onOpenChange={setIsPermanentDeleteDialogOpen}
      onConfirm={handlePermanentDelete}
      taskTitle={task.title}
      isPermanent={true}
    />
  </>
  );
}
