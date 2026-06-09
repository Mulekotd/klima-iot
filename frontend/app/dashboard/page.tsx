import type { Metadata } from "next";
import { AppShell } from "@/components/app-shell";
import { DashboardOverview } from "@/components/dashboard-overview";

export const metadata: Metadata = {
  title: "Dashboard"
};

export default function DashboardPage() {
  return (
    <AppShell
      title="Visão geral"
      subtitle="Acompanhe conforto, consumo e economia."
    >
      <DashboardOverview />
    </AppShell>
  );
}
