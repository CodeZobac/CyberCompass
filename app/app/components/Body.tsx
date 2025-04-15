/* eslint-disable react/no-unescaped-entities */
"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { Button } from "./ui/button";
import { Dialog } from "./ui/dialog";
import { motion } from "framer-motion";

const cyberthreats = [
  {
    title: "Deepfakes",
    description: "AI-generated content that can convincingly impersonate real people",
    icon: "/file.svg",
    color: "from-blue-500/20 to-purple-500/20",
    hoverColor: "group-hover:from-blue-500/30 group-hover:to-purple-500/30"
  },
  {
    title: "Disinformation",
    description: "False information deliberately spread to deceive people",
    icon: "/globe.svg",
    color: "from-amber-500/20 to-orange-500/20",
    hoverColor: "group-hover:from-amber-500/30 group-hover:to-orange-500/30"
  },
  {
    title: "Cyberbullying",
    description: "Using digital platforms to harass, threaten, or intimidate others",
    icon: "/window.svg",
    color: "from-red-500/20 to-rose-500/20",
    hoverColor: "group-hover:from-red-500/30 group-hover:to-rose-500/30"
  },
  {
    title: "Catfishing",
    description: "Creating fake online identities to deceive others into relationships",
    icon: "/window.svg",
    color: "from-emerald-500/20 to-teal-500/20",
    hoverColor: "group-hover:from-emerald-500/30 group-hover:to-teal-500/30"
  }
];

