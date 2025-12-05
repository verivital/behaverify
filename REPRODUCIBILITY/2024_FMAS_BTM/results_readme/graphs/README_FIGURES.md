# Paper Figures to Extract

These figures should be extracted from the paper PDF at: https://arxiv.org/pdf/2411.14162

## Required Figures:

1. **Figure 5** - Grid visualizations (10x10, 50x50 with dense/sparse obstacles)
   - Save as: `grid_examples_fig5.png`
   - Shows example grid layouts with obstacle patterns

2. **Figure 6** - Loop detection examples
   - Save as: `loop_detection_fig6.png`
   - Demonstrates potential loop scenarios that monitors detect

3. **Figure 8a** - Runtime timing comparisons
   - Save as: `timing_comparison_fig8.png`
   - Compares BehaVerify, Copilot, and Monitorless runtime performance

4. **Figure 8b** - Monitor file size comparisons
   - Save as: `file_sizes_fig8.png`
   - Compares automata complexity (file sizes) between frameworks

5. **Figure 9** - Design-time verification timing
   - Save as: `timing_design_time_fig9.png`
   - Shows nuXmv verification times for different grid sizes

## Extraction Instructions:

1. Download PDF from arXiv: `wget https://arxiv.org/pdf/2411.14162 -O fmas2024_btm.pdf`
2. Extract figures at 300+ DPI resolution
3. Crop to remove excess whitespace
4. Save as PNG files with names listed above
5. Delete this README_FIGURES.md file after extraction complete

## Alternative:

If figures cannot be extracted, the README can reference the paper directly with:
```markdown
See Figure X in the [paper](https://arxiv.org/pdf/2411.14162)
```
