# Project Genaris
# Consolidated World Laws and Simulation Doctrine — V0

**Purpose:** Detailed handoff to the Genaris project chat and foundation for architecture.

**Status:** Consolidated design baseline, not an implemented or tested engine. Includes explicitly accepted decisions, defaults selected under Sebastian's authorization to resolve the remaining register, and clearly labeled implementation clarifications. No further blanket approval loop is required to use this document for architecture.

**Source basis:** The Project Genaris concept brief read in this conversation, both earlier decision handoffs, the 40-section Master Open-Question Register, accepted topic packages, delegated remaining answers, and the final accepted revision to the observer/godlike role. This document is a new handoff; it does not claim to have updated files in the separate project chat.

## How the project chat should use this document

Use this as the consolidated baseline for the subjects it covers. Later explicit decisions supersede older proposals. Preserve the original aspiration of a living fantasy world, while applying the specific resolutions below.

Do not reopen settled preferences merely because an implementation requires parameters. Choose concrete implementations consistent with the rules, record those choices, and verify their behavior. Raise a new design question only when a genuine contradiction or materially different product behavior cannot be resolved within this baseline.

Three levels must remain distinct:

1. **World law:** What exists and what interactions reality permits.
2. **Simulation model:** How the engine represents and approximates those laws.
3. **Configuration:** Rates, thresholds, distributions, intervals, and initial conditions that can be tuned without changing the law.

The 40 numbered sections below correspond directly to the Master Open-Question Register. Cross-cutting doctrine is summarized first; numerical defaults, superseded ideas, remaining engineering work, and consistency checks follow the register.

## Core purpose and operating doctrine

Genaris is a living fantasy-world simulation. Establish laws, agents, resources, pressures, and initial conditions; let interacting processes produce history. Do not predetermine wars, heroes, religions, discoveries, or civilizational outcomes.

Begin with one small region containing a functioning ecosystem, approximately 100 social inhabitants, and three small communities. Expand after the seed simulation functions convincingly. The six organizing layers remain Reality, Physical World, Life, Mind, Society, and History; magic interacts across them.

| Doctrine question | Settled answer |
| --- | --- |
| Fully deterministic given a seed? | No. Partly reproducible: environmental and biological stochastic processes use seeded streams, while specified agent exploration and choices may use streams initialized independently per run. |
| Exact replay? | Not required. Support historical review through retained events, causal links, and snapshots. |
| Continuous entity existence? | Persistent individuals coexist with collectively represented populations. Established individual identities survive changes in calculation detail. |
| Time granularity? | Hybrid periodic updates and scheduled events on one global timeline. |
| Adaptive resolution? | Yes, according to world activity and accuracy needs, independent of observer attention. |
| Are outcomes generated first? | No. Major outcomes emerge from actual processes and decisions. |
| Incorrect beliefs? | Yes; they can influence actions and consequences. |
| Objective truth separate from beliefs? | Yes, and neither is automatically substituted for the other. |
| Complete historical archive? | No. Selective objective records plus separate in-world evidence. |
| Cultural forgetting? | Yes. |
| Independent rediscovery? | Yes; cultural naming does not establish a new objective capability. |
| Actual inherited information? | Yes, represented at a functional abstraction level. |
| Unexpected emergence? | Yes, within implemented capabilities and world laws. |
| Human role? | Observer combined with a godlike entity, able to intervene, manifest, bless, and curse. |

Exceptional individuals, extreme energy accumulation, abundance, collapse, and dangerous power imbalances are allowed. The engine must not secretly suppress them to restore narrative or game balance. Their consequences still require implemented mechanisms; the word emergence does not substitute for those mechanisms.

## 1. Reality, ontology, and souls

**Matter, energy, and magic.** Matter provides material structures. Energy is a measurable capacity for change. Magic introduces a field and additional interactions that carry energy, affect ordinary processes, sustain organized structures, and permit genuine creation of ordinary matter and energy. The magical field exists independently of life and remains present even where its available energy is depleted.

**Life.** Life is an organized, self-maintaining process. Biological, magically sustained, and soul-involving foundations may overlap within one being. Some organisms require magical energy to live; others do not. No universal vital force separate from the accepted structures is required.

**Consciousness.** Biological structures, magical structures, or coupled combinations can support a mind. A soul is not required for consciousness, and consciousness alone does not grant magical access.

**Souls.** A soul is a persistent, organized structure within the magical field capable of supporting mental processes and retaining individual identity. It follows world laws and can be altered, damaged, or destroyed. Beings possess souls where their development produces a stable soul structure; intelligence, moral worth, and a species name do not automatically determine possession.

A soul contains only the memories, dispositions, learned patterns, and mental processes actually encoded in it. It is not a perfect external backup. A being's mind can be distributed between body and soul, making the connections between them consequential.

**Continuity.** Personal identity follows causal continuity of the structures and processes supporting the individual. Sleep or recoverable dormancy preserves identity if the organization needed to resume remains intact. A functioning copy receives its own identity and shares an origin with the source; matching memories do not merge two independent beings into one person.

Magical life persists through maintained organization, usable energy access, and adequate stability. Sections 14, 15, and 21 specify reproduction, mental state, and death consequences.

## 2. Space, time, and causality

Physical space has three continuous spatial dimensions and is approximately Euclidean at ordinary scales. Simulation cells approximate regions; they are not literal blocks composing reality. Global world shape is an initial-world configuration rather than an additional magical law.

The past is fixed and there is one causal history per run. No rewriting events, backward travel, retroactive consequences, or in-world branching timelines is permitted.

**Distance manipulation** changes the physical length of a path through a bounded region. **Locality manipulation** establishes connections between separated boundaries so matter, energy, and signals can cross as though those boundaries were adjacent. These are distinct mechanisms.

Spatial effects require access to the region or endpoints. Extent, deformation, throughput, and precision determine support demands. They cannot silently duplicate matter or overwrite occupied space. When support ends, geometry relaxes and connections close; crossing matter resolves through that actual process into definite locations. Abrupt closure can displace or damage it, but cannot delete it from accounting.

**Local temporal rate manipulation is permitted.** Rates must remain finite and strictly positive: no complete stopping or reversal. All local processes experience the local rate, including thought, metabolism, motion, magical work, and field generation. A rate change cannot accelerate benefits while exempting ordinary costs.

Temporal boundaries have a finite transition region. Matter and transferred quantities remain continuous and accounted for when crossing. Volume, rate difference, boundary sharpness, duration, and changing conditions determine energy, control, and strain requirements. Extreme effects are difficult through these requirements rather than arbitrary personal caps.

All interactions advance along the global timeline. Spatial shortcuts cannot deliver consequences before their causes. Ending a temporal effect does not undo local elapsed experience. Global records retain event order; local elapsed time must be represented for affected processes.

## 3. Magic — fundamental energy

Magical energy is a distinct measurable quantity carried freely in the field or bound in matter. It is not simply another name for ordinary heat, motion, or a person's mental effort.

