"""
project_consumer_brandon.py

Read buzz messages from file and visualize average message length per author.
"""

#####################################
# Import Modules
#####################################
import json
import pathlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils.utils_logger import logger

#####################################
# Global Variables
#####################################
stats = {}   # Track total chars, count, avg per author

# Paths
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FILE = DATA_FOLDER.joinpath("buzz_live.json")

#####################################
# Update Function
#####################################
def update_chart(frame):
    """Read new messages and update the live bar chart."""
    try:
        with DATA_FILE.open("r") as f:
            lines = f.readlines()

        for line in lines:
            message = json.loads(line.strip())
            author = message.get("author", "Unknown")
            text = message.get("message", "")

            if author not in stats:
                stats[author] = {"total_chars": 0, "count": 0, "avg": 0.0}

            length = len(text)
            stats[author]["total_chars"] += length
            stats[author]["count"] += 1
            stats[author]["avg"] = stats[author]["total_chars"] / stats[author]["count"]

        # Prepare chart data
        authors = list(stats.keys())
        avgs = [stats[a]["avg"] for a in authors]

        # Clear and redraw chart
        plt.cla()
        plt.bar(authors, avgs, color="skyblue")
        plt.xlabel("Author")
        plt.ylabel("Average Message Length (chars)")
        plt.title("Avg Message Length per Author")

    except Exception as e:
        logger.error(f"Error updating chart: {e}")

#####################################
# Main
#####################################
def main():
    logger.info("START consumer...")
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, update_chart, interval=2000)
    plt.show()

#####################################
# Conditional Execution
#####################################
if __name__ == "__main__":
    main()
