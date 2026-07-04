/** The ClinMAP seal: a plumb line at rest inside a stone arch.
 *  Oldest instrument of judgment — gravity as the reviewer that cannot be flattered. */
export default function Mark({ size = 34, ink = '#344551', rust = '#A95F37' }: { size?: number; ink?: string; rust?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="ClinMAP seal">
      {/* stele arch */}
      <path d="M12 58 V26 C12 13.8 20.9 6 32 6 C43.1 6 52 13.8 52 26 V58" stroke={ink} strokeWidth="3" strokeLinecap="round" />
      {/* baseline */}
      <path d="M8 58 H56" stroke={ink} strokeWidth="3" strokeLinecap="round" />
      {/* plumb line */}
      <path d="M32 14 V34" stroke={ink} strokeWidth="2" strokeLinecap="round" />
      {/* knot */}
      <circle cx="32" cy="14" r="2.6" fill={ink} />
      {/* bob */}
      <path d="M32 48 L25 34 H39 Z" fill={rust} />
      {/* level mark */}
      <path d="M22 52 H42" stroke={rust} strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}
