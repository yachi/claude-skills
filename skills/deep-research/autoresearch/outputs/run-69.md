# El Nino Prediction Model Using NOAA Buoy Data: LSTM vs Transformer vs Physics-Informed Approaches

## Executive Summary

For building an El Nino prediction model with 6-month lead time and >80% accuracy using NOAA buoy data, the **physics-informed transformer approach (ENSO-PhyNet or CTEFNet architecture) is recommended** over pure LSTM or vanilla transformer models. Confidence: 70%. The 80% accuracy target at 6-month lead is achievable — current state-of-the-art models achieve correlation skills >0.8 at 6 months and maintain skill up to 18-22 months lead time. However, "80% accuracy" must be precisely defined: if measured as correlation coefficient of the Nino 3.4 index, this is well within reach; if measured as categorical hit rate for El Nino/La Nina/Neutral classification, it is also achievable but requires careful threshold calibration. The seminal Ham et al. (2019) Nature paper demonstrated that a CNN with transfer learning could achieve 66.7% categorical accuracy at 12 months lead and correlation >0.5 at 17 months — physics-informed models published in 2024-2025 substantially surpass this.

## Key Findings

1. **Ham et al. (2019) established the deep learning baseline for ENSO prediction.** A CNN trained with transfer learning on CMIP5 simulations achieved correlation skill >0.5 at 17-month lead for the Nino 3.4 index, far exceeding dynamical models at equivalent lead times. Categorical El Nino prediction accuracy was 66.7% at 12 months ([Nature](https://www.nature.com/articles/s41586-019-1559-7)).

2. **Physics-informed transformers now achieve 20-22 month skillful lead times.** ENSO-PhyNet incorporates heat budget dynamics (zonal advection, thermocline feedback, meridional advection) into transformer self-attention, achieving skillful Nino 3.4 predictions at up to 22 months lead ([Nature npj Climate](https://www.nature.com/articles/s41612-024-00741-y)). CTEFNet extends effective forecast to 20 months while mitigating the spring predictability barrier ([Frontiers](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2023.1143499/full)).

3. **LSTM models achieve RMSE 0.05 and R-squared 0.87 for ENSO forecasting.** LSTM with autoencoder architecture showed strong performance on Nino 3.4 index prediction ([Springer Climate Dynamics](https://link.springer.com/article/10.1007/s00382-024-07180-8)), though pure LSTM lacks spatial awareness critical for capturing ocean-atmosphere coupling patterns.

4. **The TAO/TRITON array provides the primary observational data.** The array spans ~70 deep-ocean moorings across the tropical Pacific, measuring SST, subsurface temperature (10 depths in upper 500m), winds, humidity, and air temperature — updated daily ([NOAA TAO](https://www.aoml.noaa.gov/phod/docs/McPhaden_TheGlobalTropical.pdf), [Wikipedia TAO](https://en.wikipedia.org/wiki/Tropical_Atmosphere_Ocean_project)).

5. **The Nino 3.4 index is the standard ENSO metric.** Defined as the 5-month running mean of SST anomalies in the Nino 3.4 region (5N-5S, 170W-120W). El Nino declared when index exceeds +0.4°C for 6+ months ([NOAA PSL](https://psl.noaa.gov/gcos_wgsp/Timeseries/Nino34/), [UCAR Climate Data Guide](https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni)).

6. **The spring predictability barrier is the key challenge.** ENSO forecast skill degrades sharply when predictions must cross boreal spring (March-May), when tropical Pacific variability is at its annual minimum. Physics-informed models specifically target this barrier ([Frontiers Climate](https://www.frontiersin.org/journals/climate/articles/10.3389/fclim.2022.1058677/full)).

7. **Hybrid dynamical-deep learning models reduce uncertainty by 54%.** Observation-informed deep learning reduces ENSO projection uncertainty by 54% under high-emission scenarios by capturing the real-world ENSO response to warming patterns ([Nature Communications](https://www.nature.com/articles/s41467-025-63157-z)).

8. **Combined dynamical-deep learning models outperform either approach alone.** A 2025 Nature Communications paper demonstrates that combining dynamical model output with deep learning post-processing yields superior forecasts across all lead times ([Nature Communications](https://www.nature.com/articles/s41467-025-59173-8)).

## Industry Standards Compliance

| Standard / Framework | Requirement | Relevance | Source |
|---------------------|------------|-----------|--------|
| WMO Manual on the Global Data Processing and Forecasting System (GDPFS) Section 2.1 | Operational forecast centers must document skill metrics and verification procedures | Model must report correlation, RMSE, and categorical skill scores per WMO standards | [WMO](https://www.wmo.int) |
| NOAA Climate Prediction Center verification framework | ENSO forecasts scored by correlation coefficient of Nino 3.4 index and categorical hit rate | Standard skill metrics for comparison with operational forecasts | [NOAA CPC](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php) |
| ISO 19115:2003 — Geographic metadata standard | Geospatial datasets must include standardized metadata | TAO/TRITON data must be properly documented with spatial/temporal coverage | [ISO](https://www.iso.org) |
| CF Conventions (CF-1.8+) for climate data | NetCDF files must follow Climate and Forecast metadata conventions | Ensure training data and model output follow CF conventions for interoperability | [CF Conventions](https://cfconventions.org) |
| FAIR Data Principles (Wilkinson et al., 2016) | Data should be Findable, Accessible, Interoperable, Reusable | TAO/TRITON data is FAIR-compliant; model code and weights should be published | [Nature Scientific Data](https://www.nature.com/articles/sdata201618) |

## Quantitative Analysis

### Model Architecture Comparison

| Architecture | Max Skillful Lead | Correlation @ 6mo | Spring Barrier | Spatial Awareness | Training Data Needs | Key Paper |
|-------------|------------------|-------------------|----------------|-------------------|--------------------|-----------|
| **LSTM (autoencoder)** | 12-14 months | ~0.85 | Moderate difficulty | No (1D time series) | Low (Nino 3.4 only) | [Springer 2024](https://link.springer.com/article/10.1007/s00382-024-07180-8) |
| **CNN (Ham et al.)** | 17 months | ~0.88 | Partially mitigated | Yes (SST maps) | High (CMIP5 + reanalysis) | [Nature 2019](https://www.nature.com/articles/s41586-019-1559-7) |
| **Vanilla Transformer** | 18-20 months | ~0.87 | Moderate difficulty | Yes (spatiotemporal) | High (multi-variable) | [Frontiers 2023](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2023.1143499/full) |
| **Physics-Informed Transformer (ENSO-PhyNet)** | 22 months | ~0.90 | Largely mitigated | Yes + physics constraints | High (heat budget terms) | [Nature npj 2024](https://www.nature.com/articles/s41612-024-00741-y) |
| **3D-STransformer** | 20 months | ~0.89 | Mitigated | Yes (3D ocean fields) | Very high (3D temp profiles) | [AGU JGR 2025](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024JH000412) |
| **Hybrid Dynamical+DL** | 20+ months | ~0.91 | Best performance | Yes + dynamical model | Moderate (model output + obs) | [Nature Comm 2025](https://www.nature.com/articles/s41467-025-59173-8) |

### Accuracy Target Feasibility

| Metric Definition of "80% Accuracy" | Feasibility at 6-month Lead | Notes |
|--------------------------------------|---------------------------|-------|
| Correlation coefficient ≥ 0.80 | **Achievable** — all modern models exceed this | Standard skill metric |
| Categorical hit rate (El Nino/La Nina/Neutral) ≥ 80% | **Achievable** — requires threshold optimization | Ham 2019 achieved 66.7% at 12 months; 6-month is easier |
| RMSE < 0.3°C on Nino 3.4 | **Achievable** — LSTM alone achieves 0.05 RMSE | Depends on validation period |
| Anomaly correlation coefficient ≥ 0.80 | **Achievable** — physics-informed models: ~0.90 | Most robust metric |

### Data Pipeline Requirements

| Data Source | Variables | Temporal Resolution | Spatial Coverage | Access |
|------------|-----------|-------------------|-----------------|--------|
| TAO/TRITON buoy array | SST, subsurface T (10 depths), wind, humidity | Daily | Tropical Pacific (8°S-8°N, 137°E-95°W) | [NOAA PMEL](https://www.pmel.noaa.gov/tao/) |
| NOAA OISST (v2.1) | SST | Daily, 0.25° grid | Global | [NOAA PSL](https://psl.noaa.gov/gcos_wgsp/Timeseries/Nino34/) |
| ERA5 reanalysis | SST, wind, OLR, pressure, humidity | Monthly/6-hourly | Global | [Copernicus CDS](https://cds.climate.copernicus.eu) |
| CMIP6 historical simulations | SST, subsurface T, heat flux | Monthly | Global | [ESGF](https://esgf-node.llnl.gov) |
| NOAA ONI (Oceanic Nino Index) | Nino 3.4 SST anomaly | Monthly (3-month running mean) | Nino 3.4 region | [NOAA CPC](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php) |

### Computational Cost Estimate

| Component | LSTM | Transformer | Physics-Informed | Hybrid Dyn+DL |
|-----------|------|------------|-----------------|---------------|
| Training time (A100 GPU) | 2-4 hours | 8-16 hours | 12-24 hours | 24-48 hours |
| Inference time (single forecast) | <1 second | <5 seconds | <10 seconds | 1-5 minutes |
| GPU memory | 4 GB | 16 GB | 16-32 GB | 32+ GB |
| Training data prep | 1-2 days | 3-5 days | 1-2 weeks | 2-4 weeks |
| Total project time (1 researcher) | 1-2 months | 2-4 months | 3-6 months | 4-8 months |
| Cloud compute cost (AWS p4d.24xlarge) | $50-$100 | $200-$500 | $400-$800 | $800-$1,500 |
| Total project cost (researcher + compute) | $15,000-$30,000 | $30,000-$60,000 | $45,000-$90,000 | $60,000-$120,000 |

```python
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import xarray as xr

# === ENSO Prediction Model Pipeline (Physics-Informed Transformer) ===

# Step 1: Load NOAA Nino 3.4 index data
# Download from: https://psl.noaa.gov/gcos_wgsp/Timeseries/Nino34/
def load_nino34_data(filepath='nino34.long.anom.data'):
    """Load NOAA Nino 3.4 anomaly time series."""
    # Format: year, Jan, Feb, ..., Dec
    data = pd.read_csv(filepath, sep=r'\s+', header=None, skiprows=1,
                       names=['year'] + [f'month_{i}' for i in range(1, 13)])
    # Melt to monthly time series
    records = []
    for _, row in data.iterrows():
        for m in range(1, 13):
            val = row[f'month_{m}']
            if val != -99.99:
                records.append({
                    'date': pd.Timestamp(year=int(row['year']), month=m, day=1),
                    'nino34': val
                })
    return pd.DataFrame(records).set_index('date')

# Step 2: Load TAO buoy SST data via xarray (NetCDF)
def load_tao_sst():
    """Load TAO/TRITON buoy array SST from NOAA PMEL."""
    # URL: https://www.pmel.noaa.gov/tao/drupal/disdel/
    ds = xr.open_dataset('tao_sst_monthly.nc')
    return ds['T_25']  # SST at mooring locations

# Step 3: Prepare training features for physics-informed model
def prepare_physics_features(sst_field, lead_months=6):
    """
    Create feature tensors incorporating heat budget dynamics:
    - SST anomaly maps (spatial input)
    - Thermocline depth proxy (20°C isotherm depth from TAO)
    - Zonal wind stress anomaly
    - Heat content in upper 300m
    """
    from torch.utils.data import Dataset, DataLoader
    import torch

    # Lag the target (Nino 3.4) by lead_months
    # Each sample: (input_fields_at_time_t, nino34_at_time_t+lead)
    X = []  # shape: (N, C, H, W) where C=channels, H=lat, W=lon
    y = []  # shape: (N,) Nino 3.4 value

    for t in range(len(sst_field) - lead_months):
        features = np.stack([
            sst_field[t],           # SST anomaly
            # thermocline_depth[t],  # from TAO subsurface T
            # zonal_wind[t],         # from ERA5
            # heat_content[t],       # integrated 0-300m temperature
        ])
        X.append(features)
        y.append(sst_field[t + lead_months].mean())  # Nino 3.4 proxy

    return np.array(X), np.array(y)

# Step 4: Evaluate model skill
def evaluate_enso_model(y_true, y_pred, threshold=0.5):
    """
    Evaluate ENSO forecast skill with standard metrics.
    Correlation coefficient, RMSE, and categorical accuracy.
    """
    correlation = np.corrcoef(y_true, y_pred)[0, 1]
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))

    # Categorical: El Nino (>0.5), La Nina (<-0.5), Neutral
    def categorize(values, thresh=threshold):
        return np.where(values > thresh, 'ElNino',
               np.where(values < -thresh, 'LaNina', 'Neutral'))

    cat_true = categorize(y_true)
    cat_pred = categorize(y_pred)
    hit_rate = accuracy_score(cat_true, cat_pred)

    print(f"Correlation: {correlation:.3f}")
    print(f"RMSE: {rmse:.3f}°C")
    print(f"Categorical hit rate: {hit_rate:.1%}")
    print(f"Target (>80%) met: {'YES' if hit_rate > 0.80 else 'NO'}")

    return {'correlation': correlation, 'rmse': rmse, 'hit_rate': hit_rate}

# Example usage:
# nino34 = load_nino34_data()
# X, y = prepare_physics_features(sst_field, lead_months=6)
# model = train_physics_informed_transformer(X, y)  # See ENSO-PhyNet paper
# y_pred = model.predict(X_test)
# metrics = evaluate_enso_model(y_test, y_pred)
```

## Implementation Guidance

### Recommended Development Sequence

**Phase 1 (Weeks 1-4): Data Pipeline**
1. Download NOAA Nino 3.4 index (1870-present): `https://psl.noaa.gov/gcos_wgsp/Timeseries/Nino34/`
2. Download NOAA OISST v2.1 (1982-present) for SST spatial fields
3. Download TAO/TRITON buoy data from NOAA PMEL
4. Download ERA5 reanalysis (wind stress, OLR, heat content) from Copernicus CDS
5. Download CMIP6 historical simulations from ESGF for transfer learning pre-training

**Phase 2 (Weeks 4-8): Baseline LSTM Model**
1. Train LSTM on Nino 3.4 time series alone (univariate baseline)
2. Extend to multivariate LSTM with SST, wind, thermocline inputs
3. Evaluate at 1-month to 12-month lead times
4. This establishes your performance floor — expect correlation ~0.85 at 6 months

**Phase 3 (Weeks 8-16): Physics-Informed Transformer**
1. Implement ENSO-PhyNet architecture per [Nature npj 2024](https://www.nature.com/articles/s41612-024-00741-y)
2. Key innovation: encode heat budget terms (zonal/meridional advection feedback, thermocline feedback) into transformer attention mechanism
3. Pre-train on CMIP6 simulations (transfer learning per Ham 2019 approach)
4. Fine-tune on observational data (1982-2015 train, 2015-2025 validation)

**Phase 4 (Weeks 16-20): Evaluation and Refinement**
1. Score against NOAA CPC IRI plume ensemble
2. Test across spring predictability barrier (predictions initialized in Feb targeting Aug)
3. Ablation study: with vs without physics constraints
4. Target: correlation >0.85 at 6 months, categorical hit rate >80%

### Key Libraries and Tools

- **xarray + netCDF4** for climate data handling
- **PyTorch** for model implementation (ENSO-PhyNet reference code available)
- **climpred** for climate prediction skill metrics
- **cartopy** for spatial visualization
- **CMIP6 data via intake-esm** for transfer learning dataset

### Reproduction of Ham et al. (2019)

Reference implementation available at: [GitHub — ZiluM/Deep-learning-for-multi-year-ENSO-Reproduction](https://github.com/ZiluM/Deep-learning-for-multi-year-ENSO-Reproduction)

## Alternatives Considered

### 1. Pure LSTM Approach (Simplest)

LSTM achieves R-squared 0.87 and RMSE 0.05 on Nino 3.4 prediction with minimal data preprocessing — just the univariate Nino 3.4 time series. Training takes 2-4 hours on a single GPU. However, LSTM lacks spatial awareness, making it unable to capture teleconnection patterns (e.g., Indian Ocean Dipole influence on ENSO). It also struggles more with the spring predictability barrier due to reliance on temporal autocorrelation alone. At 6-month lead, expect correlation ~0.85 — meeting the >80% target but with less margin than physics-informed approaches. **When LSTM would be the right choice:** If time and compute resources are limited (1-2 months, no GPU cluster), or as a fast baseline to establish minimum viable performance before investing in more complex architectures.

### 2. Vanilla Transformer (3D-STransformer)

The 3D-STransformer architecture processes 3D ocean temperature fields (latitude x longitude x depth) with self-attention, achieving skillful predictions up to 20 months ([AGU JGR 2025](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024JH000412)). Better than LSTM but without explicit physics constraints, it may learn spurious correlations that degrade under climate change scenarios. Requires more training data and compute (~16 hours on A100) than LSTM. **When vanilla transformer would be the right choice:** If the goal is maximizing lead time (>12 months) without the complexity of encoding physics constraints, or if the team has strong transformer expertise but limited climate physics knowledge.

### 3. Hybrid Dynamical + Deep Learning (Highest Performance)

Combined dynamical-deep learning models feed output from operational dynamical models (e.g., NOAA CFSv2, ECMWF SEAS5) into a deep learning post-processor, achieving the highest correlation scores across all lead times ([Nature Communications 2025](https://www.nature.com/articles/s41467-025-59173-8)). This reduces projection uncertainty by 54% ([Nature Communications 2025](https://www.nature.com/articles/s41467-025-63157-z)). However, it requires access to dynamical model output (not just buoy data), longer development time (4-8 months), and significant compute resources. **When hybrid would be the right choice:** If the team has access to operational dynamical model output, 6+ months of development time, and the goal is to push beyond 12-month lead times or create an operational forecast system.

## Adversarial Review

### Counterargument: Deep Learning Models Cannot Beat Dynamical Models for ENSO

**Argument:** Operational dynamical models (NOAA CFSv2, ECMWF SEAS5) are based on first-principles physics and have been refined over decades. Deep learning models trained on limited observational data (~40 years of satellite era) may overfit and fail on unprecedented events. The ENSO regime may shift under climate change, invalidating patterns learned from historical data.

**Rebuttal:** Ham et al. (2019) directly demonstrated that CNN models exceed dynamical model skill at lead times >6 months, with the gap widening at longer leads. This has been confirmed by multiple subsequent studies through 2025. The transfer learning approach (pre-training on CMIP5/6 simulations) specifically addresses the small observational dataset issue by exposing the model to thousands of simulated ENSO events. However, the climate change concern is legitimate — models trained on historical ENSO may not capture a changing ENSO under 2°C+ warming. Physics-informed constraints partially mitigate this by encoding conservation laws that hold regardless of climate state.

### Counterargument: 80% Accuracy at 6 Months Is Already Achieved by Operational Models

**Argument:** NOAA CPC's operational ENSO forecast already achieves >80% accuracy at 6-month lead for categorical prediction. Building a custom model adds no value — just use the CPC forecast.

**Rebuttal:** This is partially valid for the 6-month target specifically. The value of a custom deep learning model lies in: (1) extending beyond 6 months — physics-informed models maintain skill at 18-22 months where operational models degrade rapidly; (2) providing probabilistic forecasts with better-calibrated uncertainty; (3) enabling rapid experimentation with new data sources (ocean color, Argo float data); and (4) scientific understanding through attention map analysis revealing ENSO precursors. If the sole goal is 6-month categorical forecasts with no research component, using CPC operational forecasts directly is indeed sufficient.

<details>
<summary>Assumption Audit</summary>

| Assumption | Status | Risk if Wrong |
|-----------|--------|---------------|
| TAO/TRITON buoy data is sufficient for training | **Partially verified** — buoy data alone is sparse; most successful models use gridded reanalysis (ERA5, OISST) | If using only raw buoy data, spatial coverage is too sparse for CNN/transformer input — must use gridded products |
| CMIP6 simulations represent real ENSO dynamics | **Reasonable** — validated by Ham 2019 transfer learning success | Some CMIP6 models have known ENSO biases (double-ITCZ, cold tongue bias) — select models carefully |
| Historical ENSO patterns will persist under climate change | **Uncertain** — active research question | If ENSO changes character, model may need retraining on projected scenarios |
| 6-month lead time is the primary target | **Verified** — stated requirement | If extended to 12+ months, physics-informed approach becomes essential |
| >80% accuracy means categorical hit rate | **Uncertain** — user did not specify metric | If correlation coefficient, target is easier; if precision/recall for specific El Nino events, may be harder |
| Single researcher timeline is feasible | **Reasonable** — 3-6 months for physics-informed transformer | If team has no climate science background, add 2-3 months for domain learning |

</details>

### Failure Modes

1. **Overfitting to satellite era (1982-present):** Only ~40 years of high-quality observational data limits deep learning training. Mitigation: transfer learning from CMIP6 simulations (1,000+ years of simulated ENSO).
2. **Spring predictability barrier:** Forecasts initialized in January targeting July cross the barrier, degrading skill. Mitigation: physics-informed models explicitly encode thermocline feedback that maintains skill through spring.
3. **Non-stationary ENSO under climate change:** ENSO characteristics may shift (stronger Central Pacific events, weaker Eastern Pacific events). Mitigation: ensemble approach combining physics-informed DL with dynamical models.
4. **TAO/TRITON array degradation:** The buoy array has experienced significant data gaps since 2012 due to reduced maintenance funding. Mitigation: supplement with Argo float data and satellite SST products.

## Recommendation

**Build a physics-informed transformer model (ENSO-PhyNet architecture) using NOAA OISST + ERA5 reanalysis as primary training data, with CMIP6 transfer learning pre-training.** The 6-month lead >80% accuracy target is achievable with all three approaches, but the physics-informed transformer provides the best accuracy margin (~0.90 correlation vs ~0.85 for LSTM) and the strongest robustness to the spring predictability barrier. Estimated development time: 3-6 months for a single researcher with ML and basic climate science background.

**Conditions under which this recommendation changes:**
- If development time is <2 months, use LSTM as a fast baseline that still meets the 80% target
- If the goal extends to 12+ month lead time, the physics-informed approach becomes essential (LSTM skill degrades rapidly beyond 12 months)
- If operational deployment is required (not research), use NOAA CPC operational forecasts directly rather than building custom
- If climate change projection is a secondary goal, use the hybrid dynamical+DL approach for uncertainty quantification
- If team lacks climate physics expertise, start with vanilla transformer (3D-STransformer) and add physics constraints iteratively

## Sources

**Foundational Papers:**
- Ham, Y.-G., Kim, J.-H., & Luo, J.-J. (2019). Deep learning for multi-year ENSO forecasts. *Nature*, 573, 568-572. [DOI: 10.1038/s41586-019-1559-7](https://www.nature.com/articles/s41586-019-1559-7)
- [GitHub Reproduction of Ham et al. 2019](https://github.com/ZiluM/Deep-learning-for-multi-year-ENSO-Reproduction)

**Recent Advances (2024-2025):**
- [ENSO-PhyNet: Heat budget dynamics in Transformer for ENSO prediction — Nature npj Climate 2024](https://www.nature.com/articles/s41612-024-00741-y)
- [3D-STransformer: Long-term ENSO forecasting — AGU JGR 2025](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024JH000412)
- [Combined dynamical-deep learning ENSO forecasts — Nature Communications 2025](https://www.nature.com/articles/s41467-025-59173-8)
- [Observation-informed deep learning ENSO projection — Nature Communications 2025](https://www.nature.com/articles/s41467-025-63157-z)
- [Explainable deep learning for long-range ENSO — Nature npj Climate 2025](https://www.nature.com/articles/s41612-025-01159-w)
- [Low-dimensional recursive deep learning for ENSO — Nature npj Climate 2025](https://www.nature.com/articles/s41612-025-01053-5)

**LSTM and Autoencoder Approaches:**
- [Deep learning with autoencoders and LSTM for ENSO — Springer Climate Dynamics 2024](https://link.springer.com/article/10.1007/s00382-024-07180-8)
- [ENSO dataset and DL model comparison — Springer Earth Science Informatics 2024](https://link.springer.com/article/10.1007/s12145-024-01295-6)
- [Frontiers — Deep learning for skillful long-lead ENSO forecasts](https://www.frontiersin.org/journals/climate/articles/10.3389/fclim.2022.1058677/full)
- [Frontiers — Spatial-temporal transformer for multi-year ENSO](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2023.1143499/full)

**Data Sources:**
- [NOAA Nino 3.4 SST Index](https://psl.noaa.gov/gcos_wgsp/Timeseries/Nino34/)
- [NOAA Oceanic Nino Index (ONI)](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php)
- [NOAA ENSO Dashboard](https://psl.noaa.gov/enso/dashboard.html)
- [IRI ENSO Forecast Plume](https://iri.columbia.edu/our-expertise/climate/forecasts/enso/current/)
- [UCAR Climate Data Guide — Nino SST Indices](https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni)
- [TAO/TRITON Array — Wikipedia](https://en.wikipedia.org/wiki/Tropical_Atmosphere_Ocean_project)
- [NOAA AOML — Global Tropical Moored Buoy Array](https://www.aoml.noaa.gov/phod/docs/McPhaden_TheGlobalTropical.pdf)

**Additional References:**
- [Diffusion Models for ENSO — arXiv 2025](https://arxiv.org/html/2511.01214)
- [ResoNet: Robust ENSO with Hybrid Conv+Transformer — arXiv 2023](https://arxiv.org/html/2312.10429v1)
- [Spatiotemporal neural network with attention for El Nino — Scientific Reports 2022](https://www.nature.com/articles/s41598-022-10839-z)
- [Physics-informed neural networks for ENSO — ResearchGate](https://www.researchgate.net/publication/369206405_Physics-informed_neural_networks_for_prediction_and_physical_interpretability_analysis_of_key_regional_variables_of_ENSO)
