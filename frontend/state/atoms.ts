import { atom } from "jotai";

export type ClimateMode = "cool" | "fan" | "auto";
export type FanSpeed = "Auto" | "Baixa" | "Média" | "Alta";
export type DashboardPeriod = "Hoje" | "7 dias" | "30 dias";
export type RemoteControlCommand = {
  temperature: number;
  powered: boolean;
  mode: ClimateMode;
  fanSpeed: FanSpeed;
  eco: boolean;
  timer: boolean;
};

export const mobileMenuOpenAtom = atom(false);
export const authPasswordVisibleAtom = atom(false);

export const temperatureAtom = atom(22);
export const poweredAtom = atom(true);
export const climateModeAtom = atom<ClimateMode>("cool");
export const fanSpeedAtom = atom<FanSpeed>("Auto");
export const ecoModeAtom = atom(true);
export const timerEnabledAtom = atom(false);
export const remoteFeedbackAtom = atom("Sincronizado agora");
export const lastRemoteCommandAtom = atom<RemoteControlCommand | null>(null);

export const dashboardPeriodAtom = atom<DashboardPeriod>("7 dias");
