"use client";

import { authClient } from "@/lib/auth-client";

export default function DashboardPage() {
  const { data: session } = authClient.useSession();

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      <div className="bg-card p-6 rounded-lg border shadow-sm">
        <h2 className="text-xl font-semibold mb-2">Welcome, {session?.user?.name || "User"}!</h2>
        <p className="text-muted-foreground">
          Email: {session?.user?.email}
        </p>
        <p className="mt-4 text-sm text-muted-foreground">
          Your tasks will appear here in the next update.
        </p>
      </div>
    </div>
  );
}
