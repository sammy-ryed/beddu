# beedu Frontend - Next.js

Minimalistic, professional UI for the beedu mental health companion.

## Design Philosophy

- **Clean & Minimal**: No AI-generated vibes, no excessive gradients
- **Functional**: Every element serves a purpose
- **Professional**: Inspired by Linear, Notion, and Vercel
- **Accessible**: Clear typography, good contrast, subtle interactions
- **Human-designed**: Real product feel, not over-polished

## Tech Stack

- **Next.js 15** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Inter font** for clean typography

## Getting Started

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start the Backend
Make sure the Flask backend is running:
```bash
# In the beddu root directory
python web_app.py
```

The backend runs on `http://localhost:5000`

### 3. Start the Frontend
```bash
cd frontend
npm run dev
```

The frontend runs on `http://localhost:3000`

## Key Features

### Chat Interface
- Clean message bubbles (black for user, light gray for assistant)
- Smooth animations, no excessive effects
- Auto-load last 10 conversations on start
- Typing indicator with bouncing dots
- No distracting decorations

### History Page
- Tab-based navigation (Conversations / What I Remember)
- Filter conversations by stress level
- Clean card-based layout
- Subtle stress badges (no alarming colors)

### Stats/Progress Page
- Grid layout with key metrics
- Clean number displays
- Subtle color coding for improvement trends
- Human-readable explanations

## Design Tokens

### Colors
- **Primary**: `neutral-900` (black text, buttons)
- **Background**: `neutral-50` (very light gray)
- **Borders**: `neutral-200` (subtle lines)
- **Secondary text**: `neutral-600`
- **Accent colors**: Minimal use of color (green for positive, red for alerts)

### Typography
- **Font**: Inter (system font fallback)
- **Sizes**: Small (12-13px), Regular (15px), Large (18-24px)
- **Weight**: Medium (500) for headers, Regular (400) for body

### Spacing
- Consistent 4px grid system
- Generous padding (p-4, p-6)
- Good line spacing (leading-relaxed)

### Shadows
- Subtle: `shadow-sm` (no dramatic shadows)
- Borders preferred over shadows

### Interactions
- Hover states: Subtle color changes
- Active states: `scale-95` (button press feel)
- Transitions: 150ms ease-in-out (fast, not slow)

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with header/footer
│   ├── page.tsx            # Chat interface (homepage)
│   ├── history/
│   │   └── page.tsx        # Conversation history & memory
│   ├── stats/
│   │   └── page.tsx        # Progress statistics
│   └── globals.css         # Global styles
├── .env.local              # Environment variables
├── tailwind.config.ts      # Tailwind configuration
└── package.json
```

## Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Building for Production

```bash
npm run build
npm start
```

## What Makes This NOT Look AI-Generated?

1. **No gradient backgrounds** - Solid, muted colors
2. **No excessive animations** - Subtle, functional transitions
3. **No rounded-full everywhere** - Varied border radiuses
4. **Real shadows** - Subtle, not dramatic
5. **Consistent spacing** - Follows a grid system
6. **Functional design** - Not decorative
7. **Human color choices** - Neutrals, not vibrant
8. **Clean typography** - Good line heights, readable sizes
9. **No over-engineering** - Simple, straightforward components
10. **Looks like a real product** - Could be from a real startup

## Comparison: AI vs Human Design

### AI-Generated (What We Avoided):
- Purple/blue gradients everywhere
- Excessive border-radius (rounded-full on everything)
- Dramatic shadows and glows
- Over-animated (everything bounces)
- Too much color
- Overly polished
- Generic placeholder text
- Copy-paste aesthetic

### Human-Designed (What We Built):
- Neutral color palette
- Varied, purposeful border radius
- Subtle shadows
- Minimal, functional animations
- Color used sparingly
- Clean but not sterile
- Real, helpful text
- Unique, considered aesthetic

---

Built with care for real humans dealing with real stress. 🌸
