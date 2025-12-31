# Visual Guide - Brutalist Navigation & Layout Components

## Component Overview

### 1. BrutalNavigation Component

```
┌─────────────────────────────────────────────────────────────┐
│ 🛡️ CYBERCOMPASS  [Features ▼] [About] [Profile] [Sign Out] │ ← Desktop
└─────────────────────────────────────────────────────────────┘
      ↑                    ↑           ↑         ↑
   Logo (red)      Dropdown menu   Links    Auth buttons
   4px border      (opens on click)         (4px borders)

Mobile View:
┌─────────────────────────────────────┐
│ 🛡️ CYBERCOMPASS            [☰]     │
└─────────────────────────────────────┘
                              ↑
                        Hamburger menu
                        (opens drawer)

When Features dropdown is open:
┌────────────────────────────────────┐
│ [Features ▼]                       │
├────────────────────────────────────┤
│ ┌────────────────────────────────┐ │
│ │ 🎭 Deepfake Detection          │ │
│ │    Master spotting fakes       │ │
│ ├────────────────────────────────┤ │
│ │ 📱 Social Media Simulation     │ │
│ │    Navigate the feed safely    │ │
│ ├────────────────────────────────┤ │
│ │ 💬 Catfish Detection           │ │
│ │    Spot red flags in chats     │ │
│ ├────────────────────────────────┤ │
│ │ 📊 Analytics Dashboard         │ │
│ │    Track your progress         │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
```

**Key Features:**
- Sticky positioning (stays at top on scroll)
- 6px black border-bottom
- White background
- Bold uppercase text
- 4px borders on all buttons
- Hover effects (press animation)
- Focus rings for accessibility

---

### 2. FeatureHub Component

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              AI-POWERED                                     │
│              CYBER TRAINING                                 │
│                    ↑                                        │
│              (8xl font, red)                                │
│                                                             │
│   Build critical thinking skills through AI simulations    │
│                                                             │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐                  │
│   │    4     │ │   100+   │ │    ∞     │                  │
│   │ Features │ │Challenges│ │ Learning │                  │
│   └──────────┘ └──────────┘ └──────────┘                  │
│        ↑ Stats cards with 4px borders                      │
│                                                             │
│   [GET STARTED →]  [EXPLORE FEATURES]                      │
│         ↑ CTA buttons with 6px borders                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              Choose Your Training                           │
│                                                             │
│   ┌─────────────────────┐  ┌─────────────────────┐        │
│   │  🎭                  │  │  📱                  │        │
│   │                      │  │                      │        │
│   │ DEEPFAKE DETECTION   │  │ SOCIAL MEDIA SIM     │        │
│   │                      │  │                      │        │
│   │ Master spotting...   │  │ Navigate the feed... │        │
│   │                      │  │                      │        │
│   │ Challenges: 50+      │  │ Scenarios: 30+       │        │
│   │              [Start→]│  │              [Start→]│        │
│   └─────────────────────┘  └─────────────────────┘        │
│                                                             │
│   ┌─────────────────────┐  ┌─────────────────────┐        │
│   │  💬                  │  │  📊                  │        │
│   │                      │  │                      │        │
│   │ CATFISH DETECTION    │  │ ANALYTICS DASHBOARD  │        │
│   │                      │  │                      │        │
│   │ Learn to identify... │  │ Track your progress..│        │
│   │                      │  │                      │        │
│   │ Simulations: 25+     │  │ Insights: Real-time  │        │
│   │              [Start→]│  │              [Start→]│        │
│   └─────────────────────┘  └─────────────────────┘        │
│         ↑ Feature cards with 6px borders                   │
│         hover-lift effect on hover                         │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              Ready to Level Up?                             │
│                                                             │
│   Join thousands of students building digital literacy     │
│                                                             │
│              [SIGN UP NOW →]                                │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              Why CyberCompass?                              │
│                                                             │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│   │   🤖     │  │   🎯     │  │   📈     │               │
│   │          │  │          │  │          │               │
│   │AI-POWERED│  │INTERACTIVE│ │  TRACK   │               │
│   │          │  │          │  │ PROGRESS │               │
│   │Advanced  │  │Learn by  │  │Monitor   │               │
│   │AI creates│  │doing with│  │your      │               │
│   │realistic │  │hands-on  │  │growth    │               │
│   │scenarios │  │challenges│  │          │               │
│   └──────────┘  └──────────┘  └──────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Full-page landing experience
- Gradient backgrounds (gray-50 to white)
- Large typography (5xl-8xl headings)
- Feature cards with hover lift effect
- Stats cards with bold numbers
- Multiple CTA sections
- Responsive grid (1/2 columns)

---

### 3. BrutalPageLayout Component

