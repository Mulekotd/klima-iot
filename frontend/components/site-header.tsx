"use client";

import Link from "next/link";
import { useAtom } from "jotai";
import { Icon } from "@/components/icons";
import { Logo } from "@/components/logo";
import { mobileMenuOpenAtom } from "@/state/atoms";

export function SiteHeader() {
  const [open, setOpen] = useAtom(mobileMenuOpenAtom);

  return (
    <header className="site-header">
      <div className="site-header-inner page-shell">
        <Logo />

        <nav className="desktop-nav" aria-label="Navegação principal">
          <a href="#como-funciona">Como funciona</a>
          <a href="#recursos">Recursos</a>
          <a href="#impacto">Impacto</a>
        </nav>

        <div className="header-actions">
          <Link className="text-link desktop-only" href="/login">
            Entrar
          </Link>
          <Link className="button button-small button-dark" href="/register">
            Começar agora
            <Icon name="arrow-right" size={16} />
          </Link>
          <button
            aria-expanded={open}
            aria-label={open ? "Fechar menu" : "Abrir menu"}
            className="mobile-menu-button"
            onClick={() => setOpen((value) => !value)}
            type="button"
          >
            <Icon name={open ? "close" : "menu"} />
          </button>
        </div>
      </div>

      {open && (
        <nav className="mobile-nav" aria-label="Navegação mobile">
          <a href="#como-funciona" onClick={() => setOpen(false)}>
            Como funciona
          </a>
          <a href="#recursos" onClick={() => setOpen(false)}>
            Recursos
          </a>
          <a href="#impacto" onClick={() => setOpen(false)}>
            Impacto
          </a>
          <Link href="/login" onClick={() => setOpen(false)}>
            Entrar na conta
          </Link>
        </nav>
      )}
    </header>
  );
}
