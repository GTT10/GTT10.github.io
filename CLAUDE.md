# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static HTML website serving as a graduate exam portal (大学院入試過去問ポータル) for Japanese university entrance exams. The site provides exam questions and solutions for engineering subjects from 2003-2024.

## Key Architecture

### File Structure
- `index.html` - Main landing page with tabbed navigation for 4 subjects
- `about.html` - Information about the website
- `css/style.css` - Main stylesheet with comprehensive styling for all pages
- `js/script.js` - JavaScript for tab switching and accordion functionality
- `exams/` - Subject-specific exam pages organized by subject and year
  - `math/`, `fluid/`, `materials/`, `thermo/` - One HTML file per year (2003-2024)
  - `math_template.html` - Template for creating new math exam pages
- `pdfs/` - PDF files organized by question/answer and year/subject
- `images/` - Supporting images for exam content
- `original_text/` - Original text data for all subjects (2003-2024)
  - `original_math/`, `original_fluid/`, `original_material/`, `original_thermo/` - Raw text files organized by year
  - Each year folder contains `info1.txt` and `info2.txt` files with exam content data
- `test_exams/` - Test and development exam pages
  - `math/`, `fluid/`, `materials/`, `thermo/` - Sample HTML files for testing new layouts and features
  - Contains template files and experimental exam page implementations

### Page Types

1. **Main Page (`index.html`)**
   - Tabbed interface for 4 subjects: 数学 (Math), 流体力学 (Fluid Dynamics), 材料力学 (Materials), 熱力学 (Thermodynamics)
   - Card grid layout showing years 2003-2024 for each subject
   - Uses JavaScript tab switching functionality

2. **Exam Pages (`exams/{subject}/{year}.html`)**
   - Two main templates: simple format (like `2024.html`) and comprehensive format (like `math_template.html`)
   - Comprehensive format includes:
     - Problem overview section with PDF download links
     - Multi-column grid layout (4:1 ratio for content:sidebar)
     - MathJax integration for mathematical expressions
     - Accordion sections for alternative solutions
     - Structured sections: problem statement, hints, solutions, summaries

### CSS Architecture

The stylesheet (`css/style.css`) is organized into sections:
- Reset & base styles
- Tab navigation styling
- Card grid layout for index page
- Comprehensive exam page styling (`.page-wrapper`, `.exam-grid`, etc.)
- Responsive design for mobile/tablet
- Print-specific styles for exam pages

### JavaScript Functionality

- Tab switching for main page navigation
- Accordion toggle for expandable sections in exam pages
- Functions are in `js/script.js` and inline in template pages

## Development Guidelines

### Adding New Exam Years
1. Create new HTML files in appropriate subject folder (`exams/{subject}/{year}.html`)
2. Use `math_template.html` as reference for comprehensive exam pages
3. Update main `index.html` to add links to new year
4. Add corresponding PDF files in `pdfs/question/` and `pdfs/answer/` directories

### CSS Class Conventions
- `.page-wrapper` - Main container for exam pages
- `.exam-grid` - Two-column layout container (4:1 ratio)
- `.exam-col-left`/`.exam-col-right` - Grid column containers
- `.main-section-title` - Major problem section headers
- `.problem-overview-section` - Problem description with PDF links
- `.example-box` - Problem statement containers
- `.point-box` - Hint and tip containers
- `.solution-step` - Individual solution steps
- `.accordion` - Expandable content sections

### MathJax Integration
Exam pages include MathJax for mathematical notation:
- Inline math: `$...$` or `\(...\)`
- Display math: `$$...$$` or `\[...\]`
- Configuration in template head section

### Responsive Considerations
- Mobile-first design with breakpoint at 768px
- Tab navigation becomes stacked on mobile
- Grid layouts become single-column on small screens
- Print styles included for exam page printing

## File Conventions

### Naming Patterns
- Exam pages: `{year}.html` (e.g., `2024.html`)
- PDF files: `{subject}_{year}_{type}_question.pdf` or `{subject}_{year}_answer.pdf`
- Image files: `{subject}_{year}_{number}.png`

### Path References
- From exam pages to main CSS: `../../css/style.css`
- From exam pages to main JS: `../../js/script.js`
- From exam pages to index: `../../index.html`
- PDF links use relative paths to `../../pdfs/` directory

No build process, testing framework, or package management is required - this is a static HTML website that can be served directly by any web server.

## Project Context & Notes

### Target Audience
- Primary: 岡山大学 (Okayama University) students only
- Not intended for public release or other universities
- Internal use within university community

### Development Status
- Currently in active development/construction phase
- New yearly exam additions not currently planned
- Focus is on completing existing functionality and content

### Usage Analytics
- No tracking or analytics requirements
- User behavior analysis not needed