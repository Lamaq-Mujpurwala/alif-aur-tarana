import type { Metadata } from "next";
import { Gulzar, Noto_Nastaliq_Urdu, Tiro_Devanagari_Hindi } from "next/font/google";
import "./globals.css";

// Nastaʿlīq — the soul (hero + wordmark + sigils)
const gulzar = Gulzar({ weight: "400", subsets: ["arabic"], variable: "--font-gulzar", display: "swap" });
const notoNastaliq = Noto_Nastaliq_Urdu({
  weight: ["400", "700"],
  subsets: ["arabic"],
  variable: "--font-noto-nastaliq",
  display: "swap",
});
// Devanagari gloss
const tiro = Tiro_Devanagari_Hindi({
  weight: "400",
  subsets: ["devanagari", "latin"],
  variable: "--font-tiro",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Alif Aur Tarana — Urdu, mehsoos kijiye",
  description: "Learn Urdu through its content and feeling, with two companions — Alif and Tarana.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      className={`${gulzar.variable} ${notoNastaliq.variable} ${tiro.variable}`}
    >
      <body className="with-alif">{children}</body>
    </html>
  );
}
