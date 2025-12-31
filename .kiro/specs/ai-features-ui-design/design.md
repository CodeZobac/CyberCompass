# Design Document

## Overview

This document outlines the comprehensive UI/UX design for the AI-powered educational features in CyberCompass. The design follows the brutalist aesthetic with bold borders, high contrast colors, impactful typography, and tactile interactions while creating an engaging, modern learning experience.

## Design Principles

### 1. Brutalist Foundation
- **Bold Borders:** 4-6px black borders on all major elements
- **Box Shadows:** Offset shadows (4px-12px) for depth
- **High Contrast:** Black borders, white backgrounds, vibrant accent colors
- **Typography:** Bold, uppercase headings; clear hierarchy
- **Geometric Shapes:** Rectangles, squares, no rounded corners (except minimal 2px for usability)

### 2. Visual Hierarchy
- **Primary Actions:** Largest, most prominent (blue/red accents)
- **Secondary Actions:** Medium size, outlined style
- **Tertiary Actions:** Smaller, minimal styling
- **Content Sections:** Clear separation with borders and spacing

### 3. Animation Philosophy
- **Purposeful:** Animations guide attention and provide feedback
- **Snappy:** Quick transitions (150-300ms)
- **Transform-based:** Use translate/scale for performance
- **Respect Motion Preferences:** Honor prefers-reduced-motion

### 4. Color System

```
Primary Colors:
- Red (#EF4444): Danger, deepfakes, critical alerts
- Blue (#3B82F6): Primary actions, trust, authentic content
- Green (#10B981): Success, correct answers, achievements
- Yellow (#F59E0B): Warnings, hints, attention
- Purple (#8B5CF6): Analytics, premium features
- Pink (#EC4899): Social features, engagement

Neutral Colors:
- Black (#000000): Borders, text, emphasis
- White (#FFFFFF): Backgrounds, cards
- Gray-50 (#F9FAFB): Subtle backgrounds
- Gray-100 (#F3F4F6): Disabled states
- Gray-700 (#374151): Secondary text
```

## Architecture

### Page Structure Template

All AI feature pages follow this consistent structure:

```
┌─────────────────────────────────────────┐
│ Navigation Bar (Global)                 │
├─────────────────────────────────────────┤
│ Hero Section                            │
│ - Bold Title                            │
│ - Subtitle/Description                  │
│ - Key Stats/CTA                         │
├─────────────────────────────────────────┤
│ Introduction/Instructions (Optional)    │
├─────────────────────────────────────────┤
│ Main Content Area                       │
│ - Feature-specific interface           │
│ - Interactive elements                  │
├─────────────────────────────────────────┤
│ Progress/Stats Sidebar (Optional)       │
├─────────────────────────────────────────┤
│ Results/Feedback Section (Conditional)  │
├─────────────────────────────────────────┤
│ Related Features/Next Steps             │
├─────────────────────────────────────────┤
│ Footer (Global)                         │
└─────────────────────────────────────────┘
```



## Component Designs

### 1. Deepfake Detection Training Page

#### Hero Section
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  🎭 DEEPFAKE DETECTION TRAINING                    │
│  [Massive 8xl font, red color, black text-shadow] │
│                                                    │
│  Master the art of spotting manipulated media     │
│  [2xl font, gray-700, semibold]                   │
│                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ 🎯 45    │ │ ✓ 89%    │ │ 🔥 7     │          │
│  │ Trained  │ │ Accuracy │ │ Streak   │          │
│  └──────────┘ └──────────┘ └──────────┘          │
│                                                    │
│  [START TRAINING →] [VIEW PROGRESS]               │
└────────────────────────────────────────────────────┘