**Source and replenishment.** The field intrinsically generates magical energy at a regional rate. It requires neither an external realm nor an equivalent expenditure of ordinary energy. Regional generation rates are established during world generation. Generation continues where energy is already abundant.

**No equilibrium target.** There is no universal concentration cap, abundance-triggered generation cutoff, or automatic deletion to restore balance. Energy accumulates when generation and incoming transfers exceed use and outgoing transfers. Material saturation does not limit the amount in the surrounding field. Local concentrations can change through generation, transport, storage, expenditure, and release.

**Quantity and accounting.** Use one additive magical-energy quantity in consistent simulation units. Track free amounts by spatial region and bound amounts in their carriers. Concentration is free energy per represented volume. The same amount cannot appear in both reservoirs at once. Transfers debit the source and credit the received quantity at the destination; any difference has a named conversion or dispersion pathway.

**Movement.** Free energy spreads from higher to lower concentration at finite rates, affected by conductivity, barriers, and geometry. Compatible controlled interactions can redirect it. Distant access is not automatically granted by the ability to move energy.

**Availability.** Energy can become unavailable to magical use through defined expenditure or conversion. Storage leakage returns it to the surroundings unless an actual process converts it. There is no unexplained deletion. Numerical clamping is not a world sink.

**Ordinary generation restriction.** Only the field intrinsically generates new magical energy. Inhabitant techniques gather, store, transfer, and use it. Actual creation of ordinary matter and ordinary energy remains permitted, but this does not authorize an ordinary technique that manufactures fresh magical charge. Divine operations are the explicit external exception described in section 39.

Capacity, Flow, Affinity, Control, Perception, and Stability are not mandatory universal RPG statistics. Implement measurable properties needed by the accepted mechanisms; the old list does not become a fixed schema by implication.

## 4. Magic — resonance

Resonance is the physical compatibility between a structure and particular modes of the magical field. It determines the ability and efficiency of exchanging energy and sustaining interactions. It supplies access, not energy or a complete technique.

Represent it as a multidimensional continuous profile, including zero compatibility where applicable. Modes do not automatically correspond to elemental spell categories. Composition, internal arrangement, geometry, physical state, and biological tissue organization contribute.

Temporary physical-state changes can shift resonance temporarily. Lasting structural changes can shift it permanently. Magic can produce lasting shifts through completed transformations; a shift dependent on ongoing support ends or changes when that support disappears.

Different materials can have equivalent compatibility for particular modes while differing in capacity, strength, conductivity, and failure behavior. Similar resonance does not establish equivalence of complete techniques.

**Training and extraordinary development.** Practice, experimentation, adaptation, and transformation can deepen, broaden, and reshape resonance, including developing access to previously inaccessible modes. Inherited traits influence starting conditions and development but do not impose an immutable ceiling. Progress depends on effective methods, resources, adaptation, and surviving strain; it is not automatic or guaranteed.

An incompatible structure cannot perform an interaction in its present condition. It may become compatible through development or transformation. Merely adding energy does not automatically fix incompatibility.

Inherited structures can evolve resonance properties. Acquired mastery is not automatically inherited. Exceptional individuals may far exceed ordinary species capability without forced weakening or automatically generated rivals.

## 5. Magic — accumulation in matter

Composition and structure determine arrangements in which field energy can remain bound. Compatibility is necessary, but does not alone determine storage properties.

- **Capacity:** material amount, density of compatible binding structures, integrity, and physical state.
- **Absorption:** compatibility, exposed surface, conductivity, remaining capacity, and surrounding concentration. Absorption slows as stable storage fills.
- **Release:** binding strength, conductivity, release pathways, external concentration, and applied extraction. Forced extraction can exceed comfortable rates and cause strain or damage.
- **Leakage and losses:** ordinary storage leaks at material-dependent rates; some materials retain energy for extremely long periods. Absorption and extraction can disperse energy or convert part into heat.
- **Effects on material:** charge can change physical state and resonance. Mild effects may be reversible; intense loading can reorganize or damage structures. Lasting changes require actual structural alteration.
- **Changing capacity:** manufacture, repeated use, exposure, damage, development, and evolution can change binding structures. Repetition alone does not guarantee improvement.
- **Zero storage:** some materials retain effectively no magical energy while still transmitting, impeding, or otherwise interacting with the field.
- **Overload:** stable binding saturates. Additional energy remains free, passes through, or forces unstable states. Failure releases or transforms energy through defined pathways and may change future capacity.

Biological storage obeys these same principles. No global balance mechanism removes accumulating free energy when local materials fill.

## 6. Magic — equilibrium and strain

Strain is accumulated disruption caused by magical activity stressing a structure or sustaining a property outside its ordinary unsupported state. It is distinct from the available magical-energy quantity.

Strain can reside in a practitioner, target, channeling material, or local field, according to each participant's role. Rapid change, excessive throughput, sustained unsupported conditions, instability, and poor control impose load. Load need not become damage or accumulating strain when the structure can comfortably sustain it.

Tolerance depends on structure, condition, compatibility, and prior adaptation. Suitable manageable exposure followed by recovery can strengthen structures; excessive exposure can weaken or destroy them. There is no balancing rule that increases strain merely because an individual is powerful.

When support ends, unsupported properties relax through their actual behavior. Recoverable disruption subsides; associated stored energy transfers, converts, or releases. Damage already done remains. Completion of a task does not imply recovery of its participants.

Recovery depends on structure, severity, environment, and continued load. Mild disruption may recover through rest; structural damage requires repair. Consequences include temporary impairment, lasting damage, and catastrophic failure. Failures propagate through actual connections, transferred loads, and released energy rather than arbitrary nearby penalties.

Maintain distinct strain modes where recovery or failure differs, including structural deformation, biological disruption, and field instability. A single universal damage meter must not erase meaningful differences. Strain is not itself an unaccounted energy reservoir that can be converted into free energy by releasing it.

## 7. Magic — creation of matter and energy

Creation genuinely adds ordinary matter or energy. It is not necessarily conversion of an equivalent existing ordinary supply. An inhabitant must establish the necessary resonance, provide positive magical expenditure, and maintain adequate control.

Costs depend on quantity, composition, organization, precision, rate, and technique efficiency. There is no requirement of equality between magical expenditure and ordinary energy produced. There is also no zero-cost ordinary creation: mastery reduces waste and demands without removing every requirement.

Amount is limited by accessible magical energy, throughput, control, and strain tolerance rather than a universal personal quota. Rate increases throughput demands and may increase losses or strain. Some coordination demands scale nonlinearly. Dividing work can help where the intended output permits it.

Material difficulty follows composition and structure, not economic rarity or cultural value. Organized outputs require more information and control than raw material. Remote creation requires establishing access at the destination; distance control is an additional demand rather than an automatic privilege.

Creation imposes load and produces strain when participants cannot comfortably sustain it or the interaction becomes unstable. Output occupies space and has its actual heat, motion, pressure, composition, and other represented properties. Resulting displacement and reactions affect the surroundings.

