"use client";

import { useAtom, useAtomValue } from "jotai";
import { Icon, type IconName } from "@/components/icons";
import { useDebouncedRemoteCommand } from "@/hooks/use-debounced-remote-command";
import {
  climateModeAtom,
  ecoModeAtom,
  fanSpeedAtom,
  poweredAtom,
  remoteFeedbackAtom,
  temperatureAtom,
  timerEnabledAtom,
  type ClimateMode,
  type FanSpeed,
  type RemoteControlCommand,
} from "@/state/atoms";

const modes: {
  id: ClimateMode;
  label: string;
  icon: IconName;
}[] = [
  { id: "cool", label: "Resfriar", icon: "snowflake" },
  { id: "fan", label: "Ventilar", icon: "fan" },
  { id: "auto", label: "Automático", icon: "settings" },
];

const fanSpeeds: FanSpeed[] = ["Auto", "Baixa", "Média", "Alta"];

export function RemoteControl() {
  const [temperature, setTemperature] = useAtom(temperatureAtom);
  const [powered, setPowered] = useAtom(poweredAtom);
  const [mode, setMode] = useAtom(climateModeAtom);
  const [fanSpeed, setFanSpeed] = useAtom(fanSpeedAtom);
  const [eco, setEco] = useAtom(ecoModeAtom);
  const [timer, setTimer] = useAtom(timerEnabledAtom);
  const feedback = useAtomValue(remoteFeedbackAtom);
  const queueRemoteCommand = useDebouncedRemoteCommand();

  const currentCommand: RemoteControlCommand = {
    temperature,
    powered,
    mode,
    fanSpeed,
    eco,
    timer,
  };

  function queueCommand(patch: Partial<RemoteControlCommand>) {
    queueRemoteCommand({ ...currentCommand, ...patch });
  }

  function updateTemperature(delta: number) {
    const nextTemperature = Math.min(30, Math.max(16, temperature + delta));
    setTemperature(nextTemperature);
    queueCommand({ temperature: nextTemperature });
  }

  return (
    <div className="control-layout">
      <section className={`remote-panel ${powered ? "" : "is-off"}`}>
        <div className="remote-panel-head">
          <div>
            <span className="panel-label">Controle principal</span>
            <h2>Samsung WindFree</h2>
          </div>
          <button
            aria-label={powered ? "Desligar ar-condicionado" : "Ligar ar-condicionado"}
            className={`power-button ${powered ? "active" : ""}`}
            onClick={() => {
              const nextPowered = !powered;
              setPowered(nextPowered);
              queueCommand({ powered: nextPowered });
            }}
            type="button"
          >
            <Icon name="power" size={22} />
          </button>
        </div>

        <div className="temperature-control">
          <div className="temperature-arc">
            <div className="arc-ticks" aria-hidden="true">
              {Array.from({ length: 25 }).map((_, index) => (
                <i key={index} style={{ transform: `rotate(${index * 7.5 - 90}deg)` }} />
              ))}
            </div>
            <div className="temperature-value">
              <span className="temperature-status">
                <Icon name={powered ? "snowflake" : "power"} size={15} />
                {powered ? "Resfriando" : "Desligado"}
              </span>
              <strong>
                {temperature}
                <sup>°</sup>
              </strong>
              <small>Temperatura desejada</small>
            </div>
          </div>
          <div className="temp-buttons">
            <button
              aria-label="Diminuir temperatura"
              disabled={!powered || temperature === 16}
              onClick={() => updateTemperature(-1)}
              type="button"
            >
              <Icon name="minus" size={22} />
            </button>
            <span>16 °C - 30 °C</span>
            <button
              aria-label="Aumentar temperatura"
              disabled={!powered || temperature === 30}
              onClick={() => updateTemperature(1)}
              type="button"
            >
              <Icon name="plus" size={22} />
            </button>
          </div>
        </div>

        <div
          aria-live="polite"
          className="remote-feedback"
          role="status"
        >
          <span />
          {feedback}
        </div>
      </section>

      <div className="control-options">
        <section className="app-card mode-card">
          <div className="card-heading">
            <div>
              <span className="panel-label">Modo de operação</span>
              <h3>Como o ambiente deve ficar?</h3>
            </div>
          </div>
          <div className="mode-options">
            {modes.map((item) => (
              <button
                className={mode === item.id ? "active" : ""}
                disabled={!powered}
                key={item.id}
                onClick={() => {
                  setMode(item.id);
                  queueCommand({ mode: item.id });
                }}
                type="button"
              >
                <span>
                  <Icon name={item.icon} size={21} />
                </span>
                {item.label}
                {mode === item.id && <Icon name="check" size={16} />}
              </button>
            ))}
          </div>
        </section>

        <section className="app-card fan-card">
          <div className="card-heading">
            <div>
              <span className="panel-label">Velocidade do ar</span>
              <h3>Ventilação</h3>
            </div>
            <Icon name="fan" size={22} />
          </div>
          <div className="fan-options">
            {fanSpeeds.map((speed) => (
              <button
                className={fanSpeed === speed ? "active" : ""}
                disabled={!powered}
                key={speed}
                onClick={() => {
                  setFanSpeed(speed);
                  queueCommand({ fanSpeed: speed });
                }}
                type="button"
              >
                {speed}
              </button>
            ))}
          </div>
        </section>

        <section className="app-card quick-actions-card">
          <div className="card-heading">
            <div>
              <span className="panel-label">Ações rápidas</span>
              <h3>Preferências</h3>
            </div>
          </div>
          <button
            className="setting-row"
            disabled={!powered}
            onClick={() => {
              const nextEco = !eco;
              setEco(nextEco);
              queueCommand({ eco: nextEco });
            }}
            type="button"
          >
            <span className="setting-icon eco">
              <Icon name="leaf" size={20} />
            </span>
            <span>
              <strong>Modo Eco</strong>
              <small>Reduz o consumo automaticamente</small>
            </span>
            <span className={`toggle ${eco ? "active" : ""}`}>
              <i />
            </span>
          </button>
          <button
            className="setting-row"
            disabled={!powered}
            onClick={() => {
              const nextTimer = !timer;
              setTimer(nextTimer);
              queueCommand({ timer: nextTimer });
            }}
            type="button"
          >
            <span className="setting-icon timer">
              <Icon name="clock" size={20} />
            </span>
            <span>
              <strong>Desligamento programado</strong>
              <small>{timer ? "Desliga em 2 horas" : "Nenhum timer ativo"}</small>
            </span>
            <span className={`toggle ${timer ? "active" : ""}`}>
              <i />
            </span>
          </button>
        </section>
      </div>

      <section className="app-card environment-card">
        <div className="card-heading">
          <div>
            <span className="panel-label">Leitura em tempo real</span>
            <h3>Condições do ambiente</h3>
          </div>
          <span className="updated-label">Atualizado agora</span>
        </div>
        <div className="environment-metrics">
          <div>
            <span className="metric-icon temperature">
              <Icon name="thermometer" size={21} />
            </span>
            <span>
              <small>Temperatura</small>
              <strong>24,3 °C</strong>
            </span>
            <span className="metric-state warm">+1,2 °C</span>
          </div>
          <div>
            <span className="metric-icon humidity">
              <Icon name="droplet" size={21} />
            </span>
            <span>
              <small>Umidade</small>
              <strong>58%</strong>
            </span>
            <span className="metric-state">Ideal</span>
          </div>
          <div>
            <span className="metric-icon presence">
              <Icon name="motion" size={21} />
            </span>
            <span>
              <small>Presença</small>
              <strong>Detectada</strong>
            </span>
            <span className="metric-state occupied">
              <i />
              Agora
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}
