"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/layout/Navbar";
import { 
  ArrowRight, 
  Map as MapIcon, 
  Building2, 
  Lightbulb, 
  Scale, 
  GraduationCap, 
  Briefcase 
} from "lucide-react";

export default function LandingPage() {
  const features = [
    { title: "Career Explorer", desc: "Discover 500+ careers based on your interests and aptitudes.", icon: Briefcase },
    { title: "Pathway Generator", desc: "AI-generated step-by-step guides to reach your dream career.", icon: MapIcon },
    { title: "Institution Comparison", desc: "Compare universities, costs, and requirements side-by-side.", icon: Building2 },
    { title: "AI-Powered Insights", desc: "Personalized recommendations for your unique profile.", icon: Lightbulb },
    { title: "Decision Matrix", desc: "Evaluate options objectively based on your priorities.", icon: Scale },
    { title: "Scholarship Finder", desc: "Match with funding opportunities that fit your background.", icon: GraduationCap },
  ];

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      
      {/* Hero */}
      <section className="relative overflow-hidden py-20 lg:py-32 bg-gradient-to-br from-prism-bg to-white dark:from-background dark:to-background">
        <div className="container mx-auto px-4 text-center">
          <motion.h1 
            className="text-5xl md:text-7xl font-bold tracking-tight text-foreground mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            Discover Your <span className="bg-clip-text text-transparent bg-gradient-to-r from-prism-navy to-prism-purple">Perfect Career Path</span>
          </motion.h1>
          <motion.p 
            className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            PRISM-EDU uses AI to match your aptitudes with the best careers, generates personalized educational pathways, and helps you make data-driven decisions for your future.
          </motion.p>
          <motion.div 
            className="flex flex-col sm:flex-row justify-center items-center gap-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Link href="/register">
              <Button size="lg" className="w-full sm:w-auto h-12 px-8 text-lg">
                Get Started <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            <Link href="#features">
              <Button size="lg" variant="outline" className="w-full sm:w-auto h-12 px-8 text-lg">
                Learn More
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-foreground">Everything You Need to Succeed</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, idx) => {
              const Icon = feature.icon;
              return (
                <motion.div 
                  key={idx}
                  className="bg-card p-6 rounded-2xl border shadow-sm hover:shadow-md transition-shadow"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.1 }}
                >
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary mb-4">
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.desc}</p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-20 bg-prism-navy text-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">10K+</div>
              <div className="text-white/80">Students Guided</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">500+</div>
              <div className="text-white/80">Careers Mapped</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">200+</div>
              <div className="text-white/80">Partner Institutions</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">100+</div>
              <div className="text-white/80">Scholarships Found</div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-background border-t">
        <div className="container mx-auto px-4 text-center text-muted-foreground">
          <p>© 2026 PRISM-EDU. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
