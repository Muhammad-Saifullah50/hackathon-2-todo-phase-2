import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";

interface SubtaskTemplateItem {
  description: string;
}

interface Template {
  id: string;
  user_id: string;
  name: string;
  title: string;
  description: string | null;
  priority: "low" | "medium" | "high";
  subtasks_template: SubtaskTemplateItem[] | null;
  tags: Array<{ id: string; name: string; color: string }>;
  created_at: string;
  updated_at: string;
}

interface TemplateListResponse {
  templates: Template[];
  total: number;
  page: number;
  page_size: number;
}

interface CreateTemplateData {
  name: string;
  title: string;
  description?: string;
  priority: "low" | "medium" | "high";
  subtasks_template?: SubtaskTemplateItem[];
  tag_ids?: string[];
}

interface UpdateTemplateData {
  name?: string;
  title?: string;
  description?: string;
  priority?: "low" | "medium" | "high";
  subtasks_template?: SubtaskTemplateItem[];
  tag_ids?: string[];
}

interface SaveTaskAsTemplateData {
  task_id: string;
  template_name: string;
  include_subtasks?: boolean;
  include_tags?: boolean;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = localStorage.getItem("token");
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "An error occurred" }));
    throw new Error(error.detail || "Request failed");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function useTemplates(page = 1, pageSize = 50) {
  return useQuery<TemplateListResponse>({
    queryKey: ["templates", page, pageSize],
    queryFn: () =>
      fetchWithAuth(`${API_URL}/api/v1/templates?page=${page}&page_size=${pageSize}`),
  });
}

export function useTemplate(templateId: string) {
  return useQuery<Template>({
    queryKey: ["templates", templateId],
    queryFn: () => fetchWithAuth(`${API_URL}/api/v1/templates/${templateId}`),
    enabled: !!templateId,
  });
}

export function useCreateTemplate() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (data: CreateTemplateData) =>
      fetchWithAuth(`${API_URL}/api/v1/templates`, {
        method: "POST",
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["templates"] });
      toast({
        title: "Template created",
        description: "Your template has been created successfully.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message || "Failed to create template",
        variant: "destructive",
      });
    },
  });
}

export function useUpdateTemplate() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ templateId, data }: { templateId: string; data: UpdateTemplateData }) =>
      fetchWithAuth(`${API_URL}/api/v1/templates/${templateId}`, {
        method: "PATCH",
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["templates"] });
      toast({
        title: "Template updated",
        description: "Your template has been updated successfully.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message || "Failed to update template",
        variant: "destructive",
      });
    },
  });
}

export function useDeleteTemplate() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (templateId: string) =>
      fetchWithAuth(`${API_URL}/api/v1/templates/${templateId}`, {
        method: "DELETE",
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["templates"] });
      toast({
        title: "Template deleted",
        description: "Your template has been deleted successfully.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message || "Failed to delete template",
        variant: "destructive",
      });
    },
  });
}

export function useApplyTemplate() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ templateId, dueDate }: { templateId: string; dueDate?: string }) =>
      fetchWithAuth(`${API_URL}/api/v1/templates/${templateId}/apply`, {
        method: "POST",
        body: JSON.stringify({ due_date: dueDate }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      toast({
        title: "Task created from template",
        description: "A new task has been created from your template.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message || "Failed to create task from template",
        variant: "destructive",
      });
    },
  });
}

export function useSaveTaskAsTemplate() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (data: SaveTaskAsTemplateData) => {
      const params = new URLSearchParams({
        template_name: data.template_name,
        include_subtasks: String(data.include_subtasks ?? true),
        include_tags: String(data.include_tags ?? true),
      });
      return fetchWithAuth(
        `${API_URL}/api/v1/templates/tasks/${data.task_id}/save-as-template?${params}`,
        {
          method: "POST",
        }
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["templates"] });
      toast({
        title: "Template saved",
        description: "Your task has been saved as a template.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message || "Failed to save task as template",
        variant: "destructive",
      });
    },
  });
}