Created matter can possess unusual resonance when its manufactured structure supports it. It can carry magical charge only by receiving existing magical energy, absent an explicit divine operation. Creating a charged object must account for the material and the charge separately.

Living material is possible when the process supplies viable organization and conditions. A body does not automatically receive a soul, memories, or an existing person's identity.

Templates and self-organization may supply detail the practitioner does not explicitly understand. No process guarantees a specified unknown blueprint or factual memory without an informational source. Accidental patterns and newly generated ideas remain possible.

Ordinarily self-supporting output is a completed change. Output dependent on magical support retains that dependency. Abundance and its economic or ecological consequences are allowed to emerge.

## 8. Magic — permitted interaction classes

The fundamental classes are:

1. Energy transfer and conversion, subject to the magical-energy generation restriction.
2. Forces and motion.
3. Material structure and composition.
4. Spatial geometry and connections.
5. Local temporal rate.
6. Creation of ordinary matter and energy.
7. Manipulation of the magical field and its organized structures.

Access to one class does not automatically grant access to the others. They share accounting and strain rules but remain mechanistically distinct.

Motion and spatial distance map to fundamental classes. Density, separation, vibration, decay, heat, pressure, and structure describe properties or processes affected through classes; each need not be its own force. Memory and perception follow section 16 rather than being granted solely because they appeared in an old example list.

Interaction requires a functioning way to establish and control it. This can arise through instinct, imitation, practice, or experimentation without a correct scientific theory. Deeper understanding improves prediction and technique design; complex operations need operational information and compatible structures, not vocabulary alone.

Intent directs control processes. Reality responds to the operation actually established, including mistakes. It does not interpret wishes to supply missing mechanisms or information.

Discoveries can expose new applications and combinations of these laws. New fundamental classes require an explicit law revision, not an unexplained emergent exception.

## 9. Magic — technique structure

A technique is a repeatable procedure specifying interactions, arrangement, sequence, prerequisites, and control. Its objective identity is separate from names, cultural explanations, discovery provenance, and an individual's execution skill.

A distinct capability requires a mechanistic difference that materially changes its possible targets, requirements, consequences, or failure behavior. Cosmetic gestures, naming, and output-strength settings do not automatically produce new capabilities. Efficiency, precision, scale, throughput, and stability improvements are refinements unless the mechanism itself changes consequentially.

Equivalent independently discovered procedures can share an objective technique identity while retaining separate historical origins. Equivalence must be established from mechanisms and behavior; uncertain cases remain explicitly unclassified rather than falsely merged. This uncertainty is an engine knowledge/classification issue, not an unresolved user preference.

Techniques may combine mechanisms or invoke other techniques. Account for timing, energy, and strain across components without counting the same operation twice. Shared outputs such as concealment do not make pigmentation change, light redirection, and sensory interference identical abilities.

Every physically accessible, observable, and controllable interaction is discoverable in principle. Discovery is not guaranteed, nor is every interaction accessible to every organism or civilization.

Form describes spatial and temporal arrangement. A medium contributes the actual properties of the structures carrying the operation. Constraints require real enforcement, including bounded areas, durations, and transfer limits. Intent describes the practitioner's goal and control. The old five-part formula is not a mandatory technique schema.

## 10. Completed changes versus supported effects

A completed result continues under the world's ordinary processes without the particular interaction sustaining it. It may still cool, decay, react, or move; completed does not mean everlasting.

A supported effect depends on an ongoing magical interaction. Its support can come from a practitioner, artifact, organism, or environment. Leaving a practitioner's attention does not automatically terminate it.

The ordinary state follows current composition, structure, surroundings, and laws. It is not a stored pre-spell appearance to which everything resets. Completed structural transformation can make a previously supported property ordinary for the new material.

Interrupted transformations preserve work actually completed. Unsupported portions relax. Partial outputs may stabilize, continue reacting, or fail. Residual damage and strain follow their own recovery processes.

Composite effects track completed and supported components separately. Removing support affects dependencies and consequent interactions, not an automatic rollback of history.

## 11. Life and heredity

Use a structured genome of heritable parameters and developmental rules describing functional biological structures and regulatory relationships. Molecular DNA simulation is unnecessary. Inheritance must cause traits through consistent development rather than merely assigning offspring unrelated labels.

Development combines genome, nutrition, environment, exposure, age, and condition. Identical genomes need not produce identical individuals.

Mutation can alter parameter values, duplicate or remove modules, and modify regulation. Seeded random mutation operates during reproduction and specified damage/exposure processes according to relevant conditions. It does not anticipate an organism's needs. Effects may be beneficial, neutral, or harmful depending on context.

Compatible parents contribute modules according to their reproductive mechanism. Asexual reproduction copies one source with possible variation. Development, injury, experience, and training can change phenotype without changing inherited information.

Preserve parentage, genome versions, and traceable changes. Collectives retain the genetic variation and ancestry information needed for their represented processes; they must not collapse to a mean genome where rare inherited variants matter. Exact individual ancestors cannot be claimed where only collective ancestry was represented.

## 12. Magic and evolution

Exposure can alter tissue, development, regulation, or inherited information according to the interaction, dose, duration, and organism's condition. It can increase mutation rates when it disrupts copying or preservation structures, without guaranteeing useful adaptations.

An induced change becomes heritable only when it changes information or persistent regulatory state actually transmitted through reproduction. Altering ordinary body tissue alone is insufficient. Record the transmitted module, parameter, connection, or regulatory state affected; offspring develops from that change rather than receiving a copied adult trait.

Persistent magical conditions can create niches. Inherited adaptations may remain after the original exposure ends; their frequency then follows costs, benefits, reproduction, selection, and chance.

Evolution can develop access to previously unused field modes and combinations, but cannot create a new fundamental law. Extraordinary trained resonance is not automatically inherited.

## 13. Deliberate biological transformation

Self-transformation and transformation of other organisms are permitted through supported interactions with the affected structures. Lasting changes need viable resulting organization; other changes may require continued support.

Access, compatibility, precision, energy, throughput, control, defenses, and strain determine feasibility. Consent is not a physical prerequisite; its ethical and social significance belongs to inhabitants and institutions. Defenses must operate through actual mechanisms.

Transformation may affect phenotype, transmitted information, or both, under the heredity rules. Coordinated changes may be necessary across organs. Operational information can come from study, observation, templates, or evolved mechanisms. Intent alone does not specify unknown viable anatomy.

Transformation may produce exceptional capability without balancing penalties. Identity follows continuity of the mind-supporting organization. Bodily changes may preserve identity; changes to mental structures can alter personality, remove memories, or end continuity. A soul preserves only what is actually encoded within it and requires functioning connections where the mind depends on the body.

Failed or interrupted work follows section 10, including impairment, instability, and death where actual dependencies fail.

## 14. Non-biological and magical life

Magical life can originate naturally or through construction when field/material interactions produce stable self-maintaining organization. Suitable conditions permit formation but do not guarantee it.

