import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Bridging Artificial Intelligence and Physical Systems',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // ✅ GitHub Pages URL
  url: 'https://ayeshafatima123.github.io',
  baseUrl: '/hackathon--book-2025/',

  // ✅ GitHub repo info (MOST IMPORTANT)
  organizationName: 'Ayeshafatima123',
  projectName: 'hackathon--book-2025',
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',
  trailingSlash: false,

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
      },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/Ayeshafatima123/hackathon--book-2025/edit/main/',
          path: 'docs',
          routeBasePath: 'docs',
        },
        blog: {
          showReadingTime: true,
          editUrl:
            'https://github.com/Ayeshafatima123/hackathon--book-2025/edit/main/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'textbook',
        path: 'textbook',
        routeBasePath: 'textbook',
        sidebarPath: './textbook-sidebars.ts',
        editUrl:
          'https://github.com/Ayeshafatima123/hackathon--book-2025/edit/main/',
      },
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI & Humanoid Robotics Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book Chapters',
        },
        {
          type: 'doc',
          docId: 'front-matter/title-page',
          position: 'left',
          label: 'Textbook',
          docsPluginId: 'textbook',
        },
        { to: '/docs/introduction', label: 'Get Started', position: 'left' },
        { to: '/chatbot', label: 'AI Assistant', position: 'left' },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: 'https://github.com/Ayeshafatima123/hackathon--book-2025',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Book',
          items: [
            { label: 'Introduction', to: '/docs/introduction' },
            { label: 'Chapters', to: '/docs/introduction' },
            {
              label: 'Textbook Version',
              to: '/textbook/front-matter/title-page',
            },
            {
              label: 'AI Assistant',
              to: '/chatbot',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'GitHub Repository',
              href: 'https://github.com/Ayeshafatima123/hackathon--book-2025',
            },
          ],
        },
        {
          title: 'More',
          items: [
            { label: 'Blog', to: '/blog' },
            {
              label: 'GitHub',
              href: 'https://github.com/Ayeshafatima123/hackathon--book-2025',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
