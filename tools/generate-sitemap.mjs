import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const origin = 'https://gtt10.github.io';
const fixedPages = [
  '',
  'about.html',
  'statistics.html',
  'pages/math.html',
  'pages/material_mechanics.html',
  'pages/fluid_mechanics.html',
  'pages/thermodynamics.html',
];
const subjects = ['math', 'materials', 'fluid', 'thermo'];
const examPages = subjects.flatMap((subject) =>
  fs
    .readdirSync(path.join(root, 'exams', subject))
    .filter((name) => /^\d{4}\.html$/.test(name))
    .sort((a, b) => b.localeCompare(a))
    .map((name) => `exams/${subject}/${name}`),
);
const pages = [...fixedPages, ...examPages];
const escapeXml = (value) =>
  value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const body = pages
  .map((page) => `  <url><loc>${escapeXml(`${origin}/${page}`)}</loc></url>`)
  .join('\n');
const xml = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  body,
  '</urlset>',
  '',
].join('\n');

fs.writeFileSync(path.join(root, 'sitemap.xml'), xml, 'utf8');
console.log(`Generated sitemap.xml with ${pages.length} public pages.`);
