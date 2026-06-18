"use client";

import type { CSSProperties } from "react";

/** The chirāgh — the companion's presence as a breathing lamp of light.
 *  Idle: gentle breathing (CSS). Speaking: glow tracks audio `level`. */
export function Chiragh({ level, speaking }: { level: number; speaking: boolean }) {
  const style = { "--level": speaking ? Math.max(0.1, level) : 0 } as CSSProperties;
  return <div className="chiragh" role="img" aria-label="companion presence" style={style} />;
}