Styling:
- Background: Gradient from red-50 to white
- Border-bottom: 6px solid black
- Padding: 80px 24px
- Stats cards: White bg, 4px black border, 8px shadow
- Buttons: Brutal style with hover transforms
```

#### Challenge Interface
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│ ┌────────────────┐  CHALLENGE 3 OF 10             │
│ │ DIFFICULTY     │  ████████░░ 80%                │
│ │ ⚠️ HARD        │                                 │
│ └────────────────┘                                 │
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │                                              │  │
│ │         [MEDIA CONTENT AREA]                 │  │
│ │         Video/Image/Audio Player             │  │
│ │         Large, centered, bordered            │  │
│ │                                              │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ [💡 SHOW HINTS] ← Toggleable                      │
│                                                    │
│ ┌──────────────────────┐ ┌──────────────────────┐ │
│ │   ✓ AUTHENTIC        │ │   ✗ DEEPFAKE         │ │
│ │   [Large button]     │ │   [Large button]     │ │
│ └──────────────────────┘ └──────────────────────┘ │
│                                                    │
│ [SUBMIT ANSWER →]                                 │
└────────────────────────────────────────────────────┘

Styling:
- Media container: 16:9 aspect ratio, 6px border
- Decision buttons: 50% width each, 6px border
- Selected state: Filled color, 8px shadow, translate
- Hints panel: Yellow-100 bg, 4px yellow-500 border
```



#### Results Display
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│ ┌──────────────────────────────────────────────┐  │
│ │ ✓ CORRECT! WELL DONE!                        │  │
│ │ [Green-500 bg, white text, 6px border]       │  │
│ │                                              │  │
│ │ You correctly identified this as a deepfake. │  │
│ │ Your attention to detail is improving!       │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ 🔍 DETECTION CLUES REVEALED                        │
│ ┌──────────────────────────────────────────────┐  │
│ │ • Unnatural eye movements                    │  │
│ │ • Inconsistent lighting on face              │  │
│ │ • Blurred edges around hairline              │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ 🔬 TECHNICAL ANALYSIS                              │
│ ┌──────────────────────────────────────────────┐  │
│ │ • GAN artifacts detected in facial region    │  │
│ │ • Temporal inconsistencies in frame 45-67    │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ [NEXT CHALLENGE →] [VIEW DETAILED ANALYSIS]       │
└────────────────────────────────────────────────────┘

Animations:
- Slide in from bottom (300ms ease-out)
- Confetti animation for correct answers
- Pulse effect on score increase
```

### 2. Social Media Simulation Page

#### Hero Section
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  📱 SOCIAL MEDIA SIMULATION                        │
│  [Massive 8xl font, blue color]                   │
│                                                    │
│  Navigate the feed. Spot the lies.                │
│  [2xl font, gray-700]                             │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │ Test your critical thinking in a simulated  │  │
│  │ social media environment filled with both   │  │
│  │ authentic content and disinformation.       │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  [START SIMULATION →]                             │
└────────────────────────────────────────────────────┘

Styling:
- Background: Gradient blue-50 to white
- Info box: Blue-100 bg, 4px blue-500 border
- Large CTA button with pulse animation
```



#### Feed Interface
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│ POST 3 OF 10  ████████░░ 80%  [END SIMULATION]   │
├────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────┐  │
│ │ 👤 Health News Daily        [Not Verified]   │  │
│ │ 2 hours ago                                  │  │
│ ├──────────────────────────────────────────────┤  │
│ │                                              │  │
│ │ BREAKING: New study shows miracle cure      │  │
│ │ for all diseases! Doctors hate this trick!  │  │
│ │                                              │  │
│ │ [Optional: Image/Video content]              │  │
│ │                                              │  │
│ ├──────────────────────────────────────────────┤  │
│ │ ❤️ 15.2K  🔄 8.9K  💬 456                    │  │
│ ├──────────────────────────────────────────────┤  │
│ │ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐         │  │
│ │ │ LIKE │ │SHARE │ │REPORT│ │ SKIP │         │  │
│ │ └──────┘ └──────┘ └──────┘ └──────┘         │  │
│ └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘

