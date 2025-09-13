# Gemini API Integration Guide

This document explains how to set up and use the Google Gemini API integration in the Collab-with-AI platform.

## 🚀 Quick Start

### 1. Environment Setup

#### For Local Development:
```bash
# Create .env.local file in project root
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env.local
```

#### For Vercel Deployment:
1. Go to your Vercel dashboard
2. Navigate to Project Settings → Environment Variables
3. Add a new environment variable:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your Google Gemini API key
   - **Environment**: Production, Preview, Development

### 2. API Key Security

🔒 **Important Security Notes:**
- Never hardcode API keys in your source code
- Use environment variables for all API key storage
- The `.env.local` file is automatically ignored by git
- API keys are accessed securely through the backend endpoint

### 3. Basic Usage

```javascript
// Include the Gemini API service
<script src="js/gemini-api.js"></script>

// Use AI features in your application
async function useAI() {
    try {
        // Generate code
        const codeResult = await geminiAPI.generateCode('javascript', 'Sort an array');
        console.log(codeResult.code);
        
        // Get task suggestions
        const tasks = await geminiAPI.suggestTasks('Building a web app', ['Setup complete']);
        console.log(tasks);
        
        // Process natural language
        const command = await geminiAPI.processNaturalLanguageCommand('Schedule meeting tomorrow');
        console.log(command);
    } catch (error) {
        console.error('AI operation failed:', error);
    }
}
```

## 🛠️ Available AI Features

### Code Generation
```javascript
const result = await geminiAPI.generateCode('python', 'Calculate factorial', 'recursive approach');
// Returns: { code: string, explanation: string }
```

### Code Review
```javascript
const review = await geminiAPI.reviewCode(codeString, 'javascript');
// Returns: { overall: string, suggestions: array, severity: string }
```

### Documentation Generation
```javascript
const docs = await geminiAPI.generateDocumentation({
    name: 'My Project',
    description: 'A web application',
    technologies: ['React', 'Node.js'],
    features: ['Authentication', 'Real-time chat']
});
```

### Meeting Analysis
```javascript
const analysis = await geminiAPI.analyzeMeeting(transcriptText);
// Returns: { summary, keyPoints, actionItems, decisions, followUp, sentiment }
```

### Task Suggestions
```javascript
const suggestions = await geminiAPI.suggestTasks(
    'Building an e-commerce platform',
    ['User authentication completed', 'Product catalog created']
);
```

### Risk Assessment
```javascript
const risks = await geminiAPI.assessRisks({
    name: 'Mobile App',
    timeline: 12,
    teamSize: 5,
    technologies: ['React Native', 'Firebase']
});
```

### Natural Language Commands
```javascript
const command = await geminiAPI.processNaturalLanguageCommand(
    'Create a task to review the homepage design by Friday'
);
// Returns: { action, parameters, confidence, clarifications }
```

## 🔧 Configuration Options

### Generation Parameters
```javascript
const options = {
    temperature: 0.7,     // Creativity (0.0 - 1.0)
    topK: 40,            // Token selection scope
    topP: 0.95,          // Nucleus sampling
    maxTokens: 1024,     // Maximum response length
    stopSequences: []    // Stop generation at these sequences
};

const result = await geminiAPI.generateContent(prompt, options);
```

### Safety Settings
The API includes built-in safety settings to filter harmful content:
- Harassment protection
- Hate speech filtering
- Explicit content blocking
- Dangerous content prevention

## 🔐 Authentication Flow

1. **User Login**: Users authenticate through the login system
2. **Token Generation**: Valid users receive authentication tokens
3. **API Request**: Frontend requests API key through `/api/get-gemini-key`
4. **Token Validation**: Backend validates user token
5. **Key Delivery**: Secure API key delivery to authenticated users

## 📁 File Structure

```
├── js/
│   └── gemini-api.js          # Main API service
├── api/
│   └── get-gemini-key.js      # Backend endpoint for secure key access
├── .env.local                 # Local environment variables (gitignored)
├── .gitignore                 # Includes .env files
├── vercel.json                # Deployment configuration
└── gemini-demo.html           # Live demo and examples
```

## 🚨 Error Handling

```javascript
try {
    const result = await geminiAPI.generateContent(prompt);
    console.log(result.text);
} catch (error) {
    if (error.message.includes('API key')) {
        console.log('Please configure your API key');
    } else if (error.message.includes('rate limit')) {
        console.log('Too many requests, please wait');
    } else {
        console.log('Unexpected error:', error.message);
    }
}
```

## 🔄 API Response Format

### Standard Response
```javascript
{
    text: "Generated content...",
    finishReason: "STOP",
    safetyRatings: [...]
}
```

### Error Response
```javascript
{
    error: {
        message: "Error description",
        code: 400
    }
}
```

## 📊 Usage Examples

### In Collaboration Platform
```javascript
// Real-time document assistance
document.addEventListener('input', async (e) => {
    if (e.target.classList.contains('document-editor')) {
        const suggestion = await geminiAPI.generateContent(
            `Improve this text: ${e.target.value}`
        );
        showSuggestion(suggestion.text);
    }
});

// Smart task creation
async function createSmartTask(description) {
    const taskDetails = await geminiAPI.processNaturalLanguageCommand(
        `Create a task: ${description}`
    );
    
    if (taskDetails.action === 'create_task') {
        return createTask(taskDetails.parameters);
    }
}
```

### In Analytics Dashboard
```javascript
// Generate insights from data
async function generateInsights(projectData) {
    const analysis = await geminiAPI.generateContent(
        `Analyze this project data and provide insights: ${JSON.stringify(projectData)}`
    );
    
    displayInsights(analysis.text);
}
```

## 🎯 Best Practices

1. **Rate Limiting**: Implement client-side rate limiting to avoid API quotas
2. **Caching**: Cache responses for repeated requests
3. **Error Handling**: Always handle API errors gracefully
4. **User Feedback**: Show loading states and progress indicators
5. **Content Validation**: Validate AI-generated content before using
6. **Privacy**: Don't send sensitive data to external APIs

## 🔍 Debugging

### Check API Status
```javascript
console.log('API Initialized:', geminiAPI.isInitialized());
```

### Monitor API Calls
```javascript
// Enable detailed logging
geminiAPI.debug = true;
```

### Test Connection
```javascript
async function testConnection() {
    try {
        const result = await geminiAPI.generateContent('Hello, world!');
        console.log('Connection successful:', result.text);
    } catch (error) {
        console.error('Connection failed:', error);
    }
}
```

## 📈 Performance Tips

1. **Batch Requests**: Combine multiple small requests when possible
2. **Streaming**: Use streaming for long-form content generation
3. **Caching**: Implement intelligent caching for repeated queries
4. **Lazy Loading**: Initialize API only when needed
5. **Compression**: Enable response compression for large responses

## 🆘 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "API key not found" | Set GEMINI_API_KEY environment variable |
| "Unauthorized" | Check authentication token validity |
| "Rate limit exceeded" | Implement request throttling |
| "Network error" | Check internet connection and API endpoint |
| "Invalid response" | Validate request format and parameters |

### Support Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Vercel Environment Variables Guide](https://vercel.com/docs/concepts/projects/environment-variables)
- [Demo Page](gemini-demo.html) - Live examples and testing

---

For more information, visit the [live demo](gemini-demo.html) or contact the development team.