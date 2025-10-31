/**
 * Main Application Entry Point
 * DEPLOYHELP LLC Multi-Agent Orchestration System
 */

const AgentOrchestrator = require('./agents/orchestrator');
const ArchitectAgent = require('./agents/architect-agent');
const DesignerAgent = require('./agents/designer-agent');
const DeveloperAgent = require('./agents/developer-agent');
const ContentAgent = require('./agents/content-agent');
const SEOAgent = require('./agents/seo-agent');
const http = require('http');
const fs = require('fs').promises;
const path = require('path');
const url = require('url');

class DeployHelpAgentSystem {
    constructor() {
        this.orchestrator = new AgentOrchestrator();
        this.setupAgents();
        this.server = null;
    }

    setupAgents() {
        // Register all agents
        this.orchestrator.registerAgent(new ArchitectAgent());
        this.orchestrator.registerAgent(new DesignerAgent());
        this.orchestrator.registerAgent(new DeveloperAgent());
        this.orchestrator.registerAgent(new ContentAgent());
        this.orchestrator.registerAgent(new SEOAgent());

        console.log('? All agents registered');
    }

    async startServer(port = 3000) {
        this.server = http.createServer(async (req, res) => {
            const parsedUrl = url.parse(req.url, true);
            const pathname = parsedUrl.pathname;

            // CORS headers
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
            res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

            if (req.method === 'OPTIONS') {
                res.writeHead(200);
                res.end();
                return;
            }

            // API Routes
            if (pathname === '/api/messages' && req.method === 'GET') {
                const messages = this.orchestrator.getMessageHistory();
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ messages }));
                return;
            }

            if (pathname === '/api/status' && req.method === 'GET') {
                const status = this.orchestrator.getStatus();
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status }));
                return;
            }

            if (pathname === '/api/task' && req.method === 'POST') {
                let body = '';
                req.on('data', chunk => { body += chunk.toString(); });
                req.on('end', async () => {
                    try {
                        const task = JSON.parse(body);
                        const results = await this.orchestrator.executeTask(task);
                        res.writeHead(200, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ success: true, results }));
                    } catch (error) {
                        res.writeHead(500, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ success: false, error: error.message }));
                    }
                });
                return;
            }

            if (pathname === '/api/clear' && req.method === 'POST') {
                this.orchestrator.clearHistory();
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true }));
                return;
            }

            // Serve static files
            if (pathname === '/' || pathname === '/index.html') {
                try {
                    const content = await fs.readFile(path.join(__dirname, 'chat.html'), 'utf8');
                    res.writeHead(200, { 'Content-Type': 'text/html' });
                    res.end(content);
                } catch (error) {
                    res.writeHead(404);
                    res.end('File not found');
                }
                return;
            }

            // Default 404
            res.writeHead(404);
            res.end('Not found');
        });

        this.server.listen(port, () => {
            console.log(`\n?? DEPLOYHELP LLC Agent System running on http://localhost:${port}`);
            console.log(`?? Chat interface: http://localhost:${port}`);
            console.log(`\n? Agents ready for collaboration!\n`);
        });
    }

    async executeInitialTask() {
        const task = {
            type: 'website_development',
            description: 'Develop and optimize DEPLOYHELP LLC website and online presence',
            priority: 'high'
        };

        console.log('\n?? Starting initial task...\n');
        const results = await this.orchestrator.executeTask(task, 'system');
        console.log('\n? Task completed!\n');
        return results;
    }

    stop() {
        if (this.server) {
            this.server.close();
        }
    }
}

// Start the system if run directly
if (require.main === module) {
    const system = new DeployHelpAgentSystem();
    
    // Start server
    const port = process.env.PORT || 3000;
    system.startServer(port);

    // Execute initial task after a short delay
    setTimeout(() => {
        system.executeInitialTask().catch(console.error);
    }, 1000);

    // Graceful shutdown
    process.on('SIGINT', () => {
        console.log('\n\n?? Shutting down agent system...');
        system.stop();
        process.exit(0);
    });
}

module.exports = DeployHelpAgentSystem;
