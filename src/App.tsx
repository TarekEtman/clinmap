import { lazy, ReactNode, Suspense, useEffect } from 'react';
import { ArrowUpRight, FileText, Github, Linkedin, Mail } from 'lucide-react';
import Mark from './components/Mark';

const LatticeScene = lazy(() => import('./components/LatticeScene'));

/** Repo URL used by the landing page; verify after publishing/deploying. */
const SITE = {
  repoUrl: 'https://github.com/TarekEtman/clinmap',
  linkedIn: 'https://www.linkedin.com/in/tareketman',
  email: 'mailto:dr.tareketman@gmail.com',
  pdf: '/assets/clinmap_voi_v0_snapshot.pdf',
};

const STATS: Array<{ value: string; label: string }> = [
  { value: '3,971', label: 'responses reviewed, one at a time, by a licensed clinician' },
  { value: '17', label: 'models scored across hosted providers under one frozen run ID' },
  { value: '3,219', label: 'metamorphic relation annotations with oracle labels' },
  { value: 'PASS', label: 'post-review QA audit, including the gates that could have failed' },
];

const METHOD: Array<{ step: string; title: string; body: string }> = [
  {
    step: '01',
    title: 'Design the probes',
    body:
      '40 synthetic clinical decision families, 320 prompt variants, 280 metamorphic relations. Each relation is a promise: if the model understood the first case, its answer to the paired case must move in a known direction.',
  },
  {
    step: '02',
    title: 'Run the models',
    body:
      'Hosted collection across 17 models, deduplicated into a frozen corpus with a versioned run ID and SHA256 hash. The corpus you can download is the corpus that was reviewed.',
  },
  {
    step: '03',
    title: 'Review like it matters',
    body:
      'Every one of the 3,971 responses got a policy label, six dimension scores, and evidence spans tied to the text. Rubrics decide, not mood. Hard calls went to a written adjudication trail.',
  },
  {
    step: '04',
    title: 'Audit the reviewer',
    body:
      'A blind protocol QC pass agreed with the primary review at kappa 0.84. An independent external panel re-coded 720 holdout items. Where they disagreed, the disagreements were published as worked vignettes rather than smoothed over.',
  },
];

const EVIDENCE: Array<{ title: string; stat: string; body: string; href: string }> = [
  {
    title: 'QA audit',
    stat: 'PASS',
    body: 'Frozen artifact verification: holdout accuracy, kappa against blind protocol QC, relation integrity 1.00, majority-agreement gates.',
    href: SITE.pdf,
  },
  {
    title: 'Model metrics',
    stat: '17 models',
    body: 'Decision accuracy and metamorphic pass rate per model, reproducible from the frozen queue with one make target.',
    href: SITE.pdf,
  },
  {
    title: 'Holdout panel',
    stat: '720 items',
    body: 'Two independent external reviewers re-coded unseen families. Their agreement, and their disagreement, are both in the record.',
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
    const els = document.querySelectorAll('.reveal');
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('is-in');
            io.unobserve(e.target);
          }
        }),
      { threshold: 0.14 }
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);
}

function Button({ href, children, primary }: { href: string; children: ReactNode; primary?: boolean }) {
  return (
    <a
      href={href}
      target={href.startsWith('http') ? '_blank' : undefined}
      rel="noreferrer"
      className={
        primary
          ? 'inline-flex items-center gap-2 rounded-full bg-[#344551] px-7 py-3.5 text-sm font-medium text-[#F7F4EF] transition-all duration-300 hover:bg-[#A95F37] hover:shadow-[0_18px_40px_rgba(169,95,55,0.28)]'
          : 'inline-flex items-center gap-2 rounded-full border border-[#344551]/25 px-7 py-3.5 text-sm font-medium text-[#344551] transition-all duration-300 hover:border-[#344551] hover:bg-white/60'
      }
    >
      {children}
    </a>
  );
}

function Label({ children }: { children: ReactNode }) {
  return <p className="section-label mb-5">{children}</p>;
}

