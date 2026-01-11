import { useState, useEffect } from 'react';
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import { 
  Moon, Sun, Menu, X, Star, CheckCircle, Clock, Users, 
  Mail, Phone, MapPin, ArrowRight, ChevronDown 
} from 'lucide-react';

// ============================================
// HOOKS
// ============================================

const useDarkMode = () => {
  const [isDark, setIsDark] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('darkMode');
      return saved ? JSON.parse(saved) : window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(isDark));
    document.documentElement.classList.toggle('dark', isDark);
  }, [isDark]);

  return [isDark, setIsDark];
};

// ============================================
// COMPONENTS
// ============================================

// Glassmorphism Card Component
const GlassCard = ({ children, className = '', hover = true }) => (
  <motion.div
    className={`
      backdrop-blur-xl bg-white/10 dark:bg-white/5
      border border-white/20 dark:border-white/10
      rounded-2xl shadow-xl
      ${hover ? 'hover:bg-white/20 dark:hover:bg-white/10 hover:border-white/30' : ''}
      transition-all duration-300
      ${className}
    `}
    whileHover={hover ? { y: -4, scale: 1.01 } : {}}
    transition={{ type: "spring", stiffness: 300, damping: 20 }}
  >
    {children}
  </motion.div>
);

// Feature Card with Micro-interactions
const FeatureCard = ({ icon: Icon, title, description, delay = 0 }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.5, delay }}
      className="group relative"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={`
        relative p-8 rounded-2xl
        bg-white dark:bg-gray-900
        border border-gray-100 dark:border-gray-800
        shadow-sm hover:shadow-xl
        transition-all duration-500
        overflow-hidden
      `}>
        {/* Subtle glow effect on hover */}
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-primary-500/10 to-accent-500/10 opacity-0 rounded-2xl"
          animate={{ opacity: isHovered ? 1 : 0 }}
          transition={{ duration: 0.3 }}
        />
        
        {/* Icon container with micro-interaction */}
        <motion.div
          className="relative w-14 h-14 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center mb-6"
          animate={{ 
            scale: isHovered ? 1.1 : 1,
            rotate: isHovered ? 5 : 0
          }}
          transition={{ type: "spring", stiffness: 400, damping: 17 }}
        >
          <Icon 
            className="w-7 h-7 text-primary-600 dark:text-primary-400" 
            strokeWidth={1.5}
          />
          
          {/* Ripple effect */}
          <AnimatePresence>
            {isHovered && (
              <motion.div
                initial={{ scale: 0.5, opacity: 0.5 }}
                animate={{ scale: 2, opacity: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.6 }}
                className="absolute inset-0 rounded-xl bg-primary-500"
              />
            )}
          </AnimatePresence>
        </motion.div>

        <motion.h3
          className="text-xl font-semibold text-gray-900 dark:text-white mb-3"
          animate={{ x: isHovered ? 4 : 0 }}
          transition={{ type: "spring", stiffness: 400, damping: 17 }}
        >
          {title}
        </motion.h3>
        
        <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
          {description}
        </p>

        {/* Arrow indicator */}
        <motion.div
          className="mt-6 flex items-center text-primary-600 dark:text-primary-400 font-medium"
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: isHovered ? 1 : 0, x: isHovered ? 0 : -10 }}
          transition={{ duration: 0.2 }}
        >
          <span className="mr-2">Learn more</span>
          <ArrowRight className="w-4 h-4" />
        </motion.div>
      </div>
    </motion.div>
  );
};

// Service Card Component
const ServiceCard = ({ image, title, description, link, delay = 0 }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.6, delay }}
      className="group relative overflow-hidden rounded-2xl bg-white dark:bg-gray-900 shadow-lg"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Image Container */}
      <div className="relative h-56 overflow-hidden">
        <motion.img
          src={image}
          alt={title}
          className="w-full h-full object-cover"
          animate={{ scale: isHovered ? 1.08 : 1 }}
          transition={{ duration: 0.6 }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
      </div>

      {/* Content */}
      <div className="p-6">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          {title}
        </h3>
        <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-4">
          {description}
        </p>
        <motion.a
          href={link}
          className="inline-flex items-center text-primary-600 dark:text-primary-400 font-medium text-sm group/link"
          whileHover={{ x: 4 }}
        >
          Explore 
          <motion.span
            className="ml-1"
            animate={{ x: isHovered ? 4 : 0 }}
            transition={{ type: "spring", stiffness: 400, damping: 17 }}
          >
            →
          </motion.span>
        </motion.a>
      </div>

      {/* Glassmorphism overlay on hover */}
      <motion.div
        className="absolute inset-0 backdrop-blur-sm bg-primary-500/5 pointer-events-none rounded-2xl"
        initial={{ opacity: 0 }}
        animate={{ opacity: isHovered ? 1 : 0 }}
        transition={{ duration: 0.3 }}
      />
    </motion.div>
  );
};

