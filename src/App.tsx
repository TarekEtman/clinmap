import { ReactNode, useEffect } from 'react';
import { ArrowUpRight } from 'lucide-react';
import Mark from './components/Mark';
import Feather from './components/Feather';

/** Repo URL used by the landing page; verify after publishing/deploying. */
const SITE = {
  repoUrl: 'https://github.com/TarekEtman/clinmap',
  linkedIn: 'https://www.linkedin.com/in/tareketman',
  email: 'mailto:dr.tareketman@gmail.com',
  pdf: '/assets/clinmap_voi_v0_snapshot.pdf',
};

const STATS: Array<{ value: string; label: string }> = [
  { value: '3,971', label: 'responses reviewed, one at a time, by a licensed clinician' },
  { value: '17', label: 'models scored under one frozen run ID and corpus hash' },
  { value: '3,219', label: 'metamorphic relation annotations with oracle labels' },
  { value: 'PASS', label: 'post-review QA audit, including the gates that could have failed' },
];

const METHOD: Array<{ step: string; title: string; body: string }> = [
  {
    step: 'I',
    title: 'Design the probes',
    body:
      '40 synthetic clinical decision families, 320 prompt variants, 280 metamorphic relations. Each relation is a promise: if the model understood the first case, its answer to the paired case must move in a known direction.',
  },
  {
    step: 'II',
    title: 'Run the models',
    body:
      'Hosted collection across 17 models, deduplicated into a frozen corpus with a versioned run ID and SHA256 hash. The corpus you can download is the corpus that was reviewed.',
  },
  {
    step: 'III',
    title: 'Review like it matters',
    body:
      'Every one of the 3,971 responses received a policy label, six dimension scores, and evidence spans tied to the text. Rubrics decide, not mood. Hard calls went to a written adjudication trail.',
  },
  {
    step: 'IV',
    title: 'Audit the reviewer',
    body:
      'A blind protocol QC pass agreed with the primary review at kappa 0.84. An independent external panel re-coded 720 holdout items. Where they disagreed, the disagreements were published as worked vignettes.',
  },
];

const EVIDENCE: Array<{ title: string; stat: string; body: string; href: string }> = [
  {
    title: 'QA audit',
    stat: 'pass',
    body: 'Frozen artifact verification: holdout accuracy, kappa against blind protocol QC, relation integrity 1.00.',
    href: SITE.pdf,
  },
  {
    title: 'Model metrics',
    stat: '17 models',
    body: 'Decision accuracy and metamorphic pass rate per model, reproducible from the frozen queue with one command.',
    href: SITE.pdf,
  },
  {
    title: 'Holdout panel',
    stat: '720 items',
    body: 'Two independent external reviewers re-coded unseen families. Their agreement and their disagreement are both in the record.',
    href: SITE.pdf,
  },
  {
    title: 'Evidence pack',
    stat: 'Wilson CIs',
    body: 'Confidence intervals, discrimination analysis, failure atlas, gold-label independence. Built for reviewers who check.',
    href: SITE.repoUrl,
  },
];

const BOUNDARY: string[] = [
  'Synthetic probes only. No patients, no records, no clinical claims.',
  'This measures model behavior against rubrics and metamorphic consistency. It does not measure patient outcomes.',
  'One primary reviewer with QC layers, not a full multi-human panel. The audit says exactly which is which.',
  'Not a healthcare leaderboard. Rankings hold within this framework and its stated limits.',
];

function useReveal() {
  useEffect(() => {
    const els = document.querySelectorAll('.reveal, .feather-drift');
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('is-in');
            io.unobserve(e.target);
          }
        }),
      { threshold: 0.12 }
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);
}

function TextLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a
      href={href}
      target={href.startsWith('http') ? '_blank' : undefined}
      rel="noreferrer"
      className="group inline-flex items-center gap-1.5 border-b border-[#344551]/30 pb-0.5 text-sm text-[#344551] transition-colors duration-300 hover:border-[#A95F37] hover:text-[#A95F37]"
    >
      {children}
      <ArrowUpRight size={14} className="transition-transform duration-300 group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
    </a>
  );
}

