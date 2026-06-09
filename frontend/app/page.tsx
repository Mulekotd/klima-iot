import Link from "next/link";
import { Icon, type IconName } from "@/components/icons";
import { Logo } from "@/components/logo";
import { SiteHeader } from "@/components/site-header";

const features: {
  icon: IconName;
  number: string;
  title: string;
  description: string;
}[] = [
  {
    icon: "remote",
    number: "01",
    title: "Controle de qualquer lugar",
    description:
      "Ligue, desligue e ajuste seu ar-condicionado pelo celular, antes mesmo de chegar em casa."
  },
  {
    icon: "motion",
    number: "02",
    title: "Automação que percebe você",
    description:
      "Sensores de presença, temperatura e umidade adaptam o ambiente sem comandos repetitivos."
  },
  {
    icon: "chart",
    number: "03",
    title: "Consumo sem surpresas",
    description:
      "Acompanhe energia, custos e tendências para tomar decisões melhores todos os dias."
  }
];

const steps = [
  {
    number: "01",
    title: "Conecte",
    text: "Posicione o Klima perto do ar-condicionado e conecte-o ao Wi-Fi."
  },
  {
    number: "02",
    title: "Configure",
    text: "Ensine os comandos do seu controle em poucos toques pelo aplicativo."
  },
  {
    number: "03",
    title: "Respire",
    text: "Crie rotinas e deixe o Klima cuidar do conforto e da economia."
  }
];

