# animove

**Ani**mal **Move**ment project.

By:

* Zhean Robby Ganituen
* Jaztin Jacob Jimenez
* Reece Benedict Orense
* Ashley Paulianna Reyes
* Matthew Fraser Sim

## Setup

To make things easier, we use [`uv`](https://docs.astral.sh/uv/) as our build tool. You can find the [official installation guide here](https://docs.astral.sh/uv/getting-started/installation/).

Once `uv` is set up, simply execute the following command in your terminal:

```bash
uv sync
```

### Dependencies

The dependencies of the project are defined in [`pyproject.toml`](/pyproject.toml).

## Moving Around

This repository is organized into the following main directories:

1. [`data`](/data/): Contains the project datasets.
   1. `raw/`: Contains the raw data.
   2. `processed/`: Contains the updated raw datasets after cleaning
       and preprocessing.
2. [`notebooks`](/notebooks/): Contains the project Jupyter Notebooks.

## Dataset

We utilize data from the following study:

> Oliver, R. Y., et al. (2026). Interacting effects of human presence and landscape modification on birds and mammals. *Science*, 392, 879-884. DOI: 10.1126/science.adq3396

This data is hosted on [Movebank](https://www.movebank.org/cms/movebank-main), a free, online database of animal tracking data managed by the Max Planck Institute of Animal Behavior. The specific dataset used in our project is cited as:

> LaPoint S. 2026. Data from: Study "Carnivore movements near Black Rock Forest New York" [part]. Movebank Data Repository. <https://doi.org/10.5441/001/1.652>

**The dataset is available under the Creative Commons license [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en).**

## Converting Jupyter Notebooks to PDF

We have [nbconvert](https://nbconvert.readthedocs.io/) installed as a
developer dependency. Ensure that the necessary system-level
dependencies for `nbconvert` (this is Pandoc and a LaTeX distribution)
are installed on your machine.

To export a notebook to PDF, simply run:

```bash
uv run jupyter-nbconvert --to pdf notebooks/<some_ipynb>.ipynb
```
