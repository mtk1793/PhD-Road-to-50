# Topic 4: Explainable AI for Regulatory Compliance in Optimal Power Flow

## 🎯 Research Gap
While ML models achieve high accuracy, they are black boxes. Grid operators need explainable decisions for regulatory compliance and trust. Counterfactual explanations for OPF decisions are unexplored.

## 📋 Proposed Title
**"Counterfactual Explanations for Neural Network-Based Optimal Power Flow: A PyPower-Validated Approach for Regulatory Compliance"**

---

## 🔬 Methodology

### Technologies Stack
- **PyPower**: Ground truth OPF solver for validation
- **Neural Networks**: Fast OPF predictors (PyTorch)
- **Counterfactual Explanations**: DiCE (Diverse Counterfactual Explanations)
- **SHAP Values**: Local feature importance
- **Causal Inference**: DoWhy library for causal graphs
- **Visualization**: Interactive dashboards (Plotly Dash)

### Research Approach
1. Train deep neural network for fast OPF using PyPower training data
2. For each OPF solution, generate counterfactual explanations:
   - "What changes would lead to different generator dispatch?"
   - "Which load adjustments minimize cost?"
3. Validate counterfactuals using PyPower to ensure physical feasibility
4. Build causal graph showing relationships between inputs and outputs
5. Create regulatory report templates with visual explanations
6. Compare NN decisions with PyPower traditional solver explanations

---

## 💡 Novel Contributions
- First application of counterfactual reasoning to OPF
- Explainable AI framework for regulatory compliance
- Human-interpretable ML decisions for grid operators
- Bridge between fast ML predictions and trustworthy traditional solvers

---

## 📚 Key Literature & Sources

### Explainable AI in Power Systems (2023-2024)

#### **Critical Need for XAI in Energy Sector**
- **Reviews Published**: 2023-2024
- **Key Challenges**:
  - AI models perceived as "black boxes"
  - High accountability demands in energy sector
  - Need for transparent decision-making in critical infrastructure
- **Opportunities**:
  - Bridge gap between complex AI and human understanding
  - Build trust in AI-driven outcomes
  - Enable regulatory approval for AI in power systems
