# Topic 2: Causal Reinforcement Learning for Proactive Fault Prevention in Smart Grids
## Implementation Roadmap

---

## 🎯 Research Objective
Develop a causal reinforcement learning framework that learns causal mechanisms behind grid faults, enabling proactive interventions through counterfactual reasoning.

---

## 📅 Timeline Overview (20 Months)

### Phase 1: Causal Discovery (Months 1-5)
### Phase 2: Counterfactual RL (Months 6-12)
### Phase 3: Deployment & Publication (Months 13-20)

---

## Phase 1: Causal Discovery Foundation

 (Months 1-5)

### Month 1: Causality Fundamentals

**Week 1-2: Pearl's Causal Hierarchy**
- [ ] Read "The Book of Why" (Judea Pearl)
- [ ] Study do-calculus and interventional distributions
- [ ] Learn DAG terminology (colliders, confounders, mediators)
- [ ] Practice with simple examples (smoking → cancer)

**Week 3-4: Causal Discovery Algorithms**
- [ ] **Constraint-Based**: PC, FCI algorithms
- [ ] **Score-Based**: GES, NOTEARS
- [ ] **Hybrid**: CGNN, DAG-GNN
- [ ] Implement PC-Stable in Python:
  ```python
  from causal_learn.search.ConstraintBased.PC import pc
  cg = pc(data, alpha=0.05, indep_test='fisherz')
  ```

**Deliverable**: Causal discovery tutorial notebook

---

### Month 2: Grid-Specific Causal Modeling

**Week 1: Domain Knowledge Integration**
- [ ] Consult with power systems expert
- [ ] Document known causal relationships:
  - Temperature → AC Load → Power Consumption
  - Solar Irradiance → Solar Power
  - Power Imbalance → Voltage Fluctuation
- [ ] Create expert-validated prior DAG

**Week 2: Temporal Causality**
- [ ] Implement Granger causality tests
- [ ] Identify lag structures (e.g., faults lag voltage drop by 5-15 min)
- [ ] Build temporal graphical model

**Week 3: Confounder Detection**
- [ ] Use backdoor criterion to identify confounders
- [ ] Example: "Humidity affects both solar and load"
- [ ] Implement backdoor adjustment:
  ```python
  # Adjust for confounder C
  P(Y | do(X)) = Σ_c P(Y | X, C) P(C)
  ```

**Week 4: Validation with Simulations**
- [ ] Use PowerWorld/MATPOWER for ground truth
- [ ] Inject known causal interventions
- [ ] Verify learned DAG matches physical reality

**Deliverable**: Smart grid structural causal model (SCM)

---

### Month 3-4: Causal Discovery Experiments

**Month 3: Algorithm Comparison**
- [ ] Run 5 causal discovery methods on grid data:
  1. PC-Stable
  2. GES
  3. NOTEARS
  4. CGNN (Causal Generative NN)
  5. Expert prior + constraint-based
- [ ] Metrics:
  - **SHD** (Structural Hamming Distance to ground truth)
  - **Precision/Recall** of edge recovery
  - **Runtime**

**Month 4: Robustness Testing**
- [ ] Test with missing data (10%, 20%, 30%)
- [ ] Test with measurement noise (Gaussian, non-Gaussian)
- [ ] Test with different sample sizes (1K, 10K, 50K)
- [ ] Ablation: Remove domain constraints

**Deliverable**: Causal discovery benchmark paper (workshop submission)

---

### Month 5: Structural Causal Model (SCM) Learning

**Week 1-2: Functional Form Estimation**
- [ ] Linear SCM (simple baseline)
- [ ] Nonlinear SCM with neural networks:
  ```python
  # Example: Voltage = f(Load, Solar, Wind, noise)
  voltage = NN([load, solar, wind]) + ε_voltage
  ```
- [ ] Train using Maximum Likelihood

**Week 3: Identifiability Analysis**
- [ ] Check if causal effects are identifiable
- [ ] Use do-calculus to derive adjustment formulas
- [ ] Handle unobserved confounders (if any)

