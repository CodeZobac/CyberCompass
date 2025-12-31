# Motion Accessibility Implementation

## Overview

This document describes how CyberCompass respects user motion preferences to ensure accessibility for users with vestibular disorders or those who prefer reduced motion.

## WCAG 2.1 Success Criterion 2.3.3

**Animation from Interactions (Level AAA)**: Motion animation triggered by interaction can be disabled, unless the animation is essential to the functionality or the information being conveyed.

## Implementation

### CSS Media Query

All animations and transitions respect the `prefers-reduced-motion` media query:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### React Hooks

Three hooks are provided for motion-aware components:

#### 1. `useReducedMotion()`
Detects if the user prefers reduced motion.

```tsx
import { useReducedMotion } from './components/ui/use-reduced-motion';

function MyComponent() {
  const prefersReducedMotion = useReducedMotion();
  
  return (
    <div className={prefersReducedMotion ? '' : 'animate-slideIn'}>
      Content
    </div>
  );
}
```

#### 2. `useAnimationDuration(duration)`
Returns 0 if user prefers reduced motion, otherwise returns the specified duration.

```tsx
import { useAnimationDuration } from './components/ui/use-reduced-motion';

function MyComponent() {
  const duration = useAnimationDuration(300);
  
  return (
    <div style={{ transitionDuration: `${duration}ms` }}>
      Content
    </div>
  );
}
```

#### 3. `useConditionalAnimation(animationClass)`
Returns empty string if user prefers reduced motion, otherwise returns the animation class.

```tsx
import { useConditionalAnimation } from './components/ui/use-reduced-motion';

function MyComponent() {
  const animation = useConditionalAnimation('animate-slideIn');
  
  return (
    <div className={animation}>
      Content
    </div>
  );
}
```

### Components

#### `MotionWrapper`
Wraps content and disables animations if user prefers reduced motion.

```tsx
import { MotionWrapper } from './components/ui/use-reduced-motion';

function MyComponent() {
  return (
    <MotionWrapper className="animate-fadeIn">
      <p>This content will not animate if user prefers reduced motion</p>
    </MotionWrapper>
  );
}
```

#### `SafeAnimation`
Automatically respects motion preferences.

```tsx
import { SafeAnimation } from './components/ui/use-reduced-motion';

function MyComponent() {
  return (
    <SafeAnimation animationClass="animate-slideIn" duration={300} delay={100}>
      <p>This content animates safely</p>
    </SafeAnimation>
  );
}
```

## Affected Animations

### Disabled When Motion is Reduced

1. **Page Transitions**
   - Slide-in animations
   - Fade-in effects
   - Stagger animations

2. **Interactive Elements**
   - Hover lift effects
   - Button press animations
   - Card hover transforms

3. **Loading States**
   - Spinner rotations (instant display)
   - Shimmer effects
   - Pulse animations

4. **Feedback Animations**
   - Success celebrations
   - Error shake effects
   - Achievement unlocks

5. **Scroll Behaviors**
   - Smooth scrolling (becomes instant)
   - Parallax effects
   - Scroll-triggered animations

### Always Enabled (Essential Animations)

These animations are essential to functionality and remain enabled:

1. **Focus Indicators**
   - Keyboard focus outlines
   - Tab navigation highlights

2. **Loading Indicators**
   - Progress bars (position changes)
   - Status updates

3. **State Changes**
   - Form validation feedback
   - Toggle switches
   - Checkbox/radio states

## Testing

### Manual Testing

#### macOS
1. Open System Preferences
2. Go to Accessibility → Display
3. Enable "Reduce motion"
4. Reload the application

#### Windows 10/11
1. Open Settings
2. Go to Ease of Access → Display
3. Enable "Show animations in Windows"
4. Reload the application

#### iOS
1. Open Settings
2. Go to Accessibility → Motion
3. Enable "Reduce Motion"
4. Reload the application

#### Android
1. Open Settings
2. Go to Accessibility
3. Enable "Remove animations"
4. Reload the application