An individual has a coherent structure or boundary, regulated exchanges, responses to conditions, and internal maintenance. Persistence alone is insufficient. Neither consciousness nor reproductive capability is required in every individual.

Such life acquires usable energy and any materials its structure requires. It does not independently generate magical energy outside the field-generation law. Energy access can be a continuing environmental dependency.

Reproduction may use budding, division, assembly, or combination of compatible beings. Transmitted patterns govern structure, resonance, regulation, maintenance, and behavior; personal memories are not automatically inherited. Reproducing populations can evolve through variation and differential survival/reproduction.

Health includes coherence, regulation, energy access, and functional integrity. Damage disrupts these or their stored information. Repair needs sufficient surviving organization to guide it plus resources; it cannot automatically recover information that has no remaining source.

A surviving parent retains identity when producing independently functioning offspring. Complete division ends the parent and creates descendant identities. In the latter case, record continuity of lineage without claiming one person exists simultaneously as multiple independent individuals.

Magical life may possess cognition, consciousness, and souls where its organization supports them, without these being automatic properties of anything magical.

## 15. Mind and consciousness

Cognition processes information and directs behavior. Sentience denotes subjective experience; self-awareness denotes a representation of oneself. These distinctions do not require a human template or guarantee that every capacity appears together. The engine models functional properties without claiming to prove subjective experience.

Preserve retained memories and beliefs, learned capabilities, dispositions, interpreted relationships, active goals, and the condition/connections of their supporting structures. Preserve body, magical, and soul components separately where partial loss can have consequences.

Different organizations can support different senses, motivations, memory structures, and reasoning. Nonhuman intelligence is explicitly permitted. Identity follows sections 1 and 21, not the presence of a display name or an unchanged personality vector.

## 16. Magic and information

Magic can access memories through compatible interaction with their biological, magical, or soul carriers. Access requires sensitivity and interpretation of the encoding. It reveals stored content, not guaranteed historical truth.

Environmental traces can be recovered where actual surviving changes contain recoverable information. Traces may be partial, ambiguous, degraded, or overwritten. No universal complete recording accompanies every event.

Magic cannot retrieve factual information with no surviving physical, mental, written, magical, or other source. Reconstruction from evidence is inference and may be wrong. The world does not require erased information to remain fundamentally recoverable elsewhere.

Information interaction operates through carriers. Reading, copying, modification, and erasure require supported mechanisms. Meaning alone is not a separate force. New patterns and ideas may arise through computation, combination, experiment, or randomness; a specified unknown fact cannot be guaranteed without evidence.

Perception can be altered by changing signals, sensory structures, or their processing. Memories can be copied or modified with suitable access and control. Copies do not transfer identity; alterations can cause contradictory beliefs or functional damage.

Limits include compatibility, access, signal quality, encoding complexity, precision, energy, and strain. Access is not automatic comprehension. The observer archive lies outside inhabitant information pathways; ordinary magic cannot query it.

## 17. Perception

Observations arise from sensory structures, location, environment, attention, and condition. They have finite range, sensitivity, resolution, and processing capacity. Noise, obstruction, distraction, injury, and unfamiliarity can cause missed or false interpretations.

Species inherit different sensory structures; development, experience, adaptation, and damage produce individual differences. Magical perception requires compatible detectors. An organism may detect concentration, certain resonance responses, or instability without detecting all three or receiving exact values.

Active probing may be needed to estimate resonance. Strain is inferred from manifestations rather than automatically revealed as an exact universal measurement. Observations preserve time, source, and uncertainty. Recognition depends on learning or inherited recognition mechanisms.

## 18. Memory

Represent episodes, learned facts and associations, procedural skills, and spatial knowledge. Memory stores experienced content and interpretation. Attention, novelty, emotional significance, repetition, and relevance influence encoding.

Forgetting follows weak encoding, interference, disuse, decay, and damage. Rehearsal and reminders can strengthen retention. Recall reconstructs from surviving content, permitting merged details and later reinterpretation.

Confidence and accuracy are separate. Contradictory memories can coexist. Long-lived individuals summarize routine episodes into patterns while preserving selected significant experiences. This loses detail and can retain bias; it cannot be treated as lossless compression.

Skills have their own practice and retention behavior. Forgetting the episode in which something was learned need not erase the skill.

## 19. Beliefs and inference

Beliefs are claims with confidence, provenance, supporting/conflicting evidence, and time relevance. Distinguish direct observations, remembered reports, inferred conclusions, and assumptions.

Agents reason through their available concepts and learned relationships. Belief revision depends on evidence quality, source trust, prior commitments, emotional significance, personality, and reasoning ability. Authority influences credibility without guaranteeing truth.

Agents can maintain competing explanations, suspend judgment, or reject accurate evidence. Public statements can differ from private beliefs under social pressure or deception. Changed beliefs may affect dependent conclusions, but agents need not recognize every contradiction immediately.

## 20. Communication and emergent language

Begin with signals supported by organism bodies: sound, movement, touch, chemicals, or compatible magical signaling. Initial tendencies may communicate simple states without a complete language.

Shared meanings arise through repeated associations, imitation, coordination, and feedback. Vocabulary develops around repeatedly distinguished experiences. Grammar consists of learned combination and ordering patterns useful for communication, without a mandatory human grammar.

Each agent has its own expression-to-concept mappings. Engine concept identifiers do not grant agents universal translation. Languages change through imperfect learning, innovation, migration, and differentiation; isolation can produce unintelligibility.

Translation begins through shared situations, demonstrations, pointing, repeated interaction, and correction. It remains uncertain when conceptual systems differ. Writing arises when durable marks acquire shared associations with quantities, objects, expressions, or sequences, requiring suitable materials and learning.

Dead languages persist in inscriptions and residual interpretive knowledge. Decipherment requires evidence. Initial implementation can support a small compositional signal system; sophisticated language requires explicit learning mechanisms rather than narrative claims of emergence.

## 21. Death

Biological death is loss of integrated self-maintenance beyond resumption by the organism's remaining unaided processes. Some tissues and mental structures can remain recoverable. Death of magical life is collapse of integrated organization; recoverable dormancy is distinct.

Soul separation is the end of its functional connection with a body or other supporting structure. Survival depends on remaining organization and energy access. A separated soul may continue, deteriorate, enter structurally supported dormancy, or disintegrate.

Consciousness survives body death only where sufficient functioning mental organization survives elsewhere. Memories and personal identity persist only to the extent their actual carriers and continuity persist. A soul does not guarantee preservation of the whole person.

**Reincarnation exists as a possibility:** a surviving soul can connect viably to a new body. It is not guaranteed or allocated by an automatic cosmic authority. What the person remembers depends on retained encoding and new access.

**Resurrection exists as a possibility:** repair of a body and connections can resume an individual when enough of the original organization survives. If continuity is completely lost, construction from an external description produces a new individual. Magical creation of a similar body does not by itself restore the original person.

There is no automatic universal afterlife or moral sorting. Communities of surviving dead may arise where conditions support them. Gods or inhabitants may deliberately create suitable environments, but that is an actual later intervention, not a hidden preexisting system.

