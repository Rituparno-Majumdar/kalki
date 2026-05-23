# Governance

## How Kalki is Governed

Kalki is a community-owned, mission-driven project. This document defines how decisions are made, who makes them, and how contributors can grow into leadership roles.

Our governance is designed around one core belief: **the people closest to the work should make the decisions about the work.**

---

## Philosophy

**Kalki exists to serve India's public interest.** Every governance decision flows from this mission.

- **The founder provides vision; the community provides implementation.** The founder is the architect of Kalki's mission and principles. The community designs, builds, tests, and ships the platform. Neither can succeed without the other.

- **Decisions at the lowest level possible.** A module maintainer should never need to escalate to the Core Team what they can resolve themselves. The Core Team should never need to escalate to the founder what they can resolve themselves. Authority flows downward; escalation flows upward only when necessary.

- **Governance must scale.** What works at 5 contributors must work at 50 and at 500. We design for the project's future, not just its present. Roles, processes, and norms are documented explicitly so the project can grow without bottlenecks.

- **Transparency is non-negotiable.** All governance decisions, meeting notes, and policy changes are documented publicly. No decisions are made in private channels that affect the public project.

- **Earned authority.** Leadership roles are earned through sustained, high-quality contribution and demonstrated community trust — never through affiliation, seniority, or social capital alone.

---

## Roles

### Project Founder

The founder is the constitutional guardian of Kalki's mission and ethical principles.

**Responsibilities:**
- Define and protect the project's mission, vision, and core ethical principles
- Appoint the initial Core Team and Ethics Board
- Final authority on mission-level decisions (e.g., "Should Kalki operate in this domain at all?")
- Veto power on features or directions that violate core principles

**Boundaries:**
- The founder does **not** review day-to-day code, PRs, or technical decisions
- The founder does **not** manage contributors, assign tasks, or run sprints
- The founder does **not** need to be involved in module-level decisions

**Mental model:** Think of the founder as a constitutional court — they interpret the mission and intervene only when the project risks violating its own principles. Day-to-day governance is the community's responsibility.

---

### Core Team

*3–7 members. The project's operational leadership.*

The Core Team is the backbone of Kalki's day-to-day governance. They coordinate across modules, manage releases, and ensure the community is healthy and productive.

**Responsibilities:**
- Cross-module coordination and architectural decisions
- Release management and version planning
- Community health: onboarding, mentorship, conflict resolution
- Nominating and onboarding Module Maintainers
- Representing the project in external partnerships and communications

**Authority:**
- Merge access across all modules
- Can create and archive modules
- Can approve or reject cross-module proposals

**How to become a Core Team member:**
- Nominated by an existing Core Team member
- Approved by the founder
- Based on: sustained high-quality contributions, cross-module understanding, demonstrated community leadership, and alignment with Kalki's mission

**Expectations:**
- Regular availability (responsive within 48 hours on governance matters)
- Attend monthly community calls
- Actively mentor contributors and maintainers
- Disclose any potential conflicts of interest

---

### Module Maintainers

*1–2 per module. The owners of their domain.*

Module Maintainers are the first point of authority within their module. They make technical decisions, review PRs, and set the module's roadmap — independently.

**Responsibilities:**
- Own the module's technical roadmap and priorities
- Review and merge PRs within their module
- Mentor contributors working in their module
- Report progress and blockers in monthly community calls
- Maintain module documentation

**Authority:**
- Merge access within their module
- Can make technical decisions within their module without Core Team approval
- Can request Ethics Board review for new data sources or sensitive features

**How to become a Module Maintainer:**
- Nominated by the Core Team
- Based on: domain expertise, contribution history in the module, and ability to mentor others
- No minimum contribution count — quality and understanding matter more than volume

**Expectations:**
- Respond to PRs and issues in their module within 5 business days
- Participate in monthly community calls
- Proactively identify and flag risks or blockers

---

### Ethics Board

*7 members. Independent advisory and oversight body.*

The Ethics Board is Kalki's conscience. It exists to ensure the project's work serves the public interest and does not cause harm. The Ethics Board operates independently of the contributor hierarchy.

