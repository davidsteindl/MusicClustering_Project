from matplotlib import ticker
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, HTML

"""
Calculates the Calinski-Harabasz-Index for diffrent k-values and return the k-value with the highest index.
"""

def evaluate_ch_index(Data_scaled, name, k_min=1, k_max=20):
    scores = []
    k_values = range(k_min, k_max + 1)

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(Data_scaled)
        index = calinski_harabasz_score(Data_scaled, labels)
        scores.append(index)

    plt.figure(figsize=(7, 5))
    plt.plot(k_values, scores, marker='o', label='CH Index')
    plt.title(f'Calinski-Harabasz Index for {name}')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('CH Index (higher is better)')
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    best_k = k_values[scores.index(max(scores))]
    best_score = max(scores)
    plt.scatter(best_k, best_score, color='red', s=100, label=f"Best k = {best_k}")

    plt.show()

    display(HTML(f"""
    <h3><b>Best result for <i>{name}</i></b></h3>
    <ul>
    <li>Optimal number of clusters: <b>k = {best_k}</b></li>
    <li>Corresponding Calinski-Harabasz Index: <b>{best_score:,.2f}</b></li>
    </ul>
    """))

    best_k = k_values[scores.index(max(scores))]

    return best_k, scores
