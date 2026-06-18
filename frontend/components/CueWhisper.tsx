"use client";

import { AnimatePresence, motion } from "framer-motion";

/** The acknowledgement cue, whispered above the input while its cached audio plays. */
export function CueWhisper({ text }: { text: string }) {
  return (
    <div style={{ minHeight: 28, display: "grid", placeItems: "center" }}>
      <AnimatePresence mode="wait">
        {text ? (
          <motion.p
            key={text}
            className="roman"
            dir="rtl"
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.85 }}
            exit={{ opacity: 0 }}
            style={{ margin: 0, textAlign: "center", color: "var(--accent)" }}
          >
            {text}
          </motion.p>
        ) : null}
      </AnimatePresence>
    </div>
  );
}
