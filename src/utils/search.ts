import projects from '../data/projects.json';
import publications from '../data/publications.json';
import news from '../data/news.json';
import { withBase } from './content';

export type SearchItem = {
  title: string;
  description: string;
  category: string;
  url: string;
};

export const staticPages: SearchItem[] = [
  { title: 'Home', description: 'Electrochemistry, materials, and sustainable technologies.', category: 'Page', url: withBase() },
  { title: 'About', description: 'Biography, experience, expertise, education, grants, and awards.', category: 'Page', url: withBase('about/') },
  { title: 'Projects', description: 'Electrochemistry, energy storage, materials, data science, and public engagement.', category: 'Page', url: withBase('projects/') },
  { title: 'Publications', description: 'Journal articles, datasets, preprints, conference papers, and thesis.', category: 'Page', url: withBase('publications/') },
  { title: 'News & notes', description: 'Research updates, publications, presentations, fellowships, and outreach.', category: 'Page', url: withBase('news/') },
  { title: 'Gallery', description: 'Conferences, events, research activities, and community engagement.', category: 'Page', url: withBase('gallery/') },
  { title: 'Contact', description: 'Contact form and professional profiles for research enquiries.', category: 'Page', url: withBase('contact/') },
];

export const searchItems: SearchItem[] = [
  ...staticPages,
  ...projects.map((item) => ({
    title: item.title,
    description: item.summary,
    category: item.category,
    url: withBase(`projects/${item.slug}/`),
  })),
  ...publications.map((item) => ({
    title: item.title,
    description: `${item.authors} · ${item.venue}`,
    category: item.type,
    url: withBase(`publications/#${item.slug}`),
  })),
  ...news.map((item) => ({
    title: item.title,
    description: item.excerpt,
    category: item.category,
    url: withBase(`news/${item.slug}/`),
  })),
];
