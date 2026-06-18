"""Precomputed acknowledgement cues — the secret to feeling *alive*.

Short, in-character Urdu phrases the companions can play INSTANTLY (from the TTS cache,
zero latency, zero per-use cost) while the real reply is still being thought up:
  - wake      : responding to being summoned ("Alif", "suno", "Alif suno")
  - thinking  : buying a beat while the LLM reasons ("hmm, soch ke batata hoon")
  - searching : while a tool/web lookup runs ("zara dhoondh ke batata hoon")
  - affirm    : subtle backchannel acknowledgements ("hmm", "achha", "wah")

Each phrase is Urdu script (+ light [audio tags]) so the cached audio carries the real
accent. ~12 variations per category per companion so it never feels repetitive.
Run `precompute_cues.py` once to synthesise + cache all of them.
"""

from __future__ import annotations

import random
import re
from collections.abc import Iterator

from aat.config import Settings
from aat.schemas import Companion
from aat.text import strip_audio_tags

# --------------------------------------------------------------------------- #
# The phrase library
# --------------------------------------------------------------------------- #
CUES: dict[str, dict[Companion, list[str]]] = {
    "wake": {
        Companion.ALIF: [
            "[warmly] جی، فرمائیے!",
            "[warmly] بولیے، میں سن رہا ہوں۔",
            "[laughs softly] جی جناب؟",
            "[warmly] حاضر ہوں!",
            "[warmly] فرمائیے، کیا حکم ہے؟",
            "[warmly] جی، میں یہیں ہوں۔",
            "[playfully] اوہو، یاد آ ہی گئی میری؟",
            "[warmly] کہیے، کہیے۔",
            "[warmly] جی ہاں، سن رہا ہوں۔",
            "[warmly] لبیک!",
            "[warmly] بولیے، کس سوچ میں ہیں؟",
            "[laughs softly] ارے، بلایا آپ نے؟ حاضر۔",
        ],
        Companion.TARANA: [
            "[gently] جی، کہیے۔",
            "[warmly] فرمائیے۔",
            "[gently] جی، میں سن رہی ہوں۔",
            "[gently] جی ہاں؟",
            "[warmly] کہیے، کیا بات ہے؟",
            "[gently] میں حاضر ہوں۔",
            "[gently] جی، بتائیے۔",
            "[warmly] فرمائیے، میں منتظر ہوں۔",
            "[gently] جی، آپ کہیے۔",
            "[gently] ہاں جی؟",
            "[warmly] کہیے، میں سن رہی ہوں۔",
            "[gently] جی، حکم کیجیے۔",
        ],
    },
    "thinking": {
        Companion.ALIF: [
            "[warmly] ہمم… ذرا سوچنے دیجیے۔",
            "[warmly] اچھا سوال ہے… سوچ کے بتاتا ہوں۔",
            "[warmly] ایک لمحہ…",
            "[warmly] ہمم، دیکھتے ہیں۔",
            "[warmly] ذرا ٹھہریے، یاد کرتا ہوں۔",
            "[warmly] واہ، اس پر تو سوچنا پڑے گا۔",
            "[warmly] ذرا غور کرنے دیجیے…",
            "[warmly] ہمم… دلچسپ بات ہے۔",
            "[warmly] ایک سیکنڈ، خیال جمنے دیجیے۔",
            "[warmly] سوچتا ہوں… ابھی بتاتا ہوں۔",
            "[warmly] اچھا… ذرا ذہن پر زور دیتا ہوں۔",
            "[laughs softly] ہاں ہاں، آ رہا ہے خیال…",
        ],
        Companion.TARANA: [
            "[gently] ہمم… ذرا سوچنے دیجیے۔",
            "[thoughtful] اچھا سوال ہے… سوچ کے بتاتی ہوں۔",
            "[gently] ایک لمحہ…",
            "[thoughtful] ہمم، دیکھتے ہیں۔",
            "[gently] ذرا ٹھہریے…",
            "[thoughtful] اس پر ذرا غور کرتی ہوں۔",
            "[gently] ایک سیکنڈ دیجیے…",
            "[thoughtful] ہمم… دلچسپ۔",
            "[gently] سوچتی ہوں، پھر بتاتی ہوں۔",
            "[thoughtful] ذرا یاد کرنے دیجیے۔",
            "[gently] اچھا… ایک پل۔",
            "[thoughtful] دیکھتی ہوں، کیا کہا جا سکتا ہے۔",
        ],
    },
    "searching": {
        Companion.ALIF: [
            "[warmly] ذرا ڈھونڈ کے بتاتا ہوں۔",
            "[warmly] ایک منٹ، پتا کرتا ہوں۔",
            "[warmly] رکیے، دیکھ کے آتا ہوں۔",
            "[warmly] ذرا تلاش کرتا ہوں…",
            "[warmly] ابھی پتا لگاتا ہوں، ٹھہریے۔",
            "[warmly] دیکھتا ہوں کہیں مل جائے…",
            "[warmly] ذرا کھوج لگانے دیجیے۔",
            "[warmly] ایک لمحہ، معلوم کرتا ہوں۔",
            "[warmly] رکیے ذرا، ڈھونڈتا ہوں۔",
            "[warmly] اس کا پتا کرتا ہوں، ابھی آیا۔",
            "[warmly] ذرا کتابوں میں جھانک لوں…",
            "[laughs softly] رکیے، ابھی کھوج کے لاتا ہوں۔",
        ],
        Companion.TARANA: [
            "[gently] ذرا ڈھونڈ کے بتاتی ہوں۔",
            "[gently] ایک منٹ، پتا کرتی ہوں۔",
            "[thoughtful] رکیے، دیکھ کے آتی ہوں۔",
            "[gently] ذرا تلاش کرتی ہوں…",
            "[gently] ابھی معلوم کرتی ہوں۔",
            "[thoughtful] دیکھتی ہوں کہیں مل جائے…",
            "[gently] ذرا کھوج لگانے دیجیے۔",
            "[gently] ایک لمحہ، پتا لگاتی ہوں۔",
            "[gently] رکیے، ڈھونڈتی ہوں۔",
            "[thoughtful] اس کا پتا کرتی ہوں۔",
            "[gently] ذرا کتابوں میں دیکھ لوں…",
            "[gently] ابھی تصدیق کر کے بتاتی ہوں۔",
        ],
    },
    "affirm": {
        Companion.ALIF: [
            "[warmly] ہمم…",
            "[warmly] اچھا…",
            "[warmly] واہ!",
            "[warmly] جی…",
            "[warmly] بالکل۔",
            "[laughs softly] ہاں ہاں۔",
            "[warmly] اچھا اچھا۔",
            "[warmly] سبحان اللہ۔",
            "[warmly] ٹھیک، ٹھیک۔",
            "[warmly] ہمم، سمجھا۔",
            "[warmly] جی جی۔",
            "[warmly] واہ، کیا بات ہے۔",
        ],
        Companion.TARANA: [
            "[gently] ہمم…",
            "[gently] اچھا…",
            "[warmly] بہت خوب۔",
            "[gently] جی…",
            "[gently] بالکل۔",
            "[gently] ہاں۔",
            "[gently] اچھا اچھا۔",
            "[warmly] واہ۔",
            "[gently] ٹھیک ہے۔",
            "[gently] سمجھ گئی۔",
            "[gently] جی جی۔",
            "[thoughtful] ہمم، دلچسپ۔",
        ],
    },
}

