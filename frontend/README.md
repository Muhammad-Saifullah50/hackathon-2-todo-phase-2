# Todo App Frontend

Next.js frontend for the Todo Application.

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **UI Library**: React 19
- **Styling**: Tailwind CSS
- **Components**: Shadcn/ui
- **State/Data Fetching**: TanStack Query
- **Testing**: Vitest + React Testing Library

## Setup

### Prerequisites

- Node.js 22+
- npm

### Local Development

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env.local`:

   ```bash
   cp .env.example .env.local
   ```

3. **Run the development server**:

   ```bash
   npm run dev
   ```

   The app will be available at http://localhost:3000.

## Testing

Run tests with Vitest:

```bash
npm test
```

To run tests with coverage:

```bash
npm run test:cov
```

To run tests in watch mode:

```bash
npm run test:watch
```

## Code Quality

Maintain code standards with the following commands:

- **Linting**: `npm run lint`
- **Formatting**: `npm run format`
- **Type Checking**: `npm run type-check`

## Docker

Run using Docker Compose from the root directory:

```bash
docker-compose up frontend
```
