"use client";

/**
 * Tasks Layout - Error boundary wrapper for task pages.
 * Catches React errors and provides fallback UI.
 */

import { Component, ReactNode } from "react";
import { AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class TasksErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Task management error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="container max-w-7xl mx-auto py-6 px-4">
          <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
            <div className="rounded-full bg-destructive/10 p-6 mb-6">
              <AlertTriangle className="h-12 w-12 text-destructive" />
            </div>
            <h1 className="text-2xl font-bold mb-2">Something went wrong</h1>
            <p className="text-muted-foreground mb-6 max-w-md">
              An error occurred while loading your tasks. Please try refreshing the page or
              contact support if the problem persists.
            </p>
            {this.state.error && (
              <details className="mb-6 text-sm text-muted-foreground max-w-2xl">
                <summary className="cursor-pointer font-medium mb-2">
                  Error details
                </summary>
                <pre className="text-left bg-muted p-4 rounded-lg overflow-auto">
                  {this.state.error.toString()}
                </pre>
              </details>
            )}
            <Button
              onClick={() => {
                this.setState({ hasError: false, error: null });
                window.location.reload();
              }}
            >
              Reload Page
            </Button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default function TasksLayout({ children }: { children: ReactNode }) {
  return <TasksErrorBoundary>{children}</TasksErrorBoundary>;
}
