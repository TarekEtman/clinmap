/** The feather of Ma'at, grown strand by strand (299 of them) by report/make_feather_art.py.
 *  Every response in the benchmark was weighed against it. One barb is rust:
 *  the reading that disagreed, kept in the record. */

export default function Feather({
  size = 200,
  className = '',
  style,
  tint,
}: {
  size?: number;
  className?: string;
  style?: React.CSSProperties;
  /** kept for call-site compatibility; large art keeps its natural plumage */
  tint?: string;
}) {
  return (
    <img
      src={`${import.meta.env.BASE_URL}assets/maat-feather.svg`}
      width={size * 0.5}
      height={size}
      className={className}
      style={style}
      data-tint={tint}
      alt=""
      aria-hidden="true"
      draggable={false}
    />
  );
}
