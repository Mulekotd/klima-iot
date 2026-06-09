import type { Metadata } from "next";
import { AppShell } from "@/components/app-shell";
import { RemoteControl } from "@/components/remote-control";

export const metadata: Metadata = {
  title: "Controle remoto"
};

export default function ControlPage() {
  return (
    <AppShell
      title="Controle remoto"
      subtitle="Ajuste o clima da sala de onde estiver."
    >
      <RemoteControl />
    </AppShell>
  );
}
