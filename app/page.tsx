"use client"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Github, Linkedin, Twitter, Mail } from "lucide-react"

export default function FounderPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-slate-200 z-50">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="text-xl font-bold text-slate-900">AK</div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#about" className="text-slate-600 hover:text-slate-900 transition-colors">
                About
              </a>
              <a href="#education" className="text-slate-600 hover:text-slate-900 transition-colors">
                Education
              </a>
              <a href="#skills" className="text-slate-600 hover:text-slate-900 transition-colors">
                Skills
              </a>
              <a href="#experience" className="text-slate-600 hover:text-slate-900 transition-colors">
                Experience
              </a>
              <a href="#publications" className="text-slate-600 hover:text-slate-900 transition-colors">
                Publications
              </a>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="icon"><Github className="h-4 w-4" /></Button>
              <Button variant="ghost" size="icon"><Linkedin className="h-4 w-4" /></Button>
              <Button variant="ghost" size="icon"><Twitter className="h-4 w-4" /></Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-slate-900 mb-6 text-balance">Amil Khanzada</h1>
          <p className="text-xl md:text-2xl text-slate-600 mb-8 text-balance">Founder & CEO at Virufy</p>
          <p className="text-lg text-slate-500 max-w-2xl mx-auto text-balance">
            Health AI Leader | Doctoral Researcher, Venture Methodology | Founder at Virufy | One Young World Ambassador
          </p>
        </div>
      </section>


      {/* About Section */}
      <section id="about" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-2 gap-12 items-start md:items-center">
            <div className="flex justify-center md:justify-start">
              <img
                src="/Amil.jpg"
                alt="Amil Khanzada"
                className="w-full max-w-sm rounded-2xl shadow-lg object-cover"
              />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-slate-900 mb-6">About Me</h2>
              <p className="text-slate-600 leading-relaxed mb-6 text-justify">
                I am dedicated to bridging the gap between academic research and real-world impact
                in healthcare AI. As the founder of Virufy, a nonprofit research organization, I lead
                a global team in developing AI to diagnose respiratory diseases from sound. Our work has
                assembled a dataset from over 250,000 patients and has been recognized by Forbes, CNN, and MSN.
              </p>
              <p className="text-slate-600 leading-relaxed mb-6 text-justify">
                My current doctoral research at the University of Fukui formalizes this journey. I am developing
                a practical, evidence-based framework to help academic entrepreneurs transform health AI innovations
                into sustainable, high-impact ventures. This methodology covers the full lifecycle: from using behavioral
                nudges for clinical data acquisition to discovering viable B2G (Business-to-Government) operational models
                through rigorous market validation in regions like the GCC.
              </p>
              <p className="text-slate-600 leading-relaxed mb-6 text-justify">
                As a One Young World Ambassador for Japan and a speaker on global stages, my mission is to build
                cross-border collaborations that leverage technology to solve impossible problems.
              </p>
            </div>
          </div>
        </div>
      </section>




      {/* Education Section */}
      <section id="education" className="py-20 bg-gradient-to-b from-slate-50 to-slate-100">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-4xl font-extrabold text-slate-900 mb-16 text-center animate-fadeIn">
            🎓 Education Journey
          </h2>

          <div className="relative border-l-4 border-slate-300 space-y-12">

            {/* Reusable Education Card */}
            {[
              {
                school: "University of California, Berkeley",
                degree: "MBA / Master of Engineering, Business and Data Science",
                period: "Aug 2021 - Jun 2022",
                desc: "Dual degree program in MBA and M.Eng (Data Science). Took leave after 1 year of study to focus on startup."
              },
              {
                school: "Stanford University",
                degree: "Non-Degree, Artificial Intelligence",
                period: "2020 - 2021",
                desc: `Excelled with A/A+ grades in four graduate courses. Led 50+ students through global projects.
            Courses: CS230 (Deep Learning), CS231n (CNNs), CS329s (ML Systems), PEDS220 (COVID-19 Elective).`,
                extra: "Activities: Lean LaunchPad, COVID-19 Response Innovation Lab, IRB-Approved Clinical Research.",
              },
              {
                school: "University of California, Berkeley",
                degree: "Bachelor’s Degree, Computer Science",
                period: "Completed",
                desc: "Ranked in top 5% for multiple Computer Science and Finance courses. Partially completed Japanese language minor.",
                extra: "Activities: Cal Japan Club.",
              },
              {
                school: "University of Fukui",
                degree: "Doctorate of Engineering, Health AI: From Lab to Real-World Application",
                period: "Oct 2023 - Sep 2026",
                desc: `Thesis: "A Methodological Framework for Commercializing University-Developed Health AI."
            My research uses Virufy as a case study to establish a methodology for academic entrepreneurs.`,
                bullets: [
                  "Data Foundation: Acquired a large-scale clinical dataset using behavioral nudges.",
                  "Organizational Engine: Identified motivation drivers for a global volunteer team.",
                  "Go-to-Market Pivot: Conducted 150+ NSF I-Corps interviews leading to a viable model.",
                  "Additional papers underway."
                ],
                extra: "Activities: Japanese tea ceremony and calligraphy society."
              }
            ].map((edu, i) => (
              <div
                key={i}
                className="relative pl-10 opacity-0 translate-y-6 animate-fadeInUp [animation-delay:0.2s]"
              >
                {/* Timeline Dot */}
                <div className="absolute -left-5 top-4 bg-slate-900 text-white p-2 rounded-full shadow-md">
                  🎓
                </div>

                {/* Card */}
                <div className="p-6 bg-white rounded-2xl shadow-md transition transform hover:shadow-2xl hover:scale-[1.02] duration-300">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                    <div>
                      <h3 className="text-2xl font-semibold text-slate-900">{edu.school}</h3>
                      <p className="text-slate-600">{edu.degree}</p>
                    </div>
                    <span className="px-3 py-1 border rounded-md text-sm text-slate-700 bg-slate-100">
                      {edu.period}
                    </span>
                  </div>
                  <p className="text-slate-700 leading-relaxed">{edu.desc}</p>
                  {edu.bullets && (
                    <ul className="list-disc list-inside mt-2 text-slate-600 space-y-1">
                      {edu.bullets.map((point, idx) => <li key={idx}>{point}</li>)}
                    </ul>
                  )}
                  {edu.extra && (
                    <span className="block mt-3 text-sm text-slate-500">{edu.extra}</span>
                  )}
                </div>
              </div>
            ))}

          </div>
        </div>
      </section>

      <style jsx>{`
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .animate-fadeIn { animation: fadeIn 1s ease-in-out forwards; }
  .animate-fadeInUp { animation: fadeInUp 0.8s ease-out forwards; }
`}</style>



      {/* Skills Section */}
      <section id="skills" className="py-20 bg-gradient-to-b from-slate-100 to-white">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h2 className="text-4xl font-extrabold text-slate-900 mb-16 animate-fadeIn">
            🔑 Areas of Expertise
          </h2>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8 animate-fadeInUp [animation-delay:0.2s] ">
            {[
              {
                icon: "💡",
                title: "Health AI & Generative AI",
                desc: "Building cutting-edge AI solutions for healthcare applications.",
                color: "text-indigo-600",
              },
              {
                icon: "🚀",
                title: "GTM Strategy & Venture Building",
                desc: "Transforming research into sustainable, high-impact ventures.",
                color: "text-pink-600",
              },
              {
                icon: "🔬",
                title: "Clinical Research & Data Privacy",
                desc: "Ensuring ethical data practices and advancing clinical AI adoption.",
                color: "text-blue-600",
              },
              {
                icon: "🌍",
                title: "International Partnerships",
                desc: "Driving collaborations across US, Japan, UAE, and beyond.",
                color: "text-green-600",
              },
              {
                icon: "🤝",
                title: "Nonprofit Leadership",
                desc: "Motivating remote teams and scaling global nonprofit initiatives.",
                color: "text-yellow-600",
              },
            ].map((skill, i, arr) => (
              <div
                key={i}
                className={`p-6 rounded-2xl shadow-md border border-slate-200 bg-slate-50 
    hover:shadow-xl hover:-translate-y-2 transition transform duration-300 group
    ${i >= arr.length - 2 ? "sm:col-span-2 lg:col-span-1 mx-auto" : ""}`}
              >
                <span className={`${skill.color} text-3xl block mb-3 group-hover:scale-110 transform transition`}>
                  {skill.icon}
                </span>
                <h3 className={`text-lg font-semibold mb-2 ${skill.color}`}>{skill.title}</h3>
                <p className="text-slate-600 text-sm">{skill.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>


      {/* Experience Section */}
      <section id="experience" className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-slate-900 mb-12 text-center">Experience</h2>
          <div className="space-y-8">

            {/* Virufy */}
            <Card className="p-6 border-l-4 border-l-blue-500 hover:shadow-lg transition-all duration-300 animate-fadeInUp">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-slate-900">Founder, CEO/CTO – Virufy</h3>
                  <p className="text-slate-600">Nonprofit AI Healthcare Organization</p>
                </div>
                <Badge variant="secondary" className="w-fit">Mar 2020 – Present · 5 yrs 6 mos</Badge>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Virufy is a nonprofit research organization developing a smartphone app to screen for COVID-19 and other respiratory diseases
                through AI breathing sound analysis. Our team comprises 60 partner organizations and 250 volunteers from Stanford, Harvard,
                Berkeley, UW, MIT, and Fortune 50 executive advisors.
              </p>
              <p className="text-slate-600 leading-relaxed mt-2">
                Collected data from 250,000+ patients across 4 countries via IRB-approved clinical studies. Released beta app to 4,500 employees
                in South America (2023). Featured in Forbes, CNN, MSN.
              </p>
              <p className="text-sm text-slate-500 mt-2">
                Skills: Interpersonal Skills · Building Organizational Capability · IT Strategy · EHR · Entrepreneurship · Early-Stage Startups
              </p>
              {/* <a href="https://virufy.org/study" target="_blank" className="text-blue-600 text-sm mt-2 inline-flex items-center hover:underline">
          Virufy's Vision & Call to Action →
        </a> */}
            </Card>

            {/* NSF I-Corps */}
            <Card className="p-6 border-l-4 border-l-green-500 hover:shadow-lg transition-all duration-300 animate-fadeInUp">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-slate-900">Entrepreneurial Lead – National Science Foundation (NSF)</h3>
                  <p className="text-slate-600">I-Corps Fall ’23 Cohort</p>
                </div>
                <Badge variant="secondary" className="w-fit">Oct 2023 – Present · 1 yr 11 mos</Badge>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Leading Virufy’s participation in the NSF I-Corps accelerator, applying Steve Blank’s Lean Launchpad methodology
                to de-risk commercialization pathways.
              </p>
              <p className="text-sm text-slate-500 mt-2">
                Skills: Entrepreneurship · Early-Stage Startups · Building Organizational Capability
              </p>
            </Card>

            {/* One Young World */}
            <Card className="p-6 border-l-4 border-l-purple-500 hover:shadow-lg transition-all duration-300 animate-fadeInUp">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-slate-900">Ambassador (Japan) – One Young World</h3>
                  <p className="text-slate-600">Global Youth Leadership</p>
                </div>
                <Badge variant="secondary" className="w-fit">Oct 2018 – Present · 6 yrs 11 mos</Badge>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Represented Fukui, Japan at the 2018 Hague Summit. Sent delegate speaker to 2021 Munich Summit on behalf of Virufy.
                Engaged in global initiatives for youth-driven change.
              </p>
              <p className="text-sm text-slate-500 mt-2">
                Skills: Early-Stage Startups · Interpersonal Skills
              </p>
            </Card>

            {/* MIT Sandbox */}
            <Card className="p-6 border-l-4 border-l-yellow-500 hover:shadow-lg transition-all duration-300 animate-fadeInUp">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-slate-900">Technical Lead – MIT Sandbox Innovation Fund Program</h3>
                  <p className="text-slate-600">Apprenticeship</p>
                </div>
                <Badge variant="secondary" className="w-fit">Sep 2023 – Jan 2024 · 5 mos</Badge>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Part of a three-student MIT Sloan / EECS team, driving technical innovation and entrepreneurship initiatives.
              </p>
            </Card>

            {/* Pivotal */}
            <Card className="p-6 border-l-4 border-l-red-500 hover:shadow-lg transition-all duration-300 animate-fadeInUp">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-slate-900">Senior Software Engineer – Pivotal</h3>
                  <p className="text-slate-600">Full-time</p>
                </div>
                <Badge variant="secondary" className="w-fit">Apr 2016 – Dec 2019 · 3 yrs 9 mos</Badge>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Rotated across Greenplum Database teams (DevOps, workload management, backend server).
                Pair-programmed with distributed teams in US & China. Spearheaded new internal product.
              </p>
            </Card>

            {/* HP */}
            <Card className="p-6 border-l-4 border-l-slate-500 hover:shadow-lg transition-all duration-300 animate-fadeInUp">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-slate-900">HP – SIEM Security Roles</h3>
                  <p className="text-slate-600">Consultant & Developer</p>
                </div>
                <Badge variant="secondary" className="w-fit">Aug 2012 – Feb 2016 · 3 yrs 7 mos</Badge>
              </div>
              <p className="text-slate-600 leading-relaxed">
                <strong>SIEM Security Consultant:</strong> Deployed and troubleshooted security solutions across APAC.
                <br />
                <strong>ArcSight Software Developer:</strong> Built SmartConnectors for DBs, OSs, firewalls, IPS.
              </p>
            </Card>

            {/* SchoolCity */}
            <Card className="p-6 border-l-4 border-l-orange-500 hover:shadow-lg transition-all duration-300 animate-fadeInUp">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-slate-900">Graphics Software Development Consultant – SchoolCity Inc.</h3>
                </div>
                <Badge variant="secondary" className="w-fit">Dec 2009 – Aug 2012 · 2 yrs 9 mos</Badge>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Architected and implemented backend Optical Mark Recognition (OMR) engine for a web-based assessment tool.
              </p>
            </Card>
          </div>
        </div>
      </section>


      {/* Contact Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-slate-900 mb-8">Let's Connect</h2>
          <p className="text-lg text-slate-600 mb-8 max-w-2xl mx-auto text-balance">
            Interested in collaborating on healthcare AI, discussing entrepreneurship, or learning more about Virufy?
            I'd love to hear from you.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Mail className="h-4 w-4 mr-2" />
              Get in Touch
            </Button>
            <Button variant="outline">
              <Linkedin className="h-4 w-4 mr-2" />
              LinkedIn
            </Button>
            <Button variant="outline">
              <Twitter className="h-4 w-4 mr-2" />
              Twitter
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-slate-200 bg-white">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <p className="text-slate-500">© 2024 Amil Khanzada. Built with passion for healthcare innovation.</p>
        </div>
      </footer>
    </div>
  )
}
