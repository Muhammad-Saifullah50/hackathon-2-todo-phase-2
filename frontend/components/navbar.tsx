"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";
import { Button } from "@/components/ui/button";

export default function Navbar() {
  const router = useRouter();
  const { data: session, isPending } = authClient.useSession();

  const handleSignOut = async () => {
    await authClient.signOut({
      fetchOptions: {
        onSuccess: () => {
          router.push("/");
        },
      },
    });
  };

  return (
    <nav className="border-b bg-background px-4 py-3 flex items-center justify-between">
      <Link href="/" className="text-xl font-bold">
        TodoApp
      </Link>
      <div className="flex items-center gap-4">
        {isPending ? (
          <div className="h-9 w-20 animate-pulse rounded-md bg-muted" />
        ) : session ? (
          <>
            <Button variant="ghost" asChild>
              <Link href="/tasks">My Tasks</Link>
            </Button>
            <Button variant="ghost" asChild>
              <Link href="/tasks/dashboard">Dashboard</Link>
            </Button>
            <Button variant="outline" onClick={handleSignOut}>
              Logout
            </Button>
          </>
        ) : (
          <>
            <Button variant="ghost" asChild>
              <Link href="/sign-in">Login</Link>
            </Button>
            <Button asChild>
              <Link href="/sign-up">Sign Up</Link>
            </Button>
          </>
        )}
      </div>
    </nav>
  );
}
