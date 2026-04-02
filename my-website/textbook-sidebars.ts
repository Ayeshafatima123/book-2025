import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Sidebar for the textbook content
  textbookSidebar: [
    {
      type: 'category',
      label: 'Front Matter',
      items: [
        'front-matter/title-page',
        'front-matter/preface',
        'front-matter/table-of-contents',
        'front-matter/list-of-figures',
        'front-matter/list-of-tables',
        'front-matter/glossary',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Part I: Foundations',
      items: [
        {
          type: 'category',
          label: 'Chapter 1: Introduction to Physical AI',
          items: [
            'chapter-01/section-1',
            'chapter-01/section-2',
            'chapter-01/section-3',
            'chapter-01/section-4',
            'chapter-01/section-5',
            'chapter-01/summary',
          ],
          collapsed: false,
        },
        {
          type: 'category',
          label: 'Chapter 2: Fundamentals of Robotics & AI',
          items: [
            'chapter-02/section-1',
            'chapter-02/section-2',
            'chapter-02/section-3',
            'chapter-02/section-4',
            'chapter-02/section-5',
            'chapter-02/summary',
          ],
          collapsed: false,
        },
        {
          type: 'category',
          label: 'Chapter 3: AI-Hardware Integration',
          items: [
            'chapter-03/section-1',
            'chapter-03/section-2',
            'chapter-03/section-3',
            'chapter-03/section-4',
            'chapter-03/section-5',
            'chapter-03/summary',
          ],
          collapsed: false,
        },
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Part II: Core Concepts',
      items: [
        {
          type: 'category',
          label: 'Chapter 4: Sensing the Physical World',
          items: [
            'chapter-04/section-1',
            'chapter-04/section-2',
            'chapter-04/section-3',
            'chapter-04/section-4',
            'chapter-04/section-5',
            'chapter-04/summary',
          ],
          collapsed: false,
        },
        {
          type: 'category',
          label: 'Chapter 5: Acting in the Physical World',
          items: [
            'chapter-05/section-1',
            'chapter-05/section-2',
            'chapter-05/section-3',
            'chapter-05/section-4',
            'chapter-05/section-5',
            'chapter-05/summary',
          ],
          collapsed: false,
        },
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Back Matter',
      items: [
        'back-matter/appendices',
        'back-matter/bibliography',
        'back-matter/index',
      ],
      collapsed: false,
    },
    {
      type: 'link',
      label: '🤖 AI Assistant',
      href: '/chatbot',
    },
  ],
};

export default sidebars;