Styling:
- Post card: White bg, 6px black border, 8px shadow
- Verified badge: Blue-500 bg, white text
- Report button: Red-500 bg, prominent
- Hover states: Lift effect with shadow increase
- Grid layout: 2x2 for action buttons
```

#### Results Dashboard
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  📊 SIMULATION RESULTS                             │
│                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │    7     │ │    2     │ │    1     │          │
│  │ CORRECT  │ │ MISSED   │ │  FALSE   │          │
│  │ REPORTS  │ │ DISINFO  │ │ REPORTS  │          │
│  └──────────┘ └──────────┘ └──────────┘          │
│                                                    │
│  💡 ENGAGEMENT IMPACT                              │
│  ┌──────────────────────────────────────────────┐ │
│  │ Your sharing patterns amplified 2 pieces of  │ │
│  │ disinformation. Be more cautious!            │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  🎯 RECOMMENDATIONS                                │
│  • Always verify sources before sharing           │
│  • Look for verification badges                   │
│  • Be skeptical of sensational headlines          │
│                                                    │
│  [TRY AGAIN] [VIEW DETAILED ANALYSIS]             │
└────────────────────────────────────────────────────┘

Styling:
- Stats cards: Color-coded (green/red/yellow)
- Large numbers: 4xl font, bold
- Impact section: Blue-100 bg, 4px border
- Recommendations: Checklist style with icons
```



### 3. Catfish Detection Training Page

#### Hero Section
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  💬 CATFISH DETECTION TRAINING                     │
│  [Massive 8xl font, purple color]                 │
│                                                    │
│  Learn to spot red flags in online conversations  │
│  [2xl font, gray-700]                             │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │ 🎭 Chat with suspicious characters          │  │
│  │ 🚩 Identify red flags in real-time          │  │
│  │ 📊 Get detailed performance analysis        │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  [START CHAT SIMULATION →]                        │
└────────────────────────────────────────────────────┘

Styling:
- Background: Gradient purple-50 to white
- Feature list: Purple-100 bg, icons, 4px border
- Messaging app aesthetic in hero
```

#### Chat Interface
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│ 💬 CATFISH DETECTION CHAT                         │
│ Messages: 12  |  Flags: 3  |  [🚩 REPORT FLAG]   │
├────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────┐  │
│ │                                              │  │
│ │  ┌─────────────────────┐                     │  │
│ │  │ Hey! I'm 16 and     │ [Them - Left]       │  │
│ │  │ from California     │                     │  │
│ │  └─────────────────────┘                     │  │
│ │  2:34 PM                                     │  │
│ │                                              │  │
│ │                     ┌─────────────────────┐  │  │
│ │       [You - Right] │ Nice to meet you!   │  │  │
│ │                     │ What school do you  │  │  │
│ │                     │ go to?              │  │  │
│ │                     └─────────────────────┘  │  │
│ │                                     2:35 PM  │  │
│ │                                              │  │
│ │  [Typing indicator...]                       │  │
│ │                                              │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌──────────────────────────────────────────────┐  │
│ │ Type your message...              [SEND →]   │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ [END SIMULATION]                                  │
└────────────────────────────────────────────────────┘

Styling:
- Chat bubbles: Different colors for user/character
- User messages: Blue-500 bg, white text, right-aligned
- Character messages: Gray-200 bg, black text, left-aligned
- Borders: 3px on bubbles, 6px on container
- Timestamps: Small, gray-500
- Report button: Red-500, prominent, always visible
```



#### Analysis Results
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  🔍 SIMULATION ANALYSIS                            │
│                                                    │
│  ┌──────────┐ ┌──────────┐                        │
│  │    75    │ │   60%    │                        │
│  │  SCORE   │ │ DETECTED │                        │
│  └──────────┘ └──────────┘                        │
│                                                    │
│  🚩 RED FLAGS DETECTED                             │
│  ┌──────────────────────────────────────────────┐ │
│  │ ⚠️ HIGH   Age Inconsistency                  │ │
│  │          Character claimed different ages     │ │
│  ├──────────────────────────────────────────────┤ │
│  │ ⚠️ MEDIUM Evasive Behavior                   │ │
│  │          Avoided direct questions             │ │
│  ├──────────────────────────────────────────────┤ │
│  │ ⚠️ HIGH   Location Inconsistency             │ │
│  │          Mentioned UK references but said CA  │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  💡 CHARACTER INCONSISTENCIES                      │
│  • Claimed to be 16 but used 1990s slang         │
│  • Profile photo appears to be stock image        │
│  • Story about school changed between chats       │
│                                                    │
│  🎯 RECOMMENDATIONS                                │
│  • Always verify profile information              │
│  • Be cautious of people who avoid video calls    │
│  • Look for inconsistencies in stories            │
│                                                    │
│  [TRY AGAIN] [VIEW DETAILED REPORT]               │
└────────────────────────────────────────────────────┘

