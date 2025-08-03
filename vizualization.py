import matplotlib.pyplot as plt

def draw_diagram_by_words(words, counts, title="Top Words"):
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.title(title)
    plt.xlabel("Word")
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()