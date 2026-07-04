import { lazy, ReactNode, Suspense, useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import {
  ArrowUpRight,
  BrainCircuit,
  CheckCircle2,
  Database,
  FileText,
  Github,
  Linkedin,
  Mail,
  Microscope,
  Radar,
  ShieldCheck,
  Stethoscope,
  Workflow,
} from 'lucide-react';

const avatarSrc = '/assets/tarek-avatar-3d-v1.webp';
const LabScene = lazy(() => import('./components/LabScene'));

const proofMetrics = [
  { value: '3971', label: 'reviewed responses', note: 'ClinMAP-VOI v0 hosted benchmark; human domain review complete' },
  { value: '17', label: 'models scored', note: 'Decision accuracy and metamorphic pass rates in public metrics report' },
  { value: '280', label: 'metamorphic relations', note: 'Pairwise behavior constraints across synthetic decision families' },
  { value: '0', label: 'private-source examples', note: 'Synthetic probes only; no patient data or client rubrics' },
];

const systemLayers = [
  {
    title: 'Case probes',
    body: 'Healthcare-domain prompts designed to expose false reassurance, escalation gaps, missing context, and unsupported certainty.',
    icon: <FileText />,
  },
  {
    title: 'Rubric rules',
    body: 'Score anchors, cap rules, severity labels, and reviewer instructions that turn judgment into repeatable criteria.',
    icon: <Workflow />,
  },
  {
    title: 'Review records',
    body: 'Structured scoring fields, rationales, failure tags, and review records for auditability.',
    icon: <Database />,
  },
  {
    title: 'Analysis outputs',
    body: 'Agreement checks, dimension summaries, failure-frequency reporting, limitations, and reproducible run logs.',
    icon: <Radar />,
  },
];

const methods = [
  ['Evaluation design', 'Define the test surface: risk pattern, prompt context, expected safe behavior, failure tags, scoring dimensions, and review protocol.'],
  ['Clinical safety review', 'Apply dental/health-domain judgment to spot unsafe reassurance, missing escalation, medication-context gaps, and scope overreach.'],
  ['Rubric calibration', 'Convert ambiguous review decisions into score anchors, cap rules, adjudication notes, and reusable reviewer guidance.'],
  ['Response ranking', 'Compare outputs by safety, evidence alignment, uncertainty handling, usefulness, and rationale faithfulness.'],
  ['Metamorphic consistency', 'Check whether model policy behavior moves correctly when decisive facts change and stays stable under nuisance shifts.'],
  ['Reproducibility', 'Run manifests, corpus hashes, validation scripts, metrics, and audit gates—inspectable without private data.'],
];

const evidenceCards = [
  {
    number: '01',
    title: 'Clinical triage risk',
    category: 'Safety boundary',
    href: './cases/01_false_reassurance_triage.md',
    signal: 'Tests whether the model under-escalates risk when the prompt sounds ordinary but contains red-flag context.',
    tags: ['false reassurance', 'escalation omission', 'severity cap'],
    icon: <ShieldCheck />,
  },
  {
    number: '02',
    title: 'Dental medication context',
    category: 'Domain constraints',
    href: './cases/02_dental_medication_context.md',
    signal: 'Checks whether the response avoids unsafe certainty when oral-health, medication, or contraindication context is missing.',
    tags: ['medication context', 'scope control', 'missing history'],
    icon: <Stethoscope />,
  },
  {
    number: '03',
    title: 'Public-health misinformation',
    category: 'Evidence quality',
    href: './cases/03_public_health_misinformation.md',
    signal: 'Evaluates uncertainty, evidence strength, population framing, and access constraints without amplifying unsupported claims.',
    tags: ['unsupported claim', 'uncertainty', 'population context'],
    icon: <Microscope />,
  },
  {
    number: '04',
    title: 'Reasoning faithfulness',
    category: 'Auditability',
    href: './cases/04_reasoning_faithfulness_medical_qa.md',
    signal: 'Checks whether the reviewer rationale actually supports the score, failure tags, and preference decision.',
    tags: ['rationale audit', 'score trace', 'calibration'],
    icon: <BrainCircuit />,
  },
];

type FadeInProps = {
  children: ReactNode;
  delay?: number;
  duration?: number;
  x?: number;
  y?: number;
  className?: string;
};

function FadeIn({ children, className }: FadeInProps) {
  return <div className={className}>{children}</div>;
}

function PrimaryButton({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a
      href={href}
      className="inline-flex items-center gap-2 rounded-full bg-[#A95132] px-5 py-3 text-sm font-semibold text-white shadow-[0_10px_28px_rgba(169,81,50,0.18)] transition hover:-translate-y-0.5 hover:bg-[#8F4228]"
    >
      {children}
      <ArrowUpRight size={17} />
    </a>
  );
}

function SecondaryButton({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a
      href={href}
      className="inline-flex items-center gap-2 rounded-full border border-[#303846]/18 bg-white/70 px-5 py-3 text-sm font-semibold text-[#303846] transition hover:-translate-y-0.5 hover:border-[#A95132]/50 hover:bg-white"
    >
      {children}
      <ArrowUpRight size={17} />
    </a>
  );
}

function SectionLabel({ children }: { children: ReactNode }) {
  return <p className="section-label mb-4">{children}</p>;
}

function HeroAvatar() {
  return (
    <motion.div
      className="avatar-stage relative mx-auto h-[360px] w-[280px] sm:h-[430px] sm:w-[340px] lg:h-[500px] lg:w-[400px]"
      animate={{ y: [0, -8, 0], rotateY: [-2, 2, -2] }}
      transition={{ repeat: Infinity, duration: 9, ease: 'easeInOut' }}
      style={{ transformStyle: 'preserve-3d' }}
    >
      <div className="absolute inset-x-[12%] bottom-[8%] top-[14%] rounded-[42%] bg-[#0E2630]/18 blur-[52px]" />
      <div className="avatar-ring absolute left-1/2 top-1/2 h-[78%] w-[78%] -translate-x-1/2 -translate-y-1/2 rounded-full border border-[#A95132]/18" />
      <div className="avatar-ring avatar-ring-2 absolute left-1/2 top-1/2 h-[70%] w-[92%] -translate-x-1/2 -translate-y-1/2 rounded-full border border-[#303846]/14" />
      <div className="avatar-ring avatar-ring-3 absolute left-1/2 top-1/2 h-[88%] w-[60%] -translate-x-1/2 -translate-y-1/2 rounded-full border border-[#A95132]/14" />

      <motion.div
        className="avatar-card absolute left-1/2 top-[51%] h-[88%] w-[100%] -translate-x-1/2 -translate-y-1/2"
        whileHover={{ scale: 1.015, rotateY: 3 }}
        transition={{ type: 'spring', stiffness: 110, damping: 18 }}
      >
        <img src={avatarSrc} alt="3D avatar inspired by Tarek" className="avatar-image h-full w-full scale-[1.08] object-cover object-center" />
        <div className="portrait-glint pointer-events-none absolute inset-0" />
      </motion.div>
    </motion.div>
  );
}

function HeroSection() {
  const nav = [
    ['Snapshot', '#snapshot'],
    ['System', '#system'],
    ['Methods', '#methods'],
    ['Evidence', '#evidence'],
    ['Explorer', '/explorer/'],
    ['Contact', '#contact'],
  ];

  return (
    <section className="relative overflow-hidden bg-[#F7F4EF]">
      <div className="absolute left-0 top-0 h-full w-[5px] bg-[#A95132] sm:left-10" />
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-6 sm:px-10 lg:px-12">
        <FadeIn y={-10}>
          <nav className="flex items-center justify-between border-b border-[#303846]/15 pb-5 text-[0.72rem] font-semibold uppercase tracking-[0.18em] text-[#303846]/70">
            <a href="#top" className="text-[#303846]">Tarek Etman</a>
            <div className="hidden gap-7 md:flex">
              {nav.map(([label, href]) => (
                <a key={label} href={href} className="transition hover:text-[#A95132]">
                  {label}
                </a>
              ))}
            </div>
          </nav>
        </FadeIn>

        <div id="top" className="grid flex-1 items-center gap-10 py-12 lg:grid-cols-[1.02fr_0.98fr] lg:py-16">
          <div>
            <FadeIn>
              <SectionLabel>ClinMAP-VOI v0 · hosted benchmark</SectionLabel>
              <h1 className="max-w-4xl text-[clamp(3rem,8.7vw,7.6rem)] font-black uppercase leading-[0.9] tracking-[-0.04em] text-[#303846]">
                <span className="block">Tarek</span>
                <span className="block">Etman</span>
              </h1>
            </FadeIn>
            <FadeIn delay={0.08}>
              <p className="mt-6 max-w-2xl text-[clamp(1.15rem,2.4vw,2rem)] font-medium leading-snug text-[#303846]">
                I build evaluation systems for healthcare-domain model behavior.
              </p>
              <p className="mt-5 max-w-2xl text-base leading-relaxed text-[#606A72] md:text-lg">
                Metamorphic healthcare probes, hosted multi-model runs, structured human review, relation metrics, and QA audit—with explicit limits on clinical claims.
              </p>
            </FadeIn>
            <FadeIn delay={0.16}>
              <div className="mt-8 flex flex-wrap gap-3">
                <PrimaryButton href="README.md"><FileText size={17} /> ClinMAP README</PrimaryButton>
                <SecondaryButton href="/explorer/"><Radar size={17} /> v1 demo explorer</SecondaryButton>
                <SecondaryButton href="/assets/clinmap_voi_v0_snapshot.pdf"><FileText size={17} /> ClinMAP PDF</SecondaryButton>
                <SecondaryButton href="/assets/evaluation_systems_snapshot_v1.pdf"><FileText size={17} /> v1 demo PDF</SecondaryButton>
                <SecondaryButton href="mailto:dr.tareketman@gmail.com"><Mail size={17} /> Email</SecondaryButton>
              </div>
            </FadeIn>
          </div>

          <FadeIn delay={0.12}>
            <div className="relative rounded-[34px] border border-[#303846]/12 bg-[#FFFFFF]/78 p-4 shadow-[0_28px_90px_rgba(48,56,70,0.12)] backdrop-blur md:p-6">
              <div className="absolute inset-0 overflow-hidden rounded-[34px] opacity-50">
                <Suspense fallback={null}><LabScene /></Suspense>
              </div>
              <div className="relative z-10 rounded-[28px] border border-[#303846]/10 bg-gradient-to-br from-white/76 via-[#F7F4EF]/80 to-[#EDE4DC]/72 p-4">
                <HeroAvatar />
                <div className="mt-2 grid gap-2 border-t border-[#303846]/12 pt-4 text-sm text-[#303846]/72 sm:grid-cols-3">
                  <span>Licensed dentist</span>
                  <span>Global Health MPP</span>
                  <span>Model evaluation</span>
                </div>
              </div>
            </div>
          </FadeIn>
        </div>
      </div>
    </section>
  );
}

function SnapshotSection() {
  return (
    <section id="snapshot" className="bg-white px-6 py-14 sm:px-10 lg:px-12">
      <div className="mx-auto max-w-7xl">
        <FadeIn>
          <div className="grid gap-3 md:grid-cols-4">
            {proofMetrics.map((item, i) => (
              <div key={item.label} className="surface-card p-5">
                <div className="text-[clamp(2.1rem,4vw,3.8rem)] font-black leading-none text-[#A95132]">{item.value}</div>
                <div className="mt-3 text-sm font-semibold uppercase tracking-[0.12em] text-[#303846]">{item.label}</div>
                <div className="mt-3 text-sm leading-relaxed text-[#6D747B]">{item.note}</div>
                <div className="mt-5 h-px bg-[#303846]/12" />
                <div className="mt-3 text-xs font-semibold text-[#303846]/52">0{i + 1}</div>
              </div>
            ))}
          </div>
        </FadeIn>
      </div>
    </section>
  );
}

function SystemSection() {
  return (
    <section id="system" className="bg-[#F7F4EF] px-6 py-20 sm:px-10 lg:px-12">
      <div className="mx-auto grid max-w-7xl gap-10 lg:grid-cols-[0.8fr_1.2fr]">
        <div>
          <FadeIn>
            <SectionLabel>ClinMAP-VOI v0</SectionLabel>
            <h2 className="section-heading">Judgment made inspectable.</h2>
            <p className="mt-5 max-w-xl text-lg leading-relaxed text-[#606A72]">
              Hosted benchmark plus methodology: metamorphic families, review queue, relation annotations, model metrics, QA audit, and bounded claims—not a clinical outcomes study.
            </p>
          </FadeIn>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          {systemLayers.map((layer, i) => (
            <FadeIn key={layer.title} delay={i * 0.05}>
              <div className="surface-card min-h-[220px] p-6">
                <div className="mb-8 flex h-11 w-11 items-center justify-center rounded-2xl bg-[#A95132]/10 text-[#A95132] [&_svg]:h-5 [&_svg]:w-5">{layer.icon}</div>
                <h3 className="text-xl font-black uppercase tracking-[-0.02em] text-[#303846]">{layer.title}</h3>
                <p className="mt-4 text-sm leading-relaxed text-[#667078]">{layer.body}</p>
              </div>
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}

function MethodsSection() {
  return (
    <section id="methods" className="bg-white px-6 py-20 sm:px-10 lg:px-12">
      <div className="mx-auto max-w-6xl">
        <FadeIn>
          <SectionLabel>Evaluation methods</SectionLabel>
          <h2 className="section-heading max-w-4xl">Designed for review, calibration, and reproducibility.</h2>
        </FadeIn>
        <div className="mt-12 divide-y divide-[#303846]/12 border-y border-[#303846]/12">
          {methods.map(([title, body], i) => (
            <FadeIn key={title} delay={i * 0.04}>
              <div className="grid gap-5 py-7 md:grid-cols-[120px_0.8fr_1.2fr] md:items-start">
                <div className="text-3xl font-black text-[#A95132]">{String(i + 1).padStart(2, '0')}</div>
                <h3 className="text-xl font-black uppercase text-[#303846]">{title}</h3>
                <p className="text-base leading-relaxed text-[#606A72]">{body}</p>
              </div>
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}

function EvidenceCard({ card, index }: { card: (typeof evidenceCards)[number]; index: number }) {
  const ref = useRef<HTMLDivElement | null>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'start start'] });
  const y = useTransform(scrollYProgress, [0, 1], [24, 0]);
  return (
    <motion.article ref={ref} style={{ y }} className="surface-card flex h-full flex-col p-6">
      <div className="flex items-start justify-between gap-5">
        <div>
          <div className="text-sm font-black text-[#A95132]">{card.number}</div>
          <h3 className="mt-4 text-2xl font-black uppercase leading-tight text-[#303846]">{card.title}</h3>
        </div>
        <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-[#0E2630]/8 text-[#0E2630] [&_svg]:h-6 [&_svg]:w-6">{card.icon}</div>
      </div>
      <p className="mt-3 text-xs font-semibold uppercase tracking-[0.16em] text-[#303846]/48">{card.category}</p>
      <p className="mt-5 flex-1 text-sm leading-relaxed text-[#606A72]">{card.signal}</p>
      <div className="mt-6 flex flex-wrap gap-2">
        {card.tags.map((tag) => (
          <span key={tag} className="rounded-full border border-[#303846]/12 px-3 py-1.5 text-xs font-medium text-[#303846]/70">{tag}</span>
        ))}
      </div>
      <a href={card.href} className="mt-7 inline-flex items-center gap-2 text-sm font-semibold text-[#A95132] hover:text-[#8F4228]">
        Open case file <ArrowUpRight size={15} />
      </a>
    </motion.article>
  );
}

function EvidenceSection() {
  return (
    <section id="evidence" className="bg-[#F7F4EF] px-6 py-20 sm:px-10 lg:px-12">
      <div className="mx-auto max-w-7xl">
        <FadeIn>
          <div className="flex flex-col justify-between gap-6 border-b border-[#303846]/12 pb-8 md:flex-row md:items-end">
            <div>
              <SectionLabel>Case evidence</SectionLabel>
              <h2 className="section-heading max-w-4xl">Synthetic v1 demo probes (supporting lineage).</h2>
            </div>
            <SecondaryButton href="/explorer/">Open explorer</SecondaryButton>
          </div>
        </FadeIn>
        <div className="mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {evidenceCards.map((card, index) => (
            <FadeIn key={card.title} delay={index * 0.05}>
              <EvidenceCard card={card} index={index} />
            </FadeIn>
          ))}
        </div>
      </div>
    </section>
  );
}

function BackgroundSection() {
  return (
    <section id="background" className="bg-white px-6 py-20 sm:px-10 lg:px-12">
      <div className="mx-auto grid max-w-7xl gap-10 lg:grid-cols-[0.9fr_1.1fr]">
        <FadeIn>
          <SectionLabel>Background</SectionLabel>
          <h2 className="section-heading">Clinical judgment plus evaluator craft.</h2>
        </FadeIn>
        <FadeIn delay={0.08}>
          <div className="grid gap-4">
            {[
              ['Licensed dentist', 'Domain sensitivity to patient communication, missing context, oral-health constraints, and safety boundaries.'],
              ['Sciences Po Global Health MPP', 'Population context, policy reasoning, evidence review, access constraints, and scientific communication.'],
              ['Medical AI evaluator', 'Hands-on review of medical AI responses, preference rationales, response ranking, QA, and rubric calibration.'],
            ].map(([title, body]) => (
              <div key={title} className="flex gap-4 border-b border-[#303846]/10 pb-5 last:border-b-0">
                <CheckCircle2 className="mt-1 shrink-0 text-[#A95132]" size={20} />
                <div>
                  <h3 className="font-black uppercase text-[#303846]">{title}</h3>
                  <p className="mt-1 text-sm leading-relaxed text-[#606A72]">{body}</p>
                </div>
              </div>
            ))}
          </div>
        </FadeIn>
      </div>
    </section>
  );
}

function ContactSection() {
  return (
    <section id="contact" className="bg-[#303846] px-6 py-16 text-white sm:px-10 lg:px-12">
      <div className="mx-auto flex max-w-7xl flex-col justify-between gap-8 md:flex-row md:items-center">
        <FadeIn>
          <SectionLabel>Contact</SectionLabel>
          <h2 className="max-w-3xl text-[clamp(2.2rem,5vw,5rem)] font-black uppercase leading-[0.95] tracking-[-0.04em]">Open to model evaluation and clinical AI safety work.</h2>
          <p className="mt-5 max-w-2xl text-base leading-relaxed text-white/70">
            Evaluation systems, rubric design, human data quality, healthcare-domain model behavior review, and response-ranking work.
          </p>
        </FadeIn>
        <FadeIn delay={0.08}>
          <div className="flex flex-wrap gap-3 md:justify-end">
            <a href="mailto:dr.tareketman@gmail.com" className="inline-flex items-center gap-2 rounded-full bg-white px-5 py-3 text-sm font-semibold text-[#303846] transition hover:bg-[#F7F4EF]"><Mail size={17} /> Email</a>
            <a href="https://www.linkedin.com/in/tareketman" className="inline-flex items-center gap-2 rounded-full border border-white/20 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/10"><Linkedin size={17} /> LinkedIn</a>
            <a href="/assets/evaluation_systems_snapshot_v1.pdf" className="inline-flex items-center gap-2 rounded-full border border-white/20 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/10"><Github size={17} /> Snapshot</a>
          </div>
        </FadeIn>
      </div>
    </section>
  );
}

export default function App() {
  return (
    <main className="min-h-screen overflow-x-clip bg-[#F7F4EF] font-kanit text-[#303846]">
      <HeroSection />
      <SnapshotSection />
      <SystemSection />
      <MethodsSection />
      <EvidenceSection />
      <BackgroundSection />
      <ContactSection />
    </main>
  );
}
