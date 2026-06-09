"use client";

import { useAtom } from "jotai";
import { Icon, type IconName } from "@/components/icons";
import {
  dashboardPeriodAtom,
  type DashboardPeriod,
} from "@/state/atoms";

const periods: DashboardPeriod[] = ["Hoje", "7 dias", "30 dias"];

const chartData: Record<DashboardPeriod, number[]> = {
  Hoje: [18, 25, 21, 34, 31, 48, 43, 59, 51, 64, 54, 46],
  "7 dias": [38, 45, 34, 52, 47, 61, 56, 70, 64, 59, 50, 55],
  "30 dias": [55, 49, 61, 46, 58, 41, 50, 37, 43, 32, 39, 29],
};

const metricCards: {
  label: string;
  value: string;
  detail: string;
  icon: IconName;
  tone: string;
}[] = [
  {
    label: "Temperatura media",
    value: "23,4 °C",
    detail: "Dentro da meta",
    icon: "thermometer",
    tone: "mint",
  },
  {
    label: "Consumo este mês",
    value: "82,6 kWh",
    detail: "12% abaixo de maio",
    icon: "zap",
    tone: "lime",
  },
  {
    label: "Custo estimado",
    value: "R$ 71,84",
    detail: "Economia de R$ 18,20",
    icon: "chart",
    tone: "orange",
  },
  {
    label: "Tempo em uso",
    value: "46h 20min",
    detail: "3h 12min hoje",
    icon: "clock",
    tone: "blue",
  },
];

export function DashboardOverview() {
  const [period, setPeriod] = useAtom(dashboardPeriodAtom);
  const data = chartData[period];

  return (
    <div className="dashboard-layout">
      <section className="welcome-card">
        <div>
          <span className="welcome-pill">
            <Icon name="leaf" size={14} />
            Economia em dia
          </span>
          <h2>Boa tarde, Marina.</h2>
          <p>
            Seu ambiente está confortável e o consumo segue{" "}
            <strong>12% menor</strong> que no mês passado.
          </p>
        </div>
        <div className="welcome-temperature">
          <span>
            <Icon name="snowflake" size={18} />
          </span>
          <div>
            <small>Sala de estar</small>
            <strong>24,3 °C</strong>
          </div>
          <i>Ligado</i>
        </div>
      </section>

      <section className="dashboard-metrics">
        {metricCards.map((metric) => (
          <article className="metric-card" key={metric.label}>
            <div className={`dashboard-metric-icon ${metric.tone}`}>
              <Icon name={metric.icon} size={21} />
            </div>
            <span className="metric-card-label">{metric.label}</span>
            <strong>{metric.value}</strong>
            <small>
              <Icon
                name={metric.tone === "orange" ? "leaf" : "trend-down"}
                size={13}
              />
              {metric.detail}
            </small>
          </article>
        ))}
      </section>

      <section className="app-card consumption-card" id="consumo">
        <div className="card-heading dashboard-card-heading">
          <div>
            <span className="panel-label">Energia consumida</span>
            <h3>Consumo ao longo do tempo</h3>
          </div>
          <div className="period-tabs">
            {periods.map((item) => (
              <button
                className={period === item ? "active" : ""}
                key={item}
                onClick={() => setPeriod(item)}
                type="button"
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        <div className="chart-summary">
          <div>
            <strong>{period === "Hoje" ? "4,2" : period === "7 dias" ? "23,8" : "82,6"}</strong>
            <span>kWh</span>
          </div>
          <span className="chart-trend">
            <Icon name="trend-down" size={14} />
            12,4%
          </span>
          <small>comparado ao período anterior</small>
        </div>

        <div className="bar-chart">
          <div className="chart-y-axis">
            <span>8</span>
            <span>6</span>
            <span>4</span>
            <span>2</span>
            <span>0</span>
          </div>
          <div className="bars-area">
            <div className="chart-grid-lines" aria-hidden="true">
              <i />
              <i />
              <i />
              <i />
              <i />
            </div>
            <div className="bars" aria-label={`Grafico de consumo: ${period}`}>
              {data.map((height, index) => (
                <span
                  className={index === 7 ? "highlight" : ""}
                  key={`${period}-${index}`}
                  style={{ height: `${height}%` }}
                >
                  {index === 7 && <em>4,8</em>}
                </span>
              ))}
            </div>
            <div className="chart-x-axis">
              {["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"].map((day) => (
                <span key={day}>{day}</span>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="app-card cost-card">
        <div className="card-heading">
          <div>
            <span className="panel-label">Projeção mensal</span>
            <h3>Custo de energia</h3>
          </div>
          <button aria-label="Mais opcoes" className="plain-icon-button" type="button">
            <Icon name="more" size={20} />
          </button>
        </div>
        <div className="cost-ring">
          <div>
            <strong>72%</strong>
            <small>da meta</small>
          </div>
        </div>
        <div className="cost-values">
          <span>
            <small>Gasto atual</small>
            <strong>R$ 71,84</strong>
          </span>
          <span>
            <small>Meta mensal</small>
            <strong>R$ 100,00</strong>
          </span>
        </div>
        <div className="cost-tip">
          <Icon name="leaf" size={18} />
          <p>
            Mantendo este ritmo, você economiza <strong>R$ 18,20</strong> este mês.
          </p>
        </div>
      </section>

      <section className="app-card room-card">
        <div className="card-heading">
          <div>
            <span className="panel-label">Seus ambientes</span>
            <h3>Status dos dispositivos</h3>
          </div>
          <button className="text-button" type="button">
            Ver todos
          </button>
        </div>
        <div className="room-list">
          <div>
            <span className="room-icon active">
              <Icon name="snowflake" size={20} />
            </span>
            <span>
              <strong>Sala de estar</strong>
              <small>Samsung WindFree</small>
            </span>
            <span className="room-temp">24,3 °C</span>
            <span className="status-label on">
              <i />
              Ligado
            </span>
          </div>
          <div>
            <span className="room-icon">
              <Icon name="snowflake" size={20} />
            </span>
            <span>
              <strong>Quarto</strong>
              <small>LG Dual Inverter</small>
            </span>
            <span className="room-temp">26,1 °C</span>
            <span className="status-label">
              <i />
              Desligado
            </span>
          </div>
        </div>
      </section>

      <section className="app-card routines-card" id="rotinas">
        <div className="card-heading">
          <div>
            <span className="panel-label">Próxima automação</span>
            <h3>Rotinas ativas</h3>
          </div>
          <button aria-label="Adicionar rotina" className="add-button" type="button">
            <Icon name="plus" size={18} />
          </button>
        </div>
        <div className="next-routine">
          <span className="routine-time">22:30</span>
          <div>
            <strong>Modo noite</strong>
            <small>Todos os dias</small>
          </div>
          <span className="routine-mode">
            <Icon name="snowflake" size={15} />
            23 °C
          </span>
        </div>
        <div className="routine-progress">
          <span style={{ width: "68%" }} />
        </div>
        <p>Inicia em 3 horas e 42 minutos</p>
      </section>
    </div>
  );
}
