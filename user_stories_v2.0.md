# User Stories V2.0 - CyberCompass

## US-1: Multi-Role Cyberbullying Simulation Agent

As a user learning about cyberbullying, I need an interactive simulation with a multi-role AI agent that alternates between victim, attacker, and mediator roles, so I can practice intervention strategies in realistic scenarios with strategic human-in-the-loop moments.

**Acceptance Criteria:**
- Agent switches seamlessly between 3 distinct roles (victim, attacker, mediator)
- Conversation pauses at critical moments for user intervention input
- User responses are evaluated and educational feedback is provided
- Emotional intensity adapts based on user progress and responses
- Scenario difficulty scales with user competency
- Conversation memory maintained throughout simulation
- Multiple cyberbullying scenarios available (social media, gaming, messaging)
- Real-time sentiment analysis of user interventions

**Tech Stack:** LangGraphJS for agent orchestration, custom state management, structured outputs for role transitions, human-in-the-loop integration, reflection mechanisms for self-improvement, TypeScript/TSX integration

**Context:** Interactive simulations provide safe environments for users to practice ethical decision-making and cyberbullying intervention strategies without real-world consequences.

---

## US-2: Progress and Choice Persistence

Como utilizador, quero que o meu progresso e as minhas escolhas sejam guardadas, so que possa continuar a minha jornada de aprendizagem e ver a minha evolução ao longo do tempo.

**Acceptance Criteria:**
- User authentication and session management
- Progress tracking across all cybersecurity challenges
- Choice history with timestamps and outcomes
- Resume functionality for incomplete simulations
- Cross-device synchronization of user data
- Export functionality for progress reports
- Secure data encryption for sensitive information
- Offline capability with sync when reconnected

**Tech Stack:** Supabase for data persistence, NextAuth for authentication, state management for real-time updates, data encryption for sensitive information, progressive web app capabilities

**Context:** Persistent progress tracking enables personalized learning paths and helps users understand their development over time, increasing engagement and learning effectiveness.

---

## US-3: Ethical Development Summary and Improvement Areas

Como utilizador, quero ver um resumo do meu desenvolvimento ético e áreas para melhoria, para que possa entender o meu progresso e focar nas competências que preciso de desenvolver.

**Acceptance Criteria:**
- Comprehensive dashboard showing ethical development metrics
- Visual progress charts and competency radar
- Identification of strength and improvement areas
- Personalized recommendations for skill development
- Historical trend analysis over time
- Comparison with anonymized peer benchmarks
- Actionable insights and learning path suggestions
- Gamification elements (badges, achievements, levels)

**Tech Stack:** Data analytics with chart libraries (Chart.js/D3.js), machine learning for pattern recognition, recommendation engine, dashboard UI components, data visualization tools

**Context:** Self-reflection and progress awareness are crucial for ethical development. Users need clear feedback on their growth to maintain motivation and identify areas requiring additional focus.

---

## US-4: Interactive Deepfake Detection Challenge

As a user learning about deepfakes, I need an interactive challenge where I analyze audio/video content to determine if it's authentic or artificially generated, so I can develop skills to identify fabricated realities in real-world scenarios.

**Acceptance Criteria:**
- Present users with audio clips (voice deepfakes) and video content for analysis
- Users must identify content as "Real" or "Deepfake" within time constraints
- AI provides detailed feedback highlighting detection clues and techniques
- Progressive difficulty levels from obvious to sophisticated deepfakes
- Educational tooltips explaining deepfake creation methods and red flags
- Real-time confidence scoring based on user's detection accuracy
- Integration with user's own voice/image for personalized deepfake examples
- Post-analysis breakdown of key indicators missed or correctly identified

**Tech Stack:** LangGraphJS for adaptive difficulty flow control, audio/video analysis APIs, machine learning models for deepfake detection, Web Audio API for voice processing, media streaming components

**Context:** Deepfake technology is increasingly sophisticated and prevalent. Users need practical experience identifying fabricated content to protect themselves from misinformation and fraud.

---

## US-5: Viral Disinformation Social Media Simulation

As a user learning about disinformation, I need a simulated social media environment with fake posts and misleading information, so I can practice identifying and avoiding engagement with disinformation to prevent algorithm amplification.

**Acceptance Criteria:**
- Realistic social media interface with fabricated posts containing disinformation
- Dynamic comment threads with varying opinions and fact-checking attempts
- User must identify disinformation and choose appropriate actions (scroll past, report, etc.)
- AI tracks user engagement patterns and provides feedback on algorithm impact
- Multiple disinformation scenarios (health, politics, conspiracy theories, etc.)
- Timer-based challenges to simulate real scrolling behavior
- Educational content about how social media algorithms amplify content
- Scoring based on speed of disinformation detection and appropriate response

**Tech Stack:** LangGraphJS for dynamic content generation and user flow control, simulated social media UI components, sentiment analysis for comment generation, behavioral pattern analysis

**Context:** Social media algorithms amplify engaging content, including disinformation. Users need to understand how their engagement choices affect information spread and learn to identify and avoid disinformation quickly.

---

## US-6: Catfishing Detection Chat Simulation

As a user learning about catfishing, I need an interactive chat simulation where I communicate with a suspicious profile that exhibits red flags, so I can develop skills to identify potential catfishing attempts and protect myself online.

**Acceptance Criteria:**
- Realistic chat interface with AI-generated suspicious profile and conversations
- Profile inconsistencies (young photo vs. outdated language/references)
- Progressive red flag revelation through natural conversation flow
- User can ask probing questions and analyze responses for inconsistencies
- AI provides real-time subtle hints and post-chat detailed analysis
- Multiple catfishing scenarios (romance, friendship, business, etc.)
- Educational prompts about safe online communication practices
- Decision points where users choose how to respond to suspicious behavior

**Tech Stack:** LangGraphJS for conversation flow and character consistency management, natural language processing for age-appropriate speech patterns, image analysis for profile photo inconsistencies, conversation state management

**Context:** Catfishing is a prevalent online threat that can lead to emotional manipulation, financial fraud, and identity theft. Users need practical experience identifying inconsistencies and red flags in online communications.
