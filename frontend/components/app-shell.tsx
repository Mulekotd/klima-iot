"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import { Icon, type IconName } from "@/components/icons";
import { Logo } from "@/components/logo";

const navItems: { href: string; label: string; icon: IconName }[] = [
  { href: "/dashboard", label: "Visão geral", icon: "dashboard" },
  { href: "/control", label: "Controle", icon: "remote" },
  { href: "/dashboard#consumo", label: "Consumo", icon: "zap" },
  { href: "/dashboard#rotinas", label: "Rotinas", icon: "clock" }
];

export function AppShell({
  children,
  title,
  subtitle
}: {
  children: ReactNode;
  title: string;
  subtitle: string;
}) {
  const pathname = usePathname();

  return (
    <div className="app-frame">
      <aside className="app-sidebar">
        <div>
          <Logo href="/dashboard" light />
          <nav className="sidebar-nav" aria-label="Navegação do aplicativo">
            {navItems.map((item) => {
              const active = item.href === pathname;

              return (
                <Link
                  className={active ? "active" : ""}
                  href={item.href}
                  key={item.label}
                >
                  <Icon name={item.icon} size={19} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="sidebar-bottom">
          <div className="user-chip">
            <span className="avatar">MC</span>
            <span>
              <strong>Marina Costa</strong>
              <small>Conta pessoal</small>
            </span>
            <Icon name="more" size={18} />
          </div>
        </div>
      </aside>

      <div className="app-content">
        <header className="app-topbar">
          <div>
            <p className="app-eyebrow">Minha casa / Sala de estar</p>
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>
          <div className="topbar-actions">
            <span className="connection-pill">
              <span />
              Dispositivo online
            </span>
            <button aria-label="Notificações" className="icon-button" type="button">
              <Icon name="bell" size={19} />
              <i />
            </button>
            <span className="topbar-avatar">MC</span>
          </div>
        </header>

        <main className="app-main">{children}</main>
      </div>

      <nav className="bottom-nav" aria-label="Navegação inferior">
        {navItems.slice(0, 4).map((item) => {
          const active = item.href === pathname;

          return (
            <Link
              className={active ? "active" : ""}
              href={item.href}
              key={item.label}
            >
              <Icon name={item.icon} size={21} />
              <span>{item.label.split(" ")[0]}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