Styling:
- Red flags: Severity-based colors (red/yellow/green)
- Flag cards: White bg, left border (6px) in severity color
- Inconsistencies: Bullet list with icons
- Recommendations: Action-oriented with checkboxes
```

### 4. Analytics Dashboard Page

#### Hero Section
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  📊 YOUR LEARNING ANALYTICS                        │
│  [Massive 8xl font, gradient blue-purple]         │
│                                                    │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐             │
│  │  8   │ │ 🔥7  │ │  45  │ │ 78%  │             │
│  │LEVEL │ │STREAK│ │DONE  │ │RANK  │             │
│  └──────┘ └──────┘ └──────┘ └──────┘             │
│                                                    │
│  PROGRESS TO LEVEL 9                               │
│  ████████████████░░░░ 2,340 / 3,000 XP            │
│                                                    │
└────────────────────────────────────────────────────┘

Styling:
- Background: Gradient from blue-500 to purple-600
- All text: White
- Stats cards: White bg, 4px black border
- XP bar: Yellow-400 fill, white border, black outline
- Large numbers: 3xl font, bold
```



#### Tab Navigation
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│ [OVERVIEW] [ACHIEVEMENTS] [RECOMMENDATIONS]        │
└────────────────────────────────────────────────────┘

Styling:
- Active tab: Blue-500 bg, white text, 4px border, raised
- Inactive tabs: White bg, black text, 4px border
- Hover: Gray-50 bg
- Border-bottom: 4px black on container
- Smooth slide animation on tab change
```

#### Competency Scores (Overview Tab)
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  🎯 COMPETENCY SCORES                              │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ Deepfake Detection          📈 75%           │ │
│  │ ████████████████░░░░                         │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ Disinformation Awareness    📈 82%           │ │
│  │ ████████████████████░                        │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ Catfish Detection           ➡️ 68%           │ │
│  │ ██████████████░░░░░░                         │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ Cyberbullying Prevention    📈 90%           │ │
│  │ ██████████████████████░░                     │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘

Styling:
- Score cards: White bg, 4px black border, 4px shadow
- Progress bars: Color-coded by score (green/yellow/red)
- Trend icons: Animated on hover
- Bars: 4px height, 2px black border
```

#### Achievements (Achievements Tab)
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  🏆 ACHIEVEMENTS                                   │
│                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ LEGENDARY│ │   EPIC   │ │   RARE   │          │
│  │          │ │          │ │          │          │
│  │    🔥    │ │    🎯    │ │    🔍    │          │
│  │          │ │          │ │          │          │
│  │  Week    │ │ Perfect  │ │ Deepfake │          │
│  │ Warrior  │ │  Score   │ │ Detective│          │
│  │          │ │          │ │          │          │
│  │ Earned:  │ │ Earned:  │ │ Earned:  │          │
│  │ Today    │ │ 2d ago   │ │ 5d ago   │          │
│  └──────────┘ └──────────┘ └──────────┘          │
└────────────────────────────────────────────────────┘

Styling:
- Achievement cards: Gradient backgrounds by rarity
  - Legendary: Yellow-400 to orange-500
  - Epic: Purple-500 to pink-500
  - Rare: Blue-500 to cyan-500
  - Common: Gray-400 to gray-500
