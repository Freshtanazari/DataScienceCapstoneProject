"""Generate four square (1:1) capstone flowchart PNGs for PowerPoint."""
import textwrap
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

SIZE = 10          # square canvas units
DPI = 180          # 1800 x 1800 px output
BOX_W = 4.15
FONT = 6.8
TITLE_FS = 11


def wrap(text, width=38):
    return "\n".join(textwrap.wrap(text, width=width))


def draw_box(ax, x, y, w, h, text, fc="#E8F4FD", ec="#1B4F72"):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.06",
        linewidth=1.0, edgecolor=ec, facecolor=fc,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=FONT, linespacing=1.15)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=10,
        linewidth=1.0, color="#2C3E50",
        shrinkA=3, shrinkB=3,
    ))


def box_height(text):
    lines = text.count("\n") + 1
    return max(0.72, 0.30 * lines + 0.38)


def make_chart(title, steps, filename):
    fig, ax = plt.subplots(figsize=(SIZE, SIZE))
    ax.set_xlim(0, SIZE)
    ax.set_ylim(0, SIZE)
    ax.axis("off")
    ax.set_facecolor("white")

    ax.text(
        SIZE / 2, 9.55, title,
        ha="center", va="center",
        fontsize=TITLE_FS, fontweight="bold", color="#1B2631",
    )

    left_x, right_x = 2.55, 7.45
    split = (len(steps) + 1) // 2
    left_steps = steps[:split]
    right_steps = steps[split:]

    top_y = 8.55
    bottom_y = 0.95
    span = top_y - bottom_y

    def column_positions(count):
        if count == 1:
            return [top_y - span / 2]
        gap = span / (count - 1)
        return [top_y - i * gap for i in range(count)]

    left_pos = column_positions(len(left_steps))
    right_pos = column_positions(len(right_steps))

    left_boxes = []
    for (text, color), y in zip(left_steps, left_pos):
        t = wrap(text)
        h = box_height(t)
        draw_box(ax, left_x, y, BOX_W, h, t, fc=color)
        left_boxes.append((left_x, y, h))

    right_boxes = []
    for (text, color), y in zip(right_steps, right_pos):
        t = wrap(text)
        h = box_height(t)
        draw_box(ax, right_x, y, BOX_W, h, t, fc=color)
        right_boxes.append((right_x, y, h))

    for i in range(len(left_boxes) - 1):
        _, y1, h1 = left_boxes[i]
        _, y2, h2 = left_boxes[i + 1]
        arrow(ax, left_x, y1 - h1 / 2, left_x, y2 + h2 / 2)

    if left_boxes and right_boxes:
        _, y1, h1 = left_boxes[-1]
        _, y2, h2 = right_boxes[0]
        arrow(
            ax,
            left_x + BOX_W / 2, y1,
            right_x - BOX_W / 2, y2,
        )

    for i in range(len(right_boxes) - 1):
        _, y1, h1 = right_boxes[i]
        _, y2, h2 = right_boxes[i + 1]
        arrow(ax, right_x, y1 - h1 / 2, right_x, y2 + h2 / 2)

    out = f"C:/Users/lz/Desktop/datascience/presentation/{filename}"
    fig.savefig(
        out, dpi=DPI, facecolor="white",
        bbox_inches=None, pad_inches=0,
    )
    plt.close(fig)
    print(f"Saved {out}")


api_steps = [
    ("Start: import requests, pandas, numpy, datetime", "#D5F5E3"),
    ("Define helpers: getBoosterVersion, getLaunchSite, getPayloadData, getCoreData", "#D6EAF8"),
    ("GET static SpaceX launch JSON (API / IBM dataset)", "#D6EAF8"),
    ("Parse JSON and json_normalize into DataFrame", "#D6EAF8"),
    ("Subset columns: rocket, payloads, launchpad, cores, flight_number, date_utc", "#FCF3CF"),
    ("Filter single core/payload, parse dates, keep launches up to 2020-11-13", "#FCF3CF"),
    ("Resolve IDs: booster, payload mass/orbit, launch site, core outcome", "#FADBD8"),
    ("Build launch_dict DataFrame and rename launch sites", "#E8DAEF"),
    ("Keep Falcon 9 only and reset FlightNumber", "#E8DAEF"),
    ("Fill PayloadMass missing values with mean", "#E8DAEF"),
    ("Export dataset_part_1.csv", "#ABEBC6"),
]

web_steps = [
    ("Start: import requests, pandas, numpy, BeautifulSoup", "#D5F5E3"),
    ("Set Wikipedia URL for Falcon 9 / Falcon Heavy launches", "#D6EAF8"),
    ("requests.get(url) to download HTML", "#D6EAF8"),
    ("Parse page with BeautifulSoup", "#D6EAF8"),
    ("Find launch table with Date and time (UTC) column", "#FCF3CF"),
    ("Extract headers and rows into lists", "#FCF3CF"),
    ("Create pandas DataFrame from scraped table", "#FCF3CF"),
    ("Clean values: booster version, landing pad, outcome", "#FADBD8"),
    ("Drop rows with None in key columns", "#FADBD8"),
    ("Split Date and time into separate columns", "#E8DAEF"),
    ("Export spacex_web_scraped.csv", "#ABEBC6"),
]

wrangle_steps = [
    ("Start: import pandas and numpy", "#D5F5E3"),
    ("Load dataset_part_1.csv", "#D6EAF8"),
    ("Check missing values and column dtypes", "#D6EAF8"),
    ("LaunchSite counts with value_counts()", "#FCF3CF"),
    ("Orbit counts with value_counts()", "#FCF3CF"),
    ("Outcome counts to landing_outcomes", "#FCF3CF"),
    ("Define bad_outcomes for failed landings", "#FADBD8"),
    ("Create Class label: 1 success, 0 failure", "#FADBD8"),
    ("Compute success rate with Class.mean()", "#E8DAEF"),
    ("Export dataset_part_2.csv", "#ABEBC6"),
]

ml_steps = [
    ("Start: import sklearn, pandas, numpy, matplotlib, seaborn", "#D5F5E3"),
    ("Load dataset_part_2 labels and dataset_part_3 features", "#D6EAF8"),
    ("Y = data Class column as NumPy array", "#D6EAF8"),
    ("StandardScaler fit_transform on X", "#FCF3CF"),
    ("train_test_split 80/20 with random_state=2", "#FCF3CF"),
    ("GridSearchCV cv=10: Logistic Regression, SVM, Tree, KNN", "#FADBD8"),
    ("Pick best_params and best_score per model", "#FADBD8"),
    ("Evaluate test accuracy and confusion matrices", "#E8DAEF"),
    ("Bar chart compare models; top ~83.3% accuracy", "#E8DAEF"),
    ("Predict Falcon 9 first-stage landing Class 0 or 1", "#ABEBC6"),
]


if __name__ == "__main__":
    make_chart("1. SpaceX API Data Collection", api_steps, "flowchart_1_api_collection.png")
    make_chart("2. Wikipedia Web Scraping", web_steps, "flowchart_2_web_scraping.png")
    make_chart("3. Data Wrangling", wrangle_steps, "flowchart_3_data_wrangling.png")
    make_chart("4. Model Development", ml_steps, "flowchart_4_model_development.png")