- **Sources**: [Technion](https://technion.ac.il), [Frontiers](https://frontiersin.org), [Uni Hannover](https://uni-hannover.de)

### Counterfactual Explanations for Optimal Power Flow

#### **Breakthrough Research (2023-2024)**

**"Counterfactual Explanations for DC Optimal Power Flow and Unit Commitment"**
- **Venues**: 
  - IEEE PowerTech 2025 (accepted)
  - arXiv preprints (2023-2024)
  - University of Strathclyde research
- **Key Questions Answered**:
  - "Why was this generator not dispatched?"
  - "What input changes would lead to different optimal solution?"
- **Methodology**:
  - Bilevel optimization problems to find counterfactual scenarios
  - Identify minimum changes in input parameters (nodal demands, temporal profiles)
  - Compare state-of-the-art methods with data-driven heuristics
  - Improve computational efficiency and explanation accuracy
- **Applications**: DC Optimal Power Flow (DCOPF), Unit Commitment (UC)
- **Sources**: [arXiv](https://arxiv.org), [Strathclyde](https://strath.ac.uk)

#### **Counterfactual Explanation Framework**
- **Value Proposition**: Provide actionable insights in high-stakes scenarios
- **Mechanism**: Illustrate how slight input changes alter model predictions
- **Contrast with SHAP**:
  - SHAP explains **how** a model arrived at its prediction
  - Counterfactuals explain **what** changes achieve desired outcome
- **Sources**: [Medium](https://medium.com), [Polimi](https://polimi.it)

### SHAP in Power Systems (2023-2024)

#### **SHAP Overview**
- **Foundation**: Cooperative game theory (Shapley values)
- **Capabilities**: 
  - Quantify contribution of each feature to model output
  - Provide local and global interpretability
  - Both feature importance and individual prediction explanations
- **Sources**: [MDPI](https://mdpi.com), [Medium](https://medium.com)

#### **Recent Applications in Power Systems**

**1. Reactive Power Optimization**
- **Framework**: SHAP for ML-based reactive power optimization
- **Contribution**: Measure input feature contributions in distribution networks
- **Source**: [arXiv](https://arxiv.org)

**2. Energy Consumption Forecasting**
- **Application**: Enhance transparency of energy usage predictions
- **Benefits**: 
  - Insights into factors influencing forecasts
  - Optimize energy planning
- **Sources**: [ResearchGate](https://researchgate.net), [MDPI](https://mdpi.com)

**3. National Demand Forecasting**
- **Year**: 2024
- **Contribution**: SHAP as feature selection tool
- **Results**: Maintain accuracy with smaller feature sets
- **Source**: [Energy Proceedings](https://energy-proceedings.org)

**4. Solar Energy Systems**
- **Integration**: SHAP + deep learning for solar generation
- **Applications**:
  - Anomaly detection
  - Generation prediction transparency
  - Stakeholder understanding of influencing factors
- **Source**: [ResearchGate](https://researchgate.net)

---

## 🛠️ Implementation Plan

### Phase 1: Neural Network OPF Surrogate (2 months)

#### **1.1 Data Generation**
- Use PyPower to generate OPF training data
- Scenarios:
  - Varying load profiles (residential, commercial, industrial)
  - Different renewable penetrations (0%, 20%, 40%)
  - Contingency scenarios (N-1, N-2)
- Inputs: Bus loads, generator capacities, line limits
- Outputs: Generator dispatch, bus voltages, line flows, total cost

#### **1.2 Neural Network Architecture**
- **Type**: Deep feedforward neural network (PyTorch)
- **Architecture**: 
  - Input layer: Grid parameters (loads, capacities, topology)
  - Hidden layers: 4-6 layers with 128-512 neurons
  - Output layer: OPF solution (dispatch, voltages, flows, cost)
- **Training**: 
  - Loss: MSE on OPF outputs
  - Optimizer: Adam
  - Validation: 20% hold-out set

#### **1.3 Performance Benchmarking**
- Compare NN predictions vs PyPower solutions
- Metrics: RMSE, MAE, accuracy within 1%/5% thresholds
- Speed comparison: NN inference vs PyPower solver

### Phase 2: SHAP Value Computation (1.5 months)

#### **2.1 SHAP Implementation**
- Install SHAP library: `pip install shap`
- Compute Shapley values for each input feature
- Generate:
  - Local explanations: Feature importance for individual predictions
  - Global explanations: Average feature importance across dataset

#### **2.2 Visualization**
- **Force plots**: Show how each feature pushes prediction from base value
- **Summary plots**: Overall feature importance ranking
- **Dependence plots**: Relationship between feature values and SHAP values
- **Waterfall plots**: Cumulative feature contributions

#### **2.3 Validation**
- Verify SHAP values make physical sense
- Cross-check with domain knowledge (e.g., load should affect dispatch)
- Compare with sensitivity analysis from PyPower

### Phase 3: Counterfactual Explanation Generation (3 months)

#### **3.1 DiCE (Diverse Counterfactual Explanations) Integration**
- Install DiCE: `pip install dice-ml`
- Define OPF as black-box model for DiCE
- Configure:
  - Actionable features (e.g., load adjustments, generator limits)
  - Immutable features (e.g., line impedances)
  - Desired outcome constraints (e.g., cost reduction, voltage within limits)

#### **3.2 Counterfactual Generation**
For each OPF decision, generate counterfactuals answering:
- **Generator Dispatch**: "What load changes would dispatch generator X?"
- **Cost Reduction**: "What's the minimal load adjustment to reduce cost by 10%?"
- **Voltage Violations**: "What changes prevent voltage violations?"

#### **3.3 Bilevel Optimization Approach**
- Formulate counterfactual search as bilevel optimization:
  - **Upper level**: Minimize distance between original and counterfactual inputs
  - **Lower level**: Ensure counterfactual leads to desired OPF output
- Solve using gradient-based methods or heuristics

#### **3.4 PyPower Validation**
- For each generated counterfactual:
  1. Input counterfactual scenario to PyPower
  2. Solve OPF with PyPower
  3. Verify counterfactual achieves claimed outcome
  4. Check physical feasibility (voltage limits, line flows, power balance)
- Discard infeasible counterfactuals

### Phase 4: Causal Graph Construction (2 months)

#### **4.1 DoWhy Library Integration**
- Install DoWhy: `pip install dowhy`
- Define causal model for OPF:
  - Nodes: Loads, generator capacities, dispatch decisions, cost
  - Edges: Causal relationships (e.g., load → dispatch → cost)

#### **4.2 Causal Discovery**
- Learn causal DAG from OPF simulation data
- Use algorithms:
  - PC (constraint-based)
  - GES (score-based)
  - LiNGAM (linear non-Gaussian acyclic models)

#### **4.3 Causal Inference**
- Compute causal effects using do-calculus:
  - `do(Load_increase) → Effect on Cost`
  - `do(Generator_limit_increase) → Effect on Dispatch`
- Validate causal claims using PyPower experiments

### Phase 5: Regulatory Compliance Framework (2 months)

#### **5.1 Regulatory Report Templates**
- **Executive Summary**: High-level explanation of OPF decision
- **Feature Importance**: SHAP values showing key drivers
- **Counterfactual Scenarios**: "What-if" analysis for operator queries
- **Causal Justification**: Why certain decisions were made (causal graph)
- **Validation**: PyPower confirmation of feasibility

#### **5.2 Interactive Dashboard (Plotly Dash)**
- **Components**:
  - Upload OPF scenario
  - View NN prediction vs PyPower solution
  - Explore SHAP explanations (force plot, summary plot)
  - Generate custom counterfactuals (user specifies desired outcome)
  - Visualize causal graph
  - Export regulatory report (PDF)

#### **5.3 Compliance Criteria**
- **Transparency**: All decisions traceable to input features
- **Auditability**: PyPower validation ensures correctness
- **Actionability**: Counterfactuals provide operator guidance
- **Interpretability**: Visualizations accessible to non-experts

### Phase 6: Publication (2-3 months)
- Write IEEE Transactions paper
- Open-source code repository (NN OPF + SHAP + DiCE + DoWhy)
- Create tutorial for power system operators
- Demonstrate compliance dashboard

---

## 📊 Benchmark Datasets

### IEEE Test Systems
- **IEEE 14-bus**: Simple case for prototyping explanations
- **IEEE 30-bus**: Medium complexity
- **IEEE 57-bus**: Realistic system with diverse generators
- **IEEE 118-bus**: Large-scale for scalability testing

### OPF Scenarios
- **Normal Operations**: Baseline dispatch
- **Peak Load**: Stress testing generator limits
- **Contingency**: N-1, N-2 line/generator outages
- **High Renewables**: 40%+ wind/solar penetration
- **Cost Optimization**: Minimize generation cost vs emissions

---

## 🎯 Expected Outcomes

### Technical Contributions
1. First counterfactual explanation framework for OPF
2. SHAP-based feature importance analysis for power systems
3. Causal graph elucidating OPF input-output relationships
4. Regulatory compliance toolkit for ML-based OPF

### Performance Targets
- **NN Accuracy**: >98% match with PyPower solutions
- **Counterfactual Feasibility**: >90% validated by PyPower
- **Explanation Latency**: <1 second for SHAP/counterfactuals
- **Dashboard Responsiveness**: Real-time interaction

### Practical Impact
- Increased operator trust in ML-based OPF tools
- Regulatory approval for AI in critical grid operations
- Auditable decision-making for compliance
- Educational tool for training new operators
- Faster troubleshooting of unexpected OPF outcomes

### Publications
- 1-2 IEEE Transactions papers (Power Systems, AI)
- Conference paper at IEEE PowerTech
- Tutorial paper for practitioners
- Open-source toolkit release

---

## 🔗 Key References to Acquire

### Must-Read Papers
1. "Counterfactual Explanations for DC Optimal Power Flow and Unit Commitment" (IEEE PowerTech 2025, arXiv)
2. University of Strathcloh counterfactual OPF research
3. XAI in Energy Systems reviews (2023-2024)
4. SHAP applications in power systems (reactive power, forecasting, solar)
5. DoWhy library documentation and causal inference tutorials

### Technical Documentation
- SHAP library: [GitHub](https://github.com/slundberg/shap)
- DiCE: [GitHub](https://github.com/interpretml/DiCE)
- DoWhy: [GitHub](https://github.com/py-why/dowhy)
- Plotly Dash documentation
- PyPower API for OPF solving

---

## ❓ Why This Hasn't Been Done

1. **Emerging Field**: Explainable AI for power systems is nascent (2023-2024 surge)
2. **Domain-Specific Constraints**: Counterfactuals require physics constraints (power balance, voltage limits)
3. **Regulatory Focus**: Transparency demands are recent (AI Act, utility regulations)
4. **Interdisciplinary**: Requires expertise in ML, power systems, and causal inference

---

## 🚀 Getting Started

### Immediate Next Steps
1. Read IEEE PowerTech 2025 counterfactual OPF paper
2. Install SHAP and explore SHAP tutorials
3. Train simple NN for OPF on IEEE 14-bus
4. Generate first SHAP explanations and force plots
5. Prototype counterfactual with DiCE library

### Required Skills
- **Machine Learning**: Neural networks, SHAP, counterfactuals
- **Power Systems**: OPF, PyPower, grid constraints
- **Causal Inference**: DoWhy, DAGs, do-calculus
- **Software**: Python, PyTorch, Plotly Dash

### Timeline
- **Total Duration**: 12-18 months to first publication
- **Literature Review**: 1-2 months ✓ (this document starts it)
- **Implementation**: 8-10 months
- **Writing & Submission**: 2-3 months

---

## 📧 Community & Resources

### Libraries & Tools
- [SHAP](https://github.com/slundberg/shap)
- [DiCE](https://github.com/interpretml/DiCE)
- [DoWhy](https://github.com/py-why/dowhy)
- [Plotly Dash](https://dash.plotly.com)
- [PyPower](https://pypi.org/project/pypower/)

### Research Communities
- IEEE PES Machine Learning Subcommittee
- Explainable AI community (InterpretML)
- Causal inference researchers (Microsoft Research)

### Conferences
- IEEE PowerTech
- IEEE PES General Meeting
- NeurIPS (XAI workshops)
- FAccT (Fairness, Accountability, Transparency)

---

## ✅ Feasibility Assessment

### ✓ High Feasibility Factors
- Open-source XAI tools (SHAP, DiCE, DoWhy)
- PyPower readily available
- Clear regulatory and operational need
- Recent precedent in IEEE literature (2023-2024)

### ⚠️ Challenges to Address
- Ensuring counterfactual physical feasibility (needs PyPower validation)
- Computational cost of generating diverse counterfactuals
- User interface design for operators (usability testing)
- Gaining regulatory acceptance (engage with utilities)

---

*Last Updated: December 2024*
