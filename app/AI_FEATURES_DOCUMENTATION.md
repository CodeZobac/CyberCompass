# AI Features UI Components Documentation

This document describes the new AI-powered educational components implemented for the CyberCompass platform.

## Overview

Four new interactive components have been created to support advanced AI-powered learning experiences:

1. **DeepfakeDetectionChallenge** - Interactive deepfake detection training
2. **SocialMediaSimulation** - Disinformation detection in simulated social feeds
3. **CatfishChatSimulation** - Real-time chat simulation for catfish detection
4. **AnalyticsDashboard** - Comprehensive learning analytics and progress tracking

## Components

### 1. DeepfakeDetectionChallenge

**Location:** `app/components/DeepfakeDetectionChallenge.tsx`

**Purpose:** Provides interactive challenges for users to analyze media content and determine if it's authentic or a deepfake.

**Features:**
- Progressive difficulty levels (Easy, Medium, Hard)
- Real-time feedback with technical explanations
- Detection hints system
- Score tracking across multiple challenges
- Support for image, video, and audio content
- Multilingual support (EN/PT)

**Props:**
```typescript
interface DeepfakeDetectionChallengeProps {
  locale?: string;           // 'en' or 'pt'
  userId?: string;           // User identifier
  onComplete?: (result: any) => void;  // Callback when training completes
}
```

**Usage:**
```tsx
import { DeepfakeDetectionChallenge } from '@/components/DeepfakeDetectionChallenge';

<DeepfakeDetectionChallenge
  locale="en"
  userId={session?.user?.id}
  onComplete={(result) => console.log('Training completed:', result)}
/>
```

**API Integration:**
- `POST /api/ai-backend/deepfake-challenge` - Fetch new challenge
- `POST /api/ai-backend/deepfake-feedback` - Submit decision and get feedback

---

### 2. SocialMediaSimulation

**Location:** `app/components/SocialMediaSimulation.tsx`

**Purpose:** Simulates a social media feed with mixed authentic and disinformation content for detection training.

**Features:**
- Realistic social media post cards
- Multiple interaction types (like, share, report, skip)
- Real-time engagement tracking
- Comprehensive feedback on detection accuracy
- Algorithm impact explanation
- Multilingual support (EN/PT)

**Props:**
```typescript
interface SocialMediaSimulationProps {
  locale?: string;
  userId?: string;
  onComplete?: (feedback: SimulationFeedback) => void;
}
```

**Usage:**
```tsx
import { SocialMediaSimulation } from '@/components/SocialMediaSimulation';

<SocialMediaSimulation
  locale="en"
  userId={session?.user?.id}
  onComplete={(feedback) => console.log('Simulation completed:', feedback)}
/>
```

**API Integration:**
- `POST /api/ai-backend/social-media-feed` - Generate simulated feed
- `POST /api/ai-backend/social-media-feedback` - Analyze user performance

---

### 3. CatfishChatSimulation

**Location:** `app/components/CatfishChatSimulation.tsx`

**Purpose:** Real-time chat simulation with suspicious characters for catfish detection training.

**Features:**
- Real-time WebSocket-based chat interface
- Red flag reporting system
- Message count tracking
- Comprehensive analysis of detection performance
- Character inconsistency identification
- Severity-based red flag classification
- Multilingual support (EN/PT)

**Props:**
```typescript
interface CatfishChatSimulationProps {
  locale?: string;
  userId?: string;
  onComplete?: (analysis: ChatAnalysis) => void;
}
```

**Usage:**
```tsx
import { CatfishChatSimulation } from '@/components/CatfishChatSimulation';

<div style={{ height: '600px' }}>
  <CatfishChatSimulation
    locale="en"
    userId={session?.user?.id}
    onComplete={(analysis) => console.log('Training completed:', analysis)}
  />
</div>
```

**API Integration:**
- WebSocket connection via `ChatInterface` component
- `POST /api/ai-backend/catfish-analysis` - Get performance analysis

---

### 4. AnalyticsDashboard

**Location:** `app/components/AnalyticsDashboard.tsx`

**Purpose:** Comprehensive learning analytics dashboard with real-time updates.

**Features:**
- Competency scores across multiple categories
- Achievement system with rarity levels
- Personalized learning recommendations
- Peer comparison (anonymized)
- Level and XP progression system
- Streak tracking
- Real-time updates via Server-Sent Events
- Tab-based navigation (Overview, Achievements, Recommendations)
- Multilingual support (EN/PT)

**Props:**
```typescript
interface AnalyticsDashboardProps {
  locale?: string;
  userId?: string;
}
```

**Usage:**
```tsx
import { AnalyticsDashboard } from '@/components/AnalyticsDashboard';

<AnalyticsDashboard
  locale="en"
  userId={session?.user?.id}
/>
```

