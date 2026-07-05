/** The feather of Ma'at, grown strand by strand by report/make_feather_art.py.
 *  Each seed is a different bird. One barb in each is rust: the reading that
 *  disagreed, kept in the record. */

export default function Feather({
  size = 200,
  className = '',
  style,
  variant = 'ink',
  seed = 40,
}: {
  size?: number;
  className?: string;
  style?: React.CSSProperties;
  variant?: 'ink' | 'iris';
  /** 40 (default), 7, or 23 — three plumages grown from different seeds */
  seed?: 40 | 7 | 23;
}) {
  const name =
    variant === 'iris'
      ? seed === 40
        ? 'maat-feather-iris.svg'
        : `maat-feather-iris-${seed}.svg`
      : 'maat-feather.svg';
  return (
    <img
      src={`${import.meta.env.BASE_URL}assets/${name}`}
      width={size * 0.5}
      height={size}
      className={className}
      style={style}
      alt=""
      aria-hidden="true"
      draggable={false}
    />
  );
}
