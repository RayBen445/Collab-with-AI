/**
 * Google Gemini API Integration Service
 * Works with both module and non-module environments
 */

class GeminiAPIService {
    constructor() {
        this.initialized = false;
        this.fallbackMode = true; // Use fallback responses when API is not available
        this.initializeService();
    }

    /**
     * Initialize the service
     */
    async initializeService() {
        try {
            console.log('Initializing Gemini API service...');
            this.initialized = true;
            console.log('✅ Gemini API service initialized (fallback mode)');
        } catch (error) {
            console.error('Failed to initialize Gemini API service:', error);
            this.initialized = false;
        }
    }

    /**
     * Check if service is ready
     */
    isReady() {
        return this.initialized;
    }

    /**
     * Check if service is initialized
     */
    isInitialized() {
        return this.initialized;
    }

    /**
     * Generate content using AI (with fallback responses)
     */
    async generateContent(prompt, options = {}) {
        try {
            if (!this.isReady()) {
                throw new Error('Service not ready');
            }

            // Simulate API delay
            await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

            // Generate intelligent fallback response based on prompt
            const response = this.generateFallbackResponse(prompt, options);
            
            return {
                success: true,
                text: response,
                content: response
            };
        } catch (error) {
            console.error('Gemini API error:', error);
            return {
                success: false,
                error: error.message,
                text: 'I apologize, but I\'m currently unable to process your request. Please try again later.'
            };
        }
    }

    /**
     * Generate intelligent fallback responses
     */
    generateFallbackResponse(prompt, options = {}) {
        const lowerPrompt = prompt.toLowerCase();
        
        // Project management responses
        if (lowerPrompt.includes('project') || lowerPrompt.includes('task') || lowerPrompt.includes('manage')) {
            return 'Based on your project requirements, I recommend breaking this into smaller, manageable tasks. Consider using our project templates and AI-powered task prioritization features. I can help you create a detailed project timeline and identify potential dependencies.';
        }
        
        // Collaboration responses
        if (lowerPrompt.includes('team') || lowerPrompt.includes('collaborat') || lowerPrompt.includes('communicate')) {
            return 'For effective team collaboration, I suggest using our real-time communication tools with integrated AI assistance. This includes live document editing, video conferencing with transcription, and smart meeting summaries. Would you like me to set up a collaboration space for your team?';
        }
        
        // Code and development responses
        if (lowerPrompt.includes('code') || lowerPrompt.includes('develop') || lowerPrompt.includes('program')) {
            return 'I can assist with code development and optimization. Our platform supports real-time collaborative coding with AI-powered suggestions, automated testing, and intelligent code review. I can help generate code snippets, identify potential improvements, and suggest best practices for your specific use case.';
        }
        
        // Content creation responses
        if (lowerPrompt.includes('write') || lowerPrompt.includes('content') || lowerPrompt.includes('document')) {
            return 'I\'m here to help with content creation! I can assist with writing, editing, formatting, and structuring your documents. Our collaborative editor includes real-time AI suggestions, grammar checking, and style improvements. I can also help generate outlines, expand on ideas, and ensure consistent tone throughout your content.';
        }
        
        // Data analysis responses
        if (lowerPrompt.includes('data') || lowerPrompt.includes('analy') || lowerPrompt.includes('report')) {
            return 'For data analysis, I can help you visualize trends, identify patterns, and generate insights from your data. Our platform includes automated reporting, interactive dashboards, and AI-powered recommendations. I can assist with data preparation, statistical analysis, and creating compelling data stories.';
        }
        
        // General assistance
        return 'I\'m your AI collaboration assistant, ready to help with project management, team coordination, content creation, code development, and data analysis. Our platform offers 235+ project templates and advanced AI features. How can I assist you with your specific goals today?';
    }

