🏠 **Satellite Imagery–Based Property Valuation**

This project explores the problem of house price prediction by combining traditional tabular property data with satellite imagery, aiming to understand whether visual neighborhood context can improve predictive performance beyond standard machine learning approaches. The motivation behind this work is rooted in real-world real estate valuation, where factors such as greenery, neighborhood density, waterfront proximity, and urban layout strongly influence prices but are often difficult to capture using structured data alone.

The project was developed as part of the CDC × YHills initiative and follows a systematic, research-driven approach starting from data exploration, moving through strong tabular baselines, and finally experimenting with a multimodal deep learning architecture that integrates images and numerical features.

**Project Motivation and Core Idea**

Traditional house price prediction models rely heavily on structured attributes such as living area, property grade, and geographic coordinates. While these features are highly informative, they do not explicitly encode visual and environmental context, such as surrounding greenery, road layout, building density, or proximity to water bodies. Satellite imagery provides a unique opportunity to capture these latent neighborhood characteristics.

The core idea of this project is to evaluate the practical contribution of satellite images when used alongside tabular data, and to determine whether the added model complexity of a multimodal system is justified by measurable performance gains.

**Exploratory Analysis and Intuition Building**

The project begins with extensive exploratory data analysis to understand both the numerical behavior of house prices and the visual patterns present in satellite images. House prices were found to be highly right-skewed, motivating the use of logarithmic transformation to stabilize training and improve convergence.

Key tabular relationships such as the strong positive correlation between living area and price, and the monotonic increase in price with property grade confirmed that the dataset contained powerful predictors. Geospatial visualizations further revealed clear spatial clustering of high-value properties, emphasizing the importance of location-driven factors.

In parallel, visual inspection of satellite images highlighted meaningful patterns: high-priced areas frequently showed dense green cover, planned layouts, waterfront proximity, and organized residential clusters, whereas lower-priced regions were often associated with higher congestion, irregular layouts, and proximity to highways or industrial zones. These observations provided strong intuition for exploring a multimodal modeling approach.

**Modeling Strategy and Multimodal Design**

To ensure a fair and systematic evaluation, the modeling strategy followed a two stage approach.

First, multiple tabular only regression models were developed to establish a strong baseline. These included Random Forest, Ridge Regression, XGBoost, and LightGBM. Among them, LightGBM consistently achieved the lowest RMSE and highest R² score, demonstrating its effectiveness in capturing nonlinear relationships and feature interactions within structured data. This model was selected as the primary tabular benchmark.

In parallel, a multimodal deep learning architecture was designed to combine tabular data with satellite images. The tabular features were processed through a fully connected neural network to learn nonlinear interactions among property attributes. Satellite images corresponding to each property location were processed using a pretrained EfficientNetV2 model, which acted as a feature extractor to capture high-level visual cues such as greenery, density, road networks, and natural features.

The learned representations from both branches were concatenated and passed through additional dense layers to produce the final price prediction. During training, the target variable was scaled to ensure stable optimization and later inverse transformed to obtain predictions in the original price scale.

**Results and Key Findings**

Experimental results showed that the tabular only LightGBM model outperformed all multimodal configurations, achieving superior RMSE and R² scores. While the multimodal model successfully learned meaningful visual representations, it did not translate into improved predictive performance on the test set.

Further analysis revealed two key reasons for this outcome. First, the satellite images were sourced from a free public imagery API, which imposed limitations on resolution, zoom level, and visual detail. As a result, many finegrained cues relevant to property valuation such as building condition and small-scale infrastructure were not clearly distinguishable. Second, the tabular dataset already contained highly dominant predictors (living area, grade, and location), leaving limited residual variance for image features to explain.

Rather than forcing a more complex solution, the project intentionally adopts the best-performing and most reliable model, reinforcing a key real-world machine learning principle: increased complexity does not always guarantee better performance.


**Instructions to Set Up and Run the Project**

To run this project successfully, follow the steps below in the given order.

First, use the data_fetcher.py script to download satellite images for all properties in the dataset. This script uses the latitude and longitude values available in the data to fetch corresponding satellite images and store them locally. Make sure your dataset contains valid latitude and longitude columns before running this step.

After the images are downloaded, open the preprocessing.ipynb notebook. In this notebook, you only need to specify the path to your dataset file. The notebook will automatically handle data cleaning, feature preparation, and model inference. Once execution is complete, it will generate an output file containing the property id and the corresponding predicted value.

The final predictions are saved in a CSV file, which can be directly used for evaluation or submission purposes.
