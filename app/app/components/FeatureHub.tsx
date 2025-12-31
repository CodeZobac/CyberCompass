"use client";

import Link from "next/link";
import { useSession } from "next-auth/react";

interface Feature {
  id: string;
  title: string;
  description: string;
  icon: string;
  href: string;
  color: string;
  stats?: {
    label: string;
    value: string;
  };
}

export function FeatureHub() {
  const { data: session } = useSession();

  const features: Feature[] = [
    {
      id: "deepfake",
      title: "DEEPFAKE DETECTION",
      description: "Master the art of spotting manipulated media through interactive challenges",
      icon: "🎭",
      href: "/deepfake-training",
      color: "brutal-red",
      stats: {
        label: "Challenges",
        value: "50+"
      }
    },
    {
      id: "social-media",
      title: "SOCIAL MEDIA SIMULATION",
      description: "Navigate the feed and spot disinformation in realistic scenarios",
      icon: "📱",
      href: "/social-media-sim",
      color: "brutal-blue",
      stats: {
        label: "Scenarios",
        value: "30+"
      }
    },
    {
      id: "catfish",
      title: "CATFISH DETECTION",
      description: "Learn to identify suspicious behavior in online conversations",
      icon: "💬",
      href: "/catfish-training",
      color: "brutal-purple",
      stats: {
        label: "Simulations",
        value: "25+"
      }
    },
    {
      id: "analytics",
      title: "ANALYTICS DASHBOARD",
      description: "Track your progress, achievements, and learning journey",
      icon: "📊",
      href: "/analytics",
      color: "brutal-blue",
      stats: {
        label: "Insights",
        value: "Real-time"
      }
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="border-b-4 sm:border-b-6 border-black bg-gradient-to-b from-brutal-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-24">
          <div className="text-center stagger-container">
            <h1 className="text-3xl sm:text-5xl md:text-7xl lg:text-8xl font-black uppercase mb-4 sm:mb-6 text-black leading-tight">
              AI-POWERED
              <br />
              <span className="text-brutal-red">CYBER TRAINING</span>
            </h1>
            <p className="text-base sm:text-xl md:text-2xl font-bold text-brutal-gray-700 max-w-3xl mx-auto mb-6 sm:mb-8 px-4">
              Build critical thinking skills through interactive AI simulations
            </p>
            <div className="flex flex-wrap justify-center gap-3 sm:gap-4 mb-8 sm:mb-12">
              <div className="px-4 sm:px-6 py-2 sm:py-3 bg-white border-2 sm:border-4 border-black shadow-[4px_4px_0_0_#000] sm:shadow-brutal-md">
                <div className="text-2xl sm:text-3xl font-black text-brutal-blue">4</div>
                <div className="text-xs sm:text-sm font-bold uppercase">AI Features</div>
              </div>
              <div className="px-4 sm:px-6 py-2 sm:py-3 bg-white border-2 sm:border-4 border-black shadow-[4px_4px_0_0_#000] sm:shadow-brutal-md">
                <div className="text-2xl sm:text-3xl font-black text-brutal-green">100+</div>
                <div className="text-xs sm:text-sm font-bold uppercase">Challenges</div>
              </div>
              <div className="px-4 sm:px-6 py-2 sm:py-3 bg-white border-2 sm:border-4 border-black shadow-[4px_4px_0_0_#000] sm:shadow-brutal-md">
                <div className="text-2xl sm:text-3xl font-black text-brutal-purple">∞</div>
                <div className="text-xs sm:text-sm font-bold uppercase">Learning</div>
              </div>
            </div>
            {!session && (
              <div className="flex flex-col sm:flex-row justify-center gap-3 sm:gap-4 px-4">
                <Link
                  href="/auth/signin"
                  className="px-6 sm:px-8 py-3 sm:py-4 font-black uppercase text-base sm:text-lg border-4 sm:border-6 border-black bg-brutal-blue text-white shadow-[6px_6px_0_0_#000] sm:shadow-brutal-lg hover-lift focus:outline-none focus:ring-4 focus:ring-brutal-blue text-center min-h-[44px] flex items-center justify-center"
                >
                  Get Started →
                </Link>
                <Link
                  href="#features"
                  className="px-6 sm:px-8 py-3 sm:py-4 font-black uppercase text-base sm:text-lg border-4 sm:border-6 border-black bg-white hover:bg-brutal-gray-50 shadow-[6px_6px_0_0_#000] sm:shadow-brutal-lg hover-lift focus:outline-none focus:ring-4 focus:ring-brutal-blue text-center min-h-[44px] flex items-center justify-center"
                >
                  Explore Features
                </Link>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-12 sm:py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8 sm:mb-12 lg:mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black uppercase mb-3 sm:mb-4">
              Choose Your Training
            </h2>
            <p className="text-base sm:text-lg md:text-xl font-bold text-brutal-gray-700 px-4">
              Select an AI-powered feature to begin your learning journey
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
            {features.map((feature, index) => (
              <Link
                key={feature.id}
                href={feature.href}
                className="group block bg-white border-4 sm:border-6 border-black shadow-[6px_6px_0_0_#000] sm:shadow-brutal-md hover-lift focus:outline-none focus:ring-4 focus:ring-brutal-blue transition-all duration-200"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="p-4 sm:p-6 lg:p-8">
                  {/* Icon */}
                  <div className="mb-4 sm:mb-6">
                    <div className={`inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 border-2 sm:border-4 border-black bg-${feature.color} shadow-[4px_4px_0_0_#000] sm:shadow-brutal-sm`}>
                      <span className="text-4xl sm:text-5xl">{feature.icon}</span>
                    </div>
                  </div>

                  {/* Title */}
                  <h3 className="text-xl sm:text-2xl md:text-3xl font-black uppercase mb-3 sm:mb-4 group-hover:text-brutal-blue transition-colors leading-tight">
                    {feature.title}
                  </h3>

                  {/* Description */}
                  <p className="text-sm sm:text-base md:text-lg font-semibold text-brutal-gray-700 mb-4 sm:mb-6">
                    {feature.description}
                  </p>

                  {/* Stats */}
                  {feature.stats && (
                    <div className="flex items-center justify-between pt-4 sm:pt-6 border-t-2 sm:border-t-4 border-black">
                      <div>
                        <div className="text-xs sm:text-sm font-bold uppercase text-brutal-gray-700">
                          {feature.stats.label}
                        </div>
                        <div className="text-xl sm:text-2xl font-black text-black">
                          {feature.stats.value}
                        </div>
                      </div>
                      <div className="px-4 sm:px-6 py-2 sm:py-3 border-2 sm:border-4 border-black bg-brutal-blue text-white font-black uppercase text-xs sm:text-sm group-hover:translate-x-1 group-hover:translate-y-1 transition-transform min-h-[44px] flex items-center">
                        Start →
                      </div>
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="border-t-4 sm:border-t-6 border-black bg-gradient-to-b from-white to-brutal-gray-50 py-12 sm:py-16 lg:py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black uppercase mb-4 sm:mb-6">
            Ready to Level Up?
          </h2>
          <p className="text-base sm:text-lg md:text-xl font-bold text-brutal-gray-700 mb-6 sm:mb-8 px-4">
            Join thousands of students building critical digital literacy skills
          </p>
          {session ? (
            <Link
              href="/analytics"
              className="inline-block px-6 sm:px-8 py-3 sm:py-4 font-black uppercase text-base sm:text-lg border-4 sm:border-6 border-black bg-brutal-green text-white shadow-[6px_6px_0_0_#000] sm:shadow-brutal-lg hover-lift focus:outline-none focus:ring-4 focus:ring-brutal-green min-h-[44px] flex items-center justify-center"
            >
              View Your Progress →
            </Link>
          ) : (
            <Link
              href="/auth/signin"
              className="inline-block px-6 sm:px-8 py-3 sm:py-4 font-black uppercase text-base sm:text-lg border-4 sm:border-6 border-black bg-brutal-blue text-white shadow-[6px_6px_0_0_#000] sm:shadow-brutal-lg hover-lift focus:outline-none focus:ring-4 focus:ring-brutal-blue min-h-[44px] flex items-center justify-center"
            >
              Sign Up Now →
            </Link>
          )}
        </div>
      </section>

      {/* Why Choose Section */}
      <section className="py-12 sm:py-16 lg:py-24 border-t-4 sm:border-t-6 border-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black uppercase mb-8 sm:mb-12 text-center">
            Why CyberCompass?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 lg:gap-8">
            <div className="p-4 sm:p-6 lg:p-8 bg-white border-2 sm:border-4 border-black shadow-[4px_4px_0_0_#000] sm:shadow-brutal-md">
              <div className="text-4xl sm:text-5xl mb-3 sm:mb-4">🤖</div>
              <h3 className="text-lg sm:text-xl font-black uppercase mb-2 sm:mb-3">AI-Powered</h3>
              <p className="text-sm sm:text-base font-semibold text-brutal-gray-700">
                Advanced AI creates realistic, adaptive scenarios tailored to your skill level
              </p>
            </div>
            <div className="p-4 sm:p-6 lg:p-8 bg-white border-2 sm:border-4 border-black shadow-[4px_4px_0_0_#000] sm:shadow-brutal-md">
              <div className="text-4xl sm:text-5xl mb-3 sm:mb-4">🎯</div>
              <h3 className="text-lg sm:text-xl font-black uppercase mb-2 sm:mb-3">Interactive</h3>
              <p className="text-sm sm:text-base font-semibold text-brutal-gray-700">
                Learn by doing with hands-on challenges and real-time feedback
              </p>
            </div>
            <div className="p-4 sm:p-6 lg:p-8 bg-white border-2 sm:border-4 border-black shadow-[4px_4px_0_0_#000] sm:shadow-brutal-md">
              <div className="text-4xl sm:text-5xl mb-3 sm:mb-4">📈</div>
              <h3 className="text-lg sm:text-xl font-black uppercase mb-2 sm:mb-3">Track Progress</h3>
              <p className="text-sm sm:text-base font-semibold text-brutal-gray-700">
                Monitor your growth with detailed analytics and achievement systems
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