- Large emoji icons: 6xl size
- Card borders: 4px black
- Hover: Lift and glow effect
- Grid: 3 columns on desktop, 1 on mobile
```



#### Recommendations (Recommendations Tab)
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  💡 PERSONALIZED RECOMMENDATIONS                   │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ [HIGH] Catfish Detection                     │ │
│  │                                              │ │
│  │ Your catfish detection skills need           │ │
│  │ improvement. Focus on identifying            │ │
│  │ inconsistencies in conversations.            │ │
│  │                                              │ │
│  │ 🎯 SUGGESTED CHALLENGES:                     │ │
│  │ [Advanced Scenarios] [Red Flag Recognition]  │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │ [MEDIUM] Deepfake Detection                  │ │
│  │                                              │ │
│  │ Continue practicing with more complex        │ │
│  │ deepfake examples to sharpen your skills.    │ │
│  │                                              │ │
│  │ 🎯 SUGGESTED CHALLENGES:                     │ │
│  │ [Expert Analysis] [Audio Deepfakes]          │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘

Styling:
- Priority badges: Color-coded (red/yellow/green)
- Recommendation cards: White bg, left border (6px) in priority color
- Challenge buttons: Blue-500 bg, white text, 2px border
- Hover: Lift effect on entire card
```

## Shared Components

### Navigation Bar
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│ 🛡️ CYBERCOMPASS    [Features ▼] [Profile] [Sign In]│
└────────────────────────────────────────────────────┘

Styling:
- Background: White
- Border-bottom: 4px black
- Logo: Bold, red color
- Links: Black text, hover underline
- Dropdown: White bg, 4px border, shadow
- Mobile: Hamburger menu, slide-in drawer
```

### Feature Cards (Landing/Hub Page)
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │   🎭     │ │   📱     │ │   💬     │          │
│  │          │ │          │ │          │          │
│  │ DEEPFAKE │ │  SOCIAL  │ │ CATFISH  │          │
│  │DETECTION │ │  MEDIA   │ │DETECTION │          │
│  │          │ │   SIM    │ │          │          │
│  │ Master   │ │ Navigate │ │ Spot red │          │
│  │ spotting │ │ the feed │ │ flags in │          │
│  │ fakes    │ │ safely   │ │ chats    │          │
│  │          │ │          │ │          │          │
│  │[START →] │ │[START →] │ │[START →] │          │
│  └──────────┘ └──────────┘ └──────────┘          │
│                                                    │
│  ┌──────────┐                                     │
│  │   📊     │                                     │
│  │          │                                     │
│  │ANALYTICS │                                     │
│  │DASHBOARD │                                     │
│  │          │                                     │
│  │ Track    │                                     │
│  │ your     │                                     │
│  │ progress │                                     │
│  │          │                                     │
│  │[VIEW →]  │                                     │
│  └──────────┘                                     │
└────────────────────────────────────────────────────┘

Styling:
- Cards: White bg, 6px black border, 8px shadow
- Icons: 6xl size, centered
- Hover: Lift effect, shadow increase
- Grid: 3 columns desktop, 1 column mobile
- CTA buttons: Brutal style, full width
```



### Loading States
```
Skeleton Screens:
- Use gray-200 backgrounds with animated shimmer
- Maintain layout structure
- 4px black borders on skeleton elements
- Pulse animation (1.5s duration)

Spinners:
- Black border spinner (4px)
- Rotate animation (1s linear infinite)
- Centered in container
- Accompanied by text: "LOADING..."

Progress Indicators:
- Horizontal bars with percentage
- Black border, colored fill
- Animated width transition
```

### Error States
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  ⚠️ OOPS! SOMETHING WENT WRONG                     │
│                                                    │
│  We couldn't load this content. Please try again. │
│                                                    │
│  [TRY AGAIN] [GO BACK]                            │
└────────────────────────────────────────────────────┘

Styling:
- Background: Red-100
- Border: 4px red-500
- Icon: Large, red-500
- Buttons: Outlined style
- Centered in container
```

### Success Notifications
```
Visual Layout:
┌────────────────────────────────────────────────────┐
│  ✓ SUCCESS!                                        │
│  Your progress has been saved.                     │
└────────────────────────────────────────────────────┘