Post-death outcomes vary by foundation. Lost information cannot be retrieved from the observer archive by an ordinary inhabitant. Divine grants are explicitly documented external acts rather than retroactive claims of natural resurrection.

## 22. Individual versus collective simulation

Individually track beings with personal learning and decisions and objects/organisms whose distinct condition, relationships, or actions require it. Represent suitable widespread populations through counts, distributions, and shared processes, retaining variation needed for evolution and rare outcomes.

Individualization is triggered by a world interaction needing specific continuity: a lasting relationship, distinct behavior, consequential injury, or individual movement/use. Observer attention alone is not a trigger.

A new individual drawn from a collective must fit its current distributions and established constraints, with the collective adjusted to prevent double counting. Retain origins and lineage facts already represented; do not invent particular untracked past actions, relationships, or discoveries. Unspecified history remains unspecified.

Inactive individuals retain identity, location, condition, relevant inheritance, retained mental state, relationships, ownership links, ongoing effects, and pending events. Elapsed processes must still be accounted for.

Routine calculation can later use aggregates if safe, but established individual records remain and must incorporate intervening effects. If aggregation would erase consequential differences, dependencies, or identity, retain separate calculation. A population-level mortality result cannot silently remove tracked people without resolving their outcomes.

## 23. Adaptive resolution

Required detail follows rates of change, consequential thresholds, interactions, and uncertainty of coarse approximations. Fast, unstable, or tightly coupled processes require finer calculation, independently of observation.

Refine before a coarse interval risks skipping a consequential transition. If the risk cannot be bounded, use finer calculation. Coarsen only where subsequent interactions can still be supported by retained state; quietness alone does not establish safety.

Preserve identities, relevant individual state, population variation, accounted matter/resources/energy, effects and strain, relationships, pending events, and retained causal links. Replace representations at a shared time and validate accounting before the replacement becomes authoritative.

Detailed expansion restores persistent individuals and samples previously collective members consistently with retained constraints. No impossible detailed prehistory is invented. Compression preserves relevant distributions and correlations; retain detail that cannot be safely compressed.

Boundary exchanges are explicit and time-aligned. Do not count a transfer twice. Refine both sides where their interaction requires it. Archive aggregate origins honestly rather than inventing specific individual causes.

Coarse and fine results need not be identical. They must preserve invariants and defined accuracy bounds, without systematic favoring of outcomes or removal of represented rare possibilities. Recalculate uncommitted inadequate intervals more finely; never silently rewrite established history after committing consequences.

## 24. Simulation time

Use one global timeline represented as integer elapsed units from the starting epoch. The smallest addressable interval is one microsecond. Calendar labels are derived. Microsecond precision does not require whole-world microsecond updates.

Periodic processes include energy generation/transport, metabolism, growth, recovery, weather, and population change. Scheduled events include arrivals, completions, births, deaths, expiration, and predicted threshold crossings. Predictions must be revised when conditions change.

Initial maximum update intervals are 0.1 seconds for active physical/magical interaction, one minute for routine needs/decisions, ten minutes for environmental conditions, and one hour for growth/slow population processes. These are tunable maxima, not permission to miss an earlier relevant event.

Use actual elapsed duration, including local experienced duration under temporal effects. Fewer updates must not reduce accumulated generation, aging, expenditure, or recovery. Event deadlines interrupt periodic intervals.

Independent simultaneous events can resolve together. Competing actions use a joint conflict rule based on the same preceding state; incidental thread or entity iteration order must not pick winners. Causes precede consequences even at the same timestamp through explicit internal ordering.

Immediate bookkeeping can share timestamps. Actions, propagation, and repeatable processes require positive duration, preventing infinite zero-time chains. Event prerequisites are checked at execution; changed prerequisites invalidate or reschedule them.

Pause and acceleration change processing pace, not laws, probability, priority, or required accuracy. If the machine cannot sustain the requested speed, the simulation runs more slowly rather than silently changing reality.

## 25. Determinism and randomness

Seeded streams govern world generation, environmental variation, inheritance and recombination, developmental variation, and collective sampling. Their choices are reproducible for identical inputs under the same implementation.

Individual exploration, experimentation, and selection among similarly preferred actions may use streams independently initialized per run. A world seed alone does not specify those choices. Actions can subsequently change environmental and evolutionary inputs, so a seeded subsystem's later results can still differ across divergent runs.

Needs, beliefs, capabilities, and goals constrain action before random selection. Randomness belongs to a defined process with eligible outcomes and condition-dependent probabilities; it does not generate unsupported powers or demand a historical result.

Use separate streams by system and persistent entity so unrelated random draws do not shift each other's sequences. Saves retain stream states; resumption does not silently reseed.

For consequential archived choices, retain realized outcome, relevant inputs, eligible alternatives and probabilities or selection-rule version, time, and originating process. Routine low-level draws can be summarized by interval, distribution, and aggregate result. Mark missing fine detail explicitly.

Testing can force normally run-variable streams into fixed initialization, with controlled inputs and ordering. This provides test reproducibility, not a blanket exact historical replay promise.

No hidden balancing of chances to suppress power, rescue civilizations, or force variety.

## 26. History archive

Archive births/deaths of tracked individuals, discoveries, lasting relationships and institutional changes, consequential migration/conflict/failure/environmental changes, and substantial changes in individual capability or condition. Summarize routine activity unless retained as a contribution to a significant event. Divine interventions are always significant.

Events reference actual prior events, actions, and conditions used by the generating process. Link roles distinguish triggers, enabling conditions, resource contributions, constraints, and probabilistic influences. Retain multiple contributions without inventing a single primary cause or unsupported responsibility percentages.

Keep direct links among archived events, enabling long chains. Routine intermediates can be summarized with their contributions and inputs. Causal depth is bounded by retained evidence, not a predetermined universal number of ancestors.

Initial snapshot cadence is daily plus explicit saves, clean shutdowns, and before model migration. Include objective state, individuals/collectives, retained mental state, magical energy and strain, ongoing processes, pending events, stream states, and applicable model/configuration versions.

Keep a rolling detailed trace for 30 simulated days. Later significant events can promote earlier contributors from that window. Discarded detail beyond it cannot be recovered or invented.

Retain daily snapshots for 30 days, monthly snapshots for ten years, and annual snapshots afterward. Explicitly preserved investigation snapshots remain. Retained historical events and causal references are not automatically discarded when nearby fine snapshots expire.

Compress and partition records by time; index entities, places, and causal references. Preserve semantics of retained records. Significance rules and retention parameters are versioned and tunable. A seemingly minor old cause may be unrecoverable; the archive must admit that limit.

## 27. Historical review and replay

Review provides retained snapshots, events, causes, consequences, participants, relevant conditions, and visible evidence limits. Navigate from an event to its dependencies and outcomes and compare state at available snapshots.

Show intermediate state only where retained evidence supports reconstruction. Otherwise mark it unknown or estimated. Do not present interpolated display animation as exact recovered history.