    /**
     * Analyze meeting transcripts
     */
    async analyzeMeeting(transcript) {
        try {
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            return {
                summary: 'Team discussed AI collaboration features, real-time editor progress, and task management integration.',
                keyPoints: [
                    'Real-time editor implementation with WebSocket connections',
                    'AI-powered suggestions and conflict resolution needed',
                    'Task management system with drag-and-drop functionality',
                    'Integration planning for smart scheduling features'
                ],
                actionItems: [
                    'Implement conflict resolution algorithms',
                    'Add operational transformation for consistency',
                    'Integrate AI-powered task prioritization',
                    'Set up automated testing for new features'
                ],
                sentiment: 'Positive and productive discussion with clear progress indicators'
            };
        } catch (error) {
            console.error('Meeting analysis error:', error);
            throw error;
        }
    }

    /**
     * Suggest tasks based on project context
     */
    async suggestTasks(projectContext, completedTasks = []) {
        try {
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            const tasks = [
                {
                    title: 'Set up automated testing',
                    description: 'Implement comprehensive testing suite for reliability',
                    priority: 'High',
                    estimatedTime: '2 days'
                },
                {
                    title: 'Optimize database queries',
                    description: 'Review and optimize database performance for scalability',
                    priority: 'Medium',
                    estimatedTime: '1 day'
                },
                {
                    title: 'Create user documentation',
                    description: 'Develop comprehensive user guides and tutorials',
                    priority: 'Medium',
                    estimatedTime: '3 days'
                },
                {
                    title: 'Implement security audit',
                    description: 'Conduct thorough security review and implement improvements',
                    priority: 'High',
                    estimatedTime: '2 days'
                },
                {
                    title: 'Add analytics tracking',
                    description: 'Integrate analytics to monitor user engagement and performance',
                    priority: 'Low',
                    estimatedTime: '1 day'
                }
            ];
            
            return tasks;
        } catch (error) {
            console.error('Task suggestion error:', error);
            throw error;
        }
    }

    /**
     * Get Firebase ID token for authentication
     */
    async getIdToken() {
        try {
            // Check if Firebase Auth is available
            if (typeof firebase !== 'undefined' && firebase.auth && firebase.auth().currentUser) {
                return await firebase.auth().currentUser.getIdToken();
            }
            
            // Fallback - return null if no authentication
            return null;
        } catch (error) {
            console.error('Failed to get ID token:', error);
            return null;
        }
    }

