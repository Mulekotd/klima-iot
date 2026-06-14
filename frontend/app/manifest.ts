import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Klima - Clima inteligente",
    short_name: "Klima",
    description:
      "Controle seu ar-condicionado, automatize o conforto e acompanhe o consumo de energia.",
    start_url: "/dashboard",
    display: "standalone",
    background_color: "#f5f6ef",
    theme_color: "#0d2f2a",
    icons: [
      {
        src: "/icon.svg",
        sizes: "any",
        type: "image/svg+xml",
        purpose: "any",
      },
    ]
  };
}