function ClimatePreview() {
  return (
    <div className="hero-visual" aria-label="Preview do aplicativo Klima">
      <div className="ambient-orbit orbit-one" />
      <div className="ambient-orbit orbit-two" />

      <div className="sensor-card">
        <div className="sensor-card-head">
          <span className="sensor-icon">
            <Icon name="motion" size={18} />
          </span>
          <span>Presença detectada</span>
        </div>
        <strong>Sala ocupada</strong>
        <small>Atualizado agora</small>
      </div>

      <div className="phone-mockup">
        <div className="phone-top">
          <span>9:41</span>
          <span className="phone-status">
            <Icon name="wifi" size={13} />
            <i />
          </span>
        </div>
        <div className="phone-greeting">
          <span>
            Boa tarde,
            <strong>Marina</strong>
          </span>
          <span className="mini-avatar">MC</span>
        </div>
        <div className="room-label">
          <span>Sala de estar</span>
          <Icon name="chevron-down" size={15} />
        </div>
        <div className="temperature-display">
          <div className="temperature-ring">
            <div>
              <span>22</span>
              <sup>°</sup>
              <small>Resfriando</small>
            </div>
          </div>
          <div className="temperature-controls">
            <button aria-label="Diminuir temperatura" type="button">
              <Icon name="minus" size={18} />
            </button>
            <button aria-label="Aumentar temperatura" type="button">
              <Icon name="plus" size={18} />
            </button>
          </div>
        </div>
        <div className="phone-metrics">
          <span>
            <Icon name="thermometer" size={16} />
            <small>Ambiente</small>
            <strong>24,3 °C</strong>
          </span>
          <span>
            <Icon name="droplet" size={16} />
            <small>Umidade</small>
            <strong>58%</strong>
          </span>
        </div>
        <div className="mode-row">
          <span className="active">
            <Icon name="snowflake" size={17} />
            Frio
          </span>
          <span>
            <Icon name="fan" size={17} />
            Ventilar
          </span>
          <span>
            <Icon name="leaf" size={17} />
            Eco
          </span>
        </div>
      </div>

      <div className="saving-card">
        <span className="saving-icon">
          <Icon name="leaf" size={18} />
        </span>
        <span>
          <small>Economia este mês</small>
          <strong>R$ 38,70</strong>
        </span>
        <span className="saving-badge">
          <Icon name="trend-down" size={13} />
          18%
        </span>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <div className="landing-page">
      <SiteHeader />

      <main>
        <section className="hero-section page-shell">
          <div className="hero-copy">
            <div className="eyebrow">
              <span />
              Tecnologia que sente o ambiente
            </div>
            <h1>
              Seu clima.
              <br />
              <em>Mais inteligente.</em>
            </h1>
            <p>
              Transforme qualquer ar-condicionado em um sistema conectado,
              eficiente e atento a você. Sem trocar o aparelho que já tem.
            </p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/register">
                Quero conhecer o Klima
                <Icon name="arrow-right" size={18} />
              </Link>
              <a className="play-link" href="#como-funciona">
                <span>
                  <Icon name="arrow-right" size={16} />
                </span>
                Ver como funciona
              </a>
            </div>
          </div>

          <ClimatePreview />
        </section>

        <section className="trust-strip" aria-label="Principais beneficios">
          <div className="page-shell trust-grid">
            <span>
              <Icon name="wifi" size={20} />
              Conectividade Wi-Fi
            </span>
            <span>
              <Icon name="shield" size={20} />
              Dados protegidos
            </span>
            <span>
              <Icon name="leaf" size={20} />
              Menor consumo
            </span>
            <span>
              <Icon name="remote" size={20} />
              Compativel com seu AC
            </span>
          </div>
        </section>

        <section className="features-section page-shell" id="recursos">
          <div className="section-heading split-heading">
            <div>
              <span className="section-kicker">Conforto sob medida</span>
              <h2>O ambiente certo, no momento certo.</h2>
            </div>
            <p>
              O Klima combina sensores e automação para equilibrar bem-estar e
              eficiência, sem exigir que você pense nisso o tempo todo.
            </p>
          </div>

          <div className="feature-grid">
            {features.map((feature) => (
              <article className="feature-card" key={feature.number}>
                <div className="feature-card-top">
                  <span className="feature-icon">
                    <Icon name={feature.icon} size={25} />
                  </span>
                  <span className="feature-number">{feature.number}</span>
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
                <Link href="/dashboard">
                  Explorar recurso
                  <Icon name="arrow-right" size={16} />
                </Link>
              </article>
            ))}
          </div>
        </section>

        <section className="impact-section" id="impacto">
          <div className="page-shell impact-grid">
            <div className="impact-visual">
              <div className="impact-glow" />
              <div className="energy-card">
                <div className="energy-card-head">
                  <span>
                    <small>Consumo hoje</small>
                    <strong>4,2 kWh</strong>
                  </span>
                  <span className="energy-down">
                    <Icon name="trend-down" size={14} />
                    21%
                  </span>
                </div>
                <div className="energy-chart" aria-hidden="true">
                  {[34, 47, 39, 62, 54, 74, 57, 42, 67, 51, 32, 45].map(
                    (height, index) => (
                      <span
                        className={index === 5 ? "active" : ""}
                        key={`${height}-${index}`}
                        style={{ height: `${height}%` }}
                      />
                    ),
                  )}
                </div>
                <div className="energy-labels">
                  <span>06h</span>
                  <span>12h</span>
                  <span>18h</span>
                  <span>Agora</span>
                </div>
              </div>
              <div className="co2-card">
                <Icon name="leaf" size={20} />
                <span>
                  <small>CO2 evitado</small>
                  <strong>8,4 kg</strong>
                </span>
              </div>
            </div>

            <div className="impact-copy">
              <span className="section-kicker section-kicker-light">
                Eficiência visível
              </span>
              <h2>Economizar fica mais fácil quando você entende.</h2>
              <p>
                Veja quanto seu ar-condicionado consome, descubra os horários
                mais caros e acompanhe o impacto das suas automações.
              </p>
              <div className="impact-stats">
                <div>
                  <strong>ate 30%</strong>
                  <span>de redução no consumo</span>
                </div>
                <div>
                  <strong>24/7</strong>
                  <span>monitoramento contínuo</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="steps-section page-shell" id="como-funciona">
          <div className="section-heading centered-heading">
            <span className="section-kicker">Simples desde o início</span>
            <h2>Seu ar inteligente em tres passos.</h2>
          </div>
          <div className="steps-grid">
            {steps.map((step) => (
              <article className="step-card" key={step.number}>
                <span>{step.number}</span>
                <h3>{step.title}</h3>
                <p>{step.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="final-cta page-shell">
          <div className="cta-orbit cta-orbit-one" />
          <div className="cta-orbit cta-orbit-two" />
          <div className="cta-content">
            <span className="section-kicker section-kicker-light">
              O futuro cabe na sua casa
            </span>
            <h2>Pronto para respirar um ar mais inteligente?</h2>
            <p>
              Entre para a lista de acesso antecipado e acompanhe os proximos
              passos do Klima.
            </p>
            <Link className="button button-accent" href="/register">
              Criar minha conta
              <Icon name="arrow-right" size={18} />
            </Link>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div className="page-shell footer-inner">
          <div>
            <Logo />
            <p>Controle inteligente do ar que você respira.</p>
          </div>
          <div className="footer-links">
            <a href="#recursos">Recursos</a>
            <a href="#impacto">Impacto</a>
            <a href="#privacidade">Privacidade</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
