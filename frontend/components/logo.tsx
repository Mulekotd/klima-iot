import Link from "next/link";

type LogoProps = {
  compact?: boolean;
  href?: string;
  light?: boolean;
};

export function Logo({ compact = false, href = "/", light = false }: LogoProps) {
  return (
    <Link
      aria-label="Klima - página inicial"
      className={`logo ${light ? "logo-light" : ""}`}
      href={href}
    >
      <span className="logo-mark" aria-hidden="true">
        <span />
        <span />
        <span />
      </span>
      {!compact && <span className="logo-word">klima</span>}
    </Link>
  );
}
