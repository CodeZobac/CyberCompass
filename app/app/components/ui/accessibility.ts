/**
 * Accessibility Utilities Index
 * Central export for all accessibility-related components and hooks
 */

// Keyboard Navigation
export {
  useKeyboardShortcuts,
  GlobalKeyboardShortcuts,
  KeyboardShortcutsHelp,
  type KeyboardShortcut,
} from './keyboard-shortcuts';

export { KeyboardNavigationDetector } from './keyboard-navigation-detector';

// ARIA and Semantic HTML
export {
  AriaLive,
  VisuallyHidden,
  SROnly,
} from './aria-live';

// Color Contrast
export {
  getContrastRatio,
  meetsWCAGAA,
  meetsWCAGAAA,
  getAccessibleTextColor,
  ContrastChecker,
  accessibleColors,
  brutalColorCompliance,
} from './color-contrast';

// Motion Preferences
export {
  useReducedMotion,
  useAnimationDuration,
  useConditionalAnimation,
  MotionWrapper,
  SafeAnimation,
} from './use-reduced-motion';