// Portfolio Item
const PortfolioItem = ({ image, category, title, span = '' }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className={`relative overflow-hidden rounded-2xl cursor-pointer ${span}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <motion.img
        src={image}
        alt={title}
        className="w-full h-full object-cover"
        animate={{ scale: isHovered ? 1.1 : 1 }}
        transition={{ duration: 0.6 }}
      />
      
      {/* Overlay */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-t from-gray-900/90 via-gray-900/50 to-transparent flex flex-col justify-end p-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: isHovered ? 1 : 0 }}
        transition={{ duration: 0.3 }}
      >
        <span className="text-primary-400 text-xs font-semibold uppercase tracking-wider mb-1">
          {category}
        </span>
        <h3 className="text-white text-lg font-semibold">{title}</h3>
      </motion.div>
    </motion.div>
  );
};

// Stat Component
const StatCard = ({ number, label, delay = 0 }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.5, delay }}
    className="text-center"
  >
    <motion.span
      className="block text-4xl md:text-5xl font-bold text-primary-500 mb-2"
      initial={{ scale: 0.5 }}
      whileInView={{ scale: 1 }}
      viewport={{ once: true }}
      transition={{ type: "spring", stiffness: 200, delay: delay + 0.2 }}
    >
      {number}
    </motion.span>
    <span className="text-gray-600 dark:text-gray-400 text-sm uppercase tracking-wider">
      {label}
    </span>
  </motion.div>
);

// ============================================
// MAIN APP COMPONENT
// ============================================

export default function App() {
  const [isDark, setIsDark] = useDarkMode();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const { scrollY } = useScroll();

  // Scroll handler for header
  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Parallax effect for hero
  const heroY = useTransform(scrollY, [0, 500], [0, 150]);
  const heroOpacity = useTransform(scrollY, [0, 300], [1, 0]);

  // Form state
  const [formData, setFormData] = useState({
    name: '', email: '', project: '', message: ''
  });
  const [formStatus, setFormStatus] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormStatus('sending');
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        setFormStatus('success');
        setFormData({ name: '', email: '', project: '', message: '' });
      } else {
        setFormStatus('error');
      }
    } catch {
      setFormStatus('error');
    }
  };

  // Data
  const navLinks = [
    { href: '#services', label: 'Services' },
    { href: '#portfolio', label: 'Portfolio' },
    { href: '#about', label: 'About' },
    { href: '#contact', label: 'Contact' },
  ];

  const features = [
    { icon: Star, title: 'Expert Design', description: 'Professional consultation to match your unique architectural vision.' },
    { icon: CheckCircle, title: 'Quality Assured', description: 'Premium materials with rigorous quality control standards.' },
    { icon: Clock, title: 'Fast Delivery', description: 'Efficient turnaround without compromising on quality.' },
    { icon: Users, title: 'Full Support', description: 'From initial spec to final installation, we\'re with you.' },
  ];

  const services = [
    {
      image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&h=400&fit=crop',
      title: 'Residential',
      description: 'Custom entry doors, interior doors, and hardware for homes that make a statement.',
      link: '#portfolio'
    },
    {
      image: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&h=400&fit=crop',
      title: 'Commercial',
      description: 'Professional-grade doors for offices, retail, and high-traffic environments.',
      link: '#portfolio'
    },
    {
      image: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=600&h=400&fit=crop',
      title: 'Custom Design',
      description: 'Bespoke solutions tailored to your unique vision. From concept to installation.',
      link: '#contact'
    },
  ];

  const portfolioItems = [
    { image: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=600&h=900&fit=crop', category: 'Residential', title: 'Modern Entry', span: 'row-span-2' },
    { image: 'https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=600&h=400&fit=crop', category: 'Commercial', title: 'Office Entrance' },
    { image: 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=600&h=400&fit=crop', category: 'Interior', title: 'Sliding Design' },
    { image: 'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=1200&h=500&fit=crop', category: 'Custom', title: 'Luxury Estate Entry', span: 'col-span-2' },
    { image: 'https://images.unsplash.com/photo-1600573472550-8090b5e0745e?w=600&h=400&fit=crop', category: 'Interior', title: 'Contemporary Design' },
    { image: 'https://images.unsplash.com/photo-1600210492493-0946911123ea?w=600&h=400&fit=crop', category: 'Custom', title: 'Pivot Door' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-white transition-colors duration-300">
      
      {/* ============================================ */}
      {/* HEADER */}
      {/* ============================================ */}
      <motion.header
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          isScrolled 
            ? 'bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl shadow-lg border-b border-gray-200/50 dark:border-gray-800/50' 
            : 'bg-transparent'
        }`}
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <a href="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                SF
              </div>
              <span className={`font-semibold text-xl transition-colors ${
                isScrolled ? 'text-gray-900 dark:text-white' : 'text-white'
              }`}>
                SpecFlow
              </span>
            </a>

            {/* Desktop Nav */}
            <nav className="hidden md:flex items-center gap-8">
              {navLinks.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  className={`text-sm font-medium transition-colors hover:text-primary-500 ${
                    isScrolled ? 'text-gray-700 dark:text-gray-300' : 'text-white/90'
                  }`}
                >
                  {link.label}
                </a>
              ))}
            </nav>

            {/* Actions */}
            <div className="flex items-center gap-4">
              {/* Dark Mode Toggle */}
              <motion.button
                onClick={() => setIsDark(!isDark)}
                className={`p-2 rounded-lg transition-colors ${
                  isScrolled 
                    ? 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300' 
                    : 'hover:bg-white/10 text-white'
                }`}
                whileTap={{ scale: 0.95 }}
                aria-label="Toggle dark mode"
              >
                <AnimatePresence mode="wait">
                  {isDark ? (
                    <motion.div
                      key="sun"
                      initial={{ rotate: -90, opacity: 0 }}
                      animate={{ rotate: 0, opacity: 1 }}
                      exit={{ rotate: 90, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <Sun className="w-5 h-5" />
                    </motion.div>
                  ) : (
                    <motion.div
                      key="moon"
                      initial={{ rotate: 90, opacity: 0 }}
                      animate={{ rotate: 0, opacity: 1 }}
                      exit={{ rotate: -90, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <Moon className="w-5 h-5" />
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.button>

              {/* CTA Button */}
              <motion.a
                href="http://localhost:5174"
                className="hidden md:inline-flex items-center gap-2 px-5 py-2.5 bg-primary-600 hover:bg-primary-700 text-white text-sm font-medium rounded-lg transition-colors"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Door Builder
                <ArrowRight className="w-4 h-4" />
              </motion.a>

              {/* Mobile Menu Toggle */}
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className={`md:hidden p-2 rounded-lg ${
                  isScrolled ? 'text-gray-700 dark:text-gray-300' : 'text-white'
                }`}
                aria-label="Toggle menu"
              >
                {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800"
            >
              <div className="px-6 py-4 space-y-3">
                {navLinks.map((link) => (
                  <a
                    key={link.href}
                    href={link.href}
                    onClick={() => setIsMenuOpen(false)}
                    className="block text-gray-700 dark:text-gray-300 hover:text-primary-500 font-medium"
                  >
                    {link.label}
                  </a>
                ))}
                <a
                  href="http://localhost:5174"
                  className="block w-full text-center px-5 py-2.5 bg-primary-600 text-white font-medium rounded-lg mt-4"
                >
                  Door Builder
                </a>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.header>

      {/* ============================================ */}
      {/* HERO SECTION - Minimal & Professional */}
      {/* ============================================ */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gray-900">
        {/* Background Image */}
        <motion.div 
          className="absolute inset-0"
          style={{ y: heroY }}
        >
          <img
            src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1920&h=1080&fit=crop"
            alt="Elegant door entrance"
            className="w-full h-full object-cover opacity-40"
          />
          <div className="absolute inset-0 bg-gray-900/60" />
        </motion.div>

        {/* Hero Content */}
        <motion.div 
          className="relative z-10 max-w-4xl mx-auto px-6 text-center"
          style={{ opacity: heroOpacity }}
        >
          <motion.span
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-block text-primary-400 text-sm font-semibold tracking-widest uppercase mb-6"
          >
            Premium Door Solutions
          </motion.span>
          
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-semibold text-white mb-6 leading-tight tracking-tight"
          >
            Crafting Entrances
            <br />
            <span className="text-gray-300">That Inspire</span>
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Bespoke doors and precision hardware for homes and commercial spaces. 
            Elevate your architecture with expert design.
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <motion.a
              href="http://localhost:5174"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Start Your Project
              <ArrowRight className="w-5 h-5" />
            </motion.a>
            <motion.a
              href="#portfolio"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 border border-white/30 hover:bg-white/10 text-white font-medium rounded-lg transition-colors"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              View Our Work
            </motion.a>
          </motion.div>
        </motion.div>

        {/* Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center text-white/60"
        >
          <span className="text-xs uppercase tracking-widest mb-3">Scroll to explore</span>
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            <ChevronDown className="w-5 h-5" />
          </motion.div>
        </motion.div>
      </section>

      {/* ============================================ */}
      {/* SERVICES SECTION */}
      {/* ============================================ */}
      <section id="services" className="py-24 bg-white dark:bg-gray-950">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <span className="text-primary-600 dark:text-primary-400 text-sm font-semibold tracking-widest uppercase">
              Our Services
            </span>
            <h2 className="text-3xl md:text-4xl font-semibold mt-4 text-gray-900 dark:text-white">
              What We Offer
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {services.map((service, idx) => (
              <ServiceCard key={service.title} {...service} delay={idx * 0.1} />
            ))}
          </div>
        </div>
      </section>

      {/* ============================================ */}
      {/* PORTFOLIO SECTION */}
      {/* ============================================ */}
      <section id="portfolio" className="py-24 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <span className="text-primary-600 dark:text-primary-400 text-sm font-semibold tracking-widest uppercase">
              Our Work
            </span>
            <h2 className="text-3xl md:text-4xl font-semibold mt-4 text-gray-900 dark:text-white">
              Door Portfolio
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-4 max-w-lg mx-auto">
              A curated selection of our finest installations across Arizona
            </p>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 auto-rows-[200px] md:auto-rows-[250px]">
            {portfolioItems.map((item, idx) => (
              <PortfolioItem key={idx} {...item} />
            ))}
          </div>
        </div>
      </section>

      {/* ============================================ */}
      {/* ABOUT / FEATURES SECTION */}
      {/* ============================================ */}
      <section id="about" className="py-24 bg-white dark:bg-gray-950">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* Content */}
            <div>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
              >
                <span className="text-primary-600 dark:text-primary-400 text-sm font-semibold tracking-widest uppercase">
                  Why Choose Us
                </span>
                <h2 className="text-3xl md:text-4xl font-semibold mt-4 mb-6 text-gray-900 dark:text-white">
                  Precision in Every Detail
                </h2>
                <p className="text-lg text-gray-600 dark:text-gray-400 leading-relaxed mb-10">
                  At SpecFlow, we believe doors are more than functional elements—they're statements 
                  of design and quality that define your space.
                </p>
              </motion.div>

              <div className="grid sm:grid-cols-2 gap-6">
                {features.map((feature, idx) => (
                  <FeatureCard key={feature.title} {...feature} delay={idx * 0.1} />
                ))}
              </div>
            </div>

            {/* Image with Stats */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="relative"
            >
              <img
                src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=1000&fit=crop"
                alt="Quality craftsmanship"
                className="w-full h-auto rounded-2xl shadow-2xl"
              />
              
              {/* Stats Overlay */}
              <GlassCard className="absolute -bottom-8 -left-8 p-6" hover={false}>
                <div className="flex gap-8">
                  <StatCard number="500+" label="Projects" />
                  <StatCard number="15+" label="Years" delay={0.1} />
                </div>
              </GlassCard>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ============================================ */}
      {/* CTA BANNER */}
      {/* ============================================ */}
      <section className="py-24 bg-gray-900 relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, white 1px, transparent 0)`,
            backgroundSize: '40px 40px'
          }} />
        </div>

        <div className="max-w-4xl mx-auto px-6 text-center relative z-10">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-4xl font-semibold text-white mb-4"
          >
            Ready to Transform Your Space?
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-gray-400 text-lg mb-8 max-w-xl mx-auto"
          >
            Let's create something extraordinary together. Get started with our interactive door builder.
          </motion.p>
          <motion.a
            href="http://localhost:5174"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white hover:bg-gray-100 text-gray-900 font-medium rounded-lg transition-colors"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            Launch Door Builder
            <ArrowRight className="w-5 h-5" />
          </motion.a>
        </div>
      </section>

      {/* ============================================ */}
      {/* CONTACT SECTION */}
      {/* ============================================ */}
      <section id="contact" className="py-24 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid lg:grid-cols-2 gap-16">
            {/* Contact Info */}
            <div>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
              >
                <span className="text-primary-600 dark:text-primary-400 text-sm font-semibold tracking-widest uppercase">
                  Get In Touch
                </span>
                <h2 className="text-3xl md:text-4xl font-semibold mt-4 mb-4 text-gray-900 dark:text-white">
                  Let's Discuss Your Project
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mb-10 leading-relaxed">
                  Whether you're building new or renovating, we're here to help you find the perfect door solution.
                </p>
              </motion.div>

              <div className="space-y-6">
                {[
                  { icon: Mail, label: 'Email', value: 'Matt@SpecFlow.Tech', href: 'mailto:Matt@SpecFlow.Tech' },
                  { icon: Phone, label: 'Phone', value: '(480) 243-7837', href: 'tel:+14802437837' },
                  { icon: MapPin, label: 'Service Area', value: 'Phoenix & Scottsdale, AZ' },
                ].map((item, idx) => (
                  <motion.a
                    key={item.label}
                    href={item.href || '#'}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: idx * 0.1 }}
                    className="flex items-center gap-4 group"
                  >
                    <div className="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
                      <item.icon className="w-5 h-5 text-primary-600 dark:text-primary-400" />
                    </div>
                    <div>
                      <span className="text-sm text-gray-500 dark:text-gray-400">{item.label}</span>
                      <p className="text-gray-900 dark:text-white font-medium group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                        {item.value}
                      </p>
                    </div>
                  </motion.a>
                ))}
              </div>
            </div>

            {/* Contact Form */}
            <motion.form
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              onSubmit={handleSubmit}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl"
            >
              <div className="grid sm:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Name
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="Your name"
                    required
                    className="w-full px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="Your email"
                    required
                    className="w-full px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                  />
                </div>
              </div>
              
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Project Type
                </label>
                <select
                  value={formData.project}
                  onChange={(e) => setFormData({ ...formData, project: e.target.value })}
                  className="w-full px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                >
                  <option value="">Select project type</option>
                  <option value="residential">Residential</option>
                  <option value="commercial">Commercial</option>
                  <option value="custom">Custom Design</option>
                </select>
              </div>
              
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Message
                </label>
                <textarea
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  rows={4}
                  placeholder="Tell us about your project..."
                  required
                  className="w-full px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all resize-none"
                />
              </div>
              
              <motion.button
                type="submit"
                disabled={formStatus === 'sending'}
                className="w-full py-4 bg-primary-600 hover:bg-primary-700 disabled:bg-primary-400 text-white font-medium rounded-lg transition-colors"
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
              >
                {formStatus === 'sending' ? 'Sending...' : 'Send Message'}
              </motion.button>

              {formStatus && formStatus !== 'sending' && (
                <motion.p
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`mt-4 text-center text-sm ${
                    formStatus === 'success' ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {formStatus === 'success' 
                    ? '✓ Message sent! We\'ll be in touch soon.' 
                    : 'Failed to send. Please try again.'}
                </motion.p>
              )}
            </motion.form>
          </div>
        </div>
      </section>

      {/* ============================================ */}
      {/* FOOTER */}
      {/* ============================================ */}
      <footer className="py-16 bg-gray-900 dark:bg-gray-950">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-12 mb-12">
            {/* Brand */}
            <div className="md:col-span-2">
              <a href="/" className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                  SF
                </div>
                <span className="font-semibold text-xl text-white">SpecFlow</span>
              </a>
              <p className="text-gray-400 max-w-sm leading-relaxed">
                Premium door solutions for homes and businesses throughout the Phoenix metropolitan area.
              </p>
            </div>

            {/* Quick Links */}
            <div>
              <h4 className="text-white font-semibold mb-4">Quick Links</h4>
              <div className="space-y-3">
                {navLinks.map((link) => (
                  <a
                    key={link.href}
                    href={link.href}
                    className="block text-gray-400 hover:text-primary-400 transition-colors"
                  >
                    {link.label}
                  </a>
                ))}
              </div>
            </div>

            {/* Tools */}
            <div>
              <h4 className="text-white font-semibold mb-4">Tools</h4>
              <div className="space-y-3">
                <a href="http://localhost:5174" className="block text-gray-400 hover:text-primary-400 transition-colors">
                  Door Builder
                </a>
                <a href="/admin/" className="block text-gray-400 hover:text-primary-400 transition-colors">
                  Admin Portal
                </a>
              </div>
            </div>
          </div>

          <div className="pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-500 text-sm">
              © {new Date().getFullYear()} SpecFlow. All rights reserved.
            </p>
            <p className="text-gray-500 text-sm">
              Serving Phoenix & Scottsdale, Arizona
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