Exact replay is deliberately not required. It can be reconsidered only as a separate feature decision supported by an actual need. Historical investigation must function without promising every intermediate state or random draw.

## 28. In-world evidence

Traces include remains, tracks, scars, displaced materials, altered terrain, artifacts, writings, and surviving magical structures/disturbances. They contain information actually encoded by their origin, not a complete hidden event recording.

Durability, environment, disturbance, maintenance, and decay determine persistence. Records may fade, burn, fragment, be copied incorrectly, or be deliberately falsified.

Artifacts provide information through manufacture, wear, repairs, contents, inscriptions, and represented use/ownership effects. Merely possessing an engine ownership history does not make every prior owner magically readable from the artifact.

Agents assess trust using provenance, consistency, comparison, reputation, and expertise. Magical analysis can access otherwise hidden traces but remains source-bound and fallible in interpretation.

## 29. Cultural knowledge

Knowledge exists in actual carriers: people, records, practices, tools, and institutions. A culture-level index locates carriers without granting their contents to all members.

Transmission succeeds when the learner acquires enough to retain and use the relevant knowledge. Hearing words is not mastery. Teaching, apprenticeship, imitation, texts, rituals, and institutions have distinct error and loss opportunities.

Active cultural loss occurs when no member or functioning practice retains the knowledge. Unread records may remain as dormant evidence. Fragments can preserve terms, steps, examples, or false explanations.

Objective provenance distinguishes surviving transmission from rediscovery where evidence supports it. Inhabitants may incorrectly claim novelty or descent. Observer records do not prevent cultural forgetting.

## 30. Social emergence

Foundations include individual recognition, remembered interaction, communication, exchange, cooperation, threat avoidance, competition, dependent care, and responses to obligation.

Relationships are directional and multidimensional: trust, attachment, fear, rivalry, obligation, familiarity, and recognized kinship need not match in both directions. Biological kinship and believed kinship are separate.

Groups form through repeated association and reasons to coordinate or remain together. Membership can be fluid or disputed. Authority may arise through competence, influence, dependence, coercion, procedures, or resource control.

Institutions exist when roles, procedures, resources, and expectations persist beyond a particular encounter. Recruitment, succession, records, training, and continued participation permit survival beyond founders. Coordination uses communication networks, conventions, delegation, schedules, and enforcement, retaining delay and misunderstanding.

## 31. Settlements and civilization

A settlement is a persistent concentration of habitation and recurring activity supported by maintained locations or infrastructure. Temporary gatherings alone do not qualify.

Formation, growth, division, merging, migration, and collapse follow changes in resources, population, infrastructure, security, and social organization. Possession, effective control, and recognized ownership are separate state and belief relationships.

Occupations emerge from recurring work. Specialization follows skill, demand, opportunity, and exchange. Trade begins with transfers and negotiated exchange; markets, credit, currency, and trade institutions require adoption and maintenance.

Political structures emerge from recurring collective decisions and authority. Laws are communicated rules with procedures or enforcement; compliance depends on incentives, legitimacy, ties, and coercion. Military organization requires recruitment, training, supply, coordination, and command.

Classes arise through persistent differences in resources, status, rights, and access, including intergenerational transmission. Religious institutions arise when beliefs and practices develop enduring roles, resources, and authority; beliefs are not automatically true.

Guilds and magical institutions can form around training, facilities, standards, protection, and restricted knowledge. No institution is a guaranteed milestone or preset future destination.

## 32. Magic as culture and science

Discovery occurs when an individual learns a reproducible relationship between action, conditions, and observed effect. Experimentation aims to reduce uncertainty or test an expectation. Ordinary activity can yield accidental discovery.

Record failed attempts in the individual's accessible terms: observation, expectation, and changed conditions. The agent can misdiagnose failure. Technique knowledge includes operational steps, conditions, control skills, expected outcomes, and confidence; a known description is not execution ability.

Teaching uses explanation, demonstration, feedback, and practice, subject to equipment and compatibility. Transmission can omit steps, introduce errors, or preserve a working procedure under an incorrect theory.

Theories relate observations and generate predictions. Successful practice does not establish every accompanying claim. Schools develop through divergent evidence, traditions, methods, and networks. Secrets and taboos persist through access, trust, enforcement, and reproduction difficulty; they may leak, disappear, or be independently rediscovered.

## 33. Ecology and environmental simulation

Use spatial quantities/distributions for soils, water, nutrients, vegetation, and widespread resources, with persistent individuals where needed. Food webs represent actual consumption relationships, energy needs, and material transfers.

Explicit processes include growth, feeding, predation, competition, reproduction, mortality, decomposition, nutrient cycling, and dispersal. Regeneration requires actual inputs and conditions.

Geological deposits are non-renewable on biological timescales unless a represented geological, magical, or divine process produces more. Creation can change scarcity; the engine must not secretly preserve it.

Exposure affects survival, growth, development, mutation, and niches through the agreed interactions. Environmental magic follows generation, transport, storage, use, and release without a stabilizing concentration cap.

Local extinction means no viable local population remains. Global extinction requires loss of all represented viable populations and reproductive reservoirs. Collapse follows dependencies. Recovery requires survivors, migration, dormant reserves, actual new formation, or an explicit intervention—not automatic respawning.

## 34. Weather and mundane physical approximation

Use regional climate with causal local variation instead of a full atmospheric solver. Track temperature, moisture, precipitation, wind, pressure differences, surface water, soil moisture, and relevant snow/ice.

Terrain, elevation, seasons, sunlight, and neighboring regions influence conditions. Begin near 100-metre environmental cells in the initial region, refining around fires, flooding, structures, and concentrated magic where needed.

Use simplified heat transport, water flow, evaporation, infiltration, and combustion. Explicitly track quantities where survival, resources, or causal consequences depend on them. Light, sound, pressure, and detailed mechanics can use local calculations rather than universal fine simulation.

Magic modifies the same physical quantities. Magical heat can ignite fuel, alter airflow, and evaporate water through shared rules. Disasters arise from conditions and defined stochastic processes, not drama selection.

## 35. Agent behavior and cognition

The minimum model includes observations, retained knowledge, needs, capabilities, relationships, goals, and available actions. Needs reflect changing organism-specific internal conditions with actual consequences.

Goals arise from needs, rewards, commitments, curiosity, relationships, threats, and opportunities. Prioritization uses urgency, expected benefit, feasibility, risk, obligation, and personality, evaluated from the agent's beliefs.

Personality is a set of persistent but developable tendencies, not an immutable moral alignment. Skills develop through practice, feedback, and adaptation, with transfer, interference, plateaus, and possible decay. Lifetime learning includes associations, maps, procedures, expectations, social judgments, and concepts.

Inheritance supplies capacities and predispositions; experience supplies learned knowledge and development. Routine actions use inexpensive logic. Novel problems, long plans, negotiation, and experiments receive richer computation where useful.

