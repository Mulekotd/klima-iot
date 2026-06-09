import Link from "next/link";
import { AuthForm } from "@/components/auth-form";
import { Icon } from "@/components/icons";
import { Logo } from "@/components/logo";

const benefits = [
  "Controle remoto de qualquer lugar",
  "Automacoes baseadas no ambiente",
  "Analise de consumo e custo",
];

export default function RegisterPage() {
  return (
    <main className="auth-page">
      <section className="auth-panel">
        <div className="auth-panel-inner">
          <Logo />
          <div className="auth-copy">
            <span className="section-kicker">Comece agora</span>
            <h1>Uma casa mais fresca e consciente.</h1>
            <p>
              Crie sua conta e experimente o protótipo do ecossistema Klima.
            </p>
          </div>
          <AuthForm mode="register" />
          <Link className="back-home" href="/">
            <Icon name="arrow-right" size={16} />
            Voltar para o início
          </Link>
        </div>
      </section>

      <aside className="auth-visual register-visual">
        <div className="auth-visual-orb" />
        <div className="register-message">
          <span className="eyebrow eyebrow-dark">
            <span />
            Klima early access
          </span>
          <h2>Seu ar-condicionado já pode ser inteligente.</h2>
          <p>
            Tudo o que você precisa para ter mais conforto e menos desperdício
            em um único aplicativo.
          </p>
          <ul>
            {benefits.map((benefit) => (
              <li key={benefit}>
                <span>
                  <Icon name="check" size={15} />
                </span>
                {benefit}
              </li>
            ))}
          </ul>
        </div>
      </aside>
    </main>
  );
}