Styling:
- Background: Green-500
- Text: White, bold
- Border: 4px black
- Position: Top-right corner, fixed
- Animation: Slide in from right, auto-dismiss after 3s
```

## Responsive Design

### Breakpoints
```
Mobile: < 640px
Tablet: 640px - 1024px
Desktop: > 1024px
```

### Mobile Adaptations
1. **Navigation:** Hamburger menu with slide-in drawer
2. **Hero Sections:** Stack stats vertically, reduce font sizes
3. **Feature Cards:** Single column layout
4. **Chat Interface:** Full-screen on mobile
5. **Analytics:** Stack all visualizations vertically
6. **Buttons:** Full-width on mobile
7. **Touch Targets:** Minimum 44x44px

### Tablet Adaptations
1. **Grid Layouts:** 2 columns instead of 3
2. **Hero Sections:** Slightly reduced padding
3. **Font Sizes:** Scale down by 10-20%
4. **Sidebars:** Convert to collapsible panels



## Animation Specifications

### Micro-interactions
```css
/* Button Hover */
.brutal-button:hover {
  transform: translate(2px, 2px);
  box-shadow: 4px 4px 0 0 #000;
  transition: all 150ms ease-out;
}

/* Card Hover */
.feature-card:hover {
  transform: translate(-2px, -2px);
  box-shadow: 12px 12px 0 0 #000;
  transition: all 200ms ease-out;
}