**Week 4: Counterfactual Engine**
- [ ] Implement 3-step counterfactual inference:
  1. **Abduction**: Infer noise terms from data
  2. **Action**: Apply intervention
  3. **Prediction**: Forward pass through SCM
- [ ] Example:
  ```python
  # Observed: Fault = 1 at Load = 10kW
  # Counterfactual: What if Load = 8kW?
  noise = infer_noise(fault=1, load=10)
  counterfactual_fault = scm.predict(load=8, noise=noise)
  ```

**Deliverable**: Working SCM with counterfactual queries

---

## Phase 2: Causal Reinforcement Learning (Months 6-12)

### Month 6: Counterfactual Data Augmentation

**Week 1: CDA Framework**
- [ ] For each observed (s, a, r, s') transition:
  - Generate 5 counterfactual actions
  - Use SCM to predict outcomes
  - Add to RL replay buffer
- [ ] Balance observational vs. counterfactual data (70/30 split)

**Week 2: Quality Control**
- [ ] Validate counterfactuals against simulations
- [ ] Filter implausible scenarios (e.g., negative voltage)
- [ ] Measure distribution shift

**Week 3: Augmentation Strategies**
- [ ] **Nearest Counterfactual**: Minimal state change
- [ ] **Diverse Counterfactuals**: Sample from intervention distribution
- [ ] **High-Value Counterfactuals**: Focus on fault prevention scenarios

**Week 4: Impact Analysis**
- [ ] Train RL agent on:
  - Observational only
  - Observational + Random augmentation
  - Observational + Causal augmentation (ours)
- [ ] Measure generalization to unseen fault types

**Deliverable**: CDA module integrated with RL

---

### Month 7-8: Causal Q-Learning

**Month 7: Twin Q-Networks**
- [ ] Design architecture:
  ```python
  class CausalDQN:
      def __init__(self):
          self.Q_obs = DQN()   # Standard observational Q
          self.Q_int = DQN()   # Interventional Q (CDA-trained)
          self.alpha = 1.0     # Annealing parameter
      
      def get_action(self, state):
          Q_combined = self.alpha * self.Q_obs(state) + \
                       (1 - self.alpha) * self.Q_int(state)
          return Q_combined.argmax()
  ```
- [ ] Implement α annealing schedule
- [ ] Train both networks simultaneously

**Month 8: Do-Operator Integration**
- [ ] Explicitly model interventional distribution
- [ ] Use SCM to simulate do(action) effects
- [ ] Update Q_int based on interventional rewards
- [ ] Ablation: Q_int only vs. Q_obs only vs. hybrid

**Deliverable**: Causal Q-learning algorithm

---

### Month 9: Invariant Risk Minimization (IRM)

**Week 1-2: Environment Diversity**
- [ ] Create 5 distinct grid configurations:
  - Env 1: Baseline topology
  - Env 2: +20% solar capacity
  - Env 3: One transformer offline
  - Env 4: High-resistance lines (aging)
  - Env 5: Different load profile (industrial vs. residential)

**Week 3: IRM Loss Implementation**
- [ ] Implement IRM penalty:
  ```python
  def irm_loss(features, actions, rewards, envs):
      total_loss = 0
      penalties = 0
      for e in envs:
          loss_e = compute_loss(features[e], actions[e], rewards[e])
          grad_e = torch.autograd.grad(loss_e, model.parameters())
          penalties += (grad_e ** 2).sum()
      return total_loss + λ * penalties
  ```
- [ ] Tune λ hyperparameter

**Week 4: Generalization Testing**
- [ ] Train on Envs 1-3
- [ ] Test on Envs 4-5 (unseen topologies)
- [ ] Compare to standard RL (expect 30%+ improvement)

**Deliverable**: IRM-enhanced causal RL

---

### Month 10: Offline RL + Causal Discovery

**Week 1-2: Conservative Q-Learning (CQL)**
- [ ] Implement CQL to avoid out-of-distribution actions
- [ ] Combine with causal model: only extrapolate along causal edges
- [ ] Example: "Can predict effect of reducing solar, but not reversing solar"

**Week 3: Causal Uncertainty**
- [ ] Epistemic uncertainty in SCM parameters
- [ ] Propagate uncertainty through counterfactuals
- [ ] Risk-averse policy: Avoid high-uncertainty interventions

**Week 4: Integration**
- [ ] Full pipeline: Causal Discovery → SCM → CDA → IRM → Offline RL
- [ ] End-to-end training
- [ ] Measure fault prevention rate

**Deliverable**: Complete causal RL system

---

### Month 11-12: Advanced Techniques

**Month 11: Causal Imitation Learning**
- [ ] Collect expert demonstrations (from operators or heuristics)
- [ ] Use causal model to understand expert reasoning
- [ ] Imitate causal mechanisms, not just behaviors
- [ ] Example: Expert sheds load when (Voltage < threshold AND Solar_forecast = decreasing)

**Month 12: Multi-Step Causal Reasoning**
- [ ] Learn transition SCM: s_{t+1} = f(s_t, a_t, noise)
- [ ] Plan 5-10 steps ahead using causal model
- [ ] Compare to model-free RL (should be more sample-efficient)
- [ ] Implement Monte Carlo Tree Search with causal rollouts

**Deliverable**: Advanced causal RL methods

---

## Phase 3: Validation & Publication (Months 13-20)

### Month 13-14: Comprehensive Experiments

**Experimental Design**:
- [ ] **Baselines**:
  1. Reactive control (act after fault)
  2. Heuristic rules (voltage thresholds)
  3. Standard DQN
  4. Model-based RL (no causality)
  5. **Causal RL (ours)**

- [ ] **Evaluation Scenarios**:
  - Seen fault types (training distribution)
  - Unseen fault types (e.g., simultaneous solar drop + demand spike)
  - Topology changes (rewire grid)
  - Long-horizon prevention (10+ minute lead time)

- [ ] **Metrics**:
  - **Fault Prevention Rate**: % of faults avoided
  - **False Alarm Rate**: Unnecessary interventions
  - **Intervention Cost**: Economic impact
  - **Generalization Gap**: Performance drop on unseen scenarios

**Deliverable**: Complete experimental results

---

### Month 15: Explainability & Visualization

**Week 1: Causal Attribution**
- [ ] Visualize learned DAG
- [ ] Highlight critical edges for fault prevention
- [ ] Example: "Reducing load by 2kW decreases fault probability 67% because it lowers transformer stress"

**Week 2: Intervention Effect Plots**
- [ ] Plot P(Fault | do(Load = x)) vs. x
- [ ] Compare to observational P(Fault | Load = x)
- [ ] Show where causal and observational diverge

**Week 3: Operator Dashboard**
- [ ] Real-time causal graph updates
- [ ] Counterfactual "what-if" simulator
- [ ] Recommended actions with explanations

**Week 4: Human Study**
- [ ] Recruit 10 grid operators
- [ ] Compare:
  - Decisions with causal explanations
  - Decisions with correlation-only
- [ ] Measure trust, decision time, accuracy

**Deliverable**: Explainability module + user study results

---

### Month 16-17: Paper Writing

**Month 16: Conference Paper (NeurIPS/ICML)**
- [ ] Title: "Causal Reinforcement Learning for Proactive Fault Prevention in Smart Grids"
- [ ] Structure:
  1. Introduction (causality vs. correlation)
  2. Background (RL + causal inference)
  3. Method (SCM learning, CDA, Causal Q-learning, IRM)
  4. Experiments (fault prevention benchmarks)
  5. Explainability (human study)
  6. Discussion + Future Work

**Month 17: Journal Extension (IEEE Trans Power Systems)**
- [ ] Add:
  - Theoretical analysis (when does causal RL outperform?)
  - Extended baselines (more RL algorithms)
  - Real-world validation (IEEE 118-bus system)
  - Safety analysis (worst-case scenarios)
  - Code release + reproducibility

**Deliverable**: 2 papers submitted

---

### Month 18: Real-World Validation

**Option A: Simulation-Based**
- [ ] Implement in PowerWorld or PSCAD
- [ ] Test on IEEE standard test systems
- [ ] Compare to commercial energy management systems (EMS)

**Option B: Industry Partnership**
- [ ] Partner with utility company or NREL
- [ ] Deploy in testbed microgrid
- [ ] Collect real operational data
- [ ] Iterate based on operator feedback

**Option C: Hardware-in-the-Loop**
- [ ] Use OPAL-RT real-time simulator
- [ ] Closed-loop validation
- [ ] Test under worst-case scenarios

**Deliverable**: Validation report + potential pilot deployment

---

### Month 19: High-Impact Publication

**Target**: Nature Energy / Science Robotics

**Unique Angle**: "Causal AI Prevents Blackouts Before They Happen"

**Content**:
- [ ] Simplified intro for broad audience
- [ ] Emphasis on real-world impact (prevented blackouts, $M saved)
- [ ] Comparison to Texas 2021 blackout (counterfactual analysis)
- [ ] Policy implications (grid modernization)
- [ ] Beautiful visualizations

**Deliverable**: High-impact paper drafted

---

### Month 20: Thesis Integration

**Chapter 4: Causal Reinforcement Learning for Grid Resilience**
- [ ] 50-70 pages
- [ ] Integrated publications
- [ ] Connections to other thesis topics:
  - Use continual learning (Topic 1) to adapt causal model
  - Combine with distributional RL (Topic 4) for risk-aware causal policies
  - Explain causal decisions with neurosymbolic AI (Topic 5)

---

## 📊 Key Performance Indicators

### Technical Metrics
- ✅ **Fault Prevention**: 60-80% of faults preventable
- ✅ **False Alarm Reduction**: 50% fewer than threshold-based
- ✅ **Generalization**: 90%+ performance on unseen topologies
- ✅ **Lead Time**: 10-15 minute early warning

### Publication Metrics
- ✅ **Conference**: 1 NeurIPS/ICML/UAI paper
- ✅ **Journal**: 1 IEEE Trans + 1 high-impact (Nature/Science)
- ✅ **Workshop**: 1-2 causal learning workshops
- ✅ **Citations**: 50+ in 2 years (hot topic)

---

## 🛠️ Tools & Infrastructure

```yaml
Causal Inference:
  - causal-learn (Python)
  - DoWhy (Microsoft)
  - gCastle (Huawei)
  - ananke (counterfactual reasoning)

Reinforcement Learning:
  - Stable-Baselines3
  - RLlib (Ray)
  - d3rlpy (offline RL)

Power System Simulation:
  - MATPOWER (MATLAB)
  - pandapower (Python)
  - GridLAB-D

Visualization:
  - NetworkX (DAG plotting)
  - Graphviz
  - Dash (interactive)
```

---

## 📚 Key Papers to Implement

1. Pearl (2009) - Causality: Models, Reasoning, Inference
2. Zheng et al. (2018) - NOTEARS
3. Arjovsky et al. (2019) - Invariant Risk Minimization
4. Buesing et al. (2019) - Woulda, Coulda, Shoulda (Counterfactual RL)
5. Lu et al. (2021) - Discover and Cure (Causal RL)

---

## ✅ Success Criteria

**Minimum**:
- ✅ Functional causal discovery on grid data
- ✅ Causal Q-learning outperforms standard DQN
- ✅ 1 workshop paper

**Target**:
- ✅ 60%+ fault prevention rate
- ✅ 1 top conference + 1 journal paper
- ✅ Open-source causal RL library

**Stretch**:
- ✅ Nature/Science paper
- ✅ Industry pilot deployment
- ✅ 100+ citations in 2 years

---

**Next Steps**: See Month 1 checklist above  
**Last Updated**: January 2026
