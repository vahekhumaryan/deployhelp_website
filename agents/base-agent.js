/**
 * Base Agent Class
 * All specialized agents extend this class
 */

const fs = require('fs').promises;
const path = require('path');

class BaseAgent {
    constructor(name, role, capabilities = []) {
        this.name = name;
        this.role = role;
        this.capabilities = capabilities;
        this.orchestrator = null;
        this.messageQueue = [];
        this.context = {};
    }

    setOrchestrator(orchestrator) {
        this.orchestrator = orchestrator;
    }

    getCapabilities() {
        return this.capabilities;
    }

    /**
     * Check if agent can handle a task type
     * Returns a score from 0-10
     */
    canHandle(taskType) {
        const capabilityMap = {
            'architecture': ['architect', 'planner', 'strategist'],
            'design': ['designer', 'ui', 'ux'],
            'content': ['content', 'writer', 'copywriter'],
            'development': ['developer', 'coder', 'programmer'],
            'seo': ['seo', 'marketing', 'optimization']
        };

        const relevantRoles = capabilityMap[taskType] || [];
        for (const role of relevantRoles) {
            if (this.role.toLowerCase().includes(role) || 
                this.capabilities.some(c => c.toLowerCase().includes(role))) {
                return 10;
            }
        }

        return 0;
    }

    /**
     * Receive a message from the orchestrator
     */
    receiveMessage(message) {
        this.messageQueue.push(message);
    }

    /**
     * Evaluate a task and decide if agent should participate
     */
    async evaluateTask(task) {
        const canHandle = this.canHandle(task.type);
        if (canHandle > 0) {
            await this.speak(`I can help with this task! My expertise: ${this.capabilities.join(', ')}`);
        }
    }

    /**
     * Agent speaks (sends message to orchestrator)
     */
    async speak(message, targetAgents = null) {
        if (this.orchestrator) {
            return this.orchestrator.broadcast(message, this.name, targetAgents);
        }
    }

    /**
     * Execute a subtask
     */
    async execute(subtask) {
        throw new Error('Execute method must be implemented by subclass');
    }

    /**
     * Read a file (tool for agents)
     */
    async readFile(filePath) {
        try {
            const fullPath = path.join(process.cwd(), filePath);
            const content = await fs.readFile(fullPath, 'utf8');
            return content;
        } catch (error) {
            throw new Error(`Failed to read file ${filePath}: ${error.message}`);
        }
    }

    /**
     * Write a file (tool for agents)
     */
    async writeFile(filePath, content) {
        try {
            const fullPath = path.join(process.cwd(), filePath);
            const dir = path.dirname(fullPath);
            await fs.mkdir(dir, { recursive: true });
            await fs.writeFile(fullPath, content, 'utf8');
            return { success: true, path: filePath };
        } catch (error) {
            throw new Error(`Failed to write file ${filePath}: ${error.message}`);
        }
    }

    /**
     * Update a file (tool for agents)
     */
    async updateFile(filePath, updates) {
        try {
            const content = await this.readFile(filePath);
            let updatedContent = content;
            
            if (typeof updates === 'function') {
                updatedContent = updates(content);
            } else if (typeof updates === 'string') {
                updatedContent = updates;
            } else if (typeof updates === 'object') {
                // Handle object-based updates (e.g., replace patterns)
                updatedContent = content;
                for (const [pattern, replacement] of Object.entries(updates)) {
                    updatedContent = updatedContent.replace(new RegExp(pattern, 'g'), replacement);
                }
            }

            await this.writeFile(filePath, updatedContent);
            return { success: true, path: filePath };
        } catch (error) {
            throw new Error(`Failed to update file ${filePath}: ${error.message}`);
        }
    }

    /**
     * List directory contents (tool for agents)
     */
    async listDirectory(dirPath) {
        try {
            const fullPath = path.join(process.cwd(), dirPath);
            const items = await fs.readdir(fullPath, { withFileTypes: true });
            return items.map(item => ({
                name: item.name,
                type: item.isDirectory() ? 'directory' : 'file'
            }));
        } catch (error) {
            throw new Error(`Failed to list directory ${dirPath}: ${error.message}`);
        }
    }
}

module.exports = BaseAgent;
