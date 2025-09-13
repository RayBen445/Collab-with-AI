# 🔐 Complete Guide: Where to Find All Keys and Tokens

This guide provides step-by-step instructions for obtaining all the required API keys and tokens needed to deploy the Collab-with-AI application.

## 📋 Required Credentials Overview

You need to obtain **10 environment variables** from 3 different sources:

- **8 Firebase Configuration Values** (from Firebase Console)
- **1 Google Gemini API Key** (from Google AI Studio)
- **1 Admin Token** (self-generated)
- **1 Admin Email** (your choice)

---

## 🔥 Firebase Configuration (8 variables)

### Step 1: Access Firebase Console
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Sign in with your Google account
3. Click "Create a project" or select existing project

### Step 2: Create/Configure Your Project
1. **Project Name**: Enter "collab-with-ai" (or your preferred name)
2. **Google Analytics**: Enable if desired
3. Click "Create project"

### Step 3: Get Firebase Configuration
1. In your Firebase project dashboard, click the **⚙️ Settings** gear icon
2. Select **"Project settings"**
3. Scroll down to **"Your apps"** section
4. Click **"Add app"** → **Web** (</>) icon
5. **App nickname**: Enter "Collab-with-AI Web"
6. **Register app**

### Step 4: Copy Configuration Values
You'll see a configuration object like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyExample123...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123def456",
  measurementId: "G-XXXXXXXXXX"
};
```

**Map these values to environment variables:**
- `apiKey` → `FIREBASE_API_KEY`
- `authDomain` → `FIREBASE_AUTH_DOMAIN`
- `projectId` → `FIREBASE_PROJECT_ID`
- `storageBucket` → `FIREBASE_STORAGE_BUCKET`
- `messagingSenderId` → `FIREBASE_MESSAGING_SENDER_ID`
- `appId` → `FIREBASE_APP_ID`
- `measurementId` → `FIREBASE_MEASUREMENT_ID`

### Step 5: Enable Required Services
Before deploying, enable these Firebase services:

1. **Authentication**:
   - Go to **Authentication** → **Sign-in method**
   - Enable **Email/Password** and **Google** providers

2. **Firestore Database**:
   - Go to **Firestore Database** → **Create database**
   - Start in **test mode** for now

3. **Storage**:
   - Go to **Storage** → **Get started**
   - Start in **test mode** for now

---

## 🤖 Google Gemini API Key

### Step 1: Access Google AI Studio
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account

### Step 2: Create API Key
1. Click **"Create API Key"**
2. Select your **Firebase project** (or create new one)
3. Copy the generated API key
4. **Save this as**: `GEMINI_API_KEY`

### Important Notes:
- Keep this key secure and never expose it in client-side code
- The application uses it server-side only for security
- You may need to enable billing for extended usage

---

## 🔐 Admin Configuration (2 variables)

### Admin Token (`ADMIN_TOKEN`)
This is a **custom security token** you create yourself:

**Recommended generation methods:**
```bash
# Option 1: Using OpenSSL
openssl rand -base64 32

# Option 2: Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"

# Option 3: Using online generator
# Visit: https://www.random.org/passwords/ (32 chars, special chars)
```

**Example result**: `sk-admin-Xy7Kp2MnQ9Rt5Wz8Av3Bx6Nc1Df4Gh7J`

### Admin Email (`ADMIN_EMAIL`)
- Use **your email address** that will have admin privileges
- This should be the same email you use to sign into the application
- Example: `youremail@gmail.com`

---

## ⚙️ Setting Environment Variables in Vercel

### Step 1: Access Vercel Dashboard
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**

### Step 2: Add All Variables
Click **"Add New"** for each variable:

#### Firebase Variables:
- **Name**: `FIREBASE_API_KEY` **Value**: Your Firebase apiKey
- **Name**: `FIREBASE_AUTH_DOMAIN` **Value**: Your Firebase authDomain
- **Name**: `FIREBASE_PROJECT_ID` **Value**: Your Firebase projectId
- **Name**: `FIREBASE_STORAGE_BUCKET` **Value**: Your Firebase storageBucket
- **Name**: `FIREBASE_MESSAGING_SENDER_ID` **Value**: Your Firebase messagingSenderId
- **Name**: `FIREBASE_APP_ID` **Value**: Your Firebase appId
- **Name**: `FIREBASE_MEASUREMENT_ID` **Value**: Your Firebase measurementId

#### API Keys:
- **Name**: `GEMINI_API_KEY` **Value**: Your Google Gemini API key

**Note**: Set this as a regular environment variable in Vercel, not a secret reference. The application accesses it securely through the backend API endpoint.

#### Admin Configuration:
- **Name**: `ADMIN_TOKEN` **Value**: Your generated secure token
- **Name**: `ADMIN_EMAIL` **Value**: Your admin email address

### Step 3: Environment Selection
For each variable, select:
- ✅ **Production**
- ✅ **Preview** 
- ✅ **Development**

---

## 🏠 Local Development Setup

Create a `.env.local` file in your project root:

```bash
# Firebase Configuration
FIREBASE_API_KEY=AIzaSyExample123...
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123456789:web:abc123def456
FIREBASE_MEASUREMENT_ID=G-XXXXXXXXXX

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Admin Configuration
ADMIN_TOKEN=your_secure_admin_token_here
ADMIN_EMAIL=youremail@gmail.com
```

**⚠️ Important**: The `.env.local` file is automatically ignored by git for security.

---

## ✅ Verification Checklist

Before deploying, ensure you have:

- [ ] Created Firebase project and obtained 7 configuration values
- [ ] Generated Gemini API key from Google AI Studio
- [ ] Created secure admin token (32+ characters)
- [ ] Chosen admin email address
- [ ] Added all 10 environment variables to Vercel
- [ ] Enabled Firebase Authentication, Firestore, and Storage
- [ ] Verified all services are working in Firebase Console

---

## 🆘 Troubleshooting

### Common Issues:

**"Firebase configuration invalid"**
- Double-check all Firebase config values are correctly copied
- Ensure no extra spaces or quotes in environment variables

**"Gemini API key invalid"**
- Verify API key is active in Google AI Studio
- Check if billing is enabled for extended usage
- Ensure GEMINI_API_KEY is set as a regular environment variable (not a secret reference) in Vercel

**"Admin authentication failed"**
- Ensure ADMIN_TOKEN matches exactly (no extra characters)
- Verify ADMIN_EMAIL matches your login email

**"Environment variables not loading"**
- Restart Vercel deployment after adding variables
- Check that variables are enabled for correct environment (Production/Preview)

---

## 🔒 Security Best Practices

1. **Never commit secrets to code**: Always use environment variables
2. **Rotate keys regularly**: Update API keys and tokens periodically
3. **Use strong admin tokens**: Minimum 32 characters with mixed case, numbers, symbols
4. **Monitor usage**: Check Firebase and Gemini API usage dashboards
5. **Restrict API keys**: Configure Firebase security rules and Gemini API restrictions

---

*Need help? Check the Firebase Console and Google AI Studio documentation for additional setup guidance.*