**Responsibilities:**
- Review new data sources for ethical appropriateness and accessibility
- Review new signal types and model outputs for bias, fairness, and potential for misuse
- Publish ethics review reports for significant decisions
- Advise on data privacy, consent, and surveillance concerns
- Develop and maintain the project's ethical guidelines (see [ETHICS.md](ETHICS.md))

**Authority:**
- **Veto power** on features, data sources, or models that violate ethical principles
- Ethics Board vetoes can only be overridden by a unanimous Core Team vote plus founder approval
- Can initiate ethics reviews independently (not only when asked)

**Composition:**
- 7 members with diverse backgrounds: technology ethics, civil liberties, data science, Indian law, social sciences, journalism, and community advocacy
- At least 3 members must be from outside the active contributor community (external independence)
- 2-year rotating terms, staggered so no more than 3 members rotate in the same year

**How members are selected:**
- Initial board appointed by the founder
- Subsequent members nominated by the existing Ethics Board and approved by the founder
- Self-nomination welcome through a public application process

**Independence guarantees:**
- Ethics Board members are not required to be code contributors
- No single organization may hold more than 1 seat
- Board deliberations are published (redacted only for privacy-sensitive cases)
- The Ethics Board is not controlled by the founder, Core Team, or any external entity

---

### Reviewers

*Trusted contributors who can approve PRs.*

**How to become a Reviewer:**
- Nominated by a Module Maintainer for consistent, thoughtful contributions and review comments
- Demonstrated understanding of the module's code quality standards
- Approved by the relevant Module Maintainer

**Authority:**
- Can approve PRs in their module (merge still requires maintainer approval)
- Can label and triage issues in their module

---

### Contributors

*Everyone who contributes to Kalki.*

**Who qualifies:**
- Anyone who submits a merged PR
- Anyone who makes a significant non-code contribution (documentation, translation, research, ethics review, community organizing)

**No formal obligations** beyond following the [Code of Conduct](CODE_OF_CONDUCT.md).

**Growth path:**
Every Core Team member and Module Maintainer started as a contributor. The path is open and transparent:

```
Contributor → Regular Contributor → Reviewer → Module Maintainer → Core Team
```

---

## Decision Making

Decisions are made at the lowest appropriate level. The table below defines who decides what:

| Decision Type | Who Decides | Process |
|---|---|---|
| Bug fixes and minor improvements | Any Reviewer | Approve and merge |
| New features within a module | Module Maintainer | Lazy consensus: propose, wait 72 hours, merge if no objections |
| New data source integration | Module Maintainer + Ethics Board | Maintainer proposes; Ethics Board reviews for accessibility and ethics |
| Cross-module changes | Core Team | Discussion in GitHub Discussions; majority agreement required |
| New module creation | Core Team + Founder | Proposal → community discussion → Core Team vote → Founder approval |
| Ethics policy changes | Ethics Board + Founder | Ethics Board proposes; Founder approves |
| Mission-level changes | Founder | Founder decides after consulting Core Team and Ethics Board |

### Lazy Consensus

Many decisions use **lazy consensus**: a proposal is posted publicly, and if no objections are raised within 72 hours, the proposal is considered approved. This keeps the project moving without requiring active agreement from every stakeholder.

- Proposals must be posted in GitHub Discussions with the `proposal` label
- The 72-hour clock starts when the proposal is posted
- Any contributor can raise an objection — objections must be substantive and include a reason
- If an objection is raised, the decision escalates to the next level

### Voting

When voting is required (Core Team decisions, governance changes):
- Each eligible voter gets one vote
- Majority wins (>50%)
- Votes are recorded publicly
- Abstentions do not count toward the total

---

## Conflict Resolution

Disagreements are normal and healthy. Here's how we resolve them:

### Technical Disagreements

```
Try to resolve between contributors
    ↓ (if unresolved)
Module Maintainer mediates and decides
    ↓ (if cross-module or unresolved)
Core Team discusses and uses lazy consensus
    ↓ (if still unresolved)
Core Team votes (majority wins)
```

### Ethics Disagreements

- Any contributor can raise an ethics concern via GitHub Discussions or directly to the Ethics Board
- The Ethics Board reviews the concern and publishes a ruling
- **Ethics Board rulings are final** on ethical matters
- The only override path: unanimous Core Team vote + Founder approval (reserved for extraordinary circumstances)

