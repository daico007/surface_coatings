# Surface Coatings

## Overview
Surface Coatings (`surface_coatings`) is an [mBuild](https://github.com/mosdef-hub/mbuild) recipe to construct monolayer systems,
i.e., surfaces coated with monolayer films.
Recipes are designed to be add-ons to [mBuild](https://github.com/mosdef-hub/mbuild),
allowing users to construct classes of chemical systems utilizing routines developed earlier using [mBuild](https://github.com/mosdef-hub/mbuild).


## Installation
The `surface_coatings` can be install using `pip`. While its dependencies can be found in `environment.yml`. `mamba` is recommended to create the environment due to its ability to quickly solve the environmnet, however, `conda` would also work.
```bash
mamba env create --file environment.yml
mamba activate surface_coatings
pip install -e .
```

## Example Usage
```python
import mbuild as mb
from mbuild.lib.molecules import WaterSPC as H2O
from surface_coatings.surfaces import SilicaInterfaceCarve
from surface_coatings.chains import Alkylsilane
from surface_coatings import Monolayer, DualMonolayer, SolvatedMonolayer, SolvatedDualMonolayer

silane_chain = Alkylsilane()
silica_surface = SilicaInterfaceCarve()

silica_monolayer = Monolayer(surface=silica_surface,
                             chains=[silane_chain],
                             n_chains=100,
                             tile_x=1,
                             tile_y=1)
silica_monolayer.visualize()

# Create a dual monolayer with the created monolayer
dual_monolayer = DualMonolayer(top=mb.clone(silica_monolayer),
                               bottom=mb.clone(silica_monolayer),
                               separation=3)
dual_monolayer.visualize()

# Solvate a monolayer system
solvated_monolayer = SolvatedMonolayer(monolayer=mb.clone(silica_monolayer),
                                       solvent=H2O())

solvated_monolayer.visualize()

# Solvate a dual monolayer system
solvated_dual_monolayer = SolvatedDualMonolayer(dual_monolayer=dual_monolayer,
                                                solvent=H2O())
solvated_dual_monolayer.visualize()

```
