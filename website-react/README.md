# SpecFlow Modern Landing Page

A modern, high-converting landing page built with React, Tailwind CSS, and Framer Motion.

## Features

- ✨ **Glassmorphism Design** - Modern frosted glass effects throughout
- 🎭 **Framer Motion Animations** - Smooth, professional animations and micro-interactions
- 🎨 **Emerald/Cyan Color Palette** - Trending, professional color scheme
- 🌙 **Dark Mode Toggle** - Full dark mode support with system preference detection
- 📱 **Fully Responsive** - Works beautifully on all device sizes
- ⚡ **Vite Powered** - Fast development and optimized builds

## Tech Stack

- **React 18** - UI library
- **Tailwind CSS 3.4** - Utility-first CSS framework
- **Framer Motion 11** - Animation library
- **Lucide React** - Modern icon library
- **Vite 5** - Build tool

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to the website-react folder:
   ```bash
   cd door-builder-app/website-react
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:5175](http://localhost:5175) in your browser

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` folder, ready for deployment.

## Project Structure

```
website-react/
├── index.html          # HTML entry point with dark mode script
├── package.json        # Dependencies and scripts
├── vite.config.js      # Vite configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── postcss.config.js   # PostCSS configuration
└── src/
    ├── main.jsx        # React entry point
    ├── App.jsx         # Main application component
    └── styles.css      # Global styles with Tailwind
```

## Design Features

### Hero Section
- Minimal and professional design
- No gradients - clean, solid colors
- Clean sans-serif typography (Inter)
- Parallax scrolling effect
- Animated scroll indicator

### Feature Cards
- Subtle micro-interactions on hover
- Icon animation with scale and rotation
- Ripple effect on icon container
- Smooth text slide animation
- "Learn more" indicator appears on hover

### Services Section
- Card-based layout with image zoom on hover
- Glassmorphism overlay effect
- Smooth transitions

### Portfolio Gallery
- Masonry-style grid layout
- Image zoom on hover
- Overlay with category and title

### Contact Form
- Clean, accessible form design
- Form validation
- Loading and success/error states
- Dark mode compatible

### Dark Mode
- Toggle in header (sun/moon icons)
- Persists preference to localStorage
- Respects system preference on first visit
- Smooth transition between modes

## Customization

### Colors
Edit `tailwind.config.js` to change the color palette:
- `primary` - Emerald green shades (main brand color)
- `accent` - Cyan shades (secondary accent color)

### Fonts
The project uses Inter as the primary font. To change it, update:
1. The Google Fonts link in `index.html`
2. The `fontFamily` in `tailwind.config.js`

### Content
All content (services, portfolio items, features, contact info) is defined in the `App.jsx` file as data arrays for easy editing.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Private - All rights reserved.
