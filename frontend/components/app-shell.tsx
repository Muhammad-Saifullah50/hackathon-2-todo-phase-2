import { Sidebar } from "@/components/sidebar/Sidebar";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Sidebar />
      <main className="md:ml-56 overflow-x-hidden h-full w-full ">
        {children}
      </main>
    </>
  );
}
