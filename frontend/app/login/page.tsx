import Link from "next/link";
import { AuthForm } from "@/components/auth-form";
import { Icon } from "@/components/icons";
import { Logo } from "@/components/logo";

export default function LoginPage() {
  return (
    <main className="auth-page">
      <section className="auth-panel">
        <div className="auth-panel-inner">
          <Logo />
          <div className="auth-copy">
            <span className="section-kicker">Bem-vindo de volta</span>
            <h1>Seu conforto está a um toque.</h1>
            <p>
              Entre para controlar seus ambientes e acompanhar sua economia em
              tempo real.
            </p>
          </div>
          <AuthForm mode="login" />
          <Link className="back-home" href="/">
            <Icon name="arrow-right" size={16} />
            Voltar para o início
          </Link>
        </div>
      </section>

      <aside className="auth-visual">
        <div className="auth-visual-orb" />
        <div className="auth-device-card">
          <div className="auth-device-head">
            <span className="feature-icon dark-icon">
              <Icon name="snowflake" size={22} />
            </span>
            <span>
              <strong>Sala de estar</strong>
              <small>Klima conectado</small>
            </span>
            <span className="online-dot" />
          </div>
          <div className="auth-temp">
            <small>Temperatura ideal</small>
            <strong>
              22<sup>°</sup>
            </strong>
            <span>Ambiente em equilíbrio</span>
          </div>
          <div className="auth-device-stats">
            <span>
              <Icon name="droplet" size={18} />
              <small>Umidade</small>
              <strong>58%</strong>
            </span>
            <span>
              <Icon name="leaf" size={18} />
              <small>Modo</small>
              <strong>Eco</strong>
            </span>
          </div>
        </div>
        <blockquote>
          “Agora a casa está fresca quando eu chego, sem ficar ligada o dia
          inteiro.”
          <footer>
            <span className="avatar">AM</span>
            <span>
              <strong>Ana Martins</strong>
              <small>Usuária beta Klima</small>
            </span>
          </footer>
        </blockquote>
      </aside>
    </main>
  );
}
