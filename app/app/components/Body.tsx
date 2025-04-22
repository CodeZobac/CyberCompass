"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { useTranslations } from 'next-intl';
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
    activeColor: "from-blue-500/30 to-purple-500/30",
    key: "deepfakes"
  },
  {
    title: "Disinformation",
    description: "False information deliberately spread mainly in social media to deceive other people",
    icon: "/globe.svg",
    color: "from-amber-500/20 to-orange-500/20",
    activeColor: "from-amber-500/30 to-orange-500/30",
    key: "disinformation"
  },
  {
    title: "Cyberbullying",
    description: "Using digital platforms to harass, threaten, or intimidate others",
    icon: "/window.svg",
    color: "from-red-500/20 to-rose-500/20",
    activeColor: "from-red-500/30 to-rose-500/30",
    key: "cyberbullying"
  },
  {
    title: "Catfishing",
    description: "Creating fake online identities to deceive others into relationships",
    icon: "/window.svg",
    color: "from-emerald-500/20 to-teal-500/20",
    activeColor: "from-emerald-500/30 to-teal-500/30",
    key: "catfishing"
  }
];

export default function Body() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [showDialog, setShowDialog] = useState(false);
  const [statistics, setStatistics] = useState({ users: 0, challenges: 0, success: 0 });
  
  // Translation hooks
  const heroT = useTranslations('hero');
  const statsT = useTranslations('stats');
  const threatsT = useTranslations('threats');
  const howItWorksT = useTranslations('howItWorks');
  const ctaT = useTranslations('cta');
  const dialogT = useTranslations('dialog');
  
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
    }, 3000);
    
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
            {heroT('title')}
          </h1>
          <p className="text-xl text-muted-fg mb-10 max-w-3xl mx-auto">
            {heroT('description')}
          </p>
          <Button 
            size="lg" 
            variant="brutal" 
            onClick={() => setShowDialog(true)}
          >
            {heroT('button')}
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
                <RetroCardDescription className="text-muted-fg">{statsT('usersTrained')}</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
            <RetroCard className="bg-muted/50 backdrop-blur-sm rounded-xl">
              <RetroCardHeader>
                <RetroCardTitle className="text-3xl font-bold text-primary normal-case">{statistics.challenges.toLocaleString()}+</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">{statsT('challengesCompleted')}</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
            <RetroCard className="bg-muted/50 backdrop-blur-sm rounded-xl">
              <RetroCardHeader>
                <RetroCardTitle className="text-3xl font-bold text-success normal-case">{statistics.success}%</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">{statsT('improvedAwareness')}</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
          </div>
        </div>
      </section>

      {/* Threats Section */}
      <section className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold mb-2 text-center">{threatsT('sectionTitle')}</h2>
          <p className="text-muted-fg text-center mb-12 max-w-3xl mx-auto">
            {threatsT('sectionDescription')}
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
                    ${index === activeIndex ? 'ring-2 ring-accent' : ''} `}
                >
                  {/* <div className={`absolute inset-0 bg-gradient-to-br ${threat.color} ${threat.hoverColor} rounded-xl -z-10 transition-all duration-300`}></div>  */}
                  <div
                  className={`absolute inset-0 bg-gradient-to-br 
                    ${index === activeIndex ? threat.activeColor : threat.color} 
                    rounded-xl -z-10 transition-all duration-300`}> 
                  </div>
                  <RetroCardHeader className="pb-0">
                    <div className="bg-muted/50 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                      <Image src={threat.icon} alt={threat.title} width={24} height={24} />
                    </div>
                    <RetroCardTitle className="text-xl font-semibold mb-2 normal-case">
                      {threatsT(`items.${threat.key}.title`)}
                    </RetroCardTitle>
                    <RetroCardDescription className="text-muted-fg text-sm">
                      {threatsT(`items.${threat.key}.description`)}
                    </RetroCardDescription>
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
          <h2 className="text-3xl font-bold mb-2 text-center">{howItWorksT('sectionTitle')}</h2>
          <p className="text-muted-fg text-center mb-12 max-w-3xl mx-auto">
            {howItWorksT('sectionDescription')}
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            <RetroCard className="text-center border-0 bg-transparent">
              <RetroCardHeader className="pb-0">
                <div className="mx-auto w-16 h-16 rounded-full bg-accent/20 flex items-center justify-center mb-4">
                  <span className="text-2xl font-bold text-accent">1</span>
                </div>
                <RetroCardTitle className="text-xl font-semibold mb-2 normal-case">{howItWorksT('steps.step1.title')}</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">{howItWorksT('steps.step1.description')}</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
            <RetroCard className="text-center border-0 bg-transparent">
              <RetroCardHeader className="pb-0">
                <div className="mx-auto w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center mb-4">
                  <span className="text-2xl font-bold text-primary">2</span>
                </div>
                <RetroCardTitle className="text-xl font-semibold mb-2 normal-case">{howItWorksT('steps.step2.title')}</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">{howItWorksT('steps.step2.description')}</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
            <RetroCard className="text-center border-0 bg-transparent">
              <RetroCardHeader className="pb-0">
                <div className="mx-auto w-16 h-16 rounded-full bg-success/20 flex items-center justify-center mb-4">
                  <span className="text-2xl font-bold text-success">3</span>
                </div>
                <RetroCardTitle className="text-xl font-semibold mb-2 normal-case">{howItWorksT('steps.step3.title')}</RetroCardTitle>
                <RetroCardDescription className="text-muted-fg">{howItWorksT('steps.step3.description')}</RetroCardDescription>
              </RetroCardHeader>
            </RetroCard>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">{ctaT('title')}</h2>
          <p className="text-muted-fg mb-10">
            {ctaT('description')}
          </p>
          <Button 
            size="lg" 
            variant="brutal" 
            className="animate-pulse hover:animate-none"
            onClick={() => setShowDialog(true)}
          >
            {ctaT('button')}
          </Button>
        </div>
      </section>

      {/* Challenge Dialog */}
      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>{dialogT('title')}</DialogTitle>
            <DialogDescription>
              {dialogT('description')}
            </DialogDescription>
          </DialogHeader>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 py-4">
            {cyberthreats.map((threat) => (
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
                <h3 className="font-bold mt-2">{threatsT(`items.${threat.key}.title`)}</h3>
                <p className="text-sm text-center text-muted-fg mt-1">{threatsT(`items.${threat.key}.description`)}</p>
              </div>
            ))}
          </div>
          
          <DialogFooter className="flex items-center justify-between border-t border-border pt-4 mt-4">
            <Button variant="brutal-normal" onClick={() => setShowDialog(false)}>
              {dialogT('cancel')}
            </Button>
            <Button variant="brutal">
              {dialogT('random')}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
