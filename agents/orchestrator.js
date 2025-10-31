/**
 * Multi-Agent Orchestrator for DEPLOYHELP LLC
 * Coordinates multiple specialized agents working on website development
 */

class AgentOrchestrator {
    constructor() {
        this.agents = new Map();
        this.messageHistory = [];
        this.currentTask = null;
        this.agentStates = new Map();
        this.isRunning = false;
    }

    /**
     * Register an agent with the orchestrator
     */
    registerAgent(agent) {
        this.agents.set(agent.name, agent);
        this.agentStates.set(agent.name, {
            status: 'idle',
            lastMessage: null,
            tasksCompleted: 0,
            errors: []
        });
        agent.setOrchestrator(this);
    }

    /**
     * Broadcast a message to all agents or specific agents
     */
    broadcast(message, sender, targetAgents = null) {
        const messageObj = {
            id: Date.now() + Math.random(),
            timestamp: new Date(),
            sender: sender,
            message: message,
            type: 'message'
        };

        this.messageHistory.push(messageObj);

        const recipients = targetAgents || Array.from(this.agents.keys());
        recipients.forEach(agentName => {
            if (agentName !== sender && this.agents.has(agentName)) {
                const agent = this.agents.get(agentName);
                agent.receiveMessage(messageObj);
            }
        });

        return messageObj;
    }

    /**
     * Execute a task by delegating to appropriate agents
     */
    async executeTask(task, initiator = 'system') {
        this.currentTask = task;
        this.isRunning = true;

        const taskMessage = {
            id: Date.now() + Math.random(),
            timestamp: new Date(),
            sender: initiator,
            message: `TASK ASSIGNED: ${task.description}`,
            type: 'task',
            task: task
        };

        this.messageHistory.push(taskMessage);

        // Notify all agents about the new task
        for (const [name, agent] of this.agents) {
            this.agentStates.get(name).status = 'evaluating';
            await agent.evaluateTask(task);
        }

        // Let agents collaborate to complete the task
        const results = await this.coordinateTask(task);
        
        this.isRunning = false;
        return results;
    }

    /**
     * Coordinate agents to complete a task
     */
    async coordinateTask(task) {
        const results = [];
        const taskQueue = this.prioritizeTask(task);

        for (const subtask of taskQueue) {
            const agent = this.selectBestAgent(subtask);
            if (agent) {
                this.agentStates.get(agent.name).status = 'working';
                
                try {
                    const result = await agent.execute(subtask);
                    results.push({
                        agent: agent.name,
                        subtask: subtask,
                        result: result,
                        success: true
                    });
                    
                    this.agentStates.get(agent.name).tasksCompleted++;
                    this.agentStates.get(agent.name).status = 'idle';
                    
                    // Notify other agents about the result
                    this.broadcast(
                        `${agent.name} completed: ${subtask.type}`,
                        agent.name
                    );
                } catch (error) {
                    results.push({
                        agent: agent.name,
                        subtask: subtask,
                        result: error.message,
                        success: false
                    });
                    
                    this.agentStates.get(agent.name).errors.push(error);
                    this.agentStates.get(agent.name).status = 'idle';
                }
            }
        }

        return results;
    }

    /**
     * Break down task into subtasks
     */
    prioritizeTask(task) {
        const subtasks = [];
        
        // Architecture/Planning tasks first
        if (task.type === 'website_development' || task.type === 'architecture') {
            subtasks.push({
                type: 'architecture',
                description: 'Design website architecture and structure',
                priority: 1
            });
        }

        // Design tasks
        if (task.type === 'website_development' || task.type === 'design') {
            subtasks.push({
                type: 'design',
                description: 'Create visual design and UI/UX',
                priority: 2
            });
        }

        // Content tasks
        if (task.type === 'website_development' || task.type === 'content') {
            subtasks.push({
                type: 'content',
                description: 'Develop content strategy and copy',
                priority: 2
            });
        }

        // Development tasks
        if (task.type === 'website_development' || task.type === 'development') {
            subtasks.push({
                type: 'development',
                description: 'Implement website features',
                priority: 3
            });
        }

        // SEO tasks
        if (task.type === 'website_development' || task.type === 'seo') {
            subtasks.push({
                type: 'seo',
                description: 'Optimize for search engines',
                priority: 4
            });
        }

        return subtasks.sort((a, b) => a.priority - b.priority);
    }

    /**
     * Select the best agent for a subtask
     */
    selectBestAgent(subtask) {
        let bestAgent = null;
        let bestScore = 0;

        for (const [name, agent] of this.agents) {
            const score = agent.canHandle(subtask.type);
            if (score > bestScore) {
                bestScore = score;
                bestAgent = agent;
            }
        }

        return bestAgent;
    }

    /**
     * Get current status of all agents
     */
    getStatus() {
        const status = {};
        for (const [name, state] of this.agentStates) {
            status[name] = {
                ...state,
                capabilities: this.agents.get(name).getCapabilities()
            };
        }
        return status;
    }

    /**
     * Get message history
     */
    getMessageHistory() {
        return this.messageHistory;
    }

    /**
     * Clear message history
     */
    clearHistory() {
        this.messageHistory = [];
    }
}

module.exports = AgentOrchestrator;
