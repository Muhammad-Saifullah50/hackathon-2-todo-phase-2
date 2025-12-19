import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 bg-background">
      <main className="max-w-2xl w-full">
        <Card className="shadow-lg border-2">
          <CardHeader className="text-center space-y-4">
            <CardTitle className="text-4xl font-extrabold tracking-tight lg:text-5xl text-primary">
              Todo Application
            </CardTitle>
            <CardDescription className="text-xl text-muted-foreground italic">
              Phase 2: Full-Stack Implementation
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col items-center space-y-8 pt-6">
            <div className="text-center space-y-4">
              <h2 className="text-2xl font-semibold">Hello World!</h2>
              <p className="text-lg leading-7 text-muted-foreground">
                Welcome to the modernized version of our Todo application. 
                Built with <strong>Next.js 15</strong>, <strong>React 19</strong>, 
                and a <strong>FastAPI</strong> backend.
              </p>
            </div>
            
            <div className="flex gap-4">
              <Button size="lg">Get Started</Button>
              <Button variant="outline" size="lg">Learn More</Button>
            </div>
          </CardContent>
        </Card>
        
        <footer className="mt-12 text-center text-sm text-muted-foreground">
          <p>Hackathon 2 - Project Setup & Architecture</p>
        </footer>
      </main>
    </div>
  );
}
