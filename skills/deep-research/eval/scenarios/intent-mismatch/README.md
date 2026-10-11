# internal-notes app

## Deployment constraints (NON-NEGOTIABLE)

This app handles regulated patient data under a data-residency mandate. Hard
constraints, set by compliance and not up for debate:

- **Fully on-premises only.** No third-party cloud or SaaS services may process,
  index, or store app data. No data may leave our own datacenter.
- No outbound connections from the data tier to external hosts.
- All search/indexing must run on hardware we own and control.

Any feature proposal that ships data to an external service is a non-starter.
