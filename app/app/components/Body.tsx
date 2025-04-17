/* eslint-disable react/no-unescaped-entities */
"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { Button } from "./ui/button";
import { 
  Dialog,
  DialogContent, 
  DialogDescription, 
  DialogFooter, 
  DialogHeader, 
  DialogTitle 
} from "./ui/retrodialog";
import { RetroCard, RetroCardHeader, RetroCardTitle, RetroCardDescription } from "./Card";
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
    description: "False information deliberately spread mainly in social media to deceive other people",
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
            size="lg" 
            variant="brutal" 
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
            <RetroCard className="bg-muted/50 backdrop-blur-sm rounded-xl">
              <RetroCardHeader>
                <RetroCardTitle className="text-3xl font-bold text-accent normal-case">{statistics.users.toLocaleString()}+</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">Users trained</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
            <RetroCard className="bg-muted/50 backdrop-blur-sm rounded-xl">
              <RetroCardHeader>
                <RetroCardTitle className="text-3xl font-bold text-primary normal-case">{statistics.challenges.toLocaleString()}+</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">Challenges completed</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
            <RetroCard className="bg-muted/50 backdrop-blur-sm rounded-xl">
              <RetroCardHeader>
                <RetroCardTitle className="text-3xl font-bold text-success normal-case">{statistics.success}%</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">Improved awareness</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
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
                onClick={() => setActiveIndex(index)}
              >
                <RetroCard 
                  className={`group relative rounded-xl cursor-pointer 
                    ${index === activeIndex ? 'ring-2 ring-accent' : ''}`}
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${threat.color} ${threat.hoverColor} rounded-xl -z-10 transition-all duration-300`}></div>
                  <RetroCardHeader className="pb-0">
                    <div className="bg-muted/50 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                      <Image src={threat.icon} alt={threat.title} width={24} height={24} />
                    </div>
                    <RetroCardTitle className="text-xl font-semibold mb-2 normal-case">{threat.title}</RetroCardTitle>
                    <RetroCardDescription className="text-muted-fg text-sm">{threat.description}</RetroCardDescription>
                  </RetroCardHeader>
                </RetroCard>
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
            <RetroCard className="text-center border-0 bg-transparent">
              <RetroCardHeader className="pb-0">
                <div className="mx-auto w-16 h-16 rounded-full bg-accent/20 flex items-center justify-center mb-4">
                  <span className="text-2xl font-bold text-accent">1</span>
                </div>
                <RetroCardTitle className="text-xl font-semibold mb-2 normal-case">Take the Challenge</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">Choose from various scenarios that simulate real-world cyber threats.</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
            <RetroCard className="text-center border-0 bg-transparent">
              <RetroCardHeader className="pb-0">
                <div className="mx-auto w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center mb-4">
                  <span className="text-2xl font-bold text-primary">2</span>
                </div>
                <RetroCardTitle className="text-xl font-semibold mb-2 normal-case">Test Your Skills</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">Navigate through interactive challenges designed to test your ability to identify threats.</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
            <RetroCard className="text-center border-0 bg-transparent">
              <RetroCardHeader className="pb-0">
                <div className="mx-auto w-16 h-16 rounded-full bg-success/20 flex items-center justify-center mb-4">
                  <span className="text-2xl font-bold text-success">3</span>
                </div>
                <RetroCardTitle className="text-xl font-semibold mb-2 normal-case">Learn & Improve</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">Get instant feedback and actionable tips to improve your cyber awareness.</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
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
            size="lg" 
            variant="brutal" 
            className="animate-pulse hover:animate-none"
            onClick={() => setShowDialog(true)}
          >
            Start Your Cyber Challenge
          </Button>
        </div>
      </section>

      {/* Challenge Dialog */}
      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>Choose Your Challenge</DialogTitle>
            <DialogDescription>
              Select a challenge type to test your cyber awareness skills in different scenarios.
            </DialogDescription>
          </DialogHeader>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 py-4">
            {/* eslint-disable-next-line @typescript-eslint/no-unused-vars */}
            {cyberthreats.map((threat, _index) => (
              <div 
                key={threat.title}
                className="flex flex-col items-center cursor-pointer border-2 border-black p-4 hover:bg-muted/30 transition-colors rounded-sm shadow-[4px_4px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none dark:border-white dark:shadow-[4px_4px_0_0_#fff] dark:hover:shadow-none"
                onClick={() => {
                  setShowDialog(false);
                  // This would redirect to the specific challenge page
                  console.log(`Redirecting to challenge/${threat.title.toLowerCase()}`);
                  // In a real implementation, you would use Next.js router:
                  // router.push(`/challenge/${threat.title.toLowerCase()}`);
                }}
              >
                <div className={`w-12 h-12 rounded-full flex items-center justify-center ${threat.color.split(' ')[0]}`}>
                  <Image src={threat.icon} alt={threat.title} width={24} height={24} />
                </div>
                <h3 className="font-bold mt-2">{threat.title}</h3>
                <p className="text-sm text-center text-muted-fg mt-1">{threat.description}</p>
              </div>
            ))}
          </div>
          
          <DialogFooter className="flex items-center justify-between border-t border-border pt-4 mt-4">
            <Button variant="brutal-normal" onClick={() => setShowDialog(false)}>
              Cancel
            </Button>
            <Button variant="brutal">
              Random Challenge
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
