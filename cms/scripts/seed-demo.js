/**
 * LeadForge / Forma Studio Demo Content Seed Script (LF-103)
 * Provides realistic, explicitly fictional editorial content
 * for testing and static build synchronization.
 */

const demoContent = {
  siteSettings: {
    brandName: "Forma Studio",
    contactEmail: "inquiries@forma.studio",
    defaultSeo: {
      title: "Forma Studio — Digital Experiences, Built With Intent",
      description: "Independent digital consultancy engineering search-optimized web applications and conversion platforms.",
      ogImage: null,
    },
    socialLinks: [
      { label: "LinkedIn", url: "https://linkedin.com/company/forma-studio-demo" },
      { label: "GitHub", url: "https://github.com/forma-studio-demo" }
    ]
  },
  services: [
    {
      title: "Digital Experience Platforms",
      slug: "digital-experience-platforms",
      summary: "End-to-end editorial architectures and headless CMS integrations designed for autonomous content teams.",
      body: [
        {
          type: "paragraph",
          children: [{ type: "text", text: "We structure decoupled content systems that separate editorial freedom from high-performance delivery. Content editors receive clean, type-safe interfaces while visitors experience instantaneous, pre-rendered static performance." }]
        },
        {
          type: "heading",
          level: 2,
          children: [{ type: "text", text: "What we deliver" }]
        },
        {
          type: "list",
          format: "unordered",
          children: [
            { type: "list-item", children: [{ type: "text", text: "Headless CMS schema architecture and permission modeling" }] },
            { type: "list-item", children: [{ type: "text", text: "Static generation pipelines with zero runtime client bloat" }] },
            { type: "list-item", children: [{ type: "text", text: "Automated deployment gates with rollback safeguards" }] }
          ]
        }
      ],
      seo: {
        title: "Digital Experience Platforms | Forma Studio",
        description: "Decoupled editorial platforms engineered for autonomous content teams and instantaneous static delivery."
      },
      publishedAt: new Date().toISOString()
    },
    {
      title: "Search-Optimized Web Applications",
      slug: "search-optimized-web-apps",
      summary: "Technical SEO foundations, semantic markup, and crawlable pre-rendered static architectures.",
      body: [
        {
          type: "paragraph",
          children: [{ type: "text", text: "High conversion starts with crawlability. We design every route with semantic HTML5 hierarchy, truthful Open Graph and canonical metadata, automated XML sitemaps, and strict Core Web Vitals optimization." }]
        },
        {
          type: "heading",
          level: 2,
          children: [{ type: "text", text: "Technical Capabilities" }]
        },
        {
          type: "list",
          format: "unordered",
          children: [
            { type: "list-item", children: [{ type: "text", text: "100% server-generated crawlable static HTML" }] },
            { type: "list-item", children: [{ type: "text", text: "Automated dynamic sitemaps and strict robots directive handling" }] },
            { type: "list-item", children: [{ type: "text", text: "Sub-second LCP and zero Cumulative Layout Shift across viewports" }] }
          ]
        }
      ],
      seo: {
        title: "Search-Optimized Web Applications | Forma Studio",
        description: "Static-first engineering and technical SEO foundations built for crawlability and speed."
      },
      publishedAt: new Date().toISOString()
    },
    {
      title: "Performance & Conversion Architecture",
      slug: "performance-conversion-architecture",
      summary: "Resilient lead capture pipelines with strict input validation, abuse mitigation, and private storage.",
      body: [
        {
          type: "paragraph",
          children: [{ type: "text", text: "Inquiries are the lifeblood of B2B relationships. We build secure same-origin intake pipelines backed by independent APIs, isolating prospective customer data from public marketing content." }]
        },
        {
          type: "heading",
          level: 2,
          children: [{ type: "text", text: "Architecture Highlights" }]
        },
        {
          type: "list",
          format: "unordered",
          children: [
            { type: "list-item", children: [{ type: "text", text: "Same-origin reverse proxied endpoints with rate limiting" }] },
            { type: "list-item", children: [{ type: "text", text: "Strict Pydantic payload validation and honeypot filtering" }] },
            { type: "list-item", children: [{ type: "text", text: "Zero public exposure of captured prospect records" }] }
          ]
        }
      ],
      seo: {
        title: "Performance & Conversion Architecture | Forma Studio",
        description: "Secure, high-reliability lead capture pipelines and conversion-driven engineering."
      },
      publishedAt: new Date().toISOString()
    }
  ],
  caseStudies: [
    {
      title: "Decoupled Editorial Architecture for Kinetic Freight",
      slug: "kinetic-freight-platform",
      clientLabel: "Kinetic Freight (Fictional Demo)",
      challenge: "Kinetic Freight operated a monolithic CMS plagued by fragile deployments, slow response times, and content editors constantly blocked by engineering schedules.",
      solution: "Forma Studio migrated their editorial operations to a headless CMS paired with an Astro static build pipeline and automated CI/CD invalidation.",
      outcomes: [
        {
          type: "paragraph",
          children: [{ type: "text", text: "The new static infrastructure eliminated server rendering bottlenecks, allowing marketing to publish campaign pages independently while achieving sub-500ms page delivery across global regions." }]
        }
      ],
      seo: {
        title: "Kinetic Freight Case Study | Forma Studio",
        description: "How Forma Studio engineered a headless editorial platform with instant static delivery."
      },
      relatedServiceSlug: "digital-experience-platforms",
      publishedAt: new Date().toISOString()
    },
    {
      title: "High-Performance Inbound Platform for Solaris Metrics",
      slug: "solaris-metrics-rebuild",
      clientLabel: "Solaris Metrics (Fictional Demo)",
      challenge: "Solaris Metrics struggled with bot spam on their legacy web forms and suffered from unoptimized asset loading that degraded crawl performance.",
      solution: "Implemented an SEO-first static site coupled with an isolated FastAPI intake service featuring honeypot controls, reverse-proxy throttling, and private database persistence.",
      outcomes: [
        {
          type: "paragraph",
          children: [{ type: "text", text: "Spam submissions dropped by 99% immediately upon deployment, while 100% of published product routes gained verified canonical and sitemap coverage." }]
        }
      ],
      seo: {
        title: "Solaris Metrics Case Study | Forma Studio",
        description: "Eliminating form abuse and maximizing technical SEO coverage for an industrial analytics platform."
      },
      relatedServiceSlug: "performance-conversion-architecture",
      publishedAt: new Date().toISOString()
    }
  ],
  testimonials: [
    {
      authorName: "Marcus Vance",
      role: "VP of Product",
      company: "Kinetic Freight (Demo)",
      quote: "The discipline and editorial clarity Forma Studio brought to our web platform transformed our publishing speed completely. The static site is lightning fast.",
      relatedServiceSlug: "digital-experience-platforms",
      publishedAt: new Date().toISOString()
    },
    {
      authorName: "Elena Rostova",
      role: "Founder & CEO",
      company: "Solaris Metrics (Demo)",
      quote: "Our inquiry pipeline is now rock solid. Clean architecture, zero spam clutter, and an interface that projects quiet confidence.",
      relatedServiceSlug: "performance-conversion-architecture",
      publishedAt: new Date().toISOString()
    }
  ]
};

if (typeof module !== "undefined") {
  module.exports = { demoContent };
}
