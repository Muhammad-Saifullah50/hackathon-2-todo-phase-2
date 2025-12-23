import { SidebarClient } from "./SidebarClient";
import { getSession } from "@/lib/auth";

export async function Sidebar() {
  const session = await getSession();

  // Don't render sidebar if user is not authenticated
  if (!session) {
    return null;
  }

  return <SidebarClient />;
}
