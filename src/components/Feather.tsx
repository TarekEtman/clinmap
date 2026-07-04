/** The feather of Ma'at, drawn in code: a tapered shaft with fine barbs.
 *  Every response in the benchmark was weighed against it. */

const BARB_COUNT = 30;

function barbPath(i: number): { d: string; opacity: number } {
  const t = i / (BARB_COUNT - 1); // 0 at tip (top), 1 at base
  const y = 18 + t * 158;
  const x = 60 + Math.sin(t * Math.PI * 0.5) * 1.6; // shaft drift
  const len = 6 + 40 * Math.sin(Math.PI * Math.min(1, 0.18 + t * 0.92) * 0.86);
  const droop = 7 + t * 6;
  const left = `M ${x} ${y} Q ${x - len * 0.55} ${y - droop * 0.55} ${x - len} ${y - droop}`;
  const right = `M ${x} ${y} Q ${x + len * 0.55} ${y - droop * 0.55} ${x + len} ${y - droop}`;
  return { d: `${left} ${right}`, opacity: 0.28 + 0.5 * Math.sin(Math.PI * (0.1 + t * 0.9)) };
}

export default function Feather({
  size = 200,
  tint = '#344551',
  className = '',
  style,
}: {
  size?: number;
  tint?: string;
  className?: string;
  style?: React.CSSProperties;
}) {
  const barbs = Array.from({ length: BARB_COUNT }, (_, i) => barbPath(i));
  return (
    <svg
      width={size * 0.6}
      height={size}
      viewBox="0 0 120 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={style}
      aria-hidden="true"
    >
      {/* rachis */}
      <path d="M 60 6 C 59 50 62 120 60 176 L 60 196" stroke={tint} strokeWidth="1.6" strokeLinecap="round" opacity="0.75" />
      {barbs.map((b, i) => (
        <path key={i} d={b.d} stroke={tint} strokeWidth="0.75" strokeLinecap="round" opacity={b.opacity} />
      ))}
      {/* afterfeather wisps at the base */}
      <path d="M 60 176 Q 52 184 46 194 M 60 180 Q 66 188 71 195" stroke="#A95F37" strokeWidth="0.9" strokeLinecap="round" opacity="0.55" />
    </svg>
  );
}