### Interpersonal Conflicts

- First, try to resolve directly between the involved parties
- If unresolved, report to a Core Team member
- Core Team enforces the Code of Conduct
- Serious violations may result in temporary or permanent bans
- All enforcement actions are documented (names redacted for privacy)

### Mission Disagreements

- If a contributor believes the project is drifting from its mission, they can raise a concern in GitHub Discussions
- The Core Team discusses and advises
- **The founder's decision is final** on mission-level questions
- The founder must publish a written rationale for mission-level decisions

---

## Government Integration Path

Kalki is built to serve Indian public interest. Government participation is welcome — within clear boundaries.

### How Government Agencies Can Participate

| Role | Description |
|---|---|
| **Data Partners** | Provide access to public datasets via official APIs or data sharing agreements |
| **Domain Advisors** | Lend subject matter expertise to module design and data interpretation |
| **Users** | Use Kalki's outputs, dashboards, and analyses for policy planning and decision support |

### What Government Agencies May NOT Do

- **Control the project's direction or roadmap.** Kalki's priorities are set by the community, not by any government agency.
- **Require features that violate ethical principles.** All feature requests from government partners go through the same Ethics Board review as any other proposal.
- **Access non-public project data or internal audit logs.** Kalki's outputs are public; its internal processes are governed by the community.
- **Use their participation to legitimize surveillance.** Any partnership that enables or facilitates mass surveillance is prohibited under Kalki's ethical principles.

### Partnership Approval Process

1. Government agency submits a partnership proposal (public or private, at their discretion)
2. Ethics Board reviews the proposal for alignment with Kalki's principles
3. Core Team evaluates the technical and operational implications
4. Both Ethics Board and Core Team must approve
5. Partnership terms are documented publicly in [PARTNERSHIPS.md](PARTNERSHIPS.md)

> **Principle:** Government agencies are partners, not patrons. Their participation enriches Kalki's data and impact without compromising its independence.

---

## Institutional Partnerships

Kalki welcomes partnerships with institutions that share its mission.

### Academic Institutions

- **IITs, IIITs, NITs, and universities** are welcome as research partners
- Student projects, thesis work, and research collaborations are encouraged
- Academic partners may propose research-oriented modules or analyses
- Credited in publications and project documentation

### Civil Society Organizations

- **NGOs, think tanks, and advocacy groups** are welcome as domain advisors
- Can propose data sources, signal types, and use cases
- Help ensure Kalki's work reflects ground-level realities
- Credited for domain contributions

### Corporate Sponsors

- Welcome to sponsor **infrastructure costs** (hosting, CI/CD, cloud resources)
- **No influence** on project direction, roadmap, or technical decisions
- Sponsors are acknowledged in a dedicated section of the README
- Sponsorship agreements are documented publicly

### Partnership Principles

- All partnerships are documented publicly in [PARTNERSHIPS.md](PARTNERSHIPS.md)
- No partner may hold undue influence over project decisions
- The Ethics Board reviews all partnership proposals
- Partnerships can be terminated by Core Team vote if they conflict with project principles

---

## Evolution of Governance

This governance model is not permanent. It is designed to evolve as Kalki grows.

### How Governance Changes

1. **Anyone** can propose a governance change by opening an RFC in GitHub Discussions
2. The RFC is open for a **30-day public comment period**
3. The Core Team reviews all feedback and drafts a final proposal
4. The Core Team votes on the final proposal
5. The Founder approves or vetoes the change
6. Approved changes are merged into this document with a changelog entry

### Future Considerations

As Kalki scales, the community should consider:

- **Forming a registered non-profit foundation** (e.g., a Section 8 company under Indian law) to hold project assets, manage funding, and provide legal identity
- **Establishing regional chapters** to coordinate contributors and partnerships across Indian states
- **Creating a Technical Steering Committee** to manage cross-module architecture decisions as the system grows in complexity
- **Implementing elections** for Core Team seats to increase democratic accountability

### Governance Changelog

| Date | Change | Approved By |
|---|---|---|
| 2025 | Initial governance document | Founder |

---

> *Kalki's governance exists to serve one purpose: ensuring that this project remains a trustworthy, transparent, community-owned tool for India's public interest. Every role, process, and rule in this document is in service of that goal.*
