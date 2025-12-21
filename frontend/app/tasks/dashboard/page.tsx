import { StatsCards } from "@/components/dashboard/StatsCards";
import { CompletionTrendChart } from "@/components/dashboard/CompletionTrendChart";
import { PriorityBreakdownChart } from "@/components/dashboard/PriorityBreakdownChart";

export default function DashboardPage() {
  return (
    <div className="container mx-auto space-y-6 p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Overview of your tasks and productivity metrics
        </p>
      </div>

      <StatsCards />

      <div className="grid gap-6 md:grid-cols-2">
        <CompletionTrendChart />
        <PriorityBreakdownChart />
      </div>
    </div>
  );
}
