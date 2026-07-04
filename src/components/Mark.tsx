/** The seal: the feather of Ma'at standing inside the circle, as it stood on the scale.
 *  Its barbs are graduated like an instrument. One barb is rust: the reading that
 *  disagreed, kept in the record. The rust point at the quill is where judgment
 *  touches the scale. */

const BARBS = 11;

function sealBarb(i: number, side: -1 | 1): { d: string; opacity: number; rust: boolean } {
  const t = i / (BARBS - 1); // 0 near tip (top), 1 at base
  const y = 15.5 + t * 26;
  const x = 32 + Math.sin((1 - t) * 1.25) * 2.2; // rachis curve, leaning right at tip
  const len = (3.2 + 8.2 * Math.sin(Math.PI * (0.22 + t * 0.78) * 0.92)) * (side === -1 ? 1 : 0.82);
  const droop = 2.6 + t * 1.8;
  return {
    d: `M ${x} ${y} Q ${x + side * len * 0.55} ${y - droop * 0.5} ${x + side * len} ${y - droop}`,
    opacity: 0.38 + 0.5 * Math.sin(Math.PI * (0.12 + t * 0.88)),
    rust: side === -1 && i === 7,
  };
}

export default function Mark({ size = 34, ink = '#344551', rust = '#A95F37' }: { size?: number; ink?: string; rust?: string }) {
  const barbs: Array<{ d: string; opacity: number; rust: boolean }> = [];
  for (let i = 0; i < BARBS; i++) {
    barbs.push(sealBarb(i, -1));
    barbs.push(sealBarb(i, 1));
  }
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="ClinMAP seal: the feather of Ma'at">
      {/* the circle of the scale */}
      <circle cx="32" cy="32" r="28.5" stroke={ink} strokeWidth="1.4" opacity="0.75" />
      {/* rachis: quill rising, tip bowing right in the old glyph's gesture */}
      <path d="M 32 52 C 32 44 31.4 34 32.6 24 C 33.3 18.5 35 14.6 38.2 12.4" stroke={ink} strokeWidth="1.7" strokeLinecap="round" />
      {barbs.map((b, i) => (
        <path key={i} d={b.d} stroke={b.rust ? rust : ink} strokeWidth={b.rust ? 1.1 : 0.85} strokeLinecap="round" opacity={b.rust ? 0.95 : b.opacity} />
      ))}
      {/* where judgment touches the scale */}
      <circle cx="32" cy="53.5" r="1.9" fill={rust} />
    </svg>
  );
}
