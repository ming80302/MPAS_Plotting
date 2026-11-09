# MPAS_graphics

A collection of standalone Jupyter notebooks for visualizing and diagnosing MPAS
(Model for Prediction Across Scales) mesh geometry and model output. Each notebook
is self-contained; there's no shared pipeline or package, just `mpas_utils.py` for
the handful of functions duplicated across notebooks (see below).

## Environment

Depending on the notebook, you'll need some subset of: `xarray`, `netCDF4`,
`matplotlib`, `cartopy`, `scipy`, `pandas`, `uxarray`, `holoviews`, `geoviews`,
`bokeh`, `windrose`, `metpy`.

The `conda-env-miniforge3-uxarray-py` kernel (`/glade/u/home/mingge/miniforge3/envs/uxarray`)
has the full set and is what every notebook here is tested against. There's no
`environment.yml` in this repo yet — if you set one up, this is the env to export.

## Data paths

Every notebook hardcodes its input file paths (mostly under
`/glade/campaign/mmm/c3we/mingge/...`). They won't run as-is outside this account —
edit the path cell near the top before running elsewhere.

## `mpas_utils.py`

Shared helpers, imported by notebooks instead of each keeping its own copy:

- `vertical_interpolate`, `vertical_interpolate_mpas` — log-linear vertical
  interpolation to specified pressure levels.
- `mpas_lonlat_deg` — radians-to-degrees + dateline wrap for `lonCell`/`latCell`.
- `cell_edge_length_cv` — per-cell edge-length coefficient of variation, a mesh
  shape/quality proxy.

## Notebook index

**Mesh / grid**
- `plot_MPAS_mesh.ipynb` — global + regional mesh node scatter plots.
- `mesh_boundary_plot.ipynb` — limited-area mesh boundary outline (hand-rolled walk, and the equivalent uxarray subset).
- `regional_mesh_4MingChen.ipynb`, `regional_orthographic_terrain.ipynb` — regional mesh and terrain plots via uxarray.
- `plot_grid_ux.ipynb` — uxarray grid topology (nodes/edges/faces) visualization tour.
- `mesh_quality_diagnostics.ipynb` — cell-size and edge-length distributions, plus a per-cell shape-irregularity map; run this on a new mesh before trusting simulations on it.

**Fields**
- `plot_mpas_sst.ipynb`, `plot_mpas_ts.ipynb`, `plot_mpas_quiver_overlay_slp.ipynb` — SST, T2m, surface pressure + wind overlay maps via Delaunay tripcolor.
- `plot_diag_uxarray.ipynb` — surface temperature, MSLP, max wind, relative humidity, vorticity via uxarray (primal + dual grid).
- `mpas_ivgtyp_discrete.ipynb` — categorical land-cover plotting with a custom discrete colorbar.
- `mpas_regrid_comparison.ipynb` — regrid two unstructured sources onto a common lat/lon grid and difference them; the template for comparing two experiments, two resolutions, or model vs. obs/reanalysis.

**Vertical**
- `mpas_vertical_interp.ipynb`, `plot_mpas_vertical_section.ipynb` — vertical interpolation to pressure levels and a lat/lon cross-section.
- `mpas_skewt_profile.ipynb` — nearest-cell Skew-T/log-p profile with wind barbs (MetPy) from isobaric diagnostic output.
- `mpas_ke_spectrum.ipynb` — near-surface kinetic-energy spectrum vs. wavenumber (2D FFT), a standard mesoscale model-health check for noise/over-diffusion.

**Time series / health checks**
- `plot_mpas_spd_ts.ipynb`, `plot_mpas_windRose.ipynb` — wind speed time series and wind rose.
- `mpas_conservation_check.ipynb` — domain-integrated mass, moisture-budget closure, mean T2m/surface pressure, and kinetic energy over a run.
- `precip_hovmoller.ipynb` — longitude-time Hovmöller of hourly precipitation over a latitude band, for tracking propagating systems or a diurnal cycle.

**Subsetting / animation**
- `plot_subset_ux.ipynb` — uxarray regional subsetting (bounding box, bounding circle, nearest neighbor) and the inverse-index mapping back to the full grid.
- `prec_animation.ipynb` — animated precipitation (HoloViews), saved as MP4 and GIF.

## Notes

- Notebooks are committed with their outputs (including embedded images), so file
  sizes run into the low megabytes and diffs on re-run can be noisy. If that
  becomes a pain, `nbstripout` is the usual fix.
- `prec.mp4` / `prec_robinson.gif` are tracked directly in git — fine at this
  size, but worth moving to Git LFS if more/larger media gets added later.
