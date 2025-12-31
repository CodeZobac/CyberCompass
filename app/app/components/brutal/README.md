# Brutalist Design System Components

This directory contains the brutalist-themed UI components for the AI Features section of CyberCompass.

## Components

### 1. BrutalNavigation

A global navigation bar following the brutalist design aesthetic with bold borders, high contrast, and tactile interactions.

**Features:**
- Desktop navigation with logo and links
- Mobile hamburger menu with slide-in drawer
- Dropdown menu for AI features
- Authentication state display (Sign In/Profile/Sign Out)
- Keyboard navigation support (Tab, Enter, Space, Escape)
- Skip-to-content link for accessibility
- Admin panel link (conditional on user role)

**Usage:**
```tsx
import { BrutalNavigation } from '@/app/components/BrutalNavigation';

export default function Page() {
  return (
    <>
      <BrutalNavigation />
      {/* Your page content */}
    </>
  );
}
```

**Accessibility:**
- ARIA labels on all interactive elements
- Keyboard navigation with visible focus indicators
- Skip-to-content link for screen readers
- Proper semantic HTML structure

---

### 2. FeatureHub

A landing page component showcasing all AI-powered features with an engaging hero section and feature cards.

**Features:**
- Hero section with platform overview and stats
- Feature cards grid (4 AI features)
- Hover effects and animations
- Responsive layout (1 column mobile, 2 columns desktop)
- Call-to-action buttons
- "Why Choose CyberCompass" section

**Usage:**
```tsx
import { FeatureHub } from '@/app/components/FeatureHub';

export default function AIFeaturesPage() {
  return <FeatureHub />;
}
```

**Features Included:**
1. Deepfake Detection Training
2. Social Media Simulation
3. Catfish Detection Training
4. Analytics Dashboard

---

### 3. BrutalPageLayout

A consistent page structure template with breadcrumb navigation and footer.

**Features:**
- Automatic breadcrumb generation from pathname
- Custom breadcrumb support
- Brutalist footer with links and social media
- Skip-to-content link integration
- Optional footer display
- Responsive design

**Usage:**
```tsx
import { BrutalPageLayout } from '@/app/components/BrutalPageLayout';

export default function Page() {
  // Option 1: Auto-generate breadcrumbs
  return (
    <BrutalPageLayout>
      <YourContent />
    </BrutalPageLayout>
  );

  // Option 2: Custom breadcrumbs
  const breadcrumbs = [
    { label: 'Home', href: '/' },
    { label: 'AI Features', href: '/ai-features' },
    { label: 'Current Page' }
  ];

  return (
    <BrutalPageLayout breadcrumbs={breadcrumbs}>
      <YourContent />
    </BrutalPageLayout>
  );

  // Option 3: Without footer
  return (
    <BrutalPageLayout showFooter={false}>
      <YourContent />
    </BrutalPageLayout>
  );
}
```

**Props:**
- `children`: ReactNode (required) - Page content
- `breadcrumbs`: BreadcrumbItem[] (optional) - Custom breadcrumb items
- `showFooter`: boolean (optional, default: true) - Show/hide footer

---

## Design Principles

### Brutalist Foundation
- **Bold Borders:** 4-6px black borders on all major elements
- **Box Shadows:** Offset shadows (4px-12px) for depth
- **High Contrast:** Black borders, white backgrounds, vibrant accent colors
- **Typography:** Bold, uppercase headings; clear hierarchy
- **Geometric Shapes:** Rectangles, squares, minimal rounding

### Color System
```css
--brutal-red: #EF4444      /* Danger, deepfakes, critical */
--brutal-blue: #3B82F6     /* Primary actions, trust */
--brutal-green: #10B981    /* Success, correct answers */
--brutal-yellow: #F59E0B   /* Warnings, hints */
--brutal-purple: #8B5CF6   /* Analytics, premium */
--brutal-pink: #EC4899     /* Social features */
--brutal-black: #000000    /* Borders, text */
--brutal-white: #FFFFFF    /* Backgrounds */
--brutal-gray-50: #F9FAFB  /* Subtle backgrounds */
--brutal-gray-100: #F3F4F6 /* Disabled states */
--brutal-gray-700: #374151 /* Secondary text */
```

### Animation Philosophy
- **Purposeful:** Animations guide attention and provide feedback
- **Snappy:** Quick transitions (150-300ms)
- **Transform-based:** Use translate/scale for performance
- **Respect Motion Preferences:** Honor prefers-reduced-motion

### Utility Classes

**Shadows:**
```css
.shadow-brutal-sm  /* 4px 4px 0 0 #000 */
.shadow-brutal-md  /* 8px 8px 0 0 #000 */
.shadow-brutal-lg  /* 12px 12px 0 0 #000 */
```

**Hover Effects:**
```css
.hover-lift   /* Lifts element up and left on hover */
.hover-press  /* Presses element down and right on hover */
```

**Animations:**
```css
.animate-slide-in      /* Slide in from bottom */
.animate-fade-in       /* Fade in */
.animate-pulse-brutal  /* Pulse scale effect */
.animate-shimmer       /* Loading shimmer effect */
```

---

## Accessibility Features

All components follow WCAG 2.1 AA standards:

1. **Keyboard Navigation**
   - All interactive elements are keyboard accessible
   - Visible focus indicators (4px blue outline)
   - Logical tab order

2. **Screen Reader Support**
   - Semantic HTML elements
   - ARIA labels on all icons and buttons
   - ARIA live regions for dynamic content
   - Alt text on all images

3. **Color Contrast**
   - Text meets 4.5:1 contrast ratio
   - Large text meets 3:1 contrast ratio
   - Interactive elements have clear visual distinction

4. **Motion Preferences**
   - Respects `prefers-reduced-motion` media query
   - Animations disabled for users who prefer reduced motion

---

## Example Pages

### AI Features Hub
```tsx
// app/[locale]/ai-features/page.tsx
import { BrutalNavigation } from '@/app/components/BrutalNavigation';
import { FeatureHub } from '@/app/components/FeatureHub';

export default function AIFeaturesPage() {
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
// app/[locale]/deepfake-training/page.tsx
import { BrutalNavigation } from '@/app/components/BrutalNavigation';
import { BrutalPageLayout } from '@/app/components/BrutalPageLayout';

export default function DeepfakeTrainingPage() {
  const breadcrumbs = [
    { label: 'Home', href: '/' },
    { label: 'AI Features', href: '/ai-features' },
    { label: 'Deepfake Training' }
  ];

  return (
    <>
      <BrutalNavigation />
      <BrutalPageLayout breadcrumbs={breadcrumbs}>
        {/* Your page content */}
      </BrutalPageLayout>
    </>
  );
}
```

---

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Android Chrome)

---

## Performance

- Components use CSS transforms for animations (GPU-accelerated)
- Minimal JavaScript for interactions
- No external dependencies beyond Next.js and NextAuth
- Optimized for Core Web Vitals

---

## Future Enhancements

- [ ] Dark mode support (if needed)
- [ ] Additional animation variants
- [ ] More color themes
- [ ] Component variants (sizes, styles)
- [ ] Storybook documentation
