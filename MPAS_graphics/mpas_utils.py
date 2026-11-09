"""Shared helpers for MPAS notebooks in this repo."""

import numpy as np


def vertical_interpolate(vcoord_data, interp_var, interp_levels):
    """A function to interpolate sounding data from each station to
    every millibar. Assumes a log-linear relationship.

    Input
    -----
    vcoord_data : A 1D array of vertical level values (e.g., pressure from a radiosonde)
    interp_var : A 1D array of the variable to be interpolated to all pressure levels
    interp_levels : A 1D array containing vertical levels to interpolate to

    Return
    ------
    interp_data : A 1D array that contains the interpolated variable on the interp_levels
    """

    # Make vertical coordinate data and grid level log variables
    lnp = np.log(vcoord_data)
    lnp_intervals = np.log(interp_levels)

    # Use numpy to interpolate from observed levels to grid levels
    interp_data = np.interp(lnp_intervals[::-1], lnp[::-1], interp_var[::-1])[::-1]

    # Mask for missing data (generally only near the surface)
    mask_low = interp_levels > vcoord_data[0]
    mask_high = interp_levels < vcoord_data[-1]
    interp_data[mask_low] = interp_var[0]
    interp_data[mask_high] = interp_var[-1]

    return interp_data


def vertical_interpolate_mpas(vcoord_2d, vinterp_2d, plev_1d):
    """A function to interpolate MPAS grid data to
    specified millibar. Assumes a log-linear relationship.
    input:
        vcoord_2d  : 2D vertical level values (e.g., pressure)
        vinterp_2d : 2D array of the variable to be interpolated to all pressure levels
        plev_1d    : 1D array containing vertical levels to interpolate to
    return:
        interp_2d : 2D array that contains the interpolated variable on the interp_levels
    """
    interp_2d = np.empty((len(plev_1d), vinterp_2d.shape[0]))

    for nc in range(vinterp_2d.shape[0]):
        interp_2d[:, nc] = vertical_interpolate(vcoord_2d[nc].values, vinterp_2d[nc].values, plev_1d)

    return interp_2d


def mpas_lonlat_deg(lonCell, latCell):
    """Convert MPAS lonCell/latCell (radians, as stored on disk) to degrees,
    with longitude wrapped to [-180, 180] for plotting/triangulation.

    Input
    -----
    lonCell, latCell : arrays of cell coordinates in radians

    Return
    ------
    lon_deg, lat_deg : arrays of cell coordinates in degrees
    """
    lon_deg = np.degrees(lonCell)
    lat_deg = np.degrees(latCell)
    lon_deg = ((lon_deg + 180) % 360) - 180

    return lon_deg, lat_deg


def cell_edge_length_cv(nEdgesOnCell, edgesOnCell, dvEdge):
    """Coefficient of variation (std/mean) of edge lengths around each MPAS cell.

    A simple mesh-quality proxy: low values indicate near-regular hexagons;
    higher values flag irregular cells (e.g. refinement transition zones,
    pentagons/heptagons, or mesh-generation defects).

    Input
    -----
    nEdgesOnCell : 1D array (nCells,), number of edges per cell
    edgesOnCell  : 2D array (nCells, maxEdges), 1-based edge indices (0-padded)
    dvEdge       : 1D array (nEdges,), edge length

    Return
    ------
    cv : 1D array (nCells,), coefficient of variation of edge length per cell
    """
    nCells = nEdgesOnCell.shape[0]
    cv = np.empty(nCells)

    for c in range(nCells):
        n = nEdgesOnCell[c]
        lens = dvEdge[edgesOnCell[c, :n] - 1]
        cv[c] = lens.std() / lens.mean()

    return cv