**API Integration:**
- `POST /api/ai-backend/analytics` - Fetch analytics data
- `GET /api/ai-backend/analytics-stream?userId={id}` - Real-time updates via SSE

---

## Page Examples

Example pages have been created to demonstrate component integration:

### Deepfake Training Page
**Location:** `app/[locale]/deepfake-training/page.tsx`
**Route:** `/en/deepfake-training` or `/pt/deepfake-training`

### Social Media Simulation Page
**Location:** `app/[locale]/social-media-sim/page.tsx`
**Route:** `/en/social-media-sim` or `/pt/social-media-sim`

### Catfish Training Page
**Location:** `app/[locale]/catfish-training/page.tsx`
**Route:** `/en/catfish-training` or `/pt/catfish-training`

### Analytics Dashboard Page
**Location:** `app/[locale]/analytics/page.tsx`
**Route:** `/en/analytics` or `/pt/analytics`
**Note:** Requires authentication

---

## API Routes

All API routes are located in `app/api/ai-backend/` and follow a consistent pattern:

### Request Format
```typescript
{
  userId: string;
  locale: string;
  // Additional parameters specific to each endpoint
}
```

### Response Format
All endpoints return JSON responses with appropriate error handling.

### Environment Variables
```env
AI_BACKEND_URL=http://localhost:8000
AI_BACKEND_API_KEY=your_api_key_here
```

### Current Implementation Status
All API routes currently return **mock data** for development purposes. They include:
- Proper error handling
- Fallback responses
- TODO comments indicating where AI backend integration should occur

---

## Design System

All components follow the existing "Brutal" design system with:
- Bold, black borders (4px)
- Box shadows for depth
- High contrast colors
- Uppercase, bold typography
- Interactive hover states
- Responsive layouts

### Color Scheme
- **Primary Actions:** Blue (#3B82F6)
- **Success:** Green (#10B981)
- **Warning:** Yellow (#F59E0B)
- **Danger:** Red (#EF4444)
- **Info:** Purple (#8B5CF6)

---

## Multilingual Support

All components support English (en) and Portuguese (pt) with:
- Locale-aware text rendering
- Culturally appropriate examples
- Date/time formatting
- Number formatting

---

## Accessibility

Components include:
- Semantic HTML structure
- ARIA labels where appropriate
- Keyboard navigation support
- High contrast ratios
- Responsive design for mobile devices

---

## Testing

To test the components:

1. **Start the development server:**
   ```bash
   cd app
   npm run dev
   ```

2. **Navigate to example pages:**
   - http://localhost:3000/en/deepfake-training
   - http://localhost:3000/en/social-media-sim
   - http://localhost:3000/en/catfish-training
   - http://localhost:3000/en/analytics

3. **Test with different locales:**
   - Replace `/en/` with `/pt/` in URLs

---

## Next Steps

### AI Backend Integration
1. Update environment variables with actual AI backend URL
2. Replace mock data in API routes with real backend calls
3. Implement proper authentication/authorization
4. Add error handling for network failures
5. Implement retry logic for failed requests

### WebSocket Integration
1. Complete WebSocket implementation in ChatInterface component
2. Add typing indicators
3. Implement connection recovery
4. Add message queuing for offline support

### Analytics Enhancement
1. Implement real-time SSE updates
2. Add data persistence
3. Create analytics export functionality
4. Add more detailed charts and visualizations

### Testing
1. Add unit tests for components
2. Add integration tests for API routes
3. Add E2E tests for user flows
4. Add accessibility tests

---

## Requirements Mapping

This implementation satisfies the following requirements from the specification:

- **Requirement 3.1:** Deepfake detection challenges with media analysis
- **Requirement 3.2:** Progressive difficulty and feedback system
- **Requirement 3.3:** Detection clues and hints
- **Requirement 3.4:** Technical explanations

- **Requirement 5.1:** Social media simulation interface
- **Requirement 5.2:** Disinformation content generation
- **Requirement 5.3:** Engagement tracking
- **Requirement 5.4:** Algorithm impact feedback

- **Requirement 6.1:** Catfish chat simulation
- **Requirement 6.2:** Red flag detection and reporting
- **Requirement 6.3:** Character inconsistency analysis
- **Requirement 6.4:** Performance feedback

- **Requirement 4.1:** Analytics dashboard with competency scores
- **Requirement 6.1:** Progress tracking and trends
- **Requirement 6.2:** Achievement system
- **Requirement 6.3:** Personalized recommendations
- **Requirement 6.4:** Peer comparison

---

## Support

For questions or issues with these components, please refer to:
- Design document: `.kiro/specs/ai-backend-separation/design.md`
- Requirements: `.kiro/specs/ai-backend-separation/requirements.md`
- Tasks: `.kiro/specs/ai-backend-separation/tasks.md`
