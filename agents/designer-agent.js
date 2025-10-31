/**
 * Designer Agent
 * Specializes in UI/UX design, visual aesthetics, and user experience
 */

const BaseAgent = require('./base-agent');

class DesignerAgent extends BaseAgent {
    constructor() {
        super(
            'Designer',
            'UI/UX Designer',
            ['design', 'ui', 'ux', 'visual-design', 'user-experience', 'aesthetics']
        );
    }

    async execute(subtask) {
        await this.speak(`Creating design specifications for: ${subtask.description}`);

        try {
            // Analyze current design
            const currentDesign = await this.analyzeCurrentDesign();
            
            // Create design system
            const designSystem = this.createDesignSystem();
            
            // Propose improvements
            const improvements = this.proposeDesignImprovements(currentDesign);
            
            // Create design document
            const designDoc = this.createDesignDocument(designSystem, improvements);
            await this.writeFile('docs/design-system.md', designDoc);

            // Create CSS improvements
            const cssImprovements = this.createCSSImprovements();
            await this.writeFile('css/design-enhancements.css', cssImprovements);

            await this.speak('Design system completed! I\'ve created a comprehensive design guide and CSS enhancements.');

            return {
                success: true,
                designSystem: designSystem,
                improvements: improvements,
                documents: ['docs/design-system.md', 'css/design-enhancements.css']
            };
        } catch (error) {
            await this.speak(`Design process encountered an issue: ${error.message}`);
            throw error;
        }
    }

    async analyzeCurrentDesign() {
        try {
            const html = await this.readFile('index.html');
            
            // Extract current color scheme
            const colorMatches = html.match(/--[\w-]+:\s*[#\w\d(),\s.]+/g) || [];
            const colors = {};
            colorMatches.forEach(match => {
                const [key, value] = match.split(':').map(s => s.trim());
                colors[key] = value;
            });

            return {
                theme: 'cyberpunk/neon',
                colors: colors,
                typography: 'Orbitron, Share Tech Mono',
                layout: 'grid-based',
                components: ['navbar', 'hero', 'services-grid', 'contact-card']
            };
        } catch (error) {
            return {
                theme: 'unknown',
                colors: {},
                typography: 'unknown',
                layout: 'unknown',
                components: []
            };
        }
    }

    createDesignSystem() {
        return {
            colors: {
                primary: '#ff00ff',
                secondary: '#00ffff',
                accent: '#ffff00',
                neon: {
                    pink: '#ff1493',
                    blue: '#00bfff',
                    green: '#39ff14'
                },
                background: {
                    dark: '#0a0a0a',
                    darker: '#000000',
                    card: 'rgba(20, 20, 20, 0.9)'
                }
            },
            typography: {
                headings: {
                    font: 'Orbitron',
                    weights: [400, 700, 900]
                },
                body: {
                    font: 'Share Tech Mono',
                    size: '1rem'
                }
            },
            spacing: {
                unit: '1rem',
                scale: [0.25, 0.5, 1, 1.5, 2, 3, 4]
            },
            effects: {
                glow: 'text-shadow: 0 0 10px currentColor',
                neon: 'box-shadow: 0 0 20px currentColor',
                scanlines: 'repeating-linear-gradient(...)'
            },
            components: {
                card: {
                    border: '2px solid',
                    padding: '1rem',
                    background: 'var(--card-background)'
                },
                button: {
                    border: '2px solid',
                    padding: '0.5rem 1.5rem',
                    transition: 'all 0.3s ease'
                }
            }
        };
    }

    proposeDesignImprovements(currentDesign) {
        return [
            'Enhance contrast for better accessibility',
            'Add micro-interactions for better UX',
            'Implement consistent spacing system',
            'Add loading states and animations',
            'Improve mobile responsiveness',
            'Add dark mode toggle',
            'Enhance focus states for keyboard navigation',
            'Add visual feedback for interactive elements'
        ];
    }

    createDesignDocument(designSystem, improvements) {
        return `# DEPLOYHELP LLC Design System

## Overview
Comprehensive design system for maintaining visual consistency across the website.

## Color Palette

### Primary Colors
- Primary: ${designSystem.colors.primary}
- Secondary: ${designSystem.colors.secondary}
- Accent: ${designSystem.colors.accent}

### Neon Colors
- Pink: ${designSystem.colors.neon.pink}
- Blue: ${designSystem.colors.neon.blue}
- Green: ${designSystem.colors.neon.green}

### Backgrounds
- Dark: ${designSystem.colors.background.dark}
- Darker: ${designSystem.colors.background.darker}
- Card: ${designSystem.colors.background.card}

## Typography

### Headings
- Font: ${designSystem.typography.headings.font}
- Weights: ${designSystem.typography.headings.weights.join(', ')}

### Body
- Font: ${designSystem.typography.body.font}
- Size: ${designSystem.typography.body.size}

## Spacing System
Base unit: ${designSystem.spacing.unit}
Scale: ${designSystem.spacing.scale.join(', ')}

## Design Effects
- Glow: ${designSystem.effects.glow}
- Neon: ${designSystem.effects.neon}

## Proposed Improvements
${improvements.map(i => `- ${i}`).join('\n')}

## Component Specifications
See individual component documentation for detailed specs.

Generated by Designer Agent
`;
    }

    createCSSImprovements() {
        return `/* Design Enhancements for DEPLOYHELP LLC */
/* Generated by Designer Agent */

/* Enhanced Accessibility */
:focus-visible {
    outline: 2px solid var(--secondary-color);
    outline-offset: 2px;
    box-shadow: 0 0 15px var(--secondary-color);
}

/* Improved Loading States */
.loading {
    position: relative;
    overflow: hidden;
}

.loading::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.1),
        transparent
    );
    animation: loading-shimmer 1.5s infinite;
}

@keyframes loading-shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* Micro-interactions */
button, .service-card, .contact-card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

button:active {
    transform: scale(0.98);
}

/* Enhanced Mobile Experience */
@media (max-width: 768px) {
    .service-card {
        margin-bottom: 1rem;
    }
    
    .hero h1 {
        font-size: clamp(1.5rem, 5vw, 2.5rem);
    }
}

/* Print Styles */
@media print {
    .navbar,
    footer {
        display: none;
    }
    
    .service-card {
        break-inside: avoid;
    }
}
`;
    }
}

module.exports = DesignerAgent;
