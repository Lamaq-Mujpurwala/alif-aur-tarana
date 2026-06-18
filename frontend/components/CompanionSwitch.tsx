"use client";

import type { Companion } from "@/lib/types";

/** Two restrained sigils — Alif (ا) and Tarana (◐). Switching re-tints the room. */
export function CompanionSwitch({
  companion,
  onChange,
}: {
  companion: Companion;
  onChange: (c: Companion) => void;
}) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 22 }}>
      <Sigil glyph="ا" name="Alif" active={companion === "alif"} onClick={() => onChange("alif")} />
      <Sigil glyph="◐" name="Tarana" active={companion === "tarana"} onClick={() => onChange("tarana")} />
    </div>
  );
}

function Sigil({
  glyph,
  name,
  active,
  onClick,
}: {
  glyph: string;
  name: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <div style={{ display: "grid", justifyItems: "center", gap: 6 }}>
      <button className="sigil" data-active={active} aria-pressed={active} aria-label={name} onClick={onClick}>
        {glyph}
      </button>
      <span className="label" style={{ opacity: active ? 1 : 0.55 }}>{name}</span>
    </div>
  );
}