```
┌─────────────────────────────────────────────────────────────┐
│ Home / AI Features / Deepfake Training                      │ ← Breadcrumbs
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    [MAIN CONTENT]                           │
│                                                             │
│              (Your page content goes here)                  │
│                                                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                        FOOTER                               │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ 🛡️       │  │ FEATURES │  │RESOURCES │  │  LEGAL   │  │
│  │CYBERCOM- │  │          │  │          │  │          │  │
│  │  PASS    │  │Deepfake  │  │About     │  │Privacy   │  │
│  │          │  │Social    │  │Help      │  │Terms     │  │
│  │AI-powered│  │Catfish   │  │Contact   │  │Cookies   │  │
│  │training  │  │Analytics │  │FAQ       │  │          │  │
│  │          │  │          │  │          │  │          │  │
│  │ 𝕏 ⚙️ 💼  │  │          │  │          │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                             │
│  © 2025 CyberCompass          Built with 💪 for literacy   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Breadcrumb navigation (auto-generated or custom)
- Consistent page structure
- Footer with 4-column grid
- Social media links
- Responsive layout
- Optional footer display

---

## Color Usage

### Primary Colors
- **Red (#EF4444):** Deepfake feature, danger, critical alerts
- **Blue (#3B82F6):** Primary CTAs, social media feature, trust
- **Purple (#8B5CF6):** Catfish feature, analytics
- **Green (#10B981):** Success states, positive feedback
- **Yellow (#F59E0B):** Warnings, hints, attention

### Neutral Colors
- **Black (#000000):** All borders, primary text
- **White (#FFFFFF):** Backgrounds, cards
- **Gray-50 (#F9FAFB):** Subtle backgrounds
- **Gray-700 (#374151):** Secondary text

---

## Border & Shadow System

### Borders
```
2px - Thin borders (inner elements)
4px - Medium borders (buttons, cards)
6px - Thick borders (major sections, hero elements)
```

### Shadows
```
shadow-brutal-sm:  4px  4px 0 0 #000  (small elements)
shadow-brutal-md:  8px  8px 0 0 #000  (cards)
shadow-brutal-lg: 12px 12px 0 0 #000  (hero elements, CTAs)
```

---

## Animation Effects

### Hover Effects
```
hover-lift:
  Before: translate(0, 0), shadow: 8px 8px
  After:  translate(-2px, -2px), shadow: 12px 12px
  
hover-press:
  Before: translate(0, 0), shadow: 8px 8px
  After:  translate(2px, 2px), shadow: 4px 4px
```

### Entrance Animations
```
animate-slide-in:
  From: opacity 0, translateY(20px)
  To:   opacity 1, translateY(0)
  Duration: 300ms
  
animate-fade-in:
  From: opacity 0
  To:   opacity 1
  Duration: 400ms
```

---

## Responsive Breakpoints

```
Mobile:  < 640px   (1 column, stacked layout)
Tablet:  640-1024px (2 columns, adjusted spacing)
Desktop: > 1024px   (2-4 columns, full layout)
```

### Mobile Adaptations
- Navigation: Hamburger menu with drawer
- Feature cards: Single column
- Stats: Stacked vertically
- Footer: Single column
- Buttons: Full width

### Desktop Features
- Navigation: Full horizontal menu
- Feature cards: 2-column grid
- Stats: Horizontal row
- Footer: 4-column grid
- Buttons: Auto width

---

## Accessibility Features

### Keyboard Navigation
```
Tab       → Move to next interactive element
Shift+Tab → Move to previous element
Enter     → Activate button/link
Space     → Activate button
Escape    → Close dropdown/modal
```

### Focus Indicators
```
All interactive elements:
  focus:outline-none
  focus:ring-4
  focus:ring-brutal-blue
  
Result: 4px blue ring around focused element
```

### Screen Reader Support
```
- Skip-to-content link (visible on focus)
- ARIA labels on all icons
- aria-expanded on dropdowns
- aria-current on breadcrumbs
- Semantic HTML (nav, main, footer)
```

---

## Usage Examples

### Full Page with Navigation + Hub
```tsx
import { BrutalNavigation } from '@/app/components/BrutalNavigation';
import { FeatureHub } from '@/app/components/FeatureHub';

export default function Page() {
  return (
    <div className="min-h-screen bg-white">
      <BrutalNavigation />
      <FeatureHub />
    </div>
  );
}
```

### Feature Page with Layout
```tsx
import { BrutalNavigation } from '@/app/components/BrutalNavigation';
import { BrutalPageLayout } from '@/app/components/BrutalPageLayout';

export default function Page() {
  return (
    <>
      <BrutalNavigation />
      <BrutalPageLayout>
        <div className="max-w-7xl mx-auto px-4 py-16">
          {/* Your content */}
        </div>
      </BrutalPageLayout>
    </>
  );
}
```

---

## Component Hierarchy

```
BrutalNavigation (sticky, top-level)
  ├─ Logo + Brand
  ├─ Desktop Menu
  │   ├─ Features Dropdown
  │   ├─ About Link
  │   └─ Auth Buttons
  └─ Mobile Menu (drawer)
      ├─ Features Section
      ├─ About Link
      └─ Auth Buttons

FeatureHub (full page)
  ├─ Hero Section
  │   ├─ Title
  │   ├─ Stats Cards
  │   └─ CTA Buttons
  ├─ Features Grid
  │   └─ 4 Feature Cards
  ├─ CTA Section
  └─ Why Choose Section

BrutalPageLayout (wrapper)
  ├─ Breadcrumbs
  ├─ Main Content (slot)
  └─ Footer
      ├─ Brand Section
      ├─ Features Links
      ├─ Resources Links
      ├─ Legal Links
      └─ Bottom Bar
```

---

This visual guide provides a clear understanding of the component structure, styling, and usage patterns for the brutalist design system.