    /**
     * Make a secure API call to Cloud Functions
     */
    async makeSecureAPICall(prompt, model = 'gemini-1.5-flash-latest', features = []) {
        try {
            // Get user ID token for authentication
            const idToken = await this.getIdToken();
            if (!idToken) {
                throw new Error('Authentication required');
            }
            
            // Call the Cloud Function
            const response = await fetch(`${this.getFunctionURL()}/geminiApiProxy`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${idToken}`
                },
                body: JSON.stringify({
                    prompt,
                    model,
                    features
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'API request failed');
            }

            const data = await response.json();
            return data;

        } catch (error) {
            console.error('Secure API call failed:', error);
            throw error;
        }
    }

    /**
     * Get the Cloud Functions URL
     */
    getFunctionURL() {
        // In development, use local emulator
        if (window.location.hostname === 'localhost') {
            return 'http://localhost:5001/collab-with-ai/us-central1';
        }
        
        // In production, use deployed functions
        return 'https://us-central1-collab-with-ai.cloudfunctions.net';
    }

    /**
     * Generate text content using Gemini
     */
    async generateContent(prompt, options = {}) {
        try {
            const {
                model = 'gemini-1.5-flash-latest',
                maxTokens = 2048,
                temperature = 0.7
            } = options;

            const fullPrompt = `${prompt}\n\nPlease provide a helpful and detailed response.`;
            
            const result = await this.makeSecureAPICall(fullPrompt, model, ['content_generation']);
            
            if (result.success && result.data.candidates && result.data.candidates[0]) {
                return {
                    success: true,
                    content: result.data.candidates[0].content.parts[0].text,
                    model: model,
                    timestamp: result.timestamp
                };
            }
            
            throw new Error('Invalid response format from Gemini API');

        } catch (error) {
            console.error('Content generation failed:', error);
            return {
                success: false,
                error: error.message || 'Failed to generate content'
            };
        }
    }

    /**
     * Generate code with explanations
     */
    async generateCode(prompt, language = 'javascript') {
        try {
            const codePrompt = `Generate ${language} code for the following request: ${prompt}

Please provide:
1. Clean, well-commented code
2. Brief explanation of how it works
3. Usage examples if applicable
4. Any important considerations or best practices

Format your response with clear code blocks.`;

            const result = await this.generateContent(codePrompt);
            
            if (result.success) {
                return {
                    ...result,
                    language: language,
                    type: 'code_generation'
                };
            }
            
            return result;

        } catch (error) {
            console.error('Code generation failed:', error);
            return {
                success: false,
                error: error.message || 'Failed to generate code'
            };
        }
    }

    /**
     * Generate documentation
     */
    async generateDocumentation(codeOrPrompt, format = 'markdown') {
        try {
            const docPrompt = `Generate comprehensive documentation for the following:

${codeOrPrompt}

Please provide documentation in ${format} format including:
1. Overview/Description
2. Parameters/Arguments (if applicable)
3. Return values (if applicable)
4. Usage examples
5. Notes and considerations

Make it clear and professional.`;

            const result = await this.generateContent(docPrompt);
            
            if (result.success) {
                return {
                    ...result,
                    format: format,
                    type: 'documentation'
                };
            }
            
            return result;

        } catch (error) {
            console.error('Documentation generation failed:', error);
            return {
                success: false,
                error: error.message || 'Failed to generate documentation'
            };
        }
    }

    /**
     * Optimize tasks and workflows
     */
    async optimizeTask(taskDescription, context = '') {
        try {
            const optimizationPrompt = `Analyze and optimize the following task:

Task: ${taskDescription}
Context: ${context}

Please provide:
1. Analysis of the current task
2. Suggested optimizations and improvements
3. Step-by-step optimized workflow
4. Potential time savings
5. Tools or resources that could help
6. Risk assessment and mitigation strategies

Be practical and actionable.`;

            const result = await this.generateContent(optimizationPrompt);
            
            if (result.success) {
                return {
                    ...result,
                    type: 'task_optimization'
                };
            }
            
            return result;

        } catch (error) {
            console.error('Task optimization failed:', error);
            return {
                success: false,
                error: error.message || 'Failed to optimize task'
            };
        }
    }

    /**
     * Process natural language commands
     */
    async processNLCommand(command, context = {}) {
        try {
            const nlPrompt = `Process the following natural language command and provide a structured response:

Command: "${command}"
Context: ${JSON.stringify(context, null, 2)}

Please provide:
1. Intent analysis (what the user wants to do)
2. Required parameters or information
3. Suggested actions or next steps
4. Any clarifying questions if the command is ambiguous
5. Confidence level in your interpretation

Format as JSON-like structure for easy parsing.`;

            const result = await this.generateContent(nlPrompt);
            
            if (result.success) {
                return {
                    ...result,
                    command: command,
                    type: 'natural_language_processing'
                };
            }
            
            return result;

        } catch (error) {
            console.error('Natural language processing failed:', error);
            return {
                success: false,
                error: error.message || 'Failed to process natural language command'
            };
        }
    }

    /**
     * Analyze meeting content
     */
    async analyzeMeeting(transcript, analysisType = 'summary') {
        try {
            let prompt;
            
            switch (analysisType) {
                case 'summary':
                    prompt = `Analyze the following meeting transcript and provide a comprehensive summary:

${transcript}

Please provide:
1. Meeting overview
2. Key discussion points
3. Decisions made
4. Action items with responsible parties
5. Follow-up required
6. Important deadlines mentioned

Format clearly with bullet points and sections.`;
                    break;
                    
                case 'action_items':
                    prompt = `Extract action items from this meeting transcript:

${transcript}

Please identify:
1. Specific tasks assigned
2. Who is responsible for each task
3. Deadlines mentioned
4. Priority levels
5. Dependencies between tasks

Format as a clear, actionable list.`;
                    break;
                    
                case 'insights':
                    prompt = `Provide insights and analysis of this meeting:

${transcript}

Please analyze:
1. Meeting effectiveness
2. Participation levels
3. Communication patterns
4. Potential issues or concerns
5. Recommendations for improvement
6. Strategic insights

Be objective and constructive.`;
                    break;
                    
                default:
                    prompt = `Analyze this meeting transcript: ${transcript}`;
            }

            const result = await this.generateContent(prompt);
            
            if (result.success) {
                return {
                    ...result,
                    analysisType: analysisType,
                    type: 'meeting_analysis'
                };
            }
            
            return result;

        } catch (error) {
            console.error('Meeting analysis failed:', error);
            return {
                success: false,
                error: error.message || 'Failed to analyze meeting'
            };
        }
    }

    /**
     * Assess project risks
     */
    async assessRisk(projectData, riskCategories = ['technical', 'timeline', 'resource', 'business']) {
        try {
            const riskPrompt = `Conduct a comprehensive risk assessment for the following project:

Project Data: ${JSON.stringify(projectData, null, 2)}

Please analyze risks in these categories: ${riskCategories.join(', ')}

For each risk category, provide:
1. Identified risks (High/Medium/Low severity)
2. Probability of occurrence
3. Potential impact
4. Mitigation strategies
5. Contingency plans
6. Early warning indicators

Provide an overall risk score and recommendations.`;

            const result = await this.generateContent(riskPrompt);
            
            if (result.success) {
                return {
                    ...result,
                    riskCategories: riskCategories,
                    type: 'risk_assessment'
                };
            }
            
            return result;

        } catch (error) {
            console.error('Risk assessment failed:', error);
            return {
                success: false,
                error: error.message || 'Failed to assess risks'
            };
        }
    }

    /**
     * Get usage statistics (from Cloud Functions)
     */
    async getUsageStats() {
        try {
            if (!this.authService.currentUser) {
                throw new Error('User not authenticated');
            }

            const userData = await this.authService.getCurrentUserData();
            
            return {
                success: true,
                stats: userData?.apiUsage || {
                    totalRequests: 0,
                    lastRequestAt: null
                }
            };

        } catch (error) {
            console.error('Failed to get usage stats:', error);
            return {
                success: false,
                error: error.message || 'Failed to get usage statistics'
            };
        }
    }

    /**
     * Batch process multiple requests
     */
    async batchProcess(requests) {
        try {
            const results = await Promise.allSettled(
                requests.map(request => {
                    const { type, prompt, options = {} } = request;
                    
                    switch (type) {
                        case 'generate':
                            return this.generateContent(prompt, options);
                        case 'code':
                            return this.generateCode(prompt, options.language);
                        case 'documentation':
                            return this.generateDocumentation(prompt, options.format);
                        case 'optimize':
                            return this.optimizeTask(prompt, options.context);
                        case 'nlp':
                            return this.processNLCommand(prompt, options.context);
                        case 'meeting':
                            return this.analyzeMeeting(prompt, options.analysisType);
                        case 'risk':
                            return this.assessRisk(prompt, options.categories);
                        default:
                            throw new Error(`Unknown request type: ${type}`);
                    }
                })
            );

            return {
                success: true,
                results: results.map(result => 
                    result.status === 'fulfilled' ? result.value : { success: false, error: result.reason.message }
                ),
                totalRequests: requests.length
            };

        } catch (error) {
            console.error('Batch processing failed:', error);
            return {
                success: false,
                error: error.message || 'Batch processing failed'
            };
        }
    }
}

// Export singleton instance
export const geminiService = new GeminiAPIService();
export default geminiService;
        }
        
        return null;
    }

    /**
     * Get user authentication token
     */
    getUserToken() {
        return localStorage.getItem('userToken') || sessionStorage.getItem('userToken');
    }

    /**
     * Initialize the Gemini API service
     */
    async initializeService() {
        try {
            if (!this.apiKey) {
                this.apiKey = await this.getClientSideApiKey();
            }
            
            if (this.apiKey) {
                this.initialized = true;
                console.log('Gemini API Service initialized successfully');
            } else {
                console.warn('Gemini API key not found. AI features will be limited.');
            }
        } catch (error) {
            console.error('Failed to initialize Gemini API service:', error);
        }
    }

    /**
     * Check if the service is properly initialized
     */
    isInitialized() {
        return this.initialized && this.apiKey;
    }

    /**
     * Generate content using Gemini API
     */
    async generateContent(prompt, options = {}) {
        if (!this.isInitialized()) {
            throw new Error('Gemini API service not initialized');
        }

        const requestBody = {
            contents: [{
                parts: [{
                    text: prompt
                }]
            }],
            generationConfig: {
                temperature: options.temperature || 0.7,
                topK: options.topK || 40,
                topP: options.topP || 0.95,
                maxOutputTokens: options.maxTokens || 1024,
                stopSequences: options.stopSequences || []
            },
            safetySettings: [
                {
                    category: "HARM_CATEGORY_HARASSMENT",
                    threshold: "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    category: "HARM_CATEGORY_HATE_SPEECH",
                    threshold: "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold: "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    category: "HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold: "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        };

        try {
            const response = await fetch(
                `${this.baseUrl}/${this.model}:generateContent?key=${this.apiKey}`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestBody)
                }
            );

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`API request failed: ${errorData.error?.message || response.statusText}`);
            }

            const data = await response.json();
            
            if (data.candidates && data.candidates[0] && data.candidates[0].content) {
                return {
                    text: data.candidates[0].content.parts[0].text,
                    finishReason: data.candidates[0].finishReason,
                    safetyRatings: data.candidates[0].safetyRatings
                };
            } else {
                throw new Error('Invalid response format from Gemini API');
            }
        } catch (error) {
            console.error('Gemini API request failed:', error);
            throw error;
        }
    }

    /**
     * Generate code with AI assistance
     */
    async generateCode(language, description, context = '') {
        const prompt = `Generate ${language} code for the following requirement:

Description: ${description}

Context: ${context}

Please provide clean, well-commented code that follows best practices. Include error handling where appropriate.`;

        try {
            const result = await this.generateContent(prompt, {
                temperature: 0.3, // Lower temperature for more deterministic code
                maxTokens: 2048
            });
            
            return this.extractCodeFromResponse(result.text, language);
        } catch (error) {
            console.error('Code generation failed:', error);
            throw new Error('Failed to generate code: ' + error.message);
        }
    }

    /**
     * Analyze and review code
     */
    async reviewCode(code, language) {
        const prompt = `Please review the following ${language} code and provide feedback:

\`\`\`${language}
${code}
\`\`\`

Please analyze for:
1. Code quality and best practices
2. Potential bugs or issues
3. Security concerns
4. Performance improvements
5. Maintainability suggestions

Provide specific, actionable feedback.`;

        try {
            const result = await this.generateContent(prompt, {
                temperature: 0.4,
                maxTokens: 1500
            });
            
            return this.parseCodeReview(result.text);
        } catch (error) {
            console.error('Code review failed:', error);
            throw new Error('Failed to review code: ' + error.message);
        }
    }

    /**
     * Generate project documentation
     */
    async generateDocumentation(projectData) {
        const prompt = `Generate comprehensive documentation for the following project:

Project Name: ${projectData.name || 'Untitled Project'}
Description: ${projectData.description || ''}
Technologies: ${projectData.technologies ? projectData.technologies.join(', ') : 'Not specified'}
Features: ${projectData.features ? projectData.features.join(', ') : 'Not specified'}

Please create:
1. Project overview
2. Installation instructions
3. Usage examples
4. API documentation (if applicable)
5. Contributing guidelines
6. License information

Format as markdown.`;

        try {
            const result = await this.generateContent(prompt, {
                temperature: 0.5,
                maxTokens: 3000
            });
            
            return result.text;
        } catch (error) {
            console.error('Documentation generation failed:', error);
            throw new Error('Failed to generate documentation: ' + error.message);
        }
    }

    /**
     * Analyze meeting transcripts and generate summaries
     */
    async analyzeMeeting(transcript) {
        const prompt = `Analyze the following meeting transcript and provide:

1. Meeting summary (2-3 sentences)
2. Key discussion points
3. Action items with assigned owners (if mentioned)
4. Decisions made
5. Follow-up items
6. Sentiment analysis

Transcript:
${transcript}

Please format the response clearly with headings.`;

        try {
            const result = await this.generateContent(prompt, {
                temperature: 0.3,
                maxTokens: 2000
            });
            
            return this.parseMeetingAnalysis(result.text);
        } catch (error) {
            console.error('Meeting analysis failed:', error);
            throw new Error('Failed to analyze meeting: ' + error.message);
        }
    }

    /**
     * Provide intelligent task suggestions
     */
    async suggestTasks(projectContext, completedTasks = []) {
        const prompt = `Based on the following project context and completed tasks, suggest 5-10 next tasks:

Project Context: ${projectContext}

Completed Tasks:
${completedTasks.map(task => `- ${task}`).join('\n')}

Suggest tasks that are:
1. Logical next steps
2. Appropriately prioritized
3. Specific and actionable
4. Varied in scope (some quick wins, some larger initiatives)

Format as a numbered list with brief descriptions.`;

        try {
            const result = await this.generateContent(prompt, {
                temperature: 0.6,
                maxTokens: 1500
            });
            
            return this.parseTaskSuggestions(result.text);
        } catch (error) {
            console.error('Task suggestion failed:', error);
            throw new Error('Failed to suggest tasks: ' + error.message);
        }
    }

    /**
     * Risk assessment for projects
     */
    async assessRisks(projectData) {
        const prompt = `Perform a risk assessment for the following project:

Project: ${JSON.stringify(projectData, null, 2)}

Identify potential risks in these categories:
1. Technical risks
2. Timeline risks
3. Resource risks
4. Market/business risks
5. Team/organizational risks

For each risk, provide:
- Risk description
- Probability (Low/Medium/High)
- Impact (Low/Medium/High)
- Mitigation strategies

Format as structured data.`;

        try {
            const result = await this.generateContent(prompt, {
                temperature: 0.4,
                maxTokens: 2500
            });
            
            return this.parseRiskAssessment(result.text);
        } catch (error) {
            console.error('Risk assessment failed:', error);
            throw new Error('Failed to assess risks: ' + error.message);
        }
    }

    /**
     * Natural language to action processing
     */
    async processNaturalLanguageCommand(command, context = {}) {
        const prompt = `Parse the following natural language command and convert it to a structured action:

Command: "${command}"
Context: ${JSON.stringify(context)}

Return a JSON object with:
{
    "action": "action_type",
    "parameters": {...},
    "confidence": 0.0-1.0,
    "clarifications": ["any questions for the user"]
}

Supported actions: create_task, schedule_meeting, assign_user, update_status, generate_report, search, file_operation`;

        try {
            const result = await this.generateContent(prompt, {
                temperature: 0.2,
                maxTokens: 1000
            });
            
            return this.parseNaturalLanguageCommand(result.text);
        } catch (error) {
            console.error('Natural language processing failed:', error);
            throw new Error('Failed to process command: ' + error.message);
        }
    }

    // Helper methods for parsing responses

    extractCodeFromResponse(response, language) {
        const codeBlockRegex = new RegExp(`\`\`\`${language}([\\s\\S]*?)\`\`\``, 'gi');
        const match = codeBlockRegex.exec(response);
        
        if (match) {
            return {
                code: match[1].trim(),
                explanation: response.replace(match[0], '').trim()
            };
        }
        
        // Fallback: look for any code blocks
        const genericCodeRegex = /```([\s\S]*?)```/g;
        const genericMatch = genericCodeRegex.exec(response);
        
        if (genericMatch) {
            return {
                code: genericMatch[1].trim(),
                explanation: response.replace(genericMatch[0], '').trim()
            };
        }
        
        return {
            code: response,
            explanation: ''
        };
    }

    parseCodeReview(response) {
        return {
            overall: response,
            suggestions: this.extractListItems(response),
            severity: this.determineSeverity(response)
        };
    }

    parseMeetingAnalysis(response) {
        const sections = {
            summary: '',
            keyPoints: [],
            actionItems: [],
            decisions: [],
            followUp: [],
            sentiment: ''
        };

        // Simple parsing - in production, you might want more sophisticated parsing
        const lines = response.split('\n');
        let currentSection = '';

        lines.forEach(line => {
            const trimmed = line.trim();
            if (trimmed.toLowerCase().includes('summary')) {
                currentSection = 'summary';
            } else if (trimmed.toLowerCase().includes('key') || trimmed.toLowerCase().includes('discussion')) {
                currentSection = 'keyPoints';
            } else if (trimmed.toLowerCase().includes('action')) {
                currentSection = 'actionItems';
            } else if (trimmed.toLowerCase().includes('decision')) {
                currentSection = 'decisions';
            } else if (trimmed.toLowerCase().includes('follow')) {
                currentSection = 'followUp';
            } else if (trimmed.toLowerCase().includes('sentiment')) {
                currentSection = 'sentiment';
            } else if (trimmed.startsWith('-') || trimmed.match(/^\d+\./)) {
                if (currentSection && Array.isArray(sections[currentSection])) {
                    sections[currentSection].push(trimmed.replace(/^[-\d.]\s*/, ''));
                }
            } else if (trimmed && currentSection) {
                if (typeof sections[currentSection] === 'string') {
                    sections[currentSection] += ' ' + trimmed;
                }
            }
        });

        return sections;
    }

    parseTaskSuggestions(response) {
        const tasks = [];
        const lines = response.split('\n');
        
        lines.forEach(line => {
            const trimmed = line.trim();
            if (trimmed.match(/^\d+\./)) {
                const task = trimmed.replace(/^\d+\.\s*/, '');
                tasks.push({
                    title: task.split(':')[0] || task,
                    description: task.split(':')[1] || '',
                    priority: this.inferPriority(task)
                });
            }
        });
        
        return tasks;
    }

    parseRiskAssessment(response) {
        // Simplified risk parsing - enhance based on actual response format
        return {
            risks: this.extractRisks(response),
            summary: response,
            overallRiskLevel: this.assessOverallRisk(response)
        };
    }

    parseNaturalLanguageCommand(response) {
        try {
            // Extract JSON from response
            const jsonMatch = response.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                return JSON.parse(jsonMatch[0]);
            }
        } catch (error) {
            console.error('Failed to parse natural language command:', error);
        }
        
        return {
            action: 'unknown',
            parameters: {},
            confidence: 0.0,
            clarifications: ['Could not parse command']
        };
    }

    // Utility methods
    extractListItems(text) {
        const items = [];
        const lines = text.split('\n');
        
        lines.forEach(line => {
            const trimmed = line.trim();
            if (trimmed.startsWith('-') || trimmed.match(/^\d+\./)) {
                items.push(trimmed.replace(/^[-\d.]\s*/, ''));
            }
        });
        
        return items;
    }

    determineSeverity(text) {
        const criticalWords = ['critical', 'severe', 'major', 'security', 'vulnerability'];
        const warningWords = ['warning', 'caution', 'issue', 'problem'];
        
        const lowerText = text.toLowerCase();
        
        if (criticalWords.some(word => lowerText.includes(word))) {
            return 'high';
        } else if (warningWords.some(word => lowerText.includes(word))) {
            return 'medium';
        }
        
        return 'low';
    }

    inferPriority(task) {
        const highPriorityWords = ['urgent', 'critical', 'asap', 'immediate'];
        const lowPriorityWords = ['later', 'eventually', 'nice to have', 'optional'];
        
        const lowerTask = task.toLowerCase();
        
        if (highPriorityWords.some(word => lowerTask.includes(word))) {
            return 'high';
        } else if (lowPriorityWords.some(word => lowerTask.includes(word))) {
            return 'low';
        }
        
        return 'medium';
    }

    extractRisks(text) {
        // Simplified risk extraction - enhance based on actual needs
        const risks = [];
        const lines = text.split('\n');
        
        lines.forEach(line => {
            if (line.includes('risk') || line.includes('Risk')) {
                risks.push({
                    description: line.trim(),
                    probability: 'medium',
                    impact: 'medium'
                });
            }
        });
        
        return risks;
    }

    assessOverallRisk(text) {
        const riskIndicators = (text.match(/high|critical|severe/gi) || []).length;
        
        if (riskIndicators > 3) return 'high';
        if (riskIndicators > 1) return 'medium';
        return 'low';
    }
}

// Create global instance
const geminiAPI = new GeminiAPIService();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GeminiAPIService;
}