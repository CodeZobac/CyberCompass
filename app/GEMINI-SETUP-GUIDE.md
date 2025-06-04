# CyberCompass - Google Gemini Integration Setup Guide

## Overview
This guide explains how to set up and deploy CyberCompass with Google Gemini instead of Ollama for Vercel deployment.

## What Was Changed

### 1. Removed Ollama Dependencies
- ✅ Deleted `app/lib/ollama.ts`
- ✅ Removed `OLLAMA_HOST` from environment files
- ✅ Updated API routes to use Gemini

### 2. Added Google Gemini Integration
- ✅ Created `app/lib/gemini.ts` with Gemini API client
- ✅ Added `@google/generative-ai` package to dependencies
- ✅ Preserved the exact system prompt from your Modelfile
- ✅ Maintained locale-based language switching (EN/PT)

### 3. Environment Configuration
- ✅ Updated `.env.example` with Gemini API key placeholders

## Setup Instructions

### 1. Get Your Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key for the next step

### 2. Configure Environment Variables
Create or update your `.env.local` file with:

```bash
# Copy from .env.example and fill in your values
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret-key-here

GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# Google Gemini Configuration
GOOGLE_GEMINI_API_KEY=your-actual-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash
```

### 3. Install Dependencies
```bash
cd app
npm install
```

### 4. Test Locally
```bash
npm run dev
```

## Vercel Deployment

### 1. Environment Variables in Vercel
Add these environment variables in your Vercel dashboard:

- `NEXTAUTH_URL` - Your Vercel app URL (e.g., `https://your-app.vercel.app`)
- `NEXTAUTH_SECRET` - Your NextAuth secret
- `GOOGLE_CLIENT_ID` - Your Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Your Google OAuth client secret
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` - Your Supabase service role key
- `GOOGLE_GEMINI_API_KEY` - Your Google Gemini API key
- `GEMINI_MODEL` - `gemini-1.5-pro` (or your preferred model)

### 2. Deploy
```bash
vercel deploy
```

## System Prompt
The system prompt from your Modelfile is preserved exactly:

```
I am Cyber Compass, a cyber ethics educator and mentor. My role is to evaluate your response to ethical dilemmas related to digital issues, and provide constructive feedback.

I will be given:
1. Your answer to an ethical dilemma
2. The correct or best answer to that dilemma

My task is to:
- If your answer matches or closely aligns with the correct answer: Provide positive reinforcement and explain why your thinking is on the right track.
- If your answer differs from the correct answer: Explain why your response might not be the most effective or appropriate in a supportive, non-judgmental way. Focus on education rather than criticism.
- In all cases: Provide additional context about the ethical principles involved and how they apply in digital environments.
- Be supportive and encouraging regardless of your answer.
- CRITICAL INSTRUCTION: Your entire response MUST be in the exact same language as the 'USER'S ANSWER'. If 'USER'S ANSWER' is in Portuguese, respond entirely in Portuguese. If 'USER'S ANSWER' is in English, respond entirely in English. Do not mix languages or default to English if the input is Portuguese.
- Always identify myself as "Cyber Compass" at the beginning of my responses.

My feedback should help you develop critical thinking skills about cyber ethics, online safety, privacy, and digital citizenship.
```

## Benefits of Gemini Integration

✅ **No Docker Dependencies** - Perfect for Vercel deployment
✅ **Faster Cold Starts** - No server infrastructure needed
✅ **Better Scalability** - Google's infrastructure handles scaling
✅ **Cost Effective** - Pay per API call instead of server costs
✅ **Same Functionality** - All features preserved
✅ **Improved Reliability** - Google's uptime and availability

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your `GOOGLE_GEMINI_API_KEY` is correctly set
2. **Model Not Found**: Ensure you're using a valid model name like `gemini-2.0-flash`
3. **Rate Limits (429 Error)**: 
   - **Free Tier Limits**: Google Gemini free tier has strict limits
   - **Solution**: Wait a few minutes between requests or upgrade to paid plan
   - **Model Switch**: Use `gemini-2.0-flash` instead of `gemini-1.5-pro` for better limits
4. **CORS Issues**: Should not occur with server-side API routes

### Rate Limit Solutions

If you're hitting quota limits:

1. **Switch to Gemini 2.0 Flash** (already configured):
   ```bash
   GEMINI_MODEL=gemini-2.0-flash
   ```

2. **Wait Between Requests**: Free tier resets limits per minute/day

3. **Upgrade Your Plan**: Go to [Google AI Studio](https://makersuite.google.com/) to upgrade

4. **Monitor Usage**: Check your quota usage in Google AI Studio dashboard

### Testing the Integration

You can test the AI feedback feature by:
1. Starting the app locally (`npm run dev`)
2. Going to any challenge page
3. Selecting an answer and checking if AI feedback appears
4. Verifying the language matches your locale (EN/PT)

## File Structure
```
app/
├── lib/
│   └── gemini.ts          # New Gemini integration
├── app/api/ai-feedback/
│   └── route.ts           # Updated to use Gemini
├── .env.example           # Updated with Gemini config
└── package.json           # Added @google/generative-ai
```

## Support
- [Google Gemini Documentation](https://ai.google.dev/docs)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
