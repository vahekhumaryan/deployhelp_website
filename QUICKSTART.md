# Quick Start Guide

## Starting the Agent System

```bash
# Start the server
node server.js

# Or use a specific port
PORT=8080 node server.js
```

## Accessing the Interface

Once started, open your browser to:
- Chat Interface: `http://localhost:3000` (or the port shown in console)

## Using the System

1. **Start a Task**: Click "Start Task" button to begin agent collaboration
2. **Monitor Agents**: Watch agents communicate and work in the chat interface
3. **Send Custom Tasks**: Type in the input field to send specific tasks
4. **View Status**: See agent status in the sidebar

## Agent Outputs

Agents will create files in:
- `docs/` - Documentation files
- `css/` - CSS enhancements  
- `js/` - JavaScript modules
- `sitemap.xml` - SEO sitemap
- `robots.txt` - SEO robots file

## Troubleshooting

### Port Already in Use
If you get a port conflict error:
```bash
# Kill the process using the port
lsof -ti:3000 | xargs kill

# Or use a different port
PORT=8080 node server.js
```

### Agents Not Responding
- Check browser console for errors
- Verify server is running
- Check network tab for API errors

## Example Task

The system will automatically start with:
```
Task: Develop and optimize DEPLOYHELP LLC website and online presence
```

Agents will:
1. Architect - Plan the structure
2. Designer - Create design system
3. Developer - Implement features
4. Content Strategist - Develop content strategy
5. SEO Specialist - Optimize for search engines
