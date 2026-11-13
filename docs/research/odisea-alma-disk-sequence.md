# ODISEA / ALMA protoplanetary disk sequence — source register

Status: publication verified; individual ALMA observation identifiers and FITS products not yet ingested.

## Primary source
- ALMA Observatory press release (2025-05-06): https://www.almaobservatory.org/en/press-releases/alma-inspires-new-models-for-the-evolution-of-planet-forming-disks/
- Orcajo et al. (2025), *The Ophiuchus DIsk Survey Employing ALMA (ODISEA): A Unified Evolutionary Sequence of Planet-Driven Substructures Explaining the Diversity of Disk Morphologies*, Astrophysical Journal Letters. Paper: https://arxiv.org/abs/2504.14318
- Sequence initially proposed by Cieza et al. (2021), reproduced with PlanetaLP and RADMC-3D modelling in Orcajo et al. (2025).

## Five proposed morphology stages
1. I: Shallow or absent observable substructures; protoplanets, if present, may not yet open detectable gaps.
2. II: Relatively narrow gaps and rings; interpreted as possible growing protoplanets.
3. III: Widened gaps and outer-edge dust trapping/pressure bumps, potentially associated with giant-planet gas accretion.
4. IV: Dust filtration and dust-depleted inner disk with outer dust concentrated near cavity edges.
5. V: Drained dusty inner disk and one or more narrow outer rings.

## Evidence policy
- ALMA measures disk emission and morphology; the five-stage ordering and planet-driven causal explanation are *model interpretations*, not direct detections of planets in every gap.
- The ALMA release says the comparison includes 15 disks, ten ODISEA and five DSHARP observations. Preserve that distinction when building a per-object table.
- Before catalogue ingestion, extract object-to-stage assignments from the cited figure/paper, then match each to ALMA archive project ID, observation UID, observing band, angular resolution, epoch, and DOI. Do not infer these identifiers from the figure alone.
- Record alternative gap-forming mechanisms and selection effects as open questions.

## Atlas integration
This register complements `stellar-seeds-open-questions.gmi`. The separate Computing & AI Evolution Matrix is a linked independent resource, not a scientific dependency.
