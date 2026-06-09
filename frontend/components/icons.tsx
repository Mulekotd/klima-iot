import type { LucideIcon, LucideProps } from "lucide-react";
import {
  AirVent,
  ArrowRight,
  Bell,
  Calendar,
  ChartNoAxesColumnIncreasing,
  Check,
  ChevronDown,
  Clock3,
  Droplet,
  Ellipsis,
  Eye,
  EyeOff,
  Fan,
  Globe,
  House,
  LayoutDashboard,
  Leaf,
  Menu,
  Minus,
  PersonStanding,
  Plus,
  Power,
  Settings,
  ShieldCheck,
  Snowflake,
  Sun,
  Thermometer,
  TrendingDown,
  UserRound,
  Wifi,
  X,
  Zap
} from "lucide-react";

export type IconName =
  | "arrow-right"
  | "bell"
  | "calendar"
  | "chart"
  | "check"
  | "chevron-down"
  | "clock"
  | "close"
  | "dashboard"
  | "droplet"
  | "eye"
  | "eye-off"
  | "fan"
  | "google"
  | "home"
  | "leaf"
  | "menu"
  | "minus"
  | "motion"
  | "more"
  | "plus"
  | "power"
  | "remote"
  | "settings"
  | "shield"
  | "snowflake"
  | "sun"
  | "thermometer"
  | "trend-down"
  | "user"
  | "wifi"
  | "zap";

const iconMap: Record<IconName, LucideIcon> = {
  "arrow-right": ArrowRight,
  bell: Bell,
  calendar: Calendar,
  chart: ChartNoAxesColumnIncreasing,
  check: Check,
  "chevron-down": ChevronDown,
  clock: Clock3,
  close: X,
  dashboard: LayoutDashboard,
  droplet: Droplet,
  eye: Eye,
  "eye-off": EyeOff,
  fan: Fan,
  google: Globe,
  home: House,
  leaf: Leaf,
  menu: Menu,
  minus: Minus,
  motion: PersonStanding,
  more: Ellipsis,
  plus: Plus,
  power: Power,
  remote: AirVent,
  settings: Settings,
  shield: ShieldCheck,
  snowflake: Snowflake,
  sun: Sun,
  thermometer: Thermometer,
  "trend-down": TrendingDown,
  user: UserRound,
  wifi: Wifi,
  zap: Zap
};

type IconProps = LucideProps & {
  name: IconName;
};

export function Icon({ name, size = 20, ...props }: IconProps) {
  const LucideIcon = iconMap[name];

  return (
    <LucideIcon
      aria-hidden="true"
      size={size}
      strokeWidth={1.8}
      {...props}
    />
  );
}
