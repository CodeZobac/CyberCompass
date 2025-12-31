"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { useSession, signIn, signOut } from "next-auth/react";
import { usePathname } from "next/navigation";

export function BrutalNavigation() {
  const { data: session } = useSession();
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isFeaturesOpen, setIsFeaturesOpen] = useState(false);
  const [adminStatus, setAdminStatus] = useState({ isAdmin: false, isRootAdmin: false });

  // Check if user is admin
  useEffect(() => {
    if (session?.user?.id) {
      fetch('/api/admin/check')
        .then(res => res.json())
        .then(data => setAdminStatus(data))
        .catch(() => setAdminStatus({ isAdmin: false, isRootAdmin: false }));
    }
  }, [session]);

  // Close mobile menu when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
    setIsFeaturesOpen(false);
  }, [pathname]);

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (!target.closest('.features-dropdown')) {
        setIsFeaturesOpen(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  const features = [
    {
      name: "Deepfake Detection",
      href: "/deepfake-training",
      icon: "🎭",
      description: "Master spotting manipulated media"
    },
    {
      name: "Social Media Simulation",
      href: "/social-media-sim",
      icon: "📱",
      description: "Navigate the feed safely"
    },
    {
      name: "Catfish Detection",
      href: "/catfish-training",
      icon: "💬",
      description: "Spot red flags in chats"
    },
    {
      name: "Analytics Dashboard",
      href: "/analytics",
      icon: "📊",
      description: "Track your progress"
    }
  ];

  const handleKeyDown = (e: React.KeyboardEvent, action: () => void) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      action();
    }
  };

  return (
    <>
      {/* Skip to content link for accessibility */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-6 focus:py-3 focus:bg-brutal-blue focus:text-white focus:border-4 focus:border-black focus:shadow-brutal-md focus:outline-none"
      >
        Skip to main content
      </a>

      <nav className="bg-white border-b-4 sm:border-b-6 border-black sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16 sm:h-20">
            {/* Logo */}
            <Link 
              href="/" 
              className="flex items-center gap-2 sm:gap-3 hover-press focus:outline-none focus:ring-4 focus:ring-brutal-blue"
              aria-label="CyberCompass Home"
            >
              <div className="w-10 h-10 sm:w-12 sm:h-12 bg-brutal-red border-2 sm:border-4 border-black shadow-[2px_2px_0_0_#000] sm:shadow-brutal-sm flex items-center justify-center">
                <span className="text-xl sm:text-2xl">🛡️</span>
              </div>
              <span className="text-lg sm:text-2xl font-black uppercase tracking-tight text-brutal-red hidden xs:block">
                CyberCompass
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-6">
              {/* Features Dropdown */}
              <div className="relative features-dropdown">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setIsFeaturesOpen(!isFeaturesOpen);
                  }}
                  onKeyDown={(e) => handleKeyDown(e, () => setIsFeaturesOpen(!isFeaturesOpen))}
                  className="px-4 py-2 font-bold uppercase text-sm border-4 border-black bg-white hover:bg-brutal-gray-50 transition-colors focus:outline-none focus:ring-4 focus:ring-brutal-blue"
                  aria-expanded={isFeaturesOpen}
                  aria-haspopup="true"
                >
                  Features ▼
                </button>

                {isFeaturesOpen && (
                  <div className="absolute top-full left-0 mt-2 w-80 bg-white border-4 border-black shadow-brutal-lg animate-slide-in">
                    <div className="p-4 space-y-2">
                      {features.map((feature) => (
                        <Link
                          key={feature.href}
                          href={feature.href}
                          className="block p-3 border-2 border-black hover:bg-brutal-gray-50 hover-press focus:outline-none focus:ring-4 focus:ring-brutal-blue"
                        >
                          <div className="flex items-start gap-3">
                            <span className="text-2xl">{feature.icon}</span>
                            <div>
                              <div className="font-bold text-sm">{feature.name}</div>
                              <div className="text-xs text-brutal-gray-700">{feature.description}</div>
                            </div>
                          </div>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Other Navigation Links */}
              <Link
                href="/about"
                className="px-4 py-2 font-bold uppercase text-sm hover:underline focus:outline-none focus:ring-4 focus:ring-brutal-blue"
              >
                About
              </Link>

              {adminStatus.isAdmin && (
                <Link
                  href="/admin"
                  className="px-4 py-2 font-bold uppercase text-sm hover:underline focus:outline-none focus:ring-4 focus:ring-brutal-blue"
                >
                  Admin
                </Link>
              )}

              {/* Authentication */}
              {session ? (
                <div className="flex items-center gap-4">
                  <Link
                    href="/profile"
                    className="px-4 py-2 font-bold uppercase text-sm border-4 border-black bg-brutal-blue text-white hover-press focus:outline-none focus:ring-4 focus:ring-brutal-blue"
                  >
                    Profile
                  </Link>
                  <button
                    onClick={() => signOut()}
                    className="px-4 py-2 font-bold uppercase text-sm border-4 border-black bg-white hover:bg-brutal-gray-50 focus:outline-none focus:ring-4 focus:ring-brutal-blue"
                  >
                    Sign Out
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => signIn("google")}
                  className="px-6 py-2 font-bold uppercase text-sm border-4 border-black bg-brutal-blue text-white shadow-brutal-sm hover-press focus:outline-none focus:ring-4 focus:ring-brutal-blue"
                >
                  Sign In
                </button>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden p-3 border-2 sm:border-4 border-black bg-white hover:bg-brutal-gray-50 focus:outline-none focus:ring-4 focus:ring-brutal-blue min-w-[44px] min-h-[44px]"
              aria-label="Toggle mobile menu"
              aria-expanded={isMobileMenuOpen}
            >
              <div className="w-6 h-6 flex flex-col justify-center gap-1">
                <span className={`block h-1 bg-black transition-transform ${isMobileMenuOpen ? 'rotate-45 translate-y-2' : ''}`} />
                <span className={`block h-1 bg-black transition-opacity ${isMobileMenuOpen ? 'opacity-0' : ''}`} />
                <span className={`block h-1 bg-black transition-transform ${isMobileMenuOpen ? '-rotate-45 -translate-y-2' : ''}`} />
              </div>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t-2 sm:border-t-4 border-black bg-white animate-slide-in max-h-[calc(100vh-4rem)] overflow-y-auto">
            <div className="px-4 py-4 space-y-3">
              {/* Features Section */}
              <div>
                <button
                  onClick={() => setIsFeaturesOpen(!isFeaturesOpen)}
                  className="w-full text-left px-4 py-3 font-bold uppercase text-sm border-2 sm:border-4 border-black bg-brutal-gray-50 min-h-[44px]"
                  aria-expanded={isFeaturesOpen}
                >
                  Features ▼
                </button>
                {isFeaturesOpen && (
                  <div className="mt-2 space-y-2 pl-2 sm:pl-4">
                    {features.map((feature) => (
                      <Link
                        key={feature.href}
                        href={feature.href}
                        className="block p-3 border-2 border-black hover:bg-brutal-gray-50 min-h-[44px] flex items-center"
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-xl">{feature.icon}</span>
                          <span className="font-bold text-sm">{feature.name}</span>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </div>

              <Link
                href="/about"
                className="block px-4 py-3 font-bold uppercase text-sm border-2 sm:border-4 border-black hover:bg-brutal-gray-50 min-h-[44px] flex items-center"
              >
                About
              </Link>

              {adminStatus.isAdmin && (
                <Link
                  href="/admin"
                  className="block px-4 py-3 font-bold uppercase text-sm border-2 sm:border-4 border-black hover:bg-brutal-gray-50 min-h-[44px] flex items-center"
                >
                  Admin
                </Link>
              )}

              {/* Authentication */}
              {session ? (
                <>
                  <Link
                    href="/profile"
                    className="block px-4 py-3 font-bold uppercase text-sm border-2 sm:border-4 border-black bg-brutal-blue text-white text-center min-h-[44px] flex items-center justify-center"
                  >
                    Profile
                  </Link>
                  <button
                    onClick={() => signOut()}
                    className="w-full px-4 py-3 font-bold uppercase text-sm border-2 sm:border-4 border-black bg-white hover:bg-brutal-gray-50 min-h-[44px]"
                  >
                    Sign Out
                  </button>
                </>
              ) : (
                <button
                  onClick={() => signIn("google")}
                  className="w-full px-4 py-3 font-bold uppercase text-sm border-2 sm:border-4 border-black bg-brutal-blue text-white min-h-[44px]"
                >
                  Sign In
                </button>
              )}
            </div>
          </div>
        )}
      </nav>
    </>
  );
}
