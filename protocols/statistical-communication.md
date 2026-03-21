# Statistical Communication Protocol

**Source:** Andrew Dilnot & Michael Blastland, *The Tiger That Isn't: Seeing Through a World of Numbers* (2007)

**Purpose:** Ensure statistics are MEANINGFUL, not just correct. The existing statistical-sanity.md checks whether numbers are *correct*; this protocol checks whether they *answer the right question* and *can be understood*.

---

## The Core Problem

> "Numbers have amazing power to put life's anxieties into proportion... Yet this power is squandered through an often needless misalignment of the way people habitually think and the way risks and uncertainties are typically reported."

Statistics often fail not because they are wrong, but because they:
- Answer a different question than the one being asked
- Lack meaningful comparison
- Are presented at a scale humans cannot grasp
- Count things that are poorly defined
- Mistake noise for signal

---

## The Five Core Questions

Before presenting ANY statistic, ask these five questions:

### 1. MEANING: Does this answer the actual question? (Mushy Peas)

**The problem:** Counting seems simple in the nursery (1, 2, 3...), but counting *something* requires squashing messy reality into neat boxes. What gets counted depends entirely on how it is defined.

**The metaphor:** Counting real things is like counting mushy peas. There is no "bureaucrat with a clipboard" recording everything. Most statistics involve estimates, samples, and definitions that may not match what you think is being measured.

**Ask:**
- What exactly is being counted?
- What is included? What is excluded?
- Does the definition match what people think it means?
- Could the same number be produced with a radically different definition?

**Example failure:** "1 in 4 teenage boys is a criminal" sounds alarming, but what counts as a "crime"? The definition made a sensation from mundane behaviour.

---

### 2. CONTEXT: Is there a meaningful comparison? (White Rainbow)

**The problem:** A number alone means nothing. Is it big? Small? We cannot tell without comparison. Yet numbers are routinely presented in isolation.

**The metaphor:** Averaging the colours of a rainbow produces white light. But this "average" tells you nothing about the vibrancy of the original colours. Similarly, a statistic without context bleaches out all meaning.

**Ask:**
- Is that a big number?
- Compared to what?
- What is the baseline?
- What would we expect by chance?

**Example failure:** "300 million for childcare!" sounds vast. Divide by 5 years, by 1 million places = 1.15 per place per week. Could you find childcare for 1.15/week?

---

### 3. SIZE: Can readers grasp this scale? (Man and Dog)

**The problem:** Numbers in millions, billions, or percentages are abstractions. Humans understand human-scale experiences. Large numbers need to be translated into something personal.

**The metaphor:** A man walks uphill with a dog on a long lead. In the dark, you can only see the dog's fluorescent collar. The dog zips up and down. Is the man walking uphill or not? Random variation (the dog) can obscure the underlying trend (the man).

**Ask:**
- Can the reader picture this?
- What does this mean per person? Per day? Per household?
- Is this the trend or just the noise?
- Would a real person recognise this in their life?

**Technique:** Personalise large numbers. "1.15 per week per childcare place" is more meaningful than "300 million."

---

### 4. COUNTING: What exactly is being counted? (Whole Elephant)

**The problem:** A single number captures one facet of a complex reality. Measuring one thing often causes unmeasured things to misbehave. Targets notoriously "hit the target but miss the point."

**The metaphor:** The Blind Men and the Elephant. Each touches one part - trunk, tail, tusk, leg - and concludes the elephant is like a snake, rope, spear, tree. Each is "partly right and all are wrong." One measurement cannot capture the whole.

**Ask:**
- What aspects does this number NOT capture?
- Could optimising this number make other things worse?
- Is this one part being mistaken for the whole?
- What gaming or distortion might this invite?

**Example failure:** Hospital targets for 4-hour waits led to patients being moved to specialist units (stopping the clock) even when A&E could have treated them faster.

---

### 5. CHANCE: Is this signal or noise? (The Tiger That Isn't)

**The problem:** Chance creates patterns that look meaningful. We are hardwired to find causes, even where there are none. Apparent clusters, trends, and correlations often arise by accident.

**The metaphor:** Throw rice on a carpet. The grains cluster randomly into patterns that look deliberate. A "cancer cluster" of 9 cases in 20 households near a phone mast looks sinister - but such clusters occur routinely by chance across a large population. The tiger we see in the bushes often isn't there.

**Ask:**
- Could this happen by chance?
- How many other places/times showed no pattern?
- Are we searching for explanations where none exist?
- Is this regression to the mean, not a real change?

**Example failure:** The "Sports Illustrated Cover Jinx" - athletes featured on the cover often decline afterward. But they made the cover because they were at a peak. From peaks, the only direction is down. No curse required.

---

## The 15 Principles (Quick Reference)

From the "Finally" chapter - one-liners for rapid recall:

