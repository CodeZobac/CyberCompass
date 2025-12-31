"use client";

import { ReactNode } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BrutalPageLayoutProps {
  children: ReactNode;
  breadcrumbs?: BreadcrumbItem[];
  showFooter?: boolean;
}

export function BrutalPageLayout({ 
  children, 
  breadcrumbs,
  showFooter = true 
}: BrutalPageLayoutProps) {
  const pathname = usePathname();

  // Auto-generate breadcrumbs if not provided
  const generatedBreadcrumbs = breadcrumbs || generateBreadcrumbs(pathname);

  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Breadcrumb Navigation */}
      {generatedBreadcrumbs.length > 0 && (
        <nav 
          aria-label="Breadcrumb" 
          className="bg-brutal-gray-50 border-b-4 border-black py-4"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <ol className="flex items-center gap-2 text-sm font-bold">
              {generatedBreadcrumbs.map((crumb, index) => (
                <li key={index} className="flex items-center gap-2">
                  {index > 0 && (
                    <span className="text-brutal-gray-700" aria-hidden="true">
                      /
                    </span>
                  )}
                  {crumb.href ? (
                    <Link
                      href={crumb.href}
                      className="uppercase hover:text-brutal-blue hover:underline focus:outline-none focus:ring-2 focus:ring-brutal-blue"
                    >
                      {crumb.label}
                    </Link>
                  ) : (
                    <span className="uppercase text-brutal-gray-700" aria-current="page">
                      {crumb.label}
                    </span>
                  )}
                </li>
              ))}
            </ol>
          </div>
        </nav>
      )}

      {/* Main Content */}
      <main id="main-content" className="flex-1">
        {children}
      </main>

      {/* Footer */}
      {showFooter && <BrutalFooter />}
    </div>
  );
}

// Helper function to generate breadcrumbs from pathname
function generateBreadcrumbs(pathname: string): BreadcrumbItem[] {
  if (!pathname || pathname === '/') return [];

  const paths = pathname.split('/').filter(Boolean);
  const breadcrumbs: BreadcrumbItem[] = [
    { label: 'Home', href: '/' }
  ];

  let currentPath = '';
  paths.forEach((path, index) => {
    currentPath += `/${path}`;
    const isLast = index === paths.length - 1;
    
    // Format the label (remove hyphens, capitalize)
    const label = path
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');

    breadcrumbs.push({
      label,
      href: isLast ? undefined : currentPath
    });
  });

  return breadcrumbs;
}

// Brutalist Footer Component
function BrutalFooter() {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    features: [
      { label: 'Deepfake Detection', href: '/deepfake-training' },
      { label: 'Social Media Sim', href: '/social-media-sim' },
      { label: 'Catfish Detection', href: '/catfish-training' },
      { label: 'Analytics', href: '/analytics' }
    ],
    resources: [
      { label: 'About', href: '/about' },
      { label: 'Help Center', href: '/help' },
      { label: 'Contact', href: '/contact' },
      { label: 'FAQ', href: '/faq' }
    ],
    legal: [
      { label: 'Privacy Policy', href: '/privacy' },
      { label: 'Terms of Service', href: '/terms' },
      { label: 'Cookie Policy', href: '/cookies' }
    ]
  };

  return (
    <footer className="bg-white border-t-6 border-black mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Footer Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {/* Brand Section */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-brutal-red border-4 border-black shadow-brutal-sm flex items-center justify-center">
                <span className="text-2xl">🛡️</span>
              </div>
              <span className="text-xl font-black uppercase text-brutal-red">
                CyberCompass
              </span>
            </div>
            <p className="text-sm font-semibold text-brutal-gray-700 mb-4">
              AI-powered cybersecurity training for the next generation
            </p>
            <div className="flex gap-3">
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 border-4 border-black bg-white hover:bg-brutal-gray-50 flex items-center justify-center hover-press focus:outline-none focus:ring-2 focus:ring-brutal-blue"
                aria-label="Twitter"
              >
                <span className="text-xl">𝕏</span>
              </a>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 border-4 border-black bg-white hover:bg-brutal-gray-50 flex items-center justify-center hover-press focus:outline-none focus:ring-2 focus:ring-brutal-blue"
                aria-label="GitHub"
              >
                <span className="text-xl">⚙️</span>
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 border-4 border-black bg-white hover:bg-brutal-gray-50 flex items-center justify-center hover-press focus:outline-none focus:ring-2 focus:ring-brutal-blue"
                aria-label="LinkedIn"
              >
                <span className="text-xl">💼</span>
              </a>
            </div>
          </div>

          {/* Features Links */}
          <div>
            <h3 className="text-lg font-black uppercase mb-4 border-b-4 border-black pb-2">
              Features
            </h3>
            <ul className="space-y-2">
              {footerLinks.features.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm font-bold hover:text-brutal-blue hover:underline focus:outline-none focus:ring-2 focus:ring-brutal-blue"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources Links */}
          <div>
            <h3 className="text-lg font-black uppercase mb-4 border-b-4 border-black pb-2">
              Resources
            </h3>
            <ul className="space-y-2">
              {footerLinks.resources.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm font-bold hover:text-brutal-blue hover:underline focus:outline-none focus:ring-2 focus:ring-brutal-blue"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal Links */}
          <div>
            <h3 className="text-lg font-black uppercase mb-4 border-b-4 border-black pb-2">
              Legal
            </h3>
            <ul className="space-y-2">
              {footerLinks.legal.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm font-bold hover:text-brutal-blue hover:underline focus:outline-none focus:ring-2 focus:ring-brutal-blue"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t-4 border-black flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-sm font-bold text-brutal-gray-700">
            © {currentYear} CyberCompass. All rights reserved.
          </p>
          <p className="text-sm font-bold text-brutal-gray-700">
            Built with 💪 for digital literacy
          </p>
        </div>
      </div>
    </footer>
  );
}
