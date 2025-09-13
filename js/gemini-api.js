/**
 * Google Gemini API Integration Service
 * Handles all AI functionality using the Google Gemini API
 */

class GeminiAPIService {
    constructor() {
        this.apiKey = this.getApiKey();
        this.baseUrl = 'https://generativelanguage.googleapis.com/v1beta/models';
        this.model = 'gemini-1.5-flash-latest'; // Default model
        this.initialized = false;
        this.initializeService();
    }

    /**
     * Get API key from environment variables
     * Supports both client-side and server-side environments
     */
    getApiKey() {
        // For client-side applications, the key would need to be passed from server
        // This is a placeholder - in production, implement proper key management
        if (typeof process !== 'undefined' && process.env) {
            return process.env.GEMINI_API_KEY;
        }
        
        // For client-side, implement secure key retrieval
        return this.getClientSideApiKey();
    }

    /**
     * Secure API key retrieval for client-side
     * In production, this should fetch from your secure backend
     */
    async getClientSideApiKey() {
        try {
            // This would call your backend endpoint that securely provides the API key
            const response = await fetch('/api/get-gemini-key', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.getUserToken()}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                return data.apiKey;
            }
        } catch (error) {
            console.error('Failed to retrieve API key:', error);
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