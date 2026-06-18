"use client";

import { motion, type Variants } from "framer-motion";
import type { ReplyTurn } from "@/lib/types";

/** The teaching block: Nastaʿlīq hero (ink-settle reveal) + Roman + Devanagari + note. */
export function TriScript({ turn }: { turn: ReplyTurn }) {
  const { display, english_note } = turn;
  return (
    <motion.div
      key={display.urdu}
      initial="hidden"
      animate="show"
      variants={{ show: { transition: { staggerChildren: 0.09 } } }}
      style={{ display: "grid", gap: 14, textAlign: "center", maxWidth: "var(--measure)" }}
    >
      <motion.p className="nastaliq" variants={ink} style={{ margin: 0 }}>
        {display.urdu}
      </motion.p>
      <motion.p className="roman" variants={fadeUp} style={{ margin: 0 }}>
        {display.roman}
      </motion.p>
      <motion.p className="deva" variants={fadeUp} style={{ margin: 0 }}>
        {display.devanagari}
      </motion.p>
      {english_note ? (
        <motion.p
          variants={fadeUp}
          style={{ margin: 0, color: "var(--parchment-dim)", fontSize: "0.9rem", fontStyle: "italic" }}
        >
          {english_note}
        </motion.p>
      ) : null}
    </motion.div>
  );
}

const ink: Variants = {
  hidden: { opacity: 0, y: 8, filter: "blur(6px)" },
  show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.6, ease: [0.22, 0.61, 0.36, 1] } },
};
const fadeUp: Variants = {
  hidden: { opacity: 0, y: 6 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};