CATEGORIES = tuple(CUES.keys())

# --------------------------------------------------------------------------- #
# Picker (avoid repeating the last phrase per category+companion)
# --------------------------------------------------------------------------- #
_last_pick: dict[tuple[str, Companion], str] = {}


def pick(category: str, companion: Companion) -> str:
    """Return a random cue phrase, avoiding the immediately previous one."""
    options = CUES[category][companion]
    last = _last_pick.get((category, companion))
    pool = [o for o in options if o != last] or options
    choice = random.choice(pool)
    _last_pick[(category, companion)] = choice
    return choice


def iter_all() -> Iterator[tuple[str, Companion, str]]:
    """Yield (category, companion, phrase) for every cue (used by precompute)."""
    for category, per_companion in CUES.items():
        for companion, phrases in per_companion.items():
            for phrase in phrases:
                yield category, companion, phrase


# --------------------------------------------------------------------------- #
# Summon detection ("Alif", "suno", "Alif suno" -> just a wake-cue, no LLM)
# --------------------------------------------------------------------------- #
# Tokens that are *only* a call for attention, across the scripts STT may return.
_SUMMON_TOKENS = {
    # roman
    "alif", "tarana", "suno", "sunno", "suniye", "suniyo", "sun", "suniyo",
    "o", "arre", "arrey", "hey", "oye", "jee", "ji", "haan", "han", "yaar",
    "idhar", "hello", "hi", "hii", "are", "acha", "achha",
    # urdu
    "الف", "ترانہ", "سنو", "سنیے", "سن", "او", "ارے", "جی", "ہاں", "ہیلو", "ادھر", "اچھا",
    # devanagari
    "अलिफ़", "अलिफ", "तराना", "सुनो", "सुनिए", "सुन", "ओ", "अरे", "जी", "हाँ", "हां",
    "हे", "इधर", "अच्छा",
}
_PUNCT = "؟،۔!?.,।…'’‘\"-"


def is_summon(transcript: str) -> bool:
    """True if the utterance is only a call for attention (so we reply with a wake-cue)."""
    toks = [t.strip(_PUNCT).lower() for t in transcript.split()]
    toks = [t for t in toks if t]
    if not toks or len(toks) > 4:
        return False
    return all(t in _SUMMON_TOKENS for t in toks)


# --------------------------------------------------------------------------- #
# Serving (cache-first synthesis -> instant)
# --------------------------------------------------------------------------- #
async def serve(category: str, companion: Companion, settings: Settings, tts) -> tuple[bytes, str]:
    """Pick a cue and return (audio_bytes, display_text_without_tags). Cache-first."""
    from aat.personas import get_persona

    phrase = pick(category, companion)
    persona = get_persona(companion)
    audio = await tts.synthesize(
        phrase,
        voice_id=persona.voice_id(settings),
        stability=persona.stability,
        language_code="ur",
        seed=persona.seed(settings),
    )
    return audio, strip_audio_tags(phrase)
