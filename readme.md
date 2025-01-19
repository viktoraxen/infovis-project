# Character Death Timeline Visualization

## Description
This script visualizes the death timeline of characters from a show across seasons using **Plotly**. It highlights deaths, killer information, and character importance, offering insights into key moments and their narrative weight.

## Technologies Used
- **Python**: Core programming language.
- **Pandas**: For data manipulation and processing.
- **Plotly Express**: For creating an interactive scatter plot.

## Instructions to Run
1. **Setup Environment**:
   - Install required libraries:
     ```bash
     pip install pandas plotly
     ```

2. **Data Requirements**:
   - Place the following `.tsv` files in a folder named `data`:
     - `characters.tsv`
     - `episodes.tsv`
     - `scenes.tsv`
     - `scenes_characters.tsv`
     - `killers.tsv`
   - Ensure the files follow the expected schema as implied by the code.

3. **Run the Script**:
   - Execute the Python script:
     ```bash
     python death_timeline.py
     ```
   - The visualization will open in your browser.

## Output
An interactive scatter plot:
- **X-axis**: Episode titles.
- **Y-axis**: Seasons (with jitter to differentiate multiple deaths in the same episode).
- **Color**: Character importance score.
- **Tooltip**: Displays detailed death and killer information.


## Screentime per episode for characters from house Targaryen

### Dependencies

The dependencies are

- D3.js

All dependencies are included in the vendor/ directory.

### Instructions to run

Run the command

`python3 -m http.server 8000`

Using a web browser, open the url `localhost:8000`, and navigate to
`viz/st-per-episode.html`.


## Casualties Per House Visualization 

### Dependencies

The dependencies are

- D3.js

All dependencies are included in the vendor/ directory.

### Instructions to run

Run the command

`python3 -m http.server 8000`

Using a web browser, open the url `localhost:8000`, and navigate to
`viz/casualties_per_house.html`.