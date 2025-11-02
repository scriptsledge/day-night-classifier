
# Project Analysis & Discussion

This document provides an analysis of the design and performance of the Day/Night scene classifier.

---

### 1. Rationale for Feature Selection

The initial plan, as per the lab brief, was to use manually extracted, subjective features. However, to create a more robust and reproducible model, a computational approach was adopted.

The final model uses a set of four objective features, automatically extracted from each image:

1.  **`brightness` (Grayscale Mean):** This feature provides a direct measure of the image's overall luminance. It is the most intuitive and powerful indicator for distinguishing between bright day scenes and dark night scenes.

2.  **`contrast` (Grayscale Standard Deviation):** This measures the difference between light and dark areas. Daytime scenes with direct sunlight often have higher contrast than dimly lit or artificially lit night scenes.

3.  **`colorfulness` (Mean Saturation):** This feature captures the intensity of colors in the image. Night shots tend to be less colorful or even monochromatic, while daytime shots are typically rich in color. We measure this using the average of the saturation channel in the HSV color space.

4.  **`color_variety` (Hue Standard Deviation):** This feature quantifies the diversity of colors present. A high value indicates a wide palette of colors, common in complex daytime scenes, while a low value suggests the image is dominated by a few colors (e.g., the dark blue and yellow of a night street scene).

This objective feature set ensures that the classification process is entirely data-driven, repeatable, and free from human subjectivity, which was identified as a key challenge.

### 2. Rationale for Classifier Selection (KNN)

The **K-Nearest Neighbors (KNN)** algorithm was chosen for this classification task due to several key advantages:

-   **Simplicity & Interpretability:** The KNN mechanism is straightforward to understand: it classifies a new image based on the majority class of its 'neighbors' in the feature space. This makes it easy to explain and reason about.
-   **Non-Parametric:** It makes no underlying assumptions about the distribution of the data. This is highly beneficial for a small, custom dataset where the statistical properties are unknown.
-   **Effectiveness:** As demonstrated by the results, KNN can be highly effective when used with well-chosen features.

An alternative like a Decision Tree was considered but was deemed more prone to overfitting on a small dataset of only 20 samples.

### 3. Challenges Faced

The primary challenge identified early on was the **inherent subjectivity and lack of reproducibility of manual feature extraction**. Assigning a score like "Brightness (1-5)" is inconsistent and can vary from person to person, or even for the same person on different days. This introduces noise and unreliability into the model.

This challenge was overcome by **pivoting from manual to computational feature extraction**. By defining a set of objective, mathematical features, we created a robust pipeline where the feature values are determined solely by the image data itself. This makes the entire experiment more scientific and the results more reliable.

### 4. Explanation of Performance Metrics

The model achieved a **perfect accuracy of 1.0 (100%)** on the test set, as detailed in the classification report and confusion matrix.

-   **Classification Report:**
    -   **Precision (1.00 for both Day and Night):** Of all the images the model *predicted* as 'Day', 100% were correct. The same is true for 'Night'.
    -   **Recall (1.00 for both Day and Night):** Of all the images that were *actually* 'Day', the model correctly identified 100% of them. The same for 'Night'.
    -   **F1-Score (1.00):** As the harmonic mean of precision and recall, a perfect F1-score indicates flawless performance on the test set.

-   **Confusion Matrix (`confusion_matrix.png`):** The confusion matrix visually confirms this result. The values on the main diagonal show the number of correct predictions, while off-diagonal values (which are all zero in this case) would show incorrect predictions. The matrix shows that all 4 'Day' images and both 'Night' images in the test set were classified correctly.

**A Note on the Perfect Score:** While a 100% accuracy is an excellent outcome, it is important to interpret it with caution. The dataset, while unique, is very small (20 images total, with only 6 in the test set). A model's performance on such a small test set may not fully represent its performance on a larger, more varied set of unseen images. However, it strongly indicates that the chosen features are highly effective for this specific dataset.
