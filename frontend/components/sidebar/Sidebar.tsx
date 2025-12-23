"use client";

import { SidebarClient } from "./SidebarClient";
import { authClient } from "@/lib/auth-client";
import { useEffect, useState } from "react";

export function Sidebar() {
  const [session, setSession] = useState<{ user: unknown } | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const { data } = await authClient.getSession();
        setSession(data);
      } catch (error) {
        console.error("Error fetching session:", error);
        setSession(null);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSession();
  }, []);

  // Don't render sidebar if user is not authenticated or still loading
  if (isLoading || !session) {
    return null;
  }

  return <SidebarClient />;
}
