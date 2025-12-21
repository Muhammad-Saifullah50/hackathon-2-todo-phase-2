"use client";

import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Plus } from "lucide-react";
import { format } from "date-fns";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { useCreateTask } from "@/hooks/useTasks";
import { createTaskSchema, type CreateTaskFormData } from "@/lib/schemas/task";
import { DueDatePicker } from "./DueDatePicker";

export function CreateTaskDialog() {
  const [open, setOpen] = useState(false);
  const [dueDate, setDueDate] = useState<Date | null>(null);
  const { toast } = useToast();
  const { mutate: createTask, isPending } = useCreateTask();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
    watch,
    setValue,
  } = useForm<CreateTaskFormData>({
    resolver: zodResolver(createTaskSchema),
    mode: "onChange", // Real-time validation
    defaultValues: {
      title: "",
      description: "",
      priority: "medium",
      due_date: null,
    },
  });

  // Watch form values to detect changes
  const title = watch("title");
  const description = watch("description");
  const hasChanges = Boolean(title?.trim() || description?.trim() || dueDate);

  // Keyboard shortcut: Ctrl/Cmd + N to open modal
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "n") {
        e.preventDefault();
        setOpen(true);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleOpenChange = (newOpen: boolean) => {
    if (!newOpen && hasChanges) {
      if (!window.confirm("Discard unsaved changes?")) {
        return;
      }
      reset();
      setDueDate(null);
    }
    setOpen(newOpen);
  };

  const onSubmit = (data: CreateTaskFormData) => {
    createTask(
      {
        title: data.title,
        description: data.description,
        priority: data.priority,
        due_date: data.due_date,
      },
      {
        onSuccess: () => {
          toast({
            title: "Success",
            description: "Task created successfully",
          });
          setOpen(false);
          reset();
          setDueDate(null);
        },
        onError: (error: any) => {
          toast({
            title: "Error",
            description:
              error?.response?.data?.error?.message ||
              "Failed to create task. Please try again.",
            variant: "destructive",
          });
        },
      }
    );
  };

  const titleLength = title?.length || 0;
  const descriptionLength = description?.length || 0;
  const titleWords = title ? title.trim().split(/\s+/).length : 0;

  return (
    <>
      <Button onClick={() => setOpen(true)}>
        <Plus className="mr-2 h-4 w-4" />
        Add Task
      </Button>

      <Dialog open={open} onOpenChange={handleOpenChange}>
        <DialogContent className="sm:max-w-[500px] max-sm:h-full max-sm:w-full max-sm:max-w-full">
          <DialogHeader>
            <DialogTitle>Create New Task</DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* Title field */}
            <div>
              <Label htmlFor="title">
                Title <span className="text-destructive">*</span>
              </Label>
              <Input
                id="title"
                {...register("title")}
                placeholder="Enter task title..."
                maxLength={100}
                aria-invalid={errors.title ? "true" : "false"}
                aria-describedby={errors.title ? "title-error" : undefined}
              />
              <div className="flex justify-between items-center mt-1">
                <div>
                  {errors.title && (
                    <p id="title-error" className="text-sm text-destructive">
                      {errors.title.message}
                    </p>
                  )}
                </div>
                <p
                  className={`text-xs ${
                    titleLength > 90 || titleWords > 45
                      ? "text-orange-500"
                      : "text-muted-foreground"
                  }`}
                >
                  {titleLength}/100 chars · {titleWords}/50 words
                </p>
              </div>
            </div>

            {/* Description field */}
            <div>
              <Label htmlFor="description">Description (optional)</Label>
              <Textarea
                id="description"
                {...register("description")}
                placeholder="Add details (optional)..."
                maxLength={500}
                rows={4}
                aria-invalid={errors.description ? "true" : "false"}
                aria-describedby={
                  errors.description ? "description-error" : undefined
                }
              />
              <div className="flex justify-between items-center mt-1">
                <div>
                  {errors.description && (
                    <p
                      id="description-error"
                      className="text-sm text-destructive"
                    >
                      {errors.description.message}
                    </p>
                  )}
                </div>
                <p
                  className={`text-xs ${
                    descriptionLength > 450
                      ? "text-orange-500"
                      : "text-muted-foreground"
                  }`}
                >
                  {descriptionLength}/500 chars
                </p>
              </div>
            </div>

            {/* Priority field */}
            <div>
              <Label htmlFor="priority">Priority</Label>
              <Select
                onValueChange={(value) =>
                  setValue("priority", value as "low" | "medium" | "high")
                }
                defaultValue="medium"
              >
                <SelectTrigger id="priority">
                  <SelectValue placeholder="Select priority (default: Medium)" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Due Date field */}
            <div>
              <Label htmlFor="due_date">Due Date (optional)</Label>
              <DueDatePicker
                value={dueDate}
                onChange={(date) => {
                  setDueDate(date);
                  setValue("due_date", date ? format(date, "yyyy-MM-dd") : null);
                }}
              />
            </div>

            {/* Form actions */}
            <div className="flex justify-end gap-2 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => handleOpenChange(false)}
                disabled={isPending}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={isPending || isSubmitting || Object.keys(errors).length > 0}
              >
                {isPending ? "Creating..." : "Create Task"}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </>
  );
}
