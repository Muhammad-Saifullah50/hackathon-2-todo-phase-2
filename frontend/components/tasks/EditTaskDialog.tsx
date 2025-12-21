"use client";

/**
 * EditTaskDialog Component - Modal for editing task title, description, and due date.
 * Client Component because it needs form state, validation, and submit handlers.
 */

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { format, parseISO } from "date-fns";
import { Task } from "@/lib/types/task";
import { useUpdateTask } from "@/hooks/useTasks";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Loader2 } from "lucide-react";
import { DueDatePicker } from "./DueDatePicker";

// Form data type
interface EditTaskFormData {
  title: string;
  description?: string;
  due_date: string | null;
}

// Zod validation schema
const editTaskSchema = z.object({
  title: z
    .string()
    .min(1, "Title is required")
    .max(100, "Title must be 100 characters or less")
    .trim(),
  description: z
    .string()
    .max(500, "Description must be 500 characters or less")
    .trim()
    .optional(),
  due_date: z.string().nullable(),
});

interface EditTaskDialogProps {
  task: Task;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function EditTaskDialog({
  task,
  open,
  onOpenChange,
}: EditTaskDialogProps) {
  const { mutate: updateTask, isPending } = useUpdateTask();
  const [dueDate, setDueDate] = useState<Date | null>(
    task.due_date ? parseISO(task.due_date) : null
  );

  const form = useForm<EditTaskFormData>({
    resolver: zodResolver(editTaskSchema),
    defaultValues: {
      title: task.title,
      description: task.description || "",
      due_date: task.due_date || null,
    },
  });

  // Reset form and due date when task changes
  useEffect(() => {
    form.reset({
      title: task.title,
      description: task.description || "",
      due_date: task.due_date || null,
    });
    setDueDate(task.due_date ? parseISO(task.due_date) : null);
  }, [task, form]);

  const onSubmit = (data: EditTaskFormData) => {
    // Check if anything actually changed
    const hasChanges =
      data.title !== task.title ||
      (data.description || "") !== (task.description || "") ||
      (data.due_date || null) !== (task.due_date || null);

    if (!hasChanges) {
      form.setError("root", {
        message: "No changes detected. Please modify at least one field.",
      });
      return;
    }

    // Submit update
    updateTask(
      {
        taskId: task.id,
        data: {
          title: data.title !== task.title ? data.title : undefined,
          description:
            data.description !== task.description
              ? data.description
              : undefined,
          due_date:
            (data.due_date || null) !== (task.due_date || null)
              ? data.due_date
              : undefined,
        },
      },
      {
        onSuccess: () => {
          onOpenChange(false);
          form.reset();
          setDueDate(null);
        },
      }
    );
  };

  const handleCancel = () => {
    form.reset();
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[525px]">
        <DialogHeader>
          <DialogTitle>Edit Task</DialogTitle>
          <DialogDescription>
            Update the task title or description. Click save when you&apos;re done.
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            {/* Title Field */}
            <FormField<EditTaskFormData>
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Title</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Enter task title"
                      {...field}
                      disabled={isPending}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Description Field */}
            <FormField<EditTaskFormData>
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description (Optional)</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Enter task description"
                      className="min-h-[100px] resize-none"
                      {...field}
                      value={field.value ?? ""}
                      disabled={isPending}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Due Date Field */}
            <div className="space-y-2">
              <Label htmlFor="due_date">Due Date (Optional)</Label>
              <DueDatePicker
                value={dueDate}
                onChange={(date) => {
                  setDueDate(date);
                  form.setValue(
                    "due_date",
                    date ? format(date, "yyyy-MM-dd") : null
                  );
                }}
              />
            </div>

            {/* Root Error Message */}
            {form.formState.errors.root && (
              <p className="text-sm font-medium text-destructive">
                {form.formState.errors.root.message}
              </p>
            )}

            {/* Dialog Footer */}
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={handleCancel}
                disabled={isPending}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={isPending}>
                {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Save Changes
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
