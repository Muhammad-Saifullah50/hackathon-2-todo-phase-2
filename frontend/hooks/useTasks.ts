/**
 * React Query hooks for task operations.
 * Provides optimistic updates for better UX.
 */

import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query';
import { createTask, getTasks } from '@/lib/api/tasks';
import type { CreateTaskRequest, Task } from '@/lib/types/task';

/**
 * Query key for tasks list.
 */
export const TASKS_QUERY_KEY = ['tasks'];

/**
 * Hook to fetch all tasks for the authenticated user.
 */
export function useTasks() {
  return useQuery({
    queryKey: TASKS_QUERY_KEY,
    queryFn: getTasks,
  });
}

/**
 * Hook to create a new task with optimistic updates.
 * Provides instant UI feedback even before server responds.
 */
export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createTask,

    // Optimistic update: show task immediately
    onMutate: async (newTask: CreateTaskRequest) => {
      // Cancel any outgoing refetches
      await queryClient.cancelQueries({ queryKey: TASKS_QUERY_KEY });

      // Snapshot the previous value
      const previousTasks = queryClient.getQueryData(TASKS_QUERY_KEY);

      // Generate temporary ID for optimistic task
      const tempId = `temp-${crypto.randomUUID()}`;

      // Optimistically update the cache
      queryClient.setQueryData(TASKS_QUERY_KEY, (old: any) => {
        if (!old || !old.data) return old;

        const optimisticTask: Task = {
          id: tempId,
          title: newTask.title,
          description: newTask.description || null,
          priority: newTask.priority || 'medium',
          status: 'pending',
          user_id: 'temp-user',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          completed_at: null,
        };

        return {
          ...old,
          data: [optimisticTask, ...(old.data || [])],
        };
      });

      // Return context for rollback
      return { previousTasks };
    },

    // Rollback on error
    onError: (error, variables, context) => {
      // Restore previous state
      if (context?.previousTasks) {
        queryClient.setQueryData(TASKS_QUERY_KEY, context.previousTasks);
      }

      // Log error for debugging
      console.error('Failed to create task:', error);
    },

    // Refetch on success to get server data
    onSuccess: () => {
      // Invalidate and refetch tasks
      queryClient.invalidateQueries({ queryKey: TASKS_QUERY_KEY });
    },
  });
}
