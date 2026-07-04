import { ReactNode } from 'react';
import {
  ArrowUpRight,
  FileText,
  Github,
  Linkedin,
  Mail,
  ShieldCheck,
} from 'lucide-react';

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

function Button({ href, children, primary }: { href: string; children: ReactNode; primary?: boolean }) {
  return (
    <a
      href={href}
      target={href.startsWith('http') ? '_blank' : undefined}
      rel="noreferrer"
      className={
        primary
          ? 'inline-flex items-center gap-2 rounded-full bg-[#344551] px-6 py-3 text-sm font-medium text-[#F7F4EF] transition hover:bg-[#42586a]'
          : 'inline-flex items-center gap-2 rounded-full border border-[#344551]/25 px-6 py-3 text-sm font-medium text-[#344551] transition hover:border-[#344551]/50 hover:bg-white/50'
      }
    >
      {children}
    </a>
  );
}

function Label({ children }: { children: ReactNode }) {
  return <p className="section-label mb-4">{children}</p>;
}

export default function App() {
  return (
    <div className="relative dreamwash grain min-h-screen">
      <div className="relative z-10 mx-auto max-w-5xl px-6">
        {/* Nav */}
        <header className="flex items-center justify-between py-8">
          <p className="font-serif-display text-lg font-medium tracking-tight">Tarek Etman</p>
          <nav className="flex items-center gap-5 text-sm text-[#344551]/80">
            <a href="#method" className="hidden hover:text-[#344551] sm:block">Method</a>
            <a href="#evidence" className="hidden hover:text-[#344551] sm:block">Evidence</a>
            <a href="#boundary" className="hidden hover:text-[#344551] sm:block">Limits</a>
            <a href={SITE.repoUrl} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 hover:text-[#344551]">
              <Github size={16} /> GitHub
            </a>
          </nav>
        </header>

        {/* Hero */}
        <section className="pb-20 pt-16 sm:pt-24">
          <Label>ClinMAP-VOI v0 · a healthcare-domain model behavior benchmark</Label>
          <h1 className="font-serif-display max-w-3xl text-4xl font-medium leading-[1.08] tracking-tight text-[#2e3c47] sm:text-6xl">
            The dangerous answer is rarely the wrong one. It is the confident one, given too early.
          </h1>
          <p className="mt-7 max-w-2xl text-base leading-relaxed text-[#344551]/85 sm:text-lg">
            I am a licensed dentist and Sciences Po Global Health MPP who evaluates medical AI for a living.
            After reviewing 850+ responses under contract, I built my own benchmark to test the failure mode
            the clinic taught me to fear. Then I audited my own reviewing, and published what the audit found.
          </p>
          <div className="mt-9 flex flex-wrap gap-3">
            <Button href={SITE.pdf} primary><FileText size={16} /> Read the 2-page snapshot</Button>
            <Button href={SITE.repoUrl}><Github size={16} /> Inspect the repo</Button>
            <Button href={SITE.linkedIn}><Linkedin size={16} /> LinkedIn</Button>
          </div>
        </section>

        {/* Stats */}
        <section className="rule grid grid-cols-2 gap-x-8 py-10 lg:grid-cols-4">
          {STATS.map((s) => (
            <div key={s.label} className="py-3">
              <p className="font-serif-display text-4xl font-medium text-[#A95F37]">{s.value}</p>
              <p className="mt-2 text-xs leading-relaxed text-[#344551]/70">{s.label}</p>
            </div>
          ))}
        </section>

        {/* What this is */}
        <section className="rule py-20">
          <Label>What this is</Label>
          <div className="grid gap-10 lg:grid-cols-2">
            <h2 className="font-serif-display text-3xl font-medium leading-snug tracking-tight sm:text-4xl">
              Expert review, made inspectable.
            </h2>
            <div className="space-y-5 text-[15px] leading-relaxed text-[#344551]/85">
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
        <section id="method" className="rule py-20">
          <Label>How it works</Label>
          <h2 className="font-serif-display mb-12 max-w-xl text-3xl font-medium leading-snug tracking-tight sm:text-4xl">
            Four stages. Every one of them leaves evidence.
          </h2>
          <div className="grid gap-5 sm:grid-cols-2">
            {METHOD.map((m) => (
              <div key={m.step} className="card p-7">
                <p className="section-label">{m.step}</p>
                <h3 className="font-serif-display mt-3 text-xl font-medium">{m.title}</h3>
                <p className="mt-3 text-sm leading-relaxed text-[#344551]/80">{m.body}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Vignette */}
        <section className="rule py-20">
          <Label>From the disagreement record</Label>
          <div className="card p-8 sm:p-10">
            <div className="flex items-start gap-4">
              <ShieldCheck className="mt-1 shrink-0 text-[#A95F37]" size={22} />
              <div>
                <p className="font-serif-display text-xl font-medium leading-relaxed sm:text-2xl">
                  Two blinded reviewers read the same safe-looking answer and disagreed. Not about whether it was
                  unsafe, but about how firmly it should have escalated once the user pushed back.
                </p>
                <p className="mt-5 text-sm leading-relaxed text-[#344551]/75">
                  That disagreement is published as a worked vignette, with both readings and the adjudication.
                  A benchmark that hides its hard cases is advertising. This one keeps them on the record,
                  because the hard cases are where evaluation actually lives.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Evidence */}
        <section id="evidence" className="rule py-20">
          <Label>Evidence</Label>
          <h2 className="font-serif-display mb-12 max-w-xl text-3xl font-medium leading-snug tracking-tight sm:text-4xl">
            Check the work. That is the point of it.
          </h2>
          <div className="grid gap-5 sm:grid-cols-2">
            {EVIDENCE.map((e) => (
              <a key={e.title} href={e.href} target="_blank" rel="noreferrer" className="card group p-7 transition hover:-translate-y-0.5">
                <div className="flex items-center justify-between">
                  <p className="section-label">{e.title}</p>
                  <ArrowUpRight size={16} className="text-[#344551]/40 transition group-hover:text-[#A95F37]" />
                </div>
                <p className="font-serif-display mt-3 text-2xl font-medium text-[#A95F37]">{e.stat}</p>
                <p className="mt-3 text-sm leading-relaxed text-[#344551]/80">{e.body}</p>
              </a>
            ))}
          </div>
        </section>

        {/* Boundary */}
        <section id="boundary" className="rule py-20">
          <Label>Claim boundary</Label>
          <div className="grid gap-10 lg:grid-cols-2">
            <h2 className="font-serif-display text-3xl font-medium leading-snug tracking-tight sm:text-4xl">
              What this does not claim.
            </h2>
            <ul className="space-y-4 text-[15px] leading-relaxed text-[#344551]/85">
              {BOUNDARY.map((b) => (
                <li key={b} className="flex gap-3">
                  <span className="mt-[9px] h-1.5 w-1.5 shrink-0 rounded-full bg-[#A95F37]" />
                  {b}
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* About / CTA */}
        <section className="rule py-20">
          <div className="card p-8 sm:p-12">
            <Label>The person behind it</Label>
            <h2 className="font-serif-display max-w-2xl text-3xl font-medium leading-snug tracking-tight sm:text-4xl">
              Five years in a clinic. A public policy degree. And a benchmark that says so.
            </h2>
            <p className="mt-6 max-w-2xl text-[15px] leading-relaxed text-[#344551]/85">
              I practiced dentistry for five years in Cairo, took a Global Health MPP at Sciences Po, and spent the
              last year evaluating medical AI under contract: 850+ responses reviewed, 94% of my rationales adopted
              without revision. ClinMAP is the part of the work I can show you. If you run evaluation, human data,
              or safety review and want someone who treats labels like they carry weight, I would like to talk.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button href={SITE.email} primary><Mail size={16} /> dr.tareketman@gmail.com</Button>
              <Button href={SITE.linkedIn}><Linkedin size={16} /> LinkedIn</Button>
              <Button href={SITE.repoUrl}><Github size={16} /> GitHub</Button>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="flex flex-col items-start justify-between gap-3 py-10 text-xs text-[#344551]/60 sm:flex-row sm:items-center">
          <p>Tarek Etman · Licensed dentist · Global Health MPP · Clinical AI evaluation</p>
          <p>Synthetic benchmark · not clinical validation · ClinMAP-VOI v0</p>
        </footer>
      </div>
    </div>
  );
}
