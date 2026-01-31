# Claude Code Instructions

## Code and Scripts

- Always save Python scripts and code snippets to files, don't just run them inline
- Save experimental work to the `experimentation/` folder (local only, gitignored):
  - `experimentation/code/` - Python scripts and snippets
  - `experimentation/data/` - Generated or temporary data
  - `experimentation/exhibits/` - Charts, graphs, outputs
- Update `experimentation/experimentation_notes.md` to log what was done
- Use descriptive filenames like `analysis_occupancy_by_city.py` or `generate_weather_data.py`
- Include a brief comment at the top of each script explaining what it does

## Visualization

- Use the **viridis** colormap for all graphs and charts
- Example: `plt.cm.viridis`, `cmap='viridis'`, `sns.color_palette('viridis')`

## Data

- The main dataset is in `case-studies/austria-hotels/data/modified/`
- Generated data should also be saved there
- Always show summary statistics after generating new data

## Python

- Run Python directly when possible, install packages as needed via `pip install`
- Prefer pandas for data manipulation
- Use matplotlib or seaborn for visualization

## Documentation Principles

### Knowledge Base Pages

- Extract reusable technical content into `da-knowledge/` pages
- Keep week content focused on pedagogy; link to knowledge pages for technical details
- Examples of knowledge pages:
  - `install-cli.qmd` - CLI tool installation
  - `terminal-basics.qmd` - Terminal commands
  - `joining-tables.qmd` - Join concepts
  - `technical-terms-page.qmd` - Glossary

### Multi-OS Instructions

- When instructions differ by operating system, use Quarto tabset panels:
```
::: {.panel-tabset}

### Windows
[Windows instructions]

### Mac
[Mac instructions]

### Linux
[Linux instructions]

:::
```

- This applies to: installation steps, terminal commands, file paths, environment variables