export default function App() {
  useReveal();
  return (
    <div className="relative dreamwash grain min-h-screen">
      {/* Nav */}
      <header className="fixed inset-x-0 top-0 z-50 border-b border-[#344551]/10 bg-[#F7F4EF]/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <a href="#top" className="flex items-center gap-3">
            <Mark size={30} />
            <span className="font-serif-display text-lg font-medium tracking-tight">Tarek Etman</span>
          </a>
          <nav className="flex items-center gap-6 text-sm text-[#344551]/75">
            <a href="#method" className="hidden transition hover:text-[#344551] sm:block">Method</a>
            <a href="#evidence" className="hidden transition hover:text-[#344551] sm:block">Evidence</a>
            <a href="#boundary" className="hidden transition hover:text-[#344551] sm:block">Limits</a>
            <a
              href={SITE.pdf}
              className="rounded-full bg-[#344551] px-5 py-2 text-[#F7F4EF] transition-all duration-300 hover:bg-[#A95F37]"
            >
              Read the snapshot
            </a>
          </nav>
        </div>
      </header>

      <div id="top" className="relative z-10 mx-auto max-w-6xl px-6">
        {/* Hero */}
        <section className="relative flex min-h-screen items-center pt-24">
          <div className="lattice-wrap pointer-events-none absolute inset-y-0 right-[-14%] -z-10 w-[68%] opacity-90 max-lg:right-[-30%] max-lg:w-full max-lg:opacity-35">
            <Suspense fallback={null}>
              <LatticeScene />
            </Suspense>
          </div>
          <div className="max-w-3xl pb-24">
            <Label>ClinMAP-VOI v0 · a healthcare-domain model behavior benchmark</Label>
            <h1 className="font-serif-display text-5xl font-medium leading-[1.04] tracking-tight text-[#2e3c47] sm:text-7xl">
              The dangerous answer is rarely the wrong one.
            </h1>
            <p className="font-serif-display mt-6 text-2xl leading-snug text-[#A95F37] sm:text-3xl">
              It is the confident one, given too early.
            </p>
            <p className="mt-8 max-w-xl text-base leading-relaxed text-[#344551]/85 sm:text-lg">
              I am a licensed dentist and Sciences Po Global Health MPP who evaluates medical AI for a living.
              After reviewing 850+ responses under contract, I built my own benchmark to test the failure mode
              the clinic taught me to fear. Then I audited my own reviewing, and published what the audit found.
            </p>
            <div className="mt-10 flex flex-wrap gap-3">
              <Button href={SITE.pdf} primary><FileText size={16} /> Read the 2-page snapshot</Button>
              <Button href={SITE.repoUrl}><Github size={16} /> Inspect the repo</Button>
              <Button href={SITE.linkedIn}><Linkedin size={16} /> LinkedIn</Button>
            </div>
          </div>
        </section>

        {/* Stats */}
        <section className="rule grid grid-cols-2 gap-x-10 py-14 lg:grid-cols-4">
          {STATS.map((s, i) => (
            <div key={s.label} className="reveal py-4" style={{ transitionDelay: `${i * 90}ms` }}>
              <p className="font-serif-display text-5xl font-medium text-[#A95F37] sm:text-6xl">{s.value}</p>
              <p className="mt-3 text-xs leading-relaxed text-[#344551]/70">{s.label}</p>
            </div>
          ))}
        </section>

        {/* What this is */}
        <section className="rule py-24 sm:py-32">
          <div className="grid gap-12 lg:grid-cols-2">
            <div className="reveal">
              <Label>What this is</Label>
              <h2 className="font-serif-display text-4xl font-medium leading-tight tracking-tight sm:text-5xl">
                Expert review, made inspectable.
              </h2>
            </div>
            <div className="reveal space-y-6 text-[16px] leading-relaxed text-[#344551]/85">
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
        <section id="method" className="rule py-24 sm:py-32">
          <div className="reveal">
            <Label>How it works</Label>
            <h2 className="font-serif-display mb-16 max-w-2xl text-4xl font-medium leading-tight tracking-tight sm:text-5xl">
              Four stages. Every one of them leaves evidence.
            </h2>
          </div>
          <div>
            {METHOD.map((m) => (
              <div key={m.step} className="reveal rule grid gap-4 py-10 sm:grid-cols-12 sm:gap-8">
                <p className="font-serif-display text-2xl text-[#A95F37]/70 sm:col-span-1">{m.step}</p>
                <h3 className="font-serif-display text-2xl font-medium sm:col-span-4">{m.title}</h3>
                <p className="text-[15px] leading-relaxed text-[#344551]/80 sm:col-span-7">{m.body}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Vignette */}
        <section className="rule py-24 sm:py-32">
          <div className="reveal mx-auto max-w-4xl text-center">
            <div className="mb-8 flex justify-center"><Mark size={44} /></div>
            <Label>From the disagreement record</Label>
            <p className="font-serif-display text-3xl font-medium leading-snug text-[#2e3c47] sm:text-4xl">
              Two blinded reviewers read the same safe-looking answer and disagreed. Not about whether it was
              unsafe, but about how firmly it should have escalated once the user pushed back.
            </p>
            <p className="mx-auto mt-8 max-w-2xl text-[15px] leading-relaxed text-[#344551]/75">
              That disagreement is published as a worked vignette, with both readings and the adjudication.
              A benchmark that hides its hard cases is advertising. This one keeps them on the record,
              because the hard cases are where evaluation actually lives.
            </p>
          </div>
        </section>

        {/* Evidence */}
        <section id="evidence" className="rule py-24 sm:py-32">
          <div className="reveal">
            <Label>Evidence</Label>
            <h2 className="font-serif-display mb-14 max-w-xl text-4xl font-medium leading-tight tracking-tight sm:text-5xl">
              Check the work. That is the point of it.
            </h2>
          </div>
          <div className="grid gap-5 sm:grid-cols-2">
            {EVIDENCE.map((e, i) => (
              <a
                key={e.title}
                href={e.href}
                target="_blank"
                rel="noreferrer"
                className="card reveal group p-8 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_26px_60px_rgba(52,69,81,0.12)]"
                style={{ transitionDelay: `${i * 70}ms` }}
              >
                <div className="flex items-center justify-between">
                  <p className="section-label">{e.title}</p>
                  <ArrowUpRight size={17} className="text-[#344551]/40 transition group-hover:text-[#A95F37]" />
                </div>
                <p className="font-serif-display mt-4 text-3xl font-medium text-[#A95F37]">{e.stat}</p>
                <p className="mt-4 text-sm leading-relaxed text-[#344551]/80">{e.body}</p>
              </a>
            ))}
          </div>
        </section>

        {/* Boundary */}
        <section id="boundary" className="rule py-24 sm:py-32">
          <div className="grid gap-12 lg:grid-cols-2">
            <div className="reveal">
              <Label>Claim boundary</Label>
              <h2 className="font-serif-display text-4xl font-medium leading-tight tracking-tight sm:text-5xl">
                What this does not claim.
              </h2>
            </div>
            <ul className="reveal space-y-5 text-[16px] leading-relaxed text-[#344551]/85">
              {BOUNDARY.map((b) => (
                <li key={b} className="flex gap-4">
                  <span className="mt-[10px] h-1.5 w-1.5 shrink-0 rounded-full bg-[#A95F37]" />
                  {b}
                </li>
              ))}
            </ul>
          </div>
        </section>
      </div>

      {/* About / CTA — dark stone panel */}
      <section className="relative z-10 bg-[#2e3c47] py-28 text-[#F7F4EF]">
        <div className="mx-auto max-w-6xl px-6">
          <div className="reveal max-w-3xl">
            <div className="mb-8"><Mark size={40} ink="#F7F4EF" rust="#c97a4a" /></div>
            <p className="section-label !text-[#c97a4a]">The person behind it</p>
            <h2 className="font-serif-display mt-5 text-4xl font-medium leading-tight tracking-tight sm:text-5xl">
              Five years in a clinic. A public policy degree. And a benchmark that says so.
            </h2>
            <p className="mt-8 max-w-2xl text-[16px] leading-relaxed text-[#F7F4EF]/80">
              I practiced dentistry for five years in Cairo, took a Global Health MPP at Sciences Po, and spent the
              last year evaluating medical AI under contract: 850+ responses reviewed, 94% of my rationales adopted
              without revision. ClinMAP is the part of the work I can show you. If you run evaluation, human data,
              or safety review and want someone who treats labels like they carry weight, I would like to talk.
            </p>
            <div className="mt-10 flex flex-wrap gap-3">
              <a href={SITE.email} className="inline-flex items-center gap-2 rounded-full bg-[#F7F4EF] px-7 py-3.5 text-sm font-semibold text-[#2e3c47] transition-all duration-300 hover:bg-[#c97a4a] hover:text-[#F7F4EF]">
                <Mail size={16} /> dr.tareketman@gmail.com
              </a>
              <a href={SITE.linkedIn} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 rounded-full border border-[#F7F4EF]/30 px-7 py-3.5 text-sm font-medium text-[#F7F4EF] transition-all duration-300 hover:border-[#F7F4EF] hover:bg-white/10">
                <Linkedin size={16} /> LinkedIn
              </a>
              <a href={SITE.repoUrl} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 rounded-full border border-[#F7F4EF]/30 px-7 py-3.5 text-sm font-medium text-[#F7F4EF] transition-all duration-300 hover:border-[#F7F4EF] hover:bg-white/10">
                <Github size={16} /> GitHub
              </a>
            </div>
          </div>
          <div className="mt-16 flex flex-col items-start justify-between gap-3 border-t border-white/15 pt-8 text-xs text-[#F7F4EF]/55 sm:flex-row sm:items-center">
            <p>Tarek Etman · Licensed dentist · Global Health MPP · Clinical AI evaluation</p>
            <p>Synthetic benchmark · not clinical validation · ClinMAP-VOI v0</p>
          </div>
        </div>
      </section>
    </div>
  );
}