The authoritative simulation requires no LLM calls. An optional LLM may summarize observer records. Future LLM-generated agent proposals receive only that agent's accessible information and remain subject to ordinary action validation. Narrative text cannot directly create world facts or grant unsupported actions.

## 36. Ground-truth event causality

A causal link is recorded because a generating process actually used the referenced state, action, or earlier event. Multiple roles can coexist. Distinguish rule-required prerequisites from factors affecting probability. Correlation alone is not sufficient.

Do not manufacture a single elegant explanation for complex outcomes. Do not label a factor counterfactually necessary merely because it was present; that stronger claim requires a rule or an actual supported analysis.

A continuous process becomes a historical event at a consequential threshold, persistent state transition, or onset/end of a sustained condition. Record interval and relevant measurements; event labels summarize the process rather than causing it.

Causal records describe the represented model and retained evidence, not an omniscient claim about discarded detail. Divine interventions use explicit external causal origins and link to subsequent ordinary consequences.

## 37. Initial-world state

Generate a region from a seed within configured size, climate, resource, and magical-generation bounds. Begin with differentiated organisms and a functioning ecosystem rather than the origin of life.

Use approximately 100 social inhabitants across three small communities. Give them basic survival skills, simple tools, relationships, and limited oral communication consistent with their conditions. Communities share a small ancestral communication system with local variation.

Basic cooperation exists, but no preset kingdoms, guilds, academies, or developed magical science. Innate magical behavior is allowed where biology supports it. More complex language, writing, institutions, and magical knowledge can develop through represented processes.

The world predates the recorded run. Time zero starts recorded simulation, not the universe. Initial ages, parentage, knowledge, resources, and relationships must be consistent. Unsimulated prehistory is labeled initialization, not fabricated as a chain of simulated events.

Initial conditions set pressures and opportunities without assigning future outcomes. Runtime ecosystems may fail despite initialization checks; viability validation is not a promise of permanent balance.

## 38. World generation

Generate broad elevation, drainage, and simplified erosion to produce coherent landforms and watersheds. Distribute resources through geological, climatic, moisture, and biological relationships.

Initial species use compatible body plans and inherited modules with viability checks. Establish regional magical generation and material properties at creation; subsequent concentrations follow actual processes.

Generate initial terrain and populations once. Thereafter, reproduction, erosion, construction, migration, depletion, and other represented processes change the world. Do not spawn content because the observer visits.

Newly represented territory must fit boundary conditions and carry explicit initialization provenance. It cannot retroactively acquire a detailed simulated history that never ran. Before expansion is implemented, the modeled region needs a declared boundary model rather than silently assuming unlimited external resources or inhabitants.

## 39. Observer and godlike entity — final accepted replacement

The user's role combines objective observation with deliberate divine influence. This replaces the earlier ordinary-player direction and the earlier restriction of intervention to experimental mode.

**Observation.** Inspect represented objective state, retained beliefs, lineages, institutions, magic, ecology, and history. Looking does not alter reality or reveal the observer. Belief views remain available alongside objective views. Missing history remains missing.

**Divine intervention.** Directly alter environments, create or transform things, communicate, manifest avatars, and bestow blessings or curses. Interventions may exceed inhabitant capabilities and ordinary resource limits. They are explicit external operations, not ordinary techniques available by imitation.

**Blessings and curses.** Define actual effects, recipients, scope, duration, conditions, and continuing support where needed. Examples include healing, potential, resonance, protection, longevity, and access to capability. Labels alone do not implement an effect or grant unlimited unstated privileges.

**Persistence.** A divine gift may be a completed transformation, supported effect, or conditional operation. Removing support ends its dependent behavior. Changes and consequences already produced remain. An uncharged object created by divine action does not implicitly include infinite energy; any resource grant or continuing supply is explicit.

**Authority and accounting.** Divine actions may introduce matter or energy as declared external sources, including privileges exceeding ordinary generation restrictions. Their quantities, structural changes, and support dependencies enter objective state. An explicit external source is not an unexplained balancing adjustment.

**Autonomy.** Recipients retain minds and motives. Blessings do not automatically produce gratitude, loyalty, obedience, virtue, or worship. They may use gifts in unanticipated ways. The ordinary consequences of their decisions remain causal.

**Information and religion.** Inhabitants learn from manifestations, messages, observations, and traces they can actually access. They can misunderstand, doubt, conceal, or misattribute divine acts. Deliberate divine communication can convey information the observer knows; it is an external message, not proof that ordinary divination can access the observer archive. No message fabricates evidence that the stated event occurred if it did not.

**Avatars.** Manifestations may have explicitly defined abilities and limitations without turning the user into an ordinary player character. The engine must record what powers an avatar actually has rather than infer them from its title.

**Time and history.** Divine actions occur in the present global timeline. They cannot rewrite the past, undo elapsed experience, or create an in-world alternate timeline. The archive records them and their consequences; in-world records follow available evidence. Restoring a lost condition now is a new event, not erasure of the intervening history.

**Controls.** Pause, processing speed, and historical review remain observer controls. The world develops through its own processes between interventions. Any separately loaded checkpoint experiment remains a separate software run and is not an in-world branching event.

## 40. Names and identity

Project Genaris remains the internal R&D codename. Public product naming is deliberately deferred until the software develops a clearer identity; no architecture depends on resolving it now.

Cultures can develop different names for their world without agreeing on a universal one. Internal identifiers remain independent of names, permitting renaming, translation, disputed names, and lost names without changing identity or historical references.

## Numerical and implementation defaults

These selected values are starting configurations, not assertions that they have been performance-tested or mathematically calibrated.

| Setting | Initial default | Constraint on tuning |
| --- | --- | --- |
| Global timestamp resolution | 1 microsecond | One ordered global timeline; positive durations for repeatable processes. |
| Active interaction maximum update interval | 0.1 seconds | Refine sooner for accuracy, contact, thresholds, or instability. |
| Routine individual needs/decisions maximum interval | 1 minute | Relevant events can interrupt. |
| Environmental maximum interval | 10 minutes | Refine for local fast processes. |
| Growth/slow population maximum interval | 1 hour | Use actual elapsed time and preserve intermediate consequential transitions. |
| Initial environmental cell width | Approximately 100 metres | Adaptive refinement must preserve accounting and causal continuity. |
| Initial social population | Approximately 100 | Resource and relationship initialization must be coherent. |
| Initial communities | 3 | Future settlement outcomes are not prescribed. |
| Complete snapshot cadence | Daily, explicit saves, clean shutdown, before migration | Store model/configuration version and continuation state. |
| Detailed trace window | 30 simulated days | Promote important contributors while present; admit unrecoverable omissions afterward. |
| Snapshot retention | Daily for 30 days; monthly through 10 years; annual thereafter | Preserve designated investigations and retained event references. |

Generation rates, conductivities, leakage rates, material capacities, resonance coefficients, strain thresholds, creation costs, mutation probabilities, learning rates, forgetting rates, and social decision weights must be supplied as explicit versioned configurations before their corresponding systems run. Their numerical values require calibration; they do not reopen whether the underlying mechanisms exist.