| # | Principle | Meaning |
|---|-----------|---------|
| 1 | Size is for sharing | Personalise numbers to human scale |
| 2 | Numbers are neat. Life isn't | Reality is messier than any statistic |
| 3 | People count (with backache) | Data collection is hard, imperfect work |
| 4 | Chance lurks | Random patterns look meaningful |
| 5 | Stripes aren't tigers | Patterns dont prove causation |
| 6 | Up and down happens | Things fluctuate without any cause |
| 7 | "Average = middle" = muddle | Averages can be typical of no one |
| 8 | You can't see wholes through keyholes | One measure misses most of reality |
| 9 | Risk = People | Risk statistics concern real individuals |
| 10 | Most counting isn't | Most statistics are estimates, not counts |
| 11 | No data, no story | Without evidence, there is no claim |
| 12 | They don't know either | Experts are often as ignorant as us |
| 13 | Easy shocks are easily wrong | Outliers usually need higher proof |
| 14 | Thou art not a summer's day, sorry | Like-with-like comparisons only |
| 15 | This causes that - maybe | Correlation does not prove causation |

---

## Common Mistakes Catalogue

| Mistake | Example | Dilnot Fix |
|---------|---------|------------|
| **Isolated number** | "Risk up 42%!" | Give baseline AND absolute change |
| **Abstract scale** | "300 million for childcare" | Per person/day/week translation |
| **Fuzzy definition** | "1 in 4 teens criminal" | Specify what counts as "criminal" |
| **False comparison** | "US cancer survival 82%, UK 44%" | Check: same thing being measured? |
| **Outlier as typical** | "Temperatures could rise 11C" | Report most likely, not most extreme |
| **Trend from noise** | "Crime down this month!" | Is this the man or the dog? |
| **Causation from correlation** | "Loud music causes acne" | What else could explain this? |
| **Single facet for whole** | "Hospital waits down!" | What got worse while this improved? |
| **Ignoring chance** | "Cancer cluster near mast" | How many clusters expected by chance? |
| **Averaging away reality** | "Average tax rise 1800" | Who is actually typical? |

---

## Checklist for Data Analysts

### Before Calculating

- [ ] What question am I actually answering?
- [ ] Is this the question the reader cares about?
- [ ] What is NOT captured by this statistic?
- [ ] What definition am I using? Would others define it differently?

### Before Presenting

- [ ] Have I provided a meaningful comparison?
- [ ] Can a non-expert grasp the scale?
- [ ] Have I personalised large numbers?
- [ ] Could this pattern be chance?
- [ ] Am I mistaking correlation for causation?
- [ ] Is this an outlier being presented as typical?
- [ ] Am I comparing like with like?

### The "Man in the Pub" Test

If you explained this statistic to someone in a pub, would they:
1. Understand what is actually being measured?
2. Know whether it is big or small?
3. Know what to compare it to?
4. Be able to picture it in their own life?

If not, the statistic fails to communicate.

---

## Integration with Existing Protocols

This protocol EXTENDS, not replaces, existing quality gates:

| Protocol | Focus | Dilnot Adds |
|----------|-------|-------------|
| **statistical-sanity.md** | Is the number CORRECT? | Is it MEANINGFUL? |
| **data-handling.md** | Are calculations valid? | Do they answer the question? |
| **analytical-balance.md** | Both sides presented? | Comparisons fair and like-with-like? |

**Sequence:** First verify correctness (statistical-sanity), then verify communication (this protocol).

---

## Memorability Aids

The book's chapter titles are designed to stick:

| Chapter | Metaphor | Lesson |
|---------|----------|--------|
| Counting | Mushy Peas | Definitions matter |
| Size | Man and Dog | Distinguish trend from noise |
| Chance | The Tiger That Isn't | Random clusters look meaningful |
| Averages | White Rainbow | Averages hide variety |
| Targets | The Whole Elephant | One measure misses most |
| Risk | Bring Home the Bacon | Personalise risk |
| Sampling | Fire Hose | Few represent many (maybe) |
| Data | Know the Unknowns | Ignorance is widespread |
| Shocks | Wayward Tee Shots | Outliers need higher proof |
| Comparison | Mind the Gap | Like with like only |
| Correlation | Think Twice | Causation needs more than coincidence |

---

## When This Protocol Would Have Helped

**Kleinwalsertal analysis (Jan 2026):** Compared Lech (luxury international) to Kleinwalsertal (family German market). This is a "Mind the Gap" failure - unlike comparison presented as direct competition.

The mushy peas question: "What market segment does each serve?" would have revealed the comparison was invalid before any analysis began.

---

## References

- Dilnot, A. & Blastland, M. (2007). *The Tiger That Isn't: Seeing Through a World of Numbers*. Profile Books.
- Huff, D. (1954). *How to Lie with Statistics*. W. W. Norton.
- Gigerenzer, G. (2003). *Reckoning with Risk*. Penguin.
