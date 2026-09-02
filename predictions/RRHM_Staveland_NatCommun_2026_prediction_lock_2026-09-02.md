# RRHM Prediction Lock — Staveland et al. (Nature Communications, 2026)

**Timestamp (Bangkok): 2 September 2026, 17:01 ICT (UTC+7)**  
**Timestamp (UTC): 2 September 2026, 10:01 UTC**  
**Target paper:** Staveland BR, Oberschulte J, Berger B, et al. *Cortical-limbic circuit dynamics of approach-avoidance conflict in humans.* Nature Communications. 2026;17:3867. DOI: 10.1038/s41467-026-70287-5.  
**Status:** Ex ante prediction registry / adversarial forecast. This document does **not** claim that RRHM is validated, and it does not claim that the authors will necessarily observe these effects. The purpose is to create falsifiable, time-stamped predictions before the proposed analyses or follow-up experiments are reported.

## Why this paper is a decisive interlocutor

Staveland et al. report that theta coherence across a distributed cortico-limbic network is elevated during approach, falls during avoidance, and correlates with approach duration. They explicitly state that the information carried by theta remains open: candidate interpretations include cognitive control, reward, uncertainty, risk, threat, and conflict. RRHM proposes a narrower candidate variable for this unresolved computational content: the **remaining engagement-preserving regulatory recoverability margin**.

RRHM defines an estimated engagement margin:

\[
M_t^E=\widehat{eRRH}_t-\widehat{\tau}^{E}_{corr,t},
\]

where \(\widehat{eRRH}_t\) is the estimated remaining time during which an engagement-preserving corrective action is still expected to work, and \(\widehat{\tau}^{E}_{corr,t}\) is the estimated latency needed to execute that correction.

The core forecast is that approach-avoidance circuitry will align more closely to **proximity to loss of effective continued-engagement regulation** than to physical threat distance alone.

---

## Primary prediction P1 — Theta tracks recoverability margin, not merely threat proximity

In a future task that orthogonalizes physical threat imminence/probability from engagement-preserving recoverability, trialwise cortico-limbic theta coherence will be better predicted by \(M_t^E\) than by physical threat distance, reward magnitude, uncertainty, or conflict alone.

**Predicted pattern:**

- theta coherence will increase as \(M_t^E\) narrows during continued approach;
- the neural transition will align more tightly to a common recoverability-margin coordinate than to a common physical-distance coordinate;
- after commitment to defensive termination, this coherence will fall even if threat remains physically present.

**Falsifier:** after preregistered rival-model comparison, threat/imminence/reward/conflict variables fully account for the neural dynamics and a recoverability-margin variable adds no held-out predictive information.

---

## Primary prediction P2 — Same threat, same control, different engagement horizon produces different avoidance timing

A causal follow-up should hold constant:

- objective threat probability and intensity;
- physical threat imminence;
- number of available actions;
- perceived control;
- escape availability;
- reward structure;

while changing only how long an available corrective action remains capable of preserving continued engagement.

RRHM predicts:

\[
\text{shorter causal engagement-preserving horizon}
\Rightarrow
\text{earlier defensive transition}.
\]

The associated network transition should also occur earlier in time under the short-horizon condition.

**Falsifier:** defensive-transition timing and network dynamics are unchanged when engagement-preserving horizon is manipulated while conventional threat/control variables are matched.

---

## Primary prediction P3 — Restoring continued-engagement recoverability will delay avoidance more than termination-only control

Compare two conditions with the same number and salience of control actions:

1. **engagement-preserving action:** a pause/correction that restores task-compatible continuation;
2. **termination-only action:** a button that ends the trial but does not permit continuation.

RRHM predicts longer approach/persistence and a later network transition in condition 1, even when perceived control and escape availability are matched.

**Falsifier:** the two actions produce equivalent behavior once perceived control is matched.

---

## Secondary prediction P4 — MFG high-frequency activity will track loss of recoverability beyond threat proximity

Staveland et al. report sustained right-MFG high-frequency activity during imminent Ghost attack and a decline when successful escape becomes evident in Chase trials. A future experiment that holds physical threat constant but manipulates whether corrective action can still succeed should show that MFG high-frequency activity remains elevated when effective recovery is no longer available and falls when recoverability is restored.

This prediction is stronger than a generic "MFG tracks threat" account because the key manipulation is **recoverability at matched threat**.

**Falsifier:** MFG high-frequency activity is fully explained by threat proximity/probability and does not discriminate matched-threat states with different recoverability.

---

## Secondary prediction P5 — Clinical anxiety/phobia will show a left-shifted transition boundary

In a future clinical or high-fear sample performing a homologous task, RRHM predicts that excessive avoidance will not necessarily appear as greater neural response at every threat level. Instead, the **transition boundary will shift earlier**:

\[
\widehat{eRRH}_{clinical}<\widehat{eRRH}_{control}
\]

at the same objective task state.

Operationally, high-anxiety/phobic participants should turn away at a larger objective safety/recoverability margin than controls, and their neural switch from approach-maintenance to defensive-transition dynamics should also occur earlier.

A recoverability calibration error

\[
RCE=eRRH_C-\widehat{eRRH}
\]

should predict excessive avoidance beyond fear rating, trait anxiety, threat sensitivity, reward sensitivity, and perceived control.

**Falsifier:** conventional clinical variables fully explain the earlier avoidance boundary and RCE adds no incremental held-out prediction.

---

## Existing-data prediction P6 — Secondary analysis may reveal better alignment to a dynamic corrective-margin variable

The published Staveland et al. data and code are publicly available. A secondary analysis may construct task-state variables based on Pac-Man position, Ghost position/speed, attack probability, available turning/escape geometry, reward remaining, and time-to-outcome. This can test whether a dynamic **corrective-margin proxy** explains trialwise approach duration and neural synchrony better than raw distance or threat probability alone.

**Important boundary:** the current Pac-Man task was not designed to independently program organismic eRRH. Therefore any such variable is an exploratory **task-state proxy**, not direct measurement of \(eRRH_C\), and cannot by itself validate RRHM.

**Falsifier:** the proxy is non-identifiable, collapses mathematically into threat probability/distance, or fails out-of-sample comparison.

---

## Strongest future finding predicted by RRHM

The most diagnostic future result would be:

> **At matched objective threat, physical imminence, perceived control, escape availability, and action number, shortening the time during which continued-engagement correction remains effective causes both earlier behavioral avoidance and an earlier cortico-limbic network transition.**

If that result is observed reproducibly, it would support the hypothesis that a time-to-loss-of-engagement-recoverability variable contributes to approach-avoidance dynamics. It would still not, by itself, establish RRHM as a disease mechanism of specific phobia.

If that result fails under well-powered preregistered testing, the distinctive RRHM mechanism should be substantially weakened.

---

## Epistemic guardrails

1. These predictions are deliberately written before any RRHM-specific reanalysis of the Staveland dataset.
2. Findings already reported by Staveland et al. are treated only as the starting observation, not as successful RRHM predictions.
3. No post hoc redefinition of eRRH should be used to rescue failed predictions.
4. A GitHub commit provides a public version-history timestamp, but a formal OSF registration or immutable DOI-based archive would provide stronger preregistration provenance.
5. The predictions concern research mechanisms, not diagnosis or treatment recommendations.

**Prediction lock statement:** RRHM predicts that the unresolved information coordinated by the Staveland approach-avoidance circuit will prove to include a temporally defined estimate of remaining effective engagement-preserving recoverability, and that this variable will predict defensive-transition timing independently of conventional threat and control variables when the constructs are experimentally orthogonalized.
