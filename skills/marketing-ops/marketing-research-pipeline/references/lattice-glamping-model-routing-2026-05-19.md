# Lattice Glamping — Model Routing Reference (2026-05-19)

## Full Pipeline Chain

| Phase | Agent | Model | Provider | API Mode | Duration | Verified |
|---|---|---|---|---|---|---|
| P1: Awareness | Researcher | claude-opus-4-7 | anthropic | anthropic_messages | 172s | ✅ live |
| P2: Competitor | Researcher | claude-opus-4-7 | anthropic | anthropic_messages | 191s | ✅ live |
| P3: Avatar | Researcher | claude-opus-4-7 | anthropic | anthropic_messages | 312s | ✅ live |
| QA gate (docs 1-3) | QualityTester | claude-opus-4-7 | anthropic | anthropic_messages | 107s | ✅ live |
| P4: Master Doc | Researcher | claude-opus-4-7 | anthropic | anthropic_messages | 188s | ✅ live |
| P5: Desire Extract | Researcher | claude-opus-4-7 | anthropic | anthropic_messages | 108s | ✅ live |
| P6: Desire Validation | Researcher | claude-opus-4-7 | anthropic | anthropic_messages | 166s | ✅ live |
| P7: Killer Hooks | Researcher | claude-opus-4-7 | anthropic | anthropic_messages | 56s | ✅ live |
| P8: Desire Copy (batches 1-5) | Researcher | claude-opus-4-7 | anthropic | anthropic_messages | 260-320s each | ✅ live |
| P9: Marketing Angles | Researcher | claude-opus-4-7 | anthropic | anthropic_messages | 150s | ✅ live |
| Brandformance W1 | MarketingStrategist | deepseek-v4-pro | deepseek | chat_completions | 404s | ✅ live |
| Brandformance W1b | MarketingStrategist | deepseek-v4-pro | deepseek | chat_completions | 578s | ✅ live |
| Brandformance W2 | CopyWriter | claude-sonnet-4-6 | anthropic | anthropic_messages | 415s + 324s | ✅ live |
| Brandformance W3 | QualityTester | claude-opus-4-7 | anthropic | anthropic_messages | 154s | ✅ live |

### Routing Mechanism
All delegations used `[AgentName]` prefix in goal text (e.g., `[MarketingStrategist]`, `[CopyWriter]`, `[QualityTester]`). The Phase 2 Router read `agent_profiles.yaml` → selected model based on `allowed_models` + `default_profile` (premium for strategist/copywriter, auto for QA).

### Key Lessons
1. `[AgentName]` prefix correctly routed to premium models for every call
2. CopyWriter (claude-sonnet-4-6) timed out at 600s when given 4 full strategy docs — recovery: split into 2-doc batches
3. David's explicit preference: no Opus for strategy or creative. Opus = QA only.
4. All execution_attribution metadata was verified via live API call confirmation