## Implementation clarifications that prevent contradictions

The following are implementation interpretations of accepted rules, not claims that these details were separately approved earlier. They make the consolidated baseline usable without inventing new world powers.

1. **Accounting is broader than conservation.** Maintain separate ledgers for ordinary stores, magical stores, intrinsic generation, conversion, creation, and divine inputs. The totals may grow through authorized source terms. Every change still has a causal origin.
2. **No accidental magical-energy conversion loophole.** The general energy-conversion class cannot be used to bypass the ordinary rule that only the field generates fresh magical energy. Returning dispersed existing magical energy to storage is transfer; manufacturing new magical energy from ordinary output is not implicitly allowed.
3. **Temporal-rate effects and precision.** Track each affected process's local elapsed duration while using global event order. Sub-microsecond accumulated changes may be integrated numerically, but cannot create infinitely many separately ordered events at one timestamp. Unsupported extreme numerical conditions must produce an explicit computation limit, not a secret in-world power cap.
4. **No silent overflow or emergency equilibrium.** Use adequate numeric representation and detect invalid ranges. If an unbounded accumulation exceeds supported computation, pause/report the limitation or use a validated representation change. Do not erase excess or pretend the world stabilized.
5. **Joint conflict resolution is still an engineering obligation.** Specify a concrete rule for competing consumption, movement, and actions before implementing that interaction. A fair or stochastic rule must use relevant inputs and the accepted random policy; incidental execution order is not a rule.
6. **Stable IDs do not replace living continuity.** Engine identifiers preserve references; resurrection and identity claims depend on the represented surviving organization. A database row reused for a copy cannot make it the original individual.
7. **Aggregate ancestry is not fabricated individual ancestry.** Store exact lineage where represented and constrained group ancestry elsewhere. Individualization cannot pretend that unsimulated named parents and episodes are established history.
8. **Unobserved does not mean paused.** Background updates or justified catch-up calculations account for elapsed processes and cross-boundary consequences. Delayed calculation must not allow an impossible event to affect already committed history.
9. **Irreversible history permits present repair.** Repair, resurrection under surviving continuity, and divine restoration are new events. Their existence does not remove the original injury, death event, witnesses, or records.
10. **OP progression is permission, not a guarantee.** No immutable inherited ceiling or balancing intervention is imposed. Access still requires actual compatible development, information, resources, and successful control.
11. **Initial parameters and skill are not unexplained history.** Seed inhabitants can have configured abilities and inherited structures. Their provenance is initialization, not a false archive of centuries of simulated training.
12. **Foundations are not finished algorithms.** A multidimensional resonance profile, functional genome, or emergent language model needs concrete operators and mappings. This document defines their behavior and constraints; it does not claim those algorithms already exist.

## Explicitly superseded proposals

- A natural equilibrium concentration that stops field generation has been rejected.
- Automatic deletion or stabilization of excess energy has been rejected.
- Inherited resonance as an immutable personal ceiling has been replaced by trainable and transformable access.
- Fifty cosmetically different versions of the same capability are not separate objective techniques.
- Fully seed-deterministic history has been replaced by partial reproducibility.
- Exact historical replay is not required.
- Representing every organism and object individually has been replaced by persistent individuals plus collective models.
- Observer attention does not determine simulation fidelity or content generation.
- Scripted historical outcomes are replaced by causal emergence.
- Souls are neither universal consciousness requirements nor automatically immortal perfect backups.
- The ordinary player with no privileged actions has been replaced by the observer/godlike role.
- Divine intervention is not restricted to a separate experimental mode.
- The five-component magic formula and universal RPG attribute list remain nonmandatory descriptive ideas.

## Closure status and remaining work

All 40 register subjects have a settled direction or a selected design default in this document. The architecture-critical subset has rule-level decisions. This is sufficient to start architecture and staged implementation without another broad metaphysics questionnaire.

Deliberate deferrals are public product naming and any future requirement for exact replay. Numerical calibration and detailed implementation are still real work. They must not be mislabeled as already solved simply because the conceptual direction is fixed.

Engineering work that remains includes choosing exact field modes and compatible operators for the first slice; calibrated source/transfer/creation equations; phenotype-development mappings; safe aggregate/fine transformations; action conflict solvers; archive schemas; learning and communication algorithms; and performance measurements. Resolve these concretely within this baseline. Ask the user only if a proposed solution changes an established behavior or exposes a real incompatibility.

The first runnable slice may implement a subset of capabilities. Declare that subset explicitly. Unimplemented permissions remain world-design scope rather than simulated capabilities. Do not report a phenomenon as emergent when it was actually injected by initialization, a divine action, or unsupported narrative generation.

## Review checks for architecture and early implementation

These are behavioral acceptance examples, not claims that tests have already passed.

| Scenario | Required result |
| --- | --- |
| Energy generation exceeds use for a long interval | Concentration rises without a hidden equilibrium cutoff. |
| Charged material saturates | Its storage limit is respected; excess stays accounted for elsewhere or causes represented changes. |
| Ordinary creation produces an object containing charge | Material creation and transferred magical charge have separate accounted origins. |
| An exceptional individual improves resonance | New access follows actual development; no balancing penalty appears solely due to power. |
| A technique receives a new cultural name | Name/provenance changes without duplicating objective capability. |
| Spatial connection closes around crossing matter | Resolve positions and consequences; do not duplicate or delete matter. |
| Local time accelerates | All local processes experience the rate; global causality remains ordered. |
| A body changes permanently and its temporary enhancement ends | Completed structure remains; supported components relax; past damage remains. |
| A soul loses information encoded only in the destroyed body | No automatic perfect restoration of that information. |
| A copied mind runs independently | Separate individual identity with traceable shared origin. |
| A collective member becomes individually relevant | Consistent traits/counts/provenance, without invented detailed prehistory. |
| An observer switches views | No causally significant change caused solely by looking. |
| A coarse region receives a fast consequential interaction | Timely refinement and consistent boundary accounting. |
| A saved world resumes | Stored stream states and pending events continue without silent reseeding. |
| A culture loses its last active knowledge carrier | Observer archive survival does not restore cultural access. |
| A historical cause predates retained detailed evidence | Review admits the gap instead of fabricating an exact explanation. |
| A god bestows a blessing | Explicit effects and sources enter history; recipient loyalty is not automatically granted. |
| A divine blessing is revoked | Support ends as specified; completed consequences and records are not erased. |

## Pasteable instruction for the receiving project chat

Use this document as the consolidated Genaris world-law and simulation-doctrine baseline. It incorporates the original design direction, the 13 doctrine answers, all accepted topic packages, the remaining defaults selected under my authorization, and the final observer/godlike revision. Apply its supersession rules and preserve the distinction between laws, implementation models, and tunable configuration. Begin architecture and concrete implementation planning from it; do not restart the open-question register. Identify only genuine contradictions or choices that materially change an established decision. Keep the world causal, the inhabitants autonomous, and all divine interventions explicit in its history.
