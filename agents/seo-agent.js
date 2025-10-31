/**
 * SEO Agent
 * Specializes in search engine optimization and online presence
 */

const BaseAgent = require('./base-agent');

class SEOAgent extends BaseAgent {
    constructor() {
        super(
            'SEO Specialist',
            'SEO & Digital Marketing Specialist',
            ['seo', 'optimization', 'sem', 'analytics', 'online-presence', 'search-marketing']
        );
    }

    async execute(subtask) {
        await this.speak(`Optimizing SEO for: ${subtask.description}`);

        try {
            // Analyze current SEO
            const currentSEO = await this.analyzeCurrentSEO();
            
            // Create SEO strategy
            const strategy = this.createSEOStrategy();
            
            // Generate SEO improvements
            const improvements = await this.generateSEOImprovements(currentSEO);
            
            // Create SEO report
            const seoReport = this.createSEOReport(strategy, improvements, currentSEO);
            await this.writeFile('docs/seo-report.md', seoReport);

            // Create sitemap
            const sitemap = this.createSitemap();
            await this.writeFile('sitemap.xml', sitemap);

            // Create robots.txt
            const robots = this.createRobotsTxt();
            await this.writeFile('robots.txt', robots);

            await this.speak('SEO optimization completed! I\'ve created a comprehensive SEO strategy and optimization files.');

            return {
                success: true,
                strategy: strategy,
                improvements: improvements,
                documents: ['docs/seo-report.md', 'sitemap.xml', 'robots.txt']
            };
        } catch (error) {
            await this.speak(`SEO optimization encountered an issue: ${error.message}`);
            throw error;
        }
    }

    async analyzeCurrentSEO() {
        try {
            const html = await this.readFile('index.html');
            
            const analysis = {
                metaTags: {
                    title: html.match(/<title>([^<]+)<\/title>/)?.[1] || 'Not found',
                    description: html.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/)?.[1] || 'Not found',
                    keywords: html.match(/<meta\s+name=["']keywords["']\s+content=["']([^"']+)["']/)?.[1] || 'Not found'
                },
                structuredData: html.includes('application/ld+json') ? 'Present' : 'Missing',
                openGraph: html.includes('og:') ? 'Present' : 'Missing',
                canonical: html.includes('rel="canonical"') ? 'Present' : 'Missing',
                headings: {
                    h1: (html.match(/<h1/g) || []).length,
                    h2: (html.match(/<h2/g) || []).length,
                    h3: (html.match(/<h3/g) || []).length
                },
                images: {
                    total: (html.match(/<img/g) || []).length,
                    withAlt: (html.match(/<img[^>]*alt=["'][^"']+["']/g) || []).length
                },
                links: {
                    internal: (html.match(/href=["']#[^"']+["']/g) || []).length,
                    external: (html.match(/href=["']https?:\/\//g) || []).length
                }
            };

            return analysis;
        } catch (error) {
            return {
                metaTags: {},
                structuredData: 'Unknown',
                openGraph: 'Unknown',
                headings: {},
                images: {},
                links: {}
            };
        }
    }

    createSEOStrategy() {
        return {
            targetKeywords: [
                'AI customer support',
                'customer support automation',
                'support implementation services',
                'customer experience consulting',
                'AI integration services',
                'process optimization'
            ],
            contentStrategy: [
                'Focus on long-tail keywords',
                'Create pillar content',
                'Optimize for featured snippets',
                'Build topic clusters'
            ],
            technicalSEO: [
                'Optimize page speed',
                'Ensure mobile responsiveness',
                'Implement structured data',
                'Create XML sitemap',
                'Optimize images',
                'Fix broken links'
            ],
            linkBuilding: [
                'Guest posting',
                'Industry directories',
                'Partnership links',
                'Resource page links'
            ],
            localSEO: [
                'Google Business Profile',
                'Local citations',
                'Location-based content',
                'Customer reviews'
            ]
        };
    }

    async generateSEOImprovements(currentSEO) {
        const improvements = [];

        if (!currentSEO.metaTags.title || currentSEO.metaTags.title === 'Not found') {
            improvements.push('Add optimized title tag');
        }

        if (!currentSEO.metaTags.description || currentSEO.metaTags.description === 'Not found') {
            improvements.push('Add meta description');
        }

        if (currentSEO.structuredData === 'Missing') {
            improvements.push('Add structured data (JSON-LD)');
        }

        if (currentSEO.openGraph === 'Missing') {
            improvements.push('Add Open Graph tags');
        }

        if (currentSEO.headings.h1 !== 1) {
            improvements.push('Ensure single H1 tag per page');
        }

        if (currentSEO.images.total > 0 && currentSEO.images.withAlt < currentSEO.images.total) {
            improvements.push('Add alt text to all images');
        }

        improvements.push('Create XML sitemap');
        improvements.push('Add robots.txt');
        improvements.push('Optimize URL structure');
        improvements.push('Add breadcrumbs schema');

        return improvements;
    }

    createSEOReport(strategy, improvements, currentSEO) {
        return `# SEO Report - DEPLOYHELP LLC
Generated by SEO Specialist Agent

## Current SEO Status

### Meta Tags
- Title: ${currentSEO.metaTags.title || 'Missing'}
- Description: ${currentSEO.metaTags.description || 'Missing'}
- Keywords: ${currentSEO.metaTags.keywords || 'Missing'}

### Technical SEO
- Structured Data: ${currentSEO.structuredData}
- Open Graph: ${currentSEO.openGraph}
- Canonical: ${currentSEO.canonical || 'Unknown'}

### Content Structure
- H1 Tags: ${currentSEO.headings.h1 || 0}
- H2 Tags: ${currentSEO.headings.h2 || 0}
- H3 Tags: ${currentSEO.headings.h3 || 0}

### Images
- Total: ${currentSEO.images.total || 0}
- With Alt Text: ${currentSEO.images.withAlt || 0}

## SEO Strategy

### Target Keywords
${strategy.targetKeywords.map(kw => `- ${kw}`).join('\n')}

### Content Strategy
${strategy.contentStrategy.map(item => `- ${item}`).join('\n')}

### Technical SEO
${strategy.technicalSEO.map(item => `- ${item}`).join('\n')}

### Link Building
${strategy.linkBuilding.map(item => `- ${item}`).join('\n')}

### Local SEO
${strategy.localSEO.map(item => `- ${item}`).join('\n')}

## Recommended Improvements

${improvements.map(imp => `- ${imp}`).join('\n')}

## SEO Checklist

- [ ] Optimize title tags (50-60 characters)
- [ ] Write compelling meta descriptions (150-160 characters)
- [ ] Add alt text to all images
- [ ] Implement structured data
- [ ] Create XML sitemap
- [ ] Add robots.txt
- [ ] Optimize page speed
- [ ] Ensure mobile responsiveness
- [ ] Add internal linking
- [ ] Create content calendar

Generated by SEO Specialist Agent
`;
    }

    createSitemap() {
        return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
    <url>
        <loc>https://deployhelp.com/</loc>
        <lastmod>2025-01-27</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://deployhelp.com/about</loc>
        <lastmod>2025-01-27</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://deployhelp.com/services</loc>
        <lastmod>2025-01-27</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://deployhelp.com/contact</loc>
        <lastmod>2025-01-27</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
</urlset>`;
    }

    createRobotsTxt() {
        return `User-agent: *
Allow: /

# Sitemap
Sitemap: https://deployhelp.com/sitemap.xml

# Disallow admin or private areas if any
# Disallow: /admin/
# Disallow: /private/
`;
    }
}

module.exports = SEOAgent;