/* Tab Switch */
.tab-content {
  animation: slideIn 300ms ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Success Pulse */
.success-indicator {
  animation: pulse 500ms ease-out;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* Loading Shimmer */
.skeleton {
  background: linear-gradient(
    90deg,
    #f3f4f6 0%,
    #e5e7eb 50%,
    #f3f4f6 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Page Transitions
```css
/* Fade In on Load */
.page-content {
  animation: fadeIn 400ms ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Stagger Children */
.stagger-container > * {
  animation: slideUp 300ms ease-out;
  animation-fill-mode: backwards;
}

.stagger-container > *:nth-child(1) { animation-delay: 0ms; }
.stagger-container > *:nth-child(2) { animation-delay: 100ms; }
.stagger-container > *:nth-child(3) { animation-delay: 200ms; }

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

## Accessibility Features

### Keyboard Navigation
- All interactive elements: `tabindex` and focus styles
- Focus indicator: 4px blue-500 outline with 2px offset
- Skip links: "Skip to main content" at top
- Escape key: Close modals/dropdowns

### Screen Reader Support
- Semantic HTML: `<nav>`, `<main>`, `<article>`, `<section>`
- ARIA labels: All icons and interactive elements
- ARIA live regions: For dynamic content updates
- Alt text: All images and media

### Color Contrast
- Text on white: Minimum 4.5:1 ratio
- Large text (18pt+): Minimum 3:1 ratio
- Interactive elements: Clear visual distinction
- Error states: Not relying on color alone

### Motion Preferences
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```



## Data Models

### Page State Management
```typescript
interface PageState {
  isLoading: boolean;
  error: Error | null;
  data: any;
  userInteractions: UserInteraction[];
}

interface UserInteraction {
  timestamp: Date;
  action: string;
  target: string;
  metadata?: Record<string, any>;
}
```

### Animation State
```typescript
interface AnimationState {
  isAnimating: boolean;
  currentAnimation: string | null;
  queue: Animation[];
}

interface Animation {
  type: 'slide' | 'fade' | 'pulse' | 'shake';
  duration: number;
  target: string;
  onComplete?: () => void;
}
```

## Testing Strategy

### Visual Regression Testing
- Screenshot comparison for all major components
- Test across breakpoints (mobile, tablet, desktop)
- Test in light/dark modes (if applicable)
- Test with different content lengths

### Interaction Testing
- Hover states on all interactive elements
- Click/tap feedback
- Keyboard navigation flow
- Focus management

### Performance Testing
- Lighthouse scores: > 90 for all metrics
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Animation frame rate: 60fps

### Accessibility Testing
- WAVE tool: 0 errors
- axe DevTools: 0 violations
- Keyboard-only navigation: Complete all tasks
- Screen reader testing: NVDA/JAWS/VoiceOver

## Implementation Notes

### CSS Architecture
```
styles/
├── globals.css          # Global styles, resets
├── brutalist.css        # Brutalist design tokens
├── animations.css       # Animation definitions
└── components/
    ├── buttons.css
    ├── cards.css
    ├── forms.css
    └── navigation.css
```

### Component Structure
```
components/
├── pages/
│   ├── DeepfakeTrainingPage/
│   │   ├── index.tsx
│   │   ├── HeroSection.tsx
│   │   ├── ChallengeInterface.tsx
│   │   ├── ResultsDisplay.tsx
│   │   └── styles.module.css
│   ├── SocialMediaSimPage/
│   ├── CatfishTrainingPage/
│   └── AnalyticsDashboardPage/
└── shared/
    ├── Navigation/
    ├── FeatureCard/
    ├── LoadingState/
    └── ErrorState/
```

### Performance Optimizations
1. **Image Optimization:** Next.js Image component with lazy loading
2. **Code Splitting:** Dynamic imports for heavy components
3. **CSS:** Critical CSS inline, rest deferred
4. **Fonts:** Preload, font-display: swap
5. **Animations:** Use transform/opacity only, will-change sparingly



## Error Handling

### Network Errors
```
Display: Inline error message with retry button
Style: Red-100 bg, red-500 border, 4px
Message: "Connection lost. Please check your internet."
Action: [RETRY] button
```

### Validation Errors
```
Display: Below form field
Style: Red-500 text, small font
Icon: ⚠️ warning icon
Message: Specific, actionable error text
```

### System Errors
```
Display: Full-page error state
Style: Centered, red-themed
Message: "Something went wrong. We're working on it."
Actions: [GO HOME] [CONTACT SUPPORT]
```

## Internationalization (i18n)

### Text Content
- All text: Externalized to translation files
- RTL support: Mirror layouts for Arabic/Hebrew
- Date/time: Locale-aware formatting
- Numbers: Locale-aware formatting (1,000 vs 1.000)

### Visual Content
- Icons: Universal symbols preferred
- Images: Culturally appropriate alternatives
- Colors: Consider cultural meanings

## Browser Support

### Target Browsers
- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile Safari: iOS 13+
- Chrome Mobile: Android 8+

### Fallbacks
- CSS Grid: Flexbox fallback
- CSS Custom Properties: Sass variables fallback
- Modern JS: Babel transpilation
- WebP images: JPEG/PNG fallbacks

## Deployment Considerations

### Asset Optimization
- Images: WebP with fallbacks, responsive sizes
- CSS: Minified, purged unused styles
- JS: Minified, tree-shaken
- Fonts: Subset, woff2 format

### Caching Strategy
- Static assets: 1 year cache
- HTML: No cache
- API responses: Appropriate cache headers
- Service worker: Cache-first for assets

### Monitoring
- Error tracking: Sentry or similar
- Analytics: User flow tracking
- Performance: Real User Monitoring (RUM)
- A/B testing: Feature flag system

## Future Enhancements

### Phase 2 Features
1. **Dark Mode:** Complete dark theme variant
2. **Customization:** User-selectable color themes
3. **Advanced Animations:** Lottie animations for celebrations
4. **3D Elements:** Subtle 3D transforms on cards
5. **Sound Effects:** Optional audio feedback
6. **Haptic Feedback:** Mobile vibration on interactions

### Experimental Features
1. **AR Elements:** Camera-based deepfake detection
2. **Voice Interface:** Voice commands for navigation
3. **Gesture Controls:** Swipe gestures on mobile
4. **Progressive Web App:** Offline functionality

## Conclusion

This design document provides a comprehensive blueprint for creating beautiful, engaging UI/UX pages for CyberCompass's AI features. The brutalist design aesthetic is maintained throughout while ensuring modern usability, accessibility, and performance standards.

Key principles:
- **Bold and Impactful:** Strong visual hierarchy with brutalist elements
- **User-Centric:** Intuitive interactions and clear feedback
- **Accessible:** WCAG AA compliant, keyboard navigable
- **Performant:** Optimized for speed and smooth animations
- **Responsive:** Seamless experience across all devices
- **Maintainable:** Modular components, clear architecture

The design balances aesthetic appeal with functional excellence, creating an immersive learning environment that motivates users to engage with cybersecurity education.