export default function Body() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [showDialog, setShowDialog] = useState(false);
  const [statistics, setStatistics] = useState({ users: 0, challenges: 0, success: 0 });
  
  // Animate counter
  useEffect(() => {
    const interval = setInterval(() => {
      setStatistics(prev => ({
        users: prev.users < 10000 ? prev.users + 100 : prev.users,
        challenges: prev.challenges < 25000 ? prev.challenges + 250 : prev.challenges,
        success: prev.success < 85 ? prev.success + 1 : prev.success
      }));
    }, 30);
    
    return () => clearInterval(interval);
  }, []);
  
  // Rotate through threats
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveIndex(prevIndex => (prevIndex + 1) % cyberthreats.length);
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-bg to-accent/5">
      {/* Hero Section */}
      <section className="relative py-20 px-6 flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-accent to-primary bg-clip-text text-transparent">
            Test Your Digital Resilience in a Safe Environment
          </h1>
          <p className="text-xl text-muted-fg mb-10 max-w-3xl mx-auto">
            Experience real-world cyber threats in a controlled environment. 
            Learn to identify and defend against deepfakes, disinformation, 
            cyberbullying, and catfishing attacks.
          </p>
          <Button 
            size="large" 
            intent="primary" 
            className="animate-pulse hover:animate-none"
            onClick={() => setShowDialog(true)}
          >
            Start Your Cyber Challenge
          </Button>
        </motion.div>
        
        {/* Floating graphics */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 opacity-70">
          <div className="absolute top-20 left-20 w-40 h-40 bg-accent/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-40 right-20 w-60 h-60 bg-primary/10 rounded-full blur-3xl"></div>
          <div className="absolute top-60 right-40 w-20 h-20 bg-warning/20 rounded-full blur-xl"></div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-muted/50 backdrop-blur-sm p-6 rounded-xl border border-border">
              <h3 className="text-3xl font-bold text-accent mb-2">{statistics.users.toLocaleString()}+</h3>
              <p className="text-muted-fg">Users trained</p>
            </div>
            <div className="bg-muted/50 backdrop-blur-sm p-6 rounded-xl border border-border">
              <h3 className="text-3xl font-bold text-primary mb-2">{statistics.challenges.toLocaleString()}+</h3>
              <p className="text-muted-fg">Challenges completed</p>
            </div>
            <div className="bg-muted/50 backdrop-blur-sm p-6 rounded-xl border border-border">
              <h3 className="text-3xl font-bold text-success mb-2">{statistics.success}%</h3>
              <p className="text-muted-fg">Improved awareness</p>
            </div>
          </div>
        </div>
      </section>

      {/* Threats Section */}
      <section className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold mb-2 text-center">Cyber Threats You'll Learn to Identify</h2>
          <p className="text-muted-fg text-center mb-12 max-w-3xl mx-auto">
            Our interactive challenges simulate real-world scenarios to help you recognize and respond 
            to today's most common cyber threats.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {cyberthreats.map((threat, index) => (
              <motion.div
                key={threat.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className={`group relative p-6 rounded-xl border border-border cursor-pointer 
                  ${index === activeIndex ? 'ring-2 ring-accent' : ''}`}
                onClick={() => setActiveIndex(index)}
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${threat.color} ${threat.hoverColor} rounded-xl -z-10 transition-all duration-300`}></div>
                <div className="bg-muted/50 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                  <Image src={threat.icon} alt={threat.title} width={24} height={24} />
                </div>
                <h3 className="text-xl font-semibold mb-2">{threat.title}</h3>
                <p className="text-muted-fg text-sm">{threat.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-6 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold mb-2 text-center">How CyberCompass Works</h2>
          <p className="text-muted-fg text-center mb-12 max-w-3xl mx-auto">
            Our platform provides a safe environment to experience and learn from simulated cyber threats.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            <div className="text-center">
              <div className="mx-auto w-16 h-16 rounded-full bg-accent/20 flex items-center justify-center mb-4">
                <span className="text-2xl font-bold text-accent">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Take the Challenge</h3>
              <p className="text-muted-fg">Choose from various scenarios that simulate real-world cyber threats.</p>
            </div>
            <div className="text-center">
              <div className="mx-auto w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center mb-4">
                <span className="text-2xl font-bold text-primary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Test Your Skills</h3>
              <p className="text-muted-fg">Navigate through interactive challenges designed to test your ability to identify threats.</p>
            </div>
            <div className="text-center">
              <div className="mx-auto w-16 h-16 rounded-full bg-success/20 flex items-center justify-center mb-4">
                <span className="text-2xl font-bold text-success">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Learn & Improve</h3>
              <p className="text-muted-fg">Get instant feedback and actionable tips to improve your cyber awareness.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Test Your Cyber Resilience?</h2>
          <p className="text-muted-fg mb-10">
            Join thousands of users who have strengthened their cyber awareness through our interactive challenges.
          </p>
          <Button 
            size="large" 
            intent="primary" 
            className="animate-pulse hover:animate-none"
            onClick={() => setShowDialog(true)}
          >
            Begin Your Journey
          </Button>
        </div>
      </section>

      {/* Challenge Dialog */}
      {showDialog && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50">
          <Dialog className="bg-bg rounded-xl shadow-lg w-full max-w-md mx-4">
            <div className="sm:max-w-md">
              <div className="flex justify-between items-center p-4 border-b border-border">
                <Dialog.Header slot="title" className="text-xl font-semibold">Choose Your Challenge</Dialog.Header>
                <Button 
                  intent="plain" 
                  size="small" 
                  className="rounded-full" 
                  onPress={() => setShowDialog(false)}
                >
                  <span aria-hidden>×</span>
                  <span className="sr-only">Close</span>
                </Button>
              </div>
              <Dialog.Body slot="description" className="p-4 text-muted-fg">
                Select a cyber threat challenge to begin your training in a safe environment.
              </Dialog.Body>
              
              {/* Challenge Options */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4">
                {cyberthreats.map((threat) => (
                  <Button 
                    key={threat.title}
                    intent="outline" 
                    className="justify-start h-auto py-4"
                    onPress={() => window.location.href = `/challenges/${threat.title.toLowerCase()}`}
                  >
                    <div className="flex flex-col items-start text-left">
                      <span className="font-semibold">{threat.title}</span>
                      <span className="text-sm text-muted-fg">{threat.description}</span>
                    </div>
                  </Button>
                ))}
              </div>
              <div className="flex justify-end p-4 border-t border-border">
                <Button 
                  intent="secondary"
                  onPress={() => setShowDialog(false)}
                >
                  Cancel
                </Button>
              </div>
            </div>
          </Dialog>
        </div>
      )}
    </div>
  );
}