function Label({ children }: { children: ReactNode }) {
  return <p className="section-label mb-6">{children}</p>;
}

/** A feather drifting into a section as it enters the viewport. */
function DriftingFeather({
  size,
  className,
  sway = '9s',
  delay = '0s',
  tint = '#344551',
}: {
  size: number;
  className: string;
  sway?: string;
  delay?: string;
  tint?: string;
}) {
  return (
    <div className={`feather-drift pointer-events-none absolute ${className}`} aria-hidden="true">
      <div className="feather-sway" style={{ animationDuration: sway, animationDelay: delay }}>
        <Feather size={size} tint={tint} />
      </div>
    </div>
  );
}

export default function App() {
  useReveal();
  return (
    <div className="relative min-h-screen overflow-x-clip bg-[#F7F4EF]">
      {/* Nav */}
      <header className="fixed inset-x-0 top-0 z-50 bg-[#F7F4EF]/85 backdrop-blur-sm">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-5">
          <a href="#top" className="flex items-center gap-3">
            <Mark size={26} />
            <span className="font-serif-display text-[17px] font-medium tracking-tight">Tarek Etman</span>
          </a>
          <nav className="flex items-center gap-7 text-[13px] text-[#344551]/70">
            <a href="#method" className="hidden transition-colors hover:text-[#344551] sm:block">Method</a>
            <a href="#evidence" className="hidden transition-colors hover:text-[#344551] sm:block">Evidence</a>
            <a href="#boundary" className="hidden transition-colors hover:text-[#344551] sm:block">Limits</a>
            <a href={SITE.repoUrl} target="_blank" rel="noreferrer" className="transition-colors hover:text-[#344551]">GitHub</a>
          </nav>
        </div>
      </header>

      <main id="top" className="relative z-10 mx-auto max-w-5xl px-6">
        {/* Hero */}
        <section className="relative flex min-h-[92vh] items-center">
          <DriftingFeather size={300} className="right-[2%] top-[16%] hidden lg:block" sway="11s" />
          <DriftingFeather size={130} className="right-[26%] top-[58%] hidden opacity-60 lg:block" sway="14s" delay="1.2s" tint="#7d8b94" />
          <div className="max-w-2xl pt-20">
            <Label>ClinMAP-VOI v0 · a healthcare-domain model behavior benchmark</Label>
            <h1 className="font-serif-display text-[2.9rem] font-medium leading-[1.06] tracking-tight text-[#2e3c47] sm:text-[4.3rem]">
              The dangerous answer is rarely the wrong one.
            </h1>
            <p className="font-serif-display mt-5 text-2xl leading-snug text-[#A95F37] sm:text-[2rem]">
              It is the confident one, given too early.
            </p>
            <p className="mt-9 max-w-xl text-[15.5px] leading-[1.75] text-[#344551]/80">
              I am a licensed dentist and Sciences Po Global Health MPP who evaluates medical AI for a living.
              After reviewing 850+ responses under contract, I built my own benchmark to test the failure mode
              the clinic taught me to fear. Then I audited my own reviewing, and published what the audit found.
            </p>
            <div className="mt-11 flex flex-wrap items-center gap-8">
              <TextLink href={SITE.pdf}>Read the two-page snapshot</TextLink>
              <TextLink href={SITE.repoUrl}>Inspect the repository</TextLink>
            </div>
          </div>
        </section>

        {/* Stats */}
        <section className="rule grid grid-cols-2 gap-x-10 py-16 lg:grid-cols-4">
          {STATS.map((s, i) => (
            <div key={s.label} className="reveal py-3" style={{ transitionDelay: `${i * 90}ms` }}>
              <p className="font-serif-display text-[2.6rem] font-medium leading-none text-[#2e3c47]">{s.value}</p>
              <p className="mt-4 max-w-[24ch] text-[11.5px] leading-[1.7] text-[#344551]/60">{s.label}</p>
            </div>
          ))}
        </section>

        {/* What this is */}
        <section className="rule relative py-28 sm:py-36">
          <DriftingFeather size={110} className="left-[-4%] top-[24%] hidden opacity-50 xl:block" sway="13s" tint="#7d8b94" />
          <div className="grid gap-14 lg:grid-cols-12">
            <div className="reveal lg:col-span-5">
              <Label>What this is</Label>
              <h2 className="font-serif-display text-4xl font-medium leading-[1.12] tracking-tight sm:text-[3.2rem]">
                Expert review, made inspectable.
              </h2>
            </div>
            <div className="reveal space-y-6 text-[15.5px] leading-[1.8] text-[#344551]/80 lg:col-span-7 lg:pt-2">
              <p>
                Plenty of people can tell you a model answer feels unsafe. The hard part is turning that feeling
                into probes, labels, metrics, and an audit trail that a stranger can check without trusting you.
                That is what this project does, end to end.
              </p>
              <p>
                ClinMAP-VOI v0 asks one question with discipline: when a clinical decision quietly changes under
                the surface of a prompt, does the model notice? Escalation timing, missing context, medication risk.
                The cases are synthetic. The judgment applied to them is not.
              </p>
            </div>
          </div>
        </section>

        {/* Method */}
        <section id="method" className="rule relative py-28 sm:py-36">
          <div className="reveal max-w-2xl">
            <Label>How it works</Label>
            <h2 className="font-serif-display mb-6 text-4xl font-medium leading-[1.12] tracking-tight sm:text-[3.2rem]">
              Four stages. Every one leaves evidence.
            </h2>
          </div>
          <div className="mt-10">
            {METHOD.map((m) => (
              <div key={m.step} className="reveal rule grid gap-3 py-12 sm:grid-cols-12 sm:gap-8">
                <p className="font-serif-display text-xl italic text-[#A95F37]/80 sm:col-span-1 sm:pt-1">{m.step}</p>
                <h3 className="font-serif-display text-[1.65rem] font-medium leading-tight sm:col-span-4">{m.title}</h3>
                <p className="text-[15px] leading-[1.8] text-[#344551]/75 sm:col-span-7">{m.body}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Vignette */}
        <section className="rule relative py-28 sm:py-40">
          <DriftingFeather size={150} className="right-[0%] top-[8%] hidden opacity-60 lg:block" sway="12s" />
          <div className="reveal mx-auto max-w-3xl text-center">
            <div className="mb-10 flex justify-center"><Mark size={40} /></div>
            <Label>From the disagreement record</Label>
            <p className="font-serif-display text-[1.9rem] font-medium leading-[1.35] text-[#2e3c47] sm:text-[2.4rem]">
              Two blinded reviewers read the same safe-looking answer and disagreed. Not about whether it was
              unsafe, but about how firmly it should have escalated once the user pushed back.
            </p>
            <p className="mx-auto mt-9 max-w-xl text-[14.5px] leading-[1.8] text-[#344551]/70">
              That disagreement is published as a worked vignette, with both readings and the adjudication.
              A benchmark that hides its hard cases is advertising. This one keeps them on the record,
              because the hard cases are where evaluation actually lives.
            </p>
          </div>
        </section>

        {/* Evidence */}
        <section id="evidence" className="rule py-28 sm:py-36">
          <div className="reveal max-w-2xl">
            <Label>Evidence</Label>
            <h2 className="font-serif-display mb-6 text-4xl font-medium leading-[1.12] tracking-tight sm:text-[3.2rem]">
              Check the work. That is the point of it.
            </h2>
          </div>
          <div className="mt-10">
            {EVIDENCE.map((e) => (
              <a
                key={e.title}
                href={e.href}
                target="_blank"
                rel="noreferrer"
                className="reveal rule group grid gap-2 py-9 transition-colors duration-300 sm:grid-cols-12 sm:items-baseline sm:gap-8"
              >
                <p className="section-label !mb-0 sm:col-span-3">{e.title}</p>
                <p className="font-serif-display text-2xl font-medium text-[#2e3c47] transition-colors duration-300 group-hover:text-[#A95F37] sm:col-span-3">
                  {e.stat}
                </p>
                <p className="text-[14.5px] leading-[1.75] text-[#344551]/70 sm:col-span-5">{e.body}</p>
                <ArrowUpRight
                  size={18}
                  className="hidden justify-self-end text-[#344551]/35 transition-all duration-300 group-hover:-translate-y-1 group-hover:translate-x-1 group-hover:text-[#A95F37] sm:block"
                />
              </a>
            ))}
          </div>
        </section>

        {/* Boundary */}
        <section id="boundary" className="rule relative py-28 sm:py-36">
          <DriftingFeather size={100} className="left-[2%] bottom-[10%] hidden opacity-45 xl:block" sway="15s" tint="#7d8b94" />
          <div className="grid gap-14 lg:grid-cols-12">
            <div className="reveal lg:col-span-5">
              <Label>Claim boundary</Label>
              <h2 className="font-serif-display text-4xl font-medium leading-[1.12] tracking-tight sm:text-[3.2rem]">
                What this does not claim.
              </h2>
            </div>
            <ul className="reveal space-y-6 text-[15.5px] leading-[1.8] text-[#344551]/80 lg:col-span-7 lg:pt-2">
              {BOUNDARY.map((b) => (
                <li key={b} className="rule pt-6 first:border-t-0 first:pt-0">{b}</li>
              ))}
            </ul>
          </div>
        </section>
      </main>

      {/* Closing — stone panel */}
      <section className="relative z-10 bg-[#2e3c47] py-32 text-[#F7F4EF]">
        <div className="mx-auto max-w-5xl px-6">
          <div className="reveal max-w-3xl">
            <div className="mb-10"><Mark size={36} ink="#F7F4EF" rust="#c97a4a" /></div>
            <h2 className="font-serif-display text-4xl font-medium leading-[1.12] tracking-tight sm:text-[3.2rem]">
              Five years in a clinic. A public policy degree. And a benchmark that says so.
            </h2>
            <p className="mt-9 max-w-2xl text-[15.5px] leading-[1.8] text-[#F7F4EF]/75">
              I practiced dentistry for five years in Cairo, took a Global Health MPP at Sciences Po, and spent the
              last year evaluating medical AI under contract: 850+ responses reviewed, 94% of my rationales adopted
              without revision. ClinMAP is the part of the work I can show you. If you run evaluation, human data,
              or safety review and want someone who treats labels like they carry weight, I would like to talk.
            </p>
            <div className="mt-12 flex flex-wrap items-center gap-9 text-sm">
              <a href={SITE.email} className="border-b border-[#F7F4EF]/40 pb-0.5 transition-colors duration-300 hover:border-[#c97a4a] hover:text-[#c97a4a]">
                dr.tareketman@gmail.com
              </a>
              <a href={SITE.linkedIn} target="_blank" rel="noreferrer" className="border-b border-[#F7F4EF]/40 pb-0.5 transition-colors duration-300 hover:border-[#c97a4a] hover:text-[#c97a4a]">
                LinkedIn
              </a>
              <a href={SITE.repoUrl} target="_blank" rel="noreferrer" className="border-b border-[#F7F4EF]/40 pb-0.5 transition-colors duration-300 hover:border-[#c97a4a] hover:text-[#c97a4a]">
                GitHub
              </a>
            </div>
          </div>
          <div className="mt-20 flex flex-col items-start justify-between gap-3 border-t border-white/12 pt-8 text-[11.5px] text-[#F7F4EF]/50 sm:flex-row sm:items-center">
            <p>Tarek Etman · Licensed dentist · Global Health MPP · Clinical AI evaluation</p>
            <p>Synthetic benchmark · not clinical validation · ClinMAP-VOI v0</p>
          </div>
        </div>
      </section>
    </div>
  );
}