### Browser DevTools Testing

#### Chrome/Edge
1. Open DevTools (F12)
2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows)
3. Type "Emulate CSS prefers-reduced-motion"
4. Select "Emulate CSS prefers-reduced-motion: reduce"

#### Firefox
1. Open DevTools (F12)
2. Go to Settings (gear icon)
3. Under "Advanced settings", find "Enable accessibility features"
4. Use the accessibility panel to toggle motion preferences

### Automated Testing

```javascript
// Example test using Jest and Testing Library
import { render } from '@testing-library/react';
import { useReducedMotion } from './use-reduced-motion';

describe('Motion Preferences', () => {
  it('respects prefers-reduced-motion', () => {
    // Mock matchMedia
    window.matchMedia = jest.fn().mockImplementation(query => ({
      matches: query === '(prefers-reduced-motion: reduce)',
      media: query,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    }));

    const { result } = renderHook(() => useReducedMotion());
    expect(result.current).toBe(true);
  });
});
```

## Component Examples

### Deepfake Detection Challenge

```tsx
// Before
<div className="animate-slideIn">
  <Card>Challenge content</Card>
</div>

// After
<SafeAnimation animationClass="animate-slideIn" duration={300}>
  <Card>Challenge content</Card>
</SafeAnimation>
```

### Social Media Simulation

```tsx
// Before
<div className="animate-fadeIn">
  <Post />
</div>

// After
const animation = useConditionalAnimation('animate-fadeIn');
<div className={animation}>
  <Post />
</div>
```

### Analytics Dashboard

```tsx
// Before
<div className="animate-pulse-brutal">
  <StatCard />
</div>

// After
const prefersReducedMotion = useReducedMotion();
<div className={prefersReducedMotion ? '' : 'animate-pulse-brutal'}>
  <StatCard />
</div>
```

## Best Practices

### DO ✅

1. **Always respect motion preferences** for decorative animations
2. **Use the provided hooks** for consistent behavior
3. **Test with motion preferences enabled** during development
4. **Provide alternative feedback** when animations are disabled
5. **Keep essential animations** that convey important information

### DON'T ❌

1. **Don't disable focus indicators** - they're essential for accessibility
2. **Don't remove all transitions** - instant changes can be jarring
3. **Don't assume animations are always visible** - design for both states
4. **Don't use motion as the only indicator** - provide text/icon alternatives
5. **Don't override user preferences** - respect their choices

## Animation Guidelines

### Decorative Animations (Should Respect Preference)
- Hover effects on cards
- Slide-in page transitions
- Confetti celebrations
- Shimmer loading effects
- Parallax scrolling

### Functional Animations (Can Remain)
- Progress bar updates
- Form validation feedback
- Loading spinners (simplified)
- State change indicators
- Focus outlines

### Reduced Motion Alternatives

Instead of removing animations entirely, consider:

1. **Instant transitions** - Change state immediately
2. **Fade only** - Use opacity changes instead of movement
3. **Simplified effects** - Reduce complexity while maintaining feedback
4. **Static alternatives** - Show final state immediately

## Performance Benefits

Respecting motion preferences also improves performance:

1. **Reduced CPU usage** - Fewer animation calculations
2. **Better battery life** - Less GPU activity
3. **Faster perceived performance** - Instant state changes
4. **Improved accessibility** - Better for users with vestibular disorders

## Compliance Status

✅ **WCAG 2.1 Level AAA Compliant**

All animations in CyberCompass respect the `prefers-reduced-motion` media query, meeting and exceeding WCAG 2.1 Success Criterion 2.3.3 (Level AAA).

## Resources

- [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [WCAG 2.1: Animation from Interactions](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)
- [A11y Project: Motion Sensitivity](https://www.a11yproject.com/posts/understanding-vestibular-disorders/)
- [WebAIM: Accessible Animations](https://webaim.org/articles/seizure/)

---

*Last Updated: 2024*
*Implemented By: Accessibility Task 8.4*
